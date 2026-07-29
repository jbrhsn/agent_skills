# project-planner

Turns a vague idea into four rigorous planning documents under `docs/` via a structured interview and staged, per-doc approval. It interviews you in batches, then writes the spec, design, roadmap, and backlog one at a time — each gated on your explicit approval — and finishes with a cross-doc consistency check.

---

## Trigger phrases

| Input | Example |
|---|---|
| Plan a project | "help me plan out...", "create a project plan" |
| Slash command | `/plan-project` |
| Spec a feature | "spec this out" |
| Update existing docs | "update the roadmap", "the scope changed — revise the spec" |

Do **not** trigger this skill to write or refactor code (use `lean-coder`), design UI/UX screens (use `ui-ux-designer`), or write a README / publish docs for an existing repo (use `repo-docs-publisher`).

---

## What it does

Runs **seven phases** in order. The interview is mandatory, and each doc is written only after the previous one is approved:

| Phase | What happens |
|---|---|
| **Phase 0 — Detect context** | Determines greenfield vs. existing codebase; looks for source dirs, package manifests, and any `docs/` folder. For an existing codebase, **delegates the read to an `explore` subagent** for a structure/stack/conventions briefing rather than pulling the source into the main thread. If `docs/01-spec.md` (or siblings) exist, jumps to update mode |
| **Phase 1 — Interview** | Interviews the user in **batches of 5 questions** — covering problem/users, scope, non-functional requirements, constraints, stack preference, existing systems, and success criteria. Keeps going until there's enough to write a solid spec; skips anything already known from inspection |
| **Phase 2 — Spec** | Writes `docs/01-spec.md` from the spec template; presents it and waits for explicit approval before continuing |
| **Phase 3 — Design** | Writes `docs/02-design.md` (2–3 architecture/stack options with tradeoffs unless a hard preference was stated, plus Mermaid diagrams); gets approval |
| **Phase 4 — Roadmap** | Writes `docs/03-roadmap.md`, carrying team size/timeline/budget forward verbatim from the spec's Constraints; gets approval |
| **Phase 5 — Backlog** | Writes `docs/04-backlog.md` as atomic, checkbox-style, agent-executable tasks grouped by sprint. No separate gate — roadmap approval already signed off scope — but summarizes and invites edits |
| **Phase 6 — Consistency check + wrap-up** | Delegates a **cross-doc consistency check to a `general` subagent** (constraints, scope, design→roadmap/backlog, naming); the author then **fixes any mismatch itself** in the main session and summarizes the doc set |

**Non-interactive fallback:** if no live user is available to approve (batch/automated run), the skill does not block — it writes all four docs in one pass, flags at the top of the summary that they were generated without approval gates, and invites the user to review and request changes. Approval gates are kept whenever a user is present.

---

## Output files

Always created under `docs/` at the **repo root**, in this order:

| File | Purpose |
|---|---|
| `docs/01-spec.md` | Requirements, scope, non-functional requirements, success metrics, and risks/assumptions/open questions |
| `docs/02-design.md` | Architecture, tech stack, and Mermaid diagrams |
| `docs/03-roadmap.md` | Sprint-by-sprint plan with estimates, dependencies, and milestones |
| `docs/04-backlog.md` | Atomic, checkbox-style, agent-executable tasks grouped by sprint |

The templates use `<placeholder>` and `<…>` markers as fill-in guides — every one must be fully replaced with real content; no raw placeholder should remain in a finished doc.

---

## Updating existing docs

If `docs/01-spec.md` (or siblings) already exist and the user wants changes, the skill switches to update mode:

- Reads the existing file(s) first — never overwrites blind.
- Asks what's changing (new requirement, scope cut, architecture pivot, re-plan), using the same batched-question style if it's non-trivial.
- Edits only the affected file(s).
- Cascades when a change in an earlier doc invalidates a later one — flags this and asks whether to propagate through `02-design.md` → `03-roadmap.md` → `04-backlog.md`.
- For `04-backlog.md`, preserves existing checkbox state (never unchecks completed tasks) — only adds, removes, or edits task text.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| The idea / brief | Yes | The project or feature to plan; drives the interview |
| Interactive user | Optional | Answers interview questions and approves each doc; a non-interactive fallback writes all four docs with recorded assumptions if absent |
| Existing codebase | Optional | If present, an `explore` subagent briefs the interview so the skill avoids asking what it can inspect |
| Existing `docs/` planning files | Optional | If present, triggers update mode instead of a fresh run |

---

## Outputs

The four `docs/*.md` files (spec, design, roadmap, backlog) at the repo root, a wrap-up summary of what was created and where, and a living doc set the user can ask to update as the project evolves.

---

## Limitations

- **The interview is mandatory.** The skill will not skip straight to docs from a one-line idea unless the user explicitly waives the interview.
- **Approval gates assume an interactive user.** With no one to approve, the non-interactive fallback writes all four docs in one pass and flags that gates were skipped.
- **Owns only spec and design.** It is the owner of `docs/01-spec.md` and `docs/02-design.md`; it hands UX work to `ui-ux-designer` and implementation to `lean-coder`.
- **Repo-root only.** The `docs/` folder is created at the repo root, not nested inside a subpackage (unless the user specifies a package in a monorepo).

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r development/project-planner ~/.config/opencode/skills/

# Per-project only
cp -r development/project-planner .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse development\project-planner "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/project-planner.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before describing the project to plan |

---

## Companion skills

- **`ui-ux-designer`** — runs after the design phase to produce `docs/ux-design.md`; may propose edits back into the planner-owned spec/design docs, but summarizes and confirms before writing
- **`lean-coder`** — implements the `docs/04-backlog.md` tasks once planning is approved
- **`repo-docs-publisher`** — for publishing an existing repo's docs (README etc.), not project planning
