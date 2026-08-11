#!/usr/bin/env python3
"""
Sync all skills to the OpenCode, IBM Bob, and Antigravity global configs.

This unified script syncs the agent_skills repository to all three targets:
  - ~/.config/opencode/skills, ~/.config/opencode/agent, ~/.config/opencode/plugin (OpenCode)
  - ~/.bob/skills (IBM Bob)
  - ~/.gemini/config/skills (Antigravity)

It runs sync_opencode_skills.py, sync_opencode_agents.py, and
sync_opencode_plugins.py for OpenCode, sync_bob_skills.py for Bob, and
sync_antigravity_skills.py for Antigravity.

Usage:
    python scripts/sync_all.py [--dry-run]
    python scripts/sync_all.py --help

Environment:
    OPENCODE_SKILLS: Override OpenCode destination (default: ~/.config/opencode/skills)
    BOB_SKILLS: Override Bob destination (default: ~/.bob/skills)
    ANTIGRAVITY_SKILLS: Override Antigravity destination (default: ~/.gemini/config/skills)
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
        description="Sync skills to OpenCode, IBM Bob, and Antigravity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be synced without modifying files",
    )
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument(
        "--opencode-only",
        action="store_true",
        help="Sync only to OpenCode (skills, agents, plugins) — skip Bob and Antigravity",
    )
    target_group.add_argument(
        "--bob-only",
        action="store_true",
        help="Sync only to Bob — skip OpenCode and Antigravity",
    )
    target_group.add_argument(
        "--antigravity-only",
        action="store_true",
        help="Sync only to Antigravity — skip OpenCode and Bob",
    )
    args = parser.parse_args()

    # With no *-only flag, every target runs; otherwise only the requested one does.
    only_flag_used = args.opencode_only or args.bob_only or args.antigravity_only
    sync_opencode = not only_flag_used or args.opencode_only
    sync_bob = not only_flag_used or args.bob_only
    sync_antigravity = not only_flag_used or args.antigravity_only

    print("🔄 Syncing skills to global configs...")

    exit_code = 0

    # Sync to OpenCode (skills, agents, and plugins are all OpenCode-global)
    if sync_opencode:
        if run_sync("sync_opencode_skills.py", args.dry_run) != 0:
            exit_code = 1
        if run_sync("sync_opencode_agents.py", args.dry_run) != 0:
            exit_code = 1
        if run_sync("sync_opencode_plugins.py", args.dry_run) != 0:
            exit_code = 1

    # Sync to Bob
    if sync_bob:
        if run_sync("sync_bob_skills.py", args.dry_run) != 0:
            exit_code = 1

    # Sync to Antigravity
    if sync_antigravity:
        if run_sync("sync_antigravity_skills.py", args.dry_run) != 0:
            exit_code = 1

    print(f"\n{'=' * 79}")
    print("✅ All syncs complete!")
    print(f"{'=' * 79}\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
