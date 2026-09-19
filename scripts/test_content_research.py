"""Offline regression checks: uv run scripts/test_content_research.py."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
IDEA = ROOT / "skills/content-creation/Common/idea-research/scripts"
KEYWORDS = ROOT / "skills/content-creation/Common/keyword-research/scripts/kwfetch.sh"
sys.path.insert(0, str(IDEA))
spec = importlib.util.spec_from_file_location("idea_scorer", IDEA / "dedupe_and_score.py")
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.cwd = Path(self.workspace.name)

    def run_helper(self, filename, *args):
        return subprocess.run(
            ["uv", "run", "--no-project", str(IDEA / filename), *args],
            cwd=self.cwd, text=True, capture_output=True, timeout=30,
        )

    def raw(self, records):
        folder = self.cwd / ".idea-research/raw"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "fixture.json").write_text(json.dumps(records))
        return folder

    def item(self, **changes):
        return {"source": "hn", "title": "AI model inference", "url": "https://example.test/story",
                "score": 20, "comments": 2, "created_utc": time.time() - 3600,
                "age_hours": 1, **changes}

    def test_cached_age_and_duplicate_records(self):
        record = self.item(created_utc=time.time() - 10 * 86400)
        folder = self.raw([record, record, {"title": "malformed"}])
        with patch.object(scorer, "RAW_DIR", folder):
            items = scorer.load_raw()
        self.assertEqual(len(items), 1)
        self.assertEqual(scorer.recency_points(items[0]["age_hours"]), 2)

    def test_unknown_timestamp_is_not_cached_recency(self):
        folder = self.raw([self.item(created_utc=None, age_hours=0)])
        with patch.object(scorer, "RAW_DIR", folder):
            self.assertIsNone(scorer.load_raw()[0]["age_hours"])

    def test_keyword_boundaries(self):
        beats = {"AI": {"keywords": ["ai"]}}
        self.assertEqual(scorer.match_beat("Paid chair repairs", beats, []), (None, 0))
        self.assertEqual(scorer.match_beat("AI-assisted tools", beats, []), ("AI", 1))

    def test_traffic_is_not_engagement(self):
        social = self.item()
        trend = self.item(source="trends", score=1000000, comments=0)
        self.assertEqual(scorer.velocity_points([social, trend]), scorer.velocity_points([social]))
        self.assertEqual(scorer.velocity_points([trend]), 0)

    def test_zero_hour_uses_one_hour_floor(self):
        self.assertEqual(
            scorer.velocity_points([self.item(age_hours=0)]),
            scorer.velocity_points([self.item(age_hours=1)]),
        )

    def test_medium_presence_is_not_coverage_quality(self):
        result = scorer.score_cluster({"beat": "AI", "items": [
            {**self.item(source="medium"), "hits": 1},
        ]}, 10)
        self.assertEqual(result["components"]["gap"], 10)
        self.assertFalse(result["gap_checked"])

    def test_rank_preview_and_invalid_overrides(self):
        self.raw([self.item()])
        result = self.run_helper("dedupe_and_score.py", "--dry-run", "--min-score", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / ".idea-research/scored.json").exists())
        for override in ('{"idea-1": 21}', '{"idea-1": "NaN"}', '{"missing": 12}'):
            result = self.run_helper("dedupe_and_score.py", "--gap-overrides", override)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((self.cwd / ".idea-research/scored.json").exists())

    def test_scaffold_preview_create_and_protect(self):
        self.raw([self.item()])
        result = self.run_helper("dedupe_and_score.py", "--min-score", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        args = ("--id", "idea-1", "--root", "articles", "--slug", "chosen")
        result = self.run_helper("scaffold_article.py", *args, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "articles").exists())
        result = self.run_helper("scaffold_article.py", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.cwd / "articles/chosen/source.md"
        before = target.read_text()
        self.assertIn("https://example.test/story", before)
        self.assertNotEqual(self.run_helper("scaffold_article.py", *args).returncode, 0)
        self.assertEqual(target.read_text(), before)
        for slug in ("../escape", "/absolute", "..", "nested/name", ""):
            result = self.run_helper("scaffold_article.py", "--id", "idea-1", "--slug", slug)
            self.assertNotEqual(result.returncode, 0, slug)


@unittest.skipUnless(shutil.which("jq") and shutil.which("bash"), "requires bash and jq")
class KeywordTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.cwd = Path(self.workspace.name)
        curl = self.cwd / "curl"
        curl.write_text('''#!/bin/sh
case "$*" in
  *opensearch*) printf '%s\\n' '["query",["Example"],[],[]]' ;;
  *pageviews*)
    if [ "${TEST_PAGEVIEWS:-missing}" = missing ]; then exit 22; fi
    printf '%s\\n' "$TEST_PAGEVIEWS" ;;
  *) echo "Unexpected network request" >&2; exit 99 ;;
esac
''')
        curl.chmod(0o755)
        self.env = {**os.environ, "PATH": f"{self.cwd}:{os.environ['PATH']}"}

    def run_helper(self, *args):
        return subprocess.run(["bash", str(KEYWORDS), *args], cwd=self.cwd,
                              env=self.env, text=True, capture_output=True, timeout=5)

    def test_preview_writes_nothing(self):
        result = self.run_helper("all", "test", "--dry-run", "-o", "raw.tsv")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.cwd / "raw.tsv").exists())

    def test_missing_and_unknown_arguments_fail_promptly(self):
        for args in (("all", "seed", "-e"), ("all", "seed", "--unknown"),
                     ("all", "seed", "extra"), ("all", "seed", "-o", "--deep")):
            self.assertNotEqual(self.run_helper(*args).returncode, 0)

    def test_pageview_failure_is_not_zero(self):
        result = self.run_helper("entity", "example")
        self.assertNotIn("pageviews\t", result.stdout)
        self.assertIn("unavailable", result.stderr)
        self.env["TEST_PAGEVIEWS"] = '{"items":[{"views":0}]}'
        result = self.run_helper("entity", "example")
        self.assertEqual(result.stdout.strip(), "pageviews\tExample\t0")

    def test_pageview_mean_has_consistent_schema(self):
        self.env["TEST_PAGEVIEWS"] = '{"items":[{"views":10},{"views":20}]}'
        result = self.run_helper("entity", "example")
        self.assertEqual(result.stdout.strip(), "pageviews\tExample\t15")

    def test_grades_distinguish_wikimedia_from_corroboration(self):
        raw = self.cwd / "raw.tsv"
        raw.write_text("wikipedia\tSingle entity\t0\npageviews\tSingle entity\t100\n"
                       "google\tUseful phrase\t1\ndatamuse\tUseful phrase\t20\n"
                       "pageviews\tAnother entity\t0\nbing\tSearch phrase\t2\n")
        result = self.run_helper("score", str(raw))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = {r.split("\t")[0]: r.split("\t")[5]
                for r in result.stdout.splitlines()[1:]}
        self.assertEqual(rows, {"single entity": "B", "useful phrase": "A",
                                "another entity": "B", "search phrase": "C"})


if __name__ == "__main__":
    unittest.main()
