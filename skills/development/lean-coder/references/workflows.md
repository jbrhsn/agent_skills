# Review & audit workflows

Detailed steps for the two explicitly-invoked workflows in `lean-coder`. Subagent note: prefer a `general` subagent for ranked findings with rationale; use `explore` for pure "find the bloat" passes. If neither is available in the environment, do the pass inline but keep it scoped (don't read the whole repo into context).

## `/review-diff` — review a diff for over-engineering

Triggers: "review for over-engineering," "what can we delete," "is this over-engineered," "simplify review."

1. Get the current diff. Prefer `git diff` (unstaged) / `git diff --staged`, or `git diff <base>` against the branch point. If not a git repo, or git shows nothing relevant, fall back to the specific files changed this session. Confirm which baseline you're reviewing against so findings are unambiguous.
2. Delegate the review to a `general` subagent (Task tool) for a fresh-eyes pass that doesn't inherit the author's assumptions. Hand it the exact diff/baseline and instruct it to review **only** for over-engineering — not correctness or style. Look for: reinvented stdlib, unnecessary new dependencies, speculative abstractions or config with no current use, dead flexibility ("just in case" params/branches never exercised), and code that could be one line instead of many. Report findings only (don't edit), one line per finding with `file:line`, what to cut, and what replaces it.
3. Relay findings as a short, scannable list. Don't rewrite code unprompted — hand back findings and let the user decide.

## `/audit-repo` — audit the whole repo for over-engineering

Triggers: "audit this codebase," "audit for over-engineering," "what can I delete," "find bloat."

1. Delegate the scan to subagents (Task tool) rather than reading the repo into the main thread. Brief each with `references/audit-checklist.md`. Keep it token-efficient: **exclude vendored/generated dirs** (`node_modules`, `vendor`, `dist`, `build`, `.venv`, lockfiles, minified files) and **prioritize** the largest, most-depended-on source files first — don't read every file. For a large repo, split by area (one subagent per top-level package) and launch them in parallel in a single message.
2. Consolidate findings into one ranked list (biggest wins first) of what to delete, simplify, or replace with stdlib/native equivalents, each with a one-line rationale and rough impact.
3. This is a report, not an auto-fix — don't apply changes without the user asking for specific items.
