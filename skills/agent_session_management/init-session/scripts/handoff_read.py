#!/usr/bin/env python3
"""Read .agent_docs/handoff.md and report project rule files, as compact JSON.

Deliberately does NOT print the contents of AGENTS.md / CLAUDE.md. Those files are
often already auto-loaded by the host tool, and dumping them again is the single
biggest source of wasted context at session start. This script reports that they
exist and how big they are; the calling agent decides whether reading is warranted.

Usage:
    python handoff_read.py [--repo-root PATH] [--format json|text] [--open-only]

Always exits 0 when the filesystem is readable — a missing handoff is a normal
first-session state, not an error, and should not derail the session.
"""

import argparse
import json
import os
import re
import sys

SNAPSHOT = "Project Snapshot"
LEARNINGS = "Cumulative Learnings"
LAST = "Last Session"
CURRENT = "Current Session"

RULE_FILES = [
    "AGENTS.md", "CLAUDE.md", "CLAUDE.local.md",
    ".cursorrules", "GEMINI.md", ".github/copilot-instructions.md",
]

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_OPEN = re.compile(r"^\s*[-*]\s*\[( |x|X)\]\s*(.+?)\s*$", re.MULTILINE)


def find_repo_root(start):
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
    sections, matches = {}, list(_H2.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1).strip()] = text[m.end():end].strip()
    return sections


def clean(body):
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.DOTALL).strip()
    return "" if body in ("_None._", "_None recorded._", "_None recorded yet._",
                          "_No prior session._", "_Not yet described._",
                          "_Nothing recorded._") else body


def to_list(body):
    return [re.sub(r"^\s*[-*]\s*", "", ln).strip()
            for ln in clean(body).splitlines() if ln.strip().startswith(("-", "*"))]


def collect(root):
    docs = os.path.join(root, ".agent_docs")
    path = os.path.join(docs, "handoff.md")
    archive = os.path.join(docs, "archive")

    out = {
        "repo_root": root,
        "handoff_path": path,
        "handoff_exists": os.path.isfile(path),
        "rule_files": [],
        "archived_sessions": 0,
    }

    for rel in RULE_FILES:
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            size = os.path.getsize(p)
            out["rule_files"].append({
                "path": rel,
                "bytes": size,
                "approx_tokens": max(1, size // 4),
            })

    if os.path.isdir(archive):
        out["archived_sessions"] = len(
            [f for f in os.listdir(archive) if f.endswith(".md")]
        )

    if not out["handoff_exists"]:
        out["note"] = ("No handoff found. This is a fresh project or the first session — "
                       "start normally and run the end-session skill when wrapping up.")
        return out

    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        out["handoff_exists"] = False
        out["note"] = f"Handoff exists but could not be read: {e}"
        return out

    sec = parse_sections(text)
    current_body = sec.get(CURRENT, "")

    open_items, done_items = [], []
    for state, label in _OPEN.findall(current_body):
        (done_items if state.lower() == "x" else open_items).append(label)

    out.update({
        "bytes": len(text.encode("utf-8")),
        "snapshot": clean(sec.get(SNAPSHOT, "")),
        "learnings": to_list(sec.get(LEARNINGS, "")),
        "last_session": to_list(sec.get(LAST, "")),
        "current_session": {
            "date": (re.search(r"\*\*Date:\*\*\s*(.+)", current_body) or [None, ""])[1].strip()
                    if re.search(r"\*\*Date:\*\*\s*(.+)", current_body) else "",
            "focus": (re.search(r"\*\*Focus:\*\*\s*(.+)", current_body).group(1).strip()
                      if re.search(r"\*\*Focus:\*\*\s*(.+)", current_body) else ""),
            "open_items": open_items,
            "completed_items": done_items,
        },
    })
    return out


def as_text(d):
    lines = [f"repo: {d['repo_root']}"]
    if not d.get("handoff_exists"):
        lines.append(d.get("note", "No handoff found."))
    else:
        cs = d.get("current_session", {})
        if d.get("snapshot"):
            lines += ["", "SNAPSHOT", d["snapshot"]]
        if d.get("learnings"):
            lines += ["", "LEARNINGS"] + [f"- {x}" for x in d["learnings"]]
        if d.get("last_session"):
            lines += ["", "LAST SESSION"] + [f"- {x}" for x in d["last_session"]]
        lines += ["", f"CURRENT SESSION ({cs.get('date', '?')}) {cs.get('focus', '')}".rstrip()]
        lines += [f"- [ ] {x}" for x in cs.get("open_items", [])] or ["(no open items)"]
    if d["rule_files"]:
        lines += ["", "RULE FILES: " + ", ".join(
            f"{r['path']} (~{r['approx_tokens']} tok)" for r in d["rule_files"])]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Read handoff state for session init.")
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--open-only", action="store_true",
                    help="Emit only open items — cheapest possible resume.")
    args = ap.parse_args()

    root = os.path.abspath(args.repo_root) if args.repo_root else find_repo_root(os.getcwd())
    data = collect(root)

    if args.open_only:
        items = data.get("current_session", {}).get("open_items", [])
        print(json.dumps({"open_items": items}, indent=2) if args.format == "json"
              else ("\n".join(f"- [ ] {i}" for i in items) or "(no open items)"))
        return 0

    print(json.dumps(data, indent=2) if args.format == "json" else as_text(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
