# Learn-by-building mode

Only for this mode. Read after the plan files exist — the curriculum is derived from the
units, so it cannot be written first.

Two files, in this order:

```
learnings/topics.md         what to learn, sequenced against the build
learnings/learning-plan.md  how to apply it, unit by unit
```

Templates: `assets/topics.template.md`, `assets/learning-plan.template.md`.

## Sequencing principle

The curriculum follows the build order, not a textbook order. The user learns a topic
because the next unit needs it — that is what makes it stick and what stops the
curriculum from becoming a syllabus they abandon in week two.

So: walk the phases in order, and for each unit ask "what must someone at this user's
stated level already understand to build this in a production-ready way?" That set,
deduplicated and ordered by first use, is `topics.md`.

Never introduce a topic more than one phase before it is used. A topic nobody applies
within a week is a topic they forget.

Calibrate depth to the level answer from the interview. For someone who has never touched
the language, Phase 1 topics include syntax and tooling. For someone who has read the docs,
start at project structure and idioms. Do not pad the beginner path with theory they will
not use, and do not skip fundamentals for an experienced user just because they sound basic
— production-readiness is the bar, so error handling, testing, and configuration are topics
in their own right, not footnotes.

## topics.md entry format

Grouped by phase, numbered continuously. Each entry:

```markdown
### T07 — Middleware and request lifecycle
**Phase 2 · needed for P2-U1, P2-U2**

**Why this topic**
One or two sentences on what problem it solves in this project specifically. Not a
generic definition — the user can read a definition at the links.

**What you build with it**
- Request logging on every route (P2-U1)
- Auth check before the import endpoint (P2-U2)

**Skills you apply**
- Writing a middleware function and registering it in the right order
- Deciding what belongs in middleware vs in a handler
- Debugging a request that never reaches its handler

**Links**
- https://example.com/docs/middleware
- https://example.com/guide/lifecycle
```

## Rules for the Links section

- **Fetch them.** Web-search each topic and use real, current URLs. Do not reconstruct
  URLs from memory — they rot, and a broken link in a curriculum is worse than no link.
- **Bare URLs only.** No titles, no summaries, no descriptions, no annotations. The user
  asked for links, not a reading digest, and unannotated links stay correct even when the
  page behind them changes.
- **2–4 per topic.** Prefer official documentation first, then one high-quality secondary
  source. Skip anything paywalled or video-only unless nothing else exists.
- If a search turns up nothing solid for a topic, write `- (no reliable link found)` and
  move on. Do not invent one.

## learning-plan.md

One section per unit, in build order, mirroring the plan files. This is the bridge
document: the user reads a topic in `topics.md`, then comes here to apply it.

```markdown
## P2-U1 — Parse an uploaded CSV and preview it

**Learn first:** T05, T07
**Plan reference:** docs/plan/phase-02-csv-import.md

**How to think about this unit**
A short paragraph framing the problem the way an experienced developer in this framework
would frame it. What is the shape of the solution, and why that shape?

**High-level steps**
1. Non-code step describing what to set up.
2. …
4–7 steps. Each is a decision or a move, not a line of code.

**Where people get stuck**
- One or two known traps specific to this framework and this task.

**You are done when**
Mirror the "Done when" from the plan unit — same wording, so the two documents cannot
drift apart.
```

## The no-code rule applies here too

This is the file where the temptation to write code is strongest. Do not. Steps describe
what to do and why, at the level of "register the parser as a route handler and return the
first N rows as JSON" — not the handler itself. The user is meant to write the code with
the agent in a later session; handing them a solution removes the entire point of the mode.
