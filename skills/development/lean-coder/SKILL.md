---
name: lean-coder
description: Use for any task that writes, edits, refactors, or reviews code — writing a function, adding a feature, fixing a bug, refactoring, cleaning up, or the /review-diff and /audit-repo workflows for finding over-engineering. Applies a "lazy senior developer" discipline — the least code that correctly and safely solves the problem, reuse what exists, never over-engineer — with a read-before-writing pass, self-verification before reporting, and explicit hand-back gates on genuine minimal-vs-robust tradeoffs. Load it for coding work broadly, not only when invoked. Do NOT use for planning/spec docs (project-planner), UI/UX design (ui-ux-designer), or publishing repo docs (repo-docs-publisher) — those are separate skills.
metadata:
  category: engineering
  audience: developers
---

# Lean Coder

A discipline for writing the least code that correctly and safely solves the problem, applied to every coding task by default. The goal is fewer lines, fewer tokens, less to read back and maintain later — without ever cutting corners on correctness or safety. Fewer lines is a byproduct of good judgment, not a target to hit by deleting things that matter.

This discipline applies to coding work broadly — writing a function, adding a feature, fixing a bug, refactoring — not only when explicitly invoked. Because skills load on demand by matching the task, this one is pulled in for any coding request; once loaded, apply it throughout the task without needing a separate trigger. Only the explicit review/audit workflows (Units A/B below) need direct invocation.

## Two paths

- **BUILD path** (Units B1–B4) — write/edit/refactor/fix code. Use for any normal coding request.
- **REVIEW/AUDIT path** (Units A1–A2) — the explicitly-invoked `/review-diff` and `/audit-repo` workflows that find over-engineering and **report findings only** — they never auto-fix.

Pick the path from the request. Normal coding work takes the BUILD path by default; `/review-diff`, `/audit-repo`, or phrasing like "review for over-engineering," "find bloat," "what can I delete" takes the REVIEW/AUDIT path.

---

## Shared rules (defined once, referenced by units)

Every unit below references these. Do not restate them per unit.

### Writing-the-code judgment order
Once the problem and codebase are understood, apply this judgment roughly in order of preference, without being mechanical — this is instinct, not a checklist to narrate:

1. **Does this need new code at all?** If the feature is unnecessary for the actual request (speculative options, "for later" flexibility, configurability nobody asked for), don't write it. Solve what was asked, not what might be asked someday.
2. **Does it already exist in this codebase?** Reuse or extend rather than reimplement.
3. **Does the standard library or language/framework's native features cover it?** Prefer these over custom code or new abstractions.
4. **Is there already an installed dependency that does this?** Use it before adding a new one or writing custom logic. (When you do add a Python dependency, add it with `uv` — see Python tooling below.)
5. **Can it be written simply and directly?** Prefer the direct, obvious implementation over a clever or heavily abstracted one — build abstractions when a second or third real use case shows up, not preemptively.

Match whatever's idiomatic for the language, framework, and existing codebase conventions when deciding between stdlib/native/dependency — there's no blanket preference for avoiding new dependencies if one is already the idiomatic choice.

### Non-negotiables — never cut these for brevity
Never sacrificed to save lines or tokens, no matter how "minimal" the rest of the solution is:

- **Input validation and trust-boundary checks** — anything crossing a trust boundary (user input, external API responses, file contents) gets validated.
- **Error handling** — failure paths are handled explicitly, not silently swallowed or left to crash uninformatively.
- **Data-loss safety** — anything that could destroy user data (overwrites, deletes, migrations) gets appropriate safeguards (confirmations, backups, transactions) even if that costs a few extra lines.
- **Security** — auth checks, sanitization, secrets handling are never trimmed.
- **Accessibility** — for user-facing UI code, accessibility basics (semantic HTML, labels, keyboard support) are not optional scope-cuts.

If minimizing code would require compromising any of the above, don't compromise — write the correct version and note briefly why it's not smaller.

### Comments and docstrings
Follow the existing project's convention. If the codebase/language/team convention calls for docstrings or explanatory comments (e.g. public APIs, complex algorithms), write them properly — don't strip documentation to save lines. Where no such convention applies, keep comments minimal and only where the code isn't self-explanatory; don't narrate what the code obviously already says.

### Tests
Follow the project's existing testing convention. If the codebase has tests, write tests for new behavior at the same level of coverage the project expects — **tests are not a line-count target to cut.** Minimal production code does not mean skipping the tests that prove it works. Don't over-test either: cover the real behavior and edge cases that matter, not every trivial getter. If the project has no test setup and the task doesn't warrant introducing one, say so rather than silently shipping untested logic for anything non-trivial.

### Python tooling: use `uv`
For Python work, **`uv` is the default** package/environment manager over `pip`/`venv`/`pipenv`/`poetry` — unless the project already uses another tool, in which case stay consistent with it. Adding a dependency is still governed by the judgment order above (stdlib first). Command reference, per-command usage, and migration rules all live in **`references/python-uv.md`** — read it when doing Python dependency/environment work rather than relying on this summary.

### Deferred-shortcut markers
When a shortcut is deliberately taken (something deferred rather than solved — e.g. a hardcoded value that should eventually be configurable, an edge case knowingly left unhandled because it's out of scope), mark it in code with a comment in the language's native syntax:

```
// lazy: <what was deferred and why>
```

These are grep-able later (`grep -rn "lazy:"`) so deferred debt doesn't silently rot into "later means never." Don't overuse this — it's for genuine, deliberate deferrals, not a catch-all disclaimer on every function.

### What this discipline does not do
- It does not sacrifice correctness, safety, or the non-negotiables to hit a smaller line count.
- It does not silently choose between a minimal and a more robust implementation when the choice is genuinely debatable — it hands back and asks (see the STOP GATE in Unit B2).
- It does not treat "fewer lines" as inherently better when the terse version is harder to understand or maintain than a slightly longer, clearer one — the target is the smallest *correct and clear* solution, not the smallest possible.

---

## BUILD path

### Unit B1 — Read before writing (scoped exploration)
- **Goal/scope**: understand the target code and surrounding conventions well enough to avoid duplicating what exists and to match local idiom. Never write code into unfamiliar territory — skipping this is the single biggest cause of duplicated, bloated code, and it is not optional.
- **Inputs**: the task; the target file(s) or feature scope.
- **Do**:
  - Read the file(s) being touched and their direct imports/callers; skim the immediate module/package for conventions, helpers, and utilities that already exist.
  - Check for existing functions/components/utilities that already do (or nearly do) what's needed — reuse or extend them instead of a parallel implementation. For new files, check whether similar functionality lives elsewhere in the repo first.
  - Do **one scoped search** (`grep`/glob for the function or concept name) for existing equivalents.
  - **Where to stop.** Reading is scoped, not exhaustive — don't read the whole repo (it costs more tokens than it saves). Stop once you have enough to avoid duplication and match conventions. If a scoped search turns up nothing, proceed — don't keep widening indefinitely.
  - **Delegate when it's more than a couple of files.** For anything beyond a trivial single-file edit, spawn an `explore` subagent (Task tool) to do this pass instead of reading everything into the main thread — this keeps the main context lean and lets the search run thoroughly. Brief it precisely and ask it to report back only: the conventions/helpers/utilities in the target module; any existing function/component/dependency that already does (or nearly does) the job, with `file:line`; the idiomatic patterns to match. Specify thoroughness ("quick" for a small module, "medium"/"very thorough" for a large/unfamiliar codebase). Launch multiple `explore` subagents in parallel for independent areas. When the change genuinely touches one already-open file, just read it directly — a subagent would be overhead. If subagents aren't available, do the scoped read inline rather than blocking.
- **Self-verify**: confirm the target file(s) were actually read, and that a scoped search for existing equivalents was run (or a subagent reported back) — you can name the conventions/helpers found and whether an equivalent already exists.
- **Report contract**: `read: <files/scope> | existing equivalent: <found @ file:line | none> | conventions noted: <brief>`.

### Unit B2 — Decide the approach
- **Goal/scope**: choose the smallest correct approach before writing, and surface any genuine minimal-vs-robust tradeoff for a human decision.
- **Inputs**: B1's findings (existing code, conventions, equivalents).
- **Do**: apply the shared **Writing-the-code judgment order** to settle on the approach. Check it against the shared **Non-negotiables** — if minimizing would compromise any, plan the correct (possibly larger) version and note why.
- **Self-verify**: the chosen approach reuses what exists where possible, needs no code that wasn't asked for, and does not trip a non-negotiable.
- **STOP GATE (hand back) — genuine tradeoffs only**: when there's a real tradeoff between the minimal version and a slightly more robust/extensible one (not a non-negotiable — a real judgment call), **stop and ask** rather than silently picking. State the two options briefly: what the minimal version does and doesn't handle, and what the more robust version would add; let the user decide. → Hand control back for the approach decision. **Do not raise this gate for trivial cases** — only when the extra robustness is a real, defensible option someone might reasonably want; otherwise proceed straight to B3.
- **Report contract**: `approach: <one line> | reuse: <what> | tradeoff gate: <none | awaiting: minimal vs robust decision>`.

### Unit B3 — Write the code
- **Goal/scope**: implement the chosen approach as the smallest *correct and clear* solution.
- **Inputs**: the approach from B2 (including any tradeoff decision handed back).
- **Do**:
  - Write the direct, obvious implementation. Honor the shared **Comments and docstrings** and **Tests** conventions.
  - Do not swallow the **Non-negotiables** — validation, error handling, data-loss safety, security, accessibility stay in even when they cost lines.
  - Mark any deliberate deferral with a **`lazy:`** comment per the shared rule.
- **Self-verify (verify it yourself before reporting)**: run whatever the project supports — the relevant tests, build, and/or lint if they exist — and inspect your own diff. If the project has no such tooling, verify by inspection against the task's requirements. Never claim it works without having actually checked. If verification fails, fix it if the fix is obvious and in scope; otherwise report the specific failure.
- **Report contract**: `wrote/edited: <files> | verified: <tests/build/lint result, or "inspection — no tooling"> | non-negotiables intact: yes | lazy: markers: <n or none> | pass/fail`.

### Unit B4 — Report impact
- **Goal/scope**: make the savings from this discipline visible after non-trivial work.
- **Inputs**: the completed, verified change from B3.
- **Do**: briefly report the size of what was written using a **real measurement** — `git diff --stat` (or `wc -l` on new files), e.g. "Added ~18 lines across 2 files (per `git diff --stat`)." Token counts can't be measured reliably — if mentioned, label them explicitly as a rough estimate, never as a measured figure. **Skip this entirely for trivial one-line fixes** where it would just be noise.
- **Self-verify**: the reported figure came from an actual `git diff --stat`/`wc -l`, not a guess.
- **Report contract**: `impact: <measured line count from tool> (or "skipped — trivial fix")`.

---

## REVIEW/AUDIT path

Both units delegate the read-heavy pass to subagents and **return findings only — never auto-fix.** Detailed steps live in **`references/workflows.md`**; the audit's what-to-look-for / what-NOT-to-flag rules live in **`references/audit-checklist.md`**. Load those files when the corresponding unit is invoked. Subagent note: prefer a `general` subagent for ranked findings with rationale, `explore` for pure "find the bloat" passes; if neither is available, do the pass inline but keep it scoped.

### Unit A1 — `/review-diff` (review a diff for over-engineering)
- **Goal/scope**: flag over-engineering in a specific diff — reinvented stdlib, unnecessary deps, speculative abstractions/config, dead "just in case" flexibility, needless verbosity. **Report only; do not edit.**
- **Inputs**: the diff/baseline. Triggers: "review for over-engineering," "what can we delete," "is this over-engineered," "simplify review."
- **Do**:
  - Establish the baseline: prefer `git diff` (unstaged) / `git diff --staged`, or `git diff <base>` against the branch point. If not a git repo or git shows nothing relevant, fall back to the files changed this session.
  - Delegate the review to a `general` subagent (Task tool) for a fresh-eyes pass that doesn't inherit the author's assumptions. Hand it the exact diff/baseline; instruct it to review **only** for over-engineering, not correctness or style, and to report findings only (no edits) — one line per finding with `file:line`, what to cut, and what replaces it.
  - Relay findings as a short, scannable list.
- **Self-verify**: confirm which baseline was reviewed (so findings are unambiguous) and that every finding cites `file:line` + what-to-cut + replacement. Confirm no code was rewritten unprompted.
- **STOP GATE (hand back)**: present the findings list and **stop** — don't rewrite code unprompted. Changes are made only when the user asks for specific items. → Hand control back for the user's cut decisions.
- **Report contract**: `baseline: <what was diffed> | findings: N (each with file:line) | edits made: none | awaiting: which items to apply`.

### Unit A2 — `/audit-repo` (audit the whole repo for bloat)
- **Goal/scope**: produce a ranked, repo-wide list of what to delete, simplify, or replace with stdlib/native equivalents. **Report only; do not auto-fix.**
- **Inputs**: the repo. Triggers: "audit this codebase," "audit for over-engineering," "what can I delete," "find bloat."
- **Do**:
  - Delegate the scan to subagents (Task tool) rather than reading the repo into the main thread; brief each with `references/audit-checklist.md`. Keep it token-efficient: **exclude vendored/generated dirs** (`node_modules`, `vendor`, `dist`, `build`, `.venv`, lockfiles, minified files) and **prioritize** the largest, most-depended-on source files — don't read every file. For a large repo, split by area (one subagent per top-level package) and launch them in parallel in a single message.
  - Consolidate findings into one ranked list (biggest wins first), each with a one-line rationale and rough impact.
- **Self-verify**: confirm vendored/generated dirs were excluded, findings are ranked biggest-win-first, and each carries a rationale + rough impact. Confirm nothing was changed.
- **STOP GATE (hand back)**: present the ranked list and **stop** — this is a report, not an auto-fix. Apply changes only when the user asks for specific items. → Hand control back for the user's prioritization.
- **Report contract**: `audited: <scope/areas> | ranked findings: N (biggest-win first, each w/ rationale + impact) | edits made: none | awaiting: which items to apply`.
