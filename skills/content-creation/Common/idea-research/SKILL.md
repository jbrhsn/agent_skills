---
name: idea-research
description: Research and prioritize content ideas for a chosen audience or niche, with source-backed angles and optional article scaffolds. Use for topic discovery, trend research, or planning a content pipeline for Medium, LinkedIn, or Reddit.
---

# Idea Research

Find useful angles the author can credibly develop. Distinguish observed interest, editorial judgment, and original brainstorming; a popularity score is neither truth nor a promise of reach.

## Establish direction

Use the request and available writing samples to identify audience, purpose, platform, niche, geography/language, and relevant time window. Ask only about consequential ambiguity. The [beats](references/beats.md) are optional defaults, not a limit on the user's topics.

For timely claims, research live sources and check event dates as well as publication dates. Evergreen and experience-led ideas are valid without a trend anchor; label them as editorial proposals rather than measured trends. Do not invent the author's experience, expertise, results, or opinions.

## Gather proportionate evidence

Choose relevant sources instead of fetching every platform by default. Prefer primary evidence for factual claims and community discussion for audience questions. Read [sources](references/sources.md) before using the bundled fetchers. Public keyless access is their default; use other available sources when authorized and useful. Respect access controls and rate limits.

Resolve helper paths from this skill's installed directory. Run them from an isolated research working directory so old raw files cannot silently enter a new ranking. Python runs through `uv run`; if uv is missing, ask before installation, then verify it. Do not substitute bare Python. Browser research remains available if helpers cannot run.

Example, with paths resolved for the actual environment:

```bash
uv run /absolute/idea-research/scripts/fetch_hn.py --days 7
uv run /absolute/idea-research/scripts/fetch_reddit.py --subs dataengineering --window week
uv run /absolute/idea-research/scripts/dedupe_and_score.py --top 10 --min-score 0
```

The scorer reads `.idea-research/raw/` under the working directory and writes `.idea-research/scored.json`. The [scoring guide](references/scoring.md) explains biases and overrides. Scripts are optional aids; direct research may fit a niche better. Do not run keyword research unless query expansion would help the requested task.

## Select and develop angles

Inspect promising candidates beyond headlines. Check source identity, claim support, duplicated coverage, audience relevance, and whether the author can add a useful distinction, example, investigation, or experience. Search visibility is incomplete; absence from search is not proof nobody has covered a topic.

For each selected idea, give a working title, reader problem, angle, platform fit, supporting links with dates, evidence limitations, and what original material would be needed. Use engagement counts only as dated observations, not transferable audience estimates. Rank by a stated editorial rationale; do not fabricate numerical precision when research is qualitative.

## Deliver and optionally scaffold

A request for ideas can be answered directly. If the user asks to save or scaffold selected ideas, that is authorization; do not ask for a second confirmation of the same work. Without a selection, present options and ask which to develop only if file creation depends on that choice.

The scaffold helper creates one folder per invocation and refuses overwrite. Preview with `--dry-run`, then run the same command without it from the working directory holding the scored file:

```bash
uv run /absolute/idea-research/scripts/scaffold_article.py --id idea-1 --root /absolute/articles --hook "Working title" --angle "Proposed angle" --dry-run
```

Use [source_template.md](assets/source_template.md) for manual scaffolds or non-script research. Preserve provenance and clearly separate prompts for future author input from known facts. Report source gaps and created paths. This workflow does not publish or contact anyone.
