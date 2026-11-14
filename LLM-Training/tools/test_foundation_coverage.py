"""Coverage and actual contradiction guard tests; all standard library."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_foundation_coverage import load, validate, VIEW, consistency_wording_issues


class FoundationCoverageContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()
        cls.view = VIEW.read_text(encoding="utf-8")

    def test_current_coverage_and_docs_are_consistent(self):
        self.assertEqual(validate(self.data, self.view), [])

    def test_all_twelve_modules_and_five_plus_each(self):
        self.assertEqual({x["module"] for x in self.data["topics"]},
                         {f"M{i:02d}" for i in range(1, 13)})
        self.assertGreaterEqual(len(self.data["topics"]), 75)

    def test_math_prob_info_and_tokenizer_are_locatable(self):
        titles = " ".join(x["title"] for x in self.data["topics"])
        for key in ("最大似然", "信息熵", "WordPiece", "因果", "Encoder-only"):
            self.assertIn(key, titles)

    def test_duplicate_id_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["topics"].append(copy.deepcopy(copy_data["topics"][0]))
        self.assertTrue(any("duplicate" in s for s in validate(copy_data, read_repo_docs=False)))

    def test_missing_topic_reference_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["topics"][0]["guide"] = "LLM-Training/DOES_NOT_EXIST.md"
        self.assertTrue(any("broken guide" in s for s in validate(copy_data, read_repo_docs=False)))

    def test_unsafe_path_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["topics"][0]["practice"] = "../../etc/passwd"
        self.assertTrue(any("broken practice" in s for s in validate(copy_data, read_repo_docs=False)))

    def test_false_practice_claim_rejected(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["topics"][0]["practice_evidence"] = "GPU_TRAINED"
        self.assertTrue(any("false practice" in s for s in validate(copy_data, read_repo_docs=False)))

    def test_source_must_be_https(self):
        copy_data = copy.deepcopy(self.data)
        copy_data["topics"][0]["official_source"] = "http://untrusted"
        self.assertTrue(any("expected HTTPS" in s for s in validate(copy_data, read_repo_docs=False)))

    def test_mismatched_markdown_is_rejected(self):
        broken = self.view.replace("| M01.01 |", "| BROKEN.01 |")
        self.assertTrue(any("not 1:1" in s for s in validate(self.data, broken, read_repo_docs=False)))

    def test_current_wording_contradictions_are_blocked(self):
        self.assertTrue(consistency_wording_issues({
            "LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md":
                "**L3 迁移** and **L4 生产**"
        }))
        self.assertTrue(consistency_wording_issues({
            "README.md": "机器索引（12 模块 / 18 需求 / 20 来源）"
        }))

    def test_dropped_essential_concept_is_rejected(self):
        copy_data = copy.deepcopy(self.data)
        next(row for row in copy_data["topics"] if row["id"] == "M02.02")["title"] = "unknown"
        self.assertTrue(any("essential concept missing" in s for s in validate(copy_data, read_repo_docs=False)))


if __name__ == "__main__":
    unittest.main()
