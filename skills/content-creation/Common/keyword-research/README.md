# keyword-research

Keyless keyword research for article drafts. Reads a `source.md`, writes a
`kresearch.md` beside it. No API key, no login, no paid tool, no signup.

Built for a folder-per-article workflow in an agent harness (opencode, Claude
Code, or similar), where the draft comes first and the keyword work follows it —
rather than the other way round.

```
articles/agent-context-budgets/
├── source.md      # you write this
└── kresearch.md   # the skill writes this
```

## Install

Drop the folder wherever your harness looks for skills:

```bash
unzip keyword-research.zip -d ~/.config/opencode/skills/
chmod +x ~/.config/opencode/skills/keyword-research/scripts/kwfetch.sh
```

Requires `curl` and `jq` on PATH. Nothing else.

```bash
# macOS
brew install jq
# Debian/Ubuntu
sudo apt-get install jq
```

## Use

Write your draft, then ask the agent for keyword research on it. The skill is
described to trigger on the obvious phrasings and on several non-obvious ones
("what should I title this", "how do I make this rank"), so you shouldn't need to
name it.

You can also run the script directly:

```bash
cd articles/agent-context-budgets

# full harvest
../../skills/keyword-research/scripts/kwfetch.sh all "agent context management" \
    -e "Claude Code" -e "MCP" -o raw.tsv

# rank it
../../skills/keyword-research/scripts/kwfetch.sh score raw.tsv > scored.tsv
```

Single-source lookups, for when you just want one thing:

```bash
kwfetch.sh suggest   "agent harness"   # Google + Bing autocomplete
kwfetch.sh related   "agent harness"   # Datamuse semantic + co-occurring
kwfetch.sh entity    "software agent"  # Wikipedia titles + real pageview counts
kwfetch.sh questions "agent harness"   # Stack Exchange, real questions + votes
```

### Flags

| Flag | Effect |
|---|---|
| `-e <entity>` | Add an entity to expand (repeatable) |
| `-o <file>` | Write TSV to file instead of stdout |
| `--deep` | Add a–z expansion — 26 extra Google calls, slower, better long-tail |
| `--ddg` | Enable DuckDuckGo related searches (off by default; fragile) |
| `--gl` / `--hl` | Target country / language, e.g. `--gl GB --hl en` |
| `--se-site` | Stack Exchange site, e.g. `--se-site datascience` |

Environment: `KW_UA` sets the User-Agent (**set this** — Wikimedia asks for
contact info and returns 403 for generic agents). `KW_SLEEP` sets the delay
between autocomplete calls, default `0.4`.

## Where the data comes from

Two tiers, and the distinction drives the confidence grades in the report.

**Tier 1 — official, documented, keyless APIs**

| Source | Gives you |
|---|---|
| Datamuse | Semantically related and statistically co-occurring terms |
| Wikipedia OpenSearch | Canonical entity names, disambiguation |
| Wikimedia Pageviews | **Real** monthly view counts and trend direction |
| Stack Exchange | Real question phrasings with vote counts |

**Tier 2 — undocumented public endpoints**

Google Suggest, Bing Autosuggest, DuckDuckGo HTML. These work today and have for
years, but nobody documents or guarantees them. They're the best available signal
for how people actually phrase queries — and they can break without notice. The
script skips any that fail and says so.

Full parameter and response-shape details are in `references/endpoints.md`.

## What this does not do

Stated plainly, because a keyword report that overstates its certainty is worse
than no report — it gets acted on.

- **No search volume. No keyword difficulty. No CPC.** None of these sources
  expose them. Real volume needs Google Ads, Ahrefs, Semrush, or equivalent. The
  score in the report is a relative ranking heuristic, comparable only within a
  single run — never across runs or against a commercial tool's numbers.
- **No Reddit.** Reddit shut off unauthenticated `.json` access on 2026-05-28;
  those endpoints now return 403. Pushshift is gone too. There is no free
  replacement, so it was cut rather than left in as a broken fallback.
- **No real Medium or LinkedIn data.** Neither exposes a keyless API for tag or
  hashtag popularity. Tags and hashtags in the report are *inferred* from the
  keyword clusters, always marked grade D, and flagged as such in the section
  header rather than a footnote.
- **No Google SERP or People Also Ask scraping.** JavaScript-rendered,
  CAPTCHA-gated, against Google's terms, and breaks constantly.
- **No Google Trends.** The unofficial endpoints need a session-token flow that
  fails often enough to be worse than nothing.

## Confidence grades

Every row in the output carries one:

| Grade | Meaning |
|---|---|
| **A** | Measured and corroborated — 2+ sources incl. a Tier 1 API, or a real pageview count |
| **B** | Measured, single Tier 1 source |
| **C** | Observed via unofficial autocomplete only |
| **D** | Inferred by the model, no data behind it |

**Grade C is the normal case for good long-tail keywords, not a failure.** Most
of the useful output will be C. Grade D is often the most actionable content in
the report — it just isn't evidence.

## Known expiry

**Datamuse requires an API key from 2027-01-01.** Still free, but the keyless
path ends. If Datamuse calls start returning 401 after that date, that's why —
request a key at datamuse.com rather than debugging the script.

Tier 2 endpoints can break any day. That's inherent to using them, and the reason
the script treats every source as optional.

## Layout

```
keyword-research/
├── SKILL.md                      # lean — orchestration and rules only
├── README.md                     # this file
├── references/                   # loaded on demand, keeps SKILL.md small
│   ├── endpoints.md              # URLs, params, response shapes, dead sources
│   ├── methodology.md            # the 8-step pipeline
│   ├── scoring.md                # formula, limitations, grade definitions
│   └── output-schema.md          # field-by-field spec for kresearch.md
├── scripts/
│   └── kwfetch.sh                # all fetching and scoring
└── assets/
    └── kresearch_template.md     # the report template
```

The split is deliberate: `SKILL.md` stays around 80 lines so it costs little when
loaded, and the reference files are pulled in only at the step that needs them.
`scripts/` rather than `assets/` for the executable follows the usual skill
convention — `assets/` holds things that end up in the output, `scripts/` holds
things that run.

## Be a good citizen

The script rate-limits itself and identifies itself. Don't remove either. Set
`KW_UA` to something with real contact info; Wikimedia in particular asks for it,
and the Tier 2 endpoints stay usable for everyone only while nobody hammers them.
