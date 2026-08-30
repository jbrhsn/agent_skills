# Learn-by-building mode

Only for this mode. Read after the plan files exist — the curriculum is derived from the units, so it cannot be written first.

Two files, in this order:

```
learnings/topics.md         what to learn, sequenced against the build
learnings/learning-plan.md  how to apply it, unit by unit
```

Templates: `assets/topics.template.md`, `assets/learning-plan.template.md`.

## Sequencing principle

The curriculum follows the build order, not a textbook order. The user learns a topic because the next unit needs it — that is what makes it stick and what stops the curriculum from becoming a syllabus they abandon in week two.

So: walk the phases in order, and for each unit ask "what must someone at this user's stated level already understand to build this in a production-ready way?" That set, deduplicated and ordered by first use, is `topics.md`.

Never introduce a topic more than one phase before it is used. A topic nobody applies within a week is a topic they forget.

Calibrate depth to the level answer from the interview. For someone who has never touched the language, Phase 1 topics include syntax and tooling. For someone who has read the docs, start at project structure and idioms. Do not pad the beginner path with theory they will not use, and do not skip fundamentals for an experienced user just because they sound basic — production-readiness is the bar, so error handling, testing, and configuration are topics in their own right, not footnotes.

## Three topic families

A unit needs topics from up to three families. Walk all three for every unit; a curriculum that only teaches language features produces someone who can write functions and cannot ship a product.

**Build topics** — the language, framework, and library knowledge the unit's code needs.

**Interface topics** — derived from the unit's **Implements** line and the matching entry in `docs/uiux.md`. Whatever it takes to build *those specific states* in this stack: component state handling, conditional rendering, form validation and error display, loading and empty states, navigation and routing, responsive layout, keyboard and screen reader basics. For conversational surfaces: turn parsing, session state, prompt/response structure, graceful fallback. For headless: input validation, error signalling, versioning an interface. Skip the family entirely only when the unit touches no interface at all.

**Testing topics** — derived from the unit's **Test cases** table. The topic is whatever turns those rows into something runnable: the stack's test runner and its assertions, fixtures and setup/teardown, mocking an external call, testing UI states, and — separately — what to test manually and how to keep a manual pass honest. The first unit with an `Automate: Yes` row is where the test-runner topic appears; do not introduce it earlier.

Interface and testing topics are numbered in the same `T` sequence as build topics. Do not segregate them into an appendix — they are learned in build order like everything else, and a testing topic that sits at the end of the document is a testing topic that gets skipped.

## topics.md entry format

Grouped by phase, numbered continuously. Each entry:

```markdown
### T07 — Middleware and request lifecycle
**Phase 2 · needed for P2-U1, P2-U2**
**Family:** build

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

Interface and testing topics use the identical shape with `**Family:** interface` or `**Family:** testing`, and their **What you build with it** lines cite the UIUX ID or the test case ID they serve:

```markdown
### T09 — Rendering loading and error states
**Phase 2 · needed for P2-U1**
**Family:** interface

**What you build with it**
- CMP-04 preview table across its Empty / Loading / Error states (P2-U1)
- CMP-05 retry banner, including the Retrying state (P2-U2)
```

## Rules for the Links section

- **Fetch them.** Web-search each topic and use real, current URLs. Do not reconstruct URLs from memory — they rot, and a broken link in a curriculum is worse than no link.
- **Bare URLs only.** No titles, no summaries, no descriptions, no annotations. The user asked for links, not a reading digest, and unannotated links stay correct even when the page behind them changes.
- **2–4 per topic.** Prefer official documentation first, then one high-quality secondary source. Skip anything paywalled or video-only unless nothing else exists.
- If a search turns up nothing solid for a topic, write `- (no reliable link found)` and move on. Do not invent one.

## learning-plan.md

One section per unit, in build order, mirroring the plan files. This is the bridge document: the user reads a topic in `topics.md`, then comes here to apply it.

```markdown
## P2-U1 — Parse an uploaded CSV and preview it

**Learn first:** T05, T07, T09
**Plan reference:** docs/plan/phase-02-csv-import.md
**Interface reference:** docs/uiux.md § SC-02, CMP-03, CMP-04

**How to think about this unit**
A short paragraph framing the problem the way an experienced developer in this framework
would frame it. What is the shape of the solution, and why that shape?

**How to approach the interface**
A short paragraph on how this stack handles the states this unit implements — where state
lives, what re-renders, how the error path differs from the happy path. Omit for units
with no interface work.

**High-level steps**
1. Non-code step describing what to set up.
2. …
4–7 steps. Each is a decision or a move, not a line of code.

**How to verify it**
Copy the unit's Test cases table verbatim from the plan file. Same IDs, same wording —
if the two drift, the learner ends up testing something the plan never asked for. Add one
line above it on how to run these in this stack (test runner command, or "manual for now").

**Where people get stuck**
- One or two known traps specific to this framework and this task.

**You are done when**
Mirror the "Done when" from the plan unit — same wording, so the two documents cannot
drift apart.
```

## The no-code rule applies here too

This is the file where the temptation to write code is strongest. Do not. Steps describe what to do and why, at the level of "register the parser as a route handler and return the first N rows as JSON" — not the handler itself. Test guidance names what to assert, never the assertion. The user is meant to write the code with the agent in a later session; handing them a solution removes the entire point of the mode.
