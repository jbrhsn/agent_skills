# Plan quality review

Check the artifacts actually produced. This reviews the plan's usefulness and consistency, not the software's production readiness.

- The plan satisfies the requested scope and distinguishes evidence, confirmed constraints, proposals, and assumptions.
- Material unknowns identify their impact and affected work; reversible choices do not block unrelated progress.
- Requirements have observable acceptance evidence and implementation ownership, or explicit deferral/blocking reasons.
- Referenced IDs and relative links resolve; dependency order is possible and free of cycles.
- Important interaction states, data contracts, failure/recovery behavior, and trust boundaries are covered at the needed depth.
- Units can be implemented and verified coherently; enabling work serves an outcome.
- For coding-agent handoffs, ready units have settled behavior, available prerequisites, enough local context to start, and a discriminating completion check; blocked units name the unresolved decision and its owner or evidence.
- Where units share a contract, it has an owner and integration check, and the plan identifies where parallel work must converge.
- Commands are real or clearly proposed; required environments and fixtures are identified.
- Verification covers relevant failure modes and boundaries without arbitrary quotas or redundant inventories.
- Production risks have appropriate owners and checks: compatibility, migration, deployment, performance, observability, and recovery as applicable.
- Existing decisions and user work are preserved; templates contain no unexplained placeholders or irrelevant boilerplate.
- Contradicted assumptions or changed contracts are reflected in the authoritative artifact and affected units, with stable references preserved.
- Learning resources, if requested, follow the build and learner's needs, with a consistent source for acceptance checks.
- There are no invented approvals, forced Git initialization, or stop-after-each-unit rules.

Correct gaps within scope before handing off. Report unresolved choices and unavailable evidence honestly. Do not claim a document is approved or software verified because the checklist passed.
