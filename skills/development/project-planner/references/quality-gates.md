# Quality gates

Run before handing off. Fix what fails; do not report a failure to the user as a caveat
when you could have fixed it.

This checklist audits the **documents**. The software is audited by
`docs/plan/final-test-pass.md` — do not conflate the two.

## Traceability

- [ ] Every `FR-` and `NFR-` in `docs/prd.md` appears in at least one unit's **Covers** line.
- [ ] Every **Covers** ID in the plan exists in the PRD.
- [ ] Every `SC-`, `CMP-`, and `CS-` ID in `docs/uiux.md` appears in at least one unit's
      **Implements** line.
- [ ] Every **Implements** ID in the plan exists in `docs/uiux.md`.
- [ ] Every state listed in a UIUX component entry is claimed by some unit. A state no
      unit implements will not exist in the product.
- [ ] Every FR with a user-facing effect appears in the UIUX requirement→surface map.
- [ ] Every **Depends on** unit ID exists and comes earlier in the sequence.
- [ ] `docs/plan/overview.md` lists every phase file that exists, and no phase file is
      missing from it.

## Content

- [ ] No code, pseudocode, schemas, config blocks, hex colours, pixel values, or ASCII
      wireframes in any generated document.
- [ ] Every requirement has a testable Verify line, or sits in Open Questions.
- [ ] Every unit's **Done when** is checkable without building the next unit.
- [ ] Nothing in the PRD or UIUX doc that the user did not say or confirm, except items
      listed under Assumptions or Open Questions.
- [ ] Out of scope section is non-empty. If everything is in scope, v1 is too big.
- [ ] `docs/uiux.md` documents at least one failure flow, not only happy paths.
- [ ] Every UIUX entry that fetches or submits covers loading, empty, and error states,
      or says in one line why a state cannot occur.

## Testing

- [ ] Every unit has a **Test cases** table with 3–7 rows.
- [ ] No unit has only `Happy` rows unless it genuinely has no failure mode.
- [ ] Every expected result is observable — no "works correctly", "looks right".
- [ ] Every test case ID is unique and follows `T-P<n>U<n>-<n>`.
- [ ] Every phase file ends with a **Phase exit testing** section containing integration
      checks drawn from the UIUX flows.
- [ ] If any unit is marked `Automate: Yes`, a Phase 1 unit sets up the test harness.
      That harness unit's **Done when** includes: the test runner is installed, a sample
      test passes via the project's verification command, and that command is documented
      in the plan overview.
- [ ] `docs/plan/final-test-pass.md` exists and every test ID it cites exists in a unit
      or phase file — the final pass compiles tests, it never invents them.
- [ ] Every FR and NFR appears in the final pass's requirement coverage sweep.

## Agent execution readiness

- [ ] Phase 1 units collectively cover all **bootstrap expectations** from
      `references/execution-spec.md`: lockfile committed, linter passing, single
      verification command documented, `.gitignore` for the stack, environment variable
      handling.
- [ ] Every unit has a **Verify with** line naming the exact command or manual steps.
- [ ] Every unit has an **Execution contract** with isolation, verification, done signal,
      and scope boundary.
- [ ] Every unit whose **In scope** overlaps with a dependency's scope has a
      **Regression check** line listing the dependency's test case IDs to re-run.
- [ ] The single verification command named in Phase 1 is consistent across all units'
      execution contracts.

## Learning mode

- [ ] Every unit in the plan has a section in `learning-plan.md`.
- [ ] Every topic referenced by a **Learn first** line exists in `topics.md`.
- [ ] No topic is introduced more than one phase before its first use.
- [ ] Every unit with an **Implements** line has at least one `interface`-family topic.
- [ ] Every unit has at least one `testing`-family topic, or reuses one already taught.
- [ ] Test cases in `learning-plan.md` match the plan file's tables word for word.
- [ ] Links are bare URLs, fetched from a live search, 2–4 per topic, no annotations.
- [ ] Depth matches the level the user stated in the interview.

## Housekeeping

- [ ] `docs/.planner-state.md` deleted.
- [ ] Git repo initialised if it was not already.
- [ ] Relative links between documents resolve.
- [ ] `docs/prd.md`, `docs/uiux.md`, and `docs/plan/overview.md` cross-link to each other.

## Anti-patterns to catch on re-read

**Layered phases.** "Phase 1: all models. Phase 2: all APIs. Phase 3: all UI." Nothing is
runnable until the end. Re-slice end-to-end.

**Unverifiable units.** "Set up the architecture." There is no moment where that is done.
Replace with something observable.

**Assumption laundering.** A detail the user never mentioned appearing as a firm
requirement. Move it to Open Questions or Assumptions.

**Invented UI.** A screen, component, or state in `docs/uiux.md` that no answer supports.
This is the failure mode the UIUX stage exists to prevent — catching it here means the
surface interview was too short, not that the doc needs trimming.

**Happy-path testing.** Test tables where every row is a success case. The error states
are already written down in the UIUX doc; there is no excuse.

**Curriculum drift.** Topics ordered like a textbook rather than like the build. Reorder
against the units.

**Padding.** Boilerplate NFRs nobody will check, "Watch out for" notes that say nothing,
generic topic rationales, test cases that restate the Done-when line. Delete rather than
keep.
