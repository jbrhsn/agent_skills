Two templates in one file. Split them into `docs/plan/overview.md` and one
`docs/plan/phase-NN-<slug>.md` per phase.

---
# TEMPLATE A — docs/plan/overview.md
---

# <Project name> — Development Plan

**PRD:** [docs/prd.md](../prd.md)
**Mode:** standard | learn-by-building
**Curriculum:** [learnings/topics.md](../../learnings/topics.md)  *(learning mode only)*

## Phases

| # | Phase | Outcome you can run and see | Units | File |
|---|---|---|---|---|
| 1 | <Name> | <Milestone> | 3 | [phase-01-<slug>.md](phase-01-<slug>.md) |
| 2 | <Name> | <Milestone> | 4 | [phase-02-<slug>.md](phase-02-<slug>.md) |

## Sequencing

- <What must happen in order and why.>
- <What could be reordered if priorities change.>

## Requirement coverage

| Requirement | Covered by |
|---|---|
| FR-01 | P1-U2 |
| NFR-01 | P3-U1 |

<List any requirement not covered by a unit, with the reason.>

## How to use this plan

Work one unit at a time. Build it, check it against **Done when**, then stop and evaluate
before starting the next. Units are sized to be finishable in one sitting.

---
# TEMPLATE B — docs/plan/phase-NN-<slug>.md
---

# Phase <N> — <Name>

**Outcome:** <What exists and is demonstrable when this phase ends.>
**Covers:** FR-01, FR-03, NFR-02
**Depends on:** Phase <N-1>
**Units:** <count>

## Why this phase comes here

<One short paragraph. What it unblocks.>

---

### P<N>-U1 — <Unit name>

**Covers:** FR-01
**Depends on:** <unit ID, or "none">

**Goal**
<What exists after this unit that did not before. 1–2 sentences.>

**In scope**
- <…>

**Not in this unit**
- <…> — handled in P<N>-U3.

**Done when**
- <Observable statement.>
- <Observable statement.>

**How to check it**
- <Concrete action the user takes.>

**Watch out for**
- <Likely failure. Omit this section if there is nothing real to say.>

---

### P<N>-U2 — <Unit name>

<Same shape.>

---

## Phase exit check

- [ ] Every unit's **Done when** holds.
- [ ] <Anything that must be true across the whole phase.>
