---
name: keyword-research
description: Run keyless keyword research for a drafted article and write a kresearch.md next to its source.md. Use this whenever the user mentions keyword research, SEO keywords, search intent, long-tail keywords, article tags, Medium tags, LinkedIn hashtags, "what should I title this", "how do I make this rank", or asks to optimize a draft for discovery — even if they never say the words "keyword research". Also use it whenever a source.md exists in an article folder and the user asks what to do next. Requires no API key, no login, no paid tool.
---

# Keyword Research (keyless)

Turns a rough draft (`source.md`) into a ranked, source-labelled keyword report
(`kresearch.md`) in the same folder, using only free public APIs and undocumented
public autocomplete endpoints.

## Folder contract

```
articles/<article-slug>/
├── source.md      # input — the rough draft (required)
└── kresearch.md   # output — written by this skill
```

Never write `kresearch.md` anywhere except beside the `source.md` it was derived
from. If no `source.md` exists, stop and ask for one — this skill researches a
specific draft, not a bare topic, and guessing the angle produces generic output.

## Prerequisites

`curl` and `jq` must be on PATH. Check with `command -v curl jq`. If `jq` is
missing, say so and stop rather than parsing JSON by hand.

## Workflow

**1. Read `source.md`.** Extract, and write down before doing anything else:
- the working thesis in one sentence
- one **seed term** (2–4 words, the phrase a reader would actually type)
- 3–6 **entities** (named tools, models, frameworks, concepts the draft leans on)
- the **reader** (who is searching for this and what they already know)

Do not skip this. Every downstream query is derived from these, and a vague seed
produces a report full of terms the article can't credibly rank for.

**2. Confirm the seed with the user** if the draft is broad or covers several
topics. One clarifying question here saves a full useless run.

**3. Fetch.** Read `references/endpoints.md` first — it documents each endpoint's
parameters, response shape, and known failure modes. Then run:

```bash
scripts/kwfetch.sh all "<seed>" -e "<entity1>" -e "<entity2>" -o raw.tsv
scripts/kwfetch.sh score raw.tsv > scored.tsv
```

The script degrades gracefully: any endpoint that fails is skipped and reported on
stderr. A partial run is fine and normal — record which sources answered, because
the confidence grades in the report depend on it.

**4. Cluster and grade.** Read `references/methodology.md` for the clustering
procedure and `references/scoring.md` for what the numeric score does and does not
mean. The script's score is a heuristic ranking, not search volume — never present
it as volume.

**5. Write the report.** Copy `assets/kresearch_template.md` into the article
folder as `kresearch.md` and fill every section. Read
`references/output-schema.md` for what each field must contain.

## Non-negotiables

These exist because a keyword report that overstates its own certainty is worse
than no report — it gets acted on.

- **Label every claim with a confidence grade** (A–D, defined in
  `references/scoring.md`). No unlabelled rows.
- **Never invent a search volume, difficulty score, or CPC.** None of these
  sources provide them. If the user wants real volume, tell them plainly that it
  requires a paid tool or a Google Ads account.
- **Never present Medium tags or LinkedIn hashtags as measured.** No public data
  source exists for either platform. They are inferred from the keyword clusters
  and must be marked grade D.
- **Report dead or blocked sources honestly** in the Source log. Silence about a
  403 makes the report look better-sourced than it is.
