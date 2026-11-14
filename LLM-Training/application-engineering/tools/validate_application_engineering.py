"""Offline application-engineering index contracts; no network or model API."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "LLM-Training/application-engineering/index/application-engineering-index.json"
REQUIRED_IDS = {
    "APP-PROMPT", "APP-CONTEXT", "APP-RAG", "APP-RAGAS", "APP-AGENT",
    "APP-HARNESS", "APP-TOOLS", "APP-EVAL", "APP-PRODUCTION", "APP-SECURITY",
}
SOURCE_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def load() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def local_exists(path: object) -> bool:
    if not isinstance(path, str) or not path or path.startswith("/"):
        return False
    target = (ROOT / path).resolve()
    return target.is_relative_to(ROOT) and target.is_file()


def validate(data: dict, check_repo_docs: bool = True) -> list[str]:
    failures: list[str] = []
    if data.get("schema_version") != 1:
        return ["Invalid application engineering schema version"]
    sha = data.get("upstream_snapshot_sha", "")
    if not isinstance(sha, str) or not SOURCE_SHA_PATTERN.fullmatch(sha):
        failures.append("invalid upstream snapshot SHA")
    for path in ("canonical_training_index", "canonical_foundations_index",
                 "canonical_rubric", "production_gates"):
        if not local_exists(data.get(path)):
            failures.append(f"broken canonical reference: {path}")
    tracks = data.get("tracks", [])
    if not isinstance(tracks, list):
        return failures + ["tracks must be list"]
    ids = [t.get("id") for t in tracks]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED_IDS:
        failures.append("topic IDs missing or duplicated")
    module_counts = Counter()
    for t in tracks:
        ident = t.get("id", "<unknown>")
        if t.get("status") != "CURRICULUM_ONLY" or (
                t.get("execution_evidence") != "NOT_RUN_REAL_MODEL_OR_PRODUCTION"):
            failures.append(f"{ident}: unsupported execution/maturity claim")
        if not t.get("title") or not isinstance(t.get("title"), str):
            failures.append(f"{ident}: missing title")
        for key in ("guide", "practice"):
            if not local_exists(t.get(key)):
                failures.append(f"{ident}: invalid {key} file")
        mods = t.get("modules")
        if not isinstance(mods, list) or not mods:
            failures.append(f"{ident}: missing module connections")
        else:
            for module in mods:
                if not re.fullmatch(r"M(?:0[1-9]|1[0-2])", module):
                    failures.append(f"{ident}: invalid module {module}")
                else:
                    module_counts[module] += 1
                    if not local_exists(f"LLM-Training/modules/{module}.md"):
                        failures.append(f"{ident}: module missing {module}")
        concepts = t.get("concepts")
        if not isinstance(concepts, list) or len(concepts) < 4:
            failures.append(f"{ident}: fewer than 4 core concepts")
        aliases = t.get("aliases")
        if not isinstance(aliases, list) or len(aliases) < 2:
            failures.append(f"{ident}: missing query aliases")
        official = t.get("official_sources")
        if not isinstance(official, list) or not official:
            failures.append(f"{ident}: no authoritative source URLs")
        else:
            for link in official:
                url = urlparse(link)
                if url.scheme != "https" or not url.netloc:
                    failures.append(f"{ident}: expected HTTPS official source")
        upstream_path = t.get("upstream_path", "")
        upstream_url = t.get("upstream_url", "")
        if not isinstance(upstream_path, str) or not upstream_path or ".." in upstream_path:
            failures.append(f"{ident}: invalid upstream path")
        if (not isinstance(upstream_url, str) or
                f"/blob/{sha}/{upstream_path}" not in upstream_url):
            failures.append(f"{ident}: upstream URL not pinned to snapshot")
    for module in ("M02", "M06", "M10", "M11"):
        if not module_counts[module]:
            failures.append(f"critical module {module} has no application track")
    if check_repo_docs:
        guides = {
            "README": ROOT / "LLM-Training/application-engineering/README.md",
            "ATLAS": ROOT / "LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md",
            "EVAL": ROOT / "LLM-Training/application-engineering/RAGAS-EVALUATION.md",
        }
        texts = {name: path.read_text(encoding="utf-8") for name, path in guides.items()}
        for name in ("RAG", "Ragas", "Harness", "Context", "Prompt"):
            if name not in texts["README"]:
                failures.append(f"application README missing {name}")
        if "application-engineering/README.md" not in texts["ATLAS"]:
            failures.append("six-domain atlas missing application hub backlink")
        if "lm-evaluation-harness" not in texts["EVAL"]:
            failures.append("runtime/evaluation harness distinction missing")
        if "RAG" not in texts["EVAL"] or "Ragas" not in texts["EVAL"]:
            failures.append("RAG/Ragas terminology missing")
    return failures


def main() -> int:
    try:
        data = load()
        failures = validate(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"APPLICATION INDEX ERROR: {exc}", file=sys.stderr)
        return 1
    for issue in failures:
        print(f"APPLICATION INDEX ERROR: {issue}", file=sys.stderr)
    print(f"APPLICATION ENGINEERING QA: tracks={len(data['tracks'])}, "
          f"concepts={sum(len(t['concepts']) for t in data['tracks'])}, "
          f"issues={len(failures)}")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
