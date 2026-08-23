#!/usr/bin/env python3
"""
Sync OpenCode skills from the agent_skills repository to the global OpenCode config.

This script copies all skills from the source repository to ~/.config/opencode/skills,
excluding build artifacts (.venv, __pycache__, etc.) to save space.

Usage:
    python scripts/sync_opencode_skills.py [--dry-run]
    python scripts/sync_opencode_skills.py --help

Environment:
    OPENCODE_SKILLS: Override the destination path (default: ~/.config/opencode/skills)
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILLS = [
    "skills/agent_session_management/end-session",
    "skills/agent_session_management/init-session",
    "skills/content-creation/Linkedin/linkedin-post-writer",
    "skills/content-creation/Linkedin/linkedin-image-prompts",
    "skills/content-creation/Medium/medium-article-writer",
    "skills/content-creation/Medium/medium-image-prompts",
    "skills/content-creation/Medium/medium-article-brainstorm",
    "skills/content-creation/Common/keyword-research",
    "skills/development/lean-coder",
    "skills/development/project-planner",
    "skills/development/repo-docs-publisher",
    "skills/development/ui-ux-designer",
    "skills/learning/author-chapter",
    "skills/learning/create-learning-repo",
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
    """Get the destination directory, respecting OPENCODE_SKILLS env var."""
    env_path = os.environ.get("OPENCODE_SKILLS")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / ".config" / "opencode" / "skills"


def sync_skill(source_path: Path, skill_name: str, dest_dir: Path, dry_run: bool = False) -> bool:
    """
    Sync a single skill from source to destination.

    Args:
        source_path: Full path to the skill in the source repo
        skill_name: Short name of the skill (e.g., "medium-imager")
        dest_dir: Destination directory (e.g., ~/.config/opencode/skills)
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

    # Copy directory tree, excluding build artifacts
    try:
        shutil.copytree(source_path, dest_path, ignore=shutil.ignore_patterns(*EXCLUSIONS))
        print(f"✓ {skill_name}")
        return True
    except Exception as e:
        print(f"✗ {skill_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync OpenCode skills to ~/.config/opencode/skills",
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

    print("🔄 Syncing OpenCode skills...")
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
    print(f"📍 OpenCode skills: {dest_dir}")
    print(f"   Installed: {len(list(dest_dir.glob('*')))}/{len(SKILLS)} skills")

    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
