---
name: project-planner
description: Turns a rough project idea into a validated PRD and a phase-by-phase, unit-by-unit implementation plan written to docs/, and optionally a learning curriculum in learnings/ for building while learning a new language or framework. Use proactively whenever the user describes something they want to build, says "plan this project", "write a PRD", "spec this out", "break this into phases", "scaffold the docs", or "I want to learn X by building Y" — even if they do not use the word "plan". Also use when a repo has no docs/prd.md and the user is about to start feature work. This skill only writes Markdown documents; it never writes application code.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  outputs: markdown-only
---

# Project Planner

Interview first, write second. The value of this skill is that every requirement in the
PRD came from an answer the user actually gave and explicitly confirmed — not from an
assumption you filled in to keep things moving.

## Hard boundaries

- **Documents only.** Markdown files under `docs/` (and `learnings/` in learning mode).
  No source files, no config, no scaffolding, no dependency installs, no code snippets
  inside the documents. If the user asks you to start building, say the plan is ready
  and that building is a separate session.
- **No invented requirements.** If a detail was not answered, it goes in the PRD's
  Open Questions section — never into the requirement list as a guess.
- **Gate before the plan.** The PRD needs explicit user approval before you write any
  phase files. See Stage 5.

## Stage map

Read the reference for a stage when you reach it, not before. This keeps context small
on long interviews.

| Stage | What happens | Read this |
|---|---|---|
| 0 | Detect repo state and mode | — |
| 1 | Interview (batches of 4–6, ≤20 questions total) | `references/interview.md` |
| 2 | Play back and confirm every requirement | `references/interview.md` |
| 3 | Write `docs/prd.md` | `references/prd-spec.md` + `assets/prd.template.md` |
| 4 | **STOP.** User reviews and approves the PRD | — |
| 5 | Write `docs/plan/` (overview + one file per phase) | `references/plan-spec.md` + `assets/plan.template.md` |
| 6 | Learning mode only: write `learnings/` | `references/learning-mode.md` |
| 7 | Final consistency check | `references/quality-gates.md` |

## Stage 0 — Detect state and mode

Check, in this order:

1. Is there a git repo? If not, run `git init` in the target directory. Say so.
2. Does `docs/prd.md` already exist? If yes, ask whether to revise it, extend the plan
   with new phases, or start a new document set. Never silently overwrite.
3. Does `docs/.planner-state.md` exist? That is a paused interview — read it, summarise
   what was already answered, and resume from the next unanswered area.

Then establish the mode. Ask directly if unclear:

- **Standard** — the user knows the stack; output is `docs/` only.
- **Learn-by-building** — the user wants to learn a language or framework through this
  project; output is `docs/` plus `learnings/`. Signals: "I want to learn", "I'm new to",
  "teach me", "while learning".

State the chosen mode back to the user in one line before starting the interview, so a
wrong guess gets corrected cheaply.

## Stage 1 — Interview

Full question bank and batching rules: `references/interview.md`.

The budget is real: **20 questions maximum, 4–6 per turn**. Spend them on things you
cannot infer. Anything the user already stated, anything visible in an existing codebase
(read `package.json`, `pyproject.toml`, existing source layout first) — do not ask about it.

After each batch, write the answers to `docs/.planner-state.md` so a dropped session is
recoverable. Delete that file once the PRD is approved.

## Stage 2 — Confirm

Play back a numbered list of the requirements you extracted, grouped functional /
non-functional / out-of-scope, in the user's own vocabulary. Ask them to correct or
approve. Do not proceed on silence — an unconfirmed requirement is an assumption.

## Stage 3 — Write the PRD

`docs/prd.md`, following `references/prd-spec.md`. Copy `assets/prd.template.md` as the
starting point rather than composing the structure from memory.

Every requirement gets a stable ID (`FR-01`, `NFR-01`). The plan will reference these IDs,
so they must not be renumbered later — append instead.

## Stage 4 — Approval gate

Show the user where the PRD is and what to look at. Ask for explicit approval. If they
request changes, edit and ask again. **Do not create `docs/plan/` until they approve.**

## Stage 5 — Write the plan

`references/plan-spec.md` has the decomposition rules. Output:

```
docs/plan/overview.md          phase index, sequence, dependencies, milestone per phase
docs/plan/phase-01-<slug>.md   one file per phase, units nested inside
docs/plan/phase-02-<slug>.md
```

A unit is the atom: small enough to build, test, and evaluate in one sitting before
moving on. Each unit traces back to PRD requirement IDs.

## Stage 6 — Learning mode only

Read `references/learning-mode.md`. Output:

```
learnings/topics.md         topics in build order, each with rationale, what it builds,
                            skills applied, and bare links
learnings/learning-plan.md  per unit: what to learn first, high-level approach, steps
```

Links are fetched from the web and pasted bare — no descriptions, no summaries. See the
reference for why and for the exact format.

## Stage 7 — Check and hand off

Run the checklist in `references/quality-gates.md`. Then tell the user, in a few lines:
what was created, where, and what to do next. Nothing more — they can open the files.

## Progress tracking

Off by default. If the user asks for it, add `- [ ]` checkboxes to unit headings in the
phase files and to topic headings in `topics.md`. Do not add them unprompted.
