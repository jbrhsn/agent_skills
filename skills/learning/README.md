# Learning Skills

Two paired skills for learning a subject properly: one builds the structure, the other fills it in.

```
create-learning-repo/  -> goal        → folder tree of empty stubs + a plan
author-chapter/        -> one stub    → a complete zero-to-mastery chapter
```

Use them in that order, or use `author-chapter` alone for a standalone module.

| Skill | Fires when | Produces |
|---|---|---|
| [**create-learning-repo**](./create-learning-repo/README.md) | "I want to learn X", "structure my learning", "prep me for this interview", or you paste a syllabus and want it turned into files | Sections → modules → chapters → topics, one stub `.md` per topic, plus `interview.md` and `thought_leadership.md` per chapter. **Structure only — no content** |
| [**author-chapter**](./author-chapter/README.md) | "write a chapter on X", "teach me X properly", "deep dive on X" — any request whose deliverable is teaching material | One complete Markdown file taking a total beginner to architect-level on one topic |

## The split, and why

Scaffolding and authoring fail differently. Planning a curriculum needs breadth and honest gap-finding; writing a chapter needs depth and patience with a reader who knows nothing yet. Doing both in one pass produces a plan that drifts as the writing goes and chapters that assume knowledge the plan never scheduled.

So `create-learning-repo` interviews for the goal, researches to fill gaps, drafts the plan, and **shows you the tree for approval before writing anything**. Only then does `author-chapter` fill stubs one at a time — covering prerequisites, worked examples, failure modes, common misconceptions, and Socratic checkpoints, written so a bright teenager can follow it.

## Install

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy the folders into whichever skills directory your harness reads:

```bash
cp -r create-learning-repo author-chapter ~/.claude/skills/
```

`create-learning-repo` ships a stdlib-only `scripts/scaffold.py` that builds the tree from an approved `plan.yaml` — no third-party packages.

Both write into the repository you invoke them from, not into this one.
