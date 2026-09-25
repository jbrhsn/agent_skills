# Production readiness

Select concerns affected by the change and actual operational risk. Libraries, CLIs, mobile apps, pipelines, and services need different contracts. Do not add infrastructure simply to complete this guide.

## Boundaries and failure semantics

Define valid inputs, ownership, authorization, and observable errors. Keep secrets and personal data out of logs and client error details. Distinguish validation, conflicts, transient failures, and defects. Handle or propagate errors with actionable context; avoid duplicate logging unless layers add distinct operational value.

For a changed trust boundary, identify the protected data or action, who can supply inputs, and where permission and input limits are enforced. Trace a plausible unauthorized or malformed request through that path and verify rejection at the owning boundary. Expand into a broader threat analysis only when the change warrants it.

Use deadlines, bounded concurrency, queue limits, and cancellation where work can consume unbounded resources. Retry transient failures only when replay is safe, with bounded attempts and backoff/jitter as appropriate. A timed-out write may already have committed; reconcile before retrying. An idempotency key needs durable enforcement, scope, payload matching, and expiry semantics, not just a header.

Protect invariants with datastore constraints, transactions, conditional updates, or synchronization. An in-process lock does not coordinate separate workers. Atomic file replacement depends on filesystem guarantees; durability may require additional sync and recovery handling.

For new throughput-sensitive paths, establish expected input size, arrival rate, concurrency, latency target, and memory/connection limits before choosing an implementation. Use available requirements or measurements; label unknowns and assumptions. Choose bounded work and a way to measure capacity before adding caches, queues, or distributed infrastructure. State what happens when a limit is reached: reject, defer, or apply backpressure according to the contract.

## Operability and recovery

Choose useful signals: error rate, tail latency, queue age, data freshness, job completion, or crash-free sessions. Include correlation IDs, actionable errors, and bounded metric cardinality. Redact before emission. Alerts should connect to an owner and recovery action.

For long-running processes, plan bounded shutdown and recovery of interrupted work. Distinguish readiness from liveness; avoid restarting every instance because a shared dependency is down. Document safe configuration examples and validate required settings at the point their lifecycle requires.

For durable data changes, cover schema compatibility, concurrent old/new versions, migration locks/runtime, resumability, backup/restore, and reconciliation. Use expand/migrate/contract where rolling upgrades require it. Rolling back code may not undo data changes; describe roll-forward recovery when rollback is unsafe.

## Supply chain and release

Follow ecosystem reproducibility practices: application lockfiles, pinned build tools or image digests where needed, compatible ranges for reusable libraries where appropriate. Evaluate dependencies for maintenance and security rather than size thresholds.

Identify the release artifact/configuration, supported environments, smoke checks, monitoring, and recovery conditions. Rehearse high-impact migrations on representative nonproduction data. Deployment and external mutations still follow user authorization.

Use repository checks and representative integration tests. Add load, fault, concurrency, migration, or recovery tests when those properties are affected. Compare performance against an explicit workload and target; label proposed targets as assumptions. Report untested properties and target-environment checks. A checklist is a way to find gaps, not a production-readiness certificate.
