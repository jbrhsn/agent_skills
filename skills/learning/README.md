# Learning Skills

Two complementary skills support learning projects. Use either alone or combine them when the request spans planning and teaching.

| Skill | Use for | Typical output |
|---|---|---|
| [create-learning-repo](create-learning-repo/README.md) | Planning, reviewing, or organizing a learning path | A roadmap or repository with chapter briefs and progress tracking |
| [author-chapter](author-chapter/README.md) | Writing or revising substantial teaching material | A chapter, tutorial, guide, exercises, or populated learning files |

Both skills provide guidance rather than a fixed procedure. The agent adapts the depth, format, research, questions, and workflow to the request. There is no mandatory approval round, chapter-size cutoff, search quota, or ban on answer keys. Accuracy, preservation of learner work, and honest reporting still matter.

The scaffolding helper creates six files per chapter and uses a domain-specific progression. That is the helper's supported format; a custom layout can be created directly. Planning and authoring can continue in the same task when both are requested.

## Installation

From this repository, preview or sync using the standard scripts:

```bash
uv run scripts/sync_all.py --dry-run
uv run scripts/sync_all.py
```

The skills operate in the user's target project. Their bundled references and helper paths resolve relative to the installed skill directory.
