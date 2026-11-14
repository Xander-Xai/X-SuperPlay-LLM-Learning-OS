"""CPU-only checks; no downloads, torch, TRL or GPU."""
import unittest
from data_and_reward import exact_reward, fingerprint, parse_answer, samples, validate_splits


class MathDataTests(unittest.TestCase):
    def test_deterministic_and_disjoint(self):
        evidence = validate_splits()
        self.assertEqual(evidence["train"]["count"], 240)
        self.assertEqual(evidence["test"]["count"], 49)
        self.assertEqual(fingerprint("train"), evidence["train"]["sha256"])
        self.assertEqual(samples("dev"), samples("dev"))

    def test_strict_reward_blocks_format_hacking(self):
        self.assertEqual(exact_reward(["<answer>4</answer>", "<answer>5</answer>"], ["4", "4"]), [1.0, 0.0])
        for text in ['{"status":"success"}', "<answer>4</answer> bad trailing text", "4", "<answer>4</answer><answer>4</answer>", ""]:
            self.assertIsNone(parse_answer(text))
            self.assertEqual(exact_reward([text], ["4"]), [0.0])

    def test_conversational_completion(self):
        self.assertEqual(exact_reward([[{"role": "assistant", "content": "<answer>9</answer>"}]], ["9"]), [1.0])
        with self.assertRaises(ValueError):
            exact_reward(["<answer>1</answer>"], [])

    def test_no_test_answers_in_train(self):
        train = samples("train")
        test = samples("test")
        self.assertTrue(all(row["task_id"].startswith("train-") for row in train))
        self.assertTrue(all(row["task_id"].startswith("test-") for row in test))
        self.assertTrue({r["prompt"] for r in train}.isdisjoint({r["prompt"] for r in test}))

    def test_invalid_split(self):
        with self.assertRaises(ValueError):
            samples("production")


if __name__ == "__main__":
    unittest.main()
