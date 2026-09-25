# Plan quality review

Check the artifacts actually produced. This reviews the plan's usefulness and consistency, not the software's production readiness.

- The plan satisfies the requested scope and distinguishes evidence, confirmed constraints, proposals, and assumptions.
- Material unknowns identify their impact and affected work; reversible choices do not block unrelated progress.
- Requirements have observable acceptance evidence and implementation ownership, or explicit deferral/blocking reasons.
- Referenced IDs and relative links resolve; dependency order is possible and free of cycles.
- Important interaction states, data contracts, failure/recovery behavior, and trust boundaries are covered at the needed depth.
- Units can be implemented and verified coherently; enabling work serves an outcome.
- Unit boundaries avoid unrelated outcomes and unresolved design mixed with dependent implementation; consequential internal design is settled and local implementation choices remain clear.
- For coding-agent handoffs, ready units have settled behavior, available prerequisites, enough local context to start, and a discriminating completion check; blocked units name the unresolved decision and its owner or evidence.
- A unit's reading guidance locates the needed contracts, code, and tests without relying on prior conversation; execution records, when needed, distinguish planned work, implementation, and verified completion.
- Where units share a contract, it has an owner and integration check, and the plan identifies where parallel work must converge.
- Commands are real or clearly proposed; required environments and fixtures are identified.
- Verification covers relevant failure modes and boundaries without arbitrary quotas or redundant inventories.
- Production risks have appropriate owners and checks: compatibility, migration, deployment, performance, observability, and recovery as applicable.
- Existing decisions and user work are preserved; templates contain no unexplained placeholders or irrelevant boilerplate.
- Contradicted assumptions or changed contracts are reflected in the authoritative artifact and affected units, with stable references preserved.
- Learning resources, if requested, follow the build and learner's needs, with a consistent source for acceptance checks.
- There are no invented approvals, forced Git initialization, or stop-after-each-unit rules.

Correct gaps within scope before handing off. Report unresolved choices and unavailable evidence honestly. Do not claim a document is approved or software verified because the checklist passed.

## Rehearse a handoff

For substantial plans intended for coding agents, walk through a representative ready unit using only that unit and its designated context. Prefer one with a meaningful dependency or contract boundary. Identify the first edit, required behavior and edge cases, fixed design decisions versus local choices, and the completion check with its expected result. If an answer depends on missing context, an unsettled decision, or the planner's memory, repair the handoff and check affected units for the same gap. If no unit is ready, identify the prerequisite or discovery work needed before a rehearsal is possible.

This is a document walkthrough, not permission to implement or spawn an agent. Record briefly which unit was reviewed, gaps repaired or still open, and whether this was a walkthrough or an actual authorized execution. A successful walkthrough supports handoff clarity; it does not demonstrate build acceleration or reliability on a particular model.
