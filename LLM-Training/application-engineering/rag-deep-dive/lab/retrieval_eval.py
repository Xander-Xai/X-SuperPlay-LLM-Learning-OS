"""Deterministic RAG retrieval math lab. NO neural embedding, tokenizer, LLM or Ragas."""
from __future__ import annotations

from collections import Counter
from math import log, log2
from pathlib import Path
import json


DATA = Path(__file__).with_name("cases.json")


def load_cases(path: Path = DATA) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("synthetic") is not True:
        raise ValueError("expected synthetic schema_version=1")
    docs = data["documents"]
    ids = [d["id"] for d in docs]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate document id")
    known = set(ids)
    case_ids = set()
    for case in data["cases"]:
        if case["id"] in case_ids:
            raise ValueError("duplicate case id")
        case_ids.add(case["id"])
        if case["kind"] not in ("positive", "abstain"):
            raise ValueError("invalid case kind")
        if (case["kind"] == "positive") != bool(case["gold_ids"]):
            raise ValueError("positive requires gold; abstain requires empty gold")
        if not set(case["gold_ids"]) <= known:
            raise ValueError("missing gold document")
        if not set(case["dense_rank_ids"]) <= known:
            raise ValueError("unknown dense-stub document")
    return data


def visible(doc: dict, case: dict) -> bool:
    return (doc["tenant"] == case["tenant"] and doc["active"] and
            ("public" in doc["roles"] or case["role"] in doc["roles"]))


def authorized_docs(data: dict, case: dict) -> list[dict]:
    return [doc for doc in data["documents"] if visible(doc, case)]


def bm25(query_terms: list[str], docs: list[dict], k1: float = 1.2,
         b: float = 0.75) -> list[str]:
    """Simple standard-library BM25 on pre-tokenized Chinese toy documents."""
    if not docs or not query_terms:
        return []
    n = len(docs)
    avgdl = sum(len(d["terms"]) for d in docs) / n
    df = Counter(term for d in docs for term in set(d["terms"]))
    ranked = []
    for doc in docs:
        tf = Counter(doc["terms"])
        dl = len(doc["terms"])
        score = 0.0
        for term in set(query_terms):
            if not tf[term]:
                continue
            idf = log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * (tf[term] * (k1 + 1)) / (
                tf[term] + k1 * (1 - b + b * dl / avgdl))
        if score > 0:
            ranked.append((doc["id"], score))
    ranked.sort(key=lambda pair: (-pair[1], pair[0]))
    return [doc_id for doc_id, _ in ranked]


def rrf(rank_lists: list[list[str]], k: int = 60) -> list[str]:
    if k <= 0:
        raise ValueError("RRF k must be positive")
    scores: dict[str, float] = {}
    for ranking in rank_lists:
        for rank, doc_id in enumerate(dict.fromkeys(ranking), start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda doc_id: (-scores[doc_id], doc_id))


def retrieve(data: dict, case: dict, mode: str = "hybrid") -> list[str]:
    allowed = authorized_docs(data, case)
    allowed_ids = {d["id"] for d in allowed}
    lexical = bm25(case["query_terms"], allowed)
    # Precomputed hand-authored ranking is NOT a Dense embedding model.
    stub = [x for x in dict.fromkeys(case["dense_rank_ids"]) if x in allowed_ids]
    if mode == "bm25":
        return lexical
    if mode == "dense_stub":
        return stub
    if mode == "hybrid":
        return rrf([lexical, stub])
    raise ValueError(f"unknown retrieval mode: {mode}")


def rank_metrics(ranked: list[str], gold_ids: list[str], top_k: int = 3) -> dict:
    """Use only for positive gold. Binary relevance, unique documents."""
    if not gold_ids:
        raise ValueError("empty gold must be evaluated as an abstain case")
    gold = set(gold_ids)
    head = list(dict.fromkeys(ranked))[:top_k]
    found = gold.intersection(head)
    first = next((i for i, doc_id in enumerate(head, 1) if doc_id in gold), None)
    dcg = sum(1 / log2(i + 1) for i, x in enumerate(head, 1) if x in gold)
    ideal = sum(1 / log2(i + 1) for i in range(1, min(len(gold), top_k) + 1))
    return {
        "recall": len(found) / len(gold),
        "hit": int(bool(found)),
        "mrr": 1 / first if first else 0.0,
        "ndcg": dcg / ideal if ideal else 0.0,
    }


def evaluate(data: dict, mode: str = "hybrid", top_k: int = 3) -> dict:
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    records = []
    pos_scores = []
    abstain_correct = 0
    leaks = 0
    for case in data["cases"]:
        retrieved = retrieve(data, case, mode)[:top_k]
        allowed = {d["id"] for d in authorized_docs(data, case)}
        leaks += len([x for x in retrieved if x not in allowed])
        rec = {"id": case["id"], "kind": case["kind"], "retrieved": retrieved,
               "gold": case["gold_ids"]}
        if case["kind"] == "positive":
            m = rank_metrics(retrieved, case["gold_ids"], top_k)
            rec["metrics"] = m
            pos_scores.append(m)
        else:
            # Empty list is only an educational proxy; real Evidence Gate differs.
            rec["abstain_proxy_correct"] = not retrieved
            abstain_correct += int(not retrieved)
        records.append(rec)
    positive_n = len(pos_scores)
    abstain_n = len(records) - positive_n
    return {
        "mode": mode, "top_k": top_k, "synthetic": True,
        "positive_n": positive_n, "abstain_n": abstain_n,
        "metrics_positive_only": {
            key: sum(x[key] for x in pos_scores) / positive_n if positive_n else None
            for key in ("recall", "hit", "mrr", "ndcg")
        },
        "abstain_proxy_correct": abstain_correct,
        "abstain_proxy_accuracy": abstain_correct / abstain_n if abstain_n else None,
        "acl_leaks": leaks,
        "per_case": records,
    }


def main() -> None:
    data = load_cases()
    print(json.dumps({
        "note": "SYNTHETIC pretokenized BM25 + hand-authored dense_stub ranks; not live RAG",
        "comparisons": [evaluate(data, mode) for mode in
                        ("bm25", "dense_stub", "hybrid")],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
