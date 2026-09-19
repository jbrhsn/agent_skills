---
name: lean-coder
description: Implement, review, refactor, optimize, and debug production software across web, data pipelines, Web3, Android, and iOS. Use for code changes and investigations that need clear design, evidence-based diagnosis, security, and proportionate verification.
---

# Lean Coder

Optimize for correct behavior, understandable code, and dependable operation. Simplicity means fewer concepts and less unnecessary work, not the fewest lines. Adapt this guidance to the repository, task, and risk; do not turn a small fix into an architecture rewrite or release audit.

## Establish the task

Read relevant code, callers, tests, configuration, and repository instructions. Identify the observable outcome, compatibility constraints, and existing verification commands. Reuse established libraries and patterns unless there is a concrete reason to change them.

Distinguish implementation, review, diagnosis, and optimization. A review reports actionable findings with file locations and consequences; a diagnosis establishes cause and uncertainty. Neither alone authorizes edits. For an authorized fix, continue through implementation and verification. Preserve unrelated work.

Inspect installed versions and deployment targets before using version-sensitive APIs. Consult official documentation when behavior is uncertain or changing; state unavailable evidence rather than inventing compatibility.

## Make the change

- Choose the smallest coherent change that satisfies the requirement, including necessary failure behavior. Retain single-use helpers, interfaces, and named variables when they explain intent, isolate effects, or establish a useful boundary.
- Prefer existing platform capabilities when they fit. A maintained dependency can be safer and cheaper than custom parsing, cryptography, retries, or protocol code; assess compatibility, maintenance, license, and operational cost rather than line count.
- Validate untrusted input and enforce authorization at the boundary that owns the action. Types and hidden UI controls do not validate network data or prove permission.
- Model state changes, retries, cancellation, and concurrent updates explicitly where they affect correctness. Preserve existing contracts unless a change to them is intended.
- Separate computation from external effects when useful for reasoning and testing. Use fakes, mocks, integration tests, and real services according to what must be proved; no mock-count quotas.
- Optimize against a concrete workload or diagnosed bottleneck. Record a baseline and compare under equivalent conditions, including correctness, latency distribution, throughput, memory, or cost as appropriate.

## Verify and explain

Use existing project checks relevant to the change and any required CI gates. Test the defect or changed contract, including meaningful failure cases; use integration tests when a boundary cannot be proved by isolated tests. Avoid tests that merely restate implementation. Reuse valid results and expand verification when a failure or remaining risk justifies it.

For Python commands use `uv run`. If uv is missing, ask for confirmation before installing it and verify availability afterward; continue independent inspection meanwhile.

Review the final diff for unintended behavior and sensitive data. Report changes or findings, evidence from checks or measurements, and material limitations. Distinguish passed, failed, and not-run checks; never equate a green unit suite with production readiness. Report line counts only if useful or requested.

## Load relevant references

Select references for the boundary being changed; do not read every guide for every task. Polyglot work may need more than one.

| Context | Reference |
|---|---|
| Failure, incident, flaky test, performance regression | [Debugging](references/debugging/GUIDE.md) |
| Reliability, release, migrations, service boundaries | [Production readiness](references/production-grade/GUIDE.md) |
| Browser, API, backend | [Web](references/web/GUIDE.md) |
| Batch, streaming, orchestration, warehouse | [Data engineering](references/data-engineering/GUIDE.md) |
| Wallets, transactions, RPC, indexing | [Web3](references/web3/GUIDE.md) |
| Python and AI/ML | [Python](references/python/GUIDE.md) |
| SQL and database changes | [SQL](references/sql/GUIDE.md) |
| Scala and Spark | [Scala / Spark](references/scala-spark/GUIDE.md) |
| TypeScript, React, Next.js | [TypeScript / React](references/typescript-react/GUIDE.md) |
| EVM contracts | [Solidity](references/solidity/GUIDE.md) |
| Rust services and programs | [Rust](references/rust/GUIDE.md) |
| iOS and Swift | [Swift](references/swift/GUIDE.md) |
| Android and Kotlin | [Kotlin](references/kotlin/GUIDE.md) |
| Cross-platform mobile | [React Native](references/react-native/GUIDE.md) |
