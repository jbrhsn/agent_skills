#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Sync OpenCode agents to ~/.config/opencode/agent, composing selected plugin overlays."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import plugins as plug
from common import get_dest


def flatten_permissions(permission: dict) -> dict[tuple[str, str], str]:
    """{'task': {'executor': 'allow'}} -> {('task', 'executor'): 'allow'}."""
    flat = {}
    for key, value in (permission or {}).items():
        if isinstance(value, dict):
            flat.update({(key, pattern): action for pattern, action in value.items()})
        else:
            flat[(key, "*")] = value
    return flat


def verify_agents(composed: dict[str, str]) -> int:
    """Assert OpenCode's resolved config matches what we composed."""
    print("\n🔎 Verifying against `opencode debug agent`...")
    failures = []
    for filename, content in sorted(composed.items()):
        name = Path(filename).stem
        result = subprocess.run(
            ["opencode", "debug", "agent", name], capture_output=True, text=True, cwd=Path.home()
        )
        if result.returncode != 0:
            failures.append(f"{name}: opencode could not resolve this agent")
            continue
        resolved = {
            (e["permission"], e.get("pattern", "*")): e["action"]
            for e in json.loads(result.stdout).get("permission", [])
        }
        fm, _ = plug.split_frontmatter(content)
        bad = [
            f"{perm}[{pattern}] expected {action}, got {resolved.get((perm, pattern), 'missing')}"
            for (perm, pattern), action in flatten_permissions(fm.get("permission", {})).items()
            if resolved.get((perm, pattern)) != action
        ]
        if bad:
            failures.append(f"{name}: " + "; ".join(bad))
        else:
            print(f"✓ {name}")

    if failures:
        print("\n✗ Verification failed:")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("✅ All agents resolved as composed")
    return 0


def sync_agents(dest_dir: Path, selected: list[dict], dry_run: bool = False, verify: bool = False) -> int:
    composed = plug.compose_agents(selected)
    dest_dir.mkdir(parents=True, exist_ok=True)

    print("🔄 Syncing OpenCode agents...")
    print(f"  Source:      {plug.AGENTS_DIR}\n  Destination: {dest_dir}")
    print(f"  Plugins:     {', '.join(p['name'] for p in selected) or 'none (base agents only)'}\n")
    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = 0, 0
    for filename, content in sorted(composed.items()):
        if dry_run:
            print(f"→ Would sync: {filename}")
            synced += 1
            continue
        try:
            (dest_dir / filename).write_text(content)
            print(f"✓ {filename}")
            synced += 1
        except OSError as e:
            print(f"✗ {filename}: {e}")
            skipped += 1

    for stale in plug.prune(dest_dir, set(composed), dry_run):
        print(f"{'→ Would remove' if dry_run else '🗑  Removed'} (deselected): {stale}")
    if not dry_run:
        plug.write_manifest(dest_dir, list(composed))

    mode_str = "🔍 DRY RUN: No files were modified" if dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} agents\n  Skipped: {skipped} agents\n")
    print(f"📍 OpenCode agents: {dest_dir}")

    if skipped:
        return 1
    return verify_agents(composed) if verify and not dry_run else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync OpenCode agents to ~/.config/opencode/agent")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    parser.add_argument("--plugins", default="", help="Comma-separated plugin names whose overlays to apply")
    parser.add_argument("--verify", action="store_true", help="Check resolved config via `opencode debug agent`")
    parser.add_argument("--print-composed", metavar="AGENT", help="Print one composed agent and exit")
    args = parser.parse_args()

    try:
        selected = plug.select_plugins([n.strip() for n in args.plugins.split(",") if n.strip()])
        for plugin in selected:
            plug.validate(plugin)

        if args.print_composed:
            composed = plug.compose_agents(selected)
            key = args.print_composed if args.print_composed.endswith(".md") else f"{args.print_composed}.md"
            if key not in composed:
                print(f"✗ No such agent: {key}. Available: {', '.join(sorted(composed))}")
                return 1
            print(composed[key], end="")
            return 0

        return sync_agents(get_dest("OPENCODE_AGENTS", ".config/opencode/agent"), selected, args.dry_run, args.verify)
    except ValueError as e:
        print(f"✗ {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
