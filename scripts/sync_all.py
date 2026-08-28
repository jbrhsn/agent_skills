#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Sync skills, agents, and plugins to OpenCode, IBM Bob, Antigravity, and Claude Code."""

import argparse
import subprocess
import sys
from pathlib import Path

import plugins as plug

SCRIPTS_DIR = Path(__file__).resolve().parent

TARGETS = {
    # plugins before agents: --verify inspects resolved tools, which needs runtime installed
    "opencode": ["sync_opencode_skills.py", "sync_opencode_plugins.py", "sync_opencode_agents.py"],
    "bob": ["sync_bob_skills.py"],
    "antigravity": ["sync_antigravity_skills.py", "sync_antigravity_agents.py"],
    "claude": ["sync_claude_skills.py", "sync_claude_agents.py"],
}
PLUGIN_AWARE = {"sync_opencode_agents.py", "sync_opencode_plugins.py"}
VERIFY_AWARE = {
    "sync_opencode_skills.py",
    "sync_opencode_agents.py",
    "sync_bob_skills.py",
    "sync_antigravity_skills.py",
    "sync_antigravity_agents.py",
    "sync_claude_skills.py",
    "sync_claude_agents.py",
}


def run_sync(script_name: str, args: argparse.Namespace) -> int:
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.plugins and script_name in PLUGIN_AWARE:
        cmd += ["--plugins", args.plugins]
    if args.verify and script_name in VERIFY_AWARE:
        cmd.append("--verify")
    print(f"\n{'=' * 79}\nRunning: {script_name}\n{'=' * 79}\n", flush=True)
    return subprocess.run(cmd, cwd=SCRIPTS_DIR.parent).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    parser.add_argument("--plugins", default="", help="Comma-separated plugins to install (OpenCode only)")
    parser.add_argument("--list-plugins", action="store_true", help="List available plugins and exit")
    parser.add_argument("--verify", action="store_true", help="Check resolved agent config after syncing")
    group = parser.add_mutually_exclusive_group()
    for target in TARGETS:
        group.add_argument(f"--{target}-only", action="store_true", help=f"Sync only to {target.title()}")
    args = parser.parse_args()

    if args.list_plugins:
        available = plug.discover_plugins()
        print("Available plugins:\n" if available else "No plugins found.")
        for name, manifest in available.items():
            print(f"  {name}\n    {manifest['description']}")
        return 0

    active_targets = [t for t in TARGETS if getattr(args, f"{t}_only")] or list(TARGETS.keys())
    print("🔄 Syncing to global configs...")

    exit_code = 0
    for target in active_targets:
        for script in TARGETS[target]:
            if run_sync(script, args) != 0:
                exit_code = 1

    print(f"\n{'=' * 79}\n✅ All syncs complete!\n{'=' * 79}\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
