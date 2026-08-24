#!/usr/bin/env python3
"""Sync OpenCode plugins from agent_skills repo to ~/.config/opencode/plugin."""

import shutil
import sys
from pathlib import Path
from common import REPO_ROOT, get_dest, parse_dry_run_args


def sync_plugins(dest_dir: Path, dry_run: bool = False) -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    plugins_dir = REPO_ROOT / "plugins" / "token_saving"
    plugins = sorted(plugins_dir.glob("*.ts")) if plugins_dir.is_dir() else []

    print("🔄 Syncing OpenCode plugins...")
    print(f"  Source:      {plugins_dir}\n  Destination: {dest_dir}\n")
    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    if not plugins:
        print("⚠ No plugin (*.ts) files found to sync")

    synced, skipped = 0, 0
    for src in plugins:
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
    print(f"\n{mode_str}\n  Synced:  {synced} plugins\n  Skipped: {skipped} plugins\n")
    print(f"📍 OpenCode plugins: {dest_dir}")
    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    args = parse_dry_run_args("Sync OpenCode plugins to ~/.config/opencode/plugin")
    dest = get_dest("OPENCODE_PLUGINS", ".config/opencode/plugin")
    sys.exit(sync_plugins(dest, args.dry_run))
