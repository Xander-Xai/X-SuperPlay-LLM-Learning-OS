"""Numerical teaching lab: DPO margin, group-normalized GRPO advantage, reward pitfalls.

This has no policy network, no optimizer update, and no sampled LLM responses.
It is a transparent formula sandbox, NOT a DPO/GRPO model training claim.
"""
from __future__ import annotations

import math
from typing import Sequence


def stable_softplus(x: float) -> float:
    """log(1+exp(x)) without overflow."""
    if not math.isfinite(x):
        raise ValueError("expected finite x")
    return max(0.0, x) + math.log1p(math.exp(-abs(x)))


def dpo_loss(
    policy_chosen_logp: float,
    policy_rejected_logp: float,
    ref_chosen_logp: float,
    ref_rejected_logp: float,
    beta: float = 0.1,
) -> float:
    """Single-pair DPO loss, ignoring label smoothing/alternative objectives.

    L = softplus(-beta * ((logπ_c-logπ_r)-(logπref_c-logπref_r))).
    Inputs are *sequence* log-probabilities with comparable masking/length
    conventions, not per-token probabilities or verbal quality scores.
    """
    args = [policy_chosen_logp, policy_rejected_logp,
            ref_chosen_logp, ref_rejected_logp, beta]
    if not all(math.isfinite(v) for v in args) or beta <= 0:
        raise ValueError("finite log-probabilities and positive beta required")
    margin = beta * ((policy_chosen_logp - policy_rejected_logp) -
                     (ref_chosen_logp - ref_rejected_logp))
    return stable_softplus(-margin)


def group_advantages(rewards: Sequence[float], epsilon: float = 1e-8) -> list[float]:
    """Illustrative GRPO relative advantage with population std.

    Production implementations may differ in normalization and clipping;
    all-equal reward groups yield zero relative signal.
    """
    if not rewards or len(rewards) < 2 or not all(math.isfinite(r) for r in rewards):
        raise ValueError("need >=2 finite rewards for a group")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    avg = sum(rewards) / len(rewards)
    std = math.sqrt(sum((r - avg)**2 for r in rewards) / len(rewards))
    if std == 0:
        return [0.0] * len(rewards)
    return [(r - avg) / (std + epsilon) for r in rewards]


def weak_format_reward(text: str) -> float:
    """Deliberately bad reward function: format only, not answer correctness."""
    return float(text.strip().startswith("<answer>") and text.strip().endswith("</answer>"))


def independently_verified_reward(text: str, expected: str) -> float:
    """Toy exact-answer verifier, not a proof of validity for real tasks."""
    cleaned = text.replace("<answer>", "").replace("</answer>", "").strip()
    return float(cleaned == expected.strip())


def demo() -> dict:
    before = dpo_loss(-3.0, -2.5, -2.8, -2.7)
    after = dpo_loss(-1.5, -2.5, -2.8, -2.7)
    wrong_but_formatted = "<answer>5</answer>"
    correct_but_plain = "4"
    return {
        "mode": "SYNTHETIC_FORMULAS_NO_MODEL",
        "dpo_loss_before": round(before, 6),
        "dpo_loss_after_chosen_logp_rises": round(after, 6),
        "grpo_group_0_1_1_0": [round(x, 4) for x in group_advantages([0.0, 1.0, 1.0, 0.0])],
        "grpo_no_signal_when_all_equal": group_advantages([1.0, 1.0, 1.0]),
        "bad_reward_prefers_wrong_answer": weak_format_reward(wrong_but_formatted) >
                                          weak_format_reward(correct_but_plain),
        "verifier_prefers_correct_answer": independently_verified_reward(correct_but_plain, "4") >
                                           independently_verified_reward(wrong_but_formatted, "4"),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(demo(), ensure_ascii=False, indent=2))

