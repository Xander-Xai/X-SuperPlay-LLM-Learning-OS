"""Delete only SHA-pinned reviewed branches after independently verifying GitHub state.

No force pushes, broad wildcard matching, credentials in source, or production calls.
This tool is invoked once on a push to main with GITHUB_TOKEN contents:write.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

EXPECTED_REPO = "Xander-Xai/X-SuperPlay-LLM-Learning-OS"
SELF_REF = "chore/safe-retire-merged-branches-20261115"
MANIFEST = Path(__file__).with_name("branch-retirement-manifest.json")


def eligibility(candidate, branch, pr, comparison, open_prs, repo=EXPECTED_REPO):
    """Returns (safe_to_delete, reason); fail closed on every unknown state."""
    name, sha = candidate["branch"], candidate["expected_sha"]
    if name == "main" or name.startswith("refs/"):
        return False, "unsafe-name"
    if branch is None:
        return False, "already-absent"
    if branch.get("name") != name or branch.get("protected"):
        return False, "wrong-or-protected-branch"
    if branch.get("commit", {}).get("sha") != sha:
        return False, "sha-changed"
    for x in open_prs:
        head = x.get("head") or {}
        source = head.get("repo") or {}
        if head.get("ref") == name and source.get("full_name", "").lower() == repo.lower():
            return False, "referenced-by-open-pr"
    if "merged_pr" in candidate:
        if not pr or pr.get("number") != candidate["merged_pr"]:
            return False, "missing-pr"
        head = pr.get("head") or {}
        source = head.get("repo") or {}
        if (pr.get("state") != "closed" or not pr.get("merged_at")
            or head.get("ref") != name or head.get("sha") != sha
            or source.get("full_name", "").lower() != repo.lower()):
            return False, "not-merged-or-pr-head-mismatch"
        return True, "pr-" + str(candidate["merged_pr"])
    if candidate.get("ancestor_of") == "main":
        if (comparison and comparison.get("ahead_by") == 0
            and comparison.get("status") in ("behind", "identical")):
            return True, "ancestor-of-main"
        return False, "unmerged-commits"
    return False, "invalid-evidence-type"


class GitHub:
    def __init__(self, repo, token):
        if repo != EXPECTED_REPO or not token:
            raise ValueError("Missing token or unexpected repository")
        self.repo, self.token = repo, token

    def api(self, method, path, *, absent_ok=False):
        url = "https://api.github.com/repos/" + self.repo + "/" + path
        req = Request(url, method=method, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "learning-os-branch-retirement",
        })
        try:
            with urlopen(req, timeout=20) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except HTTPError as exc:
            if exc.code == 404 and absent_ok:
                return None
            details = exc.read().decode("utf-8", errors="replace")[:300]
            raise RuntimeError(f"HTTP {exc.code} for {method} {path}: {details}") from exc

    def branch(self, name):
        return self.api("GET", "branches/" + quote(name, safe=""), absent_ok=True)

    def pr(self, number):
        return self.api("GET", "pulls/" + str(number))

    def compare(self, name):
        return self.api("GET", "compare/main..." + quote(name, safe=""))

    def pull_requests(self, state):
        all_prs = []
        for page in range(1, 51):
            items = self.api("GET", f"pulls?state={state}&per_page=100&page={page}")
            all_prs.extend(items)
            if len(items) < 100:
                return all_prs
        raise RuntimeError("PR pagination limit reached")

    def delete(self, name):
        if name == "main" or name.startswith("refs/"):
            raise RuntimeError("Never delete default branch")
        self.api("DELETE", "git/refs/heads/" + quote(name, safe="/"))
        if self.branch(name) is not None:
            raise RuntimeError("Branch still present after deletion: " + name)


def load_manifest():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = data["candidates"]
    if data.get("schema_version") != 1 or not items:
        raise ValueError("Unexpected manifest format")
    names = [i["branch"] for i in items]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate candidates")
    for item in items:
        if item["branch"] == "main" or len(item.get("expected_sha", "")) != 40:
            raise ValueError("Unsafe SHA or branch")
        if ("merged_pr" in item) == ("ancestor_of" in item):
            raise ValueError("Exactly one evidence type required")
    return items


def audit(api, item, open_prs):
    name = item["branch"]
    branch = api.branch(name)
    pr = api.pr(item["merged_pr"]) if branch and "merged_pr" in item else None
    comparison = api.compare(name) if branch and item.get("ancestor_of") else None
    return eligibility(item, branch, pr, comparison, open_prs, repo=api.repo)


def main(argv=None):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply and (os.environ.get("GITHUB_EVENT_NAME") != "push"
                       or os.environ.get("GITHUB_REF") != "refs/heads/main"):
        raise RuntimeError("Deletion requires a main push GitHub Actions event")
    api = GitHub(os.environ.get("GITHUB_REPOSITORY", ""), os.environ.get("GITHUB_TOKEN", ""))
    items = load_manifest()
    open_prs = api.pull_requests("open")
    errors = []
    summary = ["## Safe branch retirement", "", "| Branch | Status | Evidence |", "|---|---|---|"]
    for item in items:
        name = item["branch"]
        safe, reason = audit(api, item, open_prs)
        if args.apply and safe:
            # Immediately re-read PRs and branch head. Any new commit/PR => skip.
            safe, reason = audit(api, item, api.pull_requests("open"))
            if safe:
                try:
                    api.delete(name)
                    reason = "deleted-and-readback-confirmed"
                except Exception as exc:
                    safe, reason = False, "delete-failed: " + str(exc)
        elif not safe and reason == "already-absent":
            reason = "previously-deleted"
        if not safe and reason not in ("already-absent", "previously-deleted"):
            errors.append(name + ": " + reason)
        print(name + ": " + ("DONE" if reason in ("deleted-and-readback-confirmed", "previously-deleted") else "CHECK")
              + " (" + reason + ")")
        summary.append("| " + name + " | " + ("DONE" if reason in ("deleted-and-readback-confirmed", "previously-deleted") else "CHECK")
                       + " | " + reason + " |")

    # Exact one-branch exception: remove the branch which merged this script.
    if args.apply and not errors:
        own = api.branch(SELF_REF)
        if own:
            matched = None
            for pr in api.pull_requests("closed"):
                head = pr.get("head") or {}
                source = head.get("repo") or {}
                if (head.get("ref") == SELF_REF and head.get("sha") == own["commit"]["sha"]
                    and source.get("full_name", "").lower() == api.repo.lower() and pr.get("merged_at")):
                    matched = pr
                    break
            if matched:
                item = {"branch": SELF_REF, "expected_sha": own["commit"]["sha"],
                        "merged_pr": matched["number"]}
                safe, reason = audit(api, item, api.pull_requests("open"))
                if safe:
                    api.delete(SELF_REF)
                    summary.append("| own cleanup branch | DONE | merged PR and readback |")
                    print("CONFIRMED DELETED: " + SELF_REF)
                else:
                    errors.append(SELF_REF + ": " + reason)
            else:
                errors.append(SELF_REF + ": merged PR not visible yet")
    summary.extend(["", "Mode: " + ("APPLY" if args.apply else "DRY-RUN"),
                    "Unresolved: " + str(len(errors)), "GPU/LLM experiment status is unaffected."])
    out = os.environ.get("GITHUB_STEP_SUMMARY")
    if out:
        with open(out, "a", encoding="utf-8") as file:
            file.write("\n".join(summary) + "\n")
    for e in errors:
        print("UNRESOLVED: " + e, file=sys.stderr)
    return int(args.apply and bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
