"""OPTIONAL local-only real SentenceTransformer embedding eval on synthetic Gold Set.

No auto-download, API key or external service. Not run by CI.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "goldset"))
from evaluate import load, authorized_docs  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from retrieval_eval import rank_metrics  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=Path, help="Already downloaded local SentenceTransformer model directory")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--rewrite", action="store_true", help="Use frozen multi-turn rewritten query")
    args = parser.parse_args()
    if args.model_path is None:
        print("DRY RUN ONLY: supply --model-path /absolute/local/model; installs are optional and no model is loaded.")
        return 0
    if not args.model_path.is_dir():
        parser.error("--model-path must be an existing local directory (no remote model IDs).")
    if args.k <= 0:
        parser.error("--k must be positive")
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        parser.error("Install a compatible sentence-transformers version in your own environment first.")
    data = load()
    model = SentenceTransformer(str(args.model_path), local_files_only=True)
    docs = data["documents"]
    # Only synthetic documents. Index all vectors in-memory, then prefilter per case.
    vecs = model.encode([d["text"] for d in docs], normalize_embeddings=True, convert_to_numpy=True)
    id_to_idx = {d["id"]: i for i, d in enumerate(docs)}
    positive = []
    per_type = {}
    leak_count = 0
    for c in data["cases"]:
        q = c.get("rewritten_query", c["query"]) if args.rewrite else c["query"]
        qvec = model.encode([q], normalize_embeddings=True, convert_to_numpy=True)[0]
        allowed = authorized_docs(data, c)
        scores = [(d["id"], float(vecs[id_to_idx[d["id"]]] @ qvec)) for d in allowed]
        scores.sort(key=lambda x: (-x[1], x[0]))
        ranking = [docid for docid, _ in scores[:args.k]]
        if set(ranking).intersection(c.get("forbidden_doc_ids", [])):
            leak_count += 1
        if not c["expected_abstain"]:
            metric = rank_metrics(ranking, c["gold_ids"], args.k)
            positive.append(metric)
            per_type.setdefault(c["question_type"], []).append(metric["recall"])
    out = {
        "model_directory": str(args.model_path), "synthetic": True,
        "real_neural_embedding_used": True, "gold_is_human_reviewed": False,
        "k": args.k, "positive_n": len(positive), "abstain_n": 120 - len(positive),
        "recall_at_k": sum(x["recall"] for x in positive) / len(positive),
        "per_type_recall": {k: sum(v) / len(v) for k, v in per_type.items()},
        "acl_leaks": leak_count,
        "abstention_not_scored": "A cosine Top-K exists even without evidence; evaluate Evidence Gate separately.",
        "limitations": "No ANN/Milvus/ES, no RAG generation, no LLM/Ragas, pre-filtered simulated ACL; only text fixtures.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
