---
name: project-planner
description: Use when the user asks to plan, spec, or document a new project or feature before coding — e.g. "help me plan out...", "create a project plan", "/plan-project", "spec this out" — or to update existing planning docs (spec, design, roadmap, backlog) under docs/ in the repo root. Runs a phased interview→spec→design→roadmap→backlog flow with an explicit hand-back to the user for approval between each doc. Do NOT use to write/refactor code (lean-coder), design UI/UX screens (ui-ux-designer), or write README/publish docs for an existing repo (repo-docs-publisher).
metadata:
  category: planning
  audience: developers
  outputs: docs/01-spec.md,docs/02-design.md,docs/03-roadmap.md,docs/04-backlog.md
---
# Project Planner

Turns a vague idea into four rigorous planning documents under `docs/` at the repo root, through a structured interview and staged approval process. Never skip straight to writing docs from a one-line idea — the interview is the point of this skill.

The workflow below is expressed as discrete **units**. Each unit is self-contained (Goal/scope, Inputs, Do, Self-verify, Report contract). Every point where the process must pause for the user to answer questions or approve a doc is an explicitly labeled **STOP GATE (hand back)** — control returns to the user/orchestrator and this skill does not proceed until it comes back. Shared reference material (output files, templates, non-interactive fallback, delegation rules) is defined once in "Shared reference" and pointed to by units — it is not restated per unit.

---

## Shared reference (defined once, referenced by every unit)

### Output files

Always created under `docs/` at the repo root, in this order:

1. `docs/01-spec.md` — requirements, scope, success metrics, risks/assumptions/open questions
2. `docs/02-design.md` — architecture, tech stack, diagrams
3. `docs/03-roadmap.md` — sprint-by-sprint plan with estimates
4. `docs/04-backlog.md` — atomic, checkbox-style, agent-executable tasks

Always create `docs/` at the **repo root**, not nested inside a subpackage, unless the user is clearly working in a monorepo and specifies a package. If `docs/` or any of these files already exist, this is an **update**, not a fresh run — see "Update path."

### Templates

Each doc-writing unit uses a template from `references/`:

| Doc | Template |
|---|---|
| `docs/01-spec.md` | `references/spec-template.md` |
| `docs/02-design.md` | `references/design-template.md` |
| `docs/03-roadmap.md` | `references/roadmap-template.md` |
| `docs/04-backlog.md` | `references/backlog-template.md` |

**The templates use `<placeholder>` and `<…>` markers as fill-in guides — replace every one with real content; never leave a raw `<placeholder>` in a finished doc.**

### Delegation rules (what stays here vs. what goes to a subagent)

- The **interview, approval gates, and doc writing all stay in this primary session** — do **not** delegate those to subagents.
- Subagents are used **only for read-heavy inspection work**: the Phase 0 codebase read (Unit 0) and the Phase 6 cross-doc consistency check (Unit 6). A subagent verifies; this session edits. If subagents aren't available, do the read/check inline instead of blocking.

### Non-interactive fallback (applies to every STOP GATE)

The per-doc STOP GATEs assume an interactive user. If you are running non-interactively (batch/automated run with no one to answer or approve), do **not** block indefinitely: write all four docs in one pass, record every assumption you made in the spec's "Risks, Assumptions & Open Questions" table, clearly state at the top of your summary that they were generated without approval gates, and invite the user to review and request changes to any doc. Keep the gates whenever a user *is* present. Each unit's STOP GATE inherits this fallback — it is not restated per unit.

---

## Workflow units

Follow the units in order. Do not skip the interview even if the user's idea sounds detailed — there are always gaps worth surfacing. Do not write a doc and move to the next without the user's explicit approval (subject to the non-interactive fallback).

### Unit 0 — Detect context

- **Goal/scope**: determine greenfield vs. existing codebase, and fresh-run vs. update, before any interview.
- **Inputs**: the repo working tree; the user's request.
- **Do**: look for existing source directories, package manifests (`package.json`, `pyproject.toml`, `go.mod`, etc.), and any existing `docs/` folder. If an existing codebase is found, **delegate the read to an `explore` subagent** (per Shared reference → Delegation rules) and ask it to report back: the project's structure, language/framework/stack, key conventions and existing patterns, and whether `docs/01-spec.md` (or siblings) already exist. Use that briefing to inform the interview and avoid asking questions you can answer from inspection. If `docs/01-spec.md` etc. already exist, switch to the **Update path** instead of continuing.
- **Self-verify**: confirm you know (a) greenfield or existing codebase, and (b) whether planning docs already exist — and therefore which path (fresh run vs. Update path) applies.
- **STOP GATE (hand back)**: if an existing codebase was inspected, present what was found and **confirm your read of it** with the user rather than asking them to restate it. → Hand control back for confirmation before the interview. (Non-interactive fallback applies.)
- **Report contract**: `context: <greenfield | existing (stack)> | existing docs: <yes → update path | no> | awaiting: read confirmation`.

### Unit 1 — Interview

- **Goal/scope**: gather enough to write a solid spec without major guesswork.
- **Inputs**: the user's idea/brief; the Unit 0 briefing (skip anything already known from inspection or already told).
- **Do**: interview the user in **batches of 5**, using the `question` tool (or plain numbered questions if that tool isn't available). Keep going in batches until you have enough — thin ideas need more batches, detailed briefs need fewer. Cover, across the batches:
  - **Problem & users**: what problem this solves, who it's for, why now
  - **Scope**: core features (must-have) vs nice-to-have vs explicitly out of scope
  - **Non-functional requirements**: expected scale, performance targets, security/compliance needs, availability needs
  - **Constraints**: team size, timeline/deadline, budget
  - **Tech stack preference**: ask if the user has a preference; if not, tell them you'll recommend one during the design phase
  - **Existing systems**: integrations, existing codebase conventions, data sources
  - **Success criteria**: how they'll know this worked, measurable if possible
- **Self-verify**: confirm every topic above is either answered, known from inspection, or captured as an explicit open question — and that there is enough to write a spec.
- **STOP GATE (hand back)**: the interview *is* a hand-back — each batch returns control to the user to answer. Do not proceed to Unit 2 until the user has answered enough to write a spec without major guesswork; where genuine gaps remain, note them as open questions rather than blocking forever. → Hand control back for answers each batch. (Non-interactive fallback: proceed with best-reasoned assumptions, each recorded in the spec's Risks/Assumptions/Open Questions table.)
- **Report contract**: `interview: <N> batches | topics covered: <list> | open questions: <list or none> | awaiting: answers / enough-to-proceed`.

### Unit 2 — Write `docs/01-spec.md`

- **Goal/scope**: produce the spec, then get approval before designing.
- **Inputs**: interview answers + Unit 0 briefing; `references/spec-template.md`.
- **Do**: write `docs/01-spec.md` from the template, replacing every placeholder. Always include:
  - Problem statement & goals
  - In-scope / out-of-scope
  - Functional requirements (informal feature list by default; convert to user-story + acceptance-criteria format only if the user explicitly asked for Agile-style docs in the interview)
  - Non-functional requirements & measurable success metrics (always required, never skip this section)
  - Constraints (team, timeline, budget)
  - Risks, assumptions, and open questions (always required)
- **Self-verify**: confirm `docs/01-spec.md` exists at the repo-root `docs/` path, contains all six required sections above, and has no raw `<placeholder>` markers remaining.
- **STOP GATE (hand back)**: present the drafted file content and ask the user to confirm or request changes. **Do not start `02-design.md` until they approve.** → Hand control back for spec approval. (Non-interactive fallback applies.)
- **Report contract**: `wrote: docs/01-spec.md | sections: all 6 present | placeholders: none | awaiting: spec approval`.

### Unit 3 — Write `docs/02-design.md`

- **Goal/scope**: produce the design, then get approval before roadmapping.
- **Inputs**: approved `docs/01-spec.md`; stated stack preference (if any); `references/design-template.md`.
- **Do**: write `docs/02-design.md` from the template. Always:
  - Propose **2–3 architecture/stack options** with tradeoffs (cost, complexity, scalability, team fit) if the user didn't already state a hard stack preference in the interview. If they did state a preference, design around it but still note any tradeoffs worth flagging.
  - Include Mermaid diagrams (architecture/component diagram at minimum; add sequence or data-flow diagrams if the system has non-trivial interactions).
  - Record the chosen option and why, once the user picks or confirms one.
- **Self-verify**: confirm `docs/02-design.md` exists at the expected path, includes the options/tradeoffs (or the design-around-preference note) and at least an architecture Mermaid diagram, and has no raw placeholders.
- **STOP GATE (hand back)**: present the draft and get explicit approval — including the chosen option — before Unit 4. → Hand control back for design approval. (Non-interactive fallback applies.)
- **Report contract**: `wrote: docs/02-design.md | options: <N or design-to-preference> | diagrams: <list> | awaiting: design approval + option pick`.

### Unit 4 — Write `docs/03-roadmap.md`

- **Goal/scope**: produce a full sprint-by-sprint plan, then get approval before the backlog.
- **Inputs**: approved `docs/01-spec.md` (esp. its Constraints section) and `docs/02-design.md`; `references/roadmap-template.md`.
- **Do**: write `docs/03-roadmap.md` from the template.
  - **Carry the team size, timeline, and budget from `docs/01-spec.md` (Constraints section) forward verbatim** into the roadmap's Planning Assumptions — do not re-derive or invent different numbers. If the spec says "solo dev, 4–6 weeks," the roadmap must plan against 4–6 weeks, not a fresh guess.
  - Break the work into sprints/phases (use the team size + timeline from the spec to size sprints realistically — don't invent velocity numbers from nothing; state the assumption you're using, e.g. "assuming 1-week sprints, team of 2").
  - Each sprint: goal, scope, deliverables, rough estimate (days or story points — pick one and be consistent), dependencies on prior sprints.
  - Flag any sprint whose estimate is highly uncertain.
- **Self-verify**: confirm `docs/03-roadmap.md` exists at the expected path, its Planning Assumptions match the spec's Constraints verbatim, every sprint has goal/scope/deliverables/estimate/dependencies, and no raw placeholders remain.
- **STOP GATE (hand back)**: present the draft and get approval before Unit 5. → Hand control back for roadmap approval. (Non-interactive fallback applies.)
- **Report contract**: `wrote: docs/03-roadmap.md | constraints carried verbatim: yes | sprints: <N> | awaiting: roadmap approval`.

### Unit 5 — Write `docs/04-backlog.md`

- **Goal/scope**: produce the atomic, agent-executable task backlog.
- **Inputs**: approved `docs/03-roadmap.md` and `docs/02-design.md`; `references/backlog-template.md`.
- **Do**: write `docs/04-backlog.md` from the template. This is the file an AI coding agent (e.g. Claude Code) will work through directly, so:
  - Tasks must be **atomic**: one task = one coherent unit of work a coding agent could pick up and finish without needing to ask clarifying questions.
  - Every task is a markdown checkbox: `- [ ] Task description`.
  - Group tasks under their sprint/phase from the roadmap, in dependency order.
  - Each task should be concrete enough to reference specific files, modules, or components where the design doc makes that clear.
- **Self-verify**: confirm `docs/04-backlog.md` exists at the expected path, every task is a checkbox grouped under its roadmap sprint in dependency order, and no raw placeholders remain.
- **Note — no approval STOP GATE here**: the Unit 4 roadmap approval already signed off on scope, so this unit does **not** pause for approval. Summarize what was generated and invite edits instead.
- **Report contract**: `wrote: docs/04-backlog.md | tasks: <N> atomic checkboxes grouped by sprint | no gate (scope pre-approved in Unit 4)`.

### Unit 6 — Consistency check & wrap-up

- **Goal/scope**: verify the four docs are mutually consistent, fix any mismatch, and summarize.
- **Inputs**: the four completed `docs/*.md` files.
- **Do**: run a **cross-doc consistency check**. **Delegate this to a `general` subagent** (per Shared reference → Delegation rules): hand it the four file paths and the checklist below, and ask it to report every mismatch with `file:line` references. A fresh reader catches mismatches the author glossed over. Then **fix any mismatch yourself** in this session (don't just report it) — the subagent verifies, you edit.
  - **Constraints match:** team size, timeline, and budget in `03-roadmap.md` Planning Assumptions match `01-spec.md` Constraints verbatim.
  - **Scope match:** every must-have feature in `01-spec.md` scope appears somewhere in the roadmap sprints and backlog tasks; nothing out-of-scope leaked into the backlog.
  - **Design → roadmap/backlog:** the chosen stack and components in `02-design.md` are the ones referenced by the roadmap deliverables and backlog tasks.
  - **Naming:** the project name and any key module/file names are consistent across all four docs.
- **Self-verify**: confirm every mismatch the check surfaced was fixed in-session (re-check the specific `file:line` references), leaving the four docs mutually consistent.
- **Do (wrap-up)**: summarize the four files created and their locations, and remind the user this is a living doc set — they can ask to update any of them as the project evolves (see Update path).
- **Report contract**: `consistency check: <N mismatches found, all fixed | clean> | summarized 4 docs + living-set note`.

---

## Update path

If `docs/01-spec.md` (or siblings) already exist and the user wants changes (detected in Unit 0), this is an **update**, not a fresh run:

- **Goal/scope**: change only the affected doc(s) without clobbering existing work.
- **Do**:
  1. Read the existing file(s) first — never overwrite blind.
  2. Ask what's changing (new requirement, scope cut, architecture pivot, re-plan, etc.) using the same batched-question style if it's non-trivial. → This is a **STOP GATE (hand back)** for the change scope. (Non-interactive fallback applies.)
  3. Edit only the affected file(s). If a change in an earlier doc invalidates a later one (e.g. a spec change breaks the roadmap), **STOP GATE (hand back)**: flag this and ask whether they want you to cascade the update through `02-design.md` → `03-roadmap.md` → `04-backlog.md`.
  4. For `04-backlog.md` specifically, preserve existing checkbox state (don't uncheck completed tasks) — only add, remove, or edit task text.
- **Self-verify**: confirm only the intended file(s) changed, backlog checkbox state is preserved, and any cascade the user approved was applied consistently (re-run the Unit 6 checklist over the touched docs).
- **Report contract**: `updated: <files> | cascade: <none | applied through …> | backlog checkbox state preserved: yes | awaiting: <change scope / cascade decision>`.

---

## Notes

- If the user explicitly says "skip the interview, just write it," you can compress Unit 1 into a single batch of clarifying questions (or skip entirely for a fully-specified request), but still keep the per-doc STOP GATEs (approval gates) unless they also waive those.

## Related skills & doc ownership

This skill is the **owner** of `docs/01-spec.md` and `docs/02-design.md`. It fits into a pipeline:

- **`ui-ux-designer`** runs after the design phase to produce `docs/ux-design.md`. It may *propose* edits back into `01-spec.md`/`02-design.md`, but must summarize and get confirmation before writing — it never silently overwrites these planner-owned docs. If UX work is expected, mention this skill hands off to `ui-ux-designer` for any user-facing interface.
- **`lean-coder`** implements the `04-backlog.md` tasks once planning is approved.
- **`repo-docs-publisher`** is for publishing an *existing* repo's docs (README etc.), not project planning — don't invoke it here.
