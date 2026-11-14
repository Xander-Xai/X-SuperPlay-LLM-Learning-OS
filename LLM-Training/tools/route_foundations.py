"""Offline searchable foundation concept index; no network, inference or live claims."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"index/foundation-coverage.json"


def load(path: Path=INDEX)->dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find(rows: list[dict], query: str)->list[dict]:
    term=query.strip().casefold()
    if not term:
        return []
    return [r for r in rows if term in " ".join((r["id"],r["title"],r["module"])).casefold()]


def describe(row: dict)->str:
    return "\n".join((
        f"[{row['id']}] {row['title']}",
        "所属模块: "+row["module"],
        "专业定义/大白话讲义: "+row["guide"],
        "最小实验/练习计划: "+row["practice"],
        "原始学习资料: "+row["official_source"],
        "证据状态: 仅定位资料/练习；未验证单点学习或真实模型训练",
    ))


def main()->int:
    parser=argparse.ArgumentParser(description="Offline LLM concept search across M01-M12")
    exclusive=parser.add_mutually_exclusive_group(required=True)
    exclusive.add_argument("--search",help="concept text, partial match")
    exclusive.add_argument("--id",help="exact Mxx.nn concept ID")
    exclusive.add_argument("--module",help="M01..M12 (all topics in module)")
    exclusive.add_argument("--list",action="store_true",help="show all topic IDs")
    args=parser.parse_args()
    rows=load()["topics"]
    if args.list:
        for r in rows:print(f"{r['id']} {r['title']}")
        return 0
    if args.id:
        hits=[r for r in rows if r["id"]==args.id.upper()]
    elif args.module:
        hits=[r for r in rows if r["module"]==args.module.upper()]
    else:
        hits=find(rows,args.search)
    if not hits:
        print("没有找到该概念/编号；可查总目录或向索引提需求，不猜测内容。")
        return 2
    print(f"命中 {len(hits)} 个核心主题：")
    for r in hits:
        print("\n"+describe(r))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
