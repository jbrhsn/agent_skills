# end-session

Writes everything worth carrying forward into `.agent_docs/handoff.md`, then stops.

Pair of [`init-session`](../init-session/README.md), which reads it back.

## When to use it

When work is stopping, or when a long session is about to be interrupted.

**Practical triggers:**
- "done for today", "wrap up", "end session", "checkpoint this", "I'll continue tomorrow"
- Before a context compaction or window reset — the classic case for losing a session's thinking
- Any time a working session is about to be cut short

## The problem it solves

Handoff files rot. Appended to every session, they grow until reading one costs
more context than it restores, and the file quietly becomes a liability.

So `handoff.md` is **compacted on every write, never appended to**. Its read cost
stays roughly flat no matter how many sessions a project accumulates. Nothing is
lost — the outgoing session is moved to `.agent_docs/archive/session-<ts>.md`,
where it costs nothing until someone deliberately opens it.

## The four sections

Fixed order, always present. The parser splits on `##` headings and drops
anything it doesn't recognise, so the shape is not negotiable.

| Section | Lifetime | Content |
|---|---|---|
| **Project Snapshot** | Rewritten only when it changes | What the project is, stack, architecture, how to run and test it |
| **Cumulative Learnings** | Forever, deduped | Durable non-obvious facts: gotchas, constraints, conventions, dead ends |
| **Last Session** | Overwritten each session | 3–5 compressed bullets of the session before this one |
| **Current Session** | Archived, then replaced | Full detail of the session that just ended, plus open items |

## What you'll get

```
.agent_docs/
├── handoff.md              # compacted every write — this is what gets read
└── archive/
    └── session-<ts>.md     # full detail of every past session
```

## How it works

The agent does the judgment; the script does the mechanics.

```bash
python scripts/handoff_write.py --input payload.json
python scripts/handoff_write.py --input payload.json --dry-run   # preview, writes nothing
cat payload.json | python scripts/handoff_write.py               # or pipe it
```

The script archives the outgoing Current Session, then re-emits all four
sections in fixed order so the format cannot drift. It never decides what
belongs in the file.

**Payload** — every field optional except `current_session`:

```json
{
  "snapshot": "FastAPI service for invoice parsing. Postgres via SQLAlchemy.",
  "learnings": ["Vitest needs --pool=forks; default worker pool deadlocks on the DB mock."],
  "last_session": ["Wired up the OCR fallback; vendor B invoices now parse."],
  "current_session": {
    "date": "2026-08-23",
    "focus": "Split the parser into per-vendor strategies",
    "done": ["Extracted VendorAStrategy and VendorBStrategy"],
    "decisions": ["Strategy chosen by issuer VAT number, not filename"],
    "open_items": [{"text": "Vendor C strategy not started", "done": false}]
  }
}
```

Omit `snapshot` or `learnings` and whatever is already on disk is preserved, so
a partial payload is always safe. Omit `last_session` when a previous session
existed and the script **warns**: the outgoing session got archived but never
compressed into the rolling window, which silently breaks the chain.

## Design decisions

**Dedup is the agent's job, not the script's.** A new learning that refines an
old one should rewrite that line, not sit beside it as a near-duplicate. This
semantic merge is the only reason the file stays bounded, and no script can do
it — which is exactly why the script refuses to try.

**The learning bar is deliberately high.** A fact is promoted to Cumulative
Learnings only if it is (a) still true next month, (b) not obvious from reading
the code, and (c) expensive to rediscover.

> ✅ `Vitest needs --pool=forks here; the default worker pool deadlocks on the DB mock.`
> ✅ `Tried moving parsing into the worker — blocked by the SDK's sync-only file handles.`
> ❌ `Fixed the login bug.` — a session event, not a durable fact
> ❌ `The project uses TypeScript.` — obvious from the repo

Dead ends belong here. Knowing a path was already tried and why it failed is
worth as much as knowing what worked.

**Compress toward outcomes, not activity.** "Refactored auth to use middleware;
token refresh still unverified" earns its place. "Discussed options, tried some
things" does not. If a bullet wouldn't change what the next session does, drop it.

**Honesty is load-bearing.** Open items are recorded as they actually are,
including what was abandoned or left broken. A handoff that reads as uniformly
successful is worse than no handoff, because the next session inherits false
confidence and finds out the hard way.

**Archive-before-write.** If the archive can't be written the script aborts with
exit 2 rather than overwriting the outgoing session. Losing a session to a
permissions error is not an acceptable outcome.

## Layout

```
end-session/
├── SKILL.md
├── README.md
├── assets/
│   └── handoff_template.md    # the four sections, with inline rules per section
└── scripts/
    └── handoff_write.py       # stdlib only; archives, composes, warns
```

## Install

From the repo root, the sync script covers every platform:

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy this folder into your harness's skills directory — see the
[category README](../README.md) for the per-platform paths. Requires Python 3.8+,
no third-party packages.

## Committing

Commit `.agent_docs/handoff.md` to share handoffs across machines or teammates.
To keep them local, add `.agent_docs/` to `.gitignore`. Committing `handoff.md`
while ignoring `archive/` is a reasonable middle ground.
