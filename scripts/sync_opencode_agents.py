#!/usr/bin/env python3
"""Sync OpenCode agents from agent_skills repo to ~/.config/opencode/agent."""

import shutil
import sys
from pathlib import Path
from common import REPO_ROOT, get_dest, parse_dry_run_args


def sync_agents(dest_dir: Path, dry_run: bool = False) -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    agents_dir = REPO_ROOT / "agents"
    agent_files = sorted(p for p in agents_dir.glob("*/*.md") if p.name != "README.md")

    print("🔄 Syncing OpenCode agents...")
    print(f"  Source:      {agents_dir}\n  Destination: {dest_dir}\n")
    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = 0, 0
    for src in agent_files:
        if dry_run:
            print(f"→ Would sync: {src.name}")
            synced += 1
            continue
        try:
            shutil.copy2(src, dest_dir / src.name)
            print(f"✓ {src.name}")
            synced += 1
        except Exception as e:
            print(f"✗ {src.name}: {e}")
            skipped += 1

    mode_str = "🔍 DRY RUN: No files were modified" if dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} agents\n  Skipped: {skipped} agents\n")
    print(f"📍 OpenCode agents: {dest_dir}")
    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    args = parse_dry_run_args("Sync OpenCode agents to ~/.config/opencode/agent")
    dest = get_dest("OPENCODE_AGENTS", ".config/opencode/agent")
    sys.exit(sync_agents(dest, args.dry_run))
