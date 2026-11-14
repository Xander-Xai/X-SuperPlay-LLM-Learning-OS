"""Offline coverage and consistency QA for bounded LLM curriculum.

Validates index references, canon learning levels and known contradiction regressions.
Does not validate external HTTP resources or actual GPU/user mastery.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "LLM-Training/index/foundation-coverage.json"
VIEW = ROOT / "LLM-Training/index/FOUNDATION-COVERAGE.md"
MODULE_IDS = {f"M{i:02d}" for i in range(1, 13)}
REQUIRED_LABELS = {"L0": "定位", "L1": "理解", "L2": "实现",
                   "L3": "诊断", "L4": "迁移"}
ALLOWED_STATES = {"CURRICULUM_POINTER_ONLY"}
REQUIRED_TOPICS = {
    "M01.04": "条件概率和最大似然",
    "M01.06": "信息熵/KL/BPB/PPL",
    "M02.02": "BPE/WordPiece/Unigram",
    "M02.07": "数据许可/Privacy/PII",
    "M03.01": "Encoder-only/Decoder-only/Encoder-Decoder",
    "M03.04": "Causal Mask 的未来隔离",
    "M04.05": "Checkpoints 完整训练状态",
    "M05.03": "灾难性遗忘与通用能力",
    "M06.02": "真实 Chat Template Generation 区间",
    "M07.02": "Reference Policy 与 DPO beta",
    "M08.04": "GRPO Group Advantage/Zero Variance",
    "M09.04": "DDP 与 FSDP/ZeRO",
    "M10.06": "置信区间/Wilson/Paired Bootstrap",
    "M11.06": "API Key 与全路径网关鉴权",
    "M12.03": "VLM/图文音视频对齐",
}
REQUIRED_GUIDES = [
    "LLM-Training/fundamentals/CORE-MATH-PROBABILITY-STATISTICS.md",
    "LLM-Training/data-engineering/TOKENIZER-AND-DATA-FOUNDATIONS.md",
    "LLM-Training/fundamentals/MODEL-FAMILIES-AND-GENERATION.md",
    "LLM-Training/training-systems/REPRODUCIBILITY-AND-EVAL-FOUNDATIONS.md",
    "LLM-Training/assessments/CAPABILITY-RUBRIC.md",
]


def load(path: Path = DATA) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _exists_within(path: object) -> bool:
    if not isinstance(path, str) or not path or path.startswith("/"):
        return False
    target = (ROOT / path).resolve()
    return target.is_relative_to(ROOT) and target.is_file()


CURRENT_WORDING_BLOCKLIST = {
    "README.md": ["12 模块 / 18 需求 / 20 来源", "18 需求 / 20 来源"],
    "LLM-Training/README.md": ["18 张机器索引卡", "20 份权威来源导航"],
    "LLM-Training/ROADMAP-V3-DEMAND-DRIVEN.md": ["12 模块/18 需求索引"],
    "LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md": [
        "**L4 生产**", "**L4 真实生产**", "**L3 迁移**"],
    "LLM-Training/demand-driven/AI-NATIVE-NEED-ROUTES.md": [
        "L3 陌生任务迁移 → L4", "L4 适用场景的生产门禁"],
    "LLM-Training/learning-progress.md": ["默认学习节奏："],
    "LLM-Training/modules/M10.md": ["15 条合成结果"],
    "LLM-Training/knowledge-graph/full-training-pipeline.md": [
        "这是学习顺序"],
}


def consistency_wording_issues(contents: dict[str, str]) -> list[str]:
    return [f"{path}: current wording contradiction: {phrase}"
            for path, phrases in CURRENT_WORDING_BLOCKLIST.items()
            for phrase in phrases if phrase in contents.get(path, "")]


def validate(index: dict, view: str | None = None,
             read_repo_docs: bool = True) -> list[str]:
    issues = []
    if not isinstance(index, dict) or index.get("schema_version") != 1:
        return ["foundation coverage version invalid"]
    rows = index.get("topics")
    if not isinstance(rows, list) or len(rows) < 75:
        return ["foundation coverage must include >=75 foundation topic pointers"]
    ids = [x.get("id") for x in rows]
    if len(ids) != len(set(ids)):
        issues.append("duplicate topic IDs")
    counts = Counter()
    for row in rows:
        ident = row.get("id")
        module = row.get("module")
        if module not in MODULE_IDS or not isinstance(ident, str) or not re.fullmatch(
                rf"{module}\.[0-9]{{2}}", ident):
            issues.append(f"invalid module or concept ID: {ident}")
        counts[module] += 1
        for key in ("guide", "practice"):
            if not _exists_within(row.get(key)):
                issues.append(f"{ident}: broken {key} file")
        source = row.get("official_source")
        if not isinstance(source, str):
            issues.append(f"{ident}: source URL is not string")
        else:
            uri = urlparse(source)
            if uri.scheme != "https" or not uri.netloc:
                issues.append(f"{ident}: expected HTTPS official source")
        if not isinstance(row.get("title"), str) or not row["title"].strip():
            issues.append(f"{ident}: empty title")
        if row.get("availability") not in ALLOWED_STATES:
            issues.append(f"{ident}: invalid claimed completion state")
        if row.get("practice_evidence") != "NOT_VERIFIED_FOR_THIS_TOPIC":
            issues.append(f"{ident}: false practice verification status")
    for mid in MODULE_IDS:
        if counts[mid] < 5:
            issues.append(f"{mid}: fewer than five foundation topics")
        if not _exists_within(f"LLM-Training/modules/{mid}.md"):
            issues.append(f"{mid}: module file missing")
    lookup = {row.get("id"): row.get("title") for row in rows}
    for concept, expected in REQUIRED_TOPICS.items():
        if lookup.get(concept) != expected:
            issues.append(f"{concept}: essential concept missing or redefined")
    if not _exists_within(index.get("canonical_levels_doc")):
        issues.append("canonical L0-L4 rubric missing")
    if not _exists_within(index.get("runtime_governance_doc")):
        issues.append("production gate document missing")
    for guide in REQUIRED_GUIDES:
        if not _exists_within(guide):
            issues.append(f"foundational reference missing: {guide}")
    if view is not None:
        for ident in ids:
            if not isinstance(ident, str) or view.count(f"| {ident} |") != 1:
                issues.append(f"{ident}: coverage table not 1:1 with JSON")
    if read_repo_docs:
        rubric = (ROOT / "LLM-Training/assessments/CAPABILITY-RUBRIC.md").read_text(encoding="utf-8")
        loop = (ROOT / "LLM-Training/learning-method/AI-NATIVE-LEARNING-LOOP.md").read_text(encoding="utf-8")
        atlas = (ROOT / "LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md").read_text(encoding="utf-8")
        for mid, term in REQUIRED_LABELS.items():
            for name, content in (("rubric", rubric), ("AI learning loop", loop)):
                line = next((x for x in content.splitlines() if x.startswith("| ") and mid in x.split("|")[1]), "")
                if term not in line:
                    issues.append(f"{name}: {mid} canonical meaning inconsistent ({term})")
        if "L4 真实上线" in loop or "**L4 真实上线**" in atlas:
            issues.append("L4 wrongly equated to mandatory production")
        if "这是学习顺序" in (ROOT / "LLM-Training/knowledge-graph/full-training-pipeline.md").read_text(encoding="utf-8"):
            issues.append("training lifecycle incorrectly called learning order")
        if "15 条合成结果" in (ROOT / "LLM-Training/modules/M10.md").read_text(encoding="utf-8"):
            issues.append("M10 fixture count stale: 15 vs actual 16")
        contents = {path: (ROOT / path).read_text(encoding="utf-8")
                    for path in CURRENT_WORDING_BLOCKLIST}
        issues.extend(consistency_wording_issues(contents))
        if "CI 待执行" in (ROOT / "LLM-Training/labs/tiny-gpt/README.md").read_text(encoding="utf-8"):
            issues.append("TinyGPT README stale CI pending status")
    return issues


def main() -> int:
    try:
        index = load()
        table = VIEW.read_text(encoding="utf-8")
        issues = validate(index, table)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FOUNDATION QA: fatal error: {exc}", file=sys.stderr)
        return 1
    for issue in issues:
        print(f"FOUNDATION ERROR: {issue}", file=sys.stderr)
    print(f"FOUNDATION QA: concepts={len(index['topics'])}, modules={len(MODULE_IDS)}, issues={len(issues)}")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
