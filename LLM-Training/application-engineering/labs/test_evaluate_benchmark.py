"""Frozen RAG/Agent regression suite, including deliberate negative mutations."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from evaluate_benchmark import (load_cases, validate_cases, evaluate,
                                evaluate_retrieval, execute_tool_case)
from pipeline import load_documents

HERE = Path(__file__).resolve().parent


class FrozenApplicationBenchmark(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases()
        self.docs = load_documents()

    def test_schema_and_references(self):
        self.assertEqual(validate_cases(self.cases, self.docs), [])

    def test_case_count_and_explicit_denominators(self):
        report = evaluate(self.cases, self.docs)
        self.assertEqual(report["suite"], {"retrieval": 10, "tool": 9, "all": 19})
        self.assertEqual(report["retrieval"]["positive_retrieval_count"], 5)
        self.assertEqual(report["retrieval"]["abstain_total"], 5)

    def test_known_fixture_passes_with_recall_and_abstention_separate(self):
        report = evaluate(self.cases, self.docs)
        self.assertTrue(report["all_pass"])
        self.assertEqual(report["retrieval"]["mean_recall_at_k"], 1.0)
        self.assertEqual(report["retrieval"]["abstain_correct"], 5)
        self.assertEqual(report["retrieval"]["unauthorized_or_forbidden_case_count"], 0)
        self.assertEqual(report["tool"]["case_pass"], 9)

    def test_each_case_has_independent_id_and_failure_family(self):
        all_cases = self.cases["retrieval_cases"] + self.cases["tool_cases"]
        self.assertEqual(len({x["id"] for x in all_cases}), 19)
        self.assertTrue(all(isinstance(x["family"], str) for x in all_cases))

    def test_duplicate_case_id_is_rejected(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][1]["id"] = "R01"
        self.assertTrue(any("duplicate" in x for x in validate_cases(broken, self.docs)))

    def test_unknown_gold_is_rejected(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][0]["gold_ids"] = ["not-a-doc"]
        self.assertTrue(any("unknown document" in x for x in validate_cases(broken, self.docs)))

    def test_inaccessible_gold_is_rejected(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][0]["gold_ids"] = ["a-secret"]
        self.assertTrue(any("unavailable under policy" in x for x in validate_cases(broken, self.docs)))

    def test_gold_and_abstain_cannot_conflict(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][0]["should_abstain"] = True
        self.assertTrue(any("ambiguous" in x for x in validate_cases(broken, self.docs)))

    def test_zero_budget_on_answerable_case_is_regression(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][0]["budget"] = 0
        report = evaluate(broken, self.docs)
        self.assertFalse(report["all_pass"])
        self.assertIn("R01", report["failed_ids"])

    def test_false_abstain_is_regression(self):
        broken = copy.deepcopy(self.cases)
        broken["retrieval_cases"][3]["query"] = "product a stock"
        report = evaluate(broken, self.docs)
        self.assertFalse(report["all_pass"])
        self.assertIn("R04", report["failed_ids"])

    def test_wrong_tool_side_effect_is_regression(self):
        broken = copy.deepcopy(self.cases)
        broken["tool_cases"][3]["expected_remaining"] = 8
        report = evaluate(broken, self.docs)
        self.assertFalse(report["all_pass"])
        self.assertIn("T04", report["failed_ids"])

    def test_invalid_action_rejected(self):
        broken = copy.deepcopy(self.cases)
        broken["tool_cases"][3]["action"] = "destroy"
        self.assertTrue(any("unsupported action" in x for x in validate_cases(broken, self.docs)))

    def test_untrusted_external_text_not_executed_by_benchmark(self):
        report = evaluate(self.cases, self.docs)
        row = next(x for x in report["case_details"]["retrieval"] if x["id"] == "R09")
        self.assertIn("a-untrusted", row["selected_doc_ids"])
        self.assertNotIn("R09", report["failed_ids"])
        self.assertNotIn("task_success", report)

    def test_report_is_json_serializable(self):
        result = json.dumps(evaluate(self.cases, self.docs), ensure_ascii=False)
        self.assertIn("SYNTHETIC_DETERMINISTIC_NO_LLM_NO_RAGAS", result)

    def test_cli_can_execute_without_external_dependencies(self):
        output = subprocess.run(
            [sys.executable, str(HERE / "evaluate_benchmark.py")],
            capture_output=True, text=True, check=True)
        self.assertIn('"all_pass": true', output.stdout)
        self.assertIn('"retrieval": 10', output.stdout)


if __name__ == "__main__":
    unittest.main()
