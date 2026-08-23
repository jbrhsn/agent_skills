# Methodology

The pipeline in order. Steps 1–2 are judgement, 3 is mechanical, 4–7 are
judgement again. The mechanical step is the smallest part — the value is in
choosing the right seed and in reading the output honestly.

## Step 1 — Extract intent from source.md

Read the whole draft, not just the title. Produce:

| Field | What good looks like |
|---|---|
| Thesis | One sentence. "Agent harnesses fail on long tasks because context is managed as a buffer, not a budget." |
| Seed term | 2–4 words a reader would type. "agent context management" |
| Entities | Proper nouns the draft relies on. "Claude Code", "MCP", "RAG" |
| Reader | "Mid-level engineers already building with LLM APIs" |
| Angle | What this draft says that the top results don't |

The angle matters most and is the easiest to skip. A keyword the article cannot
answer better than page one is not an opportunity, it is a distraction.

**Bad seed:** "AI" — too broad, nothing rankable.
**Bad seed:** "why my opencode harness kept dropping tool results in month three" — too
specific, no search demand, autocomplete returns nothing.
**Good seed:** "opencode agent harness" — specific enough to be about something,
broad enough that people search it.

## Step 2 — Confirm before spending calls

If the draft supports two plausible seeds, ask. A run against the wrong seed
produces a plausible-looking report aimed at the wrong article, which is more
expensive to detect than to prevent.

## Step 3 — Fetch

```bash
scripts/kwfetch.sh all "<seed>" -e "<entity>" -e "<entity>" -o raw.tsv
```

Useful flags: `--deep` adds the a–z expansion (26 extra Google calls, slower,
better long-tail); `--ddg` enables DuckDuckGo related searches; `--se-site` picks
a different Stack Exchange site; `--gl`/`--hl` set target country and language.

Output is TSV: `source <TAB> term <TAB> rank_or_score`.

Note on stderr as you go. Which sources answered determines the confidence grades,
and you cannot reconstruct it afterwards from the TSV alone.

## Step 4 — Score

```bash
scripts/kwfetch.sh score raw.tsv > scored.tsv
```

Output columns: `term, score, breadth, best_rank, words, grade, sources`.

Read `scoring.md` before interpreting any of it.

## Step 5 — Cluster by intent

Group the scored terms into these buckets. Cluster by what the searcher wants,
not by shared words — "X vs Y" and "is X better than Y" belong together even
though they share one token.

| Cluster | Signals | What the article owes them |
|---|---|---|
| **Informational** | "what is", "how does", "explained", bare nouns | A definition early, before the opinion |
| **How-to / procedural** | "how to", "setup", "tutorial", "step by step" | Concrete runnable steps |
| **Comparison** | "vs", "alternative", "better than", "or" | An actual verdict, not a table with no conclusion |
| **Troubleshooting** | "not working", "error", "fix", "why does" | The specific failure named in the text |
| **Evaluative** | "best", "worth it", "review", "should I" | A recommendation with stated conditions |

Drop clusters the draft does not serve. A report listing keywords the article
does not address invites writing filler sections to chase them, which makes the
article worse.

## Step 6 — Pick the primary keyword

Choose one, from the top of the scored list, subject to all three:

1. **The draft already answers it.** Not "could be made to."
2. **It survives in the title naturally.** If it only fits as a keyword-stuffed
   clause, it is the wrong primary.
3. **Grade C or better**, ideally appearing in both Google and Bing suggest.

Then pick 2–3 alternates for subheadings, and 5–15 long-tail terms as section
headings. Long-tail is where a new post actually wins; the primary is mostly a
title and framing decision.

## Step 7 — Separate the two output sections

The report has two halves that must not be blended, because they rest on
completely different evidence.

**SEO / Google** — built on measured autocomplete, Datamuse, Wikipedia,
Stack Exchange data. Grades A–C. Applies to both Medium and LinkedIn articles,
since both get indexed.

**Native discovery** — Medium tags and LinkedIn hashtags. No public data source
exists for either platform (see `endpoints.md` §8). These are **inferred from the
Step 5 clusters** and are always grade D. Say so in the section header, not just
in a footnote. Practical guidance that does not require data:

- Medium allows 5 tags. Mix one broad, three mid, one niche.
- LinkedIn hashtags: 3–5 is the working consensus; more reads as spam.
- Prefer tags that match phrases already in the draft's own vocabulary.

## Step 8 — Write kresearch.md

Copy `assets/kresearch_template.md` into the article folder and fill it. Complete
the Source log honestly, including anything that failed. Then delete `raw.tsv`
and `scored.tsv` unless the user asked to keep them — they are intermediate
artefacts and clutter the article folder.
