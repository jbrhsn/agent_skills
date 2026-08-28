# Plan spec

Only after both the PRD and the UIUX doc are approved. Start from
`assets/plan.template.md`. Read `references/testing-spec.md` before writing units — the
test cases are part of the unit, not an afterthought.

## Files

```
docs/plan/overview.md
docs/plan/phase-01-<slug>.md
docs/plan/phase-02-<slug>.md
docs/plan/final-test-pass.md   (written at Stage 10, after all phase files exist)
```

`<slug>` is 2–4 lowercase hyphenated words describing the phase outcome
(`phase-02-csv-import`, not `phase-02-backend`).

## Phases

A phase ends at a milestone the user can actually run and look at. Aim for 3–6 phases
for a v1; more than 7 means the phases are too thin.

Order by dependency, not by architectural layer. "All the models, then all the routes,
then all the UI" gives the user nothing runnable until the end and hides integration
problems until they are expensive. Prefer a thin end-to-end slice first, then widen it.

Phase 1 is almost always: project skeleton + one trivial end-to-end path + a way to run
and test it. That path is what every later unit plugs into.

**Phase 1 also decides the test harness.** If any unit anywhere in the plan is marked
`Automate: Yes`, one Phase 1 unit sets up the ability to run tests at all. Otherwise the
Automate column is a wish, not a plan. In learn-by-building mode this is non-negotiable —
writing tests is one of the things being learned.

Phase 1 also carries **bootstrap expectations** — see `references/execution-spec.md`.

## Units

A unit is the atom of work: **one sitting — build it, test it, evaluate it, then stop.**
Roughly 2–4 units per phase; if a phase has more than 6, split the phase.

A unit is sized right when:
- it produces one observable change the user can demonstrate,
- it can be verified without building the next unit first,
- describing its acceptance takes one or two lines, not a paragraph,
- its test cases fit in 3–7 rows without any row needing a paragraph of steps.

Too big: "Build the import feature." Too small: "Create the file." Right: "Accept a CSV
upload and show the parsed first 5 rows on screen."

### Regression guard

See `references/execution-spec.md`. When a unit touches behavior from a dependency,
that dependency's test cases re-run as part of this unit — not deferred to phase exit.

### Slicing against the UIUX doc

For visual and conversational surfaces, let the UIUX doc drive unit boundaries:

- A unit usually implements **one screen in one or two of its states**, or one component
  across all its states, or one command with its responses.
- Do not split a component's states across units unless the later states genuinely depend
  on work that has not happened yet (e.g. the error state needs the API that a later unit
  builds). When you do split, say which unit finishes the component.
- A screen whose states span more than one unit needs a note in the earlier unit saying
  the screen is incomplete until the later one lands — otherwise the build session will
  think it is done.

## Unit format

```markdown
### P2-U1 — Parse an uploaded CSV and preview it

**Covers:** FR-03, FR-04
**Implements:** SC-02 (Empty, Preview states), CMP-03, CMP-04
**Depends on:** P1-U3
**Regression check:** T-P1U3-1, T-P1U3-2 (re-run — this unit modifies the upload handler P1-U3 introduced)

**Goal**
One or two sentences: what exists after this unit that did not before.

**In scope**
- Bullet list of what this unit touches.

**Not in this unit**
- The things a reader would reasonably assume are included, but are not. Name them and
  point at the unit that does handle them.

**Done when**
- Observable, checkable statements. Each maps to a Verify line from the PRD or a state
  from the UIUX doc.

**Test cases**

| ID | Type | Steps | Expected result | Automate |
|---|---|---|---|---|
| T-P2U1-1 | Happy | … | … | Yes |
| T-P2U1-2 | Empty | … | … | Yes |
| T-P2U1-3 | Error | … | … | No — manual |

**Verify with**
Run the project's verification command and confirm all test cases in this unit pass.
For units with only manual tests: start the dev server, walk through each test case,
and record the result.

**Execution contract**
- Isolation: work on a branch; commit on green
- Verification: <the project's single verification command from Phase 1, or manual steps>
- Done signal: all test cases pass, regression check passes, lint clean
- Scope boundary: do not modify files outside what **In scope** names; do not start the
  next unit

**Watch out for**
- The one or two things most likely to go wrong here. Optional — omit rather than pad.
```

**Implements** is the UIUX counterpart of **Covers**. Name the exact states, not just the
screen ID — "SC-02" tells a build session nothing about whether the error state is in
scope this sitting. For headless projects, cite the interface IDs (`CS-01`) instead.

**Regression check**, **Verify with**, and **Execution contract** are explained in
`references/execution-spec.md`. They scope the executing agent's session so it knows how
to verify, what to re-test, and when to stop.

No code, no file paths that presume an implementation, no library names unless the PRD
already fixed them as constraints. The plan says *what* and *done when*; the build session
decides *how*. The execution contract says *how to scope and verify the session* — that is
planning, not implementation.

## Phase file structure

```
# Phase N — Name
Outcome / Covers / Implements / Depends on / Units count
## Why this phase comes here
### P<N>-U1 …  (units, each with test cases)
### P<N>-U2 …
## Phase exit testing        ← see testing-spec.md
```

Every phase file ends with **Phase exit testing**, not a bare checklist. The format is in
`references/testing-spec.md`.

## overview.md

- One-line description of the project, linking to `docs/prd.md` and `docs/uiux.md`.
- Table: phase number, name, outcome/milestone, unit count, file link.
- Dependency notes — anything that must happen in order, and anything that can be
  reordered if the user wants to.
- **Requirement coverage:** every `FR-` and `NFR-` ID from the PRD appears in at least one
  unit's Covers line. List any that do not, and say why (deferred to Later, or genuinely
  uncovered — the second one is a bug in the plan, fix it before handing off).
- **Surface coverage:** every `SC-`, `CMP-`, and `CS-` ID from `docs/uiux.md` appears in at
  least one unit's Implements line, with every state accounted for. A component state that
  no unit implements is a state that will not exist in the product.
- **Testing summary:** total test case count, how many are automatable, and which unit
  sets up the test harness.

## Learning mode

Same structure. Do not add learning material to the plan files — the plan stays a build
document, and `learnings/` stays the teaching document. Keeping them separate is what lets
the user re-read the plan later without wading through tutorial content.
