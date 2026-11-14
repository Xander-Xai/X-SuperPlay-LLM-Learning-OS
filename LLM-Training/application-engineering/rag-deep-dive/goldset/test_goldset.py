"""Gold Set contract, negative cases and deterministic benchmark (no model/network)."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from evaluate import load, retrieve, evaluate


class GoldSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()

    def test_all_120_cases_and_80_docs(self):
        self.assertEqual(len(self.data["cases"]), 120)
        self.assertEqual(len(self.data["documents"]), 80)
        self.assertEqual(sum(self.data["expected_counts"].values()), 120)

    def test_buckets_have_independent_denominators(self):
        r = evaluate(self.data)
        self.assertEqual(r["positive_n"], 105)
        self.assertEqual(r["abstain_n"], 15)
        self.assertEqual(r["acl_leaks"], 0)
        self.assertIsNone(r["buckets"]["acl"]["recall_at_k"])
        self.assertIsNone(r["buckets"]["no_answer"]["mrr_at_k"])

    def test_rewrite_changes_multiturn_retrieval(self):
        case = next(x for x in self.data["cases"] if x["question_type"] == "multi_turn")
        before = retrieve(self.data, case, "bm25")[:1]
        after = retrieve(self.data, case, "rewrite_bm25")[:1]
        self.assertNotEqual(before, after)
        self.assertEqual(after[0], case["gold_ids"][0])

    def test_pre_filter_prevents_cross_tenant_and_stale(self):
        for case in self.data["cases"]:
            if case["question_type"] == "acl":
                for mode in ("bm25", "rewrite_bm25", "multiquery_rrf"):
                    self.assertFalse(set(retrieve(self.data, case, mode)) & set(case["forbidden_doc_ids"]))

    def test_all_modes_have_no_leaks(self):
        for mode in ("bm25", "rewrite_bm25", "multiquery_rrf"):
            self.assertEqual(evaluate(self.data, mode)["acl_leaks"], 0)

    def _validate_bad(self, mutate, msg: str):
        data = deepcopy(self.data)
        mutate(data)
        with TemporaryDirectory() as td:
            path = Path(td) / "bad.json"
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, msg):
                load(path)

    def test_reject_missing_gold(self):
        self._validate_bad(lambda d: d["cases"][0].update(gold_ids=[]), "abstain/gold mismatch")

    def test_reject_fake_source_quote(self):
        self._validate_bad(lambda d: d["cases"][0]["gold_source_spans"][0].update(quote="不存在的原文"), "invalid source quote")

    def test_reject_hidden_gold(self):
        self._validate_bad(lambda d: d["cases"][0].update(gold_ids=["XP01"]), "illegal gold document")

    def test_reject_duplicate_document(self):
        self._validate_bad(lambda d: d["documents"].append(d["documents"][0]), "80 synthetic")

    def test_reject_fake_human_review(self):
        self._validate_bad(lambda d: d["cases"][0].update(annotation_review="HUMAN_REVIEWED"), "unsupported human review claim")

    def test_invalid_k_and_mode(self):
        with self.assertRaises(ValueError):
            evaluate(self.data, top_k=0)
        with self.assertRaises(ValueError):
            retrieve(self.data, self.data["cases"][0], "foobar")


if __name__ == "__main__":
    unittest.main()
