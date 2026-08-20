# Rust — Lean Rules

## Stdlib and derives first

| Need | Use | Not |
|---|---|---|
| Boilerplate impls | `#[derive(Debug, Clone, PartialEq, Default)]` | hand-written impls |
| Errors | `thiserror` for libs, `anyhow` for bins | custom error enum + 5 `From` impls |
| Conversions | `From`/`Into`, `?` | manual match-and-map |
| Optionality | `Option` combinators (`map`, `unwrap_or`, `ok_or`) | if-let ladders |
| Iteration | iterator chains, `collect::<Result<Vec<_>,_>>()` | index loops with `push` |
| Constructors | `Default` + struct update syntax | builder for <5 fields |
| Concurrency | `Arc<Mutex<T>>`, channels, `tokio::join!` | bespoke sync primitives |

## Cut

- `match` with only `Some`/`None` arms → `if let` or a combinator
- `.clone()` added to appease the borrow checker — restructure or borrow
- `return` on the last expression; `else` after `return`
- Trait definitions with one implementor
- `mod.rs` re-export shims
- `unwrap()` in library code — propagate with `?`
- Explicit lifetimes the compiler infers

## Rules

- Take `&str`/`&[T]` in parameters, return owned types.
- Make illegal states unrepresentable: newtypes and enums instead of validation branches sprinkled at call sites. This deletes code.
- `#[non_exhaustive]` on public enums; `pub(crate)` by default.
- One `unsafe` block, documented with its invariant, or none at all.

## Security (never cut)

- No `unsafe` without a `// SAFETY:` comment stating the upheld invariant.
- Parse, don't validate: convert untrusted bytes into a typed struct at the edge (`serde` with `deny_unknown_fields`).
- Bound allocations from untrusted length prefixes; set read/decompression limits.
- Use checked/saturating arithmetic where input drives the value — release builds wrap.
- `zeroize` for key material; `constant_time_eq` for secret comparison.
- `cargo audit` and `cargo deny` in CI.

## Testability

- `#[cfg(test)] mod tests` in-file for unit tests; `tests/` for public-API integration tests.
- Depend on traits only where a second implementation genuinely exists (real + test fake).
- `proptest` on parsers and numeric code instead of a dozen hand-written cases.
- Assert on `Result` variants, not on error message strings.

## Example

```rust
// before — 11 lines of match/push
// after — 3
fn active_names(users: &[User]) -> Vec<&str> {
    users.iter().filter(|u| u.active).map(|u| u.name.as_str()).collect()
}
```
