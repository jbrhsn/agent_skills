---
name: project-planner
description: Use when the user asks to plan, spec, or document a new project or feature before coding — e.g. "help me plan out...", "create a project plan", "/plan-project", "spec this out" — or to update existing planning docs (spec, design, roadmap, backlog) under docs/ in the repo root. Do NOT use to write/refactor code (lean-coder), design UI/UX screens (ui-ux-designer), or write README/publish docs for an existing repo (repo-docs-publisher).
metadata:
  category: planning
  audience: developers
  outputs: docs/01-spec.md,docs/02-design.md,docs/03-roadmap.md,docs/04-backlog.md
---
# Project Planner

Turns a vague idea into four rigorous planning documents under `docs/` at the repo root, through a structured interview and staged approval process. Never skip straight to writing docs from a one-line idea — the interview is the point of this skill.

## Output files

Always created under `docs/` at the repo root, in this order:

1. `docs/01-spec.md` — requirements, scope, success metrics, risks/assumptions/open questions
2. `docs/02-design.md` — architecture, tech stack, diagrams
3. `docs/03-roadmap.md` — sprint-by-sprint plan with estimates
4. `docs/04-backlog.md` — atomic, checkbox-style, agent-executable tasks

If `docs/` or any of these files already exist, this is an **update**, not a fresh run — see "Updating existing docs" below.

## Workflow

Follow these phases in order. Do not skip the interview even if the user's idea sounds detailed — there are always gaps worth surfacing. Do not write a doc and move to the next without the user's explicit approval.

**Approval gates when no live user is available:** the per-doc approval gates assume an interactive user. If you are running non-interactively (batch/automated run with no one to approve), do not block indefinitely — write all four docs in one pass, clearly state at the top of your summary that they were generated without approval gates, and invite the user to review and request changes to any doc. Keep the gates whenever a user *is* present.

### Phase 0: Detect context

Before anything else, check whether this is a greenfield project or an existing codebase:

- Look for existing source directories, package manifests (`package.json`, `pyproject.toml`, `go.mod`, etc.), and any existing `docs/` folder.
- If an existing codebase is found, **delegate the read to an `explore` subagent** (via the Task tool) rather than reading the codebase into the main thread — you only need a briefing to run the interview, not the full source in your context. Ask the subagent to report back: the project's structure, language/framework/stack, key conventions and existing patterns, and whether `docs/01-spec.md` (or siblings) already exist. Use the subagent's summary to inform the interview and avoid asking questions you can answer from inspection. Mention what was found to the user and confirm your read of it rather than asking them to restate it. (If subagents aren't available, do a scoped read inline instead of blocking.)
- If `docs/01-spec.md` etc. already exist, jump to "Updating existing docs."

The interview, approval gates, and doc writing all stay in this primary session — do **not** delegate those to subagents. Subagents here are only for the read-heavy inspection work (this phase and the Phase 6 consistency check).

### Phase 1: Interview

Interview the user thoroughly before writing anything. Ask questions in **batches of 5**, using the `question` tool (or plain numbered questions in chat if that tool isn't available in this environment). Keep going in batches until you have enough to write a solid spec — thin ideas need more batches, detailed briefs need fewer.

**When the `question` tool is unavailable** (e.g. non-interactive environment, or the user is not present to answer): fall back to plain numbered questions in your reply. If you also cannot get answers at all (batch/automated run), do NOT block — proceed by writing the docs with your best-reasoned assumptions, and record every assumption you made explicitly in the spec's "Risks, Assumptions & Open Questions" table so the user can correct them later.

Cover, across the batches (skip anything the user already told you, or that you determined by inspecting an existing codebase):

- **Problem & users**: what problem this solves, who it's for, why now
- **Scope**: core features (must-have) vs nice-to-have vs explicitly out of scope
- **Non-functional requirements**: expected scale, performance targets, security/compliance needs, availability needs
- **Constraints**: team size, timeline/deadline, budget
- **Tech stack preference**: ask if the user has a preference; if not, tell them you'll recommend one during the design phase
- **Existing systems**: integrations, existing codebase conventions, data sources
- **Success criteria**: how they'll know this worked, measurable if possible

Do not proceed to Phase 2 until the user has answered enough for you to write a spec without major guesswork. Where genuine gaps remain, note them as open questions in the spec rather than blocking forever on them.

### Phase 2: Write `docs/01-spec.md`, get approval

Use `references/spec-template.md` as the structure. **The templates use `<placeholder>` and `<…>` markers as fill-in guides — replace every one with real content; never leave a raw `<placeholder>` in a finished doc.** Always include:

- Problem statement & goals
- In-scope / out-of-scope
- Functional requirements (informal feature list by default; convert to user-story + acceptance-criteria format only if the user explicitly asked for Agile-style docs in the interview)
- Non-functional requirements & measurable success metrics (always required, never skip this section)
- Constraints (team, timeline, budget)
- Risks, assumptions, and open questions (always required)

Present the drafted file content to the user and ask them to confirm or request changes before moving on. Do not start `02-design.md` until they approve.

### Phase 3: Write `docs/02-design.md`, get approval

Use `references/design-template.md`. Always:

- Propose **2–3 architecture/stack options** with tradeoffs (cost, complexity, scalability, team fit) if the user didn't already state a hard stack preference in the interview. If they did state a preference, design around it but still note any tradeoffs worth flagging.
- Include Mermaid diagrams (architecture/component diagram at minimum; add sequence or data-flow diagrams if the system has non-trivial interactions).
- Record the chosen option and why, once the user picks or confirms one.

Present the draft, get explicit approval, before moving to Phase 4.

### Phase 4: Write `docs/03-roadmap.md`, get approval

Use `references/roadmap-template.md`. This is a full sprint-by-sprint plan:

- **Carry the team size, timeline, and budget from `docs/01-spec.md` (Constraints section) forward verbatim** into the roadmap's Planning Assumptions — do not re-derive or invent different numbers. If the spec says "solo dev, 4–6 weeks," the roadmap must plan against 4–6 weeks, not a fresh guess.
- Break the work into sprints/phases (use the team size + timeline from the spec to size sprints realistically — don't invent velocity numbers from nothing; state the assumption you're using, e.g. "assuming 1-week sprints, team of 2").
- Each sprint: goal, scope, deliverables, rough estimate (days or story points — pick one and be consistent), dependencies on prior sprints.
- Flag any sprint whose estimate is highly uncertain.

Present, get approval, before moving to Phase 5.

### Phase 5: Write `docs/04-backlog.md`

Use `references/backlog-template.md`. This is the file an AI coding agent (e.g. Claude Code) will work through directly, so:

- Tasks must be **atomic**: one task = one coherent unit of work a coding agent could pick up and finish without needing to ask clarifying questions.
- Every task is a markdown checkbox: `- [ ] Task description`.
- Group tasks under their sprint/phase from the roadmap, in dependency order.
- Each task should be concrete enough to reference specific files, modules, or components where the design doc makes that clear.
- Don't ask for approval before writing this one — the roadmap approval in Phase 4 already signed off on scope — but do summarize what was generated and invite edits.

### Phase 6: Wrap up

Before summarizing, run a **cross-doc consistency check** across all four files. Delegate this to a `general` subagent (via the Task tool): a fresh reader catches mismatches the author glossed over, and it keeps the four full docs out of your main context. Hand it the four file paths and the checklist below, and ask it to report every mismatch it finds with `file:line` references. Then **fix any mismatch yourself** in the main session (don't just report it) — the subagent verifies, you edit. (If subagents aren't available, run the checklist yourself against the four files.)

- **Constraints match:** team size, timeline, and budget in `03-roadmap.md` Planning Assumptions match `01-spec.md` Constraints verbatim.
- **Scope match:** every must-have feature in `01-spec.md` scope appears somewhere in the roadmap sprints and backlog tasks; nothing out-of-scope leaked into the backlog.
- **Design → roadmap/backlog:** the chosen stack and components in `02-design.md` are the ones referenced by the roadmap deliverables and backlog task files.
- **Naming:** the project name and any key module/file names are consistent across all four docs.

Then summarize the four files created, their locations, and remind the user this is a living doc set — they can ask you to update any of them as the project evolves (see below).

## Updating existing docs

If `docs/01-spec.md` (or siblings) already exist and the user wants changes:

1. Read the existing file(s) first — never overwrite blind.
2. Ask what's changing (new requirement, scope cut, architecture pivot, re-plan, etc.) using the same batched-question style if it's non-trivial.
3. Edit only the affected file(s). If a change in an earlier doc invalidates a later one (e.g. a spec change breaks the roadmap), flag this to the user and ask whether they want you to cascade the update through `02-design.md` → `03-roadmap.md` → `04-backlog.md`.
4. For `04-backlog.md` specifically, preserve existing checkbox state (don't uncheck completed tasks) — only add, remove, or edit task text.

## Notes

- Always create the `docs/` folder at the **repo root**, not nested inside a subpackage, unless the user is clearly working in a monorepo and specifies a package.
- If the user explicitly says "skip the interview, just write it," you can compress Phase 1 into a single batch of clarifying questions (or skip entirely for a fully-specified request), but still keep the per-doc approval gates unless they also waive those.

## Related skills & doc ownership

This skill is the **owner** of `docs/01-spec.md` and `docs/02-design.md`. It fits into a pipeline:

- **`ui-ux-designer`** runs after the design phase to produce `docs/ux-design.md`. It may *propose* edits back into `01-spec.md`/`02-design.md`, but must summarize and get confirmation before writing — it never silently overwrites these planner-owned docs. If UX work is expected, mention this skill hands off to `ui-ux-designer` for any user-facing interface.
- **`lean-coder`** implements the `04-backlog.md` tasks once planning is approved.
- **`repo-docs-publisher`** is for publishing an *existing* repo's docs (README etc.), not project planning — don't invoke it here.
