"""Optional OpenAI Chat Completions tool-call adapter for SYNTHETIC orders.

DEFAULT: no network and no API key required. Import is lazy and --live explicit.
No real refunds or persistent transactions. This is educational protocol code, not
a production-ready authentication, budget accounting, or distributed system.
"""
from __future__ import annotations
import argparse
import json
import os
import time

from mini_agent_loop import ToolGateway, GatewayError

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Read only a synthetic order visible to the authenticated caller.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "refund_order",
            "description": "Refund a synthetic order ONLY after gateway approval; disabled in live demo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "idempotency_key": {"type": "string"},
                },
                "required": ["order_id", "idempotency_key"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]


def run_chat_tool_loop(client, gateway, model, user_text, *, max_turns=4,
                       max_tool_calls=5, max_seconds=60, max_completion_tokens=400):
    """A mockable SDK boundary. Every call id must match its tool observation."""
    if not model or not isinstance(model, str):
        raise ValueError("model must be explicit")
    if max_turns < 1 or max_tool_calls < 0 or max_seconds <= 0:
        raise ValueError("invalid budgets")
    messages = [
        {"role": "system", "content": (
            "Synthetic test environment. Do not invent order status or bypass gateway. "
            "If a tool call fails, report a failure instead of claiming success."
        )},
        {"role": "user", "content": user_text},
    ]
    trace = []
    total_tool_calls = 0
    start = time.monotonic()
    for turn in range(1, max_turns + 1):
        if time.monotonic() - start >= max_seconds:
            return {"status": "timeout", "trace": trace}
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, tools=TOOLS,
                tool_choice="auto", parallel_tool_calls=False,
                max_completion_tokens=max_completion_tokens,
            )
        except Exception as exc:
            # Never include API request bodies, credentials or unexpected exception text.
            trace.append({"turn": turn, "event": "model_api_error", "error_type": type(exc).__name__})
            return {"status": "model_error", "trace": trace}
        choices = getattr(response, "choices", None)
        if not choices:
            return {"status": "invalid_model", "reason": "NO_CHOICES", "trace": trace}
        message = choices[0].message
        calls = list(getattr(message, "tool_calls", None) or [])
        content = getattr(message, "content", None)
        if not calls:
            if isinstance(content, str) and content.strip():
                trace.append({"turn": turn, "event": "final"})
                return {"status": "completed", "answer": content, "trace": trace}
            return {"status": "invalid_model", "reason": "EMPTY_FINAL", "trace": trace}

        if total_tool_calls + len(calls) > max_tool_calls:
            return {"status": "tool_limit", "trace": trace}
        ids = [getattr(c, "id", None) for c in calls]
        if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
            return {"status": "invalid_model", "reason": "CALL_IDS", "trace": trace}
        assistant_calls = []
        for call in calls:
            function = getattr(call, "function", None)
            if getattr(call, "type", "function") != "function" or function is None:
                return {"status": "invalid_model", "reason": "TOOL_TYPE", "trace": trace}
            name = getattr(function, "name", None)
            arguments = getattr(function, "arguments", None)
            if not isinstance(name, str) or not isinstance(arguments, str):
                return {"status": "invalid_model", "reason": "CALL_FORMAT", "trace": trace}
            assistant_calls.append({
                "id": call.id, "type": "function",
                "function": {"name": name, "arguments": arguments},
            })
        messages.append({"role": "assistant", "content": content, "tool_calls": assistant_calls})
        for call in calls:
            total_tool_calls += 1
            name = call.function.name
            try:
                args = json.loads(call.function.arguments)
                result = gateway.execute(name, args)
            except (ValueError, TypeError):
                trace.append({"turn": turn, "event": "tool_error", "name": name, "code": "INVALID_JSON"})
                return {"status": "tool_error", "reason": "INVALID_JSON", "trace": trace}
            except GatewayError as exc:
                trace.append({"turn": turn, "event": "tool_error", "name": name, "code": exc.code})
                return {"status": "tool_error", "reason": exc.code, "trace": trace}
            # A true API tool response MUST reference exactly this Assistant call ID.
            messages.append({
                "role": "tool", "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
            trace.append({"turn": turn, "event": "tool_result", "name": name, "call_id": call.id})
    return {"status": "step_limit", "trace": trace}


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic orders; real model optional and metered.")
    parser.add_argument("--live", action="store_true", help="Explicitly enable paid network API calls.")
    parser.add_argument("--model", default=None, help="Provider model name required for --live.")
    parser.add_argument("--max-turns", type=int, default=3)
    parser.add_argument("--max-seconds", type=float, default=45)
    args = parser.parse_args()
    if not args.live:
        print("OFFLINE ONLY: run test_real_llm_optional.py to validate the protocol with FakeClient.")
        print("To opt into metered API: python .../real_llm_optional.py --live --model MODEL")
        return 0
    if not args.model or not os.getenv("OPENAI_API_KEY"):
        parser.error("--live requires --model and OPENAI_API_KEY (never commit credentials)")
    try:
        from openai import OpenAI
    except ImportError:
        parser.error("Install an appropriate version of the official openai Python SDK separately.")
    # Gateway only recognizes two fictional in-memory orders; no write permission is granted.
    gateway = ToolGateway(tenant="A", actor="synthetic-demo", can_refund=False, approvals=set())
    client = OpenAI(timeout=min(args.max_seconds, 60), max_retries=0)
    result = run_chat_tool_loop(
        client, gateway, args.model, "Please look up fictional order o-1.",
        max_turns=args.max_turns, max_seconds=args.max_seconds,
    )
    # Do not show raw provider messages or credentials; trace contains no user text.
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
