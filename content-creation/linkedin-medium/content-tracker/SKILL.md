---
name: content-tracker
description: Use when the user wants to track content, manage a content backlog, check a content log, update post status, ask "what haven't I posted", check posting cadence, find overdue posts, archive posted pieces, or see everything for a platform. A lightweight cross-session tracker for a LinkedIn/Medium content pipeline. Do NOT use to author the content itself.
---

# Content Tracker

Lightweight, cross-session tracker for a LinkedIn/Medium content pipeline. It owns a
single log at the current working directory root and moves each content idea through
its lifecycle: `idea -> drafted -> reviewed -> posted -> archived`.

## When to use

Use this skill when the user asks to:

- Track a new content idea or piece ("add this to my backlog").
- Update the status of a piece ("mark X as drafted / reviewed / posted").
- Query the pipeline: "what haven't I posted yet", "show my backlog", "what's overdue
  this week", "show everything for LinkedIn".
- Archive published content ("archive the ones I've posted").

Do NOT use it to write or draft the content — that belongs to the authoring skills.

## Optional infrastructure (standalone)

This tracker is **optional**. It works alone; other skills MAY write to the log but
must never require it. If the log is missing, the other skills degrade gracefully — a
missing tracker is not an error, just an absent convenience.

## Log location and shape

- Source of truth: `content-log.json` at the **current working directory root**.
- Human-readable mirror: `content-log.md`, rendered from the JSON. Never hand-edit the
  MD; regenerate it with `render`.
- Archived content files live under a cwd-relative `archive/` folder.

Every path is **cwd-relative**. If a required folder or file is missing, ASK the user
how to proceed — do not guess another location.

Each entry:

| field | meaning |
|-------|---------|
| `slug` | unique key |
| `title` | display title |
| `status` | `idea` \| `drafted` \| `reviewed` \| `posted` \| `archived` |
| `platform` | LinkedIn / Medium / both |
| `type` | content-matrix type |
| `created` | ISO date |
| `updated` | ISO date |
| `posted_date` | ISO date or null |
| `sources` | list of URLs (optional) |
| `notes` | optional |

## Ask-before-create rule

The tracker must tolerate a missing or empty log. If `content-log.json` does not exist,
**ASK the user first** before creating it. Never silently create files. The script can
create the JSON lazily, but you must confirm with the user before running any command
that would bring it into existence.

## Review-first confirmation

Before writing any change to the log or moving any file:

1. Show the user the exact intended change (the entry to add, the status transition,
   or the files to move).
2. Get explicit confirmation.
3. Only then run the mutating command.

## Dedup rule

`slug` is the unique key. `add` refuses to create a second entry with an existing slug.
If the user really wants to overwrite/merge, confirm and re-run with `--force`.

## Cadence heuristic (overdue)

Target cadence is **2–3 posts per week**. The tracker flags the backlog as *overdue /
behind cadence* if EITHER:

- fewer than **2 posts** occurred in the **last 7 days**, OR
- **nothing has been posted in more than 4 days**.

Only `posted` entries with a valid `posted_date` count toward cadence. This is a simple,
documented heuristic — not a scheduler.

## Workflows

### Add an entry
1. Confirm the details with the user (review-first).
2. If the log doesn't exist yet, ASK before first creation.
3. Run `add`. It refuses duplicate slugs unless `--force`.

### Update status
1. Show the intended transition and confirm.
2. Run `update`. Sane forward transitions are enforced; anything else needs `--force`
   (confirm with the user before overriding). Setting status to `posted` stamps
   `posted_date` automatically.

### Query
- Unposted work: `list --unposted` (excludes `posted` and `archived`).
- Backlog / everything: `list`.
- By platform: `list --platform LinkedIn` (entries marked `both` always match).
- Overdue: `list --overdue` reports cadence status and lists work if behind.

### Archive (posted -> archived)
1. Confirm which entries to archive and which content file(s) will move.
2. Ensure the cwd-relative `archive/` folder exists — if missing, ASK the user.
3. Move the associated content file(s) into `archive/` — **ask before moving, never
   silently**.
4. Run `update --slug S --status archived`.

## Invoking the script

`scripts/track.py` is standard-library Python. Default log path is `content-log.json`
in the cwd; override with `--file`.

```
python3 scripts/track.py --help
python3 scripts/track.py add --slug my-post --title "My Post" \
    --status idea --platform LinkedIn --type howto --source https://example.com
python3 scripts/track.py update --slug my-post --status posted
python3 scripts/track.py list --unposted
python3 scripts/track.py list --platform Medium
python3 scripts/track.py list --overdue
python3 scripts/track.py render
```

Add `--json` to any command for machine-readable output. Every mutation re-renders
`content-log.md`; run `render` to rebuild it on demand.
