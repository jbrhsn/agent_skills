# Scoring and confidence

## What this score is not

It is **not search volume, not keyword difficulty, not CPC, and not a traffic
estimate.** None of the sources in this stack expose any of those. Anyone who
needs real volume needs Google Ads, Ahrefs, Semrush, or similar.

It is a **relative ranking heuristic**: given a pile of candidate phrases from
free sources, which ones look most worth writing a section about. Comparable
within one run, meaningless across runs or against any commercial tool's numbers.

State this in the report. A bare number in a table gets read as volume by default,
and that misreading is the main way this skill can do harm.

## The formula

```
score = 45 × (breadth / max_breadth)     # corroboration across sources
      + 30 × position_value               # autocomplete rank
      + 25 × specificity                  # long-tail shape
```

Rounded to an integer, 0–100.

**breadth** — how many distinct sources produced this term. A phrase surfacing in
Google Suggest, Bing, and Datamuse is far more trustworthy than one seen once.
This is the heaviest weight because corroboration is the only real defence
against noise when no source is authoritative.

**position_value** — best autocomplete rank across Tier 2 sources:
`(11 − rank) / 10` for ranks 1–10, else `0.3`. Autocomplete ordering reflects
Google's own popularity signal — the closest thing to demand data available here.
Terms with no autocomplete rank get the 0.3 floor rather than zero, since absence
is weak evidence, not evidence of absence.

**specificity** — word count as a proxy for long-tail shape: 3–7 words scores
`1.0`, 2 words `0.6`, anything else `0.3`. Three-to-seven-word phrases are where
a new article realistically competes; single words are dominated by established
domains.

### Deliberate limitations

- No commercial-intent weighting. Nothing free distinguishes buyer intent.
- No competition estimate. That needs SERP data this stack does not have.
- Word count is a crude specificity proxy and will misjudge compound terms.
- Breadth rewards phrasings common to several autocomplete systems, which mildly
  biases toward mainstream wording over emerging jargon. For genuinely new topics,
  expect low scores across the board and lean on judgement instead.

Adjust the ranking by hand where the draft's angle justifies it. Note any manual
override in the report so it is visible later.

## Confidence grades

Every row in `kresearch.md` carries one. This is the mechanism that keeps
inference from being read as measurement.

| Grade | Meaning | Earned when |
|---|---|---|
| **A** | Measured, corroborated | Appears in 2+ sources including at least one Tier 1 official API, **or** backed by a real Wikimedia pageview count |
| **B** | Measured, single source | One Tier 1 official API only (Datamuse, Wikipedia, Stack Exchange) |
| **C** | Observed, unofficial | Tier 2 autocomplete only (Google, Bing, DuckDuckGo) — real observed behaviour, undocumented and unguaranteed source |
| **D** | Inferred | Produced by reasoning over the clusters with no data behind it. All Medium tags and LinkedIn hashtags are D. |

Grade C is the *typical* case for good long-tail keywords, not a failure state.
Most of what makes this report useful will be C.

Grade D is legitimate and often the most actionable content in the report — it is
just not evidence. Label it and let the user weigh it.

## Reading the output

- **Score above ~70 with grade A or B** — strong candidate for primary keyword.
- **Score 40–70 with grade C** — the long-tail workhorses. Use as section
  headings. This is where most of the value sits.
- **Below 40** — usually noise, one-off autocomplete artefacts, or terms too
  broad to win. Skim for anything the draft uniquely answers, then discard.
- **High breadth but low position** — widely recognised phrasing that no engine
  suggests prominently. Often a good subheading, rarely a good title.
- **Everything scoring low** — usually means the seed was too narrow or too new.
  Go back to Step 1 rather than shipping a weak report.
