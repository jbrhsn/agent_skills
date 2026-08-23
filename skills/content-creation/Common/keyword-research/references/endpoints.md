# Endpoint reference

Read this before running or debugging `scripts/kwfetch.sh`.

Endpoints are split into two tiers. The tier determines the confidence grade a
keyword can earn (see `scoring.md`), so keep them straight.

- **Tier 1 — official, documented, keyless.** Publisher supports programmatic
  access. Safe to depend on.
- **Tier 2 — undocumented public endpoints.** They work today and have for years,
  but the publisher does not document, support, or guarantee them. Treat every
  Tier 2 result as unverified.

Contents:
1. Tier 1 — Datamuse
2. Tier 1 — Wikipedia OpenSearch
3. Tier 1 — Wikimedia Pageviews
4. Tier 1 — Stack Exchange
5. Tier 2 — Google Suggest
6. Tier 2 — Bing Autosuggest
7. Tier 2 — DuckDuckGo HTML
8. Dead sources — do not use
9. Shared conventions

---

## 1. Tier 1 — Datamuse

Word-finding engine. The single most useful source here: `rel_trg` returns words
that statistically co-occur with the seed, which is as close to genuine "related
terms" as anything free gets.

```
GET https://api.datamuse.com/words?ml=<seed>&max=50      # means-like / semantic
GET https://api.datamuse.com/words?rel_trg=<seed>&max=50 # trigger / co-occurring
GET https://api.datamuse.com/words?sug=<prefix>          # /sug endpoint, autocomplete
```

Response: `[{"word":"machine learning","score":51232}, ...]`

- Free, no key, 100,000 requests/day.
- **Expiry: from 2027-01-01 an API key is required.** Still free, but the keyless
  path ends. If calls start returning 401 after that date, this is why — tell the
  user they need to request a key from datamuse.com rather than debugging further.
- `score` has no absolute meaning. It ranks results within one response and
  nothing more. Never convert it to a volume estimate.
- Works on multi-word phrases but degrades; prefer 1–3 word seeds.

## 2. Tier 1 — Wikipedia OpenSearch

Canonical entity names and disambiguation. Use it to find the *correct* name for
a concept before measuring interest in it.

```
GET https://en.wikipedia.org/w/api.php?action=opensearch&search=<term>&limit=10&format=json
```

Response: `["query", ["Title 1","Title 2"], ["desc",...], ["url",...]]` — titles
are element `[1]`.

## 3. Tier 1 — Wikimedia Pageviews

The only source in this stack that returns a **real absolute number**. Use it to
sanity-check whether a topic has meaningful public interest and whether that
interest is rising or falling.

```
GET https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/
    en.wikipedia/all-access/user/<URL-encoded_Title>/monthly/<YYYYMMDD>/<YYYYMMDD>
```

Response: `{"items":[{"timestamp":"2026010100","views":48213}, ...]}`

- Article titles use underscores and are case-sensitive. Resolve them via
  OpenSearch first; a guessed title returns 404.
- **A descriptive `User-Agent` is required.** Wikimedia returns 403 for generic
  or absent agents. The script sets one; do not strip it.
- This measures Wikipedia readership, not Google searches. It is a directional
  proxy for topic interest and correlates loosely with search demand. Say that in
  the report — do not launder it into a volume figure.
- Only meaningful for topics that *have* a Wikipedia article. Most long-tail
  keywords will not.

## 4. Tier 1 — Stack Exchange

Only worth calling for technical topics. Returns real questions real people asked,
with vote counts — excellent raw material for question-shaped headings.

```
GET https://api.stackexchange.com/2.3/search/advanced
    ?q=<seed>&order=desc&sort=votes&site=stackoverflow&pagesize=25
```

- **Responses are always gzipped.** curl needs `--compressed` or you get binary.
- Anonymous quota is 300 requests/day per IP. Ample here; do not loop it.
- Swap `site=` for `datascience`, `stats`, `serverfault`, `superuser` etc. when
  the topic fits better elsewhere.
- Check `.quota_remaining` in the response if calls start failing.

## 5. Tier 2 — Google Suggest

Not an API. Undocumented, unsupported, no SLA. It is nonetheless the best
available signal for how people actually phrase queries.

```
GET https://suggestqueries.google.com/complete/search
    ?client=firefox&hl=en&gl=US&q=<query>
```

Response: `["query", ["suggestion 1","suggestion 2", ...], [], {...}]`

- `client=firefox` yields plain JSON. Other client values return XML or JSONP.
- **Order carries signal.** Position 1 is a stronger indication than position 8.
  The script preserves rank; the scorer uses it.
- Expansion technique ("alphabet soup"): re-query the seed with modifiers appended
  and prepended — `<seed> for`, `<seed> vs`, `how to <seed>`, `best <seed>`, and
  optionally `<seed> a` … `<seed> z`. Each returns a different slice.
- Rate-limit yourself. The script sleeps between calls. Hammering it earns a
  temporary block, and there is no error message that says so — you just get
  empty arrays.
- Set `gl`/`hl` to the target audience's country/language, not yours.

## 6. Tier 2 — Bing Autosuggest

Same category. Valuable mainly as a cross-check: a phrase appearing in both
Google and Bing suggest is a stronger signal than one appearing in either alone.

```
GET https://api.bing.com/osjson.aspx?query=<query>
```

Response: `["query", ["suggestion 1", ...]]`

Despite the hostname this is the OpenSearch JSON endpoint, not the paid Bing
Autosuggest API on Azure. No key. No documentation either.

## 7. Tier 2 — DuckDuckGo HTML

```
GET https://html.duckduckgo.com/html/?q=<query>
```

Returns server-rendered HTML — no JavaScript needed, unlike Google SERPs. Used
only to harvest related-search phrases. Optional; the script skips it unless
`--ddg` is passed, because HTML structure changes without warning and a broken
selector silently yields zero results rather than an error.

If you use it, verify the output looks like phrases before trusting it.

## 8. Dead sources — do not use

Listed so nobody re-adds them.

- **Reddit `.json` endpoints** — Reddit announced deprecation of unauthenticated
  `.json` access on 2026-05-28; requests began returning 403 within days. Not
  rate-limited, blocked. Pushshift is also gone. There is no free replacement.
- **Google SERP / People Also Ask scraping** — JavaScript-rendered, CAPTCHA-gated,
  and against Google's terms. Anything built on it breaks quickly.
- **Medium search** — no public API. Scraping their search is fragile and outside
  the spirit of their terms. Medium tags in the report are inferred, not measured.
- **LinkedIn** — search and feed are behind authentication with no public
  alternative. Hashtag suggestions in the report are inferred, not measured.
- **Google Trends unofficial endpoints** — the `widgetdata` endpoints require a
  session token flow that breaks constantly and is aggressively rate-limited.
  Excluded deliberately; a source that works one run in three is worse than none.

## 9. Shared conventions

- Always URL-encode query values (`curl --data-urlencode`, never string
  concatenation — seeds contain spaces and `&`).
- Set a descriptive `User-Agent` on every request. Required by Wikimedia, good
  manners everywhere else. Override with the `KW_UA` environment variable.
- Set a timeout on every call so one hung endpoint cannot stall the run.
- Treat any non-zero exit or empty result as "source unavailable" and continue.
  Partial data clearly labelled beats a failed run.
