#!/usr/bin/env python3
"""Compose .agent_docs/handoff.md from structured JSON, archiving the outgoing session.

All judgment (what counts as a learning, how to compress a session) happens in the
calling agent. This script only does the mechanical part: parse the existing file,
move the outgoing "Current Session" into the archive, and re-emit the four canonical
sections in a fixed order so the format can never drift.

Usage:
    python handoff_write.py --input payload.json [--repo-root PATH] [--dry-run]
    cat payload.json | python handoff_write.py

Payload schema (every field optional except current_session):
    {
      "snapshot": "markdown string",          # omitted -> existing snapshot preserved
      "learnings": ["bullet", ...],           # omitted -> existing learnings preserved
                                              # provided -> REPLACES the list wholesale
      "last_session": ["bullet", ...],        # omitted -> existing preserved (warns)
      "current_session": {
        "date": "2026-08-23",                 # omitted -> today
        "focus": "one line",
        "done": ["bullet", ...],
        "decisions": ["bullet", ...],
        "open_items": ["text", {"text": "...", "done": true}, ...]
      }
    }

Exit codes: 0 ok, 1 bad input, 2 filesystem problem.
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys

SNAPSHOT = "Project Snapshot"
LEARNINGS = "Cumulative Learnings"
LAST = "Last Session"
CURRENT = "Current Session"
SECTION_ORDER = [SNAPSHOT, LEARNINGS, LAST, CURRENT]

DOC_TITLE = "# Project Handoff"
HEADER_NOTE = (
    "<!-- Managed by the end-session / init-session skills. Section order is fixed; "
    "the file is compacted on every write, not appended to. -->"
)

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def find_repo_root(start):
    """Walk up looking for a project marker; fall back to the starting directory."""
    cur = os.path.abspath(start)
    while True:
        for marker in (".git", ".agent_docs"):
            if os.path.exists(os.path.join(cur, marker)):
                return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start)
        cur = parent


def parse_sections(text):
    """Split markdown into {heading: body}. Unknown headings are preserved as-is."""
    sections, matches = {}, list(_H2.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1).strip()] = text[m.end():end].strip()
    return sections


def strip_comments(body):
    """Drop HTML comments so template placeholders never read as real content."""
    return re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()


def bullets(items, empty="_None recorded._"):
    items = [str(i).strip() for i in (items or []) if str(i).strip()]
    if not items:
        return empty
    return "\n".join(b if b.startswith(("-", "*")) else f"- {b}" for b in items)


def checkboxes(items):
    if not items:
        return "_None._"
    out = []
    for it in items:
        if isinstance(it, dict):
            text, done = str(it.get("text", "")).strip(), bool(it.get("done"))
        else:
            text, done = str(it).strip(), False
        if text:
            out.append(f"- [{'x' if done else ' '}] {text}")
    return "\n".join(out) if out else "_None._"


def render_current(cs):
    date = str(cs.get("date") or _dt.date.today().isoformat())
    parts = [f"**Date:** {date}"]
    focus = str(cs.get("focus", "")).strip()
    if focus:
        parts.append(f"**Focus:** {focus}")
    parts.append("")
    parts.append("### Done")
    parts.append(bullets(cs.get("done"), "_Nothing recorded._"))
    decisions = cs.get("decisions") or []
    if decisions:
        parts += ["", "### Decisions", bullets(decisions)]
    parts += ["", "### Open Items", checkboxes(cs.get("open_items"))]
    return "\n".join(parts)


def compose(snapshot, learnings, last, current):
    blocks = [
        DOC_TITLE,
        "",
        HEADER_NOTE,
        "",
        f"## {SNAPSHOT}",
        "",
        snapshot or "_Not yet described._",
        "",
        f"## {LEARNINGS}",
        "",
        learnings or "_None recorded yet._",
        "",
        f"## {LAST}",
        "",
        last or "_No prior session._",
        "",
        f"## {CURRENT}",
        "",
        current,
        "",
    ]
    return "\n".join(blocks)


def main():
    ap = argparse.ArgumentParser(description="Write a compacted handoff.md.")
    ap.add_argument("--input", help="Path to JSON payload. Reads stdin if omitted.")
    ap.add_argument("--repo-root", default=None, help="Project root. Auto-detected if omitted.")
    ap.add_argument("--dry-run", action="store_true", help="Print result; write nothing.")
    args = ap.parse_args()

    try:
        raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
        payload = json.loads(raw)
    except FileNotFoundError:
        print(f"ERROR: payload not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: payload is not valid JSON: {e}", file=sys.stderr)
        return 1

    cs = payload.get("current_session")
    if not isinstance(cs, dict):
        print("ERROR: 'current_session' is required and must be an object.", file=sys.stderr)
        return 1

    root = os.path.abspath(args.repo_root) if args.repo_root else find_repo_root(os.getcwd())
    docs_dir = os.path.join(root, ".agent_docs")
    archive_dir = os.path.join(docs_dir, "archive")
    handoff_path = os.path.join(docs_dir, "handoff.md")

    existing = {}
    if os.path.exists(handoff_path):
        try:
            existing = parse_sections(open(handoff_path, encoding="utf-8").read())
        except OSError as e:
            print(f"ERROR: cannot read existing handoff: {e}", file=sys.stderr)
            return 2

    prev_current = strip_comments(existing.get(CURRENT, ""))
    warnings = []

    # Sections default to whatever is already on disk, so a partial payload is safe.
    snapshot = payload.get("snapshot")
    snapshot = snapshot.strip() if isinstance(snapshot, str) and snapshot.strip() \
        else strip_comments(existing.get(SNAPSHOT, ""))

    if "learnings" in payload:
        learnings = bullets(payload["learnings"], "_None recorded yet._")
    else:
        learnings = strip_comments(existing.get(LEARNINGS, ""))
        warnings.append("no 'learnings' supplied; existing list preserved unchanged")

    if "last_session" in payload:
        last = bullets(payload["last_session"], "_No prior session._")
    elif prev_current:
        last = strip_comments(existing.get(LAST, ""))
        warnings.append(
            "no 'last_session' supplied but a previous session existed; "
            "the outgoing session was archived but NOT compressed into 'Last Session'"
        )
    else:
        last = strip_comments(existing.get(LAST, ""))

    new_doc = compose(snapshot, learnings, last, render_current(cs))

    if args.dry_run:
        sys.stdout.write(new_doc)
        for w in warnings:
            print(f"WARNING: {w}", file=sys.stderr)
        return 0

    try:
        os.makedirs(archive_dir, exist_ok=True)
    except OSError as e:
        print(f"ERROR: cannot create {archive_dir}: {e}", file=sys.stderr)
        return 2

    archived = None
    if prev_current:
        stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        archived = os.path.join(archive_dir, f"session-{stamp}.md")
        try:
            with open(archived, "w", encoding="utf-8") as fh:
                fh.write(f"# Archived Session — {stamp}\n\n{prev_current}\n")
        except OSError as e:
            print(f"ERROR: cannot write archive (aborting to avoid data loss): {e}", file=sys.stderr)
            return 2

    try:
        with open(handoff_path, "w", encoding="utf-8") as fh:
            fh.write(new_doc)
    except OSError as e:
        print(f"ERROR: cannot write handoff: {e}", file=sys.stderr)
        return 2

    result = {
        "handoff": handoff_path,
        "archived": archived,
        "bytes": len(new_doc.encode("utf-8")),
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
