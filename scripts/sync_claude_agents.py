#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Sync OpenCode subagents to Claude Code's ~/.claude/agents, translating frontmatter.

Only `mode: subagent` agents translate — Claude Code's own top-level session is
the `primary`-agent equivalent, governed by CLAUDE.md rather than an agent file,
so `orchestrator`/`ask` have no target here. Claude Code subagent frontmatter has
no per-command bash permission map, so the granular allow/ask/deny gates on
`executor.md` can't be represented there; a plain-language equivalent is
appended to the body instead.
"""

import sys

import yaml

import plugins as plug
from common import get_dest, parse_args

DESTRUCTIVE_NOTE = (
    "\n\nBefore destructive commands (`rm -rf`, `git push`, `git reset --hard`, "
    "`git clean`, force-checkout/restore, `sudo`, piping a remote script into a "
    "shell), stop and ask the user first rather than proceeding."
)


def translate(path) -> tuple[str, str] | None:
    """OpenCode subagent -> Claude Code subagent frontmatter. None if not a subagent."""
    fm, body = plug.split_frontmatter(path.read_text())
    if fm.get("mode") != "subagent":
        return None
    claude_fm = {"name": path.stem, "description": fm["description"]}
    if "steps" in fm:
        claude_fm["maxTurns"] = fm["steps"]
    dumped = yaml.safe_dump(claude_fm, sort_keys=False, default_flow_style=False, allow_unicode=True, width=4096)
    return path.name, f"---\n{dumped}---\n{body.rstrip()}{DESTRUCTIVE_NOTE}\n"


def verify_claude_agents(dest_dir, translated: dict[str, str]) -> int:
    """Verify translated agent files exist in destination and match content."""
    print("\n🔎 Verifying Claude Code subagents parity...")
    failures = []
    for filename, content in sorted(translated.items()):
        dest_file = dest_dir / filename
        if not dest_file.exists():
            failures.append(f"{filename}: missing in destination")
        elif dest_file.read_text() != content:
            failures.append(f"{filename}: content mismatch")
        else:
            print(f"✓ {filename}")
    if failures:
        print("\n✗ Claude Code agents verification failed:")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("✅ All Claude Code subagents verified (100% parity)")
    return 0


def main() -> int:
    args = parse_args("Sync OpenCode subagents to Claude Code's ~/.claude/agents")
    dest_dir = get_dest("CLAUDE_AGENTS", ".claude/agents")
    translated = dict(filter(None, (translate(p) for p in plug.base_agents())))

    print("🔄 Syncing Claude Code subagents...")
    print(f"  Source:      {plug.AGENTS_DIR}\n  Destination: {dest_dir}\n")
    if args.dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = plug.install(dest_dir, translated, args.dry_run)

    mode_str = "🔍 DRY RUN: No files were modified" if args.dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} agents\n  Skipped: {skipped} agents\n")
    print(f"📍 Claude Code agents: {dest_dir}")

    if skipped:
        return 1
    return verify_claude_agents(dest_dir, translated) if args.verify and not args.dry_run else 0


if __name__ == "__main__":
    sys.exit(main())
