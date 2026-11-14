"""Read-only command line navigation of the demand-driven curriculum.

Try:
  python LLM-Training/tools/route_learning.py --list
  python LLM-Training/tools/route_learning.py --search QLoRA
  python LLM-Training/tools/route_learning.py --search 工具调用
  python LLM-Training/tools/route_learning.py --module M11
  python LLM-Training/tools/route_learning.py --id tool-calling

Static keywords/aliases, NOT semantic search or a live project/recruiting scan.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index" / "learning-index.json"


def get_catalog(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def select(data: dict, demand_id: str | None, search: str | None,
           module_id: str | None = None) -> list[dict]:
    records = data["demands"]
    if demand_id:
        return [item for item in records if item["id"] == demand_id]
    if module_id:
        return [item for item in records if module_id.upper() in item["modules"]]
    if search:
        needle = search.casefold().strip()
        if not needle:
            return []
        modules = {m["id"]: m for m in data["modules"]}
        return [d for d in records if any(
            needle in fragment.casefold() for fragment in (
                [d["id"], d["problem"], *d.get("aliases", [])] +
                [modules[mid]["title"] for mid in d["modules"]]
            )
        )]
    return records


def pretty(demand: dict, catalog: dict) -> str:
    module_lookup = {m["id"]: m for m in catalog["modules"]}
    source_lookup = {s["id"]: s for s in catalog["sources"]}
    labels = catalog["production"]["gate_labels"]
    lines = [
        f"需求：{demand['problem']}  [{demand['id']}]",
        f"学习状态：{demand['status']}（不是实际训练结果）",
        "需求总入口：" + demand["entry"],
        "建议模块（当前症状的排查顺序，非课程顺序）：",
    ]
    for mid in demand["modules"]:
        m = module_lookup[mid]
        refs = "、".join(source_lookup[s]["title"] for s in m.get("sources", []))
        lines.extend([
            f"  - {mid} {m['title']} → {m['path']}",
            f"      首个问题：{m.get('question', '')}",
            f"      实践：{m.get('practice', '')}",
            f"      模块权威资料：{refs}",
        ])
    lines.append("需求主要来源：")
    for sid in demand["sources"]:
        s = source_lookup[sid]
        lines.append(f"  - {s['title']}: {s['url']}")
    lines.append("示范需求卡：" + demand["practice"])
    lines.append("上线时需核查门禁：" + "、".join(f"{g} {labels[g]}" for g in demand["gates"]))
    lines.append("说明：这是手工维护的关键词路由，未自动抓取实时业务或验证学习者能力。")
    return "\n".join(lines)


def main() -> int:
    cli = argparse.ArgumentParser(description="Demand → LLM learning route (offline)")
    group = cli.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="show IDs and demand names")
    group.add_argument("--id", help="exact demand ID")
    group.add_argument("--search", help="title/alias/module-title substring search")
    group.add_argument("--module", help="M01..M12 cross-lookup; e.g. --module M11")
    args = cli.parse_args()
    data = get_catalog()
    if args.module and args.module.upper() not in {m["id"] for m in data["modules"]}:
        print("无效模块编号；使用 M01–M12。")
        return 2
    hits = select(data, args.id, args.search, args.module)
    if args.list:
        print("\n".join(f"{x['id']:25s} {x['problem']}" for x in hits))
        return 0
    if not hits:
        print("未命中已编目的关键词。查看 --list，或按需求卡模板添加新问题；不要猜测结果。")
        return 2
    print("\n\n".join(pretty(d, data) for d in hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

