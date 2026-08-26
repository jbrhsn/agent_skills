# Lean Coder

Write cleaner, shorter code without sacrificing correctness or security. This skill removes bloat while keeping your code testable, secure, and actually doing what it's supposed to do.

## When to Use It

Use Lean Coder whenever you're writing new code, refactoring existing code, reviewing a diff, or debugging a failure — whether it's a complete function, a small snippet, or a pull request. The skill is language-aware and works across multiple languages, so even small bits of code benefit from the discipline.

**Practical triggers:**
- You're about to write a new function or feature
- You've written something and want to trim unnecessary parts
- You're reviewing code and want to spot bloat (dead branches, unnecessary variables, over-engineering)
- You need a refactor but aren't sure where to start
- You're debugging a failure and need to fix it without adding defensive cruft
- You want to improve test-ability of an existing function
- You'd phrase it as "clean this up," "is this good code," "make this production-ready," "review my PR," or "why is this slow/broken"

## What You'll Get

- **Fewer lines of code** — unnecessary comments removed, helpers inlined, defensive checks cut
- **Better testability** — code restructured to reduce mocks and make unit tests simpler
- **Security intact** — input validation, auth checks, and error handling stay; bloat doesn't
- **Clear before/after metrics** — line-count delta shown on refactors so you know what changed

## Key Principles

The core philosophy is **"fewer lines is the tiebreaker, never the goal":**

- **Delete first** — if a line isn't required by an actual requirement, cut it
- **Use the standard library** — leverage what your language ships, not third-party packages
- **Inline ruthlessly** — a helper used once is not a helper; make it inline
- **Security always stays** — input validation, access checks, error handling never get cut
- **Test-friendly design** — if a function is hard to test without mocks, the code design is wrong

## Supported Languages & Framework

Lean Coder includes language-specific reference guides for:

- Python (including AI/ML and agent frameworks)
- SQL
- Scala / Spark
- TypeScript / React / Next.js
- Solidity
- Rust
- Swift
- Kotlin
- React Native

Each language has its own security list and best practices built into the skill.

## How It Works

The skill follows a consistent loop for every code task:

1. **Delete** — Cut anything not required by the specification
2. **Stdlib** — Use built-in language features before adding dependencies
3. **Inline** — Remove single-use helpers
4. **Secure** — Apply language-specific security rules (always kept)
5. **Production-grade** — Structured logging, no swallowed errors, run the project's own lint/test gate before calling it done
6. **Test** — Restructure until the code can be tested without excessive mocks

An additional `references/production-grade/GUIDE.md` covers cross-language hardening (logging, error propagation, dependency pinning, the pre-"done" gate). It's opt-in — load it when the task is explicitly about hardening or shipping, not on every edit.

For details on the full workflow, language guides, and the "cut on sight" checklist, see **[SKILL.md](./SKILL.md)**.

---

**Start here:** Load the skill when you're about to write code, review a diff, or refactor something that feels bloated.
