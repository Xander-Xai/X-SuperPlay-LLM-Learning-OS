"""Standard-library contract tests; requires no torch or model downloads."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_learning_index import load_index, validate  # noqa: E402
from route_learning import select, pretty  # noqa: E402


class IndexContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_index()

    def test_index_valid(self):
        self.assertEqual(validate(self.catalog), [])

    def test_modules_complete(self):
        self.assertEqual(
            {m["id"] for m in self.catalog["modules"]},
            {f"M{i:02d}" for i in range(1, 13)},
        )

    def test_demand_tool_call_routes_to_sft(self):
        hit = select(self.catalog, "tool-calling", None)
        self.assertEqual(len(hit), 1)
        self.assertIn("M06", hit[0]["modules"])
        self.assertIn("M06", pretty(hit[0], self.catalog))

    def test_no_hit_returns_empty_not_fake_route(self):
        self.assertEqual(select(self.catalog, "nonexistent", None), [])
        self.assertEqual(select(self.catalog, None, "###missing###"), [])

    def test_detects_broken_path(self):
        data = copy.deepcopy(self.catalog)
        data["modules"][0]["path"] = "LLM-Training/modules/DOES_NOT_EXIST.md"
        self.assertTrue(any("missing or escaped" in issue for issue in validate(data)))

    def test_detects_claimed_mastery(self):
        data = copy.deepcopy(self.catalog)
        data["learning_status"] = "ALL_PASSED"
        self.assertTrue(any("must not claim learner mastery" in issue for issue in validate(data)))

    def test_detects_unknown_dependency(self):
        data = copy.deepcopy(self.catalog)
        data["modules"][0]["prerequisites"] = ["M99"]
        self.assertTrue(any("invalid prerequisite" in issue for issue in validate(data)))

    def test_search_works_without_external_service(self):
        results = select(self.catalog, None, "延迟")
        self.assertTrue(any(r["id"] == "serving-p95" for r in results))


if __name__ == "__main__":
    unittest.main()

