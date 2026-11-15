"""Offline guards for destructive GitHub branch cleanup. No network or tokens."""
import unittest
from retire_merged_branches import eligibility, load_manifest


def branch(name="docs/example", sha="a"*40, protected=False):
    return {"name": name, "commit": {"sha": sha}, "protected": protected}


def merged_pr(name="docs/example", sha="a"*40, number=1):
    return {"number": number, "state": "closed", "merged_at": "2026-11-15T00:00:00Z",
            "head": {"ref": name, "sha": sha,
                     "repo": {"full_name": "Xander-Xai/X-SuperPlay-LLM-Learning-OS"}}}


class BranchRetirementSafetyTests(unittest.TestCase):
    def setUp(self):
        self.record = {"branch": "docs/example", "expected_sha": "a"*40, "merged_pr": 1}

    def check(self, **overrides):
        values = {"candidate": self.record, "branch": branch(), "pr": merged_pr(),
                  "comparison": None, "open_prs": []}
        values.update(overrides)
        return eligibility(**values)

    def test_expected_merged_branch_allowed(self):
        self.assertEqual(self.check(), (True, "pr-1"))

    def test_changed_head_blocked(self):
        self.assertEqual(self.check(branch=branch(sha="b"*40))[1], "sha-changed")

    def test_protected_ref_blocked(self):
        self.assertEqual(self.check(branch=branch(protected=True))[1], "wrong-or-protected-branch")

    def test_merged_pr_mismatch_blocked(self):
        self.assertEqual(self.check(pr=merged_pr(number=2))[1], "missing-pr")
        self.assertEqual(self.check(pr=merged_pr(sha="b"*40))[1], "not-merged-or-pr-head-mismatch")

    def test_open_pr_blocks_even_merged_one(self):
        open_pr = {"head": {"ref": "docs/example", "repo": {
            "full_name": "Xander-Xai/X-SuperPlay-LLM-Learning-OS"}}}
        self.assertEqual(self.check(open_prs=[open_pr])[1], "referenced-by-open-pr")

    def test_no_ref_or_main(self):
        record = {"branch": "main", "expected_sha": "a"*40, "ancestor_of": "main"}
        self.assertEqual(self.check(candidate=record)[1], "unsafe-name")
        self.assertEqual(self.check(branch=None)[1], "already-absent")

    def test_ancestor_requires_no_new_commits(self):
        record = {"branch": "docs/example", "expected_sha": "a"*40, "ancestor_of": "main"}
        self.assertEqual(self.check(candidate=record, pr=None,
                                    comparison={"status": "behind", "ahead_by": 0}),
                         (True, "ancestor-of-main"))
        self.assertEqual(self.check(candidate=record, pr=None,
                                    comparison={"status": "diverged", "ahead_by": 2})[1],
                         "unmerged-commits")

    def test_fixed_manifest(self):
        manifest = load_manifest()
        self.assertEqual(len(manifest), 25)
        self.assertEqual(len({x["branch"] for x in manifest}), 25)
        self.assertEqual(sum("merged_pr" in x for x in manifest), 24)
        self.assertNotIn("main", [x["branch"] for x in manifest])


if __name__ == "__main__":
    unittest.main()
