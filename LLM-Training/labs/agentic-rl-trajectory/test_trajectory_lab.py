"""Run with unittest discover; demonstrates toy RL, not a trained LLM."""
import unittest
from trajectory_lab import (
    RefundSandbox, Task, TabularQPolicy, evaluate,
    run_scripted, superficial_format_reward, train_tabular_policy,
)


class SandboxTests(unittest.TestCase):
    def test_successful_refund(self):
        env = run_scripted(Task("eligible", True), ("lookup", "policy", "refund"))
        self.assertTrue(env.success)
        self.assertTrue(env.refund_executed)
        self.assertEqual([x.state for x in env.trajectory], ["start", "looked_up", "eligible"])

    def test_correct_denial_after_policy(self):
        env = run_scripted(Task("ineligible", False), ("lookup", "policy", "deny"))
        self.assertTrue(env.success)
        self.assertFalse(env.refund_executed)

    def test_unsafe_refund_always_blocked(self):
        for actions in [("refund",), ("lookup", "refund"), ("lookup", "policy", "refund")]:
            env = run_scripted(Task("ineligible", False), actions)
            self.assertTrue(env.guardrail_blocked)
            self.assertFalse(env.refund_executed)
            self.assertFalse(env.success)

    def test_hidden_eligibility_until_policy_and_reset(self):
        env = RefundSandbox()
        env.reset(Task("e", True))
        env.step("lookup")
        self.assertEqual(env.state, "looked_up")
        env.reset(Task("n", False))
        self.assertEqual(env.trajectory, [])
        self.assertFalse(env.refund_executed)
        env.step("lookup")
        self.assertEqual(env.step("policy").observation, "refund_ineligible")

    def test_format_reward_hacking(self):
        wrong = run_scripted(Task("w", False), ("refund",))
        right = run_scripted(Task("r", True), ("lookup", "policy", "refund"))
        self.assertEqual(superficial_format_reward('{"status":"failed"}'), 1.0)
        self.assertEqual(superficial_format_reward('{"status":"done"}'), 1.0)
        self.assertFalse(wrong.success)
        self.assertTrue(right.success)
        self.assertLess(sum(t.reward for t in wrong.trajectory), sum(t.reward for t in right.trajectory))

    def test_invalid_action_and_terminal(self):
        env = RefundSandbox()
        env.reset(Task("t", True))
        with self.assertRaises(ValueError):
            env.step("pay")
        env.step("refund")
        with self.assertRaises(RuntimeError):
            env.step("lookup")

    def test_train_updates_policy_and_heldout_evaluation(self):
        before = evaluate(TabularQPolicy())
        policy = train_tabular_policy(episodes=2400, seed=19)
        after = evaluate(policy)
        self.assertNotEqual(policy.values("start")["lookup"], 0.0)
        self.assertGreater(after["task_success_rate"], before["task_success_rate"])
        self.assertGreaterEqual(after["task_success_rate"], 0.9)
        self.assertEqual(after["blocked_unsafe_action_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
