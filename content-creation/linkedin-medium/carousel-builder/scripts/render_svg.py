#!/usr/bin/env python3
"""Render carousel slides to individual SVG files.

Reads a JSON file describing carousel slides and writes one portrait
(1080x1350) SVG per slide into an output directory. Pure standard library:
no pip installs required to produce SVGs.

Layout is auto-fit: if a slide's title+body would overflow the safe area or
collide with the footer band, font sizes are stepped down (and, past a floor,
the script WARNS that the slide is over budget so you can split it). The same
canvas/palette/spacing constants are shared with the HTML template so the
slide-1 preview matches the final render.

JSON schema (index/total auto-filled from array position):

    {
      "slug": "my-carousel",
      "slides": [
        {"title": "Hook", "body": "One clear idea.", "footer": "@handle"},
        {"title": "Point", "body": "Supporting detail."}
      ]
    }

Example:
    python3 render_svg.py slides.json --out linkedin/carousels/my-carousel
"""
import argparse
import json
import os
import sys
from xml.sax.saxutils import escape

# --- Shared layout constants (keep in sync with templates/slide.html) -------
CANVAS_W = 1080
CANVAS_H = 1350
MARGIN = 100
FOOTER_BAND = 140  # reserved vertical space at the bottom for the footer row

# Font stack: list real fallbacks so PNG rasterizers (e.g. cairosvg) find a
# font even when Helvetica is absent (common on Linux).
FONT_STACK = "Helvetica, 'Helvetica Neue', Arial, 'Liberation Sans', 'DejaVu Sans', sans-serif"

BG = "#0f172a"
ACCENT = "#38bdf8"
TITLE_COLOR = "#f8fafc"
BODY_COLOR = "#cbd5e1"
FOOTER_COLOR = "#64748b"

# Auto-fit: try these (title, body) size pairs largest-first until it fits.
FIT_STEPS = [(68, 40), (60, 36), (54, 32), (48, 30), (44, 28)]
# Approx glyph-width factor for character-per-line estimation.
CHAR_W_FACTOR = 0.55


def chars_per_line(font_size, width):
    return max(8, int(width / (font_size * CHAR_W_FACTOR)))


def wrap_text(text, cpl):
    """Greedy word-wrap by character count. Returns a list of lines."""
    if not text:
        return []
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = ""
        for word in words:
            candidate = word if not current else current + " " + word
            if len(candidate) <= cpl:
                current = candidate
            else:
                if current:
                    lines.append(current)
                while len(word) > cpl:
                    lines.append(word[:cpl])
                    word = word[cpl:]
                current = word
        if current:
            lines.append(current)
    return lines


def fit_slide(title, body):
    """Choose the largest font pair whose content fits the safe area.

    Returns (title_size, body_size, title_lines, body_lines, overflow: bool).
    """
    inner_w = CANVAS_W - 2 * MARGIN
    safe_h = CANVAS_H - MARGIN - FOOTER_BAND  # bottom of usable content area
    top = MARGIN + 40 + 40  # accent bar + gap before title

    for t_size, b_size in FIT_STEPS:
        t_lines = wrap_text(title, chars_per_line(t_size, inner_w))
        b_lines = wrap_text(body, chars_per_line(b_size, inner_w))
        t_lh = int(t_size * 1.15)
        b_lh = int(b_size * 1.4)
        gap = 60
        used = top + len(t_lines) * t_lh + gap + len(b_lines) * b_lh
        if used <= safe_h:
            return t_size, b_size, t_lines, b_lines, False

    # Smallest step still overflows: render at floor and flag it.
    t_size, b_size = FIT_STEPS[-1]
    t_lines = wrap_text(title, chars_per_line(t_size, inner_w))
    b_lines = wrap_text(body, chars_per_line(b_size, inner_w))
    return t_size, b_size, t_lines, b_lines, True


def tspans(lines, x, start_y, line_height, size, color, weight="normal"):
    if not lines:
        return ""
    parts = [
        f'<text x="{x}" y="{start_y}" font-family="{FONT_STACK}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">'
    ]
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def render_slide_svg(slide, index, total):
    """Render one slide. Returns (svg_string, overflow: bool)."""
    t_size, b_size, title_lines, body_lines, overflow = fit_slide(
        slide.get("title", ""), slide.get("body", "")
    )
    footer = slide.get("footer", "")

    accent_y = MARGIN
    title_y = accent_y + 40 + 40 + t_size
    title_lh = int(t_size * 1.15)
    body_y = title_y + len(title_lines) * title_lh + 60 + b_size
    body_lh = int(b_size * 1.4)

    footer_y = CANVAS_H - MARGIN + 20
    footer_size = 28

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" '
        f'height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}">',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="{BG}"/>',
        f'<rect x="{MARGIN}" y="{accent_y}" width="120" height="10" fill="{ACCENT}"/>',
        tspans(title_lines, MARGIN, title_y, title_lh, t_size, TITLE_COLOR, "bold"),
        tspans(body_lines, MARGIN, body_y, body_lh, b_size, BODY_COLOR),
    ]
    if footer:
        svg.append(
            f'<text x="{MARGIN}" y="{footer_y}" font-family="{FONT_STACK}" '
            f'font-size="{footer_size}" fill="{FOOTER_COLOR}">{escape(footer)}</text>'
        )
    counter = f"{index}/{total}"
    svg.append(
        f'<text x="{CANVAS_W - MARGIN}" y="{footer_y}" text-anchor="end" '
        f'font-family="{FONT_STACK}" font-size="{footer_size}" '
        f'fill="{FOOTER_COLOR}">{escape(counter)}</text>'
    )
    svg.append("</svg>")
    return "\n".join(svg), overflow


def load_slides(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("JSON must contain a non-empty 'slides' array.")
    slug = data.get("slug", "carousel")
    return slug, slides


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render carousel slides to individual SVG files (1080x1350, auto-fit).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("slides_json", help="Path to slides JSON file.")
    parser.add_argument("--out", required=True,
                        help="Output directory for .svg files (cwd-relative recommended).")
    parser.add_argument("--only", type=int, default=None,
                        help="Render only the given 1-based slide number (for previews).")
    args = parser.parse_args(argv)

    slug, slides = load_slides(args.slides_json)
    total = len(slides)
    os.makedirs(args.out, exist_ok=True)

    written = []
    overflows = []
    for i, slide in enumerate(slides, start=1):
        if args.only is not None and i != args.only:
            continue
        svg, overflow = render_slide_svg(slide, i, total)
        fname = os.path.join(args.out, f"{slug}-{i:02d}.svg")
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(svg)
        written.append(fname)
        if overflow:
            overflows.append(i)

    if not written:
        print("No slides written (check --only value).", file=sys.stderr)
        return 1
    for f in written:
        print(f"wrote {f}")
    print(f"\n{len(written)} SVG file(s) written to {args.out}")
    if overflows:
        print(
            f"WARNING: slide(s) {overflows} still overflow at the smallest font "
            "size. Shorten the copy or split into more slides.",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
