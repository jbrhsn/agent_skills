#!/usr/bin/env python3
"""Sync all skills to OpenCode, IBM Bob, Antigravity, and Claude Code global configs."""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

TARGETS = {
    "opencode": ["sync_opencode_skills.py", "sync_opencode_agents.py", "sync_opencode_plugins.py"],
    "bob": ["sync_bob_skills.py"],
    "antigravity": ["sync_antigravity_skills.py"],
    "claude": ["sync_claude_skills.py"],
}


def run_sync(script_name: str, dry_run: bool = False) -> int:
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)]
    if dry_run:
        cmd.append("--dry-run")
    print(f"\n{'=' * 79}\nRunning: {script_name}\n{'=' * 79}\n")
    return subprocess.run(cmd, cwd=SCRIPTS_DIR.parent).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync skills to OpenCode, IBM Bob, Antigravity, and Claude Code")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    group = parser.add_mutually_exclusive_group()
    for target in TARGETS:
        group.add_argument(f"--{target}-only", action="store_true", help=f"Sync only to {target.title()}")
    args = parser.parse_args()

    active_targets = [t for t in TARGETS if getattr(args, f"{t}_only")] or list(TARGETS.keys())
    print("🔄 Syncing skills to global configs...")

    exit_code = 0
    for target in active_targets:
        for script in TARGETS[target]:
            if run_sync(script, args.dry_run) != 0:
                exit_code = 1

    print(f"\n{'=' * 79}\n✅ All syncs complete!\n{'=' * 79}\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
