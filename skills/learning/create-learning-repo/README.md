# Create-Learning-Repo Skill

## Skill Overview

The create-learning-repo skill transforms a learning goal into a folder structure with stub files — never writing the actual content. Use this skill whenever someone asks to structure a learning repository, prepare for an interview, build a study plan, turn a syllabus or curriculum into files, or organize notes for a subject. It differs from author-chapter: this skill scaffolds the **structure only**; author-chapter fills in **one chapter's content**.

## When to Use

Trigger this skill when the user:
- Wants to **organize** learning material into a repo structure (not write it)
- Needs to **prepare for an interview** or certification and wants a study plan
- Has a **syllabus or curriculum** they want turned into files and folders
- Says "structure my learning", "build a learning roadmap", "create a study plan"
- Provides an **existing plan** they want scaffolded with blank stubs

Do **not** use this skill to:
- **Write one chapter** — use author-chapter instead
- **Edit existing content** — use lean-coder instead

## Key Non-Negotiables

1. **Goal-based.** Never scaffold until you know the concrete goal (role, interview, project, deadline). Vague topic lists are not goals.
2. **Approval gate.** Show the plan as readable text and get an explicit yes before creating any files.
3. **Stubs only.** Every generated file is blank or contains only a prompt. No explanations, no answers, no filled-in content.
4. **No scheduling.** Do not map chapters to weeks unless the user asks directly.

## Workflow

```
Intake → Interview → Research (if needed) → Draft Plan → Approve → Scaffold → Report
```

**Intake:** Classify whether input is vague, partial, or complete. Vague topics trigger a full interview; partial plans get gap-filling interview; complete plans get analyzed for gaps without rewriting.

**Interview:** Ask in one or two batched rounds. Pin down goal, scope, level (beginner / practitioner / architect), and depth needed.

**Research:** Only if gaps exist. Search for standard curricula, certifications, or learning paths in the domain.

**Draft plan:** Write `plan.yaml` that decomposes learning into sections → modules → chapters → topics. Present to user as a readable tree with goal statement and exclusions.

**Approve:** User says yes to the plan (or requests changes).

**Scaffold:** Run the Python script (or bash fallback) to create the folder structure and stub files.

**Report:** Print the tree, file counts, and locations of PLAN.md and progress.md.

## Reference Files

| File | When to read |
|---|---|
| `references/interview.md` | Step 2 — question banks by input type |
| `references/research.md` | Step 3 — search strategy, weighting sources |
| `references/plan-schema.md` | Step 4 — plan.yaml schema, naming rules, sizing heuristics |
| `references/gap-analysis.md` | User supplied a plan — finding what's missing |
| `references/templates.md` | Editing stub templates or generating files by hand |
| `references/bash-fallback.md` | No Python available |

## Key Outputs

At the end of the workflow, the user receives:

- **Folder tree** with sections, modules, and chapters
- **Stub files** for each topic (blank, no content)
- **Interview prep and thought-leadership stubs** per chapter
- **PLAN.md** (the approved plan) and **progress.md** (tracking template)
- **Exact command** to scaffold it themselves if desired

The repo is ready for the user (or author-chapter) to populate with content.

## Quick Start Example

**User request:** "I'm interviewing for a senior backend role at a fintech company in 6 weeks. Set up a learning repo to prepare."

**Workflow:**

1. **Intake:** Goal is clear (senior BE interview, fintech, 6 weeks). → Full interview needed.
2. **Interview:** Ask about depth (system design only? Fintech domain knowledge?), prior experience, problem areas.
3. **Research:** Look for fintech seniority ladder, common interview topics (distributed systems, trading, settlement, fraud detection).
4. **Draft plan:** Structure as: Foundations (distributed systems, fintech basics) → Advanced (trading systems, fraud detection, compliance) → Architect (scaling, tradeoffs). Each chapter has 2–4 topics.
5. **Approve:** User reviews and approves the tree.
6. **Scaffold:** Run script. Create `interview-prep.md` and `thought-leadership.md` stubs in each chapter.
7. **Report:** "Created 5 chapters, 14 topics, 28 stub files. Start with `PLAN.md` and track progress in `progress.md`."

User now fills in each stub with author-chapter or their own research.

## Distinction: Structure vs. Content

- **create-learning-repo** = folders, files, plan, blank stubs
- **author-chapter** = one complete .md with full teaching content

They work together: structure first, then populate.
