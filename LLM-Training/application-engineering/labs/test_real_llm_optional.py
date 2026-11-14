"""Contract tests: fake SDK only. No external API/model/costs."""
from __future__ import annotations
import unittest
from types import SimpleNamespace as NS

from real_llm_optional import run_chat_tool_loop
from mini_agent_loop import ToolGateway


def tool(name, arguments, cid):
    return NS(id=cid, type="function", function=NS(name=name, arguments=arguments))


def msg(content=None, calls=None):
    return NS(choices=[NS(message=NS(content=content, tool_calls=calls or []))])


class FakeClient:
    def __init__(self, *responses):
        self.queue = list(responses)
        self.snapshots = []
        self.chat = NS(completions=NS(create=self.create))

    def create(self, **kw):
        self.snapshots.append(kw)
        return self.queue.pop(0)


class OptionalProviderTests(unittest.TestCase):
    def test_default_read_only_success_and_id_roundtrip(self):
        fake = FakeClient(msg(calls=[tool("lookup_order", '{"order_id":"o-1"}', "c1")]),
                          msg(content="synthetic paid order"))
        result = run_chat_tool_loop(fake, ToolGateway(), "synthetic-model", "look up")
        self.assertEqual(result["status"], "completed")
        history = fake.snapshots[1]["messages"]
        self.assertEqual(history[-1]["role"], "tool")
        self.assertEqual(history[-1]["tool_call_id"], "c1")
        self.assertEqual(history[-2]["tool_calls"][0]["id"], "c1")

    def test_multiple_calls_all_observed(self):
        fake = FakeClient(msg(calls=[
            tool("lookup_order", '{"order_id":"o-1"}', "c1"),
            tool("lookup_order", '{"order_id":"o-1"}', "c2"),
        ]), msg(content="done"))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["status"], "completed")
        self.assertEqual([m["tool_call_id"] for m in fake.snapshots[1]["messages"] if m["role"] == "tool"],
                         ["c1", "c2"])

    def test_unknown_tool_denied_no_final_success(self):
        fake = FakeClient(msg(calls=[tool("delete_all", '{}', "c1")]), msg(content="success"))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "delete")
        self.assertEqual(r["status"], "tool_error")
        self.assertEqual(r["reason"], "UNKNOWN_TOOL")
        self.assertEqual(len(fake.snapshots), 1)

    def test_bad_json(self):
        fake = FakeClient(msg(calls=[tool("lookup_order", '{"order_id":', "c1")]))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["reason"], "INVALID_JSON")

    def test_cross_tenant_access(self):
        fake = FakeClient(msg(calls=[tool("lookup_order", '{"order_id":"o-2"}', "c1")]))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["reason"], "FORBIDDEN_TENANT")

    def test_write_without_permission(self):
        gw = ToolGateway(can_refund=False)
        fake = FakeClient(msg(calls=[
            tool("refund_order", '{"order_id":"o-1","idempotency_key":"k"}', "c1")
        ]))
        r = run_chat_tool_loop(fake, gw, "m", "refund")
        self.assertEqual(r["reason"], "FORBIDDEN_ACTION")
        self.assertEqual(gw.effects, 0)

    def test_call_budget_prevents_partial_execution(self):
        gw = ToolGateway()
        fake = FakeClient(msg(calls=[
            tool("lookup_order", '{"order_id":"o-1"}', "c1"),
            tool("lookup_order", '{"order_id":"o-1"}', "c2"),
        ]))
        r = run_chat_tool_loop(fake, gw, "m", "lookup", max_tool_calls=1)
        self.assertEqual(r["status"], "tool_limit")
        self.assertEqual(r["trace"], [])

    def test_duplicate_call_id(self):
        fake = FakeClient(msg(calls=[
            tool("lookup_order", '{"order_id":"o-1"}', "c1"),
            tool("lookup_order", '{"order_id":"o-1"}', "c1"),
        ]))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["reason"], "CALL_IDS")

    def test_empty_final(self):
        fake = FakeClient(msg(content=None))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["reason"], "EMPTY_FINAL")

    def test_step_limit(self):
        fake = FakeClient(msg(calls=[tool("lookup_order", '{"order_id":"o-1"}', "c1")]))
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup", max_turns=1)
        self.assertEqual(r["status"], "step_limit")

    def test_bad_budget(self):
        with self.assertRaises(ValueError):
            run_chat_tool_loop(FakeClient(), ToolGateway(), "m", "lookup", max_turns=0)

    def test_provider_error_sanitized(self):
        fake = FakeClient()
        r = run_chat_tool_loop(fake, ToolGateway(), "m", "lookup")
        self.assertEqual(r["status"], "model_error")
        self.assertNotIn("API", str(r))


if __name__ == "__main__":
    unittest.main()
