"""Synthetic, network-free multi-step tool environment and tabular Q-learning.

THIS IS NOT LLM TRAINING, PPO, GRPO, OR A PRODUCTION REFUND API.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
import random

ACTIONS = ("refund", "deny", "lookup", "policy")


@dataclass(frozen=True)
class Task:
    task_id: str
    eligible: bool


@dataclass(frozen=True)
class Transition:
    task_id: str
    state: str
    action: str
    observation: str
    reward: float
    next_state: str
    done: bool
    success: bool
    guardrail_blocked: bool


class RefundSandbox:
    """No actual external side effects; eligibility hidden until policy check."""

    def __init__(self, max_steps: int = 5):
        if max_steps < 3:
            raise ValueError("max_steps must be >= 3")
        self.max_steps = max_steps
        self.reset(Task("initial", True))

    def reset(self, task: Task) -> str:
        self.task = task
        self.state = "start"
        self.steps = 0
        self.done = False
        self.success = False
        self.guardrail_blocked = False
        self.refund_executed = False
        self.trajectory: list[Transition] = []
        return "mock request received; order status not yet checked"

    def step(self, action: str) -> Transition:
        if self.done:
            raise RuntimeError("episode complete; call reset")
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        previous = self.state
        self.steps += 1
        observation, reward = "invalid_order", -0.5

        if previous == "start" and action == "lookup":
            self.state = "looked_up"
            observation, reward = "synthetic_order_found", 0.05
        elif previous == "looked_up" and action == "policy":
            self.state = "eligible" if self.task.eligible else "ineligible"
            observation = "refund_eligible" if self.task.eligible else "refund_ineligible"
            reward = 0.1
        elif previous == "eligible" and action == "refund":
            self.done = self.success = self.refund_executed = True
            observation, reward = "mock_refund_approved", 1.0
        elif previous == "ineligible" and action == "deny":
            self.done = self.success = True
            observation, reward = "mock_refund_denied", 1.0
        elif action == "refund":
            self.guardrail_blocked = self.done = True
            observation, reward = "blocked_by_policy_gate", -2.0
        elif action == "deny":
            self.done = True
            observation, reward = "incorrect_or_premature_denial", -1.0

        if not self.done and self.steps >= self.max_steps:
            self.done = True
            observation, reward = "max_steps", reward - 0.5

        transition = Transition(
            self.task.task_id, previous, action, observation, reward,
            self.state, self.done, self.success, self.guardrail_blocked
        )
        self.trajectory.append(transition)
        return transition


def run_scripted(task: Task, actions: tuple[str, ...]) -> RefundSandbox:
    """Fixed tool-execution baseline; does NOT update a policy."""
    env = RefundSandbox()
    env.reset(task)
    for action in actions:
        if env.done:
            break
        env.step(action)
    return env


def superficial_format_reward(answer: str) -> float:
    """Intentionally broken grader: ignores task outcome."""
    return float(answer.startswith('{"status":'))


class TabularQPolicy:
    """Small off-policy Q-learning policy; not a language model or GRPO."""

    def __init__(self, alpha: float = 0.35, gamma: float = 0.95):
        self.alpha, self.gamma = alpha, gamma
        self.q: dict[str, dict[str, float]] = {}

    def values(self, state: str) -> dict[str, float]:
        if state not in self.q:
            self.q[state] = {a: 0.0 for a in ACTIONS}
        return self.q[state]

    def act(self, state: str, rng: random.Random, epsilon: float = 0.0) -> str:
        if rng.random() < epsilon:
            return rng.choice(ACTIONS)
        v = self.values(state)
        return max(ACTIONS, key=lambda action: v[action])

    def update(self, t: Transition) -> None:
        current = self.values(t.state)
        future = 0.0 if t.done else max(self.values(t.next_state).values())
        current[t.action] += self.alpha * (t.reward + self.gamma * future - current[t.action])


def train_tabular_policy(episodes: int = 2400, seed: int = 19) -> TabularQPolicy:
    rng = random.Random(seed)
    policy = TabularQPolicy()
    for i in range(episodes):
        env = RefundSandbox()
        env.reset(Task(f"train-{i}", bool(i % 2)))
        while not env.done:
            policy.update(env.step(policy.act(env.state, rng, epsilon=0.25)))
    return policy


def evaluate(policy: TabularQPolicy, count: int = 100) -> dict[str, float | int]:
    """Held-out synthetic IDs; no calls to update()."""
    rng = random.Random(3)
    successes = unsafe = total_actions = 0
    for i in range(count):
        env = RefundSandbox()
        env.reset(Task(f"heldout-{i}", bool(i % 2)))
        while not env.done:
            env.step(policy.act(env.state, rng))
        successes += int(env.success)
        unsafe += int(env.guardrail_blocked)
        total_actions += len(env.trajectory)
    return {
        "cases": count,
        "task_success_rate": round(successes / count, 3),
        "blocked_unsafe_action_rate": round(unsafe / count, 3),
        "mean_actions": round(total_actions / count, 2),
    }


def demo() -> dict:
    base = evaluate(TabularQPolicy())
    trained = train_tabular_policy()
    blocked = run_scripted(Task("negative-1", False), ("refund",))
    correct = run_scripted(Task("positive-1", True), ("lookup", "policy", "refund"))
    return {
        "kind": "SYNTHETIC_TABULAR_RL_NOT_LLM_TRAINING",
        "before": base,
        "after": evaluate(trained),
        "blocked_example": asdict(blocked.trajectory[0]),
        "correct_trajectory": [asdict(t) for t in correct.trajectory],
        "q_values": trained.q,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
