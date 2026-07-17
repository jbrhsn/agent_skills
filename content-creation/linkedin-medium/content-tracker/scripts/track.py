#!/usr/bin/env python3
"""content-tracker: a standard-library helper for a cross-session content pipeline log.

Source of truth is a JSON file (default: ./content-log.json in the current working
directory). A human-readable Markdown mirror (content-log.md, sibling of the JSON) is
rendered from the JSON via the `render` subcommand and after any mutation.

Entry shape:
    slug        unique key (string)
    title       display title
    status      one of: idea, drafted, reviewed, posted, archived
    platform    e.g. LinkedIn / Medium / both
    type        content-matrix type (free-form)
    created     ISO date (YYYY-MM-DD)
    updated     ISO date (YYYY-MM-DD)
    posted_date ISO date or null
    sources     list of urls (optional)
    notes       optional string

This script creates the JSON lazily on first mutation. The accompanying SKILL.md
instructs the agent to ASK the user before that first creation happens.
"""

import argparse
import datetime
import json
import os
import shutil
import sys

STATUSES = ["idea", "drafted", "reviewed", "posted", "archived"]

# Sane forward transitions. Anything else requires --force (agent confirms with user).
ALLOWED_TRANSITIONS = {
    "idea": {"drafted", "archived"},
    "drafted": {"reviewed", "idea", "archived"},
    "reviewed": {"posted", "drafted", "archived"},
    "posted": {"archived"},
    "archived": set(),
}


def today():
    return datetime.date.today().isoformat()


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def load(path):
    """Load the log. Returns a dict with an 'entries' list. Missing file -> empty log."""
    if not os.path.exists(path):
        return {"entries": []}
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "entries" not in data or not isinstance(data["entries"], list):
        data = {"entries": []}
    return data


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def md_path_for(json_path):
    root, _ = os.path.splitext(json_path)
    return root + ".md"


def render_md(data):
    lines = ["# Content Log", ""]
    entries = data["entries"]
    lines.append("_Rendered from the JSON source of truth. Do not edit by hand._")
    lines.append("")
    lines.append("| slug | title | status | platform | type | created | updated | posted |")
    lines.append("|------|-------|--------|----------|------|---------|---------|--------|")
    for e in sorted(entries, key=lambda x: (x.get("status", ""), x.get("slug", ""))):
        lines.append(
            "| {slug} | {title} | {status} | {platform} | {type} | {created} | {updated} | {posted} |".format(
                slug=e.get("slug", ""),
                title=e.get("title", ""),
                status=e.get("status", ""),
                platform=e.get("platform", ""),
                type=e.get("type", ""),
                created=e.get("created", ""),
                updated=e.get("updated", ""),
                posted=e.get("posted_date") or "-",
            )
        )
    lines.append("")
    # Notes / sources detail block
    detail = [e for e in entries if e.get("sources") or e.get("notes")]
    if detail:
        lines.append("## Details")
        lines.append("")
        for e in sorted(detail, key=lambda x: x.get("slug", "")):
            lines.append("### {}".format(e.get("slug", "")))
            if e.get("notes"):
                lines.append("- notes: {}".format(e["notes"]))
            for u in e.get("sources", []) or []:
                lines.append("- source: {}".format(u))
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_md(json_path, data):
    mp = md_path_for(json_path)
    with open(mp, "w", encoding="utf-8") as fh:
        fh.write(render_md(data))
    return mp


def find(entries, slug):
    for e in entries:
        if e.get("slug") == slug:
            return e
    return None


def is_overdue(entries, ref=None):
    """Cadence heuristic for a 2-3x/week target.

    Returns True (backlog is behind cadence) if EITHER:
      * fewer than 2 posts happened in the last 7 days, OR
      * nothing has been posted in more than 4 days.
    Only 'posted' entries with a valid posted_date count toward cadence.
    """
    ref = ref or datetime.date.today()
    posted_dates = []
    for e in entries:
        if e.get("status") == "posted":
            d = parse_date(e.get("posted_date"))
            if d:
                posted_dates.append(d)
    posts_last_7 = sum(1 for d in posted_dates if (ref - d).days <= 7 and (ref - d).days >= 0)
    if posts_last_7 < 2:
        return True
    most_recent = max(posted_dates) if posted_dates else None
    if most_recent is None or (ref - most_recent).days > 4:
        return True
    return False


# --------------------------------------------------------------------------- #
# Subcommands
# --------------------------------------------------------------------------- #

def cmd_add(args):
    data = load(args.file)
    entries = data["entries"]
    existing = find(entries, args.slug)
    if existing and not args.force:
        _emit(
            args,
            {"ok": False, "error": "duplicate_slug", "slug": args.slug},
            "Refusing: an entry with slug '{}' already exists. Use --force to overwrite/merge, "
            "or choose a different slug.".format(args.slug),
        )
        return 1
    entry = {
        "slug": args.slug,
        "title": args.title,
        "status": args.status,
        "platform": args.platform,
        "type": args.type,
        "created": today(),
        "updated": today(),
        "posted_date": today() if args.status == "posted" else None,
        "sources": list(args.source or []),
        "notes": args.notes,
    }
    if existing:
        entries.remove(existing)
        # preserve original created date on overwrite
        entry["created"] = existing.get("created", entry["created"])
    entries.append(entry)
    save(args.file, data)
    mp = write_md(args.file, data)
    _emit(
        args,
        {"ok": True, "action": "added", "entry": entry, "md": mp},
        "Added '{}' (status={}). Rendered {}.".format(args.slug, args.status, mp),
    )
    return 0


def cmd_update(args):
    data = load(args.file)
    entries = data["entries"]
    entry = find(entries, args.slug)
    if not entry:
        _emit(
            args,
            {"ok": False, "error": "not_found", "slug": args.slug},
            "No entry with slug '{}'.".format(args.slug),
        )
        return 1
    current = entry.get("status")
    target = args.status
    if target not in ALLOWED_TRANSITIONS.get(current, set()) and target != current and not args.force:
        _emit(
            args,
            {
                "ok": False,
                "error": "bad_transition",
                "from": current,
                "to": target,
            },
            "Refusing transition '{}' -> '{}'. Use --force to override (confirm with the "
            "user first).".format(current, target),
        )
        return 1
    entry["status"] = target
    entry["updated"] = today()
    if target == "posted" and not entry.get("posted_date"):
        entry["posted_date"] = today()
    save(args.file, data)
    mp = write_md(args.file, data)
    _emit(
        args,
        {"ok": True, "action": "updated", "entry": entry, "md": mp},
        "Updated '{}': {} -> {}{}. Rendered {}.".format(
            args.slug,
            current,
            target,
            " (posted_date={})".format(entry["posted_date"]) if target == "posted" else "",
            mp,
        ),
    )
    return 0


def cmd_list(args):
    data = load(args.file)
    entries = list(data["entries"])
    if args.status:
        entries = [e for e in entries if e.get("status") == args.status]
    if args.platform:
        entries = [e for e in entries if (e.get("platform") or "").lower() == args.platform.lower()
                   or (e.get("platform") or "").lower() == "both"]
    if args.unposted:
        entries = [e for e in entries if e.get("status") not in ("posted", "archived")]
    overdue_flag = is_overdue(data["entries"])
    if args.overdue and not overdue_flag:
        entries = []
    if args.json:
        print(json.dumps({"ok": True, "overdue": overdue_flag, "entries": entries}, indent=2))
        return 0
    if args.overdue:
        print("Cadence status: {}".format("BEHIND (overdue)" if overdue_flag else "on track"))
    if not entries:
        print("(no matching entries)")
        return 0
    for e in sorted(entries, key=lambda x: (x.get("status", ""), x.get("slug", ""))):
        print("- [{status}] {slug}: {title} | {platform} | {type} | posted={posted}".format(
            status=e.get("status", ""),
            slug=e.get("slug", ""),
            title=e.get("title", ""),
            platform=e.get("platform", ""),
            type=e.get("type", ""),
            posted=e.get("posted_date") or "-",
        ))
    return 0


def cmd_render(args):
    data = load(args.file)
    mp = write_md(args.file, data)
    _emit(args, {"ok": True, "action": "rendered", "md": mp},
          "Rendered {}.".format(mp))
    return 0


def cmd_archive(args):
    data = load(args.file)
    entries = data["entries"]
    entry = find(entries, args.slug)
    if not entry:
        _emit(
            args,
            {"ok": False, "error": "not_found", "slug": args.slug},
            "No entry with slug '{}'.".format(args.slug),
        )
        return 1
    if args.content_file:
        if not os.path.exists(args.content_file):
            _emit(
                args,
                {"ok": False, "error": "file_not_found", "file": args.content_file},
                "File not found: {}".format(args.content_file),
            )
            return 1
        archive_dir = os.path.join(os.getcwd(), "archive")
        if not os.path.isdir(archive_dir):
            _emit(
                args,
                {"ok": False, "error": "no_archive_dir"},
                "archive/ directory not found. Create it first or use "
                "`update --slug {} --status archived` to update status only.".format(args.slug),
            )
            return 1
        dest = shutil.move(args.content_file, archive_dir)
        print("Moved {} -> {}".format(args.content_file, dest))
    current = entry.get("status")
    entry["status"] = "archived"
    entry["updated"] = today()
    save(args.file, data)
    mp = write_md(args.file, data)
    _emit(
        args,
        {"ok": True, "action": "archived", "entry": entry, "md": mp},
        "Archived '{}': {} -> archived. Rendered {}.".format(args.slug, current, mp),
    )
    return 0


def _emit(args, payload, human):
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2))
    else:
        print(human)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def build_parser():
    p = argparse.ArgumentParser(
        prog="track.py",
        description="Manage a content pipeline log (content-log.json + rendered content-log.md).",
    )
    p.add_argument("--file", default="content-log.json",
                   help="Path to the JSON log (default: content-log.json in cwd).")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="Add a new entry (refuses duplicate slug unless --force).")
    a.add_argument("--slug", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--status", default="idea", choices=STATUSES)
    a.add_argument("--platform", default="")
    a.add_argument("--type", default="")
    a.add_argument("--source", action="append", default=[], help="Source URL (repeatable).")
    a.add_argument("--notes", default=None)
    a.add_argument("--force", action="store_true", help="Overwrite an existing slug.")
    a.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    a.set_defaults(func=cmd_add)

    u = sub.add_parser("update", help="Update an entry's status (sets updated/posted_date).")
    u.add_argument("--slug", required=True)
    u.add_argument("--status", required=True, choices=STATUSES)
    u.add_argument("--force", action="store_true", help="Override transition guard.")
    u.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    u.set_defaults(func=cmd_update)

    l = sub.add_parser("list", help="List/query entries.")
    l.add_argument("--status", choices=STATUSES)
    l.add_argument("--platform")
    l.add_argument("--unposted", action="store_true",
                   help="Only entries not yet posted/archived.")
    l.add_argument("--overdue", action="store_true",
                   help="Report cadence status; show entries only if behind cadence.")
    l.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    l.set_defaults(func=cmd_list)

    r = sub.add_parser("render", help="Regenerate content-log.md from the JSON.")
    r.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    r.set_defaults(func=cmd_render)

    ar = sub.add_parser("archive", help="Archive an entry, optionally moving its file.")
    ar.add_argument("--slug", required=True)
    ar.add_argument("--file", dest="content_file", default=None,
                    help="Path to content file to move into archive/.")
    ar.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    ar.set_defaults(func=cmd_archive)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
