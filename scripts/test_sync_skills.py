"""Regression checks for manifest-scoped skill synchronization."""

import json
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import common  # noqa: E402


class SkillSyncManifestTests(unittest.TestCase):
    def test_excludes_project_temp_directory(self):
        self.assertTrue(common.is_excluded(Path("skill/.temp/reusable-check.py")))
        self.assertFalse(common.is_excluded(Path("skill/scripts/reusable-check.py")))

    def test_prunes_only_manifest_owned_folders(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            (destination / "retired-skill").mkdir()
            (destination / "retired-skill" / "SKILL.md").write_text("retired")
            (destination / "user-skill").mkdir()
            (destination / "user-skill" / "SKILL.md").write_text("user")
            common.write_skill_manifest(destination, {"retired-skill", "missing-skill"})

            removed = common.prune_stale_skills(destination, {"current-skill"})

            self.assertEqual(removed, ["retired-skill"])
            self.assertFalse((destination / "retired-skill").exists())
            self.assertTrue((destination / "user-skill").is_dir())

    def test_dry_run_leaves_manifest_owned_folder_intact(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            (destination / "retired-skill").mkdir()
            common.write_skill_manifest(destination, {"retired-skill"})

            removed = common.prune_stale_skills(destination, set(), dry_run=True)

            self.assertEqual(removed, ["retired-skill"])
            self.assertTrue((destination / "retired-skill").is_dir())

    def test_rejects_duplicate_flattened_names(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for category in ("one", "two"):
                skill = root / "skills" / category / "duplicate"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("---\nname: duplicate\ndescription: test\n---\n")

            with patch.object(common, "REPO_ROOT", root):
                with self.assertRaisesRegex(ValueError, "Duplicate flattened skill name"):
                    common.discover_skills()

    def test_manifest_uses_only_simple_folder_names(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            (destination / common.SKILL_MANIFEST_NAME).write_text(json.dumps({"folders": ["valid", "../invalid", 3]}))

            self.assertEqual(common.read_skill_manifest(destination), {"valid"})

    def test_verify_allows_unmanaged_skill_folders(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "skills" / "category" / "canonical"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("canonical")
            destination = root / "destination"
            destination.mkdir()
            (destination / "canonical").mkdir()
            (destination / "canonical" / "SKILL.md").write_text("canonical")
            (destination / "user-skill").mkdir()
            (destination / "user-skill" / "SKILL.md").write_text("user")

            with patch.object(common, "REPO_ROOT", root), redirect_stdout(StringIO()):
                self.assertEqual(common.verify_skills("Test", destination), 0)


if __name__ == "__main__":
    unittest.main()
