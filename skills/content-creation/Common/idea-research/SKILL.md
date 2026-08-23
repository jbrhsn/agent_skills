---
name: idea-research
description: Research and generate ranked, evidence-backed content ideas for Medium, LinkedIn, and Reddit across AI, data engineering, finance, personal finance, writing, productivity, product reviews, and thought leadership. Use this skill whenever the user asks what to write about, wants article or post ideas, asks for trending or viral topics, wants to refill their content pipeline, mentions their `source.md` article workflow, or asks to research a niche for content opportunities — even if they don't say the word "skill" or name a specific platform. Uses only free, no-login public sources.
---

# Idea Research

Generates ranked content ideas from live public sources, then (only after the user
approves) scaffolds a `source.md` stub per approved idea.

**Hard constraints — never violate:**
- No authentication, API keys, logins, OAuth, or MCP connectors. Public endpoints only.
- Never create folders or files without explicit user confirmation.
- Every idea must cite a live source. No idea invented from memory.

## Workflow

### 1. Set up the environment (once per project)

```bash
bash scripts/setup_env.sh
```

Read the script's output and act on it:
- **uv found** → run all scripts as `uv run scripts/<name>.py`. Continue.
- **uv missing** → STOP and ask the user: *"`uv` isn't installed. Install it from
  https://docs.astral.sh/uv/getting-started/installation/, or should I proceed with
  plain `python3` instead?"* Only fall back to `python3 scripts/<name>.py` after the
  user explicitly says yes. Never silently fall back.

Scripts are stdlib-only, so there is nothing to `pip install` either way.

### 2. Fetch raw signals

Run all four fetchers. They write JSON into `.idea-research/raw/`.

```bash
uv run scripts/fetch_hn.py
uv run scripts/fetch_reddit.py
uv run scripts/fetch_trends.py
uv run scripts/fetch_medium_tags.py
```

A fetcher that fails is not fatal — the pipeline runs on whatever succeeded. Report
which sources came back empty so the user knows the coverage. See
`references/sources.md` for endpoints, rate limits, and failure modes.

### 3. Optional: expand keywords

If a keyword-research skill is available in this environment, call it now with the
beats from `references/beats.md` as seeds, save the returned terms to
`.idea-research/keywords.txt` (one per line), and pass it in step 4 with
`--keywords .idea-research/keywords.txt`.

That skill returns **terms only, no volume or competition metrics** — treat it as
query expansion, never as a scoring input. **If it is unavailable, skip this step
entirely.** The pipeline must never depend on it.

### 4. Cluster and score

```bash
uv run scripts/dedupe_and_score.py --top 15
```

Outputs a ranked table to stdout and `.idea-research/scored.json`. Scoring is
recency + engagement velocity + beat fit + a curation-gap slot. Read
`references/scoring.md` before interpreting or explaining scores.

### 5. Close the curation gap (agent work, not scriptable)

The script leaves `gap_score` at a neutral default. For the top candidates only,
web-search `site:medium.com <topic>` and check LinkedIn coverage, then adjust:

- Hot topic, no good recent coverage → raise the gap score, this is the opportunity
- Covered well and recently → lower it, or find a differentiated angle
- Large audience but the best existing piece is months old → raise it, strongest signal

Apply adjustments with `--gap-overrides` (see `references/scoring.md`).

### 6. Write the angle, not just the topic

A bare topic is not an idea. For each idea presented, produce:

- **Hook/title** — specific and concrete, with a number, named tool, or verifiable
  claim. Vague curiosity hooks underperform.
- **Angle** — the argument or story, ideally where the user's own experience meets
  the trend.
- **Platform** — Medium (long-form, 1,200–3,000 words, depth), LinkedIn (niche,
  conversation-starting, thought leadership), or Reddit (community-first, no pitch).
- **Evidence** — the source URL and its engagement numbers.

Read `references/scoring.md` § *What actually drives pickup* before writing hooks.

### 7. Present, then ask before writing anything

Show the ranked table in the conversation. Then ask which ideas to scaffold — never
scaffold automatically, never scaffold the whole list, never assume a high score is
consent.

Once the user names specific ideas, echo the exact folder paths that will be created
and wait for a final yes. Then, per approved idea:

```bash
uv run scripts/scaffold_article.py --id <idea-id> --root articles/
```

This creates `articles/<slug>/source.md` from `assets/source_template.md`. It refuses
to overwrite an existing folder.

## Reference files

- `references/beats.md` — the user's topic beats and the subreddits/tags per beat
- `references/sources.md` — endpoints, headers, rate limits, what to do when one dies
- `references/scoring.md` — the scoring formula, thresholds, and what drives pickup
- `assets/source_template.md` — the `source.md` scaffold
