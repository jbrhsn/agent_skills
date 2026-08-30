# Scoring

## Contents

- [The formula](#the-formula)
- [Why velocity, not volume](#why-velocity-not-volume)
- [The curation gap](#the-curation-gap)
- [Thresholds](#thresholds)
- [Applying gap overrides](#applying-gap-overrides)
- [What actually drives pickup](#what-actually-drives-pickup)
- [Platform routing](#platform-routing)

## The formula

Each clustered idea scores out of 100:

| Component | Max | Source |
|---|---|---|
| Recency | 30 | Age of the newest item in the cluster |
| Velocity | 30 | Engagement per hour, log-normalized |
| Beat fit | 20 | Keyword match, see `beats.md` |
| Curation gap | 20 | Agent-supplied, defaults to neutral 10 |

**Recency** decays by half-life: 0–6h = 30, 6–24h = 24, 1–3d = 16, 3–7d = 8, >7d = 2. Items with no timestamp get 12.

**Velocity** = `(score + 2 × comments) / max(age_hours, 1)`, then `min(30, 10 × log10(1 + rate) )`. Comments are weighted double — a post generating argument is a better essay seed than one generating silent upvotes. Sources without engagement data score 0 here and must earn their rank elsewhere.

**Cross-source bonus**: +5 per additional distinct source in a cluster, capped at +10, folded into the velocity component. A topic appearing on both HN and Reddit within a few days is a much stronger signal than one appearing twice on the same site.

## Why velocity, not volume

Raw mention counts identify topics that have *already* peaked. By the time a topic is everywhere, the good version has been written and the algorithmic window is closed. Rate of change identifies topics that are still climbing — 200 upvotes in 3 hours beats 200 upvotes in 3 days, and only the first is worth writing about this week.

This is the single most important difference between this skill and a generic "what's trending" search.

## The curation gap

The scripts cannot see how well a topic is already covered — that requires judgment. So `gap_score` defaults to a neutral 10 and the **agent must adjust it** for the top candidates before presenting results.

Check `site:medium.com <topic>` plus LinkedIn, then score:

| Situation | Gap score |
|---|---|
| Large audience, best existing piece is 3+ months old | 18–20 |
| Actively discussed elsewhere, thin on Medium/LinkedIn | 14–17 |
| Unknown / not yet checked | 10 (default) |
| Several solid recent pieces exist | 4–8 — needs a differentiated angle |
| Saturated in the last two weeks | 0–3 — drop it |

The best opportunity is not the hottest topic. It is a topic with a proven audience whose best available coverage is stale or shallow.

## Thresholds

- **< 50** — dropped, not shown
- **50–64** — shown as a backlog idea
- **65–79** — solid, worth writing
- **80+** — lead with it

Thresholds gate *presentation only*. They never authorize creating files. Scaffolding always requires explicit user approval regardless of score.

## Applying gap overrides

```bash
uv run scripts/dedupe_and_score.py --top 15 --gap-overrides '{"idea-3": 19, "idea-7": 4}'
```

Or pass a JSON file path. Re-run after research; the raw fetch is not repeated.

## What actually drives pickup

Findings from 2026 platform research — these shape the *hook*, not the score:

- **Medium's algorithm weights read ratio, completion, and click-through.** A CTR under 3% signals an unclear title; 7–10% is the target band. When a piece fails, the title is usually the cause, not the topic.
- **Specific, concrete claims beat vague curiosity hooks.** Use numbers, named tools, named people, verifiable outcomes. "I replaced Airflow with DuckDB and cut our bill 73%" beats "Rethinking modern data pipelines".
- **Timeliness is itself a ranking signal.** A current news anchor in the first paragraph helps; so do named, checkable specifics that build trust early.
- **Volume strategies are actively suppressed.** Fewer, deeper, harder pieces outperform daily posting. Medium favors 1,200–3,000 words with H2 breaks every 300–500 words and short paragraphs.
- **Generic AI-sounding content is deprioritized.** First-hand experience, specific detail, and a human voice are what clear curation.
- **Stories outperform listicles for sharing.** The share impulse is emotional ("I need to send this to someone"), not informational.

## Platform routing

| Platform | Fits | Shape |
|---|---|---|
| Medium | Depth, narrative, a real result to report | 1,200–3,000 words, concrete title, story arc |
| LinkedIn | Niche professional angle, contrarian take, career-relevant lesson | Short, conversation-starting, first-hour engagement matters |
| Reddit | Genuine question, tool comparison, community-relevant finding | Community-first, no self-promotion, expect scrutiny |

One idea can route to several — a Medium piece with a LinkedIn teaser is the common pairing. Say which is primary.
