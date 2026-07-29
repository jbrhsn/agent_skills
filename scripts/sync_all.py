#!/usr/bin/env python3
"""
Sync all skills to both OpenCode and IBM Bob global configs.

This unified script syncs the agent_skills repository to both:
  - ~/.config/opencode/skills, ~/.config/opencode/agent, ~/.config/opencode/plugin (OpenCode)
  - ~/.bob/skills (IBM Bob)

It runs sync_opencode_skills.py, sync_opencode_agents.py, and
sync_opencode_plugins.py for OpenCode, and sync_bob_skills.py for Bob.

Usage:
    python scripts/sync_all.py [--dry-run]
    python scripts/sync_all.py --help

Environment:
    OPENCODE_SKILLS: Override OpenCode destination (default: ~/.config/opencode/skills)
    BOB_SKILLS: Override Bob destination (default: ~/.bob/skills)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_sync(script_name: str, dry_run: bool = False) -> int:
    """Run a sync script and return its exit code."""
    script_path = Path(__file__).parent / script_name
    cmd = [sys.executable, str(script_path)]
    if dry_run:
        cmd.append("--dry-run")

    print(f"\n{'=' * 79}")
    print(f"Running: {script_name}")
    print(f"{'=' * 79}\n")

    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Sync skills to both OpenCode and IBM Bob",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be synced without modifying files",
    )
    parser.add_argument(
        "--opencode-only",
        action="store_true",
        help="Sync only to OpenCode, not Bob",
    )
    parser.add_argument(
        "--bob-only",
        action="store_true",
        help="Sync only to Bob, not OpenCode",
    )
    args = parser.parse_args()

    print("🔄 Syncing skills to global configs...")

    exit_code = 0

    # Sync to OpenCode (skills, agents, and plugins are all OpenCode-global)
    if not args.bob_only:
        if run_sync("sync_opencode_skills.py", args.dry_run) != 0:
            exit_code = 1
        if run_sync("sync_opencode_agents.py", args.dry_run) != 0:
            exit_code = 1
        if run_sync("sync_opencode_plugins.py", args.dry_run) != 0:
            exit_code = 1

    # Sync to Bob
    if not args.opencode_only:
        if run_sync("sync_bob_skills.py", args.dry_run) != 0:
            exit_code = 1

    print(f"\n{'=' * 79}")
    print("✅ All syncs complete!")
    print(f"{'=' * 79}\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
