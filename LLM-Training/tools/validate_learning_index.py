"""Offline contract checks for the demand-driven curriculum index.

No network, GPU, model access or personal data. GitHub CI validates structure only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "LLM-Training" / "index" / "learning-index.json"
VALID_GATES = {f"G{i}" for i in range(9)}


def load_index(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_file(path: str, errors: list[str], label: str) -> None:
    if not isinstance(path, str) or not path or path.startswith(("http://", "https://")):
        errors.append(f"{label}: invalid repository file: {path!r}")
        return
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        errors.append(f"{label}: missing or escaped path: {path}")


def validate(index: dict) -> list[str]:
    problems: list[str] = []
    if index.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    identity = index.get("identity", {})
    if not isinstance(identity, dict):
        return ["identity must be object"]
    for key in ("readme", "roadmap", "legacy_roadmap"):
        _repo_file(identity.get(key), problems, f"identity.{key}")
    if index.get("learning_status") != "CURRICULUM_READY_LEARNER_UNASSESSED":
        problems.append("index must not claim learner mastery")

    modules = index.get("modules", [])
    if not isinstance(modules, list) or len(modules) != 12:
        return problems + ["modules must be array of 12"]
    module_ids = {m.get("id") for m in modules}
    if module_ids != {f"M{i:02d}" for i in range(1, 13)}:
        problems.append("module IDs must be exactly M01..M12")
    for m in modules:
        mid = m.get("id")
        _repo_file(m.get("path"), problems, f"module {mid}")
        deps = m.get("prerequisites", [])
        if not isinstance(deps, list):
            problems.append(f"module {mid}: prerequisites not list")
            continue
        if mid in deps or any(dep not in module_ids for dep in deps) or len(set(deps)) != len(deps):
            problems.append(f"module {mid}: invalid prerequisite link")

    sources = index.get("sources", [])
    if not isinstance(sources, list) or not sources:
        return problems + ["sources must be non-empty array"]
    source_ids = [s.get("id") for s in sources]
    if len(source_ids) != len(set(source_ids)):
        problems.append("duplicate source IDs")
    for s in sources:
        url = s.get("url", "")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            problems.append(f"source {s.get('id')}: expected HTTPS URL")

    demands = index.get("demands", [])
    if not isinstance(demands, list) or not demands:
        return problems + ["demands must be non-empty array"]
    demand_ids = [d.get("id") for d in demands]
    if len(demand_ids) != len(set(demand_ids)):
        problems.append("duplicate demand IDs")
    for d in demands:
        did = d.get("id")
        if d.get("status") != "DESIGN_ONLY":
            problems.append(f"demand {did}: cannot claim learner outcome from index")
        for key in ("entry", "practice"):
            _repo_file(d.get(key), problems, f"demand {did}.{key}")
        chosen = d.get("modules", [])
        if not isinstance(chosen, list) or not chosen or len(set(chosen)) != len(chosen) or any(x not in module_ids for x in chosen):
            problems.append(f"demand {did}: invalid modules")
        if not isinstance(d.get("sources"), list) or any(x not in source_ids for x in d.get("sources", [])):
            problems.append(f"demand {did}: unknown source ID")
        if not isinstance(d.get("gates"), list) or any(x not in VALID_GATES for x in d.get("gates", [])):
            problems.append(f"demand {did}: invalid gate")

    tracks = index.get("tracks", [])
    if not isinstance(tracks, list) or not tracks:
        return problems + ["tracks must be non-empty array"]
    if len({t.get("id") for t in tracks}) != len(tracks):
        problems.append("duplicate track IDs")
    for t in tracks:
        _repo_file(t.get("entry"), problems, f"track {t.get('id')}")
        if not isinstance(t.get("modules"), list) or any(x not in module_ids for x in t.get("modules", [])):
            problems.append(f"track {t.get('id')}: invalid modules")

    prod = index.get("production", {})
    _repo_file(prod.get("entry"), problems, "production.entry")
    if set(prod.get("gates", [])) != VALID_GATES:
        problems.append("production gates must include G0..G8")
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

