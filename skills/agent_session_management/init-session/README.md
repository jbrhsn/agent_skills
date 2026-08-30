# init-session

Rebuilds just enough project context to keep working, then gets out of the way.

Pair of [`end-session`](../end-session/README.md), which writes the file this one reads.

## When to use it

At the start of a session on a project you've worked on before.

**Practical triggers:**
- "catch me up", "what were we doing", "resume", "where did we leave this"
- You open a project after a few days and don't remember the open threads
- A context window reset and the session needs its bearings back
- The user starts giving instructions that assume context the agent doesn't have

The skill fires on the intent, not the vocabulary — nobody has to say "handoff.md".

## What you'll get

A recap you can scan in about five seconds:

- One line of project identity, and only when the snapshot suggests you may have switched projects
- What last session ended with
- **Open items, verbatim** — the part that actually matters
- Any cumulative learning that bears on those specific open items

Then a question, or a proposed next step if there's an obvious one.

What you will *not* get: the full handoff replayed into chat, every cumulative
learning restated, a summary of your own `AGENTS.md`, or a narration of the
loading process. You wrote the handoff so you wouldn't have to read it again.

## How it works

```bash
python scripts/handoff_read.py --format json     # full state
python scripts/handoff_read.py --open-only       # just the next tasks
python scripts/handoff_read.py --format text     # human-readable
```

The script walks up for `.git` or `.agent_docs`, so it runs from any
subdirectory. It returns the four parsed sections, open items split from
completed ones, the archived-session count, and a list of which rule files
exist with their approximate token cost.

## Design decisions

**Rule files are reported, never printed.** The script detects `AGENTS.md`,
`CLAUDE.md`, `CLAUDE.local.md`, `.cursorrules`, `GEMINI.md`, and
`.github/copilot-instructions.md` — and deliberately does not read them out.
Re-injecting a file the harness already auto-loaded is the single largest
source of wasted context at session start. The agent is told they exist and how
big they are, and decides.

The decision rule is asymmetric on purpose: if the file is already in context,
skip it; if it isn't, read it; **if you're unsure, read it.** A duplicated small
file costs less than silently violating the project's conventions all session.

**Rules and state stay separate.** `AGENTS.md` governs *how* to work; the
handoff records *where the work stands*. Copying rules into `handoff.md` makes
the two drift, and then nobody knows which is current.

**A missing handoff is not an error.** `handoff_exists: false` is the normal
first-session state. The script exits 0, the agent says so in one line and
starts working. No offer to reconstruct history that doesn't exist.

**The handoff is treated as stale until confirmed.** It describes the repo as
of last session's end — you may have committed, reverted, or worked elsewhere
since. Before acting on an open item the agent verifies the current state of
the relevant files, and if the repo contradicts the handoff, the repo wins and
the agent says so.

## Layout

```
init-session/
├── SKILL.md
├── README.md
└── scripts/
    └── handoff_read.py     # stdlib only, exits 0 when the filesystem is readable
```

No `references/` — the whole workflow is five steps and fits in `SKILL.md`.

## Install

From the repo root, the sync script covers every platform:

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy this folder into your harness's skills directory — see the
[category README](../README.md) for the per-platform paths. Requires Python 3.8+,
no third-party packages.

## Failure modes it's built against

| Failure | What stops it |
|---|---|
| Burning the first thousand tokens narrating a file the user wrote | Recap is capped at open items plus what bears on them |
| Re-reading `CLAUDE.md` that the host already injected | Script reports rule files without printing them |
| Acting on a stale open item that was fixed out-of-session | Verify the files before acting; the repo overrides the handoff |
| Treating a first session as a broken state | Missing handoff exits 0 and is stated in one line |
