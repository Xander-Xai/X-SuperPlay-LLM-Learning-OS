"""Offline snapshot/index/route regression; no network or model downloads."""
from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from route_atlas import load, match_topics, match_needs, topic_details, need_details, topic_relations, shortest_relation_path, relation_summary, path_summary
from validate_atlas import read_json, MANIFEST, validate


class AtlasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idx=load()
        cls.manifest=read_json(MANIFEST)

    def test_full_contract(self):
        self.assertEqual(validate(self.idx,self.manifest),[])

    def test_six_domains(self):
        self.assertEqual({d["id"] for d in self.idx["domains"]},set("FSPEAO"))

    def test_all_topics_have_official_and_upstream_links(self):
        for t in self.idx["topics"]:
            self.assertGreater(len(t["sources"]),0)
            self.assertGreater(len(t["upstream"]),0)
        self.assertGreaterEqual(len(self.idx["topics"]),30)

    def test_rag_search_works(self):
        self.assertIn("A03",{t["id"] for t in match_topics(self.idx,"RAG")})

    def test_kv_search(self):
        self.assertIn("E02",{t["id"] for t in match_topics(self.idx,"KV")})

    def test_tool_call_alias(self):
        self.assertIn("A04",{t["id"] for t in match_topics(self.idx,"工具调用")})

    def test_no_results_not_hallucinated(self):
        self.assertEqual(match_topics(self.idx,"no-such-topic-000"),[])
        self.assertEqual(match_needs(self.idx,"no-such-need-000"),[])

    def test_need_lookup(self):
        target=next(n for n in self.idx["needs"] if n["id"]=="N02")
        self.assertIn("A04",target["topics"])
        self.assertIn("工具",need_details(self.idx,target))

    def test_topic_details_return_pinned_url_and_official(self):
        t=next(t for t in self.idx["topics"] if t["id"]=="A04")
        result=topic_details(self.idx,t)
        self.assertIn(self.idx["snapshot"]["sha"],result)
        self.assertIn("modelcontextprotocol.io",result)

    def test_missing_frozen_upstream_path_rejected(self):
        c=copy.deepcopy(self.idx)
        c["topics"][0]["upstream"]=["docs/atlas/nonexistent.md"]
        self.assertTrue(any("upstream refs" in s for s in validate(c,self.manifest)))

    def test_unknown_source_rejected(self):
        c=copy.deepcopy(self.idx)
        c["topics"][0]["sources"]=["imaginary"]
        self.assertTrue(any("official source refs" in s for s in validate(c,self.manifest)))

    def test_dangling_graph_edge_rejected(self):
        c=copy.deepcopy(self.idx)
        c["relations"][0]["from"]="A99"
        self.assertTrue(any("invalid/duplicate relationship" in s for s in validate(c,self.manifest)))

    def test_duplicate_graph_edge_rejected(self):
        c=copy.deepcopy(self.idx)
        c["relations"].append(copy.deepcopy(c["relations"][0]))
        self.assertTrue(any("invalid/duplicate relationship" in s for s in validate(c,self.manifest)))

    def test_wrong_snapshot_rejected(self):
        c=copy.deepcopy(self.idx)
        c["snapshot"]["sha"]="f"*40
        self.assertTrue(any("manifest and snapshot mismatch" in s for s in validate(c,self.manifest)))

    def test_false_mastery_rejected(self):
        c=copy.deepcopy(self.idx)
        c["topics"][0]["status"]="LEARNER_PASSED"
        self.assertTrue(any("false learner verification" in s for s in validate(c,self.manifest)))

    def test_false_demand_status_rejected(self):
        c=copy.deepcopy(self.idx)
        c["needs"][0]["status"]="REALLY_RUN"
        self.assertTrue(any("unverified claim" in s for s in validate(c,self.manifest)))


    def test_tool_relation_has_action_and_security_edges(self):
        relations = topic_relations(self.idx, "A04")
        self.assertTrue(any(r["from"] == "A04" and r["to"] == "A05" and
                            r["type"] == "supplies-actions" for r in relations))
        self.assertTrue(any(r["from"] == "O03" and r["to"] == "A04" and
                            r["type"] == "guards" for r in relations))

    def test_relation_summary_preserves_arrow_direction(self):
        text = relation_summary(self.idx, "A04")
        self.assertIn("O03", text)
        self.assertIn("O03", text.split("--guards-->")[0])
        self.assertIn("--supplies-actions-->", text)

    def test_shortest_connection_to_observability(self):
        steps = shortest_relation_path(self.idx, "A04", "O02")
        self.assertIsNotNone(steps)
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]["from"], "A04")
        self.assertEqual(steps[0]["to"], "A05")
        self.assertEqual(steps[1]["from"], "O02")
        self.assertEqual(steps[1]["to"], "A05")

    def test_path_summary_labels_graph_as_exploration(self):
        answer = path_summary(self.idx, "A04", "O02")
        self.assertIn("无向连通性", answer)
        self.assertIn("原始方向", answer)
        self.assertIn("O02 --observes--> A05", answer)

    def test_self_path_empty(self):
        self.assertEqual(shortest_relation_path(self.idx, "A04", "A04"), [])

    def test_unknown_path_not_hallucinated(self):
        self.assertIsNone(shortest_relation_path(self.idx, "A04", "A99"))
        self.assertIsNone(path_summary(self.idx, "A04", "A99"))

    def test_unknown_topic_relation_is_explicit(self):
        self.assertIn("未知主题", relation_summary(self.idx, "A99"))



if __name__=="__main__":
    unittest.main()
