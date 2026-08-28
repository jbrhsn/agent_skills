---
name: project-planner
description: Turns a rough project idea into a validated PRD, a UI/UX (or interaction-contract) spec, and a phase-by-phase, unit-by-unit implementation plan with built-in test cases — written to docs/, plus an optional learning curriculum in learnings/. Use proactively whenever the user describes something they want to build, says "plan this project", "write a PRD", "spec this out", "break this into phases", "scaffold the docs", "design the UI/UX", or "I want to learn X by building Y" — even if they do not use those exact words. Also use when a repo has no docs/prd.md and the user is about to start feature work. This skill only writes Markdown documents; it never writes application code.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  outputs: markdown-only
---

# Project Planner

Interview first, write second. The value of this skill is that every requirement, every
screen, and every test case came from an answer the user actually gave and explicitly
confirmed — not from an assumption you filled in to keep things moving.

## Hard boundaries

- **Documents only.** Markdown files under `docs/` (and `learnings/` in learning mode).
  No source files, no config, no scaffolding, no dependency installs, no code, no JSON/
  YAML schemas, no wireframe images inside the documents. If the user asks you to start
  building, say the plan is ready and that building is a separate session.
- **No invented requirements.** If a detail was not answered, it goes in an Open
  Questions section — never into the requirement, screen, or test list as a guess.
- **Gate before the next document.** PRD needs explicit approval before UIUX. UIUX needs
  explicit approval before the plan. See Stages 4 and 7.

## Stage map

Read the reference for a stage when you reach it, not before. This keeps context small
on long interviews.

| Stage | What happens | Read this |
|---|---|---|
| 0 | Detect repo state, mode, and surface type | — |
| 1 | Interview (batches of 4–6, ≤20 questions total) | `references/interview.md` |
| 2 | Play back and confirm every requirement | `references/interview.md` |
| 3 | Write `docs/prd.md` | `references/prd-spec.md` + `assets/prd.template.md` |
| 4 | **STOP.** User reviews and approves the PRD | — |
| 5 | Surface interview (skip for headless unless underspecified) | `references/uiux-interview.md` |
| 6 | Write `docs/uiux.md` | `references/uiux-spec.md` + `assets/uiux.template.md` |
| 7 | **STOP.** User reviews and approves the UIUX doc | — |
| 8 | Write `docs/plan/` (overview + one file per phase, test cases inline) | `references/plan-spec.md` + `references/execution-spec.md` + `references/testing-spec.md` + `assets/plan.template.md` |
| 9 | Learning mode only: write `learnings/` | `references/learning-mode.md` |
| 10 | Write `docs/plan/final-test-pass.md` (auto, once every phase file exists) | `references/testing-spec.md` + `assets/final-test-pass.template.md` |
| 11 | Final consistency check | `references/quality-gates.md` |

## Stage 0 — Detect state, mode, and surface type

Check, in this order:

1. Is there a git repo? If not, run `git init` in the target directory. Say so.
2. Does `docs/prd.md` already exist? If yes, ask whether to revise it, extend the plan
   with new phases, or start a new document set. Never silently overwrite.
3. Does `docs/.planner-state.md` exist? That is a paused interview — read it, summarise
   what was already answered, and resume from the next unanswered area.

Then establish **mode**. Ask directly if unclear:

- **Standard** — the user knows the stack; output is `docs/` only.
- **Learn-by-building** — the user wants to learn a language or framework through this
  project; output is `docs/` plus `learnings/`. Signals: "I want to learn", "I'm new to",
  "teach me", "while learning".

Then establish **surface type**, from what the user has already said about what they're
building — do not spend an interview question on this unless it's genuinely ambiguous:

- **web** — browser-based app or site
- **mobile** — native or cross-platform mobile app
- **desktop** — desktop GUI app
- **conversational** — CLI tool, chatbot, or any turn-based text/voice interface
- **headless** — library, API-only service, data pipeline, script with no direct
  end-user interaction surface

State the chosen mode and surface type back to the user in one line before starting the
interview, so a wrong guess gets corrected cheaply.

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

Every requirement gets a stable ID (`FR-01`, `NFR-01`). The UIUX doc and the plan will
reference these IDs, so they must not be renumbered later — append instead.

## Stage 4 — PRD approval gate

Show the user where the PRD is and what to look at. Ask for explicit approval. If they
request changes, edit and ask again. **Do not start Stage 5 until they approve.**

## Stage 5 — Surface interview

Read `references/uiux-interview.md`. A short, separate interview from Stage 1 — it only
runs once the PRD's functional requirements exist, because the questions are about how
those specific requirements surface to the user.

- **web / mobile / desktop / conversational** — always run this stage.
- **headless** — skip unless the PRD's Technical constraints and Data model sections
  leave the interfaces genuinely unclear; then ask only the 2–3 questions needed to
  close the gap. A headless project still gets a `docs/uiux.md`, just a short one
  written mostly from what the PRD already established.

## Stage 6 — Write the UIUX doc

`docs/uiux.md`, following `references/uiux-spec.md`. Copy the template variant from
`assets/uiux.template.md` that matches the surface type — visual (web/mobile/desktop),
conversational, or interaction-contract (headless).

Every screen, component, or conversation state traces back to one or more PRD
requirement IDs. Nothing here is a wireframe or code — states and behavior are described
in prose, not drawn.

## Stage 7 — UIUX approval gate

Show the user where `docs/uiux.md` is. Ask for explicit approval. If they request
changes, edit and ask again. **Do not create `docs/plan/` until they approve.** The plan's
units will cite UIUX sections the same way they cite requirement IDs — building the plan
against an unapproved UIUX doc means redoing units later.

## Stage 8 — Write the plan

`references/plan-spec.md` has the decomposition rules; `references/testing-spec.md` has
the per-unit and per-phase test case rules — read both before writing. Output:

```
docs/plan/overview.md          phase index, sequence, dependencies, milestone per phase
docs/plan/phase-01-<slug>.md   one file per phase, units nested inside
docs/plan/phase-02-<slug>.md
```

A unit is the atom: small enough to build, test, and evaluate in one sitting before
moving on. Each unit traces back to PRD requirement IDs, a UIUX section, and carries its
own test cases.

## Stage 9 — Learning mode only

Read `references/learning-mode.md`. Output:

```
learnings/topics.md         topics in build order, each with rationale, what it builds,
                            skills applied, and bare links — includes UI/UX and testing
                            topics when the unit calls for them
learnings/learning-plan.md  per unit: what to learn first, high-level approach, steps,
                            and the same test cases as the matching plan unit
```

Links are fetched from the web and pasted bare — no descriptions, no summaries. See the
reference for why and for the exact format.

## Stage 10 — Final test pass

Once every phase file in `docs/plan/` exists, write `docs/plan/final-test-pass.md`
automatically — do not wait for the user to ask. It compiles every unit's test cases plus
every phase's integration tests into one full-system pass the user runs after all
development is done, to catch what unit- and phase-level testing missed. Start from
`assets/final-test-pass.template.md`; rules are in `references/testing-spec.md`.

## Stage 11 — Check and hand off

Run the checklist in `references/quality-gates.md`. Then tell the user, in a few lines:
what was created, where, and what to do next. Nothing more — they can open the files.

## Progress tracking

Off by default. If the user asks for it, add `- [ ]` checkboxes to unit headings in the
phase files and to topic headings in `topics.md`. Do not add them unprompted.
