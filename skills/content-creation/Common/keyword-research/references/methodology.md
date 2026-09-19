# Keyword methodology

Start with what the reader needs and what the article actually delivers. Identify thesis, audience, angle, useful seeds/entities, language, and target region. For a topic-only request, identify proposed coverage and label it provisional.

Choose seed phrases that represent the task without being unnecessarily broad. Ask about materially different directions; otherwise use a stated assumption or investigate alternatives. Do not equate absent autocomplete with absent demand.

Select sources from [endpoint guidance](endpoints.md). Prefer bounded useful queries over automatic alphabet expansion. The optional helper supports `suggest`, `related`, `entity`, `questions`, `all`, and `score`; pass `--dry-run` to preview without network calls or file writes.

Keep raw TSV and diagnostics in a run-specific directory when helpful. Record query, date, country/language, site, and expansion options; not every endpoint supports localization. Wikipedia/pageviews are English and Datamuse is used with its default vocabulary regardless of the autocomplete locale flags.

Cluster terms by intent: explanation, procedure, comparison, troubleshooting, or evaluation. Inspect representative public results when available to understand the expected answer format and competing coverage; do not infer difficulty from autocomplete.

Choose primary and supporting phrases by fit, natural usage, and evidence. An inferred phrase can be the best choice for an emerging topic if labeled. Avoid quotas for long-tail terms, headings, or tags. Suggest concrete placements without requiring every variant to appear.

Separate search phrasing, entity/interest observations, and platform metadata recommendations. Do not turn Wikipedia readership into Google searches or community votes into traffic forecasts. See [scoring](scoring.md) for the helper's provenance grades.

Deliver actionable recommendations, evidence limitations, and source coverage. Keep audit artifacts if useful; do not delete unrelated files named raw.tsv or scored.tsv.
