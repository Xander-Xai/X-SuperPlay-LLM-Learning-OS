"""Offline contract and failure tests for mini_agent_loop."""
import unittest
from mini_agent_loop import ToolGateway, ScriptedModel, GatewayError, run_agent


def call(name, **arguments):
    return {"type": "tool", "name": name, "arguments": arguments}


def final(answer="done"):
    return {"type": "final", "answer": answer}


class MiniLoopTests(unittest.TestCase):
    def test_read_only_success(self):
        gw = ToolGateway()
        r = run_agent(ScriptedModel([call("lookup_order", order_id="o-1"), final()]), gw)
        self.assertEqual(r["status"], "completed")
        self.assertEqual(r["trace"][0]["result"]["status"], "paid")
        self.assertEqual(gw.effects, 0)

    def test_approved_refund_once(self):
        gw = ToolGateway(can_refund=True, approvals={"o-1"})
        r = run_agent(ScriptedModel([call("refund_order", order_id="o-1", idempotency_key="k"), final()]), gw)
        self.assertEqual(r["status"], "completed")
        self.assertEqual(gw.effects, 1)
        self.assertEqual(gw.orders["o-1"]["status"], "refunded")

    def test_missing_approval(self):
        gw = ToolGateway(can_refund=True)
        r = run_agent(ScriptedModel([call("refund_order", order_id="o-1", idempotency_key="k")]), gw)
        self.assertEqual(r["reason"], "APPROVAL_REQUIRED")
        self.assertEqual(gw.effects, 0)

    def test_permission(self):
        gw = ToolGateway(approvals={"o-1"})
        r = run_agent(ScriptedModel([call("refund_order", order_id="o-1", idempotency_key="k")]), gw)
        self.assertEqual(r["reason"], "FORBIDDEN_ACTION")

    def test_tenant_isolation(self):
        r = run_agent(ScriptedModel([call("lookup_order", order_id="o-2")]), ToolGateway(tenant="A"))
        self.assertEqual(r["reason"], "FORBIDDEN_TENANT")

    def test_unknown_tool(self):
        r = run_agent(ScriptedModel([call("delete_database", order_id="o-1")]), ToolGateway())
        self.assertEqual(r["reason"], "UNKNOWN_TOOL")

    def test_invalid_schema(self):
        r = run_agent(ScriptedModel([call("lookup_order", order_id=123)]), ToolGateway())
        self.assertEqual(r["reason"], "INVALID_ARGS")

    def test_extra_argument_cannot_elevate_role(self):
        r = run_agent(ScriptedModel([call("lookup_order", order_id="o-1", role="admin")]), ToolGateway())
        self.assertEqual(r["reason"], "INVALID_ARGS")

    def test_idempotency_duplicate_payload(self):
        gw = ToolGateway(can_refund=True, approvals={"o-1"})
        first = gw.execute("refund_order", {"order_id": "o-1", "idempotency_key": "k"})
        second = gw.execute("refund_order", {"order_id": "o-1", "idempotency_key": "k"})
        self.assertEqual(first, second)
        self.assertEqual(gw.effects, 1)

    def test_idempotency_conflicting_payload(self):
        gw = ToolGateway(tenant="A", can_refund=True, approvals={"o-1"})
        gw.execute("refund_order", {"order_id": "o-1", "idempotency_key": "k"})
        # A second order in the same tenant makes this a payload-conflict rather than tenant denial.
        gw.orders["o-3"] = {"tenant": "A", "status": "paid"}
        gw.approvals.add("o-3")
        with self.assertRaisesRegex(GatewayError, "IDEMPOTENCY_CONFLICT"):
            gw.execute("refund_order", {"order_id": "o-3", "idempotency_key": "k"})
        self.assertEqual(gw.effects, 1)

    def test_empty_key(self):
        gw = ToolGateway(can_refund=True, approvals={"o-1"})
        with self.assertRaisesRegex(GatewayError, "INVALID_ARGS"):
            gw.execute("refund_order", {"order_id": "o-1", "idempotency_key": ""})

    def test_step_limit(self):
        gw = ToolGateway()
        r = run_agent(ScriptedModel([call("lookup_order", order_id="o-1")] * 5), gw, max_steps=3)
        self.assertEqual(r["status"], "step_limit")
        self.assertEqual(len(r["trace"]), 3)

    def test_model_exhaustion_no_fake_success(self):
        r = run_agent(ScriptedModel([]), ToolGateway())
        self.assertEqual(r["status"], "invalid_model")

    def test_final_invalid(self):
        r = run_agent(ScriptedModel([final("")]), ToolGateway())
        self.assertEqual(r["status"], "invalid_model")

    def test_error_cannot_be_turned_into_success(self):
        gw = ToolGateway()
        r = run_agent(ScriptedModel([call("refund_order", order_id="o-1", idempotency_key="k"), final("refunded")]), gw)
        self.assertEqual(r["status"], "tool_error")
        self.assertNotIn("answer", r)
        self.assertEqual(gw.effects, 0)

    def test_bad_step_budget(self):
        with self.assertRaises(ValueError):
            run_agent(ScriptedModel([final()]), ToolGateway(), max_steps=0)


if __name__ == "__main__":
    unittest.main()
