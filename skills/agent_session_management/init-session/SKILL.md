---
name: init-session
description: Restore project context at the start of a session by reading .agent_docs/handoff.md and, only if not already loaded, the repo's AGENTS.md or CLAUDE.md. Use this skill whenever the user opens a project and wants to pick up where they left off — "catch me up", "what were we doing", "resume", "continue where we left off", "load context", "init", "where did we leave this" — even if they never mention handoff.md or name this skill. Also use when the user starts giving instructions that clearly assume prior context you do not have.
---

# Init Session

Rebuild just enough context to continue working, then hand control back. The failure mode to avoid is spending the first thousand tokens of a session narrating a file the user already knows the contents of.

## Workflow

**1. Read the handoff.**

```bash
python scripts/handoff_read.py --format json
```

The script finds the repo root by walking up for `.git` or `.agent_docs`, so it works from any subdirectory. It returns the parsed sections, open items split from completed ones, a list of rule files present with their approximate token cost, and an archived-session count.

Use `--open-only` when the user just wants the next task rather than a full recap — it is the cheapest possible resume.

**2. Handle a missing handoff gracefully.** `handoff_exists: false` is the normal first-session state, not an error. Say so in one line and start work. Do not offer to reconstruct history you do not have, and do not treat it as a problem to solve.

**3. Decide whether to read rule files — do not read them reflexively.** The script reports which of `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, `.cursorrules`, `GEMINI.md` exist, but deliberately does not print their contents, because re-reading a file the host already injected is pure waste.

- **Already in your context** (Claude Code auto-loads `CLAUDE.md`; some harnesses auto-load `AGENTS.md`): do not read it again. Check whether you can already recall its actual rules — not just its name.
- **Not in your context** (typical for Open Code Harness, Antigravity, or a bare API session): read it now with the file tool. This is the case the skill exists for.
- **Uncertain**: read it. A duplicated small file costs less than silently violating the project's conventions all session.

Rule files govern *how* to work; the handoff records *where the work stands*. They are separate concerns — never copy rules into `handoff.md`, or the two will drift and you will not know which is current.

**4. Give a short recap, then stop.** Aim for something the user can scan in five seconds:

- One line of project identity (only if the snapshot suggests they may have switched projects)
- What last session ended with
- **Open items, verbatim** — this is the part that actually matters
- Any learning that bears directly on those open items — not the whole list

Then ask what to pick up, or if there is one obvious next item, propose it directly.

**Do not** dump the full handoff back into chat, restate every cumulative learning, summarise the rule files, or explain what you just did to load context. The user wrote this file specifically so they would not have to re-read it.

**5. Treat the handoff as stale until confirmed.** It describes the repo as of the last session's end. Anything may have changed since — the user may have committed, reverted, or worked elsewhere. Before acting on an open item, verify the current state of the relevant files rather than assuming the handoff is still accurate. If what you find contradicts the handoff, say so and trust the repo.

## Example recap

> Picking up the invoice parser. Last session split parsing into per-vendor strategies, chosen by issuer VAT number.
>
> Open:
> - [ ] Vendor C strategy not started
> - [ ] Retry backoff still hardcoded to 3s
>
> Worth knowing for the first one: vendor B invoices are scanned, so the OCR path is mandatory — vendor C may be the same.
>
> Start with vendor C?
