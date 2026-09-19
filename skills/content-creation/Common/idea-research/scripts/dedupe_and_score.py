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
import time
from pathlib import Path

from common import RAW_DIR, load_beats, tokenize


def slugify(text, maxlen=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].rstrip("-") or "idea"


def load_raw():
    if not RAW_DIR.exists():
        sys.exit("No .idea-research/raw/ directory — run the fetchers first.")
    items = []
    seen = set()
    now = time.time()
    for path in sorted(RAW_DIR.glob("*.json")):
        try:
            records = json.loads(path.read_text())
            if not isinstance(records, list):
                raise ValueError("expected a JSON array")
            for record in records:
                if not isinstance(record, dict) or not all(
                    isinstance(record.get(key), str) and record[key].strip()
                    for key in ("source", "title", "url")
                ):
                    print(f"  [warn] skipping invalid item in {path}", file=sys.stderr)
                    continue
                key = (record["source"], record["url"])
                if key in seen:
                    continue
                try:
                    timestamp = record.get("created_utc")
                    age = max(0.0, (now - float(timestamp)) / 3600) if timestamp is not None else None
                    score = max(0, int(record.get("score") or 0))
                    comments = max(0, int(record.get("comments") or 0))
                    if timestamp is not None and not math.isfinite(float(timestamp)):
                        raise ValueError("non-finite timestamp")
                except (TypeError, ValueError, OverflowError):
                    print(f"  [warn] skipping invalid metrics in {path}", file=sys.stderr)
                    continue
                seen.add(key)
                items.append({**record, "age_hours": age, "score": score,
                              "comments": comments})
        except (ValueError, OSError) as exc:
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
        hits = sum(1 for kw in cfg["keywords"]
                   if re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", text))
        if hits > best_hits:
            best, best_hits = name, hits
    if best and extra_keywords:
        if any(re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", text)
               for kw in extra_keywords):
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
        if it["source"] not in {"hn", "reddit"} or it.get("age_hours") is None:
            continue  # traffic estimates and unknown-age counts are not velocity
        age = max(it["age_hours"], 1.0)
        rate += (it.get("score", 0) + 2 * it.get("comments", 0)) / age
    base = min(30.0, 10.0 * math.log10(1 + rate)) if rate > 0 else 0.0

    distinct = {it["source"] for it in items if it["source"] in {"hn", "reddit"}
                and it.get("age_hours") is not None
                and (it.get("score", 0) or it.get("comments", 0))}
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
    gap = gap_default  # feed presence alone does not establish coverage quality

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
    ap.add_argument("--beats", help="project-specific beats table; defaults to bundled beats")
    ap.add_argument("--dry-run", action="store_true", help="preview ranking without writing")
    args = ap.parse_args()
    if not 0 <= args.gap_default <= 20 or args.top < 1:
        ap.error("--gap-default must be 0..20 and --top must be positive")

    extra = []
    if args.keywords and Path(args.keywords).exists():
        extra = [l.strip().lower() for l in
                 Path(args.keywords).read_text().splitlines() if l.strip()]
        print(f"Keyword expansion active: {len(extra)} terms (terms only, no volume).")

    beats = load_beats(args.beats) if args.beats else load_beats()
    clusters = cluster(load_raw(), beats, extra)
    ideas = [score_cluster(c, args.gap_default) for c in clusters]
    ideas.sort(key=lambda x: -x["score"])

    for n, idea in enumerate(ideas, 1):
        idea["id"] = f"idea-{n}"
        idea["slug"] = slugify(idea["title"])

    overrides = load_overrides(args.gap_overrides)
    if not isinstance(overrides, dict):
        ap.error("--gap-overrides must be an object mapping idea IDs to 0..20")
    try:
        overrides = {key: float(value) for key, value in overrides.items()}
    except (TypeError, ValueError):
        ap.error("gap overrides must be numeric")
    if any(not 0 <= value <= 20 for value in overrides.values()):
        ap.error("gap overrides must be in 0..20")
    unknown = set(overrides) - {idea["id"] for idea in ideas}
    if unknown:
        ap.error(f"unknown idea IDs: {', '.join(sorted(unknown))}")
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
    if not args.dry_run:
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
    print("\n* gap judgment not supplied — inspect relevant coverage and "
          "re-run with --gap-overrides (see references/scoring.md).")
    print(f"{'Would write' if args.dry_run else 'Full detail'}: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
