# content-tracker

A lightweight, cross-session tracker for a LinkedIn/Medium content pipeline. It owns a single log at the current working directory root and moves each content idea through its lifecycle: `idea -> drafted -> reviewed -> posted -> archived`. It is **optional infrastructure**. Other skills may write to the log but never require it.

---

## Trigger phrases

| Input | Example |
|---|---|
| Add a new idea/piece | "add this to my backlog", "track this idea" |
| Update status | "mark X as drafted", "mark X as reviewed", "mark X as posted" |
| Query the pipeline | "what haven't I posted yet", "show my backlog", "what's overdue this week", "show everything for LinkedIn" |
| Archive published work | "archive the ones I've posted" |

Do **not** use it to write or draft content. That belongs to the authoring skills. Expanding an idea is `seed-expander`, drafting is `draft-builder`, platform reshaping is `platform-adapter`, editing/variants is `editorial-reviewer`, carousels are `carousel-builder`, step verification is `tutorial-verifier`, and voice capture is `voice-profiler`. This skill only tracks state; it never produces content.

---

## What it does

- **Owns one source of truth.** `content-log.json` at the cwd root is authoritative; `content-log.md` is a human-readable mirror rendered from the JSON. Never hand-edit the MD. Regenerate it with `render`. Every mutation re-renders the MD automatically.
- **Moves pieces through a status lifecycle.** Each entry advances `idea -> drafted -> reviewed -> posted -> archived`, with sane forward transitions enforced.
- **Tracks structured entries.** Each entry carries `slug` (unique key), `title`, `status`, `platform` (LinkedIn / Medium / both), `type`, `created`, `updated`, `posted_date`, optional `sources` (URLs), and optional `notes`.
- **Queries the pipeline.** Lists everything, unposted-only work, per-platform slices (entries marked `both` always match), and a cadence/overdue report.
- **Archives published work.** Moves associated content files into a cwd-relative `archive/` folder (asking first, never silently) and flips the entry to `archived`.
- **Runs on a standard-library Python script.** `scripts/track.py` has no dependencies; the default log path is `content-log.json` in the cwd, overridable with `--file`. Add `--json` to any command for machine-readable output.

---

## Optional infrastructure

This tracker is **optional**. It works alone; other skills MAY write to the log but must never require it. If the log is missing, the other skills degrade gracefully. A missing tracker is not an error, just an absent convenience.

---

## Status lifecycle

`idea -> drafted -> reviewed -> posted -> archived`

Only sane forward transitions are allowed; anything else needs `--force` (the agent confirms with the user first):

| From | Allowed to |
|---|---|
| `idea` | `drafted`, `archived` |
| `drafted` | `reviewed`, `idea`, `archived` |
| `reviewed` | `posted`, `drafted`, `archived` |
| `posted` | `archived` |
| `archived` | (terminal) |

Setting status to `posted` stamps `posted_date` automatically.

---

## Scripts

`scripts/track.py`: standard-library Python, no dependencies. Subcommands:

| Subcommand | What it does |
|---|---|
| `add` | Adds a new entry; refuses a duplicate `slug` unless `--force` |
| `update` | Updates an entry's status; enforces forward transitions (override with `--force`); stamps `posted_date` on `posted` |
| `list` | Lists/queries entries (`--status`, `--platform`, `--unposted`, `--overdue`) |
| `render` | Regenerates `content-log.md` from the JSON |

Example invocations:

```bash
python3 scripts/track.py --help

# Add an idea (repeat --source for multiple URLs)
python3 scripts/track.py add --slug my-post --title "My Post" \
    --status idea --platform LinkedIn --type howto --source https://example.com

# Advance status (posted auto-stamps posted_date)
python3 scripts/track.py update --slug my-post --status posted

# Query
python3 scripts/track.py list --unposted
python3 scripts/track.py list --platform Medium
python3 scripts/track.py list --overdue

# Rebuild the Markdown mirror on demand
python3 scripts/track.py render
```

Add `--json` to any command for machine-readable output.

---

## Dedup rule

`slug` is the unique key. `add` refuses to create a second entry with an existing slug. If the user really wants to overwrite/merge, confirm and re-run with `--force` (an overwrite preserves the original `created` date).

---

## Cadence heuristic (overdue)

Target cadence is **2-3 posts per week**. The backlog is flagged *overdue / behind cadence* if EITHER:

- fewer than **2 posts** occurred in the **last 7 days**, OR
- **nothing has been posted in more than 4 days**.

Only `posted` entries with a valid `posted_date` count toward cadence. This is a simple, documented heuristic, not a scheduler.

---

## Review-first + ask-before-create

- **Ask before first creation.** If `content-log.json` does not exist, ASK the user before creating it. The script creates the JSON lazily on first mutation, so the agent must confirm before running any command that would bring it into existence.
- **Review-first confirmation.** Before any log write or file move, show the exact intended change (the entry to add, the status transition, or the files to move), get explicit confirmation, then run the mutating command.
- **Archive moves are never silent.** Moving content files into `archive/` requires confirmation; if the `archive/` folder is missing, ASK the user.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| `content-log.json` | Created on first use | Source-of-truth JSON log at the cwd root (default path; override with `--file`) |
| Entry details | For `add` | `slug`, `title`, and optionally `status`, `platform`, `type`, `source`(s), `notes` |
| Status transition | For `update` | Target `status` for a given `slug`; `--force` to override the transition guard |
| `archive/` folder | For archiving | Cwd-relative destination for moved content files; the skill asks if missing |

---

## Outputs

- `content-log.json`: the authoritative pipeline log (created only after the user confirms).
- `content-log.md`: a rendered, human-readable mirror; regenerated on every mutation or via `render`.
- Query results: backlog, unposted work, per-platform slices, and a cadence/overdue report (human-readable or `--json`).
- Archived entries with their content files moved into `archive/` (after confirmation).

---

## Limitations

- **Optional, never required.** Other skills degrade gracefully when the log is absent; a missing tracker is not an error.
- **Never silently creates the log.** The agent asks before first creation and confirms before every mutation or file move.
- **Dedup by slug.** `add` refuses duplicate slugs unless `--force`.
- **Forward transitions only.** Out-of-order status changes need `--force` and user confirmation.
- **Cadence is a heuristic, not a scheduler.** It flags "behind cadence" from `posted_date`s; it does not plan or post anything.
- **Does not author content.** It only tracks pipeline state.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/content-tracker ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/content-tracker .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\content-tracker "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/content-tracker.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the tracking task |

For any platform, `scripts/track.py` is standard-library Python and can be run directly with `python3`.

---

## Companion skills

A cross-cutting support skill for the LinkedIn/Medium content suite. Pipeline order: `seed-expander` -> `draft-builder` -> `platform-adapter` -> {`carousel-builder`, `tutorial-verifier`} -> `editorial-reviewer`, with `voice-profiler` and **`content-tracker`** as cross-cutting support.

- **`seed-expander`**, **`draft-builder`**, **`platform-adapter`**, **`carousel-builder`**, **`tutorial-verifier`**, **`editorial-reviewer`**: the authoring/publishing pipeline; each MAY record status here but never requires it
- **`voice-profiler`**: the other cross-cutting support skill; captures voice into `voice-tone/profile.md`

`content-tracker` is the optional memory layer that keeps the pipeline's state visible across sessions.
