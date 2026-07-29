# lean-coder

A "lazy senior developer" discipline for writing the least code that correctly and safely solves the problem. Reads before writing, reuses what already exists, never over-engineers — and never trades correctness or safety for a smaller line count. Applies to coding work broadly, and adds two explicit workflows for finding over-engineering in a diff or a whole repo.

---

## Trigger phrases

| Input | Example |
|---|---|
| Broad coding work | "write a function", "edit this", "refactor", "fix this bug", "add a feature", "clean up" |
| Review a diff | `/review-diff` — "review for over-engineering", "what can we delete", "is this over-engineered" |
| Audit a repo | `/audit-repo` — "audit this codebase", "find bloat", "what can I delete" |

This skill loads **on demand for coding work broadly** — not only when explicitly invoked. Because skills load by matching the task, it is pulled in for any coding request; once loaded, the discipline applies throughout the task. Only the two review/audit workflows above need direct invocation.

Do **not** use it for planning or spec docs (use `project-planner`), UI/UX design (use `ui-ux-designer`), or publishing repo docs (use `repo-docs-publisher`).

---

## What it does

Applies a "lazy senior developer" discipline to every coding task: the smallest *correct and clear* solution, reusing what exists, never over-engineering.

- **Read before writing.** Never writes into unfamiliar territory. Reads the target file(s), their direct imports/callers, and the immediate module for conventions and existing helpers, plus one scoped search for existing equivalents. Reading is **scoped, not exhaustive** — it stops once there's enough to avoid duplication and match local conventions. For anything beyond a trivial single-file edit, it delegates this read-before-writing pass to an `explore` subagent to keep the main context lean, falling back to inline scoped reads if subagents aren't available.
- **Writing-the-code judgment order.** Roughly in order of preference, not as a rigid checklist: (1) does this need new code at all — solve what was asked, not what might be asked someday; (2) does it already exist in this codebase — reuse or extend; (3) does the standard library or language/framework native feature cover it; (4) is there an already-installed dependency for it; (5) can it be written simply and directly rather than cleverly abstracted.
- **Non-negotiables — never cut for brevity.** Input validation and trust-boundary checks, explicit error handling, data-loss safety (confirmations, backups, transactions), security (auth, sanitization, secrets), and accessibility for user-facing UI are never trimmed to save lines. If minimizing would compromise any of these, it writes the correct version and notes briefly why it isn't smaller.
- **Minimal-vs-robust — pause and ask.** On a genuine tradeoff between a minimal and a more robust/extensible version (not a non-negotiable, a real judgment call), it states both options briefly and lets the user decide rather than silently picking one. It does not ask for trivial cases.
- **Deferred-shortcut markers.** Deliberate deferrals are marked in code with a `lazy: <what and why>` comment (native comment syntax) so they stay grep-able (`grep -rn "lazy:"`) and don't rot into "later means never."
- **Impact reporting.** After a non-trivial task, briefly reports the size of what was written using a real measurement (`git diff --stat`, or `wc -l` for new files), so the savings are visible. Token counts, if mentioned, are labelled as rough estimates.

---

## Additional workflows

Two explicitly-invoked workflows are documented in `references/workflows.md`. Both delegate the read-heavy pass to subagents and **return findings only — they never auto-fix.**

| Workflow | What it does |
|---|---|
| **`/review-diff`** | Confirms the baseline (`git diff`, `git diff --staged`, `git diff <base>`, or the files changed this session), then delegates a fresh-eyes review to a `general` subagent that flags over-engineering only — reinvented stdlib, unnecessary deps, speculative abstractions, dead flexibility, needless verbosity. Relays a short scannable list with `file:line`, what to cut, and what replaces it. |
| **`/audit-repo`** | Delegates a repo-wide scan to subagents (briefed with `references/audit-checklist.md`), excluding vendored/generated dirs and prioritizing the largest, most-depended-on source files. Consolidates a ranked list (biggest wins first) of what to delete, simplify, or replace, each with a one-line rationale and rough impact. |

The audit's what-to-look-for and what-NOT-to-flag rules live in `references/audit-checklist.md`.

---

## Python tooling

For Python work, **`uv` is the default** package/environment manager over `pip`/`venv`/`pipenv`/`poetry` — unless the project is already committed to a different tool, in which case it stays consistent. Adding a dependency is still governed by the stdlib-first judgment above. The full command reference, per-command usage, and migration rules live in `references/python-uv.md`.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Target codebase / files | Yes | The code to write, edit, refactor, or fix; the skill reads it (scoped) before changing it |
| Diff / baseline | For `/review-diff` | The `git diff`, staged diff, `<base>` comparison, or session-changed files to review against |
| Subagents (`explore`, `general`) | Optional | Used to delegate read-heavy exploration and review passes; falls back to inline scoped reads if unavailable |

---

## Outputs

- **Normal coding tasks:** edited or new code, plus a brief impact report for non-trivial work (line count from `git diff --stat` / `wc -l`). Trivial one-line fixes skip the report.
- **Workflows (`/review-diff`, `/audit-repo`):** a ranked findings report, not auto-applied fixes. Changes are only made when the user asks for specific items.

---

## Limitations

- **Never sacrifices correctness, safety, or the non-negotiables** (validation, error handling, data-loss safety, security, accessibility) to hit a smaller line count.
- **Asks rather than silently choosing** when a minimal-vs-robust tradeoff is genuinely debatable.
- **Targets the smallest *correct and clear* solution**, not the smallest possible — a terse version that is harder to understand or maintain than a slightly longer, clearer one is not preferred.
- **Workflows report only.** `/review-diff` and `/audit-repo` return findings and never auto-apply fixes.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r development/lean-coder ~/.config/opencode/skills/

# Per-project only
cp -r development/lean-coder .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse development\lean-coder "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/lean-coder.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the coding task |

---

## Companion skills

- **`project-planner`** — produces the plans and spec docs
- **`ui-ux-designer`** — handles UI/UX design work
- **`repo-docs-publisher`** — publishes repo documentation

`lean-coder` implements the plans those skills produce.
