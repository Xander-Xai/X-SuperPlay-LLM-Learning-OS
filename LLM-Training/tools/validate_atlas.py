"""Offline integrity contract for the pinned AI-Learning-OS knowledge bridge.

Does not validate that external web URLs currently respond, nor that source
information is universally valid. Upstream file paths were Git-tree checked
at the pinned commit on 2026-11-14; this script checks the frozen manifest.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/"LLM-Training/index/upstream-knowledge-index.json"
MANIFEST=ROOT/"LLM-Training/index/upstream-path-manifest.json"
DOMAINS=set("FSPEAO")
MODULES={f"M{i:02d}" for i in range(1,13)}
RELATION_TYPES={
    "feeds","implements","produces-base-for","provides-baseline","supplies",
    "reduces-cost-of","constrains","accelerates","evaluates","gates",
    "enables","deploys-into","hosts","supplies-evidence","controls-context",
    "supplies-actions","persists","guards","observes","informs-choice",
    "is-cross-cutting-view-of","extends","requires",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def nonblank_unique(items: object) -> bool:
    return isinstance(items,list) and all(isinstance(x,str) and bool(x.strip()) for x in items) and len({x.casefold() for x in items})==len(items)


def validate(data: dict, manifest: dict) -> list[str]:
    bad=[]
    if not isinstance(data,dict) or data.get("schema_version")!=1:
        return ["atlas index schema_version must be 1"]
    snapshot=data.get("snapshot",{})
    if snapshot.get("repo")!="Xander-Xai/X-SuperPlay-AI-Learning-OS":
        bad.append("upstream repository mismatch")
    sha=snapshot.get("sha","")
    if not isinstance(sha,str) or not re.fullmatch(r"[0-9a-f]{40}",sha):
        bad.append("snapshot SHA invalid")
    if manifest.get("verified_sha")!=sha or manifest.get("upstream_repository")!=snapshot.get("repo"):
        bad.append("manifest and snapshot mismatch")
    frozen=manifest.get("paths",[])
    if not nonblank_unique(frozen) or any(x.startswith("/") or x.startswith("..") or "\\" in x for x in frozen):
        bad.append("invalid or duplicate manifest paths")
    paths=set(frozen)
    domains=data.get("domains",[])
    if not isinstance(domains,list) or len(domains)!=6:
        return bad+["expected 6 domains"]
    if {d.get("id") for d in domains}!=DOMAINS:
        bad.append("expected domain IDs F/S/P/E/A/O")
    for d in domains:
        if d.get("upstream") not in paths:
            bad.append(f"domain missing frozen upstream path: {d.get('id')}")
    src=data.get("official_sources",[])
    if not isinstance(src,list) or len(src)<12:
        return bad+["too few official sources"]
    sid=[s.get("id") for s in src]
    if not nonblank_unique(sid):
        bad.append("duplicate official source IDs")
    for s in src:
        url=s.get("url","")
        if not isinstance(url,str) or urlparse(url).scheme!="https" or not urlparse(url).netloc:
            bad.append(f"invalid source URL {s.get('id')}")
    topics=data.get("topics",[])
    if not isinstance(topics,list) or len(topics)<30:
        return bad+["expected >=30 topics"]
    tid=[t.get("id") for t in topics]
    if not nonblank_unique(tid):
        bad.append("duplicate/invalid topic IDs")
    topic_ids=set(tid)
    for t in topics:
        ident=t.get("id")
        if t.get("domain") not in DOMAINS or not isinstance(ident,str) or not re.fullmatch(r"[FSPEAOX][0-9]{2}",ident):
            bad.append(f"invalid domain/topic {ident}")
        if not nonblank_unique(t.get("modules",[])) or any(m not in MODULES for m in t.get("modules",[])):
            bad.append(f"invalid module refs {ident}")
        else:
            for m in t["modules"]:
                if not (ROOT/f"LLM-Training/modules/{m}.md").is_file():
                    bad.append(f"module path missing {m}")
        if not nonblank_unique(t.get("upstream",[])) or not t.get("upstream") or any(p not in paths for p in t["upstream"]):
            bad.append(f"missing/invalid upstream refs {ident}")
        if not nonblank_unique(t.get("sources",[])) or not t.get("sources") or any(s not in sid for s in t["sources"]):
            bad.append(f"missing/invalid official source refs {ident}")
        if not nonblank_unique(t.get("aliases",[])):
            bad.append(f"invalid aliases {ident}")
        for key in ("definition","plain","practice","title"):
            if not isinstance(t.get(key),str) or len(t[key].strip())<6:
                bad.append(f"empty explanation {ident}:{key}")
        if t.get("status")!="CURRICULUM_NOT_LEARNER_VERIFIED":
            bad.append(f"false learner verification status {ident}")
    relations=data.get("relations",[])
    if not isinstance(relations,list) or len(relations)<25:
        bad.append("expected 25+ typed links")
    else:
        seen=set()
        for r in relations:
            pair=(r.get("from"),r.get("to"),r.get("type"))
            if pair in seen or pair[0] not in topic_ids or pair[1] not in topic_ids or pair[2] not in RELATION_TYPES:
                bad.append(f"invalid/duplicate relationship {pair}")
            seen.add(pair)
            if not r.get("explain"):
                bad.append(f"unexplained relationship {pair}")
    needs=data.get("needs",[])
    if not isinstance(needs,list) or len(needs)<10:
        bad.append("expected >=10 demands")
    else:
        nids=[n.get("id") for n in needs]
        if not nonblank_unique(nids):
            bad.append("duplicate demand IDs")
        for n in needs:
            if not nonblank_unique(n.get("topics",[])) or not n.get("topics") or any(x not in topic_ids for x in n["topics"]):
                bad.append(f"dangling demand topics {n.get('id')}")
            if not nonblank_unique(n.get("keywords",[])) or not n.get("keywords"):
                bad.append(f"missing demand keywords {n.get('id')}")
            if n.get("status")!="ROUTING_GUIDE_ONLY":
                bad.append(f"unverified claim in demand {n.get('id')}")
    for key in ("roadmap","full_atlas","resource_guide","need_guide"):
        p=data.get("identity",{}).get(key,"")
        if not isinstance(p,str) or not (ROOT/p).is_file():
            bad.append(f"missing local identity entry {key}")
    return bad


def main() -> int:
    try:
        errors=validate(read_json(INDEX),read_json(MANIFEST))
    except (OSError,json.JSONDecodeError) as e:
        print(f"ATLAS ERROR: {e}",file=sys.stderr)
        return 1
    for e in errors:
        print(f"ATLAS ERROR: {e}",file=sys.stderr)
    print(f"Upstream atlas contract: {len(errors)} issues")
    return int(bool(errors))


if __name__=="__main__":
    raise SystemExit(main())
