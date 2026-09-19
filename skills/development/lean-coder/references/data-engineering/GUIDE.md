# Data engineering

Use for ETL/ELT, batch, streaming, orchestration, warehouse models, and platform changes; add SQL, Python, or Spark guidance as relevant.

## Data contracts

Establish row/event grain, business key, schema/nullability, units, timezone, event versus processing time, ordering, and ownership. Identify source of truth, expected volume/freshness, retention, and downstream consumers. Avoid silently inferring production schemas or turning malformed values into valid-looking defaults.

Check contract-specific uniqueness, required fields, referential integrity, ranges, reconciliation totals, and freshness. Decide whether bad records fail a batch, are quarantined with reasons, or are accepted with explicit warnings. Protect sensitive fields in fixtures, samples, lineage, and logs.

## Replay and recovery

Define delivery semantics across source, processing, and sink. Scheduler retries and checkpoints alone do not prove exactly-once effects. Choose a stable deduplication key/window, then enforce atomic/idempotent writes or reconcile partial results. Test failure between writing output and acknowledging progress.

Specify incremental boundaries, late/out-of-order events, deletes/tombstones, schema evolution, and watermarks. A timestamp cursor can miss equal-timestamp records or late corrections; use suitable tie-breakers or overlapping windows plus deduplication.

Backfills need explicit ranges, isolation from live runs, resource limits, rerun semantics, and completion/reconciliation checks. Do not reset checkpoints or overwrite production partitions to debug without establishing scope and recovery. Check concurrent attempts and partial publication to downstream consumers.

## Performance and evidence

Inspect plans, scanned bytes, pruning, shuffle, skew, spills, sink throughput, and orchestration critical paths. Bound driver memory and task concurrency. Partitioning/clustering follows query patterns and data distribution. Avoid small-file explosions and needless full refreshes; balance cost against latency and complexity.

Use deterministic fixtures for duplicates, nulls, ties, timezone boundaries, and late data. Also test sources, sinks, and orchestration: partial failure, retry, restart, schema migration, and repeated backfill. Reconcile counts and business totals, not merely successful job status. Tiny local tests cannot establish cluster throughput or production delivery guarantees.
