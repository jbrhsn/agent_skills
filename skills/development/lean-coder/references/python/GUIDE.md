# Python

Use the project's supported Python version, environment, lockfile, and established libraries. Run Python through `uv run`; obtain confirmation before installing uv if missing. Do not replace an existing dependency simply because a shorter standard-library example exists.

## Design and resource use

Prefer straightforward functions, dataclasses, and context managers when they fit. Preserve useful types and abstractions; validate runtime data at trust boundaries. Keep I/O separable from transformations without requiring every function to be pure.

Use streaming/chunked reads for unbounded inputs and bound concurrent requests. Async code must not block the event loop with synchronous I/O or CPU-heavy work; choose threads, processes, batching, or async clients based on the workload. Set network deadlines and connection limits; close clients and propagate cancellation.

Vectorize dataframe operations where semantics and memory permit; do not assume all row iteration is a defect. Check nulls, decimal precision, timezones, and implicit dtype coercion. Profile before replacing clear loops with clever expressions.

## Security and correctness

Parameterize SQL and pass subprocess arguments as lists with shell execution disabled unless explicitly required and safely handled. Avoid evaluating or deserializing executable content from untrusted input. Validate paths, archive extraction destinations, input sizes, and tool arguments. Generate security tokens with cryptographic randomness.

For AI/ML integrations, treat model output as untrusted, validate tool actions against permissions, bound cost/time/retries, and record model/data/configuration versions. Seeds alone do not prove reproducibility. Scope caches by model, configuration, content, and tenant permissions.

## Verification

Inject clocks or clients where determinism helps. Test pure logic with representative edge cases and external boundaries with integration tests or appropriate fakes. Use the repository's configured test, lint, and typing tools. For pipelines, also read [data engineering](../data-engineering/GUIDE.md).
