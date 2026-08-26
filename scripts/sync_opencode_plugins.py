#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Sync OpenCode plugin runtime files to ~/.config/opencode/plugin."""

import argparse
import shutil
import sys
from pathlib import Path

import plugins as plug
from common import get_dest


def sync_plugins(dest_dir: Path, selected: list[dict], dry_run: bool = False) -> int:
    files = plug.runtime_files(selected)
    dest_dir.mkdir(parents=True, exist_ok=True)

    print("🔄 Syncing OpenCode plugins...")
    print(f"  Source:      {plug.PLUGINS_DIR}\n  Destination: {dest_dir}")
    print(f"  Plugins:     {', '.join(p['name'] for p in selected) or 'none selected'}\n")
    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = 0, 0
    for owner, src in files:
        if dry_run:
            print(f"→ Would sync: {src.name} ({owner})")
            synced += 1
            continue
        try:
            shutil.copy2(src, dest_dir / src.name)
            print(f"✓ {src.name} ({owner})")
            synced += 1
        except OSError as e:
            print(f"✗ {src.name}: {e}")
            skipped += 1

    for stale in plug.prune(dest_dir, {src.name for _, src in files}, dry_run):
        print(f"{'→ Would remove' if dry_run else '🗑  Removed'} (deselected): {stale}")
    if not dry_run:
        plug.write_manifest(dest_dir, [src.name for _, src in files])

    mode_str = "🔍 DRY RUN: No files were modified" if dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} plugins\n  Skipped: {skipped} plugins\n")
    print(f"📍 OpenCode plugins: {dest_dir}")
    if selected:
        # A plugin tool is allowed by default in every agent, so installing runtime
        # without the matching overlays silently grants it to the orchestrator.
        print("⚠  Run sync_opencode_agents.py with the same --plugins, or use sync_all.py.")
    return 0 if skipped == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync OpenCode plugins to ~/.config/opencode/plugin")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    parser.add_argument("--plugins", default="", help="Comma-separated plugin names to install")
    args = parser.parse_args()

    try:
        selected = plug.select_plugins([n.strip() for n in args.plugins.split(",") if n.strip()])
        for plugin in selected:
            plug.validate(plugin)
    except ValueError as e:
        print(f"✗ {e}")
        return 1

    return sync_plugins(get_dest("OPENCODE_PLUGINS", ".config/opencode/plugin"), selected, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
