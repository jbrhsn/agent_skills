# Scoring and provenance

The helper emits a relative ordering within one candidate set, not search volume, keyword difficulty, CPC, probability of ranking, or forecast traffic. More sources do not make an irrelevant term useful.

## Formula

Score = 45 × source breadth / maximum breadth + 30 × position value + 25 × phrase-shape value, rounded to an integer.

Position value is (11 − rank) / 10 for autocomplete ranks 1–10; otherwise 0.3. Phrase-shape value is 1 for 3–7 whitespace-separated words, 0.6 for two, otherwise 0.3. These are arbitrary prioritization heuristics, not calibrated demand estimates. Source breadth counts distinct raw source labels and can overweight related services.

Autocomplete position is an observed suggestion order, not a search-frequency rank. Phrase length misses many languages and compound concepts; low-scoring terms may best fit a new or specialist topic.

## Provenance grades

The output column remains `grade` for compatibility. Interpret it as provenance only:

| Grade | Meaning |
|---|---|
| A | Observed in multiple source families including a documented API |
| B | Observed in a documented API family only |
| C | Observed only through unofficial suggestion/search endpoints |
| D | Inferred or supplied by an unclassified source; inspect provenance manually |

Wikipedia titles and Wikimedia pageviews count as one family for grading. Pageviews alone earn B, not corroboration. Grades describe where a phrase appeared, not factual correctness or confidence that it will rank.

Datamuse gives lexical associations, Wikipedia gives entities/readership, Stack Exchange gives questions/votes, and autocomplete gives candidate phrasing. None of these observations measures demand for the exact article. Keep pageview metrics separate and identify article, window, and access filters.

Platform tags/hashtags are editorial suggestions unless supported by a specifically identified measurement source; label inference explicitly. Do not require inferred suggestions to earn a measured grade.

Document editorial overrides by reader fit, intent, evidence, and actual article coverage. A high score is not a reason to add filler.
