"""Search only registered application-engineering routes. No semantic or internet search."""
from __future__ import annotations
import argparse
from pathlib import Path
import json

INDEX = Path(__file__).resolve().parents[1] / "index/application-engineering-index.json"


def load(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def choose(index: dict, query: str | None = None,
           topic_id: str | None = None, module: str | None = None) -> list[dict]:
    rows = index["tracks"]
    if topic_id:
        return [r for r in rows if r["id"] == topic_id.upper()]
    if module:
        return [r for r in rows if module.upper() in r["modules"]]
    if query:
        q = query.strip().casefold()
        if not q:
            return []
        return [r for r in rows if q in " ".join(
            [r["id"], r["title"]] + r["aliases"] + r["concepts"]).casefold()]
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline RAG/Agent/Harness/Context/Prompt routes")
    args = parser.add_mutually_exclusive_group(required=True)
    args.add_argument("--search")
    args.add_argument("--id")
    args.add_argument("--module")
    args.add_argument("--list", action="store_true")
    parsed = parser.parse_args()
    result = choose(load(), parsed.search, parsed.id, parsed.module)
    if not result:
        print("无命中：仅检索当前已编目的应用工程主题，不猜测结果。")
        return 2
    for item in result:
        print(f"[{item['id']}] {item['title']}")
        print(f"  本仓专业+白话: {item['guide']}")
        print(f"  最小实战: {item['practice']}")
        print(f"  上游完整课程: {item['upstream_url']}")
        print(f"  官方: {item['official_sources'][0]}")
        print("  状态：学习索引，不代表真实 LLM/生产测试。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
