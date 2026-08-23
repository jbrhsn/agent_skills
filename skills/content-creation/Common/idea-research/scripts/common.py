"""Shared helpers for idea-research fetchers. Standard library only, no auth."""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "idea-research-skill/1.0 (personal content research; contact: local user)"
RAW_DIR = Path(".idea-research/raw")
TIMEOUT = 20


def http_get(url, accept="application/json"):
    """GET a public URL. Returns decoded text, or raises."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": accept}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def warn(msg):
    print(f"  [warn] {msg}", file=sys.stderr)


def write_raw(source, items):
    """Write items to .idea-research/raw/<source>.json and report."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{source}.json"
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    degraded = sum(1 for i in items if i.get("degraded"))
    note = f" ({degraded} degraded)" if degraded else ""
    print(f"{source}: {len(items)} items -> {path}{note}")
    return path


def make_item(source, title, url, score=0, comments=0, created_utc=None,
              degraded=False):
    now = time.time()
    age = round((now - created_utc) / 3600.0, 2) if created_utc else None
    return {
        "source": source,
        "title": " ".join((title or "").split()),
        "url": url,
        "score": int(score or 0),
        "comments": int(comments or 0),
        "created_utc": int(created_utc) if created_utc else None,
        "age_hours": age,
        "degraded": bool(degraded),
    }


def load_beats(path="references/beats.md"):
    """Parse the beats table. Returns {beat: {keywords, subreddits, tags}}."""
    p = Path(path)
    if not p.exists():
        p = Path(__file__).resolve().parent.parent / "references" / "beats.md"
    beats = {}
    for line in p.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] in ("Beat", "") or set(cells[0]) <= {"-", ":"}:
            continue
        beats[cells[0]] = {
            "keywords": [k.strip().lower() for k in cells[1].split(",") if k.strip()],
            "subreddits": [s.strip() for s in cells[2].split(",") if s.strip()],
            "tags": [t.strip() for t in cells[3].split(",") if t.strip()],
        }
    if not beats:
        raise SystemExit("Could not parse references/beats.md — check the table format.")
    return beats


STOPWORDS = set("""a an the and or but if for of to in on at by with from as is are was
were be been being this that these those it its i you we they he she how what why when
where which who will can could should would do does did not no yes new your my our their
about into over after before more most just like get got make made use used using than
then them there here out up down off very s t re ve ll d m""".split())


def tokenize(text):
    words = re.findall(r"[a-z0-9][a-z0-9+.#-]*", (text or "").lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def strip_tags(html):
    return re.sub(r"<[^>]+>", " ", html or "")
