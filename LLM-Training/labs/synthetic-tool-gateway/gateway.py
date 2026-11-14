"""Deterministic, synthetic tool-calling boundary lab (NO LLM model or network).

This is a contract test for trusted tool execution. It does not certify that
any LLM generates correct calls, that free-text claims are grounded, or that a
real service meets a production SLA.
"""
from __future__ import annotations

import time
from typing import Any

INVENTORY = {
    "A": {"stock": 12, "visibility": "public"},
    "B": {"stock": 3, "visibility": "staff"},
}
DOCS = {
    "doc-A": {"product_id": "A", "claim": "适合基础保湿", "visibility": "public"},
    "doc-B": {"product_id": "B", "claim": "仅内部展示", "visibility": "staff"},
}
VALID_ROLES = {"guest", "staff"}


class GatewayError(Exception):
    """Base error for testable gateway failures."""


class AccessDenied(GatewayError):
    pass


class InvalidCall(GatewayError):
    pass


class EvidenceMismatch(GatewayError):
    pass


def _authorized(role: str, visibility: str) -> bool:
    return visibility == "public" or role == "staff"


def execute(role: str, call: dict, trace: list[dict[str, Any]]) -> dict:
    """Validate model-proposed tool call before executing a read-only tool.

    Trust boundary: role comes from an authenticated system, NOT from the
    model's tool-call text. trace records metadata only (no sensitive payload).
    """
    started = time.perf_counter()
    name = call.get("name") if isinstance(call, dict) else None
    status = "error"
    try:
        if role not in VALID_ROLES:
            raise AccessDenied("Unknown role")
        if not isinstance(call, dict) or set(call) != {"name", "arguments"}:
            raise InvalidCall("Expected exactly name and arguments")
        args = call["arguments"]
        if not isinstance(args, dict) or set(args) != {"product_id"}:
            raise InvalidCall("Expected exactly product_id")
        product_id = args["product_id"]
        if not isinstance(product_id, str) or product_id not in INVENTORY:
            raise InvalidCall("Unknown product ID")
        item = INVENTORY[product_id]
        if not _authorized(role, item["visibility"]):
            raise AccessDenied("Access to product denied")
        if name == "query_inventory":
            result = {"product_id": product_id, "stock": item["stock"]}
        elif name == "search_docs":
            result = [
                {"id": doc_id, "product_id": product_id, "claim": doc["claim"]}
                for doc_id, doc in DOCS.items()
                if doc["product_id"] == product_id and _authorized(role, doc["visibility"])
            ]
        else:
            raise InvalidCall("Tool not allowlisted")
        status = "success"
        return result
    finally:
        trace.append(
            {"tool": name if isinstance(name, str) else "<invalid>",
             "status": status,
             "duration_ms": round((time.perf_counter() - started) * 1000, 3)}
        )


def verify_final(role: str, product_id: str, final: dict, observations: list) -> bool:
    """Check structured inventory and citation evidence.

    Does not inspect arbitrary natural-language claims. A production system
    must add claim-level support checking, ACL audit and real data provenance.
    """
    if role not in VALID_ROLES or product_id not in INVENTORY:
        raise AccessDenied("Invalid actor or product")
    item = INVENTORY[product_id]
    if not _authorized(role, item["visibility"]):
        raise AccessDenied("Unauthorized final")
    if not isinstance(final, dict) or set(final) != {"product_id", "stock", "citation_id"}:
        raise EvidenceMismatch("Expected product_id, stock, citation_id")
    if final["product_id"] != product_id or type(final["stock"]) is not int:
        raise EvidenceMismatch("Product or stock format mismatch")
    inv_ok = any(
        isinstance(obs, dict) and obs.get("product_id") == product_id
        and obs.get("stock") == final["stock"]
        for obs in observations
    )
    cited = [
        doc for obs in observations if isinstance(obs, list) for doc in obs
        if isinstance(doc, dict) and doc.get("id") == final["citation_id"]
        and doc.get("product_id") == product_id
    ]
    if not inv_ok or not cited:
        raise EvidenceMismatch("Answer is not supported by tool observations")
    return True


def synthetic_example() -> dict:
    """Explicit test fixture, not a generated model response."""
    trace: list[dict] = []
    inventory = execute("guest", {"name": "query_inventory", "arguments": {"product_id": "A"}}, trace)
    docs = execute("guest", {"name": "search_docs", "arguments": {"product_id": "A"}}, trace)
    final = {"product_id": "A", "stock": 12, "citation_id": "doc-A"}
    return {"verified": verify_final("guest", "A", final, [inventory, docs]),
            "events": trace, "mode": "SYNTHETIC_NO_MODEL"}

