---
name: end-session
description: Capture the current session into a compact handoff at .agent_docs/handoff.md so the next session resumes instantly with no re-explaining. Use this skill whenever the user signals work is stopping or should be checkpointed — "done for today", "wrap up", "end session", "save context", "checkpoint this", "update the handoff", "I'll continue tomorrow" — even if they never say "handoff" or name this skill. Also use before a context compaction or window reset, and whenever a long working session is about to be interrupted.
---

# End Session

Write everything worth carrying forward into `.agent_docs/handoff.md`, then stop.

The reason this skill exists is that handoff files rot: appended to every session, they grow until reading them costs more than the context they restore. So this file is **compacted on every write, never appended to**. Full detail is not lost — it is moved to `.agent_docs/archive/` where it costs nothing until someone deliberately looks.

## The four sections

`handoff.md` always has exactly these, in this order (see `assets/handoff_template.md`):

| Section | Lifetime | Content |
|---|---|---|
| **Project Snapshot** | Rewritten only when it changes | What the project is, stack, architecture, how to run and test it |
| **Cumulative Learnings** | Forever, deduped | Durable non-obvious facts: gotchas, constraints, conventions, dead ends |
| **Last Session** | Overwritten each session | 3-5 compressed bullets of the session before this one |
| **Current Session** | Archived, then replaced | Full detail of the session that just ended, plus open items |

## Workflow

**1. Read the existing handoff.** `cat .agent_docs/handoff.md` (or use init-session's reader). If it does not exist, this is session one — skip to step 3 and write a Snapshot.

**2. Compress the outgoing Current Session into 3-5 bullets.** These become the new **Last Session**; the previous Last Session is discarded, not stacked. Compress toward outcomes and unresolved threads, not activity logs. "Refactored auth to use middleware; token refresh still unverified" earns its place. "Discussed options, tried some things" does not — if a bullet would not change what the next session does, drop it.

**3. Decide what is a durable learning.** This is the judgment call that makes or breaks the file. Promote a fact to **Cumulative Learnings** only if it is (a) still true next month, (b) not obvious from reading the code, and (c) would cost real time to rediscover.

Good: `Vitest needs --pool=forks here; the default worker pool deadlocks on the DB mock.`
Good: `Tried moving parsing into the worker — blocked by the SDK's sync-only file handles.`
Bad: `Fixed the login bug.` (a session event, not a durable fact)
Bad: `The project uses TypeScript.` (obvious from the repo — belongs in Snapshot at most)

Then **merge semantically against the existing list** — if a new learning refines an old one, rewrite that line rather than adding a near-duplicate. This dedup is why the file stays bounded, and it is the part no script can do.

**4. Write the payload and run the script.** Build JSON and pass it to the writer, which archives the outgoing session and re-emits all four sections in fixed order:

```bash
python scripts/handoff_write.py --input /tmp/handoff_payload.json
```

```json
{
  "snapshot": "FastAPI service for invoice parsing. Postgres via SQLAlchemy.\nRun: `make dev`. Test: `pytest -q`.",
  "learnings": [
    "Vitest needs --pool=forks; default worker pool deadlocks on the DB mock.",
    "Invoice PDFs from vendor B are scanned — OCR path is mandatory, not optional."
  ],
  "last_session": [
    "Wired up the OCR fallback; vendor B invoices now parse.",
    "Left the retry backoff hardcoded — needs config."
  ],
  "current_session": {
    "date": "2026-08-23",
    "focus": "Split the parser into per-vendor strategies",
    "done": ["Extracted VendorAStrategy and VendorBStrategy", "Added fixtures for both"],
    "decisions": ["Strategy chosen by issuer VAT number, not filename — filenames are unreliable"],
    "open_items": [
      {"text": "Vendor C strategy not started", "done": false},
      {"text": "Retry backoff still hardcoded to 3s", "done": false}
    ]
  }
}
```

Omit `snapshot` or `learnings` to preserve what is already on disk. Always supply `last_session` — the script warns if you skip it, because that silently breaks the rolling window. Use `--dry-run` to preview without touching anything.

**5. Confirm briefly.** State where it was written, what was archived, and how many open items carried forward. Two lines. Do not re-print the file the user just watched you write.

## Keep it honest

Record open items as they actually are, including things that were abandoned or that failed. A handoff that reads as uniformly successful is worse than none, because the next session inherits false confidence. If something was left broken, say so plainly in the open items.
