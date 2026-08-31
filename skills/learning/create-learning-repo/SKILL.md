---
name: create-learning-repo
description: Scaffolds a goal-based learning repository — sections, modules, chapters, and six briefed stub files per chapter (learning, examples, practice, interview, thought_leadership, quizzies) with a tier ladder matched to the domain. Use whenever the user wants to learn a technology, craft, habit, or exam subject, prepare for an interview, build a study plan or roadmap, "structure my learning", turn a syllabus or curriculum into files, or organize notes for a subject — even if they don't say "repo" or "scaffold". Also use when a user pastes an existing learning plan and wants it turned into a folder structure or reviewed for gaps.
---

# Create Learning Repo

Turns a learning goal into a **structure with briefs** — never the learning content itself. Every generated file is a stub whose brief says what belongs in it and how deep to go; the user writes the rest.

## Non-negotiables

1. **Goal-based.** No scaffolding until the user's concrete goal is known (role, interview, project, promotion, deadline). Vague topic lists are not goals.
2. **Approval gate.** Show the plan as text and get an explicit yes before creating any file.
3. **Stubs only.** The brief is instruction — what to cover, why, how deep, in what style. It is never the answer. No explanations, no worked examples, no filled-in questions.
4. **No scheduling.** Do not map chapters to days/weeks unless the user asks directly.

## What a chapter looks like

Six files, the same six in every domain:

| File | Holds |
|---|---|
| `learning.md` | The brief, then one section per tier rung, covering all the chapter's topics |
| `examples.md` | Worked specimens you study and annotate |
| `practice.md` | Tasks you actually do |
| `interview.md` | Questions someone else puts to you |
| `thought_leadership.md` | Public-writing angles |
| `quizzies.md` | Self-assessment, answered from memory |

Topics are **sections inside `learning.md`**, not separate files. That is deliberate: one file per topic produced chapters whose parts never referred to each other. One tiered file per chapter forces a single narrative.

The **profile** (`technical`, `craft`, `practice`, `exam`, `custom`) sets the tier ladder and the labels inside those files — never their names.

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
Read `references/interview.md`. Ask in one or two batched rounds, not a drip. Stop when goal, scope, level, depth, and **profile** are pinned.

### 3. Research — only if the plan has gaps or no plan was given
Read `references/research.md`. Research must return per-chapter depth notes, not just topic names — those notes become the brief. Skip entirely when the user supplied a complete plan and no gaps were agreed.

### 4. Draft the plan
Read `references/plan-schema.md` and `references/profiles.md`. Write `plan.yaml` (or `plan.json`), then present it as a readable tree — sections → modules → chapters — plus the goal statement, the chosen profile and ladder, and any deliberate exclusions. Ask for approval.

Every chapter needs a `purpose` or the scaffolder refuses to run. Chapters missing `depth`, `style`, or `serves` are reported as **thin briefs** — fix them before scaffolding rather than shipping a stub nobody knows how to fill.

### 5. Scaffold
```bash
uv run scripts/scaffold.py plan.yaml --out ./<repo-name>
```

`python3 scripts/scaffold.py plan.json` also works; YAML input then needs PyYAML installed. Add `--dry-run` to print the tree without writing. The script refuses to overwrite existing files unless `--force` is passed.

If Python is unavailable entirely, fall back to `references/bash-fallback.md`.

### 6. Report
Print the tree, counts (sections / modules / chapters / files), the profile and ladder in use, any thin-brief warnings, and where `PLAN.md` and `progress.md` live. Do not summarize the learning content — there isn't any.

## Reference map

| File | Read when |
|---|---|
| `references/interview.md` | Step 2 — question banks by input type, profile detection |
| `references/research.md` | Step 3 — what to search, how to weight sources |
| `references/profiles.md` | Step 4 — choosing the profile, ladders, `tier_count`, `custom` |
| `references/plan-schema.md` | Step 4 — schema, brief fields, cohesion fields, sizing |
| `references/gap-analysis.md` | User supplied a plan — checklist for finding what's missing |
| `references/templates.md` | Editing stub templates or generating files by hand |
| `references/bash-fallback.md` | No Python available |
