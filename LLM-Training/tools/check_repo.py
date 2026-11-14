"""Offline repository QA: check required learning files and relative Markdown links.

Run from any cwd: python LLM-Training/tools/check_repo.py
Does not make network requests or validate external URLs or model training.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
REQUIRED = [
    "README.md", "LICENSE", "LLM-Training/README.md", "LLM-Training/ROADMAP-V2.md",
    "LLM-Training/knowledge-graph/full-training-pipeline.md",
    "LLM-Training/knowledge-graph/pretrain-posttrain-relations.md",
    "LLM-Training/knowledge-graph/concept-dependencies.md",
    "LLM-Training/evaluation/evaluation-protocol.md",
    "LLM-Training/experiments/EXPERIMENT-TEMPLATE.md",
    "LLM-Training/ACCEPTANCE-V2.md",
    "LLM-Training/ROADMAP-V3-DEMAND-DRIVEN.md",
    "LLM-Training/demand-driven/README.md",
    "LLM-Training/demand-driven/DEMAND-CARD-TEMPLATE.md",
    "LLM-Training/demand-driven/worked-demand-cards.md",
    "LLM-Training/knowledge-graph/dependency-and-capability-map.md",
    "LLM-Training/production/PRODUCTION-READINESS.md",
    "LLM-Training/labs/capability-ladder.md",
    "LLM-Training/assessments/CAPABILITY-RUBRIC.md",
    "LLM-Training/resources/AUTHORITATIVE-INDEX.md",
    "LLM-Training/index/learning-index.json",
    "LLM-Training/index/README.md",
    "LLM-Training/index/UPSTREAM-DOWNSTREAM.md",
    "LLM-Training/tools/route_learning.py",
    "LLM-Training/tools/validate_learning_index.py",
    "LLM-Training/tools/test_learning_index.py",
    "LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md",
    "LLM-Training/resources/UPSTREAM-RESOURCE-MAP.md",
    "LLM-Training/demand-driven/AI-NATIVE-NEED-ROUTES.md",
    "LLM-Training/learning-method/AI-NATIVE-LEARNING-LOOP.md",
    "LLM-Training/index/upstream-knowledge-index.json",
    "LLM-Training/index/upstream-path-manifest.json",
    "LLM-Training/tools/route_atlas.py",
    "LLM-Training/tools/validate_atlas.py",
    "LLM-Training/tools/test_atlas.py",
    "LLM-Training/fundamentals/CORE-MATH-PROBABILITY-STATISTICS.md",
    "LLM-Training/data-engineering/TOKENIZER-AND-DATA-FOUNDATIONS.md",
    "LLM-Training/fundamentals/MODEL-FAMILIES-AND-GENERATION.md",
    "LLM-Training/training-systems/REPRODUCIBILITY-AND-EVAL-FOUNDATIONS.md",
    "LLM-Training/index/foundation-coverage.json",
    "LLM-Training/index/FOUNDATION-COVERAGE.md",
    "LLM-Training/tools/route_foundations.py",
    "LLM-Training/tools/test_route_foundations.py",
    "LLM-Training/tools/validate_foundation_coverage.py",
    "LLM-Training/tools/test_foundation_coverage.py",
    "LLM-Training/ACCEPTANCE-FOUNDATION-CONSISTENCY-20261114.md",
    "LLM-Training/labs/tiny-gpt/README.md",
    "LLM-Training/labs/tiny-gpt/tiny_gpt.py",
    "LLM-Training/labs/tiny-gpt/test_tiny_gpt.py",
    "LLM-Training/experiments/EXPERIMENTS-A-E-CROSSWALK.md",
    "LLM-Training/learning-method/SIX-CAPABILITY-UNITS.md",
    "LLM-Training/knowledge-graph/TRAINING-SIGNAL-AND-LIFECYCLE.md",
    "LLM-Training/resources/TRAINING-SOURCE-ROLES.md",
    "LLM-Training/ACCEPTANCE-TRAINING-ROADMAP-20261114.md",
    "LLM-Training/resources/OFFICIAL-RUNTIME-DELTA-20261114.md",
    "LLM-Training/ACCEPTANCE-RECHECK-20261114.md",
    "LLM-Training/ACCEPTANCE-FULL-STACK-20261114.md",
    "LLM-Training/ACCEPTANCE-V3-AUDIT.md",
    "LLM-Training/labs/preference-rl-math/README.md",
    "LLM-Training/labs/preference-rl-math/alignment_math.py",
    "LLM-Training/labs/preference-rl-math/test_alignment_math.py",
    "LLM-Training/labs/task-evaluation/README.md",
    "LLM-Training/labs/task-evaluation/evaluate.py",
    "LLM-Training/labs/task-evaluation/synthetic_cases.json",
    "LLM-Training/labs/task-evaluation/test_evaluate.py",
    "LLM-Training/labs/synthetic-tool-gateway/README.md",
    "LLM-Training/labs/synthetic-tool-gateway/gateway.py",
    "LLM-Training/labs/synthetic-tool-gateway/run_demo.py",
    "LLM-Training/labs/synthetic-tool-gateway/test_gateway.py",
    "LLM-Training/experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md",
    "LLM-Training/labs/toy_train.py", "LLM-Training/labs/test_toy_train.py",
    *[f"LLM-Training/modules/M{i:02d}.md" for i in range(1, 13)],
    *[f"LLM-Training/experiments/{i:02d}-{slug}/README.md" for i, slug in [
        (1, "minimind-whitebox"), (2, "qwen-cpt-replay"),
        (3, "agent-tool-sft"), (4, "dpo"), (5, "grpo"), (6, "deployment"),
    ]],
]


def main() -> int:
    failures = [f"Missing required file: {p}" for p in REQUIRED if not (ROOT / p).is_file()]
    markdown = list(ROOT.rglob("*.md"))
    local_links = 0
    for file in markdown:
        content = file.read_text(encoding="utf-8")
        for raw in LINK.findall(content):
            href = raw.strip().split(" ", 1)[0].strip("<>")
            if not href or href.startswith(("#", "http:", "https:", "mailto:", "data:")):
                continue
            local_links += 1
            path_part = unquote(href.split("#", 1)[0].split("?", 1)[0])
            target = ((ROOT if path_part.startswith("/") else file.parent) / path_part.lstrip("/")).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                failures.append(f"Broken local link: {file.relative_to(ROOT)} -> {raw}")
    for i in range(1, 7):
        exp = ROOT / f"LLM-Training/experiments/{i:02d}-{['minimind-whitebox','qwen-cpt-replay','agent-tool-sft','dpo','grpo','deployment'][i-1]}/README.md"
        if not exp.exists():
            continue
        content = exp.read_text(encoding="utf-8")
        status = re.search(r"(?m)^\*\*状态：\s*(NOT RUN|RUNNING|PASS|FAIL|INCONCLUSIVE)\*\*", content)
        if not status:
            failures.append(f"Experiment missing an explicit supported status: {exp.relative_to(ROOT)}")
        elif status.group(1) in {"PASS", "FAIL", "INCONCLUSIVE"} and "## 实际运行证据" not in content:
            failures.append(f"Experiment marked {status.group(1)} without evidence heading: {exp.relative_to(ROOT)}")
    required_depth_markers = [
        "## V3 深入：", "### 机制：", "### 大白话：", "### 可执行学习任务",
        "**失败注入 / 负例：**", "**模块主参考", "**本次能力退出门槛：**",
    ]
    for i in range(1, 13):
        path = ROOT / f"LLM-Training/modules/M{i:02d}.md"
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for marker in required_depth_markers:
            if marker not in content:
                failures.append(f"Module M{i:02d} missing V3 depth section: {marker}")
    for issue in failures:
        print("ERROR:", issue, file=sys.stderr)
    print(f"Documentation QA: markdown={len(markdown)}, local_links={local_links}, required={len(REQUIRED)}, issues={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

