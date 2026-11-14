"""Offline search contract including missing-term behavior."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from route_foundations import load,find,describe

class FoundationRouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load()["topics"]

    def test_search_tokenizers(self):
        self.assertTrue(any(x["id"]=="M02.02" for x in find(self.data,"WordPiece")))

    def test_search_information_theory(self):
        self.assertTrue(any(x["id"]=="M01.06" for x in find(self.data,"信息熵")))

    def test_search_training_system(self):
        self.assertTrue(any(x["module"]=="M09" for x in find(self.data,"显存")))

    def test_search_no_fabricated_results(self):
        self.assertEqual(find(self.data,"not-a-concept-xyz"),[])

    def test_index_explains_evidence_limit(self):
        row=next(x for x in self.data if x["id"]=="M03.04")
        out=describe(row)
        self.assertIn("因果",row["title"])
        self.assertIn("未验证",out)
        self.assertIn("https://",out)

if __name__=="__main__":
    unittest.main()
