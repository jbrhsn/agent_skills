# Output schema — kresearch.md

Field definitions for `assets/kresearch_template.md`. Fill every section; write "none found" rather than deleting a section, so a thin result is visible as a thin result instead of looking like an oversight.

## Front matter

| Field | Rules |
|---|---|
| `article` | Folder slug. Must match the directory containing `source.md`. |
| `generated` | ISO date of the run. Keyword data goes stale; an undated report gets trusted a year later. |
| `seed` | The exact seed string passed to the script, not a tidied version. Reproducibility. |
| `entities` | The `-e` values used. |
| `locale` | `hl`/`gl` used, e.g. `en/US`. Autocomplete is locale-dependent — omitting this makes results unreproducible. |
| `sources_ok` / `sources_failed` | From the run's stderr. Both required. |

## Thesis and angle

One sentence each, copied from Step 1 of `methodology.md`. Present so a reader six weeks later can tell whether the keyword set still matches the draft's direction.

## Primary keyword

| Field | Rules |
|---|---|
| Term | Exact phrase, lowercase. |
| Score / Grade | From `scored.tsv`. Never a grade the sources do not support. |
| Why | One line tying it to the draft's angle — why *this* article can win it. |
| Title candidates | 2–3 real titles containing the term naturally. Reject any where the keyword only fits as a bolted-on clause. |

## Alternate primaries

2–3 rows, same columns. These are subheading candidates and A/B title options.

## Long-tail keywords by intent

One table per cluster from `methodology.md` Step 5. Columns:

`term | score | grade | sources | suggested use`

- `sources` — comma-separated source names, so any row can be traced.
- `suggested use` — concrete: "H2 heading", "opening paragraph", "FAQ item". Vague entries like "mention somewhere" are not useful.

Omit clusters the draft does not serve. Do not pad.

## Topic interest signal

Only when Wikimedia Pageviews returned data. Give the article title queried, mean monthly views, and direction (rising / flat / falling) over the window.

Always include the caveat inline: this measures Wikipedia readership, not search volume, and is directional only.

If no entity had a Wikipedia article, write that. Absence is itself a signal — usually that the topic is too new or too niche for encyclopedic coverage, which is worth knowing.

## Real questions asked

From Stack Exchange, when the topic is technical. Give question titles and vote counts. These are literal phrasings from real people — the single best raw material for headings and for an FAQ block.

Paraphrase rather than copying titles verbatim where you can; these are other people's words.

## Native discovery (grade D — inferred)

Header must carry the grade-D marker. Include the one-line explanation that no public data source exists for Medium or LinkedIn, so the reason is visible at the point of use rather than buried in a footnote.

- **Medium tags** — exactly 5. One broad, three mid, one niche. Note which cluster each came from.
- **LinkedIn hashtags** — 3–5, in `#camelCase`.
- **Hook line** — one sentence for the LinkedIn post body, using the primary keyword's vocabulary. LinkedIn distribution is engagement-driven, not keyword-driven; the hook does more work than any hashtag.

## Gaps and warnings

The section that makes the report trustworthy. Include:

- Terms in the data the draft does **not** currently address — flagged as gaps to fill or to consciously ignore, not as an instruction to bolt on sections.
- Sources that failed and what that costs (e.g. "Stack Exchange unavailable — no real-question data, so heading phrasing is unvalidated").
- Any manual score override and its reason.
- The standing caveat: no search volume, difficulty, or CPC anywhere in this report.

## Source log

Table of every endpoint called: source, tier, status (ok / failed / skipped), terms returned. This is what makes the confidence grades auditable — without it the grades are just assertions.
