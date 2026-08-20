# Plan spec

Only after PRD approval. Start from `assets/plan.template.md`.

## Files

```
docs/plan/overview.md
docs/plan/phase-01-<slug>.md
docs/plan/phase-02-<slug>.md
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

## Units

A unit is the atom of work: **one sitting — build it, test it, evaluate it, then stop.**
Roughly 2–4 units per phase; if a phase has more than 6, split the phase.

A unit is sized right when:
- it produces one observable change the user can demonstrate,
- it can be verified without building the next unit first,
- describing its acceptance takes one or two lines, not a paragraph.

Too big: "Build the import feature." Too small: "Create the file." Right: "Accept a CSV
upload and show the parsed first 5 rows on screen."

## Unit format

```markdown
### P2-U1 — Parse an uploaded CSV and preview it

**Covers:** FR-03, FR-04
**Depends on:** P1-U3

**Goal**
One or two sentences: what exists after this unit that did not before.

**In scope**
- Bullet list of what this unit touches.

**Not in this unit**
- The things a reader would reasonably assume are included, but are not. Name them and
  point at the unit that does handle them.

**Done when**
- Observable, checkable statements. Each maps to a Verify line from the PRD where possible.

**How to check it**
- The concrete action the user takes to confirm. Manual steps are fine.

**Watch out for**
- The one or two things most likely to go wrong here. Optional — omit rather than pad.
```

No code, no file paths that presume an implementation, no library names unless the PRD
already fixed them as constraints. The plan says *what* and *done when*; the build session
decides *how*.

## overview.md

- One-line description of the project, linking to `docs/prd.md`.
- Table: phase number, name, outcome/milestone, unit count, file link.
- Dependency notes — anything that must happen in order, and anything that can be
  reordered if the user wants to.
- Coverage check: every `FR-` and `NFR-` ID from the PRD appears in at least one unit.
  List any that do not, and say why (deferred to Later, or genuinely uncovered — the
  second one is a bug in the plan, fix it before handing off).

## Learning mode

Same structure. Do not add learning material to the plan files — the plan stays a build
document, and `learnings/` stays the teaching document. Keeping them separate is what lets
the user re-read the plan later without wading through tutorial content.
