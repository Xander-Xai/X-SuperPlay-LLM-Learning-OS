"""Offline contract checks for Loop Engineering curriculum, not production readiness."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = Path(__file__).with_name("loop-course-manifest.json")


def validate(data: dict, root: Path = ROOT, check_files: bool = True) -> list[str]:
    errors = []
    if data.get("canonical_rubric") != "LLM-Training/assessments/CAPABILITY-RUBRIC.md":
        errors.append("Must preserve canonical L0-L4 rubric")
    if data.get("weeks") != [1, 2, 3, 4]:
        errors.append("Expected 4 optional weeks")
    if data.get("labs") != list("ABCDEF"):
        errors.append("Expected six ordered labs A-F")
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != 6 or len(set(chapters)) != 6:
        errors.append("Six distinct knowledge topics required")
    links = data.get("source_urls")
    if not isinstance(links, list) or len(links) < 5 or len(set(links)) != len(links):
        errors.append("At least five unique primary sources required")
    else:
        domains = {"www.ibm.com", "www.anthropic.com", "arxiv.org",
                   "docs.langchain.com", "openai.github.io"}
        for url in links:
            u = urlparse(url)
            if u.scheme != "https" or u.netloc not in domains:
                errors.append("Non-primary or insecure source: " + url)
    states = data.get("states") or {}
    for key in ("real_model", "distributed", "production"):
        if states.get(key) != "NOT_RUN":
            errors.append("Unsupported real-system claim: " + key)
    if states.get("learner") != "UNASSESSED":
        errors.append("Cannot assign learner proficiency from repository CI")
    if not check_files:
        return errors

    required = data.get("required_files", [])
    if not isinstance(required, list):
        return errors + ["required_files must be list"]
    for file in required:
        if not isinstance(file, str):
            errors.append("Non-string required file")
            continue
        path = (root / file).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            errors.append("Missing or unsafe required file: " + file)

    base = root / "LLM-Training/application-engineering/agent-deep-dive/loop-engineering"
    checks = {
        "CORE.md": ["Agent Loop", "Loop Engineering", "Verifier", "STAGNATED",
                    "idempotency", "Task State"],
        "ROADMAP.md": ["Day 1", "Day 2", "Day 3", "W1", "W2", "W3", "W4"],
        "LABS.md": ["Lab A", "Lab B", "Lab C", "Lab D", "Lab E", "Lab F"],
        "CASE-STUDY.md": ["Coding Agent", "退款", "Verifier"],
        "SOURCES.md": ["IBM", "Anthropic", "2026"],
        "labs/outer_loop.py": ["VERIFIED_SUCCESS", "BUDGET_EXHAUSTED",
                               "STAGNATED", "ESCALATED", "TRIGGER_CONTRACT_CONFLICT"],
    }
    for name, tokens in checks.items():
        path = base / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token.lower() not in text.lower():
                errors.append(f"{name} missing contract term {token}")
    return errors


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate(data)
    print("Loop course:", len(data["chapters"]), "topics;",
          len(data["weeks"]), "weeks;", len(data["labs"]),
          "labs;", len(data["source_urls"]), "sources; issues:", len(errors))
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
