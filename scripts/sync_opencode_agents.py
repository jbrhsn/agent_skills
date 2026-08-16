#!/usr/bin/env python3
"""
Sync OpenCode agents from the agent_skills repository to the global OpenCode config.

This script copies the agent definition files from the source repository to
~/.config/opencode/agent (note: OpenCode discovers agents from the singular
`agent/` directory), excluding documentation (README.md).

Usage:
    python scripts/sync_opencode_agents.py [--dry-run]
    python scripts/sync_opencode_agents.py --help

Environment:
    OPENCODE_AGENTS: Override the destination path (default: ~/.config/opencode/agent)
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


AGENTS = [
    ("orchestrator_mode_agents", "orchestrator.md"),
    ("orchestrator_mode_agents", "executor.md"),
    ("ask_mode_agents", "ask.md"),
]

EXCLUSIONS = [
    "README.md",
]


def get_dest_dir() -> Path:
    """Get the destination directory, respecting OPENCODE_AGENTS env var."""
    env_path = os.environ.get("OPENCODE_AGENTS")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / ".config" / "opencode" / "agent"


def sync_agent(source_path: Path, agent_name: str, dest_dir: Path, dry_run: bool = False) -> bool:
    """
    Sync a single agent file from source to destination.

    Args:
        source_path: Full path to the agent file in the source repo
        agent_name: File name of the agent (e.g., "orchestrator.md")
        dest_dir: Destination directory (e.g., ~/.config/opencode/agent)
        dry_run: If True, don't actually copy files

    Returns:
        True if sync successful, False otherwise
    """
    if agent_name in EXCLUSIONS:
        return True

    if not source_path.is_file():
        print(f"⚠ Skip: {agent_name} (not found at {source_path})")
        return False

    dest_path = dest_dir / agent_name

    if dry_run:
        print(f"→ Would sync: {agent_name}")
        return True

    try:
        shutil.copy2(source_path, dest_path)
        print(f"✓ {agent_name}")
        return True
    except Exception as e:
        print(f"✗ {agent_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync OpenCode agents to ~/.config/opencode/agent",
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

    print("🔄 Syncing OpenCode agents...")
    print(f"  Source:      {repo_root / 'agents'}")
    print(f"  Destination: {dest_dir}")
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)")
        print()

    synced = 0
    skipped = 0

    for agent_dir, agent_name in AGENTS:
        source_path = repo_root / "agents" / agent_dir / agent_name

        if sync_agent(source_path, agent_name, dest_dir, args.dry_run):
            synced += 1
        else:
            skipped += 1

    print()
    if args.dry_run:
        print("🔍 DRY RUN: No files were modified")
    else:
        print("✅ Sync complete!")
    print(f"  Synced:  {synced} agents")
    print(f"  Skipped: {skipped} agents")
    print()
    print(f"📍 OpenCode agents: {dest_dir}")

    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
