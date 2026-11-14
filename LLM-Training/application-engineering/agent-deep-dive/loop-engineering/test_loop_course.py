"""Pure contract tests; no network, LLM or external tools."""
import copy
import json
import unittest
from validate_loop_course import MANIFEST, validate


class LoopCurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_source_manifest_and_paths(self):
        self.assertEqual(validate(self.good), [])

    def test_missing_week(self):
        x = copy.deepcopy(self.good)
        x["weeks"] = [1, 2, 3]
        self.assertTrue(any("weeks" in e for e in validate(x, check_files=False)))

    def test_missing_lab(self):
        x = copy.deepcopy(self.good)
        x["labs"] = ["A", "B", "C"]
        self.assertTrue(any("labs" in e for e in validate(x, check_files=False)))

    def test_duplicate_primary_source(self):
        x = copy.deepcopy(self.good)
        x["source_urls"].append(x["source_urls"][0])
        self.assertTrue(validate(x, check_files=False))

    def test_unapproved_source_domain(self):
        x = copy.deepcopy(self.good)
        x["source_urls"][0] = "https://untrusted.invalid/test"
        self.assertTrue(any("source" in e for e in validate(x, check_files=False)))

    def test_false_production_pass_is_rejected(self):
        x = copy.deepcopy(self.good)
        x["states"]["production"] = "PASS"
        self.assertTrue(any("real-system" in e for e in validate(x, check_files=False)))

    def test_cannot_fake_learner_level(self):
        x = copy.deepcopy(self.good)
        x["states"]["learner"] = "L4"
        self.assertTrue(any("proficiency" in e for e in validate(x, check_files=False)))

    def test_cannot_replace_canonical_rubric(self):
        x = copy.deepcopy(self.good)
        x["canonical_rubric"] = "new-rubric.md"
        self.assertTrue(any("canonical" in e for e in validate(x, check_files=False)))

    def test_unknown_missing_file_is_reported(self):
        x = copy.deepcopy(self.good)
        x["required_files"].append("LLM-Training/does-not-exist.xyz")
        self.assertTrue(any("does-not-exist" in e for e in validate(x)))

if __name__ == "__main__":
    unittest.main()
