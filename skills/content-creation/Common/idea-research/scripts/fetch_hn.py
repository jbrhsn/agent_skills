#!/usr/bin/env python3
"""Fetch recent Hacker News stories via the free Algolia API. No auth required."""

import argparse
import json
import sys
import time

from common import http_get, make_item, warn, write_raw

API = ("https://hn.algolia.com/api/v1/search_by_date"
       "?tags=story&numericFilters=created_at_i>{since},points>{minpts}"
       "&hitsPerPage={n}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="lookback window (default 7)")
    ap.add_argument("--min-points", type=int, default=20)
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    since = int(time.time() - args.days * 86400)
    url = API.format(since=since, minpts=args.min_points, n=args.limit)

    items = []
    try:
        data = json.loads(http_get(url))
        for hit in data.get("hits", []):
            title = hit.get("title") or hit.get("story_title")
            if not title:
                continue
            link = hit.get("url") or (
                f"https://news.ycombinator.com/item?id={hit.get('objectID')}")
            items.append(make_item(
                "hn", title, link,
                score=hit.get("points"),
                comments=hit.get("num_comments"),
                created_utc=hit.get("created_at_i"),
            ))
    except Exception as exc:
        warn(f"Hacker News fetch failed: {exc}")
        warn("Pipeline continues without HN. Check network or retry later.")

    write_raw("hn", items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
