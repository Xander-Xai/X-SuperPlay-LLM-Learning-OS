"""Deterministic synthetic arithmetic, exact reward and split verification.

Standard-library only. NOT a trained LLM or evidence of model improvement.
"""
from __future__ import annotations
from hashlib import sha256
import json
import random
import re

RANGES = {"train": range(2, 26), "dev": range(26, 33), "test": range(33, 40)}
ANSWER_RE = re.compile(r"\s*<answer>\s*(-?\d+)\s*</answer>\s*\Z")


def prompt_for(a: int, b: int) -> str:
    return f"Calculate {a} + {b}. Return only <answer>integer</answer>.\n"


def samples(split: str) -> list[dict]:
    """Disjoint operand ranges prevent exact task-pair overlap across splits."""
    if split not in RANGES:
        raise ValueError(f"Unknown split: {split}")
    values = list(RANGES[split])
    pairs = [(a, b) for a in values for b in values]
    random.Random({"train": 17, "dev": 23, "test": 31}[split]).shuffle(pairs)
    if split == "train":
        pairs = pairs[:240]
    return [
        {"task_id": f"{split}-{a}-{b}",
         "prompt": prompt_for(a, b),
         "answer": str(a + b),
         "completion": f"<answer>{a + b}</answer>"}
        for a, b in pairs
    ]


def parse_answer(text: str) -> int | None:
    """Reject missing, malformed, multiple or trailing answers."""
    if not isinstance(text, str):
        return None
    match = ANSWER_RE.fullmatch(text)
    return int(match.group(1)) if match else None


def exact_reward(completions, answer, **kwargs) -> list[float]:
    """TRL callable signature; grade completion ONLY, never the prompt.

    For LLM GRPO, this is the training reward. The independent test protocol
    must use held-out labels and record errors, not trust reward mean alone.
    """
    if len(completions) != len(answer):
        raise ValueError("Mismatched completion/answer lengths")
    scores = []
    for completion, target in zip(completions, answer):
        if isinstance(completion, list):
            completion = completion[-1].get("content", "") if completion else ""
        if isinstance(completion, dict):
            completion = completion.get("content", "")
        value = parse_answer(completion)
        scores.append(float(value is not None and value == int(target)))
    return scores


def fingerprint(split: str) -> str:
    payload = json.dumps(samples(split), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return sha256(payload).hexdigest()


def validate_splits() -> dict:
    all_sets = {name: samples(name) for name in RANGES}
    ids = {name: {row["task_id"] for row in rows} for name, rows in all_sets.items()}
    assert not (ids["train"] & ids["dev"] or ids["train"] & ids["test"] or ids["dev"] & ids["test"])
    prompts = {name: {row["prompt"] for row in rows} for name, rows in all_sets.items()}
    assert not (prompts["train"] & prompts["dev"] or prompts["train"] & prompts["test"] or prompts["dev"] & prompts["test"])
    for rows in all_sets.values():
        assert all(exact_reward([r["completion"]], [r["answer"]]) == [1.0] for r in rows)
    return {name: {"count": len(rows), "sha256": fingerprint(name)} for name, rows in all_sets.items()}


if __name__ == "__main__":
    print(json.dumps({"kind": "SYNTHETIC_DATA_NOT_MODEL_TRAINING", "splits": validate_splits()}, indent=2))
