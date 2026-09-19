---
name: create-learning-repo
description: Design or review a learning roadmap, organize a syllabus, or scaffold a learning repository with chapter briefs and progress tracking. Use for requests to plan or structure learning, interview preparation, or exam study; a request to explain a topic alone does not require a repository.
---

# Create Learning Repo

Turn a learning goal into a usable path with clear chapter purposes, appropriate depth, and meaningful ways to assess progress. Deliver a plan, review, or repository according to the request.

## How to use this guidance

Treat the workflow, profiles, sizing heuristics, and layouts as adaptable defaults. Use the user's context and your judgment to choose the amount of planning, research, and structure the task needs. This skill adds no approval gate: a request to create a repository authorizes routine file creation within that scope. If the user asks to review a plan first, present it and wait before implementation.

Preserve existing work and explicit scope choices. Ask only about consequential ambiguity that cannot reasonably be resolved from context. A broad interest can be a valid starting goal; a deadline, job title, or detailed interview is not a prerequisite for useful progress.

## Understand the goal

Identify the desired outcome, starting level, constraints, and any supplied syllabus or plan. Infer missing details where reasonable and record assumptions that affect the result. Use [interview.md](references/interview.md) as a question bank, not a questionnaire to administer in full.

For an existing plan, preserve the parts that work and use [gap-analysis.md](references/gap-analysis.md) to identify meaningful gaps. A review request calls for findings; an improvement request can authorize the corresponding edits. Avoid replacing the user's direction with a larger curriculum they did not request.

## Build a useful plan

Organize topics around capabilities and prerequisites. Describe what each chapter is for and how deeply it should teach its topics. Choose domain-appropriate progression from [profiles.md](references/profiles.md), or another structure when useful. Scheduling can help when time planning is part of the request; otherwise a sequence and rough effort estimates may be enough.

Research when needed to resolve gaps, verify changing expectations, or satisfy the user's request and environment requirements. [research.md](references/research.md) suggests sources and useful outputs without a query quota. Lack of search access should lead to qualified assumptions, not invented sources or a blanket halt.

For a plan-only request, deliver the plan without creating an unsolicited repository. When file creation is requested, proceed once the direction is sufficiently clear; a preview or dry run can clarify the result without requiring a separate approval round.

## Choose a layout and create it

The bundled helper offers a consistent layout: sections → modules → chapters, with six briefed stubs per chapter:

| File | Intended use |
|---|---|
| `learning.md` | Explanation of chapter topics |
| `examples.md` | Worked examples or specimens to study |
| `practice.md` | Tasks, success criteria, and learner reflections |
| `interview.md` | Interview, peer, or examiner questions |
| `thought_leadership.md` | Optional writing angles and supporting evidence |
| `quizzies.md` | Self-assessment and recall |

This is the helper's format, not a requirement for every learning project. For a smaller or custom layout, create files directly and keep links and tracking consistent. Do not pass unsupported layout options to the helper.

For the standard layout, read [plan-schema.md](references/plan-schema.md) and create `plan.yaml` or `plan.json`. The script requires chapter `purpose` and other schema fields; warnings about missing optional depth or style are useful review signals, not automatic blockers.

Run the helper from this skill's directory, or resolve its path relative to this skill rather than the user's project:

```bash
uv run scripts/scaffold.py /path/to/plan.yaml --out /path/to/learning-repo --dry-run
uv run scripts/scaffold.py /path/to/plan.yaml --out /path/to/learning-repo
```

`python3 scripts/scaffold.py /path/to/plan.json` works without third-party dependencies. YAML input requires PyYAML. If the helper is unavailable or unsuitable, create the requested files with available tools; [templates.md](references/templates.md) describes its output and [bash-fallback.md](references/bash-fallback.md) offers a shell option.

The helper skips existing files unless `--force` is used. Inspect existing content before replacement; prefer targeted edits for a repository with learner work. Keep the machine-readable plan, `PLAN.md`, links, and `progress.md` consistent when changing scope. `PLAN.md` is a human-readable summary, not an input format the script reads.

## Continue to the requested outcome

Scaffolding normally produces briefs and empty study slots. If the request also includes teaching content, continue authoring it; use the `author-chapter` skill if available and useful, or write it directly. The distinction between planning and authoring organizes work rather than imposing a stopping point.

Report the plan or files created, important assumptions, and material gaps or skipped files. For a standard repository, include the location of the plan and progress tracker; include a tree and counts when they help the user navigate.
