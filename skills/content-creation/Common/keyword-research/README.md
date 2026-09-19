# Keyword Research

Research search intent and phrasing for an article, supplied text, or a defined topic. The output recommends useful terms and placements while separating observed evidence from inference. A topic-only report remains provisional.

Default output is kresearch.md beside the source; explicit paths or inline requests take precedence. See [SKILL.md](SKILL.md).

## Optional helper

The Bash helper requires curl and jq. Resolve its installed path and use a dedicated run directory:

```bash
bash /absolute/keyword-research/scripts/kwfetch.sh all "agent context management" -e "MCP" --gl US --hl en --dry-run
bash /absolute/keyword-research/scripts/kwfetch.sh all "agent context management" -e "MCP" --gl US --hl en -o raw.tsv
bash /absolute/keyword-research/scripts/kwfetch.sh score raw.tsv
```

Individual modes are suggest, related, entity, and questions. --deep expands autocomplete queries; --ddg opts into fragile HTML extraction; --se-site selects a Stack Exchange site. KW_UA sets a descriptive user agent and KW_SLEEP controls autocomplete spacing.

A preview performs no network requests or writes. Actual runs may return partial/empty data; retain diagnostics and report coverage. Browser research or authorized user data remains useful when helpers are unavailable.

## Interpretation

Scores are within-run heuristics, not volume, difficulty, CPC, or forecasts. A/B/C/D grades describe provenance only. Wikipedia and its pageviews form one source family; a pageview count alone is not corroborated keyword demand.

Autocomplete, lexical associations, encyclopedia readership, and question votes measure different things. The helper emits mean monthly pageviews, which cannot establish a trend direction. Tags/hashtags remain editorial inference unless actual relevant measurement is supplied.

See [endpoints](references/endpoints.md) for availability and the documented Datamuse key requirement planned for 2027-01-01, and [scoring](references/scoring.md) for the exact ranking formula. No particular source or installation is required merely to make progress on the research.
