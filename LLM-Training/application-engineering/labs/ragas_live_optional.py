"""Optional REAL Ragas Faithfulness demo; --live and API key required.

Offline default prints setup only, makes NO requests and imports NO extra packages.
Based on Ragas collections API as inspected on 2026-11-14:
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys

from pipeline import Principal, load_documents, select_context


async def run_live(model: str) -> None:
    try:
        from openai import AsyncOpenAI
        from ragas.llms import llm_factory
        from ragas.metrics.collections import Faithfulness
    except ImportError as exc:
        raise RuntimeError(
            "Install compatible ragas and openai in a dedicated environment; "
            "check official docs API revisions.") from exc
    docs, manifest = select_context(load_documents(),
                                    Principal("demo", "viewer"), "product a stock",
                                    budget=60, limit=3)
    # Avoid passing fixture "prompt injection" to an external judge by default.
    contexts = [d.content for d in docs if d.id == "a-public"]
    if not contexts:
        raise RuntimeError("No authorized gold context; cannot run faithfulness.")
    # Response is intentionally a frozen synthetic example; no model generated it.
    question = "What is the stock of product a in the synthetic ledger?"
    response = "Product a stock is 8 units."
    client = AsyncOpenAI()
    scorer = Faithfulness(llm=llm_factory(model, client=client))
    result = await scorer.ascore(
        user_input=question, response=response, retrieved_contexts=contexts
    )
    print(f"Ragas Faithfulness example score (judge={model}): {result.value}")
    print(f"Synthetic source IDs: {[d.id for d in docs if d.id == 'a-public']}")
    print("This is a REAL external judge evaluation of a manually fixed "
          "synthetic response, NOT live RAG retrieval or end-to-end Agent success.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Optional live Ragas Faithfulness")
    parser.add_argument("--live", action="store_true",
                        help="Explicitly allow LLM judge requests and possible cost")
    parser.add_argument("--model", default="gpt-4o-mini",
                        help="Available OpenAI judge model; verify account access")
    args = parser.parse_args()
    if not args.live:
        print("NOT RUN. To run with an authorized provider: install compatible ragas/openai, "
              "set OPENAI_API_KEY in your local environment, then pass --live. "
              "This script never connects without --live.")
        return 0
    if not os.environ.get("OPENAI_API_KEY"):
        print("NO-GO: OPENAI_API_KEY is not set; refusing live evaluation.",
              file=sys.stderr)
        return 2
    try:
        asyncio.run(run_live(args.model))
    except Exception as exc:
        # Do not print secrets or raw provider request bodies.
        print(f"NO-GO: live Ragas evaluation failed ({type(exc).__name__}); "
              "check dependency/API version and provider access.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
