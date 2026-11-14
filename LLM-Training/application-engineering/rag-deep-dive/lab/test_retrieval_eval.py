"""Negative tests for the deterministic RAG teaching lab (stdlib only)."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from retrieval_eval import (
    load_cases, authorized_docs, bm25, rrf, rank_metrics, retrieve, evaluate,
)


class RetrievalLabTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_cases()

    def case(self, ident):
        return next(c for c in self.data["cases"] if c["id"] == ident)

    def test_fixture_counts_and_boundary(self):
        self.assertEqual(len(self.data["documents"]), 6)
        self.assertEqual(len(self.data["cases"]), 10)
        self.assertTrue(self.data["synthetic"])

    def test_bm25_lexical_candidate(self):
        self.assertEqual(bm25(["烟酰胺"],
                              authorized_docs(self.data, self.case("q2")))[0], "d1")
        self.assertEqual(bm25(["完全未知术语"],
                              authorized_docs(self.data, self.case("q9"))), [])

    def test_rrf_rank_not_score(self):
        self.assertEqual(rrf([["a", "b"], ["b", "a"]]), ["a", "b"])
        self.assertEqual(rrf([["a"], ["b", "b", "a"]]), ["a", "b"])
        with self.assertRaises(ValueError):
            rrf([["a"]], k=0)

    def test_acl_tenant_before_retrieval(self):
        for ident, forbidden in [("q6", "d3"), ("q7", "d4"),
                                 ("q8", "d2"), ("q10", "d1")]:
            case = self.case(ident)
            for mode in ("bm25", "dense_stub", "hybrid"):
                self.assertNotIn(forbidden, retrieve(self.data, case, mode))

    def test_legal_role_can_read_authorized_doc(self):
        self.assertIn("d4", retrieve(self.data, self.case("q4"), "hybrid"))
        self.assertNotIn("d4", retrieve(self.data, self.case("q7"), "hybrid"))

    def test_positive_metrics_not_abstain(self):
        res = evaluate(self.data, "hybrid")
        self.assertEqual(res["positive_n"], 5)
        self.assertEqual(res["abstain_n"], 5)
        self.assertEqual(res["acl_leaks"], 0)
        self.assertEqual(res["abstain_proxy_correct"], 5)
        self.assertGreater(res["metrics_positive_only"]["recall"], 0)

    def test_all_gold_recall_not_hit(self):
        m = rank_metrics(["a", "x"], ["a", "b"], 2)
        self.assertEqual(m["recall"], 0.5)
        self.assertEqual(m["hit"], 1)
        self.assertEqual(m["mrr"], 1.0)
        with self.assertRaises(ValueError):
            rank_metrics(["a"], [])

    def test_case_with_frozen_wrong_ranking(self):
        d = deepcopy(self.data)
        q = next(c for c in d["cases"] if c["id"] == "q1")
        q["dense_rank_ids"] = ["d5"]
        result = evaluate(d, "dense_stub")
        self.assertLess(result["metrics_positive_only"]["recall"], 1.0)

    def test_cannot_smuggle_expired_or_cross_tenant_via_dense_stub(self):
        d = deepcopy(self.data)
        q = next(c for c in d["cases"] if c["id"] == "q2")
        q["dense_rank_ids"] = ["d2", "d3", "d1"]
        result = retrieve(d, q, "hybrid")
        self.assertNotIn("d2", result)
        self.assertNotIn("d3", result)

    def test_invalid_mode_and_topk(self):
        with self.assertRaises(ValueError):
            retrieve(self.data, self.case("q1"), mode="not-a-mode")
        with self.assertRaises(ValueError):
            evaluate(self.data, top_k=0)

    def test_gold_missing_rejected_by_loader(self):
        d = deepcopy(self.data)
        d["cases"][0]["gold_ids"] = []
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "positive requires gold"):
                load_cases(path)

    def test_unknown_dense_document_rejected_by_loader(self):
        d = deepcopy(self.data)
        d["cases"][0]["dense_rank_ids"].append("unknown-document")
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown dense-stub"):
                load_cases(path)

    def test_injection_document_is_only_data(self):
        case = self.case("q5")
        self.assertIn("d6", retrieve(self.data, case))
        self.assertEqual(self.data["documents"][-1]["id"], "d6")


if __name__ == "__main__":
    unittest.main()
