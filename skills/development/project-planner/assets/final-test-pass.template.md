# <Project name> — Final Test Pass

**PRD:** [prd.md](../prd.md) · **UIUX:** [uiux.md](../uiux.md) · **Plan:** [overview.md](overview.md)

**Last updated:** <YYYY-MM-DD>

Run this once all phases are complete. Work top to bottom and log failures as you go rather than fixing mid-pass — a fix applied halfway through can hide a second failure.

Every test ID below already exists in a unit or phase file. This document compiles; it does not invent. If a scenario here has no owning test case, add it to the unit that owns the behavior first.

## 1. Requirement coverage sweep

| Requirement | Verified by | Result | Notes |
|---|---|---|---|
| FR-01 | T-P2U1-1, T-P2-EXIT-1 | ☐ | |
| FR-02 | <…> | ☐ | |
| NFR-01 | <…> | ☐ | |

<Every FR and NFR from the PRD appears here. A row with no test is a gap in the plan.>

## 2. Flow walkthroughs

| ID | Flow | Steps | Expected result | Result |
|---|---|---|---|---|
| T-FINAL-01 | FLOW-01 | <end to end> | <observable outcome> | ☐ |
| T-FINAL-02 | FLOW-02 | <failure and recovery> | <…> | ☐ |

<One row per flow in docs/uiux.md — happy and unhappy alike.>

## 3. Interface state sweep

| ID | Surface | State | How to reach it | Expected | Result |
|---|---|---|---|---|---|
| T-FINAL-08 | CMP-05 | Retrying | <…> | <…> | ☐ |
| T-FINAL-09 | SC-02 | Empty | <…> | <…> | ☐ |

<One row per screen state, component state, conversation state, or interface failure mode in docs/uiux.md. This is the pass that catches the empty state nobody ever looked at.>

## 4. Non-functional checks

| ID | NFR | How to measure | Target | Measured | Result |
|---|---|---|---|---|---|
| T-FINAL-20 | NFR-01 | <…> | <…> | ______ | ☐ |

<Record the actual measurement, not just pass/fail.>

## 5. Cross-cutting checks

- [ ] **Fresh install** — works with no data at all; every empty state is reachable and sane.
- [ ] **Interrupted operation** — kill mid-action and restart; no corrupt or stuck state.
- [ ] **Permissions and roles** — each role can do exactly what the PRD allows, no more.
- [ ] **Accessibility floor** — the cross-cutting rules in `docs/uiux.md` hold on every screen.
- [ ] **Error message audit** — every reachable error says something a user can act on.
- [ ] **Repeat run** — running the main flow twice in a row behaves identically.

## 6. Defect log

| # | Test ID | What happened | Severity | Status |
|---|---|---|---|---|
| 1 | <…> | <…> | Blocker / Major / Minor | Open / Fixed / Won't fix |

## 7. Sign-off

- [ ] No Blocker defects open.
- [ ] Every Major defect is either fixed or explicitly accepted below.
- [ ] Success criteria from `docs/prd.md` § 8 are met.

**Accepted known issues:** <…>
