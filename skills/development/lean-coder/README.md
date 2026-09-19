# Lean Coder

Guidance for building and maintaining software whose behavior can be explained, tested, and operated. Supports implementation, review, refactoring, performance work, troubleshooting, and debugging without line-count goals or a fixed architecture.

The agent reads relevant code and contracts, makes a focused change when authorized, and verifies affected behavior. Helpers, dependencies, and tests are selected for their value rather than arbitrary size or mock-count limits. A diagnosis or review stays within that scope unless a fix is requested.

| Area | Practical focus |
|---|---|
| Web | Server authorization, cache isolation, API compatibility, accessible states, measured browser/backend performance |
| Data engineering | Grain/schema contracts, replay, partial writes, backfills, data quality, streaming recovery, Spark/SQL execution |
| Web3 | Chain/account identity, transaction lifecycle, signatures, indexing/reorgs, contract invariants/upgrades |
| Android / iOS | Lifecycle, cancellation, offline state, secure storage, permissions, persistence migrations, release-device validation |
| Troubleshooting | Reproduction, evidence, hypothesis testing, root cause, bounded mitigation, regression verification |

[SKILL.md](SKILL.md) routes to focused language and domain guides. Load only relevant references. Production guidance scales with operational risk; routine edits do not require a full audit.

Results include changes or findings, test or measurement evidence, and remaining risks. Python commands use `uv run`; installing uv requires confirmation if absent.
