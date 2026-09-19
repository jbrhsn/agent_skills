# Idea scoring

The optional scorer prioritizes a fetched candidate set; it does not measure truth, audience size, originality, virality, or publishing success. Editorial relevance and available evidence can override numerical order.

## Implemented formula

| Component | Maximum | Implementation |
|---|---|---|
| Recency | 30 | Newest known publication age: ≤6h 30, ≤24h 24, ≤72h 16, ≤168h 8, older 2; missing timestamp 12 |
| Engagement rate heuristic | 30 | HN/Reddit counts only: sum of (score + 2 × comments) / max(age hours, 1); 10 × log10(1 + rate), plus 5 per additional eligible source, capped at 30 |
| Beat fit | 20 | Best keyword match: 1 hit 8, 2 hits 14, ≥3 hits 20 |
| Coverage-gap judgment | 20 | Default 10; replace with a documented editorial assessment when researched |

The rate uses cumulative counts divided by age, not repeated observations of growth. It is not measured acceleration, and HN/Reddit counts are not directly comparable audience units. Google Trends traffic and Medium feed presence are excluded from engagement rate. Missing metrics are not evidence of zero reader interest.

Repeated source/URL pairs are deduplicated, and ages are recomputed from publication timestamps at scoring time. Unknown publication dates stay unknown; old cached age fields are not trusted. Scores can change with time.

A custom beats table is available through `--beats /path/beats.md`. The optional `--keywords` file adds one match bonus to an already matched beat; it does not independently discover new beats or provide demand metrics.

## Editorial review

Inspect clusters: shared title tokens can join unrelated stories or miss synonyms. Read source content before treating entries as one event. Different websites repeating one press release are not independent factual corroboration.

Check existing coverage for usefulness, evidence, freshness, and audience fit. A tag feed's presence or an unsuccessful search cannot prove saturation or a gap. Keep default gaps labeled unchecked; do not claim verification solely because an override was supplied.

## Overrides and previews

Run from the research directory containing the raw files, using the resolved installed helper path:

```bash
uv run /absolute/idea-research/scripts/dedupe_and_score.py --top 10 --min-score 0 --dry-run
uv run /absolute/idea-research/scripts/dedupe_and_score.py --gap-overrides '{"idea-1": 15}'
```

Overrides range from 0 to 20. IDs describe the current clustering run; do not reuse them after changing raw data or beats without checking the associated title and URL. Preview without writing using `--dry-run`. Default threshold 50 is a convenience filter, not a quality gate; lower it or research directly when niche/evergreen ideas are excluded.

Explain why selected ideas serve the reader and what the author can add. No score authorizes publication or unrelated file creation.
