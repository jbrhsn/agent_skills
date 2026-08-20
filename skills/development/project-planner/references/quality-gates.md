# Quality gates

Run before handing off. Fix what fails; do not report a failure to the user as a caveat
when you could have fixed it.

## Traceability

- [ ] Every `FR-` and `NFR-` in `docs/prd.md` appears in at least one unit's **Covers** line.
- [ ] Every **Covers** ID in the plan exists in the PRD.
- [ ] Every **Depends on** unit ID exists and comes earlier in the sequence.
- [ ] `docs/plan/overview.md` lists every phase file that exists, and no phase file is
      missing from it.

## Content

- [ ] No code, pseudocode, schemas, or config blocks in any generated document.
- [ ] Every requirement has a testable Verify line, or sits in Open Questions.
- [ ] Every unit's **Done when** is checkable without building the next unit.
- [ ] Nothing in the PRD that the user did not say or confirm, except items listed under
      Assumptions.
- [ ] Out of scope section is non-empty. If everything is in scope, v1 is too big.

## Learning mode

- [ ] Every unit in the plan has a section in `learning-plan.md`.
- [ ] Every topic referenced by a **Learn first** line exists in `topics.md`.
- [ ] No topic is introduced more than one phase before its first use.
- [ ] Links are bare URLs, fetched from a live search, 2–4 per topic, no annotations.
- [ ] Depth matches the level the user stated in the interview.

## Housekeeping

- [ ] `docs/.planner-state.md` deleted.
- [ ] Git repo initialised if it was not already.
- [ ] Relative links between documents resolve.

## Anti-patterns to catch on re-read

**Layered phases.** "Phase 1: all models. Phase 2: all APIs. Phase 3: all UI." Nothing is
runnable until the end. Re-slice end-to-end.

**Unverifiable units.** "Set up the architecture." There is no moment where that is done.
Replace with something observable.

**Assumption laundering.** A detail the user never mentioned appearing as a firm
requirement. Move it to Open Questions or Assumptions.

**Curriculum drift.** Topics ordered like a textbook rather than like the build. Reorder
against the units.

**Padding.** Boilerplate NFRs nobody will check, "Watch out for" notes that say nothing,
generic topic rationales. Delete rather than keep.
