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
        if exp.exists() and "NOT RUN" not in exp.read_text(encoding="utf-8"):
            failures.append(f"Experiment missing honest NOT RUN marker: {exp.relative_to(ROOT)}")
    for issue in failures:
        print("ERROR:", issue, file=sys.stderr)
    print(f"Documentation QA: markdown={len(markdown)}, local_links={local_links}, required={len(REQUIRED)}, issues={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

