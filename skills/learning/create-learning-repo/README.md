# Create Learning Repo

Design or review a learning path, organize a syllabus, or create a repository with chapter briefs and progress tracking. A plan-only request produces a plan; a repository request can proceed to file creation without a separate approval round unless the user asks to review first.

## Approach

Use the learner's goal, starting level, and constraints to choose scope and depth. Build the smallest useful path, covering essential capabilities and prerequisites while deferring enrichment. Each chapter gets coverage, a depth boundary, a connection to the goal, and an observable completion check; the plan also defines how to demonstrate the overall goal. Infer reasonable defaults, ask only consequential unanswered questions, and research where verification or gap-filling helps. A broad exploratory goal is enough to begin.

The skill usually scaffolds briefs. If teaching content is also requested, the agent continues authoring, optionally using `author-chapter`. There is no mandatory handoff that leaves the requested work incomplete.

## Bundled helper

The helper generates sections → modules → chapters with three files per chapter by default: `learning.md`, `examples.md`, and `practice.md`. Set `chapter_files` to select from these plus `interview`, `thought_leadership`, and `quizzies`, always retaining `learning`. It also creates `README.md`, a linked `PLAN.md` roadmap with chapter coverage and completion checks, and `progress.md`. Activity stubs carry their purpose and completion check and direct the author to the full chapter brief before filling them.

Profiles select tier labels and study prompts: `technical`, `craft`, `practice`, `exam`, or `custom`. Presets default to two progression levels; custom profiles use their declared ladder. `tier_count` selects one to four levels. Activity defaults are small (two examples and two practice tasks, or three exam drills); `counts` adjusts them. Navigation and tracking include only selected files. Create a custom layout directly when another directory structure fits better.

Resolve the helper from this skill's installed directory, then run it through the target learning project's `.venv`:

```bash
uv run --python /path/to/repo/.venv/bin/python python /absolute/path/to/create-learning-repo/scripts/scaffold.py /path/to/plan.yaml --out /path/to/repo --dry-run
uv run --python /path/to/repo/.venv/bin/python python /absolute/path/to/create-learning-repo/scripts/scaffold.py /path/to/plan.yaml --out /path/to/repo
```

YAML requires PyYAML in the target `.venv`; create that environment with `uv venv` when absent and install the dependency with `uv pip install --python /path/to/repo/.venv/bin/python pyyaml`. Existing files are skipped unless `--force` is supplied; inspect before replacing content and prefer targeted edits where learning has already begun.

Keep `plan.yaml` or `plan.json`: it is the helper's actual input. `PLAN.md` is a generated human-readable summary, so editing it alone cannot change a later scaffold run. Keep the plan, summary, links, and progress tracker consistent when scope changes. Regeneration with `--force` replaces authored files and resets generated progress.

Existing plans without file or tier settings now use the smaller defaults. To reproduce the former technical layout, explicitly select all six files, set `tier_count: 4`, and set `counts` to `examples: 3`, `practice: 4`, `interview: 12`, `thought_leadership: 4`, and `quizzies: 10`. Deselected files are never deleted; update existing repositories with targeted edits to preserve learner work and avoid stale navigation.

The helper rejects invalid chapter references and prerequisite ordering, and warns when chapter depth, goal connection, or completion checks are absent. Older plans remain loadable without the new `goal_check` and chapter `completion_check` fields. The agent reviews coverage, scope, effort, and generated output before delivery; script success alone does not establish educational completeness.

## References

| Reference | Use |
|---|---|
| [Interview](references/interview.md) | Optional questions for missing context |
| [Gap analysis](references/gap-analysis.md) | Review an existing plan |
| [Research](references/research.md) | Verify expectations and improve depth notes |
| [Profiles](references/profiles.md) | Helper presets and custom tiers |
| [Plan schema](references/plan-schema.md) | Required input fields and optional metadata |
| [Templates](references/templates.md) | Standard helper output |
| [Bash fallback](references/bash-fallback.md) | Shell creation when useful |
