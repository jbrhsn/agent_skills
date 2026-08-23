#!/usr/bin/env python3
"""Create articles/<slug>/source.md for ONE approved idea.

The agent must have explicit user confirmation before calling this. The script
refuses to overwrite anything and never runs in bulk by design.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

SCORED = Path(".idea-research/scored.json")
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "source_template.md"


def find_idea(idea_id):
    if not SCORED.exists():
        sys.exit(f"{SCORED} not found — run dedupe_and_score.py first.")
    for idea in json.loads(SCORED.read_text()):
        if idea["id"] == idea_id:
            return idea
    sys.exit(f"No idea with id '{idea_id}' in {SCORED}.")


def render_evidence(idea):
    lines = []
    for ev in idea.get("evidence", []):
        age = ev.get("age_hours")
        age_s = f"{age:.0f}h old" if age is not None else "no timestamp"
        lines.append(
            f"- **{ev['source']}** · {ev.get('score', 0)} pts · "
            f"{ev.get('comments', 0)} comments · {age_s}\n"
            f"  - {ev['title']}\n  - {ev['url']}"
        )
    return "\n".join(lines) or "- (none recorded)"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", required=True, help="idea id, e.g. idea-3")
    ap.add_argument("--root", default="articles/")
    ap.add_argument("--slug", help="override the generated folder name")
    ap.add_argument("--hook", default="", help="working title / hook")
    ap.add_argument("--angle", default="", help="one-line angle")
    ap.add_argument("--platform", default="", help="Medium | LinkedIn | Reddit")
    args = ap.parse_args()

    idea = find_idea(args.id)
    folder = Path(args.root) / (args.slug or idea["slug"])

    if folder.exists():
        sys.exit(f"REFUSING: {folder} already exists. Pick another slug or edit "
                 f"the existing source.md by hand.")
    if not TEMPLATE.exists():
        sys.exit(f"Template missing: {TEMPLATE}")

    c = idea["components"]
    body = TEMPLATE.read_text().format(
        title=args.hook or idea["title"],
        topic=idea["title"],
        beat=idea["beat"],
        platform=args.platform or "TBD",
        angle=args.angle or "TBD — fill this in before drafting.",
        score=idea["score"],
        recency=c["recency"], velocity=c["velocity"],
        beat_fit=c["beat_fit"], gap=c["gap"],
        gap_checked="yes" if idea.get("gap_checked") else "NOT VERIFIED",
        sources=", ".join(idea["sources"]),
        evidence=render_evidence(idea),
        date=date.today().isoformat(),
        idea_id=idea["id"],
    )

    folder.mkdir(parents=True)
    (folder / "source.md").write_text(body)
    print(f"Created {folder / 'source.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
