"""Offline Agent Outer Loop contract and negative tests; no network or model API."""
import tempfile
import unittest
from pathlib import Path

from outer_loop import (
    OuterLoop, TaskStore, ScriptedRunner, IndependentVerifier, TERMINAL
)


class OuterLoopContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "state.json"
        self.loop = OuterLoop(TaskStore(self.path))

    def test_pass_after_independent_failure(self):
        self.loop.submit("e1", "ok")
        runner = ScriptedRunner([
            {"artifact": "bad", "claim_done": True},
            {"artifact": "ok", "claim_done": True},
        ])
        result = self.loop.run("e1", runner)
        self.assertEqual(result["status"], "VERIFIED_SUCCESS")
        self.assertEqual(result["attempts"], 2)
        self.assertFalse(result["history"][0]["passed"])
        self.assertTrue(result["history"][1]["passed"])

    def test_self_claim_not_success(self):
        self.loop.submit("e", "ok", max_attempts=1)
        result = self.loop.run("e", ScriptedRunner([
            {"artifact": "not-ok", "claim_done": True},
        ]))
        self.assertNotEqual(result["status"], "VERIFIED_SUCCESS")
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")

    def test_duplicate_trigger_does_not_create_new_task(self):
        a = self.loop.submit("same-event", "ok")
        b = self.loop.submit("same-event", "ok")
        self.assertEqual(a["task_id"], b["task_id"])
        self.assertEqual(len(self.loop.store.load_all()), 1)

    def test_conflicting_duplicate_trigger_rejected(self):
        self.loop.submit("event", "expected")
        with self.assertRaisesRegex(ValueError, "TRIGGER_CONTRACT_CONFLICT"):
            self.loop.submit("event", "modified")

    def test_cross_tenant_trigger_conflict(self):
        self.loop.submit("event", "ok", tenant="A")
        with self.assertRaisesRegex(ValueError, "TRIGGER_CONTRACT_CONFLICT"):
            self.loop.submit("event", "ok", tenant="B")

    def test_unchanged_failures_stagnate(self):
        self.loop.submit("event", "ok", max_attempts=10, max_units=10)
        result = self.loop.run("event", ScriptedRunner([
            {"artifact": "same"}, {"artifact": "same"}, {"artifact": "ok"},
        ]))
        self.assertEqual(result["status"], "STAGNATED")
        self.assertEqual(result["attempts"], 2)

    def test_changed_failures_do_not_count_as_same_stagnation(self):
        self.loop.submit("event", "ok", max_attempts=4, max_units=4)
        runner = ScriptedRunner([
            {"artifact": "wrong-1"}, {"artifact": "wrong-2"}, {"artifact": "ok"},
        ])
        result = self.loop.run("event", runner)
        self.assertEqual(result["status"], "VERIFIED_SUCCESS")
        self.assertEqual(result["attempts"], 3)

    def test_retries_bounded_by_attempts(self):
        self.loop.submit("event", "ok", max_attempts=2, max_units=5)
        result = self.loop.run("event", ScriptedRunner([
            {"artifact": "wrong-1"}, {"artifact": "wrong-2"}, {"artifact": "ok"},
        ]))
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")
        self.assertEqual(result["attempts"], 2)

    def test_retries_bounded_by_synthetic_units(self):
        self.loop.submit("event", "ok", max_attempts=8, max_units=1)
        result = self.loop.run("event", ScriptedRunner([{"artifact": "fail"}]))
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")
        self.assertEqual(result["used_units"], 1)

    def test_unsafe_action_escalates(self):
        self.loop.submit("event", "ok")
        result = self.loop.run("event", ScriptedRunner([{"error": "unsafe"}]))
        self.assertEqual(result["status"], "ESCALATED")
        self.assertEqual(result["last_feedback"], ["UNCONFIRMED_SIDE_EFFECT"])

    def test_transient_error_can_retry(self):
        self.loop.submit("event", "ok")
        result = self.loop.run("event", ScriptedRunner([
            {"error": "transient"}, {"artifact": "ok"},
        ]))
        self.assertEqual(result["status"], "VERIFIED_SUCCESS")
        self.assertEqual(result["attempts"], 2)

    def test_transient_error_exhausts(self):
        self.loop.submit("event", "ok", max_attempts=1)
        result = self.loop.run("event", ScriptedRunner([{"error": "transient"}]))
        self.assertEqual(result["status"], "BUDGET_EXHAUSTED")

    def test_state_survives_reload(self):
        self.loop.submit("event", "ok")
        first = self.loop.step("event", ScriptedRunner([{"artifact": "not-ok"}]))
        self.assertEqual(first["status"], "RETRY_READY")
        second_loop = OuterLoop(TaskStore(self.path))
        result = second_loop.run("event", ScriptedRunner([{"artifact": "ok"}]))
        self.assertEqual(result["status"], "VERIFIED_SUCCESS")
        self.assertEqual(result["attempts"], 2)

    def test_unknown_running_state_escalates_not_rerun(self):
        self.loop.submit("event", "ok")
        state = self.loop.store.get("event")
        state["status"] = "RUNNING"
        self.loop.store.put("event", state)
        runner = ScriptedRunner([{"artifact": "ok"}])
        result = self.loop.step("event", runner)
        self.assertEqual(result["status"], "ESCALATED")
        self.assertEqual(runner.calls, 0)

    def test_terminal_duplicate_run_is_noop(self):
        self.loop.submit("event", "ok")
        first = self.loop.run("event", ScriptedRunner([{"artifact": "ok"}]))
        runner = ScriptedRunner([{"artifact": "something else"}])
        second = self.loop.run("event", runner)
        self.assertEqual(first["history"], second["history"])
        self.assertEqual(runner.calls, 0)

    def test_runner_does_not_see_target(self):
        self.loop.submit("event", "SECRET_TARGET")
        runner = ScriptedRunner([{"artifact": "not target"}])
        self.loop.step("event", runner)
        self.assertNotIn("target", runner.received[0])
        self.assertNotIn("SECRET_TARGET", str(runner.received[0]))

    def test_invalid_contract_budget(self):
        with self.assertRaises(ValueError):
            self.loop.submit("e", "ok", max_attempts=0)
        with self.assertRaises(ValueError):
            self.loop.submit("e", "ok", max_units=True)
        with self.assertRaises(ValueError):
            self.loop.submit("", "ok")

    def test_malformed_runner_output_is_failure(self):
        self.loop.submit("e", "ok")
        result = self.loop.run("e", ScriptedRunner([{"claim_done": True}]))
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["last_feedback"], ["INVALID_RUN_ARTIFACT"])

    def test_unexpected_runner_error_fails_closed(self):
        self.loop.submit("e", "ok")
        def explode(_):
            raise RuntimeError("token-should-not-be-leaked")
        result = self.loop.run("e", explode)
        self.assertEqual(result["status"], "FAILED")
        self.assertNotIn("token-should-not-be-leaked", str(result))

    def test_independent_verifier_version(self):
        v = IndependentVerifier()
        r = v.evaluate("ok", "no")
        self.assertEqual(r["verifier_revision"], "exact-text-v1")
        self.assertEqual(r["failed_checks"], ["ARTIFACT_MISMATCH"])
        self.assertFalse(r["passed"])


if __name__ == "__main__":
    unittest.main()
