"""Standard-library contract tests; no torch, model or internet required."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_learning_index import load_index, validate
from route_learning import select, pretty


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

    def test_all_modules_have_sources_and_practices(self):
        for m in self.catalog["modules"]:
            self.assertGreater(len(m["sources"]),0)
            self.assertTrue(m["practice"])
            self.assertTrue(m["question"])

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
        self.assertTrue(any("unknown/self prerequisite" in issue for issue in validate(data)))

    def test_search_works_without_external_service(self):
        results = select(self.catalog, None, "延迟")
        self.assertTrue(any(r["id"] == "serving-p95" for r in results))

    def test_alias_qlora(self):
        result = select(self.catalog, None, "QLoRA")
        self.assertTrue(any(x["id"] == "qwen-finetune" for x in result))

    def test_alias_chinese_tool(self):
        result = select(self.catalog, None, "工具调用")
        self.assertTrue(any(x["id"] == "tool-calling" for x in result))

    def test_module_reverse_lookup(self):
        results = select(self.catalog, None, None, "M11")
        self.assertTrue(any(x["id"] == "serving-p95" for x in results))
        self.assertTrue(any(x["id"] == "production-agent" for x in results))

    def test_sources_are_resolved_in_output(self):
        hits = select(self.catalog, "grpo-reward-hacking", None)
        text = pretty(hits[0], self.catalog)
        self.assertIn("DeepSeekMath", text)
        self.assertIn("G2", text)

    def test_detects_cycle(self):
        data = copy.deepcopy(self.catalog)
        m1 = next(m for m in data["modules"] if m["id"] == "M01")
        m4 = next(m for m in data["modules"] if m["id"] == "M04")
        m1["prerequisites"] = ["M04"]
        self.assertIn("M01", m4["prerequisites"])
        self.assertTrue(any("cyclic module prerequisites" in s for s in validate(data)))

    def test_detects_unknown_module_source(self):
        data = copy.deepcopy(self.catalog)
        data["modules"][0]["sources"] = ["SRC-INVENTED"]
        self.assertTrue(any("authoritative sources" in s for s in validate(data)))

    def test_tinygpt_route_and_new_sources(self):
        hit = select(self.catalog, "tinygpt-mechanism", None)
        self.assertEqual(len(hit), 1)
        self.assertEqual(hit[0]["practice"], "LLM-Training/labs/tiny-gpt/README.md")
        self.assertIn("M03", hit[0]["modules"])
        self.assertTrue(any(x["id"] == "SRC-MEGATRONCORE" for x in self.catalog["sources"]))
        self.assertTrue(any(x["id"] == "SRC-PYTHIA" for x in self.catalog["sources"]))

    def test_tinygpt_alias_and_practice(self):
        hits = select(self.catalog, None, "手写GPT")
        self.assertTrue(any(x["id"] == "tinygpt-mechanism" for x in hits))
        self.assertEqual(
            next(m for m in self.catalog["modules"] if m["id"] == "M03")["practice_toy"],
            "LLM-Training/labs/tiny-gpt/README.md",
        )

    def test_invalid_optional_toy_practice_rejected(self):
        broken = copy.deepcopy(self.catalog)
        next(m for m in broken["modules"] if m["id"] == "M03")["practice_toy"] = "../NOTHERE.md"
        self.assertTrue(any("practice_toy" in s for s in validate(broken)))

    def test_detects_duplicate_alias(self):
        data = copy.deepcopy(self.catalog)
        data["demands"][0]["aliases"] = ["RAG", "rag"]
        self.assertTrue(any("aliases missing/duplicate" in s for s in validate(data)))


if __name__ == "__main__":
    unittest.main()

