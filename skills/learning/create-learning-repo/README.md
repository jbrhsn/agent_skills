# Create-Learning-Repo Skill

## Skill Overview

The create-learning-repo skill transforms a learning goal into a folder structure of **briefed stubs** — never the learning content itself. Each generated file opens with a brief saying what belongs in it and how deep to go; writing the rest is the user's work. Use this skill whenever someone asks to structure a learning repository, prepare for an interview or exam, build a study plan, turn a syllabus into files, or organize notes for a subject. It differs from author-chapter: this skill scaffolds the **structure and the assignment**; author-chapter fills in **one chapter's content**.

## When to Use

Trigger this skill when the user:
- Wants to **organize** learning material into a repo structure (not write it)
- Needs to **prepare for an interview, exam, or certification** and wants a study plan
- Has a **syllabus or curriculum** they want turned into files and folders
- Says "structure my learning", "build a learning roadmap", "create a study plan"
- Provides an **existing plan** they want scaffolded

Do **not** use this skill to:
- **Write one chapter** — use author-chapter instead
- **Edit existing content** — use lean-coder instead

## Key Non-Negotiables

1. **Goal-based.** Never scaffold until you know the concrete goal (role, interview, project, deadline). Vague topic lists are not goals.
2. **Approval gate.** Show the plan as readable text and get an explicit yes before creating any files.
3. **Stubs only.** The brief is instruction — what to cover, why, how deep, in what style. It is never the answer.
4. **No scheduling.** Do not map chapters to weeks unless the user asks directly.

## What a chapter contains

Six files, identical across every domain:

| File | Holds |
|---|---|
| `learning.md` | The brief, then one section per tier rung, covering all the chapter's topics |
| `examples.md` | Worked specimens you study and annotate |
| `practice.md` | Tasks you actually do |
| `interview.md` | Questions someone else puts to you |
| `thought_leadership.md` | Public-writing angles |
| `quizzies.md` | Self-assessment, answered from memory |

Topics are sections **inside** `learning.md`, not separate files — one file per topic produced chapters whose parts never referred to each other.

## Profiles

A profile sets the tier ladder and the labels inside those six files, never their names:

| Profile | Fits | Ladder |
|---|---|---|
| `technical` | Programming, data, infra, ML | Junior → Senior → Architect → Expert |
| `craft` | Writing, blogging, design, speaking | Beginner → Practitioner → Voice → Authority |
| `practice` | Productivity, habits, fitness, money | Aware → Consistent → Adaptive → Designer |
| `exam` | Certifications, licensing, academic exams | Recall → Applied → Scenario → Edge |
| `custom` | Anything else — the plan declares its own rungs | |

`tier_count` (2–4) trims the ladder for short horizons.

## Cohesion

What stops a repo becoming disconnected files. All six files of a chapter carry the same frontmatter: `serves` (which part of the goal this delivers), `builds_on` / `enables` (the dependency graph), and `position` / `prev` / `next` (derived from plan order, so the repo reads front to back). Section and module `arc` lines appear in every chapter file, saying where it sits in the larger story.

## Workflow

```
Intake → Interview → Research (if needed) → Draft Plan → Approve → Scaffold → Report
```

**Intake:** Classify input as vague, partial, or complete. Complete plans get gap analysis, never a rewrite.

**Interview:** One or two batched rounds. Pin down goal, scope, level, depth, and the evidence standard — the last one becomes the briefs. Infer the profile rather than asking for it by name.

**Research:** Only if gaps exist. Must return per-chapter depth notes, not just topic names.

**Draft plan:** Write `plan.yaml`. Every chapter needs a `purpose`; `depth`, `style`, and `serves` are warned when missing. Present as a readable tree with the goal, profile, and ladder.

**Approve:** User says yes (or requests changes).

**Scaffold:** `uv run scripts/scaffold.py plan.yaml --out ./repo` (`--dry-run` to preview, `--force` to overwrite).

**Report:** Tree, counts, profile and ladder, thin-brief warnings, and where PLAN.md and progress.md live.

## Reference Files

| File | When to read |
|---|---|
| `references/interview.md` | Step 2 — question banks, profile detection |
| `references/research.md` | Step 3 — search strategy, depth notes |
| `references/profiles.md` | Step 4 — choosing a profile, ladders, `tier_count`, `custom` |
| `references/plan-schema.md` | Step 4 — schema, brief and cohesion fields, sizing |
| `references/gap-analysis.md` | User supplied a plan — coverage, cohesion, brief quality |
| `references/templates.md` | Editing stub templates or generating files by hand |
| `references/bash-fallback.md` | No Python available |

## Key Outputs

- **Folder tree** with sections, modules, and chapters
- **Six briefed stub files** per chapter, cross-linked and carrying the dependency graph
- **PLAN.md** (source of truth) and **progress.md** (per-chapter tracker with `tier_reached`)
- **Exact command** to re-scaffold after amending the plan

## Quick Start Example

**User request:** "I'm interviewing for a senior backend role at a fintech company in 6 weeks. Set up a learning repo to prepare."

1. **Intake:** Goal is clear (senior BE interview, fintech, 6 weeks) → full interview.
2. **Interview:** Depth vs breadth, prior experience, weak areas, and what would convince them they'd learned it. Profile inferred: `technical`.
3. **Research:** Fintech seniority expectations, recent loop reports — returning depth notes per chapter, not just topic names.
4. **Draft plan:** Sections ordered so each unblocks the next, `builds_on`/`enables` set, a `purpose` and `depth` per chapter.
5. **Approve:** User reviews the tree, profile, and ladder.
6. **Scaffold:** `uv run scripts/scaffold.py plan.yaml`.
7. **Report:** "Created 11 chapters, 66 files, technical profile, Junior→Expert. 2 chapters have thin briefs — worth fixing before you start."

The user now fills each stub themselves or with author-chapter, which reads the brief as its assignment.

## Distinction: Structure vs. Content

- **create-learning-repo** = folders, plan, and briefed stubs that say what to write
- **author-chapter** = one complete .md with the actual teaching content

They work together: structure and brief first, then populate.
