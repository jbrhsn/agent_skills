#!/usr/bin/env python3
"""Fetch top posts from public subreddits. No OAuth — public .json, RSS fallback."""

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from calendar import timegm

from common import http_get, load_beats, make_item, strip_tags, warn, write_raw

JSON_URL = "https://www.reddit.com/r/{sub}/top.json?t={window}&limit={n}"
RSS_URL = "https://www.reddit.com/r/{sub}/.rss"
ATOM = "{http://www.w3.org/2005/Atom}"


def from_json(sub, window, limit):
    data = json.loads(http_get(JSON_URL.format(sub=sub, window=window, n=limit)))
    out = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        if d.get("stickied"):
            continue
        out.append(make_item(
            "reddit", d.get("title"),
            "https://www.reddit.com" + d.get("permalink", ""),
            score=d.get("score"), comments=d.get("num_comments"),
            created_utc=d.get("created_utc"),
        ))
    return out


def from_rss(sub):
    """Lower-fidelity fallback: no scores available."""
    root = ET.fromstring(http_get(RSS_URL.format(sub=sub), accept="application/atom+xml"))
    out = []
    for entry in root.findall(f"{ATOM}entry"):
        title = (entry.findtext(f"{ATOM}title") or "").strip()
        link_el = entry.find(f"{ATOM}link")
        link = link_el.get("href") if link_el is not None else ""
        updated = entry.findtext(f"{ATOM}updated")
        ts = None
        if updated:
            try:
                ts = timegm(time.strptime(updated[:19], "%Y-%m-%dT%H:%M:%S"))
            except ValueError:
                ts = None
        out.append(make_item("reddit", title, link, created_utc=ts, degraded=True))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--window", default="week", choices=["day", "week", "month"])
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--subs", help="comma-separated override; default = all beats")
    args = ap.parse_args()

    if args.subs:
        subs = [s.strip() for s in args.subs.split(",") if s.strip()]
    else:
        subs = sorted({s for b in load_beats().values() for s in b["subreddits"]})

    items, failed = [], []
    for sub in subs:
        try:
            items.extend(from_json(sub, args.window, args.limit))
        except Exception as exc:
            warn(f"r/{sub}: JSON endpoint failed ({exc}); trying RSS")
            try:
                items.extend(from_rss(sub))
            except Exception as exc2:
                warn(f"r/{sub}: RSS also failed ({exc2}); skipping")
                failed.append(sub)
        time.sleep(1.5)  # be a good citizen; unauthenticated limits are tight

    if failed:
        warn(f"Skipped subreddits: {', '.join(failed)}")
    write_raw("reddit", items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
