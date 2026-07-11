#!/usr/bin/env python3
"""claim_lint.py — enforce claim integrity in a source draft.

draft-builder's core promise is: never fabricate facts. In Expansion mode the
model develops sparse notes into full prose, which is exactly where invented
statistics, fake studies, and made-up attributions creep in. This linter turns
that prose promise into an enforced gate.

CONTRACT
========
Every *risky* claim in a draft's prose must be explicitly accounted for as
EITHER:

  * CITED     -> followed by an inline marker `[source: <url-or-ref>]`
  * FLAGGED   -> marked `[UNVERIFIED]` (author knowingly ships an unbacked claim)
  * ANECDOTE  -> marked `[personal]` (first-hand experience, not a public fact)

A risky claim is a sentence that trips one of the detectors below (numbers,
percentages, money, dates/years, "studies show"-style phrasing, named
attributions like "X says", or absolute superlatives). Any risky sentence that
carries NONE of the three markers is an UNACCOUNTED claim and fails the lint.

This is a HEURISTIC, best-effort denylist of risky patterns — like
tutorial-verifier's dangerous-command scan, it is a safety net, not a proof.
It can miss a laundered claim and can occasionally over-flag. Over-flagging is
the safe direction: the author resolves it by citing, flagging, or rewording.

SCOPE
=====
By default only the drafting prose is linted. Fenced code blocks, blockquotes,
Markdown headings, list scaffolding lines, and the stub's own metadata/section
headers (Status, Platform, Hook, Why now, Research sources, Raw notes) are
skipped so the linter judges the NEW prose, not the seed-expander scaffolding.
Pass --whole-file to lint everything.

USAGE
=====
    python3 claim_lint.py drafts/my-post.md
    python3 claim_lint.py drafts/my-post.md --json
    python3 claim_lint.py drafts/my-post.md --section Draft   # only the ## Draft body
    python3 claim_lint.py drafts/my-post.md --whole-file

EXIT CODES
==========
    0  clean  — no unaccounted risky claims
    1  fail   — one or more unaccounted risky claims (details printed)
    2  usage  — bad arguments / file not found
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# --- Markers that ACCOUNT for a risky claim --------------------------------
CITED_RE = re.compile(r"\[source:[^\]]+\]", re.IGNORECASE)
UNVERIFIED_RE = re.compile(r"\[UNVERIFIED\]", re.IGNORECASE)
ANECDOTE_RE = re.compile(r"\[personal\]", re.IGNORECASE)

# --- Risky-claim detectors (heuristic denylist) ----------------------------
# Each: (name, compiled regex, short human hint).
RISK_PATTERNS = [
    ("percentage", re.compile(r"\b\d{1,3}(?:\.\d+)?\s?%"),
     "a percentage — cite it or flag it"),
    ("money", re.compile(r"[$£€]\s?\d[\d,]*(?:\.\d+)?\s?(?:[KMB]|billion|million|thousand)?", re.IGNORECASE),
     "a monetary figure — cite it or flag it"),
    ("multiplier", re.compile(r"\b\d+(?:\.\d+)?\s?x\b", re.IGNORECASE),
     "a multiplier claim (e.g. 10x) — cite it or flag it"),
    ("big_number", re.compile(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+(?:\.\d+)?\s?(?:billion|million|thousand)\b", re.IGNORECASE),
     "a large quantity — cite it or flag it"),
    ("year", re.compile(r"\b(?:in|since|by|during)\s+(?:19|20)\d{2}\b", re.IGNORECASE),
     "a dated claim — cite the source for that year's data or flag it"),
    ("study", re.compile(r"\b(?:studies|study|research|survey|reports?\s+(?:show|found|say)|according to|found that|shows? that|proven|proves|statistics?)\b", re.IGNORECASE),
     "an appeal to research/data — cite the study or flag it"),
    # A named attribution: a capitalized name/source followed by an attribution
    # verb ("Gartner estimates", "Dr. Lee argues"). Common capitalized sentence
    # openers (I, We, The, This, It, ...) are excluded via ATTRIBUTION_STOPWORDS
    # in find_risks() so ordinary sentences like "This shows..." don't over-flag.
    ("attribution", re.compile(r"\b([A-Z][a-zA-Z.'-]+(?:\s+[A-Z][a-zA-Z.'-]+)?)\s+(?:says?|said|argues?|claims?|reports?|predicts?|estimates?|found)\b"),
     "a named attribution — cite the quote/source or flag it"),
    ("superlative", re.compile(r"\b(?:most|worst|largest|smallest|fastest|slowest|biggest|highest|lowest|never|always|guaranteed|proven|the\s+only)\b", re.IGNORECASE),
     "an absolute/superlative factual claim — soften, cite, or flag it"),
]

# Bare integers/decimals not caught above (e.g. "50 examples", "3 out of 4").
BARE_NUMBER_RE = re.compile(r"(?<![\w$£€.])\d+(?:\.\d+)?(?![\w%])")

# Capitalized words that are ordinary sentence openers, not named sources. When
# the attribution detector's captured subject is one of these, it's almost
# always plain prose ("This shows...", "It found...") rather than a citable
# attribution, so we don't flag it.
ATTRIBUTION_STOPWORDS = {
    "i", "we", "you", "he", "she", "it", "they", "the", "this", "that",
    "these", "those", "there", "here", "one", "some", "many", "most",
    "everyone", "someone", "nobody", "everybody", "who", "which", "what",
    "and", "but", "so", "then", "when", "if", "as", "my", "our", "your",
    "his", "her", "its", "their",
}

# Lines that are scaffolding, not drafting prose — skipped by default.
STUB_META_RE = re.compile(r"^\s*\*\*(?:Status|Platform|Angle|Hook)\b", re.IGNORECASE)
SKIP_HEADINGS = {
    "why now", "research sources", "raw notes / seed", "raw notes", "seed",
}


def split_sentences(text: str):
    """Very light sentence splitter that keeps offsets stable enough for hints."""
    # Split on ., !, ? followed by space/newline, but keep it simple & robust.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def iter_prose_lines(raw: str, whole_file: bool, section: str | None):
    """Yield (line_number, line_text) for lines that should be linted."""
    lines = raw.splitlines()
    in_code = False
    active_section = None
    want_section = section.strip().lower() if section else None

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Toggle fenced code blocks.
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code and not whole_file:
            continue

        # Track current ## section heading.
        m = re.match(r"^#{1,6}\s+(.*)$", stripped)
        if m:
            active_section = m.group(1).strip().lower()
            continue

        if whole_file:
            yield i, line
            continue

        # Section filter: if --section given, only lint that section's body.
        if want_section is not None:
            if active_section == want_section:
                yield i, line
            continue

        # Default: skip known scaffolding sections and stub metadata lines.
        if active_section in SKIP_HEADINGS:
            continue
        if STUB_META_RE.match(line):
            continue
        if stripped.startswith(">"):  # blockquotes / callouts
            continue
        yield i, line


def line_is_accounted(line: str) -> bool:
    return bool(CITED_RE.search(line) or UNVERIFIED_RE.search(line)
                or ANECDOTE_RE.search(line))


def find_risks(line: str):
    """Return a list of (risk_name, hint, matched_text) for a single line."""
    hits = []
    for name, rx, hint in RISK_PATTERNS:
        m = rx.search(line)
        if m:
            if name == "attribution":
                # Skip ordinary sentence openers ("This shows", "It found")
                # whose captured subject isn't a real named source.
                subject = m.group(1).split()[0].lower()
                if subject in ATTRIBUTION_STOPWORDS:
                    continue
            hits.append((name, hint, m.group(0).strip()))
    # Bare numbers only if no richer numeric detector already fired.
    if not any(n in {"percentage", "money", "multiplier", "big_number", "year"}
               for n, _, _ in hits):
        m = BARE_NUMBER_RE.search(line)
        if m:
            hits.append(("number", "a bare number — cite it or flag it", m.group(0)))
    return hits


def lint(raw: str, whole_file: bool, section: str | None):
    findings = []
    for lineno, line in iter_prose_lines(raw, whole_file, section):
        if not line.strip():
            continue
        if line_is_accounted(line):
            continue  # author already cited / flagged / marked personal
        risks = find_risks(line)
        if risks:
            findings.append({
                "line": lineno,
                "text": line.strip(),
                "risks": [{"type": n, "hint": h, "match": mt} for n, h, mt in risks],
            })
    return findings


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="claim_lint.py",
        description="Enforce claim integrity: every risky claim must be cited "
                    "[source: ...], flagged [UNVERIFIED], or marked [personal].",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("draft", help="Path to the draft markdown file.")
    p.add_argument("--section", default=None,
                   help="Only lint the body under this ## heading (e.g. 'Draft').")
    p.add_argument("--whole-file", action="store_true",
                   help="Lint everything, including code blocks and scaffolding.")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = p.parse_args(argv)

    if not os.path.isfile(args.draft):
        print(f"error: file not found: {args.draft}", file=sys.stderr)
        return 2

    with open(args.draft, "r", encoding="utf-8") as fh:
        raw = fh.read()

    findings = lint(raw, args.whole_file, args.section)

    if args.json:
        print(json.dumps({
            "ok": not findings,
            "file": args.draft,
            "unaccounted_claims": findings,
            "count": len(findings),
        }, indent=2))
        return 0 if not findings else 1

    if not findings:
        print(f"CLAIM LINT: PASS — no unaccounted risky claims in {args.draft}")
        print("Every risky claim is cited [source: ...], flagged [UNVERIFIED], "
              "or marked [personal].")
        return 0

    print(f"CLAIM LINT: FAIL — {len(findings)} unaccounted risky claim(s) in {args.draft}\n")
    for f in findings:
        print(f"  line {f['line']}: {f['text']}")
        for r in f["risks"]:
            print(f"      -> {r['type']}: {r['hint']}  (matched: '{r['match']}')")
        print()
    print("Resolve EACH by one of:")
    print("  * add a real citation:      ... [source: https://example.com/report]")
    print("  * knowingly ship unbacked:  ... [UNVERIFIED]")
    print("  * mark first-hand anecdote: ... [personal]")
    print("\nNever invent a citation to silence the linter. If you cannot source "
          "a claim, flag it [UNVERIFIED] or cut it.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
