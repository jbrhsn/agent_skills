#!/usr/bin/env python3
"""Render carousel slides to individual HTML files from templates/slide.html.

Fills the slide template with each slide's real content and writes one .html
per slide into an output directory. Pure standard library. HTML files are
valid, self-contained output on their own (open in a browser to view/print).

Optional PNG export: if a headless browser is available you can screenshot
each 1080x1350 page. This script does NOT require it and prints a hint only.

JSON schema (index/total auto-filled from array position):

    {
      "slug": "my-carousel",
      "slides": [
        {"title": "Hook", "body": "One clear idea.", "footer": "@handle"}
      ]
    }

Example:
    python3 render_html.py slides.json --out linkedin/carousels/my-carousel
"""
import argparse
import json
import os
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.normpath(os.path.join(HERE, "..", "templates", "slide.html"))

PNG_HINT = (
    "\nTo export PNGs from these HTML files (optional), use a headless browser:\n"
    "  playwright:  npx playwright screenshot --viewport-size=1080,1350 "
    "file://<abs>/slide.html slide.png\n"
    "  puppeteer / Chrome headless can do the same.\n"
    "Otherwise the HTML files are valid output and can be opened in any browser."
)


def load_slides(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("JSON must contain a non-empty 'slides' array.")
    slug = data.get("slug", "carousel")
    return slug, slides


def fill_template(template, slide, index, total):
    mapping = {
        "{{TITLE}}": escape(slide.get("title", "")),
        "{{BODY}}": escape(slide.get("body", "")),
        "{{FOOTER}}": escape(slide.get("footer", "")),
        "{{INDEX}}": str(index),
        "{{TOTAL}}": str(total),
    }
    out = template
    for key, val in mapping.items():
        out = out.replace(key, val)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render carousel slides to HTML files from templates/slide.html.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("slides_json", help="Path to slides JSON file.")
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for .html files (cwd-relative recommended).",
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE,
        help=f"Path to slide HTML template (default: {DEFAULT_TEMPLATE}).",
    )
    parser.add_argument(
        "--only",
        type=int,
        default=None,
        help="Render only the given 1-based slide number (for previews).",
    )
    args = parser.parse_args(argv)

    if not os.path.isfile(args.template):
        print(f"error: template not found: {args.template}", file=sys.stderr)
        return 2

    with open(args.template, "r", encoding="utf-8") as fh:
        template = fh.read()

    slug, slides = load_slides(args.slides_json)
    total = len(slides)
    os.makedirs(args.out, exist_ok=True)

    written = []
    for i, slide in enumerate(slides, start=1):
        if args.only is not None and i != args.only:
            continue
        html_out = fill_template(template, slide, i, total)
        fname = os.path.join(args.out, f"{slug}-{i:02d}.html")
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(html_out)
        written.append(fname)

    if not written:
        print("No slides written (check --only value).", file=sys.stderr)
        return 1
    for f in written:
        print(f"wrote {f}")
    print(f"\n{len(written)} HTML file(s) written to {args.out}")
    print(PNG_HINT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
