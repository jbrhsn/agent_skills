# Verification planning

Plan checks that prove behavior and expose realistic failures. Test volume follows risk, not a row quota. Implementation units may require unit, integration, contract, property, device, or end-to-end tests; the name “unit” in a plan does not prescribe a testing level.

## Useful test cases

Identify setup/input, action, expected observable outcome, test level/environment, and whether automation exists or is proposed. Include failure, boundary, authorization, concurrency, and recovery cases when relevant. Reuse stable IDs where documents cross-reference them.

For example: interrupt an import after output commits but before acknowledgement, replay the batch, then verify no duplicate business keys and matching totals. This proves more than checking a mock writer was called once.

Use fast deterministic tests for logic and real boundary tests for persistence, protocols, migrations, and lifecycle. Mocks help reproduce faults but cannot establish the external service's contract. Select critical end-to-end journeys rather than duplicating every lower-level test in a slow suite.

## Domain-sensitive evidence

- Web: direct server authorization, cache isolation, request races, keyboard/focus behavior, production rendering when affected.
- Data: grain/quality, duplicate/late input, partial write/restart, schema evolution, repeat backfill, source-to-sink reconciliation.
- Web3: invariant/fuzz tests, privileged versus permissionless access, signature replay, transaction failure/replacement, reorg recovery, pinned fork integration.
- Mobile: process death/backgrounding, denied permissions, offline recovery, storage migration, device/OS differences, release builds.
- Debugging: a reproduction of the original fault, a discriminating causal check, and relevant regression coverage.

Performance checks define workload, environment, warmup, concurrency, metrics, and budget. Security analysis and tests do not replace an independent audit when one is required.

## Integration and release

At milestones, verify completed flows and affected regressions. Reuse still-valid check results; rerun when code, environment, or risk warrants it. Record baseline failures separately.

For substantial release work, use [the release-pass template](../assets/final-test-pass.template.md) as an index of important evidence, cross-system checks, and remaining gaps. Reference authoritative test cases instead of copying all tables. Release-specific checks may have their own IDs and owners; they need not pretend to be unit tests.

Include migration/rollback or roll-forward rehearsals, old/new compatibility, representative data, observability, and recovery where relevant. Distinguish planned, passed, failed, and not-run checks and record the tested revision/environment. Documents containing test cases are not evidence those tests passed.
