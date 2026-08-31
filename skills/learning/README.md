# Learning Skills

Two paired skills for learning a subject properly: one builds the structure, the other fills it in.

```
create-learning-repo/  -> goal        → folder tree of briefed stubs + a plan
author-chapter/        -> one stub    → a complete chapter, in five-minute units
```

Use them in that order, or use `author-chapter` alone for a standalone module.

| Skill | Fires when | Produces |
|---|---|---|
| [**create-learning-repo**](./create-learning-repo/README.md) | "I want to learn X", "structure my learning", "prep me for this interview", or you paste a syllabus and want it turned into files | Sections → modules → chapters, six briefed stubs per chapter (`learning`, `examples`, `practice`, `interview`, `thought_leadership`, `quizzies`) on a domain-matched tier ladder. **Structure and assignment only — no content** |
| [**author-chapter**](./author-chapter/README.md) | "write a chapter on X", "teach me X properly", "deep dive on X" — any request whose deliverable is teaching material, or filling any file the scaffolder produced | One complete Markdown file: takeaway first, the vital 20% marked as a core path, cut into self-contained ~5-minute units, on the ladder and domain the brief specifies |

## The split, and why

Scaffolding and authoring fail differently. Planning a curriculum needs breadth and honest gap-finding; writing a chapter needs depth and patience with a reader who knows nothing yet. Doing both in one pass produces a plan that drifts as the writing goes and chapters that assume knowledge the plan never scheduled.

So `create-learning-repo` interviews for the goal, researches to fill gaps, drafts the plan, and **shows you the tree for approval before writing anything**. Only then does `author-chapter` fill stubs one at a time — reading each file's brief as its assignment rather than re-planning, and using the tier ladder the plan chose rather than imposing an engineering one.

The reader model is an intelligent 28-year-old who knows nothing about the field: nothing assumed inside the subject, nothing explained about the world, nothing padded. Chapters open with the takeaway, mark the 20% that makes you functional, and are cut into units you can finish in one sitting and return to a week later.

## Install

```bash
uv run scripts/sync_all.py            # every skill in the repo, all five platforms
```

Or copy the folders into whichever skills directory your harness reads:

```bash
cp -r create-learning-repo author-chapter ~/.claude/skills/
```

`create-learning-repo` ships `scripts/scaffold.py`, which builds the tree from an approved `plan.yaml`. Run it with `uv run` (a PEP 723 header pulls in PyYAML); plain `python3` works too, and needs no third-party package at all if the plan is JSON.

Both write into the repository you invoke them from, not into this one.
