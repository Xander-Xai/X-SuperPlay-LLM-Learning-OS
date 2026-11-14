"""Offline routes are discoverable, no made-up term matches."""
import unittest
from route_application import load, choose

class ApplicationRouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load()
    def test_ragas_alias(self):
        self.assertTrue(choose(self.data,query="RAGA"))
    def test_prompt_and_context_distinct(self):
        p=choose(self.data,topic_id="APP-PROMPT")
        c=choose(self.data,topic_id="APP-CONTEXT")
        self.assertNotEqual(p[0]["guide"],c[0]["guide"])
    def test_harness_and_eval_distinct(self):
        h=choose(self.data,topic_id="APP-HARNESS")
        e=choose(self.data,topic_id="APP-EVAL")
        self.assertNotEqual(h[0]["guide"],e[0]["guide"])
    def test_case_insensitive(self):
        self.assertTrue(choose(self.data,query="hArNeSs"))
    def test_unknown_topic(self):
        self.assertEqual(choose(self.data,topic_id="APP-UNKNOWN"),[])

if __name__=="__main__":
    unittest.main()
