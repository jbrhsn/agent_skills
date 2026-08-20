---
name: lean-coder
description: Write and review code with the minimum lines needed, using the standard library over dependencies and inlining over helper indirection, while keeping it secure and testable. Use this skill whenever writing new code, refactoring, reviewing a diff, or evaluating an implementation in Python, SQL, Scala/Spark, TypeScript/React, Solidity, Rust, Swift, Kotlin, or React Native — even when the user does not say "keep it short," and even for small snippets, since most bloat enters at that size.
---
# Lean Hyphen Coder

Minimum code that is correct, secure, and testable. Fewer lines is the tiebreaker, never the goal — never trade correctness or security for brevity.

## Loop (every code write or review)

1. **Delete** — Is this line required by a stated requirement? If no requirement names it, cut it.
2. **Stdlib** — Does the language/framework already ship this? Use it. No dependency for what stdlib does in ≤5 lines.
3. **Inline** — A helper used once is not a helper. Inline it.
4. **Secure** — Apply the language's security list from its reference file. Security code is never cut.
5. **Test** — Can this be tested without mocks or setup? If not, restructure until it can.

Report LOC delta on refactors: `before → after`.

## Cut on sight

Comments restating the code · defensive checks for conditions the type system rules out · try/catch that logs and rethrows · getters/setters wrapping public fields · single-use variables named `result`/`temp`/`data` · config for values with one caller · abstract base classes with one implementation · custom code duplicating stdlib · dead branches · `else` after `return`.

## Keep, always

Input validation at trust boundaries · auth and access checks · error handling that changes control flow · anything a test asserts on · a comment explaining *why* a non-obvious choice was made.

## Testability rules

Pure functions over stateful classes. Inject I/O (clock, network, DB) as arguments, not imports. One reason to change per function. If a test needs >2 mocks, the code is wrong, not the test.

## References

Load **only** the file for the language in play. Do not read the others.

| Language / framework         | File                                     |
| ---------------------------- | ---------------------------------------- |
| Python (incl. AI/ML, agents) | `references/python/GUIDE.md`           |
| SQL                          | `references/sql/GUIDE.md`              |
| Scala / Spark                | `references/scala-spark/GUIDE.md`      |
| TypeScript / React / Next.js | `references/typescript-react/GUIDE.md` |
| Solidity                     | `references/solidity/GUIDE.md`         |
| Rust                         | `references/rust/GUIDE.md`             |
| Swift                        | `references/swift/GUIDE.md`            |
| Kotlin                       | `references/kotlin/GUIDE.md`           |
| React Native                 | `references/react-native/GUIDE.md`     |

Polyglot task: load each relevant file at the moment you write that language, not upfront.
