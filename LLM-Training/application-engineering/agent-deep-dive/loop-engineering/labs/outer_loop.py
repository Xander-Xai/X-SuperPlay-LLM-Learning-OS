"""Synthetic Loop Engineering lab: trigger -> runner -> verifier -> persist -> stop.

Only Python stdlib, no LLM, network, paid APIs, parallel workers or real writes.
JSON os.replace is not a distributed transaction. Unit cost is fictitious.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile


TERMINAL = {
    "VERIFIED_SUCCESS", "STAGNATED", "BUDGET_EXHAUSTED",
    "ESCALATED", "FAILED", "BLOCKED", "CANCELLED",
}


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class TransientRunError(Exception):
    pass


class UnsafeRunError(Exception):
    pass


class TaskStore:
    """Single-process demo persistence; NOT multiprocess-safe or a job queue."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load_all(self) -> dict:
        if not self.path.exists():
            return {}
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("invalid task store")
        return value

    def save_all(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(
            dir=str(self.path.parent), prefix=".loop-", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=2)
                file.flush()
                os.fsync(file.fileno())
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    def get(self, trigger_id: str) -> dict:
        return self.load_all()[trigger_id]

    def put(self, trigger_id: str, state: dict) -> None:
        data = self.load_all()
        data[trigger_id] = state
        self.save_all(data)


class ScriptedRunner:
    """Fixed outputs simulate entire Agent runs; cannot change verifier contract."""

    def __init__(self, actions: list[dict]):
        self.actions = list(actions)
        self.calls = 0
        self.received = []

    def __call__(self, context: dict) -> dict:
        self.received.append(context)
        if self.calls >= len(self.actions):
            raise TransientRunError("NO_SCRIPTED_ACTION")
        action = self.actions[self.calls]
        self.calls += 1
        if action.get("error") == "transient":
            raise TransientRunError("SYNTHETIC_NETWORK")
        if action.get("error") == "unsafe":
            raise UnsafeRunError("UNKNOWN_SIDE_EFFECT")
        return action


class IndependentVerifier:
    """Compares actual synthetic artifact with frozen trusted target; ignores self-report."""

    revision = "exact-text-v1"

    def evaluate(self, target: str, artifact: str) -> dict:
        return {
            "passed": artifact == target,
            "failed_checks": [] if artifact == target else ["ARTIFACT_MISMATCH"],
            "artifact_sha256": digest(artifact),
            "verifier_revision": self.revision,
        }


class OuterLoop:
    def __init__(self, store: TaskStore, verifier=None):
        self.store = store
        self.verifier = verifier or IndependentVerifier()

    def submit(self, trigger_id: str, target: str, *, tenant="A", actor="demo",
               max_attempts=3, max_units=3) -> dict:
        # Identity is provided by trusted caller in this toy, never model-generated.
        if not all(isinstance(x, str) and x.strip()
                   for x in (trigger_id, target, tenant, actor)):
            raise ValueError("trigger, target and identity must be nonempty")
        if not all(type(x) is int and x >= 1 for x in (max_attempts, max_units)):
            raise ValueError("positive integer budgets required")
        all_tasks = self.store.load_all()
        existing = all_tasks.get(trigger_id)
        contract = {
            "target": target, "tenant": tenant, "actor": actor,
            "max_attempts": max_attempts, "max_units": max_units,
            "verifier_revision": self.verifier.revision,
        }
        if existing:
            if existing["contract"] != contract:
                raise ValueError("TRIGGER_CONTRACT_CONFLICT")
            return existing
        state = {
            "task_id": "task-" + digest(trigger_id)[:16], "status": "QUEUED",
            "contract": contract, "attempts": 0, "used_units": 0,
            "history": [], "last_feedback": [],
        }
        all_tasks[trigger_id] = state
        self.store.save_all(all_tasks)
        return state

    def step(self, trigger_id: str, runner) -> dict:
        state = self.store.get(trigger_id)
        if state["status"] in TERMINAL:
            return state
        if state["status"] == "RUNNING":
            # Previous process may have written to an external system.
            state["status"] = "ESCALATED"
            state["last_feedback"] = ["UNKNOWN_PREVIOUS_RUN_STATE"]
            self.store.put(trigger_id, state)
            return state
        if state["status"] not in {"QUEUED", "RETRY_READY"}:
            raise ValueError("invalid task state")
        contract = state["contract"]
        if state["attempts"] >= contract["max_attempts"] or state["used_units"] >= contract["max_units"]:
            state["status"] = "BUDGET_EXHAUSTED"
            self.store.put(trigger_id, state)
            return state

        state["status"] = "RUNNING"
        state["attempts"] += 1
        state["used_units"] += 1  # Synthetic unit: one complete runner invocation, NOT tokens.
        self.store.put(trigger_id, state)
        # Do not pass target to the runner; it sees feedback only.
        view = {
            "task_id": state["task_id"], "tenant": contract["tenant"],
            "actor": contract["actor"], "attempt": state["attempts"],
            "feedback": list(state["last_feedback"]),
        }
        try:
            result = runner(view)
        except UnsafeRunError:
            state["status"] = "ESCALATED"
            state["last_feedback"] = ["UNCONFIRMED_SIDE_EFFECT"]
        except TransientRunError:
            state["last_feedback"] = ["TRANSIENT_RUN_ERROR"]
            state["status"] = ("BUDGET_EXHAUSTED"
                               if self._exhausted(state) else "RETRY_READY")
        except Exception as exc:
            # Do not print secrets, traceback or arbitrary external error strings.
            state["status"] = "FAILED"
            state["last_feedback"] = ["UNEXPECTED_RUNNER_ERROR", type(exc).__name__]
        else:
            artifact = result.get("artifact") if isinstance(result, dict) else None
            if not isinstance(artifact, str):
                state["status"] = "FAILED"
                state["last_feedback"] = ["INVALID_RUN_ARTIFACT"]
            else:
                verdict = self.verifier.evaluate(contract["target"], artifact)
                evidence = {
                    "attempt": state["attempts"],
                    "runner_claim": bool(result.get("claim_done")),
                    "verifier_revision": verdict["verifier_revision"],
                    "passed": verdict["passed"],
                    "failed_checks": verdict["failed_checks"],
                    "artifact_sha256": verdict["artifact_sha256"],
                }
                state["history"].append(evidence)
                state["last_feedback"] = verdict["failed_checks"]
                if verdict["passed"]:
                    state["status"] = "VERIFIED_SUCCESS"
                elif self._unchanged_twice(state):
                    state["status"] = "STAGNATED"
                elif self._exhausted(state):
                    state["status"] = "BUDGET_EXHAUSTED"
                else:
                    state["status"] = "RETRY_READY"
        self.store.put(trigger_id, state)
        return state

    @staticmethod
    def _unchanged_twice(state: dict) -> bool:
        history = state["history"]
        if len(history) < 2:
            return False
        a, b = history[-2], history[-1]
        return (not a["passed"] and not b["passed"]
                and a["failed_checks"] == b["failed_checks"]
                and a["artifact_sha256"] == b["artifact_sha256"])

    @staticmethod
    def _exhausted(state: dict) -> bool:
        c = state["contract"]
        return state["attempts"] >= c["max_attempts"] or state["used_units"] >= c["max_units"]

    def run(self, trigger_id: str, runner) -> dict:
        while True:
            current = self.store.get(trigger_id)
            if current["status"] in TERMINAL:
                return current
            result = self.step(trigger_id, runner)
            if result["status"] in TERMINAL:
                return result


def demo() -> dict:
    # Isolated temp workspace; no files in the user's project are modified.
    with tempfile.TemporaryDirectory() as tmp:
        store = TaskStore(Path(tmp) / "task-state.json")
        outer = OuterLoop(store)
        outer.submit("git-issue-001", "tests-pass")
        runner = ScriptedRunner([
            {"artifact": "tests-fail", "claim_done": True},
            {"artifact": "tests-pass", "claim_done": True},
        ])
        result = outer.run("git-issue-001", runner)
        return {
            "status": result["status"], "attempts": result["attempts"],
            "history": result["history"], "used_units": result["used_units"],
            "warning": "Synthetic runner and exact-text verifier; not real CI, LLM or production",
        }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
