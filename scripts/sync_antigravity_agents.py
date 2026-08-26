#!/usr/bin/env python3
"""Sync the canonical Antigravity global agent instructions to ~/.gemini/config/AGENTS.md."""

import sys
from pathlib import Path

from common import REPO_ROOT, get_dest, parse_dry_run_args

SOURCE = REPO_ROOT / "agents" / "ANTIGRAVITY_AGENTS.md"


def sync(dest: Path, dry_run: bool = False) -> int:
    print("🔄 Syncing Antigravity global agent instructions...")
    print(f"  Source:      {SOURCE}\n  Destination: {dest}\n")
    if dry_run:
        print(f"→ Would write: {dest}")
        print("\n🔍 DRY RUN: No files were modified")
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(SOURCE.read_text())
    print(f"✓ {dest.name}\n\n✅ Sync complete!\n📍 Antigravity AGENTS.md: {dest}")
    return 0


if __name__ == "__main__":
    args = parse_dry_run_args("Sync Antigravity global agent instructions to ~/.gemini/config/AGENTS.md")
    sys.exit(sync(get_dest("ANTIGRAVITY_AGENTS", ".gemini/config/AGENTS.md"), args.dry_run))
