"""Offline scaffold regression checks: uv run scripts/test_learning_scaffold.py."""

import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "skills/learning/create-learning-repo/scripts/scaffold.py"


def sample_plan():
    return {
        "repo_name": "query-basics", "goal": "Answer questions about a single table.",
        "goal_check": "Answer three new analysis questions with correct SQL and explain the results.",
        "sections": [{"name": "Querying", "arc": "Select rows, then summarise them.", "modules": [
            {"name": "Selection", "chapters": [{
                "name": "Filter rows", "purpose": "Select relevant records for analysis.",
                "serves": "The filtering part of the final analysis.",
                "depth": "Write and explain predicates; omit query optimisation.",
                "topics": [{"name": "WHERE", "covers": ["predicates", "NULL handling"],
                            "depth": "Explain which rows survive."}],
                "completion_check": "Filter an unfamiliar table and explain NULL handling.",
                "effort": "1–2 hours", "enables": ["Summarise rows"],
            }]},
            {"name": "Aggregation", "chapters": [{
                "name": "Summarise rows", "purpose": "Produce totals for selected records.",
                "serves": "The summary part of the final analysis.", "depth": "Single-table aggregates.",
                "topics": ["COUNT", "SUM"], "builds_on": ["Filter rows"],
                "completion_check": "Compute and verify totals against a hand-worked example.",
            }]},
        ]}],
    }


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.out = self.root / "repo"

    def run_helper(self, plan, *flags):
        source = self.root / "plan.json"
        source.write_text(json.dumps(plan), encoding="utf-8")
        return subprocess.run(["uv", "run", "--python", sys.executable, "python", str(HELPER), str(source), "--out", str(self.out), *flags],
                              capture_output=True, text=True, timeout=10)

    def assert_links_exist(self):
        for file in self.out.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                path, _, anchor = target.partition("#")
                resolved = file.parent / path
                self.assertTrue(resolved.is_file(), (file, target))
                if anchor == "brief":
                    self.assertIn("## Brief", resolved.read_text())

    def test_dry_run(self):
        result = self.run_helper(sample_plan(), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.out.exists())

    def test_default_roadmap_and_briefs(self):
        plan = sample_plan()
        result = self.run_helper(plan)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(self.out.rglob("*.md"))), 9)
        roadmap = (self.out / "PLAN.md").read_text()
        self.assertIn(plan["goal_check"], roadmap)
        self.assertIn("NULL handling", roadmap)
        self.assertIn("1–2 hours", roadmap)
        for ch in [m["chapters"][0] for m in plan["sections"][0]["modules"]]:
            self.assertIn(ch["purpose"], roadmap)
            self.assertIn(ch["completion_check"], roadmap)
            self.assertIn(ch["completion_check"], (self.out / "progress.md").read_text())
        for file in self.out.rglob("practice.md"):
            content = file.read_text()
            self.assertIn("Completion check:", content)
            self.assertIn("learning.md#brief", content)
            self.assertIn('tiers: ["Junior", "Senior"]', content)
            self.assertEqual(content.count("## Task "), 2)
        self.assert_links_exist()

    def test_selection_profiles_and_counts(self):
        for profile in ("technical", "craft", "practice", "exam", "custom"):
            with self.subTest(profile=profile):
                self.out = self.root / profile
                plan = sample_plan()
                plan.update(profile=profile, chapter_files=["quizzies", "learning"],
                            counts={"quizzies": 2}, tier_count=1)
                if profile == "custom":
                    plan["tiers"] = [["Starter", "Complete a guided task."], ["Independent", "Complete a new task."]]
                result = self.run_helper(plan)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(list(self.out.rglob("*.md"))), 7)
                self.assertFalse(list(self.out.rglob("practice.md")))
                self.assertNotIn("practice.md", (self.out / "progress.md").read_text())
                for quiz in self.out.rglob("quizzies.md"):
                    self.assertEqual(quiz.read_text().count("## Q "), 2)
                self.assert_links_exist()

    def test_invalid_dependencies_fail_before_writing(self):
        cases = [("builds_on", ["Missing"]), ("builds_on", ["Filter rows"]),
                 ("builds_on", ["Summarise rows"]), ("builds_on", "Filter rows"),
                 ("enables", ["Missing"])]
        for field, refs in cases:
            with self.subTest(field=field, refs=refs):
                plan = sample_plan()
                plan["sections"][0]["modules"][0]["chapters"][0][field] = refs
                result = self.run_helper(plan)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(self.out.exists())
        plan = sample_plan()
        modules = plan["sections"][0]["modules"]
        modules[0]["chapters"].append(copy.deepcopy(modules[0]["chapters"][0]))
        result = self.run_helper(plan)
        self.assertIn("ambiguous", result.stderr)
        self.assertFalse(self.out.exists())

    def test_invalid_selection_and_structure(self):
        for selection in ([], ["practice"], ["learning", "unknown"], ["learning", "learning"], "learning"):
            plan = sample_plan()
            plan["chapter_files"] = selection
            self.assertNotEqual(self.run_helper(plan).returncode, 0)
            self.assertFalse(self.out.exists())
        plan = sample_plan()
        plan["sections"] = ["wrong type"]
        result = self.run_helper(plan)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_exam_defaults_and_custom_ladder(self):
        plan = sample_plan()
        plan["profile"] = "exam"
        self.assertEqual(self.run_helper(plan).returncode, 0)
        for file in self.out.rglob("practice.md"):
            self.assertEqual(file.read_text().count("## Drill "), 3)
            self.assertIn('tiers: ["Recall", "Applied"]', file.read_text())
        self.out = self.root / "custom"
        plan.update(profile="custom", chapter_files=["learning"],
                    tiers=[["Starter", "Complete a guided task."], ["Independent", "Complete a new task."],
                           ["Teacher", "Explain a solution to a peer."]])
        self.assertEqual(self.run_helper(plan).returncode, 0)
        for file in self.out.rglob("learning.md"):
            self.assertIn('tiers: ["Starter", "Independent", "Teacher"]', file.read_text())
            self.assertNotIn("**This chapter:**", file.read_text())
        self.assert_links_exist()

    def test_cycle_and_backward_enables(self):
        plan = sample_plan()
        second = plan["sections"][0]["modules"][1]["chapters"][0]
        second["enables"] = ["Filter rows"]
        result = self.run_helper(plan)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("appearing later", result.stderr)
        self.assertFalse(self.out.exists())

    def test_old_plan_and_preservation(self):
        plan = sample_plan()
        del plan["goal_check"]
        for module in plan["sections"][0]["modules"]:
            del module["chapters"][0]["completion_check"]
        plan["chapter_files"] = ["learning", "examples", "practice", "interview", "thought_leadership", "quizzies"]
        plan["tier_count"] = 4
        result = self.run_helper(plan)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("completion_check", result.stdout)
        self.assertEqual(len(list(self.out.rglob("*.md"))), 15)
        file = next(self.out.rglob("practice.md"))
        file.write_text("Learner work", encoding="utf-8")
        plan["chapter_files"] = ["learning"]
        self.assertEqual(self.run_helper(plan).returncode, 0)
        self.assertEqual(file.read_text(), "Learner work")
        self.assertTrue(list(self.out.rglob("interview.md")))


if __name__ == "__main__":
    unittest.main()
