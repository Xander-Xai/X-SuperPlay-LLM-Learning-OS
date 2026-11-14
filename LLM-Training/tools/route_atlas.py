"""Offline navigation: six domains, 33 topics, 12 entry needs, pinned official sources.

Not a semantic AI retriever, not a live sync, no network, models or user files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
INDEX = HERE / "index" / "upstream-knowledge-index.json"
REPO = "https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS"


def load(path: Path = INDEX) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def match_topics(data: dict, text: str) -> list[dict]:
    term = text.strip().casefold()
    if not term:
        return []
    return [t for t in data["topics"] if any(term in part.casefold() for part in
        [t["id"], t["title"], t["definition"], t["plain"], *t["aliases"]])]


def match_needs(data: dict, text: str) -> list[dict]:
    term = text.strip().casefold()
    if not term:
        return []
    return [n for n in data["needs"] if any(term in part.casefold()
            for part in [n["id"], n["problem"], *n["keywords"]])]


def topic_details(data: dict, topic: dict) -> str:
    sources = {s["id"]: s for s in data["official_sources"]}
    base = f"{REPO}/blob/{data['snapshot']['sha']}/"
    out = [
        f"[{topic['id']}] {topic['title']}  域：{topic['domain']}",
        "专业原理：" + topic["definition"],
        "大白话：" + topic["plain"],
        "最小实践：" + topic["practice"],
        "相关专项模块：" + "、".join(topic["modules"]),
        "上游原始资料（固定 SHA）：",
        *(f"  {base}{p}" for p in topic["upstream"]),
        "官方/原始资料：",
        *(f"  {sources[sid]['title']}: {sources[sid]['url']}" for sid in topic["sources"]),
        "证据边界：课程导航，不代表学习者掌握、模型运行或生产就绪。",
    ]
    return "\n".join(out)


def need_details(data: dict, need: dict) -> str:
    topics = {t["id"]: t for t in data["topics"]}
    ids = need["topics"]
    out = [f"[{need['id']}] {need['problem']}",
           "入口详情：LLM-Training/demand-driven/AI-NATIVE-NEED-ROUTES.md",
           "建议按需查看（并非强制前置顺序）：" +
           " → ".join(f"{x} {topics[x]['title']}" for x in ids),
           "关键词：" + "、".join(need["keywords"]),
           "学习证据：先不训练基线→单点实验→负例→独立迁移/停止。"]
    return "\n".join(out)




def topic_relations(data: dict, topic_id: str) -> list[dict]:
    """Incoming AND outgoing typed relations; no asserted prerequisites."""
    return [r for r in data["relations"]
            if r["from"] == topic_id or r["to"] == topic_id]


def shortest_relation_path(data: dict, start: str, goal: str) -> list[dict] | None:
    """Shortest *undirected exploration* route over typed relationships.

    Walking an edge backwards never changes that edge's stored direction.
    This is for understanding how concepts connect, NOT a topological learning
    order or a claim that all edges are prerequisites.
    """
    from collections import deque

    ids = {t["id"] for t in data["topics"]}
    if start not in ids or goal not in ids:
        return None
    if start == goal:
        return []
    adjacency = {tid: [] for tid in ids}
    for relation in data["relations"]:
        adjacency[relation["from"]].append((relation["to"], relation))
        adjacency[relation["to"]].append((relation["from"], relation))
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        current, steps = queue.popleft()
        for neighbor, rel in adjacency[current]:
            if neighbor in visited:
                continue
            result = steps + [rel]
            if neighbor == goal:
                return result
            visited.add(neighbor)
            queue.append((neighbor, result))
    return None


def relation_summary(data: dict, topic_id: str) -> str:
    topics = {t["id"]: t["title"] for t in data["topics"]}
    if topic_id not in topics:
        return "未知主题；使用 --list 查看真实 ID。"
    lines = [f"[{topic_id}] {topics[topic_id]} 的关联关系",
             "关系箭头为原始语义方向，不表示必修顺序；逆向查询不颠倒原关系。"]
    rels = topic_relations(data, topic_id)
    if not rels:
        lines.append("本索引目前没有声明关联边；不是说技术上毫无关系。")
    for r in rels:
        position = "出边" if r["from"] == topic_id else "入边"
        lines.append(
            f"  {position}: {r['from']} {topics[r['from']]} --{r['type']}-->"
            f" {r['to']} {topics[r['to']]} | {r['explain']}"
        )
    return "\n".join(lines)


def path_summary(data: dict, start: str, goal: str) -> str | None:
    topics = {t["id"]: t["title"] for t in data["topics"]}
    steps = shortest_relation_path(data, start, goal)
    if steps is None:
        return None
    lines = [
        f"知识关联路径：{start} {topics[start]} ⇢ {goal} {topics[goal]}",
        "警告：按无向连通性查找最短探索路径；以下每个边显示原始方向。",
        "它只揭示概念关联，不证明先修关系、最佳学习顺序或实际实验效果。",
    ]
    if not steps:
        lines.append("起点和终点相同，不需要跨节点。")
    for i, r in enumerate(steps, 1):
        lines.append(
            f"  {i}. {r['from']} --{r['type']}--> {r['to']}：{r['explain']}"
        )
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description="Offline LLM all-stack atlas route")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="all domains/topics")
    group.add_argument("--topic", help="exact topic ID e.g. A04")
    group.add_argument("--domain", help="domain ID F/S/P/E/A/O")
    group.add_argument("--need", help="exact demand card ID e.g. N02")
    group.add_argument("--search", help="substring topic/name/aliases or demand keyword")
    group.add_argument("--relate", help="show incoming/outgoing typed edges for topic ID")
    group.add_argument("--path", nargs=2, metavar=("FROM", "TO"),
                       help="explore shortest graph connection; NOT prerequisites")
    args = parser.parse_args()
    data = load()
    domains = {d["id"]: d for d in data["domains"]}
    topics = {t["id"]: t for t in data["topics"]}
    needs = {n["id"]: n for n in data["needs"]}
    if args.relate:
        key = args.relate.upper()
        if key not in topics:
            print("未知主题；使用 --list 查看真实 ID。")
            return 2
        print(relation_summary(data, key))
        return 0
    if args.path:
        start, goal = (x.upper() for x in args.path)
        result = path_summary(data, start, goal)
        if result is None:
            print("没有收录这两个主题之间的连通路径（或 ID 无效）。不能编造概念关系。")
            return 2
        print(result)
        return 0
    if args.list:
        for domain in data["domains"]:
            print(f"\n[{domain['id']}] {domain['name']}")
            for t in data["topics"]:
                if t["domain"] == domain["id"]:
                    print(f"  {t['id']:4s} {t['title']}")
        print("\n[需求卡] " + "、".join(needs))
        return 0
    if args.topic:
        t = topics.get(args.topic.upper())
        if not t:
            print("未找到主题；用 --list 查看目录。")
            return 2
        print(topic_details(data, t))
        return 0
    if args.domain:
        key = args.domain.upper()
        if key not in domains:
            print("未知域；只能使用 F/S/P/E/A/O。")
            return 2
        print(f"[{key}] {domains[key]['name']}")
        for t in data["topics"]:
            if t["domain"] == key:
                print(topic_details(data, t) + "\n")
        return 0
    if args.need:
        n = needs.get(args.need.upper())
        if not n:
            print("未知需求；用 --list 查看目录。")
            return 2
        print(need_details(data, n))
        for tid in n["topics"]:
            print("\n" + topic_details(data, topics[tid]))
        return 0
    hits = match_topics(data, args.search)
    needs_hit = match_needs(data, args.search)
    if not hits and not needs_hit:
        print("无已编目的关键词命中；这不是语义搜索。可按需求卡模板手工增补，不猜测用户意图。")
        return 2
    print(f"命中主题 {len(hits)}，需求卡 {len(needs_hit)}。")
    for n in needs_hit[:12]:
        print("\n" + need_details(data, n))
    for t in hits[:25]:
        print("\n" + topic_details(data, t))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
