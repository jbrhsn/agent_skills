---
name: create-learning-repo
description: Scaffolds a goal-based learning repository — sections, modules, chapters, and one stub .md per topic plus interview.md and thought_leadership.md per chapter. Use whenever the user wants to learn a technology, prepare for an interview, build a study plan or roadmap, "structure my learning", turn a syllabus or curriculum into files, or organize notes for a subject — even if they don't say "repo" or "scaffold". Also use when a user pastes an existing learning plan and wants it turned into a folder structure or reviewed for gaps.
---

# Create Learning Repo

Turns a learning goal into a **structure only**. Never write learning content — every generated file is a stub the user fills in later.

## Non-negotiables

1. **Goal-based.** No scaffolding until the user's concrete goal is known (role, interview, project, promotion, deadline). Vague topic lists are not goals.
2. **Approval gate.** Show the plan as text and get an explicit yes before creating any file.
3. **Stubs only.** No explanations, no answers, no filled-in interview questions.
4. **No scheduling.** Do not map chapters to days/weeks unless the user asks directly.

## Workflow

```
Intake → Interview → Research (conditional) → Draft PLAN → Approve → Scaffold → Report
```

### 1. Intake — classify the input

| Input | Do this |
|---|---|
| Vague ("learn Python for a senior DE interview in 20 days") | Full interview → research → draft plan |
| Partial plan / topic list | Interview on gaps only → research to fill gaps → draft plan |
| Complete plan | **Do not rewrite it.** Analyze for gaps, present findings, ask follow-ups, then scaffold their plan + agreed additions |

### 2. Interview
Read `references/interview.md`. Ask in one or two batched rounds, not a drip. Stop when goal, scope, level, and depth are pinned.

### 3. Research — only if the plan has gaps or no plan was given
Read `references/research.md`. Skip entirely when the user supplied a complete plan and no gaps were agreed.

### 4. Draft the plan
Read `references/plan-schema.md`. Write `plan.yaml` (or `plan.json`), then present it to the user as a readable tree — sections → modules → chapters → topic counts — plus the goal statement and any deliberate exclusions. Ask for approval.

### 5. Scaffold
Preferred:
```bash
python3 scripts/scaffold.py plan.yaml --out ./<repo-name>
```
Add `--dry-run` to print the tree without writing. The script refuses to overwrite existing files unless `--force` is passed.

If Python or PyYAML is unavailable, convert the plan to `plan.json` (the script reads both) or fall back to `references/bash-fallback.md`.

### 6. Report
Print the tree, counts (sections / modules / chapters / files), and tell the user where `PLAN.md` and `progress.md` live. Do not summarize the learning content — there isn't any.

## Reference map

| File | Read when |
|---|---|
| `references/interview.md` | Step 2 — question banks by input type |
| `references/research.md` | Step 3 — what to search, how to weight sources |
| `references/plan-schema.md` | Step 4 — plan.yaml schema, naming rules, sizing heuristics |
| `references/gap-analysis.md` | User supplied a plan — checklist for finding what's missing |
| `references/templates.md` | Editing stub templates or generating files by hand |
| `references/bash-fallback.md` | No Python available |
