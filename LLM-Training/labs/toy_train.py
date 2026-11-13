"""CPU-only teaching lab: token-level assistant-only masking and one-token shift.

This intentionally does NOT implement/replace MiniMind. Actual chat-template masks
must be taken from the target tokenizer and checked against token boundaries.
Requires torch, but no model download or GPU.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F

ASSISTANT_TARGET_ROLES = frozenset({"assistant_tool_call", "assistant_final"})
ALL_ROLES = ASSISTANT_TARGET_ROLES | {"system", "user", "tool"}
IGNORE_INDEX = -100


def toy_dialogue() -> tuple[list[int], list[str]]:
    """Synthetic token IDs and their already-aligned message roles."""
    segments = [
        ("system", [1, 2]),
        ("user", [3, 4]),
        ("assistant_tool_call", [5, 6, 7]),
        ("tool", [8, 9]),
        ("assistant_final", [10, 11, 12]),
    ]
    ids, roles = [], []
    for role, tokens in segments:
        ids.extend(tokens)
        roles.extend([role] * len(tokens))
    return ids, roles


def assistant_only_labels(input_ids: list[int], token_roles: list[str]) -> list[int]:
    """Create label mask AFTER a chat template has aligned roles to token IDs."""
    if len(input_ids) != len(token_roles):
        raise ValueError("input_ids and token_roles must have equal length")
    if any(role not in ALL_ROLES for role in token_roles):
        raise ValueError("Unknown role; check your template and boundary mapping")
    return [token if role in ASSISTANT_TARGET_ROLES else IGNORE_INDEX
            for token, role in zip(input_ids, token_roles)]


def shifted_causal_ce(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """logits[:, t] predicts labels[:, t+1]; shift exactly once.

    Use only if your model's forward did NOT already calculate/shift its loss.
    """
    if logits.ndim != 3 or labels.ndim != 2 or logits.shape[:2] != labels.shape:
        raise ValueError("Expected logits [B,T,V], labels [B,T]")
    if logits.shape[1] < 2:
        raise ValueError("Need at least two tokens")
    if not bool((labels[:, 1:] != IGNORE_INDEX).any()):
        raise ValueError("No supervised next-token targets after shift")
    vocab = logits.shape[-1]
    return F.cross_entropy(
        logits[:, :-1, :].contiguous().view(-1, vocab),
        labels[:, 1:].contiguous().view(-1),
        ignore_index=IGNORE_INDEX,
    )


def smoke() -> None:
    ids, roles = toy_dialogue()
    labels = assistant_only_labels(ids, roles)
    torch.manual_seed(42)
    # Trainable fake logits prove gradient alignment; NOT a Transformer/pretrained LM.
    logits = torch.nn.Parameter(torch.randn(1, len(ids), 16))
    opt = torch.optim.SGD([logits], lr=0.1)
    before = shifted_causal_ce(logits, torch.tensor([labels])).item()
    opt.zero_grad(set_to_none=True)
    loss = shifted_causal_ce(logits, torch.tensor([labels]))
    loss.backward()
    opt.step()
    after = shifted_causal_ce(logits, torch.tensor([labels])).item()
    print(f"CPU toy mask + shift PASSED: loss {before:.5f} -> {after:.5f}")
    print("Reminder: this is a toy logit sanity check, NOT a MiniMind training result.")


if __name__ == "__main__":
    smoke()

