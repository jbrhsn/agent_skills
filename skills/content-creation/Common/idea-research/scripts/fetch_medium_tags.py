#!/usr/bin/env python3
"""Fetch recent Medium posts per tag via public RSS. No auth.

This is a SATURATION signal, not a trending signal: it shows what is already
being published, which feeds the curation-gap check in scoring.md.
"""

import argparse
import sys
import time
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from common import http_get, load_beats, make_item, warn, write_raw

RSS = "https://medium.com/feed/tag/{tag}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tags", help="comma-separated override; default = all beats")
    args = ap.parse_args()

    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    else:
        tags = sorted({t for b in load_beats().values() for t in b["tags"]})

    items, failed = [], []
    for tag in tags:
        try:
            root = ET.fromstring(http_get(RSS.format(tag=tag),
                                          accept="application/rss+xml"))
            for it in root.iter("item"):
                title = (it.findtext("title") or "").strip()
                if not title:
                    continue
                ts = None
                pub = it.findtext("pubDate")
                if pub:
                    try:
                        ts = int(parsedate_to_datetime(pub).timestamp())
                    except (TypeError, ValueError):
                        ts = None
                items.append(make_item("medium", title,
                                       (it.findtext("link") or "").strip(),
                                       created_utc=ts, degraded=True))
        except Exception as exc:
            warn(f"tag '{tag}' failed ({exc}); skipping")
            failed.append(tag)
        time.sleep(1.0)

    if failed:
        warn(f"Skipped tags: {', '.join(failed)}")
    write_raw("medium", items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
