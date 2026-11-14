"""Formula checks for DPO/GRPO and reward hacking — no model downloads."""
import math
import unittest

from alignment_math import (
    dpo_loss,
    group_advantages,
    weak_format_reward,
    independently_verified_reward,
    stable_softplus,
    demo,
)


class AlignmentMathTests(unittest.TestCase):
    def test_softplus_zero(self):
        self.assertAlmostEqual(stable_softplus(0), math.log(2))

    def test_softplus_extreme_inputs(self):
        self.assertAlmostEqual(stable_softplus(1000), 1000, places=7)
        self.assertGreater(stable_softplus(-1000), -1e-9)

    def test_dpo_equal_policy_reference_zero_margin(self):
        self.assertAlmostEqual(dpo_loss(-3, -4, -3, -4), math.log(2))

    def test_dpo_increasing_chosen_policy_probability_reduces_loss(self):
        base = dpo_loss(-3, -2, -3, -2)
        improved = dpo_loss(-1, -2, -3, -2)
        self.assertLess(improved, base)

    def test_invalid_beta_and_non_finite(self):
        with self.assertRaises(ValueError):
            dpo_loss(-2, -3, -2, -3, 0)
        with self.assertRaises(ValueError):
            dpo_loss(-2, float("nan"), -2, -3)

    def test_group_relative_advantages(self):
        a = group_advantages([0, 1, 1, 0])
        self.assertAlmostEqual(sum(a), 0.0, places=7)
        self.assertLess(a[0], 0)
        self.assertGreater(a[1], 0)

    def test_equal_rewards_have_no_relative_signal(self):
        self.assertEqual(group_advantages([1, 1, 1]), [0, 0, 0])

    def test_invalid_group(self):
        with self.assertRaises(ValueError):
            group_advantages([1])
        with self.assertRaises(ValueError):
            group_advantages([1, float("inf")])

    def test_format_reward_can_be_gamed(self):
        wrong = "<answer>5</answer>"
        correct = "4"
        self.assertGreater(weak_format_reward(wrong), weak_format_reward(correct))
        self.assertLess(independently_verified_reward(wrong, "4"),
                        independently_verified_reward(correct, "4"))

    def test_demo_is_labeled_no_model(self):
        self.assertEqual(demo()["mode"], "SYNTHETIC_FORMULAS_NO_MODEL")


if __name__ == "__main__":
    unittest.main()

