"""Offline contract checks for the V3 demand-driven LLM curriculum.

This validates catalog integrity, paths and false mastery claims; it does NOT
make HTTP requests, execute models or judge human capability.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "LLM-Training" / "index" / "learning-index.json"
VALID_GATES = {f"G{i}" for i in range(9)}
MODULE_IDS = {f"M{i:02d}" for i in range(1, 13)}


def load_index(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_file(path: str, errors: list[str], label: str) -> None:
    if not isinstance(path, str) or not path or path.startswith(("http://", "https://")):
        errors.append(f"{label}: invalid repository file: {path!r}")
        return
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        errors.append(f"{label}: missing or escaped path: {path}")


def _unique_strings(items: object) -> bool:
    return (isinstance(items, list) and
            all(isinstance(x, str) and bool(x.strip()) for x in items) and
            len({x.strip().casefold() for x in items}) == len(items))


def _cycle_errors(deps: dict[str, list[str]]) -> list[str]:
    """Detect back-edges, even when a module is not a demand's first hop."""
    state: dict[str, int] = {}
    errors: list[str] = []

    def visit(mid: str, stack: list[str]) -> None:
        status = state.get(mid, 0)
        if status == 1:
            errors.append("cyclic module prerequisites: " + " → ".join(stack + [mid]))
            return
        if status == 2:
            return
        state[mid] = 1
        for dep in deps.get(mid, []):
            if dep in deps:
                visit(dep, stack + [mid])
        state[mid] = 2

    for mid in sorted(deps):
        if state.get(mid, 0) == 0:
            visit(mid, [])
    return errors


def validate(index: dict) -> list[str]:
    problems: list[str] = []
    if not isinstance(index, dict):
        return ["index must be object"]
    if index.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    identity = index.get("identity", {})
    if not isinstance(identity, dict):
        return ["identity must be object"]
    for key in ("readme", "roadmap", "legacy_roadmap"):
        _repo_file(identity.get(key), problems, f"identity.{key}")
    if index.get("learning_status") != "CURRICULUM_READY_LEARNER_UNASSESSED":
        problems.append("index must not claim learner mastery")

    sources = index.get("sources", [])
    if not isinstance(sources, list) or not sources:
        return problems + ["sources must be non-empty array"]
    source_ids = [s.get("id") for s in sources]
    if not _unique_strings(source_ids):
        problems.append("duplicate/invalid source IDs")
    for s in sources:
        url = s.get("url", "")
        if not isinstance(url, str):
            problems.append(f"source {s.get('id')}: invalid URL type")
            continue
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            problems.append(f"source {s.get('id')}: expected HTTPS URL")

    modules = index.get("modules", [])
    if not isinstance(modules, list) or len(modules) != 12:
        return problems + ["modules must be array of 12"]
    module_ids = [m.get("id") for m in modules]
    if set(module_ids) != MODULE_IDS or not _unique_strings(module_ids):
        problems.append("module IDs must be exactly M01..M12 (unique)")
    deps_map = {}
    for m in modules:
        mid = m.get("id")
        _repo_file(m.get("path"), problems, f"module {mid}")
        _repo_file(m.get("practice"), problems, f"module {mid}.practice")
        if "practice_toy" in m:
            _repo_file(m.get("practice_toy"), problems, f"module {mid}.practice_toy")
        if not isinstance(m.get("question"), str) or len(m["question"].strip()) < 8:
            problems.append(f"module {mid}: missing concrete entry question")
        deps = m.get("prerequisites", [])
        if not _unique_strings(deps):
            problems.append(f"module {mid}: invalid prerequisite list")
        elif mid in deps or any(dep not in MODULE_IDS for dep in deps):
            problems.append(f"module {mid}: unknown/self prerequisite")
        else:
            deps_map[mid] = deps
        refs = m.get("sources")
        if not _unique_strings(refs) or not refs or any(s not in source_ids for s in refs):
            problems.append(f"module {mid}: must point to valid authoritative sources")
        gates = m.get("gates")
        if not _unique_strings(gates) or not gates or any(x not in VALID_GATES for x in gates):
            problems.append(f"module {mid}: missing/invalid production gates")
    problems.extend(_cycle_errors(deps_map))

    demands = index.get("demands", [])
    if not isinstance(demands, list) or not demands:
        return problems + ["demands must be non-empty array"]
    demand_ids = [d.get("id") for d in demands]
    if not _unique_strings(demand_ids):
        problems.append("duplicate/invalid demand IDs")
    for d in demands:
        did = d.get("id")
        if d.get("status") != "DESIGN_ONLY":
            problems.append(f"demand {did}: cannot claim learner outcome from index")
        for key in ("entry", "practice"):
            _repo_file(d.get(key), problems, f"demand {did}.{key}")
        chosen = d.get("modules")
        if not _unique_strings(chosen) or not chosen or any(x not in MODULE_IDS for x in chosen):
            problems.append(f"demand {did}: invalid modules")
        if not _unique_strings(d.get("aliases")) or not d["aliases"]:
            problems.append(f"demand {did}: aliases missing/duplicate")
        if not _unique_strings(d.get("sources")) or not d["sources"] or any(x not in source_ids for x in d["sources"]):
            problems.append(f"demand {did}: unknown source ID")
        if not _unique_strings(d.get("gates")) or not d["gates"] or any(x not in VALID_GATES for x in d["gates"]):
            problems.append(f"demand {did}: invalid gate")

    tracks = index.get("tracks", [])
    if not isinstance(tracks, list) or not tracks:
        return problems + ["tracks must be non-empty array"]
    if not _unique_strings([t.get("id") for t in tracks]):
        problems.append("duplicate track IDs")
    for t in tracks:
        _repo_file(t.get("entry"), problems, f"track {t.get('id')}")
        if not _unique_strings(t.get("modules")) or any(x not in MODULE_IDS for x in t["modules"]):
            problems.append(f"track {t.get('id')}: invalid modules")

    prod = index.get("production", {})
    _repo_file(prod.get("entry"), problems, "production.entry")
    if set(prod.get("gates", [])) != VALID_GATES:
        problems.append("production gates must include G0..G8")
    labels = prod.get("gate_labels", {})
    if not isinstance(labels, dict) or set(labels) != VALID_GATES or not all(
            isinstance(v, str) and v.strip() for v in labels.values()):
        problems.append("production gate_labels must describe G0..G8")

    assessment = index.get("assessments", {})
    _repo_file(assessment.get("entry"), problems, "assessments.entry")
    if assessment.get("levels") != [f"L{i}" for i in range(5)]:
        problems.append("assessment levels must be L0..L4")
    return problems


def main() -> int:
    try:
        issues = validate(load_index())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INDEX ERROR: {exc}", file=sys.stderr)
        return 1
    for issue in issues:
        print(f"INDEX ERROR: {issue}", file=sys.stderr)
    print(f"LLM index validation: {len(issues)} issues")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())

