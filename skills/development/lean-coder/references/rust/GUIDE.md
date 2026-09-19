# Rust

Use the repository's edition, minimum supported Rust version, features, runtime, and dependency conventions. Prefer clear ownership and explicit error contracts over eliminating every clone, trait, or match.

## Design and concurrency

Borrow where lifetimes remain understandable; owned values and clones are appropriate at task boundaries or when they simplify correct ownership at acceptable cost. Use enums/newtypes for real domain distinctions. Retain traits for meaningful contracts and substitution even with one production implementation.

Use Result for expected failure and preserve context without leaking secrets. Do not turn malformed input into panics; a proven internal invariant may justify an assertion. Select checked arithmetic or documented saturation according to domain semantics; overflow behavior depends on build settings.

For async tasks, define cancellation, join/error ownership, bounded channels, and shutdown. Avoid blocking the executor or holding synchronization guards across await when it can deadlock or serialize work. Separate CPU work when measurements justify it.

Keep unsafe code as small as practical and document each safety invariant, including aliasing, lifetimes, initialization, and concurrency. A safety comment alone is not proof; inspect callers and use suitable dynamic checks where applicable.

## Security and verification

Bound parsing, allocation, decompression, and recursion for untrusted data. Use maintained cryptographic primitives and appropriate secret handling; do not invent protocols. Deserialization strictness must fit compatibility requirements rather than rejecting unknown fields universally.

Use unit and public-API integration tests, property/fuzz tests for parsers/state machines when useful, and repository fmt/clippy/test/security checks as configured. Build relevant feature combinations and targets.

For on-chain programs, also use [Web3](../web3/GUIDE.md) and chain-specific documentation: validate signer/owner relationships, account derivation, permitted cross-program calls, arithmetic, and resource limits. Rust memory safety does not establish contract authorization or economic safety.
