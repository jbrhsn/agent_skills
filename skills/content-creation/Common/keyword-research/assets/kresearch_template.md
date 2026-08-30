---
article: <folder-slug>
generated: <YYYY-MM-DD>
seed: "<exact seed string passed to kwfetch>"
entities: [<entity1>, <entity2>]
locale: <hl>/<gl>
sources_ok: [<google, bing, datamuse, ...>]
sources_failed: [<...>]
---

# Keyword research — <Article title>

**Thesis:** <one sentence from source.md>

**Angle:** <what this draft says that page one doesn't>

**Reader:** <who is searching for this>

> No search volume, keyword difficulty, or CPC appears anywhere in this report. Those require a paid tool or a Google Ads account. Scores below are a relative ranking heuristic, comparable only within this run. Every row carries a confidence grade: **A** measured + corroborated · **B** measured, single source · **C** observed via unofficial autocomplete · **D** inferred, no data.

---

## 1. Primary keyword

| Term | Score | Grade | Sources |
|---|---|---|---|
| `<term>` | <n> | <A–D> | <source list> |

**Why this one:** <one line tying it to the angle>

**Title candidates**
1. <title containing the term naturally>
2. <title>
3. <title>

### Alternate primaries

| Term | Score | Grade | Use as |
|---|---|---|---|
| `<term>` | <n> | <g> | <H2 / A-B title test> |
| `<term>` | <n> | <g> | <...> |

---

## 2. Long-tail keywords by intent

Drop any cluster this draft doesn't actually serve. Don't pad.

### Informational
| Term | Score | Grade | Sources | Suggested use |
|---|---|---|---|---|
| `<term>` | <n> | <g> | <srcs> | <H2 heading> |

### How-to / procedural
| Term | Score | Grade | Sources | Suggested use |
|---|---|---|---|---|

### Comparison
| Term | Score | Grade | Sources | Suggested use |
|---|---|---|---|---|

### Troubleshooting
| Term | Score | Grade | Sources | Suggested use |
|---|---|---|---|---|

### Evaluative
| Term | Score | Grade | Sources | Suggested use |
|---|---|---|---|---|

---

## 3. Topic interest signal

*Wikimedia Pageviews — real numbers. Measures Wikipedia readership, not search volume. Directional only.*

| Wikipedia article | Mean monthly views | Direction |
|---|---|---|
| <Title> | <n> | <rising / flat / falling> |

<If no entity had an article, say so and note what that implies.>

---

## 4. Real questions people asked

*Stack Exchange — actual question titles with vote counts. Best raw material for headings and an FAQ block. Paraphrase rather than copying verbatim.*

| Question (paraphrased) | Votes | Covered in draft? |
|---|---|---|
| <question> | <n> | yes / no / partly |

---

## 5. Native discovery — Medium & LinkedIn (grade D, inferred)

> No public data source exists for Medium tag popularity or LinkedIn hashtag reach — both are behind authentication with no keyless API. Everything in this section is inferred from the clusters above. Treat as informed judgement, not measurement.

**Medium tags (5)**
| Tag | Breadth | From cluster |
|---|---|---|
| <tag> | broad | <cluster> |
| <tag> | mid | <cluster> |
| <tag> | mid | <cluster> |
| <tag> | mid | <cluster> |
| <tag> | niche | <cluster> |

**LinkedIn hashtags (3–5)** `#<tag>` `#<tag>` `#<tag>`

**LinkedIn hook line**
> <one sentence using the primary keyword's vocabulary — LinkedIn distribution is engagement-driven, so this does more work than the hashtags>

---

## 6. Gaps and warnings

**Keywords the draft doesn't currently address**
- `<term>` (<score>, grade <g>) — <fill this gap, or consciously ignore it>

**Source failures and what they cost**
- <source> unavailable — <what's missing as a result>

**Manual overrides**
- <term moved up/down and why, or "none">

**Standing caveats**
- No search volume, difficulty, or CPC data in this report.
- Autocomplete results are locale-dependent (`<hl>/<gl>`) and change over time; this snapshot is dated <YYYY-MM-DD>.
- Medium and LinkedIn sections are inferred (grade D).

---

## 7. Source log

| Source | Tier | Status | Terms returned |
|---|---|---|---|
| Google Suggest | 2 — unofficial | ok / failed | <n> |
| Bing Autosuggest | 2 — unofficial | ok / failed | <n> |
| DuckDuckGo HTML | 2 — unofficial | ok / skipped | <n> |
| Datamuse | 1 — official API | ok / failed | <n> |
| Wikipedia OpenSearch | 1 — official API | ok / failed | <n> |
| Wikimedia Pageviews | 1 — official API | ok / failed | <n> |
| Stack Exchange | 1 — official API | ok / failed | <n> |
