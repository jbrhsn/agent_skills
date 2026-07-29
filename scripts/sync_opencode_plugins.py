#!/usr/bin/env python3
"""
Sync OpenCode plugins from the agent_skills repository to the global OpenCode config.

This script copies all TypeScript plugin files from the source repository to
~/.config/opencode/plugin (note: OpenCode discovers plugins from the singular
`plugin/` directory), excluding documentation (README.md and other markdown).

Usage:
    python scripts/sync_opencode_plugins.py [--dry-run]
    python scripts/sync_opencode_plugins.py --help

Environment:
    OPENCODE_PLUGINS: Override the destination path (default: ~/.config/opencode/plugin)
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


EXCLUSIONS = [
    "README.md",
]


def get_dest_dir() -> Path:
    """Get the destination directory, respecting OPENCODE_PLUGINS env var."""
    env_path = os.environ.get("OPENCODE_PLUGINS")
    if env_path:
        return Path(env_path).expanduser()
    return Path.home() / ".config" / "opencode" / "plugin"


def discover_plugins(plugins_dir: Path) -> list[Path]:
    """Find all *.ts plugin files in the source dir, sorted for stable output."""
    if not plugins_dir.is_dir():
        return []
    return sorted(p for p in plugins_dir.glob("*.ts") if p.name not in EXCLUSIONS)


def sync_plugin(source_path: Path, plugin_name: str, dest_dir: Path, dry_run: bool = False) -> bool:
    """
    Sync a single plugin file from source to destination.

    Args:
        source_path: Full path to the plugin file in the source repo
        plugin_name: File name of the plugin (e.g., "token-guard.ts")
        dest_dir: Destination directory (e.g., ~/.config/opencode/plugin)
        dry_run: If True, don't actually copy files

    Returns:
        True if sync successful, False otherwise
    """
    if not source_path.is_file():
        print(f"⚠ Skip: {plugin_name} (not found at {source_path})")
        return False

    dest_path = dest_dir / plugin_name

    if dry_run:
        print(f"→ Would sync: {plugin_name}")
        return True

    try:
        shutil.copy2(source_path, dest_path)
        print(f"✓ {plugin_name}")
        return True
    except Exception as e:
        print(f"✗ {plugin_name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync OpenCode plugins to ~/.config/opencode/plugin",
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
    plugins_dir = repo_root / "plugins" / "token_saving"
    dest_dir = get_dest_dir()

    dest_dir.mkdir(parents=True, exist_ok=True)

    print("🔄 Syncing OpenCode plugins...")
    print(f"  Source:      {plugins_dir}")
    print(f"  Destination: {dest_dir}")
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)")
        print()

    plugins = discover_plugins(plugins_dir)

    synced = 0
    skipped = 0

    if not plugins:
        print("⚠ No plugin (*.ts) files found to sync")

    for source_path in plugins:
        plugin_name = source_path.name

        if sync_plugin(source_path, plugin_name, dest_dir, args.dry_run):
            synced += 1
        else:
            skipped += 1

    print()
    if args.dry_run:
        print("🔍 DRY RUN: No files were modified")
    else:
        print("✅ Sync complete!")
    print(f"  Synced:  {synced} plugins")
    print(f"  Skipped: {skipped} plugins")
    print()
    print(f"📍 OpenCode plugins: {dest_dir}")

    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
