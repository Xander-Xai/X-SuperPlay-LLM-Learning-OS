"""Catalog validation, negative cases and offline routing."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_application_engineering import load, validate
from route_application import choose


class ApplicationIndexContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()

    def test_application_coverage_and_backlink(self):
        self.assertEqual(validate(self.data), [])
        self.assertEqual(len(self.data["tracks"]), 10)

    def test_all_key_terms_locatable(self):
        for keyword in ("Ragas", "Context", "Prompt", "Harness", "RAG", "MCP"):
            self.assertTrue(choose(self.data, query=keyword), keyword)

    def test_search_module_and_exact_id(self):
        self.assertTrue(choose(self.data, module="M10"))
        self.assertEqual(choose(self.data, topic_id="APP-HARNESS")[0]["id"], "APP-HARNESS")

    def test_unknown_keyword_has_no_fabricated_match(self):
        self.assertEqual(choose(self.data, query="unknown-abczz-2026"), [])

    def test_missing_referenced_doc_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"][0]["guide"] = "LLM-Training/not-found.md"
        self.assertTrue(any("invalid guide" in x for x in validate(fake, False)))

    def test_unpinned_upstream_source_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"][0]["upstream_url"] = "https://github.com/example/main"
        self.assertTrue(any("not pinned" in x for x in validate(fake, False)))

    def test_false_pass_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"][0]["execution_evidence"] = "PRODUCTION_SAFE"
        self.assertTrue(any("unsupported" in x for x in validate(fake, False)))

    def test_duplicate_or_missing_track_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"].pop()
        self.assertTrue(any("missing or duplicated" in x for x in validate(fake, False)))

    def test_missing_source_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"][0]["official_sources"] = []
        self.assertTrue(any("no authoritative" in x for x in validate(fake, False)))

    def test_not_enough_concepts_rejected(self):
        fake = copy.deepcopy(self.data)
        fake["tracks"][0]["concepts"] = ["one"]
        self.assertTrue(any("fewer than" in x for x in validate(fake, False)))


if __name__ == "__main__":
    unittest.main()
