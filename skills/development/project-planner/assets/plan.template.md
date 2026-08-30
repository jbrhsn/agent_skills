Two templates in one file. Split them into `docs/plan/overview.md` and one `docs/plan/phase-NN-<slug>.md` per phase. The final test pass has its own template: `assets/final-test-pass.template.md`.

---
# TEMPLATE A — docs/plan/overview.md
---

# <Project name> — Development Plan

**PRD:** [prd.md](../prd.md)

**UIUX:** [uiux.md](../uiux.md)

**Final test pass:** [final-test-pass.md](final-test-pass.md)

**Mode:** standard | learn-by-building

**Surface:** web | mobile | desktop | conversational | headless

**Curriculum:** [learnings/topics.md](../../learnings/topics.md)  *(learning mode only)*

## Phases

| # | Phase | Outcome you can run and see | Units | File |
|---|---|---|---|---|
| 1 | <n> | <Milestone> | 3 | [phase-01-<slug>.md](phase-01-<slug>.md) |
| 2 | <n> | <Milestone> | 4 | [phase-02-<slug>.md](phase-02-<slug>.md) |

## Sequencing

- <What must happen in order and why.>
- <What could be reordered if priorities change.>

## Requirement coverage

| Requirement | Covered by |
|---|---|
| FR-01 | P1-U2 |
| NFR-01 | P3-U1 |

<List any requirement not covered by a unit, with the reason.>

## Surface coverage

| Surface item | States | Implemented by |
|---|---|---|
| SC-02 | Empty, Preview | P2-U1 |
| SC-02 | Working, Error | P2-U2 |
| CMP-05 | all | P2-U2 |

<List any surface item or state not implemented by a unit, with the reason. A state with no unit will not exist in the product.>

## Testing summary

- **Total test cases:** <n> across <n> units
- **Automatable:** <n> · **Manual only:** <n>
- **Test harness set up in:** P1-U<n>
- **Full-system pass:** [final-test-pass.md](final-test-pass.md), run after Phase <last>

## How to use this plan

Work one unit at a time. Build it, run its **Test cases**, check it against **Done when**, then stop and evaluate before starting the next. Do not carry a failing test case into the next unit. At the end of each phase, run **Phase exit testing** before moving on.

---
# TEMPLATE B — docs/plan/phase-NN-<slug>.md
---

# Phase <N> — <n>

**Outcome:** <What exists and is demonstrable when this phase ends.>

**Covers:** FR-01, FR-03, NFR-02

**Implements:** SC-02, CMP-03, CMP-04, CMP-05

**Depends on:** Phase <N-1>

**Units:** <count>

## Why this phase comes here

<One short paragraph. What it unblocks.>

---

### P<N>-U1 — <Unit name>

**Covers:** FR-01

**Implements:** SC-02 (Empty, Preview), CMP-03

**Depends on:** <unit ID, or "none">

**Regression check:** <test IDs from dependency units to re-run, or "none">

**Goal** <What exists after this unit that did not before. 1–2 sentences.>

**In scope**
- <…>

**Not in this unit**
- <…> — handled in P<N>-U3.

**Done when**
- <Observable statement.>
- <Observable statement.>

**Test cases**

| ID | Type | Steps | Expected result | Automate |
|---|---|---|---|---|
| T-P<N>U1-1 | Happy | <…> | <…> | Yes |
| T-P<N>U1-2 | Empty | <…> | <…> | Yes |
| T-P<N>U1-3 | Error | <…> | <…> | Yes |
| T-P<N>U1-4 | Edge | <…> | <…> | No — manual |

**Verify with** <The project's verification command, or manual steps for manual-only units.>

**Execution contract**
- Isolation: <branch per unit, commit on green, or project convention>
- Verification: <the single verification command from Phase 1, or manual steps>
- Done signal: all test cases pass, regression check passes, lint clean
- Scope boundary: do not modify files outside what **In scope** names; do not start the next unit

**Watch out for**
- <Likely failure. Omit this section if there is nothing real to say.>

---

### P<N>-U2 — <Unit name>

<Same shape.>

---

## Phase exit testing

**Every unit's test cases pass.** Re-run them; do not assume.

**Integration checks**

| ID | Steps | Expected result | Automate |
|---|---|---|---|
| T-P<N>-EXIT-1 | <Run FLOW-01 end to end> | <…> | Yes |
| T-P<N>-EXIT-2 | <Run FLOW-02, then recover> | <…> | Yes |

**Regression from earlier phases**
- [ ] <What earlier work this phase could have broken, and how to check it.>

**Phase is done when**
- [ ] Every unit test case above passes.
- [ ] Every integration check passes.
- [ ] Every regression item passes.
- [ ] <Anything else that must be true across the whole phase.>
