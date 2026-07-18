#!/usr/bin/env python3
"""Suggest cover/quote/callout candidates from an existing medium/<slug>.md draft.

Parses a Medium draft markdown file and prints candidate copy for the agent
to present in chat for user confirmation. This script NEVER writes
images.json itself — it only surfaces suggestions; the agent must get
explicit user approval/edits before any copy is written.

Heuristics (best-effort, not exhaustive):
    - First H1 (`# Title`)                  -> cover title candidate
    - First paragraph right after the H1    -> cover subtitle candidate
    - Blockquotes (`> ...`) or sentences
      wrapped in quotes                     -> quote card candidates
    - Each H2 (`## Section`) heading        -> callout/label candidates,
      paired with the first sentence of that section as callout text
    - Standalone bold short lines matching
      a number/percentage pattern           -> stat candidates

Example:
    python3 suggest_from_draft.py medium/my-article.md
    python3 suggest_from_draft.py medium/my-article.md --json
"""
import argparse
import json
import re
import sys

STAT_RE = re.compile(r"\*\*([^*]*\d+[.,]?\d*\s?(?:%|[kKmMbB]x?|x)[^*]*)\*\*")


def parse_draft(text):
    lines = text.splitlines()

    title = None
    subtitle = None
    quotes = []
    callouts = []
    stats = []

    i = 0
    n = len(lines)

    # First H1 -> title
    while i < n:
        line = lines[i].strip()
        if line.startswith("# "):
            title = line[2:].strip()
            i += 1
            break
        i += 1

    # First non-empty paragraph after H1 -> subtitle candidate
    while i < n:
        line = lines[i].strip()
        if line:
            if not line.startswith("#") and not line.startswith(">"):
                subtitle = line
            break
        i += 1

    current_h2 = None
    current_h2_body = []

    def flush_h2():
        if current_h2 and current_h2_body:
            first_sentence = current_h2_body[0]
            callouts.append({"label": current_h2, "text": first_sentence})

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> "):
            quotes.append(stripped[2:].strip())
        elif stripped.startswith("## "):
            flush_h2()
            current_h2 = stripped[3:].strip()
            current_h2_body = []
        elif current_h2 is not None and stripped and not stripped.startswith("#"):
            if not current_h2_body:
                # take first sentence only
                sentence = re.split(r"(?<=[.!?])\s", stripped, maxsplit=1)[0]
                current_h2_body.append(sentence)
        m = STAT_RE.search(stripped)
        if m:
            stats.append(m.group(1).strip())
    flush_h2()

    return {
        "cover_title": title,
        "cover_subtitle": subtitle,
        "quote_candidates": quotes[:5],
        "callout_candidates": callouts[:5],
        "stat_candidates": stats[:5],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Suggest cover/quote/callout/stat candidates from a Medium draft.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("draft_path", help="Path to medium/<slug>.md draft file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args(argv)

    try:
        with open(args.draft_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    suggestions = parse_draft(text)

    if args.json:
        print(json.dumps(suggestions, indent=2))
        return 0

    print("DRAFT SUGGESTIONS (present these to the user for confirmation/edits)")
    print(f"  cover title:    {suggestions['cover_title'] or '(none found)'}")
    print(f"  cover subtitle: {suggestions['cover_subtitle'] or '(none found)'}")
    print("  quote candidates:")
    for q in suggestions["quote_candidates"]:
        print(f"    - {q}")
    print("  callout candidates:")
    for c in suggestions["callout_candidates"]:
        print(f"    - [{c['label']}] {c['text']}")
    print("  stat candidates:")
    for s in suggestions["stat_candidates"]:
        print(f"    - {s}")
    print("\n  JSON:")
    print(json.dumps(suggestions, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
