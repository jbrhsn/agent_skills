# idea-research

An opencode skill that generates **ranked, evidence-backed content ideas** for Medium,
LinkedIn, and Reddit — then scaffolds a `source.md` per approved idea, matching a
folder-per-article workflow.

It is built around one rule: **every idea must cite a live source.** Nothing is
invented from the model's memory, because that produces generic listicle bait rather
than timely angles.

---

## Constraints this skill was built under

| Constraint | How it's honoured |
|---|---|
| No authentication | Public endpoints only — no API keys, OAuth, logins, or MCP connectors. If a source ever goes auth-only, it gets dropped rather than worked around. |
| No surprise writes | Folders and `source.md` files are only created after explicit user confirmation. High score never equals consent. |
| uv as the runner | `setup_env.sh` checks for `uv` and creates a venv. If `uv` is missing, the agent must stop and ask before falling back to `python3`. |
| Optional keyword skill | If a keyword-research skill exists it widens the search terms. If not, the pipeline runs unchanged. Never a dependency. |
| Zero dependencies | All scripts are Python 3 standard library. Nothing to `pip install`. |

---

## Install

Drop the folder into your skills directory:

```
~/.config/opencode/skills/idea-research/
```

Then run from your writing project root (where `articles/` lives):

```bash
bash scripts/setup_env.sh
```

Requires Python 3.9+ and, preferably, [uv](https://docs.astral.sh/uv/).

---

## Layout

```
idea-research/
├── SKILL.md                     # lean — trigger + workflow, delegates detail
├── README.md
├── scripts/
│   ├── setup_env.sh             # uv check, venv creation, fallback gate
│   ├── common.py                # http, beat parsing, tokenising
│   ├── fetch_hn.py              # Hacker News (Algolia API)
│   ├── fetch_reddit.py          # public .json, RSS fallback
│   ├── fetch_trends.py          # Google Trends RSS
│   ├── fetch_medium_tags.py     # Medium tag RSS — saturation signal
│   ├── dedupe_and_score.py      # clustering + ranking
│   └── scaffold_article.py      # writes ONE source.md, refuses to overwrite
├── references/
│   ├── beats.md                 # your topics, subreddits, tags — edit this first
│   ├── sources.md               # endpoints, rate limits, failure modes
│   └── scoring.md               # the formula and what drives pickup
└── assets/
    └── source_template.md       # the source.md scaffold
```

Heavy logic lives in `scripts/`, heavy prose in `references/`. `SKILL.md` stays short
so it costs little context when it triggers.

---

## How it works

**1. Fetch.** Four fetchers write JSON into `.idea-research/raw/`. Any one can fail
without stopping the run — you're told which sources came back empty so you can judge
coverage.

**2. Expand (optional).** If a keyword-research skill is present, its terms widen the
match set. It returns terms only — no volume or competition metrics — so it is used
for query expansion, never for scoring.

**3. Cluster.** Titles are tokenised and grouped by shared significant tokens within a
beat, so the same story from HN and Reddit becomes one idea instead of two.

**4. Score.** Out of 100:

| Component | Max | Why |
|---|---|---|
| Recency | 30 | Half-life decay on the newest item in the cluster |
| Velocity | 30 | Engagement **per hour**, log-normalised, comments weighted 2× |
| Beat fit | 20 | Keyword match against `references/beats.md` |
| Curation gap | 20 | Agent-supplied after checking existing coverage |

**5. Verify the gap.** The scripts can't judge how well a topic is already covered, so
`gap_score` starts neutral and the agent checks `site:medium.com <topic>` and LinkedIn
for the top candidates, then re-runs with `--gap-overrides`.

**6. Present, confirm, scaffold.** You get a ranked table with a hook, angle, and
target platform per idea. You pick which ones to scaffold. Only then do files appear.

---

## Design decisions worth knowing

**Velocity, not volume.** Counting mentions finds topics that already peaked — by then
the good version exists and the window is shut. Rate of change finds topics still
climbing. 200 upvotes in 3 hours beats 200 upvotes in 3 days, and only the first is
worth your week.

**Medium is a saturation signal, not a trending one.** The Medium tag feed shows what
is *already published*. Heavy presence there is evidence against writing the obvious
version of a topic, so it subtracts from the gap score rather than adding to it.

**The best gap isn't the hottest topic.** It's a topic with a proven audience whose
best existing coverage is stale or shallow.

**A topic is not an idea.** The output includes a hook and an angle, because platform
research is clear that the title is what determines whether a piece is read — a Medium
click-through rate under 3% usually means the title failed, not the topic. Concrete
claims with numbers and named tools outperform vague curiosity hooks.

**Comments weighted double.** A thread generating argument is a better essay seed than
one generating silent upvotes.

---

## Usage

```bash
# once per project
bash scripts/setup_env.sh

# gather
uv run scripts/fetch_hn.py --days 7 --min-points 20
uv run scripts/fetch_reddit.py --window week
uv run scripts/fetch_trends.py --geo US
uv run scripts/fetch_medium_tags.py

# rank
uv run scripts/dedupe_and_score.py --top 15

# after checking coverage on the top candidates
uv run scripts/dedupe_and_score.py --top 15 --gap-overrides '{"idea-1": 19, "idea-2": 4}'

# after you approve specific ideas
uv run scripts/scaffold_article.py --id idea-1 --root articles/ \
  --platform Medium --hook "..." --angle "..."
```

Produces `articles/<slug>/source.md`, pre-filled with the evidence, the signal
breakdown, and prompts for the parts only you can write.

---

## Customising

Edit `references/beats.md` first — it's a plain markdown table of topics, keywords,
subreddits, and Medium tags, read at runtime by the fetchers and the scorer. Adding a
beat needs no code change.

Tune thresholds via `--min-score` (default 50) and `--gap-default` (default 10).

---

## Troubleshooting

**All sources return 0 items** — usually a network or proxy block. Endpoints are
public; try one in a browser. Corporate networks often block `reddit.com` and
`trends.google.com`.

**Reddit returns 403** — the fetcher automatically falls back to RSS, which has no
scores, so those items get zero velocity and are marked `degraded`. Not a failure,
just lower fidelity.

**`uv` not found** — the setup script exits with `STATUS: UV_MISSING` and the agent
must ask you before using `python3`. This is deliberate, not a bug.

**Nothing clears the threshold** — either your beats are too narrow for the week's
signal, or the lookback is too short. Try `--days 14` on the HN fetcher, or
`--min-score 40`.

**A source dies permanently** — add items by hand to `.idea-research/raw/manual.json`
using the schema in `references/sources.md`. The scorer treats them identically. Never
add a credential to fix a source.
