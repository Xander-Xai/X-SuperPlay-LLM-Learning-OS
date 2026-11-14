"""Frozen offline retrieval + scripted tool regression evaluation.

This is NOT Ragas, a model-based faithfulness judge, a live Agent, or production E2E.
All scores have explicit denominators and negative cases remain in the suite.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pipeline import (Principal, ToolCall, ToolError, PolicyError,
                      ToolGateway, load_documents, recall_at_k,
                      scripted_agent, select_context)

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "benchmark_cases.json"


def load_cases(path: Path = FIXTURES) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_cases(data: dict, documents: list | None = None) -> list[str]:
    docs = load_documents() if documents is None else documents
    known = {doc.id for doc in docs}
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("unsupported benchmark schema version")
    retrieval = data.get("retrieval_cases")
    tools = data.get("tool_cases")
    if not isinstance(retrieval, list) or not isinstance(tools, list):
        return errors + ["retrieval_cases and tool_cases must be lists"]
    if len(retrieval) < 8 or len(tools) < 7:
        errors.append("too few positive/negative benchmark cases")
    all_ids = [x.get("id") for x in retrieval + tools]
    if len(all_ids) != len(set(all_ids)):
        errors.append("duplicate benchmark case ID")
    for case in retrieval:
        ident = case.get("id", "?")
        gold = case.get("gold_ids")
        forbidden = case.get("forbidden_ids")
        if (not isinstance(gold, list) or not isinstance(forbidden, list)
                or not all(isinstance(s, str) for s in gold + forbidden)):
            errors.append(f"{ident}: invalid gold/forbidden ID list")
            continue
        if not set(gold + forbidden).issubset(known):
            errors.append(f"{ident}: unknown document ID")
        if set(gold).intersection(forbidden):
            errors.append(f"{ident}: gold conflicts with forbidden")
        if case.get("should_abstain") is not (len(gold) == 0):
            errors.append(f"{ident}: ambiguous abstain/gold contract")
        if (not isinstance(case.get("k"), int) or case["k"] < 1 or
                not isinstance(case.get("budget"), int) or case["budget"] < 0):
            errors.append(f"{ident}: invalid k/budget")
        principal = Principal(str(case.get("tenant")), str(case.get("role")))
        allowed = {d.id for d in docs if d.active and d.tenant == principal.tenant
                   and principal.role in d.allowed_roles}
        if not set(gold).issubset(allowed):
            errors.append(f"{ident}: gold document unavailable under policy")
        if not isinstance(case.get("query"), str) or not case["query"].strip():
            errors.append(f"{ident}: missing query")
        if "family" not in case:
            errors.append(f"{ident}: missing failure family")
    valid_actions = {"lookup", "reserve", "replay", "conflict", "unknown", "step_limit"}
    for case in tools:
        ident = case.get("id", "?")
        if case.get("action") not in valid_actions:
            errors.append(f"{ident}: unsupported action")
        if case.get("expected") not in {"ok", "PolicyError", "ToolError"}:
            errors.append(f"{ident}: invalid expected outcome")
        if case.get("expected_remaining") not in (8, 6):
            errors.append(f"{ident}: missing expected inventory effect")
        for key in ("tenant", "role", "actor", "family"):
            if not isinstance(case.get(key), str) or not case[key]:
                errors.append(f"{ident}: missing {key}")
    return errors


def evaluate_retrieval(cases: list[dict], docs: list) -> tuple[list[dict], dict]:
    records: list[dict] = []
    recall_values = []
    abstain_results = []
    violations = 0
    for case in cases:
        who = Principal(case["tenant"], case["role"])
        selected, manifest = select_context(docs, who, case["query"],
                                            case["budget"], limit=case["k"])
        ids = [doc.id for doc in selected]
        valid = {d.id for d in docs if d.active and d.tenant == who.tenant
                 and who.role in d.allowed_roles}
        leaked = set(ids) - valid
        prohibited = set(ids).intersection(case["forbidden_ids"])
        violations += int(bool(leaked or prohibited))
        gold = set(case["gold_ids"])
        if gold:
            score = recall_at_k(ids, gold, case["k"])
            recall_values.append(score)
            expectation_met = score == 1.0
        else:
            score = None
            expectation_met = not ids
            abstain_results.append(expectation_met)
        passed = expectation_met and not leaked and not prohibited
        records.append({
            "id": case["id"], "family": case["family"], "pass": passed,
            "selected_doc_ids": ids, "gold_doc_ids": sorted(gold),
            "recall_at_k": score, "should_abstain": case["should_abstain"],
            "actual_abstain": not ids, "unauthorized_ids": sorted(leaked),
            "prohibited_ids": sorted(prohibited),
            "used_proxy_units": manifest["used_proxy_units"],
        })
    denominator = len(cases)
    return records, {
        "case_pass": sum(bool(r["pass"]) for r in records),
        "case_total": denominator,
        "positive_retrieval_count": len(recall_values),
        "mean_recall_at_k": sum(recall_values) / len(recall_values) if recall_values else None,
        "abstain_correct": sum(abstain_results),
        "abstain_total": len(abstain_results),
        "unauthorized_or_forbidden_case_count": violations,
    }


def execute_tool_case(case: dict) -> dict:
    who = Principal(case["tenant"], case["role"], case["actor"])
    gateway = ToolGateway()
    basic = ToolCall("reserve_stock", {"product_id": "product-a", "units": 2},
                     key="benchmark-key")
    try:
        if case["action"] == "lookup":
            result = gateway.execute(who, ToolCall(
                "lookup_stock", {"product_id": "product-a"}))
        elif case["action"] == "reserve":
            result = gateway.execute(who, basic, approved=case.get("approved", False))
        elif case["action"] == "replay":
            first = gateway.execute(who, basic, approved=True)
            result = gateway.execute(who, basic, approved=True)
            if first != result or gateway.trace.events[-1]["status"] != "replayed":
                raise AssertionError("duplicate write was not a safe replay")
        elif case["action"] == "conflict":
            gateway.execute(who, basic, approved=True)
            result = gateway.execute(who, ToolCall("reserve_stock", {
                "product_id": "product-a", "units": 3}, key="benchmark-key"), approved=True)
        elif case["action"] == "unknown":
            result = gateway.execute(who, ToolCall("delete_account", {}))
        elif case["action"] == "step_limit":
            result = scripted_agent(gateway, who, [
                ToolCall("lookup_stock", {"product_id": "product-a"}),
                ToolCall("lookup_stock", {"product_id": "product-b"})], max_steps=1)
        else:
            raise ValueError("invalid action should have been caught by schema check")
        outcome = "ok"
    except (PolicyError, ToolError) as exc:
        result = {"error_type": type(exc).__name__}
        outcome = type(exc).__name__
    return {
        "id": case["id"], "family": case["family"],
        "pass": outcome == case["expected"] and gateway.stock["product-a"] ==
                case["expected_remaining"],
        "expected_outcome": case["expected"], "actual_outcome": outcome,
        "expected_remaining": case["expected_remaining"],
        "actual_remaining": gateway.stock["product-a"],
        "trace_event_count": len(gateway.trace.events),
    }


def evaluate(data: dict | None = None, docs: list | None = None) -> dict:
    fixtures = load_cases() if data is None else data
    documents = load_documents() if docs is None else docs
    problems = validate_cases(fixtures, documents)
    if problems:
        raise ValueError("invalid frozen benchmark: " + "; ".join(problems))
    rag_rows, rag_summary = evaluate_retrieval(fixtures["retrieval_cases"], documents)
    tool_rows = [execute_tool_case(x) for x in fixtures["tool_cases"]]
    failed_ids = [x["id"] for x in rag_rows + tool_rows if not x["pass"]]
    by_family = Counter(x["family"] for x in rag_rows + tool_rows if not x["pass"])
    return {
        "status": "SYNTHETIC_DETERMINISTIC_NO_LLM_NO_RAGAS",
        "suite": {"retrieval": len(rag_rows), "tool": len(tool_rows),
                  "all": len(rag_rows) + len(tool_rows)},
        "retrieval": rag_summary,
        "tool": {"case_pass": sum(bool(x["pass"]) for x in tool_rows),
                 "case_total": len(tool_rows)},
        "failed_ids": failed_ids,
        "failed_families": dict(by_family),
        "case_details": {"retrieval": rag_rows, "tool": tool_rows},
        "all_pass": not failed_ids,
    }


def main() -> int:
    report = evaluate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return int(not report["all_pass"])


if __name__ == "__main__":
    raise SystemExit(main())
