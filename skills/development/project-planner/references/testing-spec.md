# Testing spec

Read alongside `plan-spec.md` at Stage 8, and again at Stage 10.

Testing is planned at the same moment as the work, not bolted on at the end. Every unit
carries the test cases that prove it works, every phase carries the tests that prove its
units work *together*, and the whole project ends with one pass that proves nothing broke
on the way.

## Three levels

| Level | Lives in | Proves | Written at |
|---|---|---|---|
| Unit tests | Each unit in a phase file | This unit does what it claims | Stage 8 |
| Phase exit tests | End of each phase file | The phase's units integrate; earlier phases still work | Stage 8 |
| Final test pass | `docs/plan/final-test-pass.md` | The whole product works end to end | Stage 10 |

## Test case ID scheme

`T-<phase><unit>-<n>` for unit tests: `T-P2U1-3` is the third test case of unit P2-U1.
Phase exit tests: `T-P2-EXIT-1`. Final pass tests get `T-FINAL-01`.

IDs are permanent, same as requirement IDs — the final test pass cites them.

## Unit test case format

Every unit in a phase file ends with a **Test cases** table. Not prose, not a checklist of
vibes — a table someone can execute without asking a question:

```markdown
**Test cases**

| ID | Type | Steps | Expected result | Automate |
|---|---|---|---|---|
| T-P2U1-1 | Happy | Upload a valid 20-row CSV | First 5 rows appear in the preview table; import action becomes enabled | Yes |
| T-P2U1-2 | Empty | Open the screen with no file chosen | Preview area shows the empty state; import action disabled | Yes |
| T-P2U1-3 | Error | Upload a file that is not a CSV | Error banner names the problem; chosen file is cleared | Yes |
| T-P2U1-4 | Edge | Upload a CSV with headers but zero data rows | Preview shows the empty state, not an error | Yes |
| T-P2U1-5 | Visual | Resize to a narrow viewport during preview | Table scrolls horizontally; no content is clipped | No — manual |
```

Column rules:

- **Type** — one of `Happy`, `Empty`, `Error`, `Edge`, `Permission`, `Perf`, `Visual`,
  `Regression`. The type set forces coverage; a unit with only `Happy` rows is
  under-tested and you should say so rather than shipping it.
- **Steps** — what a person actually does, in one line. If it takes more than two
  sentences, the unit is too big — go back and split it.
- **Expected result** — observable. "Works correctly" is not a result. State what appears,
  what changes, what is stored, or what is refused.
- **Automate** — `Yes`, or `No — manual` with the reason in three words. This column is a
  planning signal for the build session, not a promise that automation exists.

### How many, and where they come from

**3–7 per unit.** Derive them, do not brainstorm them:

1. One per **Verify** line of every requirement the unit covers → `Happy` rows.
2. One per **state** in the UIUX entries the unit implements — empty, loading, error,
   disabled → `Empty` / `Error` rows. This is the whole reason the UIUX doc comes first.
3. One per **edge case** or behavior rule named in the UIUX component entry.
4. One `Regression` row if the unit changes something an earlier unit built.

A unit that covers no requirement and no UIUX section should not exist. If you cannot
derive test cases for a unit, the unit is not observable — fix the unit.

### The no-code rule applies

Name the test, never write it. "Assert the preview renders 5 rows" is a test case.
`expect(rows).toHaveLength(5)` is code and does not belong in any document this skill
produces. Test framework choice is a build-session decision unless the PRD already fixed
it as a constraint.

## Phase exit tests

Each phase file ends with:

```markdown
## Phase exit testing

**Every unit's test cases pass.** Re-run them; do not assume.

**Integration checks**

| ID | Steps | Expected result | Automate |
|---|---|---|---|
| T-P2-EXIT-1 | Run FLOW-01 start to finish without reloading | Import completes and the result screen shows the correct row count | Yes |
| T-P2-EXIT-2 | Run FLOW-02 (unparseable file), then immediately retry with a valid file | Retry succeeds; no state left over from the failed attempt | Yes |

**Regression from earlier phases**
- [ ] P1-U2's login still works after the session changes in P2-U3.

**Phase is done when**
- [ ] Every unit test case above passes.
- [ ] Every integration check passes.
- [ ] Every regression item passes.
- [ ] <Anything else that must be true across the whole phase.>
```

Integration checks come from the **flows** in `docs/uiux.md` — a flow crosses units by
definition, so it cannot be tested inside one. Aim for one integration check per flow the
phase completes, plus one per pair of units that talk to each other.

## Final test pass — `docs/plan/final-test-pass.md`

Written automatically at Stage 10, once every phase file exists. This is the pre-release
sweep: the user has finished building and wants to know what is actually broken.

Structure:

```markdown
# <Project name> — Final Test Pass

**PRD:** [prd.md](../prd.md) · **UIUX:** [uiux.md](../uiux.md) · **Plan:** [overview.md](overview.md)

Run this once all phases are complete. Work top to bottom; log failures as you go rather
than fixing mid-pass, so a fix does not hide a second failure.

## 1. Requirement coverage sweep

| Requirement | Verified by | Result |
|---|---|---|
| FR-01 | T-P2U1-1, T-P2-EXIT-1 | ☐ |
| NFR-02 | T-P4U2-3 | ☐ |

Every FR and NFR in the PRD appears here. Any row with no test is a gap — fix the plan,
not the table.

## 2. Flow walkthroughs

| ID | Flow | Steps | Expected result | Result |
|---|---|---|---|---|
| T-FINAL-01 | FLOW-01 | <end-to-end> | <observable outcome> | ☐ |

One row per flow in `docs/uiux.md`, happy and unhappy alike.

## 3. Interface state sweep

One row per screen/component state, or conversation state, or interface failure mode in
`docs/uiux.md`. This is the pass that catches the empty state nobody ever looked at.

| ID | Surface | State | How to reach it | Expected | Result |
|---|---|---|---|---|---|
| T-FINAL-08 | CMP-05 | Retrying | Fail an import, press retry | Banner stays, action disabled | ☐ |

## 4. Non-functional checks

One row per NFR, with the actual measurement recorded, not just pass/fail.

## 5. Cross-cutting checks

- Fresh install: does the product work with no data at all?
- Interrupted operations: kill the process mid-action, restart — what state is left?
- Permissions/roles: can each role do exactly what the PRD says and nothing more?
- Accessibility floor from the UIUX doc's cross-cutting rules.
- Error message audit: every error a user can reach says something useful.

## 6. Defect log

| # | Test ID | What happened | Severity | Status |
|---|---|---|---|---|
```

Every test case referenced here must already exist in a unit or phase file — the final
pass **compiles**, it does not invent new tests. If writing this document surfaces a
scenario nothing covers, add the case to the unit that owns it and cite it here, so the
two stay in sync.

## Anti-patterns

**Happy-path-only units.** Five test cases that all describe things going right. Every
unit with a failure mode gets at least one `Error` row.

**Untestable expected results.** "Works as expected", "looks right", "no bugs". Replace
with something a stranger could check.

**Automation theatre.** Marking everything `Yes` in the Automate column when the project
has no test harness planned. If Phase 1 does not include setting one up, most early units
are `No — manual` and that is fine — say so honestly.

**Duplicated test cases.** The same check appearing in three units. Put it in the unit
that introduces the behavior; later units cite it as a `Regression` row instead of
restating it.

**Testing the plan instead of the product.** `quality-gates.md` checks the documents.
This file checks the software. Do not mix them.
