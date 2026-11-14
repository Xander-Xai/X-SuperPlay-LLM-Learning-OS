"""Offline schema/content validation for the Agent deep-dive curriculum.

No network, LLM, API keys, database or paid calls.
Only validates learning inventory and local evidence contracts.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).with_name("agent-curriculum-manifest.json")


def validate_manifest(data: dict, root: Path = REPO, check_files: bool = True) -> list[str]:
    issues: list[str] = []
    modules = data.get("modules")
    if not isinstance(modules, list) or [m.get("id") for m in modules if isinstance(m, dict)] != [
        f"A{i}" for i in range(1, 9)
    ]:
        issues.append("Expected exactly ordered A1..A8 module IDs")
    if data.get("weeks") != list(range(1, 9)):
        issues.append("Eight exact week values required")
    if data.get("day_plans") != ["Day 1", "Day 2", "Day 3"]:
        issues.append("Day 1/2/3 required")
    projects = data.get("projects")
    if not isinstance(projects, list) or len(projects) != 3 or len(set(projects)) != 3:
        issues.append("Three distinct projects required")
    resources = data.get("resources")
    if not isinstance(resources, list) or len(resources) != 10 or len(set(resources)) != 10:
        issues.append("Ten distinct official resource URLs required")
    else:
        hosts = {"huggingface.co", "www.anthropic.com", "openai.github.io",
                 "docs.langchain.com", "google.github.io"}
        for url in resources:
            parsed = urlparse(url)
            if parsed.scheme != "https" or parsed.netloc not in hosts:
                issues.append(f"Invalid source URL or publisher: {url}")
    if data.get("canonical_rubric") != "LLM-Training/assessments/CAPABILITY-RUBRIC.md":
        issues.append("Do not redefine canonical L0–L4 rubric")
    states = data.get("states") or {}
    if states.get("provider") != "LIVE_NOT_RUN" or states.get("learner") != "UNASSESSED":
        issues.append("Unsupported live/learner pass claim")
    if check_files:
        for name in data.get("required_docs", []):
            path = (root / name).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                issues.append(f"Missing or unsafe file path: {name}")
        for module in modules or []:
            if not isinstance(module, dict):
                continue
            guide = (root / module.get("guide", "")).resolve()
            if not guide.is_relative_to(root.resolve()) or not guide.is_file():
                issues.append(f"Missing module guide {module.get('id')}")
                continue
            body = guide.read_text(encoding="utf-8")
            for token in module.get("keywords", []):
                if token not in body:
                    issues.append(f"Missing {module.get('id')} key concept: {token}")
        schedule = root / "LLM-Training/application-engineering/agent-deep-dive/STUDY-SCHEDULE.md"
        if schedule.is_file():
            body = schedule.read_text(encoding="utf-8")
            for token in ["150 分钟", "20%", "25%", "30%", "Day 1", "Day 2", "Day 3",
                          "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]:
                if token not in body:
                    issues.append(f"Missing schedule token: {token}")
        labs = root / "LLM-Training/application-engineering/agent-deep-dive/LABS.md"
        if labs.is_file():
            body = labs.read_text(encoding="utf-8")
            for token in projects or []:
                if token not in body:
                    issues.append(f"Missing project in labs: {token}")
    return issues


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    issues = validate_manifest(data)
    print("Agent deep-dive manifest:", len(data["modules"]), "modules,",
          len(data["weeks"]), "weeks,", len(data["resources"]), "sources; issues:", len(issues))
    for issue in issues:
        print("ERROR:", issue)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
