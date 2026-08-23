# Sources

Every source here is public and requires **no login, no API key, no OAuth, no MCP
connector**. If a source ever starts requiring auth, drop it — do not work around it.

## Contents

- [Hacker News](#hacker-news)
- [Reddit](#reddit)
- [Google Trends](#google-trends)
- [Medium tags](#medium-tags)
- [Failure handling](#failure-handling)
- [Raw output schema](#raw-output-schema)
- [Manual fallback](#manual-fallback)

## Hacker News

Algolia's HN API. Free, documented, no key.

```
https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i>UNIX,points>20&hitsPerPage=100
```

Best signal of the four: exposes `points`, `num_comments`, and an exact timestamp, so
velocity is computable directly. Generous rate limits; the fetcher still sleeps
between queries.

## Reddit

Public JSON endpoints — no OAuth for read-only listings.

```
https://www.reddit.com/r/<sub>/top.json?t=week&limit=50
```

**A descriptive `User-Agent` header is mandatory.** Reddit returns 429 or 403 for the
default Python urllib agent. The fetcher sets one.

If JSON starts 403-ing, fall back to the RSS feed, which is more permissive:

```
https://www.reddit.com/r/<sub>/.rss
```

RSS lacks scores, so those items get velocity 0 and rank on recency and beat fit
only. The fetcher does this automatically and flags it in its output.

## Google Trends

The daily trending RSS feed. Public, no key, no `pytrends` dependency.

```
https://trends.google.com/trending/rss?geo=US
```

Set `--geo` to change region (`IN`, `GB`, `US`). Broad and consumer-skewed — most
items will fail the beat filter, which is expected and fine. It exists to catch the
occasional mainstream break-out in the user's beats, not to be a primary source.

Provides approximate traffic (e.g. `20,000+`) but **no per-item timestamp**, so items
get a flat mid-range recency score.

## Medium tags

Public per-tag RSS. No login.

```
https://medium.com/feed/tag/<tag>
```

Returns roughly the 10 most recent posts per tag. This is a **saturation signal, not
a trending signal** — it shows what is already being published, which feeds the
curation-gap check rather than the hot-topic check. A topic appearing heavily here is
evidence *against* writing the obvious version of it.

## Failure handling

Any fetcher can fail without stopping the pipeline. Each writes its own file to
`.idea-research/raw/`; the scorer globs whatever is there.

- Fetcher fails → it writes an empty array and exits 0 with a warning on stderr
- All fetchers fail → the scorer exits with a clear error, no partial results
- Always tell the user which sources returned nothing, so they can judge coverage

Never fabricate items to fill a gap.

## Raw output schema

Every fetcher writes `.idea-research/raw/<source>.json` — a flat array of:

```json
{
  "source": "hn",
  "title": "Show HN: A DuckDB-backed replacement for our Airflow pipeline",
  "url": "https://news.ycombinator.com/item?id=...",
  "score": 340,
  "comments": 128,
  "created_utc": 1755900000,
  "age_hours": 6.2,
  "degraded": false
}
```

`created_utc` may be `null` (Trends, some RSS) → the scorer applies a neutral recency
score. `degraded: true` means the source fell back to a lower-fidelity endpoint.

## Manual fallback

If a source is blocked in the user's network or has gone auth-only, do it manually:
have the user paste titles/links, then append them to
`.idea-research/raw/manual.json` in the schema above. The scorer treats manual items
identically. This keeps the workflow unblocked without ever adding a credential.
