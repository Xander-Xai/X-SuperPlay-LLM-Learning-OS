"""120-case synthetic RAG retrieval curriculum benchmark. No external modules or model API."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))
from retrieval_eval import bm25, rank_metrics, rrf  # noqa: E402

DATA = Path(__file__).with_name("goldset.json")


def load(path: Path = DATA) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("synthetic") is not True:
        raise ValueError("invalid synthetic dataset schema")
    if data.get("annotation_status") != "TEMPLATE_GENERATED_NOT_HUMAN_VERIFIED":
        raise ValueError("missing synthetic labeling disclaimer")
    docs = data.get("documents", [])
    cases = data.get("cases", [])
    if len(docs) != 80 or len(cases) != 120:
        raise ValueError("expected 80 synthetic documents and 120 cases")
    all_docs = {d["id"]: d for d in docs}
    if len(all_docs) != len(docs):
        raise ValueError("duplicate document id")
    case_ids = [c["case_id"] for c in cases]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("duplicate case id")
    counts = Counter(c["question_type"] for c in cases)
    if counts != data["expected_counts"]:
        raise ValueError("question bucket counts differ from manifest")
    for c in cases:
        gold = c["gold_ids"]
        if len(set(gold)) != len(gold):
            raise ValueError(f"{c['case_id']}: duplicate gold id")
        if bool(gold) == c["expected_abstain"]:
            raise ValueError(f"{c['case_id']}: abstain/gold mismatch")
        if c["annotation_review"] != "SYNTHETIC_TEMPLATE_NOT_HUMAN_REVIEWED":
            raise ValueError(f"{c['case_id']}: unsupported human review claim")
        if not isinstance(c["query_terms"], list):
            raise ValueError(f"{c['case_id']}: missing pretokenized query")
        for source in gold:
            if source not in all_docs:
                raise ValueError(f"{c['case_id']}: unknown gold")
            doc = all_docs[source]
            if doc["tenant"] != c["tenant"] or not doc["active"]:
                raise ValueError(f"{c['case_id']}: illegal gold document")
            if "public" not in doc["roles"] and c["role"] not in doc["roles"]:
                raise ValueError(f"{c['case_id']}: unauthorized gold document")
        spans = c["gold_source_spans"]
        if sorted(s["source_id"] for s in spans) != sorted(gold):
            raise ValueError(f"{c['case_id']}: source spans do not match gold")
        for span in spans:
            doc = all_docs[span["source_id"]]
            if not span.get("quote") or span["quote"] not in doc["text"]:
                raise ValueError(f"{c['case_id']}: fabricated/invalid source quote")
            if span["page"] != doc["page"]:
                raise ValueError(f"{c['case_id']}: page mismatch")
        for x in c.get("forbidden_doc_ids", []):
            if x not in all_docs:
                raise ValueError(f"{c['case_id']}: unknown forbidden id")
            doc = all_docs[x]
            if doc["tenant"] == c["tenant"] and doc["active"] and (
                "public" in doc["roles"] or c["role"] in doc["roles"]
            ):
                raise ValueError(f"{c['case_id']}: forbidden document is authorized")
    return data


def authorized_docs(data: dict, case: dict) -> list[dict]:
    return [
        d for d in data["documents"]
        if d["tenant"] == case["tenant"] and d["active"]
        and ("public" in d["roles"] or case["role"] in d["roles"])
    ]


def retrieve(data: dict, case: dict, mode: str = "bm25") -> list[str]:
    docs = authorized_docs(data, case)
    original = bm25(case["query_terms"], docs)
    if mode == "bm25":
        return original
    expanded = bm25(case.get("query_terms_rewritten", case["query_terms"]), docs)
    if mode == "rewrite_bm25":
        return expanded
    if mode == "multiquery_rrf":
        return rrf([original, expanded])
    raise ValueError("Unknown mode. Use bm25, rewrite_bm25 or multiquery_rrf.")


def evaluate(data: dict, mode: str = "bm25", top_k: int = 5) -> dict:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    counts = Counter()
    buckets: dict[str, dict] = {}
    failed = []
    for case in data["cases"]:
        ranked = retrieve(data, case, mode)[:top_k]
        allowed = {d["id"] for d in authorized_docs(data, case)}
        if set(ranked) - allowed or set(ranked).intersection(case.get("forbidden_doc_ids", [])):
            counts["acl_leaks"] += 1
        category = case["question_type"]
        bucket = buckets.setdefault(category, {
            "positive_n": 0, "abstain_n": 0, "recall_sum": 0.0,
            "hit_sum": 0.0, "mrr_sum": 0.0, "ndcg_sum": 0.0,
            "abstain_empty_proxy": 0,
        })
        if case["expected_abstain"]:
            counts["abstain_n"] += 1
            bucket["abstain_n"] += 1
            bucket["abstain_empty_proxy"] += int(not ranked)
            if ranked:
                failed.append({"case_id": case["case_id"], "failure": "nonempty_on_abstain", "top_ids": ranked})
        else:
            counts["positive_n"] += 1
            bucket["positive_n"] += 1
            metric = rank_metrics(ranked, case["gold_ids"], top_k)
            for key in ("recall", "hit", "mrr", "ndcg"):
                bucket[key + "_sum"] += metric[key]
            if metric["recall"] < 1:
                failed.append({"case_id": case["case_id"], "failure": "missing_gold_in_top_k",
                               "gold": case["gold_ids"], "top_ids": ranked})
    if counts["positive_n"] + counts["abstain_n"] != 120:
        raise ValueError("denominator mismatch")
    for bucket in buckets.values():
        n = bucket["positive_n"]
        for key in ("recall", "hit", "mrr", "ndcg"):
            bucket[key + "_at_k"] = (bucket.pop(key + "_sum") / n) if n else None
    positive_n = counts["positive_n"]
    return {
        "mode": mode, "k": top_k, "synthetic": True,
        "model_or_embedding_used": False, "official_ragas_used": False,
        "positive_n": positive_n, "abstain_n": counts["abstain_n"],
        "acl_leaks": counts["acl_leaks"],
        "macro_recall_at_k": sum(b["recall_at_k"] * b["positive_n"] for b in buckets.values()
                                 if b["positive_n"]) / positive_n if positive_n else None,
        "abstain_empty_proxy": sum(b["abstain_empty_proxy"] for b in buckets.values()),
        "buckets": buckets, "failure_examples": failed[:12],
        "warning": "Synthetic templated gold; no OCR, real ANN, neural embeddings, answer generation or human annotations. Empty result is not a validated answer gate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("bm25", "rewrite_bm25", "multiquery_rrf"), default="bm25")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(evaluate(load(), args.mode, args.k), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
