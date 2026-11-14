"""Offline task-level evaluator for SYNTHETIC LLM/Agent outcomes.

This evaluates already-labeled, externally provided outcomes; it does NOT
run an LLM, verify real-world citations, execute tools, or measure latency.
It exposes denominators, different failure stages, and uncertainty.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACTIONS = {"query_inventory", "search_docs", "refuse"}
REQUIRED = {
    "id", "split", "family", "expected_action", "predicted_action",
    "schema_valid", "expected_id", "predicted_id", "tool_succeeded",
    "citation_required", "citation_supported", "should_refuse", "latency_ms",
}


def validate_cases(cases: list[dict]) -> None:
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    ids = set()
    for i, c in enumerate(cases):
        if not isinstance(c, dict) or set(c) != REQUIRED:
            raise ValueError(f"Case {i}: expected exactly {sorted(REQUIRED)}")
        if not isinstance(c["id"], str) or c["id"] in ids:
            raise ValueError(f"Case {i}: duplicate or invalid id")
        ids.add(c["id"])
        if c["split"] != "test" or not isinstance(c["family"], str) or not c["family"]:
            raise ValueError(f"Case {i}: only labeled test cases supported")
        if c["expected_action"] not in ACTIONS or c["predicted_action"] not in ACTIONS:
            raise ValueError(f"Case {i}: unknown action")
        if c["should_refuse"] != (c["expected_action"] == "refuse"):
            raise ValueError(f"Case {i}: refusal label conflict")
        for flag in ("schema_valid","tool_succeeded","citation_required","citation_supported","should_refuse"):
            if type(c[flag]) is not bool:
                raise ValueError(f"Case {i}: {flag} must be boolean")
        if not isinstance(c["latency_ms"], (int, float)) or type(c["latency_ms"]) is bool \
                or not math.isfinite(c["latency_ms"]) or c["latency_ms"] < 0:
            raise ValueError(f"Case {i}: invalid illustrative latency")
        if c["expected_action"] == "refuse":
            if c["expected_id"] is not None or c["citation_required"]:
                raise ValueError(f"Case {i}: refusal must have no expected argument/citation")
        elif not isinstance(c["expected_id"], str) or not c["expected_id"]:
            raise ValueError(f"Case {i}: tool target requires expected_id")
        if c["predicted_id"] is not None and not isinstance(c["predicted_id"], str):
            raise ValueError(f"Case {i}: invalid predicted_id")


def score_case(c: dict) -> dict[str, bool]:
    selection = c["predicted_action"] == c["expected_action"]
    if c["should_refuse"]:
        # A refusal should not invoke tools or leak a source/citation.
        complete = selection and not c["tool_succeeded"] and c["predicted_id"] is None
        return {"tool_selection": selection, "args_correct": False,
                "execution": False, "citation": False, "refusal": complete,
                "task_success": complete}
    arguments = selection and c["schema_valid"] and c["predicted_id"] == c["expected_id"]
    execution = arguments and c["tool_succeeded"]
    citation = bool(c["citation_supported"]) if c["citation_required"] else True
    success = execution and citation
    return {"tool_selection": selection, "args_correct": arguments,
            "execution": execution, "citation": citation,
            "refusal": False, "task_success": success}


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float] | None:
    if trials == 0:
        return None
    p = successes / trials
    denom = 1 + z*z/trials
    center = (p + z*z/(2*trials)) / denom
    radius = z * math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / denom
    return max(0, center-radius), min(1, center+radius)


def ratio(successes: int, trials: int) -> dict:
    return {"passed": successes, "total": trials, "rate": successes/trials if trials else None}


def evaluate(cases: list[dict]) -> dict:
    validate_cases(cases)
    rows = [score_case(c) for c in cases]
    tools = [i for i,c in enumerate(cases) if not c["should_refuse"]]
    citations = [i for i,c in enumerate(cases) if not c["should_refuse"] and c["citation_required"]]
    refusals = [i for i,c in enumerate(cases) if c["should_refuse"]]
    count = lambda indices,key: sum(rows[i][key] for i in indices)
    all_idx=list(range(len(cases)))
    passed=count(all_idx,"task_success")
    families=sorted({c["family"] for c in cases})
    return {
        "mode": "SYNTHETIC_LABELED_OUTCOMES_NO_MODEL",
        "sample_size": len(cases),
        "tool_selection_accuracy": ratio(count(all_idx, "tool_selection"), len(cases)),
        "schema_valid_rate": ratio(sum(c["schema_valid"] for c in cases), len(cases)),
        "argument_accuracy_given_tool_required": ratio(count(tools,"args_correct"), len(tools)),
        "tool_execution_success_given_tool_required": ratio(count(tools,"execution"), len(tools)),
        "citation_support_given_citation_required": ratio(count(citations,"citation"),len(citations)),
        "correct_refusal_given_refusal_required": ratio(count(refusals,"refusal"), len(refusals)),
        "end_to_end_task_success": ratio(passed,len(cases)),
        "e2e_wilson_95pct": wilson_interval(passed,len(cases)),
        "e2e_by_family": {
            fam: ratio(sum(rows[i]["task_success"] for i,c in enumerate(cases) if c["family"] == fam),
                       sum(c["family"] == fam for c in cases)) for fam in families
        },
        "failure_ids": [c["id"] for c,r in zip(cases,rows) if not r["task_success"]],
        "limitations": "Outcomes/latencies are synthetic labels. No actual model, judge, real traffic or SLA benchmark.",
    }


def main():
    cases=json.loads((HERE/"synthetic_cases.json").read_text(encoding="utf-8"))
    print(json.dumps(evaluate(cases),ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()

