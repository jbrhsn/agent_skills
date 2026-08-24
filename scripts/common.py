"""Shared utilities and constants for agent_skills sync scripts."""

import argparse
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUSIONS = {
    ".venv",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
    ".git",
    "*.egg-info",
    "dist",
    "build",
}


def get_dest(env_var: str, default_relpath: str) -> Path:
    """Get destination directory, respecting environment variable overrides."""
    val = os.environ.get(env_var)
    return Path(val).expanduser() if val else Path.home() / default_relpath


def discover_skills() -> list[Path]:
    """Find all skill directories containing a SKILL.md file, sorted by name."""
    return sorted((p.parent for p in (REPO_ROOT / "skills").glob("**/SKILL.md")), key=lambda p: p.name)


def sync_skills(target_name: str, dest_dir: Path, dry_run: bool = False) -> int:
    """Sync all discovered skills to target destination."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    skills = discover_skills()

    print(f"🔄 Syncing {target_name} skills...")
    print(f"  Source:      {REPO_ROOT}")
    print(f"  Destination: {dest_dir}\n")

    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = 0, 0
    for src in skills:
        name = src.name
        dest = dest_dir / name
        if dry_run:
            print(f"→ Would sync: {name}")
            synced += 1
            continue

        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*EXCLUSIONS))
            print(f"✓ {name}")
            synced += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            skipped += 1

    mode_str = "🔍 DRY RUN: No files were modified" if dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} skills\n  Skipped: {skipped} skills\n")
    print(f"📍 {target_name} skills: {dest_dir}")
    print(f"   Installed: {len(list(dest_dir.glob('*')))}/{len(skills)} skills")
    return 0 if skipped == 0 else 1


def parse_dry_run_args(description: str) -> argparse.Namespace:
    """Parse common --dry-run CLI argument."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    return parser.parse_args()
