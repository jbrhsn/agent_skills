#!/usr/bin/env python3
"""Cluster raw signals into ideas and rank them.

Score = recency (30) + velocity (30) + beat fit (20) + curation gap (20).
See references/scoring.md for the rationale behind each component.
"""

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

from common import RAW_DIR, load_beats, tokenize

MEDIUM_SATURATION_PENALTY = 6  # per existing Medium post in the cluster, capped


def slugify(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].rstrip("-") or "idea"


def load_raw():
    if not RAW_DIR.exists():
        sys.exit("No .idea-research/raw/ directory — run the fetchers first.")
    items = []
    for path in sorted(RAW_DIR.glob("*.json")):
        try:
            items.extend(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  [warn] could not read {path}: {exc}", file=sys.stderr)
    if not items:
        sys.exit("All sources returned empty. Nothing to score — check network "
                 "or add items manually per references/sources.md.")
    return items


def match_beat(title, beats, extra_keywords):
    """Return (beat_name, hits). Extra keywords add a small widening bonus."""
    text = title.lower()
    best, best_hits = None, 0
    for name, cfg in beats.items():
        hits = sum(1 for kw in cfg["keywords"] if kw in text)
        if hits > best_hits:
            best, best_hits = name, hits
    if best and extra_keywords:
        if any(kw in text for kw in extra_keywords):
            best_hits += 1
    return best, best_hits


def beat_points(hits):
    if hits >= 3:
        return 20
    if hits == 2:
        return 14
    if hits == 1:
        return 8
    return 0


def recency_points(age_hours):
    if age_hours is None:
        return 12  # no timestamp available
    if age_hours <= 6:
        return 30
    if age_hours <= 24:
        return 24
    if age_hours <= 72:
        return 16
    if age_hours <= 168:
        return 8
    return 2


def velocity_points(items):
    """Engagement per hour, log-normalised, plus a cross-source bonus."""
    rate = 0.0
    for it in items:
        if it["source"] == "medium":
            continue  # saturation signal, not engagement
        age = max(it.get("age_hours") or 24.0, 1.0)
        rate += (it.get("score", 0) + 2 * it.get("comments", 0)) / age
    base = min(30.0, 10.0 * math.log10(1 + rate)) if rate > 0 else 0.0

    distinct = {it["source"] for it in items if it["source"] != "medium"}
    bonus = min(10, 5 * max(0, len(distinct) - 1))
    return round(min(30.0, base + bonus), 1)


def cluster(items, beats, extra_keywords, min_overlap=2):
    """Greedy clustering on shared significant tokens."""
    enriched = []
    for it in items:
        beat, hits = match_beat(it["title"], beats, extra_keywords)
        if not beat or hits == 0:
            continue  # off-beat, dropped
        enriched.append({**it, "beat": beat, "hits": hits,
                         "tokens": set(tokenize(it["title"]))})

    # Anchor on the strongest signals first so clusters form around real momentum.
    enriched.sort(key=lambda x: -(x.get("score", 0) + 2 * x.get("comments", 0)))

    clusters = []
    for it in enriched:
        placed = False
        for cl in clusters:
            if len(it["tokens"] & cl["tokens"]) >= min_overlap and \
                    it["beat"] == cl["beat"]:
                cl["items"].append(it)
                cl["tokens"] |= it["tokens"]
                placed = True
                break
        if not placed:
            clusters.append({"beat": it["beat"], "tokens": set(it["tokens"]),
                             "items": [it]})
    return clusters


def score_cluster(cl, gap_default):
    items = cl["items"]
    ages = [i["age_hours"] for i in items if i.get("age_hours") is not None]
    recency = recency_points(min(ages) if ages else None)
    velocity = velocity_points(items)
    beat = beat_points(max(i["hits"] for i in items))

    medium_hits = sum(1 for i in items if i["source"] == "medium")
    gap = gap_default - min(gap_default, MEDIUM_SATURATION_PENALTY * medium_hits)

    lead = max(items, key=lambda i: i.get("score", 0) + 2 * i.get("comments", 0))
    return {
        "title": lead["title"],
        "beat": cl["beat"],
        "score": round(recency + velocity + beat + gap, 1),
        "components": {"recency": recency, "velocity": velocity,
                       "beat_fit": beat, "gap": gap},
        "gap_checked": False,
        "sources": sorted({i["source"] for i in items}),
        "medium_posts_seen": medium_hits,
        "evidence": [
            {"source": i["source"], "title": i["title"], "url": i["url"],
             "score": i.get("score", 0), "comments": i.get("comments", 0),
             "age_hours": i.get("age_hours")}
            for i in sorted(items,
                            key=lambda x: -(x.get("score", 0) + 2 * x.get("comments", 0)))[:4]
        ],
    }


def load_overrides(raw):
    if not raw:
        return {}
    p = Path(raw)
    return json.loads(p.read_text() if p.exists() else raw)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--min-score", type=float, default=50.0)
    ap.add_argument("--keywords", help="optional keyword file (one term per line) "
                                       "from the keyword-research skill")
    ap.add_argument("--gap-overrides", help="JSON dict or path: {\"idea-3\": 19}")
    ap.add_argument("--gap-default", type=float, default=10.0)
    ap.add_argument("--out", default=".idea-research/scored.json")
    args = ap.parse_args()

    extra = []
    if args.keywords and Path(args.keywords).exists():
        extra = [l.strip().lower() for l in
                 Path(args.keywords).read_text().splitlines() if l.strip()]
        print(f"Keyword expansion active: {len(extra)} terms (terms only, no volume).")

    beats = load_beats()
    clusters = cluster(load_raw(), beats, extra)
    ideas = [score_cluster(c, args.gap_default) for c in clusters]
    ideas.sort(key=lambda x: -x["score"])

    for n, idea in enumerate(ideas, 1):
        idea["id"] = f"idea-{n}"
        idea["slug"] = slugify(idea["title"])

    overrides = load_overrides(args.gap_overrides)
    for idea in ideas:
        if idea["id"] in overrides:
            new_gap = float(overrides[idea["id"]])
            idea["score"] = round(idea["score"] - idea["components"]["gap"] + new_gap, 1)
            idea["components"]["gap"] = new_gap
            idea["gap_checked"] = True
    if overrides:
        ideas.sort(key=lambda x: -x["score"])

    shown = [i for i in ideas if i["score"] >= args.min_score][:args.top]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ideas, indent=2, ensure_ascii=False))

    print(f"\n{len(ideas)} ideas clustered, {len(shown)} above threshold "
          f"{args.min_score}\n")
    print(f"{'ID':<9}{'Score':>6}  {'Beat':<20}{'Sources':<20}Title")
    print("-" * 104)
    for i in shown:
        flag = "" if i["gap_checked"] else " *"
        srcs = ",".join(i["sources"])[:19]
        print(f"{i['id']:<9}{i['score']:>6}  {i['beat']:<20}"
              f"{srcs:<20}{i['title'][:44]}{flag}")
    print("\n* gap score not yet verified — check Medium/LinkedIn coverage and "
          "re-run with --gap-overrides (see references/scoring.md).")
    print(f"Full detail: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
