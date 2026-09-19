# Endpoint reference

The optional `kwfetch.sh` uses curl/jq with bounded request timeouts. Availability and policies can change. Inspect actual responses and log coverage; a documented API is not an uptime guarantee, and public access is not permission to evade limits.

## Documented sources

- [Datamuse](https://www.datamuse.com/api/): `https://api.datamuse.com/words?ml=<seed>&max=50` or `rel_trg=<seed>` returns lexical candidates with relative scores. The documented separate suggestion endpoint is `/sug?s=<prefix>`. Checked 2026-09-19: the publisher says keys will be required from 2027-01-01. The bundled keyless helper should skip unavailable calls; adding credentials is a separate authorized choice.
- Wikipedia OpenSearch: `https://en.wikipedia.org/w/api.php?action=opensearch&search=<term>&limit=10&format=json` returns candidate titles and URLs. Resolve identity before interpreting pageviews.
- Wikimedia pageviews: `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/<encoded_title>/monthly/<start>/<end>`. The helper requests the last 12 full months and emits the mean. These are Wikipedia views, not query searches.
- Stack Exchange: `https://api.stackexchange.com/2.3/search/advanced?q=<seed>&site=<site>&sort=votes&order=desc`. Questions and votes can reveal reader problems. Observe returned quotas/backoff and stop or defer requests when instructed. The helper does not coordinate backoff across separate runs.

## Unofficial sources

Google Suggest (`suggestqueries.google.com/complete/search?client=firefox&q=<query>`) and Bing's OpenSearch endpoint (`api.bing.com/osjson.aspx?query=<query>`) can provide observed suggestions; neither helper path establishes volume or ranking difficulty. Results depend on query, locale support, and date.

DuckDuckGo HTML related-phrase extraction is opt-in with `--ddg`; it can fail when markup changes. Validate outputs before treating them as phrases. Do not bypass access controls or CAPTCHA.

## Operational use

Use a descriptive User-Agent, URL-encoded values, sensible request spacing, and limited expansion. Set `KW_UA` appropriately; never invent a contact identity. `--gl`/`--hl` affect the Google requests, not every source. `--se-site` selects the Stack Exchange site. `--deep` adds many queries; use only when useful.

The helper can exit 0 with partial or empty evidence. A 403/429, parse failure, empty body, or successful empty result should not become a numerical observation. Preserve diagnostics and explain uncertainty. Use browser research or authorized user-provided data when an endpoint is unavailable.

No absolute claim that a platform has no data API is needed. The bundled sources simply do not measure Medium tag reach or LinkedIn hashtag performance; such suggestions remain inference unless supplemented by real evidence.
