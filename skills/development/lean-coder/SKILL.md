---
name: lean-coder
description: Use for any task that writes, edits, refactors, or reviews code — writing a function, adding a feature, fixing a bug, refactoring, cleaning up, or the /review-diff and /audit-repo workflows for finding over-engineering. Applies a "lazy senior developer" discipline — the least code that correctly and safely solves the problem, reuse what exists, never over-engineer. Load it for coding work broadly, not only when invoked. Do NOT use for planning/spec docs (project-planner), UI/UX design (ui-ux-designer), or publishing repo docs (repo-docs-publisher) — those are separate skills.
metadata:
  category: engineering
  audience: developers
---

# Lean Coder

A discipline for writing the least code that correctly and safely solves the problem, applied to every coding task by default. The goal is fewer lines, fewer tokens, less to read back and maintain later — without ever cutting corners on correctness or safety.

This discipline is meant to apply to coding work broadly — writing a function, adding a feature, fixing a bug, refactoring — not only when explicitly invoked. Because skills load on demand by matching the task, this one is written to be pulled in for any coding request; once loaded, apply it throughout the task without needing a separate trigger. Only the explicit review/audit workflows below need direct invocation.

## Core principle

Before writing any code, understand the problem and the surrounding codebase, then write the smallest, most boring solution that actually solves it. Fewer lines is a byproduct of good judgment, not a target to hit by deleting things that matter.

## Required first step: read before writing

Never write code into unfamiliar territory. Before making any change:

- Read the file(s) being touched, and enough of the surrounding module/package to know what conventions, helpers, and utilities already exist there.
- Check for existing functions, components, or utilities that already do what's needed, or nearly do — reuse or extend them instead of writing a parallel implementation.
- For new files, check whether similar functionality exists elsewhere in the repo first.

Skipping this step is the single biggest cause of duplicated, bloated code — it is not optional.

**Where to stop reading.** Reading is scoped, not exhaustive — don't read the whole repo (that costs more tokens than it saves). Read the target file(s) and their direct imports/callers, skim the immediate module/package for conventions and helpers, and do one scoped search (e.g. `grep`/glob for the function or concept name) for existing equivalents. Stop once you have enough to avoid duplicating existing code and to match local conventions. If a scoped search turns up nothing, proceed — don't keep widening the search indefinitely.

**Delegate the exploration to a subagent when it's more than a couple of files.** For anything beyond a trivial single-file edit, spawn an `explore` subagent (via the Task tool) to do this read-before-writing pass instead of reading everything into the main thread yourself. This keeps the main context lean (the whole point of this skill) and lets the search run thoroughly without burning your working context. Give the subagent a precise brief and ask it to report back only what you need to write correct, non-duplicative code:

- the conventions/helpers/utilities already present in the target module,
- any existing function/component/dependency that already does (or nearly does) what's needed, with `file:line` references,
- the idiomatic patterns to match.

Specify thoroughness ("quick" for a small module, "medium"/"very thorough" for a large or unfamiliar codebase). When the change genuinely touches only one already-open file, just read it directly — a subagent would be overhead. When you need to explore several independent areas, launch multiple `explore` subagents in parallel in a single message. If subagents aren't available in the environment, do the scoped read inline instead of blocking.

## Writing the code

Once the problem and codebase are understood, apply this judgment, roughly in order of preference, without being mechanical about it — this is not a rigid checklist to narrate, it's the instinct to write from:

1. **Does this need new code at all?** If the feature is unnecessary for the actual request (speculative options, "for later" flexibility, configurability nobody asked for), don't write it. Solve what was asked, not what might be asked someday.
2. **Does it already exist in this codebase?** Reuse or extend rather than reimplement.
3. **Does the standard library or language/framework's native features cover it?** Prefer these over custom code or new abstractions.
4. **Is there already an installed dependency that does this?** Use it before adding a new one or writing custom logic. (When you do add a Python dependency, add it with `uv` — see "Python tooling" below.)
5. **Can it be written simply and directly?** Prefer the direct, obvious implementation over a clever or heavily abstracted one, even if the abstraction feels more "correct" in the abstract — build abstractions when a second or third real use case shows up, not preemptively.

Match whatever's idiomatic for the language, framework, and existing codebase conventions when deciding between stdlib/native/dependency — there's no blanket preference for avoiding new dependencies if one is already the idiomatic choice.

## Comments and docstrings

Follow the existing project's convention. If the codebase/language/team convention calls for docstrings or explanatory comments (e.g. public APIs, complex algorithms), write them properly — don't strip documentation to save lines. Where no such convention applies, keep comments minimal and only where the code isn't self-explanatory; don't narrate what the code obviously already says.

## Tests

Follow the project's existing testing convention. If the codebase has tests, write tests for new behavior at the same level of coverage the project expects — **tests are not a line-count target to cut.** Minimal production code does not mean skipping the tests that prove it works; correctness visibility is part of the non-negotiables below. Don't over-test either: cover the real behavior and edge cases that matter, not every trivial getter. If the project has no test setup and the task doesn't warrant introducing one, say so rather than silently shipping untested logic for anything non-trivial.

## Python tooling: use `uv`

For Python work, **`uv` is the default** package/environment manager over `pip`/`venv`/`pipenv`/`poetry` — unless the project already uses another tool, in which case stay consistent with it. Adding a dependency is still governed by the "Writing the code" judgment above (stdlib first). Command reference, per-command usage, and migration rules all live in **`references/python-uv.md`** — read it when doing Python dependency/environment work rather than relying on this summary.

## Non-negotiables — never cut these for brevity

These are never sacrificed to save lines or tokens, no matter how "minimal" the rest of the solution is:

- **Input validation and trust-boundary checks** — anything crossing a trust boundary (user input, external API responses, file contents) gets validated.
- **Error handling** — failure paths are handled explicitly, not silently swallowed or left to crash uninformatively.
- **Data-loss safety** — anything that could destroy user data (overwrites, deletes, migrations) gets appropriate safeguards (confirmations, backups, transactions) even if that costs a few extra lines.
- **Security** — auth checks, sanitization, secrets handling are never trimmed.
- **Accessibility** — for user-facing UI code, accessibility basics (semantic HTML, labels, keyboard support) are not optional scope-cuts.

If minimizing code would require compromising any of the above, don't compromise — write the correct version and note briefly why it's not smaller.

## Handling genuine minimal-vs-robust tradeoffs

When there's a real tradeoff between the minimal version and a slightly more robust or extensible one (not a non-negotiable from above, just a judgment call), **pause and ask** rather than silently picking one. State the two options briefly: what the minimal version does and doesn't handle, and what the more robust version would add, then let the user decide. Don't ask this for trivial cases — only when the extra robustness is a real, defensible option someone might reasonably want.

## Tracking deferred shortcuts

When a shortcut is deliberately taken (something deferred rather than solved, e.g. a hardcoded value that should eventually be configurable, an edge case knowingly left unhandled because it's out of scope right now), mark it in code with a comment:

```
// lazy: <what was deferred and why>
```

Use the language's native comment syntax. These are grep-able later (`grep -rn "lazy:"`) so deferred debt doesn't silently rot into "later means never." Don't overuse this — it's for genuine, deliberate deferrals, not a catch-all disclaimer on every function.

## Reporting impact

After a non-trivial coding task, briefly report the size of what was written so the savings from this discipline are visible. Prefer a real measurement over a guess: use `git diff --stat` (or `wc -l` on new files) for the line count, e.g. "Added ~18 lines across 2 files (per `git diff --stat`)." Token counts can't be measured reliably — if you mention one, label it explicitly as a rough estimate, don't present it as a measured figure. Skip this reporting for trivial one-line fixes where it would just be noise.

## Additional workflows

Two explicitly-invoked workflows are documented in **`references/workflows.md`**: `/review-diff` (review a diff for over-engineering) and `/audit-repo` (audit a whole repo for bloat). Load that file when either is invoked or when the user asks to "review for over-engineering," "find bloat," "what can I delete," etc. Both delegate the read-heavy pass to subagents and return findings only, not automatic fixes.

## What this skill does not do

- It does not sacrifice correctness, safety, or the non-negotiables above to hit a smaller line count.
- It does not silently choose between a minimal and a more robust implementation when the choice is genuinely debatable — it asks.
- It does not treat "fewer lines" as inherently better when the terse version is harder to understand or maintain than a slightly longer, clearer one — the target is the smallest *correct and clear* solution, not the smallest possible one.