# Create Learning Repo

Design or review a learning path, organize a syllabus, or create a repository with chapter briefs and progress tracking. A plan-only request produces a plan; a repository request can proceed to file creation without a separate approval round unless the user asks to review first.

## Approach

Use the learner's goal, starting level, and constraints to choose scope and depth. Infer reasonable defaults, ask only consequential unanswered questions, and research where verification or gap-filling helps. A broad exploratory goal is enough to begin. Profiles, size estimates, and interview questions are guidance rather than prerequisites.

The skill usually scaffolds briefs. If teaching content is also requested, the agent continues authoring, optionally using `author-chapter`. There is no mandatory handoff that leaves the requested work incomplete.

## Bundled helper

The helper generates sections → modules → chapters with six files per chapter: `learning.md`, `examples.md`, `practice.md`, `interview.md`, `thought_leadership.md`, and `quizzies.md`. It also creates `README.md`, `PLAN.md`, and `progress.md`.

Profiles select tier labels and study prompts: `technical`, `craft`, `practice`, `exam`, or `custom`. The helper supports two to four progression levels and configurable slot counts. These limits describe the script, not all learning projects. Create a custom layout directly when the request needs another shape; the script has no option to select a subset of chapter files.

From this skill's directory:

```bash
uv run scripts/scaffold.py /path/to/plan.yaml --out /path/to/repo --dry-run
uv run scripts/scaffold.py /path/to/plan.yaml --out /path/to/repo
```

JSON input also works with plain Python without external dependencies. YAML requires PyYAML. Existing files are skipped unless `--force` is supplied; inspect before replacing content and prefer targeted edits where learning has already begun.

Keep `plan.yaml` or `plan.json`: it is the helper's actual input. `PLAN.md` is a generated human-readable summary, so editing it alone cannot change a later scaffold run. Keep the plan, summary, links, and progress tracker consistent when scope changes. Regeneration with `--force` replaces authored files and resets generated progress.

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
