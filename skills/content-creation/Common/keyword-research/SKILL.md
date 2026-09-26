---
name: keyword-research
description: Research search intent, query phrasing, and discovery terms for an article or defined topic. Use for keyword research, SEO framing, search-focused titles, and relevant platform tags, with explicit evidence limitations.
---

# Keyword Research

Run the bundled shell helper as its saved file. Before executing newly authored shell, Python, or Node automation, save it under the target project's `.temp/` and invoke it from there; do not pass program source through the terminal. Python, when needed, runs through `uv run` with the target project's `.venv`.

Help the right reader find content that answers their question. Keyword selection follows the article's substance; do not add unsupported sections or distort a thesis to chase a score.

## Establish intent

Read the named draft or supplied text. A nearby `source.md` is a useful convention, not a prerequisite. For topic-only requests, establish the audience and angle, then label recommendations provisional until a draft exists. Identify useful seeds, entities, language/region, and the reader's task. Ask only when plausible interpretations would materially change research.

Default file output is `kresearch.md` beside the source; follow explicit output paths or respond in conversation when appropriate. Preserve source material and existing user edits.

## Research

Read [methodology](references/methodology.md) and relevant [endpoint details](references/endpoints.md). The optional Bash helper needs curl and jq; missing dependencies do not prevent browser-based research. Installation requires applicable authorization. Resolve its absolute path from this skill's installed location and use a dedicated run directory for artifacts.

```bash
bash /absolute/keyword-research/scripts/kwfetch.sh all "seed phrase" -e "entity" --gl US --hl en -o raw.tsv
bash /absolute/keyword-research/scripts/kwfetch.sh score raw.tsv
```

Choose only useful sources or expansion options; `all` is a convenience, not an obligatory workflow. Retain source diagnostics, query/locale/date, and raw observations needed to audit the report. Respect blocks and rate limits; do not repeatedly retry denied access.

Public keyless sources are the default. User-provided analytics or authorized tools can add evidence; identify their measurement and coverage. Do not send private manuscript text to search services; query only the minimum non-sensitive terms.

## Interpret honestly

Read [scoring](references/scoring.md) before reporting helper scores. A/B/C/D describe provenance, not confidence in ranking, search demand, or accuracy. Autocomplete rank, semantic similarity, Wikipedia views, and community votes measure different things. Never relabel them as search volume, difficulty, CPC, or expected traffic.

Cluster by intent and retain terms the draft can actually answer. A relevant low-score or inferred term can be preferable to an irrelevant high-score phrase. Mark platform tags/hashtags as editorial suggestions unless an identified source actually measures them.

## Deliver

Use [output guidance](references/output-schema.md) and the adaptable [report template](assets/kresearch_template.md). Explain recommended primary/secondary phrases, their fit, useful placements, evidence, uncertainty, and sources that failed or were not queried. Avoid tag quotas and keyword stuffing.

Keep raw evidence when useful for reproducibility; remove only disposable artifacts owned by this run when appropriate. Report material missing evidence. Do not promise ranking or treat research as authorization to rewrite or publish the article.
