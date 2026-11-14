"""Offline negative/contract tests for Agent course manifest."""
import copy
import json
import unittest
from pathlib import Path
from validate_agent_curriculum import MANIFEST, validate_manifest


class AgentCurriculumContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_base_manifest_and_files(self):
        self.assertEqual(validate_manifest(self.valid), [])

    def test_missing_module_detected(self):
        data = copy.deepcopy(self.valid)
        data["modules"].pop()
        self.assertTrue(any("A1..A8" in x for x in validate_manifest(data, check_files=False)))

    def test_duplicate_module_detected(self):
        data = copy.deepcopy(self.valid)
        data["modules"][4]["id"] = "A3"
        self.assertTrue(validate_manifest(data, check_files=False))

    def test_day_plan_missing_detected(self):
        data = copy.deepcopy(self.valid)
        data["day_plans"] = ["Day 1", "Day 3"]
        self.assertTrue(any("Day" in x for x in validate_manifest(data, check_files=False)))

    def test_untrusted_source_rejected(self):
        data = copy.deepcopy(self.valid)
        data["resources"][0] = "https://fake-blog.example/course"
        self.assertTrue(any("source" in x for x in validate_manifest(data, check_files=False)))

    def test_duplicates_sources_rejected(self):
        data = copy.deepcopy(self.valid)
        data["resources"][0] = data["resources"][1]
        self.assertTrue(any("Ten distinct" in x for x in validate_manifest(data, check_files=False)))

    def test_claiming_live_run_rejected(self):
        data = copy.deepcopy(self.valid)
        data["states"]["provider"] = "PASS"
        self.assertTrue(any("pass claim" in x for x in validate_manifest(data, check_files=False)))

    def test_canonical_rubric_is_not_replaced(self):
        data = copy.deepcopy(self.valid)
        data["canonical_rubric"] = "new-rubric.md"
        self.assertTrue(any("rubric" in x for x in validate_manifest(data, check_files=False)))


if __name__ == "__main__":
    unittest.main()
