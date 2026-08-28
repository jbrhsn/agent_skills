#!/usr/bin/env python3
"""Sync the canonical Antigravity global agent instructions to ~/.gemini/config/AGENTS.md."""

import sys
from pathlib import Path

from common import REPO_ROOT, file_hash, get_dest, parse_args

SOURCE = REPO_ROOT / "agents" / "ANTIGRAVITY_AGENTS.md"


def sync(dest: Path, dry_run: bool = False, verify: bool = False) -> int:
    print("🔄 Syncing Antigravity global agent instructions...")
    print(f"  Source:      {SOURCE}\n  Destination: {dest}\n")
    if dry_run:
        print(f"→ Would write: {dest}")
        print("\n🔍 DRY RUN: No files were modified")
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(SOURCE.read_text())
    print(f"✓ {dest.name}\n\n✅ Sync complete!\n📍 Antigravity AGENTS.md: {dest}")

    if verify:
        print("\n🔎 Verifying Antigravity AGENTS.md parity...")
        if not dest.exists() or file_hash(SOURCE) != file_hash(dest):
            print("✗ Antigravity AGENTS.md checksum mismatch")
            return 1
        print("✓ AGENTS.md (SHA256 verified)")
        print("✅ Antigravity agent instructions verified (100% parity)")
    return 0


if __name__ == "__main__":
    args = parse_args("Sync Antigravity global agent instructions to ~/.gemini/config/AGENTS.md")
    sys.exit(sync(get_dest("ANTIGRAVITY_AGENTS", ".gemini/config/AGENTS.md"), args.dry_run, args.verify))

