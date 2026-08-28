# Production-Grade — Cross-Language Rules

Load this alongside the language-specific guide when the task is explicitly
about hardening or shipping, not on every routine edit. These are the things
"lean" doesn't cover on its own: what to add once correctness and brevity are
settled.

## Logging & observability

- Structured/leveled logging (`info`/`warn`/`error` + context fields) over
  `print`/`console.log`. A log line with no level or context is unusable in
  aggregation.
- Log at the point that has context (what operation, what input identifiers),
  not deep in a shared helper that doesn't know why it was called.
- One log line per meaningful state transition or failure — not one per
  function call. Noise buries signal.
- Before shipping, ask: if this fails at 3am, does the log tell you what to
  do next? If not, add the missing field, don't add more logs.

## Errors

- Propagate or handle — never catch-and-ignore, never catch-log-rethrow (that's
  two log lines for one failure).
- Fail fast at the boundary that first detects the problem. Don't let a bad
  value travel three layers deep before something rejects it.
- Distinguish expected failures (validation, not-found) from unexpected ones
  (bugs, infra). Expected failures get typed/structured results or specific
  exceptions; unexpected ones should crash loudly in dev and alert in prod —
  never both silently return `null`/`None`.
- Retries need idempotency. Don't add a retry loop around an operation with a
  side effect (write, charge, send) unless it's safe to run twice.

## Dependencies & versioning

- Pin versions for anything that ships (lockfile committed, no floating
  ranges in production dependencies).
- Before adding a dependency, check: does this replace <20 lines of stdlib
  code? If yes, don't add it (same rule as the base lean-coder loop, restated
  because it's the first thing people relax under deadline pressure).

## The gate before "done"

- Run the project's own lint, typecheck, and test commands — whatever's
  already configured (`package.json` scripts, `Makefile`, CI config) — before
  declaring work finished. Don't invent a new tool; use what's there.
- If no such tooling exists, verify by re-reading the diff against the stated
  requirement and say so explicitly rather than claiming a check that didn't
  happen.
- A change that "works on my machine" but wasn't run through the project's
  existing gate isn't verified yet.

## Security posture (on top of the language guide's list)

- Secrets never appear in code, logs, or error messages — including stack
  traces surfaced to a client.
- Any input crossing a trust boundary (network, file, subprocess, DB) gets
  validated there, not three functions later where it happens to be used.

## Configuration management

- Config from environment variables or a config file, never hardcoded
  literals. `localhost:3000`, `http://api.example.com`, feature flags — all
  of these are config.
- Fail fast on missing config at startup, not at first use. A service that
  boots successfully and then crashes on the first request because `DB_URL`
  is unset is worse than one that refuses to start.
- One config surface: a single module/file that reads all config and
  exports typed values. No `os.environ["X"]` / `process.env.X` scattered
  across 12 files.
- Provide a `.env.example` (or equivalent) listing every variable the
  service needs, with dummy values. The next developer — or the next
  agent session — should not have to read code to discover what to set.

## Graceful shutdown & lifecycle

- Handle termination signals (`SIGTERM`, `SIGINT`). Stop accepting new
  work, finish in-flight requests/jobs, close connections, then exit.
- A process killed mid-write should not leave corrupt state. Use
  transactions, write-ahead patterns, or temp-file-then-rename — whatever
  the stack provides.
- Long-running background tasks need a cancellation path. A worker that
  cannot be stopped without `kill -9` is not production-ready.

## Health checks & readiness

- Expose a health endpoint (HTTP `/health`, gRPC health service, CLI
  `--healthcheck`) that returns quickly and checks only what matters:
  can the service do its job right now?
- Distinguish liveness (process is not stuck) from readiness (process can
  serve traffic). A service that is alive but cannot reach its database
  is not ready.
- Do not health-check optional dependencies — a missing analytics
  service should not make the core service report unhealthy.

## Idempotency

- Any write operation that could be retried — webhooks, queue consumers,
  API handlers behind a retry-capable client — needs an idempotency
  strategy. Assume the caller *will* retry.
- Common patterns: idempotency keys, upserts, conditional writes
  (`IF NOT EXISTS`, optimistic locking). Pick the one the data store
  supports natively.
- A retry that silently creates a duplicate is worse than a retry that
  fails loudly. Design for the duplicate case first.

## Rate limiting & backpressure

- At every trust boundary that accepts external input: cap the rate.
  An endpoint with no rate limit is a production incident waiting for
  a misbehaving client or a retry storm.
- Backpressure inward: if a downstream service is slow, shed load
  (return 503, drop from the queue with a dead-letter) rather than
  queueing unboundedly in memory.
- Log and alert on rate-limit hits — they are a signal, not just a
  guard.

## Concurrency & state safety

- Shared mutable state needs synchronization. If two requests can
  reach the same data structure, protect it (lock, atomic, channel)
  or make it immutable.
- Database operations that read-then-write need a transaction or an
  atomic operation — not two separate queries with a hope that nothing
  changes between them.
- File writes use a temp-file-then-rename pattern, not direct
  overwrite. A crash mid-write should leave the old file intact, not a
  half-written one.
- Caches shared across processes need an invalidation strategy decided
  upfront, not bolted on after the first stale-data bug.
