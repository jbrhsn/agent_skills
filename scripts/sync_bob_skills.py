#!/usr/bin/env python3
"""
Sync IBM Bob skills from the agent_skills repository to the global Bob config.

This script copies all skills from the source repository to ~/.bob/skills,
excluding build artifacts (.venv, __pycache__, etc.) to save space.

Usage:
    python scripts/sync_bob_skills.py [--dry-run]
    python scripts/sync_bob_skills.py --help

Environment:
    BOB_SKILLS: Override the destination path (default: ~/.bob/skills)
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILLS = [
    "agent_session_management/end-session",
    "agent_session_management/init-session",
    "content-creation/linkedin-medium/carousel-builder",
    "content-creation/linkedin-medium/content-tracker",
    "content-creation/linkedin-medium/draft-builder",
    "content-creation/linkedin-medium/editorial-reviewer",
    "content-creation/linkedin-medium/linkedin-writer",
    "content-creation/linkedin-medium/medium-imager",
    "content-creation/linkedin-medium/medium-writer",
    "content-creation/linkedin-medium/seed-expander",
    "content-creation/linkedin-medium/tutorial-verifier",
    "content-creation/linkedin-medium/voice-profiler",
    "development/lean-coder",
    "development/project-planner",
    "development/repo-docs-publisher",
    "development/ui-ux-designer",
    "learning/author-chapter",
    "learning/create-learning-repo",
    "learning/generate-practice-exam",
]

EXCLUSIONS = [
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
]


def get_dest_dir() -> Path:
    """Get the destination directory, respecting BOB_SKILLS env var."""
    env_path = os.environ.get("BOB_SKILLS")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / ".bob" / "skills"


def sync_skill(source_path: Path, skill_name: str, dest_dir: Path, dry_run: bool = False) -> bool:
    """
    Sync a single skill from source to destination.

    Args:
        source_path: Full path to the skill in the source repo
        skill_name: Short name of the skill (e.g., "medium-imager")
        dest_dir: Destination directory (e.g., ~/.bob/skills)
        dry_run: If True, don't actually copy files

    Returns:
        True if sync successful, False otherwise
    """
    if not source_path.is_dir():
        print(f"⚠ Skip: {skill_name} (not found at {source_path})")
        return False

    dest_path = dest_dir / skill_name

    if dry_run:
        print(f"→ Would sync: {skill_name}")
        return True

    # Remove old destination
    if dest_path.exists():
        shutil.rmtree(dest_path)

    # Copy with exclusions
    try:
        dest_path.mkdir(parents=True, exist_ok=True)

        for item in source_path.iterdir():
            # Skip excluded items
            if item.name in EXCLUSIONS or any(
                item.name.endswith(ext.lstrip("*")) for ext in EXCLUSIONS if ext.startswith("*")
            ):
                continue

            if item.is_dir():
                shutil.copytree(item, dest_path / item.name, ignore=shutil.ignore_patterns(*EXCLUSIONS))
            else:
                shutil.copy2(item, dest_path / item.name)

        print(f"✓ {skill_name}")
        return True
    except Exception as e:
        print(f"✗ {skill_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync IBM Bob skills to ~/.bob/skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be synced without modifying files",
    )
    args = parser.parse_args()

    # Determine source and destination
    repo_root = Path(__file__).parent.parent
    dest_dir = get_dest_dir()

    dest_dir.mkdir(parents=True, exist_ok=True)

    print("🔄 Syncing IBM Bob skills...")
    print(f"  Source:      {repo_root}")
    print(f"  Destination: {dest_dir}")
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)")
        print()

    synced = 0
    skipped = 0

    for skill_path in SKILLS:
        source_path = repo_root / skill_path
        skill_name = skill_path.split("/")[-1]

        if sync_skill(source_path, skill_name, dest_dir, args.dry_run):
            synced += 1
        else:
            skipped += 1

    print()
    if args.dry_run:
        print("🔍 DRY RUN: No files were modified")
    else:
        print("✅ Sync complete!")
    print(f"  Synced:  {synced} skills")
    print(f"  Skipped: {skipped} skills")
    print()
    print(f"📍 Bob skills: {dest_dir}")
    print(f"   Installed: {len(list(dest_dir.glob('*')))}/{len(SKILLS)} skills")

    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
