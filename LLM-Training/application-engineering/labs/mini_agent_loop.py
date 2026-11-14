"""Deterministic teaching-only Agent Loop. No LLM, network, auth, DB or real payments.

ScriptedModel returns prewritten decisions; this is NOT an SDK tool-call wire format.
All identity and approvals are provided by the trusted caller in this toy gateway.
"""
from __future__ import annotations
import json


class GatewayError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class ScriptedModel:
    """A fixed output sequence, not a language model."""

    def __init__(self, decisions: list[dict]):
        self.decisions = list(decisions)
        self.index = 0

    def decide(self, _history: list[dict]) -> dict:
        if self.index >= len(self.decisions):
            raise GatewayError("MODEL_EXHAUSTED")
        item = self.decisions[self.index]
        self.index += 1
        return item


class ToolGateway:
    """Synthetic tools with authorization, approval and scoped idempotency."""

    def __init__(self, tenant="A", actor="operator-1", can_refund=False, approvals=None):
        self.tenant, self.actor = tenant, actor
        self.can_refund = can_refund
        self.approvals = set(approvals or [])
        self.orders = {
            "o-1": {"tenant": "A", "status": "paid"},
            "o-2": {"tenant": "B", "status": "paid"},
        }
        self.effects = 0
        self.receipts = {}

    def _order(self, args: dict, allowed_fields: set[str]) -> tuple[str, dict]:
        if not isinstance(args, dict) or set(args) != allowed_fields:
            raise GatewayError("INVALID_ARGS")
        order_id = args.get("order_id")
        if not isinstance(order_id, str) or not order_id:
            raise GatewayError("INVALID_ARGS")
        order = self.orders.get(order_id)
        if order is None:
            raise GatewayError("NOT_FOUND")
        if order["tenant"] != self.tenant:
            raise GatewayError("FORBIDDEN_TENANT")
        return order_id, order

    def execute(self, name: str, args: dict) -> dict:
        if name == "lookup_order":
            order_id, order = self._order(args, {"order_id"})
            return {"order_id": order_id, "status": order["status"]}
        if name != "refund_order":
            raise GatewayError("UNKNOWN_TOOL")
        order_id, order = self._order(args, {"order_id", "idempotency_key"})
        if not self.can_refund:
            raise GatewayError("FORBIDDEN_ACTION")
        if order_id not in self.approvals:
            raise GatewayError("APPROVAL_REQUIRED")
        key = args["idempotency_key"]
        if not isinstance(key, str) or not key.strip():
            raise GatewayError("INVALID_ARGS")
        # Identity is supplied to this gateway by trusted caller, not LLM arguments.
        scope = (self.tenant, self.actor, key)
        payload = ("refund_order", order_id)
        previous = self.receipts.get(scope)
        if previous is not None:
            if previous["payload"] != payload:
                raise GatewayError("IDEMPOTENCY_CONFLICT")
            return dict(previous["result"])
        if order["status"] != "paid":
            raise GatewayError("ALREADY_REFUNDED")
        order["status"] = "refunded"
        self.effects += 1
        result = {"order_id": order_id, "status": "refunded"}
        self.receipts[scope] = {"payload": payload, "result": result}
        return dict(result)


def run_agent(model: ScriptedModel, gateway: ToolGateway, max_steps: int = 4) -> dict:
    """Every model decision counts as one step; no hidden retries or final-success claim."""
    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    history, trace = [], []
    for step in range(1, max_steps + 1):
        try:
            action = model.decide(list(history))
        except GatewayError as exc:
            return {"status": "invalid_model", "reason": exc.code, "trace": trace}
        if not isinstance(action, dict):
            return {"status": "invalid_model", "reason": "INVALID_DECISION", "trace": trace}
        if action.get("type") == "final":
            answer = action.get("answer")
            if not isinstance(answer, str) or not answer.strip():
                return {"status": "invalid_model", "reason": "INVALID_FINAL", "trace": trace}
            trace.append({"step": step, "kind": "final"})
            return {"status": "completed", "answer": answer, "trace": trace}
        if action.get("type") != "tool":
            return {"status": "invalid_model", "reason": "INVALID_DECISION", "trace": trace}
        name, args = action.get("name"), action.get("arguments")
        if not isinstance(name, str):
            return {"status": "invalid_model", "reason": "INVALID_TOOL_NAME", "trace": trace}
        # The real API message protocol and tool_call_id handling are SDK-specific.
        try:
            result = gateway.execute(name, args)
        except GatewayError as exc:
            trace.append({"step": step, "kind": "tool_error", "name": name, "reason": exc.code})
            return {"status": "tool_error", "reason": exc.code, "trace": trace}
        history.append({"tool": name, "result": result})
        trace.append({"step": step, "kind": "tool_result", "name": name, "result": result})
    return {"status": "step_limit", "reason": "MAX_STEPS", "trace": trace}


if __name__ == "__main__":
    gateway = ToolGateway(tenant="A", actor="operator-1", can_refund=True, approvals={"o-1"})
    scripted = ScriptedModel([
        {"type": "tool", "name": "lookup_order", "arguments": {"order_id": "o-1"}},
        {"type": "tool", "name": "refund_order", "arguments": {"order_id": "o-1", "idempotency_key": "demo-1"}},
        {"type": "final", "answer": "Synthetic order refunded after preconfigured approval."},
    ])
    print(json.dumps(run_agent(scripted, gateway), indent=2, ensure_ascii=False))
    print("synthetic_side_effects=", gateway.effects)
