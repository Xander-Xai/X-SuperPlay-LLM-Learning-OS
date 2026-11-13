"""Run: python -m unittest discover -s LLM-Training/labs -p 'test_*.py'"""
import unittest

import torch

from toy_train import (
    IGNORE_INDEX, assistant_only_labels, shifted_causal_ce, toy_dialogue,
)


class ToyTrainingTests(unittest.TestCase):
    def setUp(self):
        self.ids, self.roles = toy_dialogue()
        self.labels = assistant_only_labels(self.ids, self.roles)

    def test_mask_roles(self):
        for role, token, label in zip(self.roles, self.ids, self.labels):
            if role in ("assistant_tool_call", "assistant_final"):
                self.assertEqual(label, token)
            else:
                self.assertEqual(label, IGNORE_INDEX)
        self.assertEqual(sum(label != IGNORE_INDEX for label in self.labels), 6)

    def test_invalid_boundary_mapping_fails(self):
        with self.assertRaises(ValueError):
            assistant_only_labels([1, 2], ["user"])
        with self.assertRaises(ValueError):
            assistant_only_labels([1], ["assistant_or_tool?"])

    def test_shift_is_exactly_one_token(self):
        length, vocab = len(self.ids), 16
        logits = torch.full((1, length, vocab), -4.0)
        for t in range(length - 1):
            target = self.labels[t + 1]
            if target != IGNORE_INDEX:
                logits[0, t, target] = 4.0
        loss = shifted_causal_ce(logits, torch.tensor([self.labels]))
        self.assertLess(float(loss), 0.01)

    def test_gradient_is_on_logits_predicting_assistant_not_tool_targets(self):
        torch.manual_seed(0)
        logits = torch.randn((1, len(self.ids), 16), requires_grad=True)
        shifted_causal_ce(logits, torch.tensor([self.labels])).backward()
        for t in range(len(self.ids) - 1):
            grad = float(logits.grad[0, t].abs().sum())
            if self.labels[t + 1] == IGNORE_INDEX:
                self.assertEqual(grad, 0.0)
            else:
                self.assertGreater(grad, 0.0)
        self.assertEqual(float(logits.grad[0, -1].abs().sum()), 0.0)

    def test_all_ignored_is_invalid(self):
        with self.assertRaises(ValueError):
            shifted_causal_ce(torch.zeros(1, 3, 16), torch.tensor([[-100, -100, -100]]))


if __name__ == "__main__":
    unittest.main()

