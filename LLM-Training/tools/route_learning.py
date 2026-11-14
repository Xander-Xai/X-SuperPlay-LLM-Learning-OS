"""Read-only CLI for demand-driven entrypoints.

Examples:
  python LLM-Training/tools/route_learning.py --list
  python LLM-Training/tools/route_learning.py --id tool-calling
  python LLM-Training/tools/route_learning.py --search 延迟
Only indexes manually curated concepts; never queries users' private repositories.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index" / "learning-index.json"


def get_catalog(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def select(data: dict, demand_id: str | None, search: str | None) -> list[dict]:
    records = data["demands"]
    if demand_id:
        return [item for item in records if item["id"] == demand_id]
    if search:
        needle = search.casefold().strip()
        if not needle:
            return []
        return [d for d in records if needle in (d["id"] + " " + d["problem"]).casefold()]
    return records


def pretty(demand: dict, catalog: dict) -> str:
    module_lookup = {m["id"]: m for m in catalog["modules"]}
    source_lookup = {s["id"]: s for s in catalog["sources"]}
    lines = [
        f"需求：{demand['problem']}  [{demand['id']}]",
        f"学习状态：{demand['status']}（并非实际训练结果）",
        "入口：" + demand["entry"],
        "模块（按症状建议的排查顺序，不是课程前后顺序）：",
    ]
    for mid in demand["modules"]:
        m = module_lookup[mid]
        lines.append(f"  - {mid} {m['title']} → {m['path']}")
    lines.append("主要来源：")
    for src in demand["sources"]:
        s = source_lookup[src]
        lines.append(f"  - {s['title']}: {s['url']}")
    lines.append("实践：" + demand["practice"])
    lines.append("上线时需核查门禁：" + ", ".join(demand["gates"]))
    return "\n".join(lines)


def main() -> int:
    cli = argparse.ArgumentParser(description="Demand → LLM learning entry (offline)")
    group = cli.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="show all IDs and demand names")
    group.add_argument("--id", help="select exact demand ID")
    group.add_argument("--search", help="substring search within known demand titles")
    args = cli.parse_args()
    data = get_catalog()
    hits = select(data, args.id, args.search)
    if args.list:
        print("\n".join(f"{x['id']:25s} {x['problem']}" for x in hits))
        return 0
    if not hits:
        print("未命中当前需求卡。查看 --list，再按模板添加新需求；不要臆造匹配结果。")
        return 2
    print("\n\n".join(pretty(d, data) for d in hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

