# SQL and database changes

Identify the engine/version, isolation level, schema, constraints, row counts, and workload before choosing syntax or an optimization. Dialects, CTE execution, upsert semantics, and indexes differ.

## Correctness

Define result grain and expected join cardinality. Test duplicate keys, nulls, missing relations, ties, timezone boundaries, and decimal rounding. Do not use DISTINCT to conceal unexplained fan-out. Use deterministic ordering with a stable tie-breaker when pagination, latest-row selection, or top-N depends on order.

Prefer set-based operations when appropriate, while preserving outer-join and filter semantics. Parameterize values; identifiers generally need validated allowlists or dialect-aware quoting. Select explicit columns for stable interfaces. Enforce tenant boundaries and least-privilege access.

Read-then-write operations need suitable constraints, transactions, locking, or conditional writes; a transaction alone may not prevent a race at the chosen isolation level. Check conflict handling, affected row counts, deadlocks, and retry semantics. Verify the engine's MERGE/upsert behavior under concurrency.

## Performance and migrations

Use plans and representative data to examine estimated versus actual rows, scans, indexes, join strategy, sorts, spills, and lock waits. EXPLAIN ANALYZE may execute the statement and side effects; use a safe environment or non-executing plan inspection as appropriate. Do not impose a universal query length or index-every-join rule.

For schema changes, consider table rewrites, lock duration, online index support, defaults, backfill, old/new application compatibility, and rollback or roll-forward. Estimate impact before touching large production tables.

## Verification

Compare full expected results on small fixtures and reconcile counts/totals on representative data. Use database integration tests for constraints, isolation, migrations, and concurrency. Prefer stable performance budgets over brittle exact-plan snapshots. Add [data engineering](../data-engineering/GUIDE.md) for warehouse and pipeline behavior.
