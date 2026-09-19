# Idea Research

Research useful content angles for a chosen audience and prioritize them with traceable evidence. Timely topics, evergreen questions, and experience-led pieces are all valid; only measured trend claims require trend evidence.

[SKILL.md](SKILL.md) guides source choice, editorial judgment, and optional scaffolding. Default beats are examples, not topic restrictions. The workflow preserves source limitations and never invents the author's experience.

## Optional helper workflow

Resolve the installed skill path. Run helpers from a fresh research directory so cached JSON from unrelated work cannot enter the ranking.

```bash
bash /absolute/idea-research/scripts/setup_env.sh
uv run /absolute/idea-research/scripts/fetch_hn.py --days 7
uv run /absolute/idea-research/scripts/dedupe_and_score.py --min-score 0 --dry-run
uv run /absolute/idea-research/scripts/dedupe_and_score.py --min-score 0
uv run /absolute/idea-research/scripts/scaffold_article.py --id idea-1 --root /absolute/articles --dry-run
```

Remove --dry-run to create a requested scaffold. Existing folders are not overwritten. Each helper call handles one scaffold; repeat for a user-requested selection without another confirmation gate.

The setup script only checks uv; it does not create a venv or install packages. Python scripts use uv run. If uv is missing, obtain installation confirmation rather than falling back to bare Python.

## Evidence and scores

Fetchers support HN, Reddit JSON/RSS, Google Trends RSS, and Medium tag RSS; choose only relevant ones. They may succeed with empty/partial data, so inspect diagnostics. Raw files live under .idea-research/raw/ in the working directory.

The scorer deduplicates identical source/URL pairs and refreshes ages from publication timestamps. It uses recency, bounded keyword fit, an HN/Reddit engagement-rate proxy, and an explicitly provisional coverage-gap judgment. It excludes Trends traffic from social engagement and does not penalize Medium presence automatically.

Use --beats for a custom table, --keywords for an optional match bonus, --gap-overrides for documented judgments from 0 to 20, and --top/--min-score for presentation. IDs apply to the current candidate run, not a permanent content database. Read [scoring](references/scoring.md) and [sources](references/sources.md) for limitations.

No scores guarantee interest, truth, originality, or reach. Scaffolding is appropriate when requested; research alone does not authorize publication.
