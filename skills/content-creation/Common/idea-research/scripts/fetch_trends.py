#!/usr/bin/env python3
"""Fetch Google Trends daily trending searches via the public RSS feed. No auth."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET

from common import http_get, make_item, warn, write_raw

RSS = "https://trends.google.com/trending/rss?geo={geo}"
NS = {"ht": "https://trends.google.com/trending/rss"}


def parse_traffic(text):
    """'20,000+' -> 20000. Used as a coarse score proxy only."""
    if not text:
        return 0
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--geo", default="US", help="region code, e.g. US, IN, GB")
    args = ap.parse_args()

    items = []
    try:
        root = ET.fromstring(http_get(RSS.format(geo=args.geo),
                                      accept="application/rss+xml"))
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            if not title:
                continue
            traffic = it.findtext("ht:approx_traffic", namespaces=NS)
            link = (it.findtext("link") or
                    f"https://trends.google.com/trends/explore?q={title}")
            # No reliable per-item timestamp: created_utc stays None, and the
            # scorer applies a neutral recency score.
            items.append(make_item("trends", title, link,
                                   score=parse_traffic(traffic), degraded=True))
    except Exception as exc:
        warn(f"Google Trends fetch failed: {exc}")
        warn("Pipeline continues without Trends.")

    write_raw("trends", items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
