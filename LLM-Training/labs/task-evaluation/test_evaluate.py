"""Tests for metric denominator, confidence intervals and evidence honesty."""
import copy
import json
import math
import unittest
from pathlib import Path

from evaluate import evaluate, ratio, validate_cases, wilson_interval, score_case

HERE=Path(__file__).resolve().parent


class TaskMetricTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads((HERE/"synthetic_cases.json").read_text(encoding="utf-8"))

    def test_fixture_valid(self):
        validate_cases(self.cases)
        self.assertEqual(len(self.cases),16)

    def test_schema_rate_denominator_includes_all_cases(self):
        result=evaluate(self.cases)
        self.assertEqual(result["schema_valid_rate"]["total"],16)
        self.assertEqual(result["schema_valid_rate"]["passed"],15)

    def test_args_denominator_includes_all_tool_required(self):
        result=evaluate(self.cases)
        self.assertEqual(result["argument_accuracy_given_tool_required"]["total"],12)
        self.assertLess(result["argument_accuracy_given_tool_required"]["rate"],1)

    def test_refusal_requires_no_tool_execution(self):
        refused=[c for c in self.cases if c["id"]=="T16"][0]
        self.assertFalse(score_case(refused)["task_success"])

    def test_wrong_citation_fails_task_even_if_tool_executed(self):
        wrong=[c for c in self.cases if c["id"]=="T09"][0]
        self.assertFalse(score_case(wrong)["task_success"])

    def test_wilson_bounds(self):
        lo,hi=wilson_interval(9,16)
        self.assertLess(lo,9/16)
        self.assertGreater(hi,9/16)
        self.assertTrue(0<=lo<=hi<=1)
        self.assertIsNone(wilson_interval(0,0))

    def test_empty_denominator_is_null_not_success(self):
        self.assertIsNone(ratio(0,0)["rate"])

    def test_duplicate_id_rejected(self):
        bad=copy.deepcopy(self.cases)
        bad[-1]["id"]=bad[0]["id"]
        with self.assertRaises(ValueError):
            validate_cases(bad)

    def test_bad_untrusted_flag_type_rejected(self):
        bad=copy.deepcopy(self.cases)
        bad[0]["schema_valid"]="true"
        with self.assertRaises(ValueError):
            validate_cases(bad)

    def test_refusal_label_mismatch_rejected(self):
        bad=copy.deepcopy(self.cases)
        bad[0]["should_refuse"]=True
        with self.assertRaises(ValueError):
            validate_cases(bad)

    def test_synthetic_label_and_no_actual_latency_claim(self):
        result=evaluate(self.cases)
        self.assertEqual(result["mode"],"SYNTHETIC_LABELED_OUTCOMES_NO_MODEL")
        self.assertIn("synthetic",result["limitations"])

    def test_family_slices_reconcile(self):
        result=evaluate(self.cases)
        total=sum(x["total"] for x in result["e2e_by_family"].values())
        passed=sum(x["passed"] for x in result["e2e_by_family"].values())
        self.assertEqual(total,16)
        self.assertEqual(passed,result["end_to_end_task_success"]["passed"])


if __name__=="__main__":
    unittest.main()

