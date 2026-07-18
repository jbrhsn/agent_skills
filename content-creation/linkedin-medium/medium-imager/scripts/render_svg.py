#!/usr/bin/env python3
"""Render medium-imager images (cover + inner slide types) to SVG files.

Reads images.json (see images.py for schema) and writes:
    <out>/<slug>-cover.svg
    <out>/<slug>-01-<type>.svg, <out>/<slug>-02-<type>.svg, ...

Two canvases:
    COVER: 1500x750  (wide featured image)
    SLIDE: 1600x900  (shared by quote / callout / stat / code types)

Each theme ships two templates: templates/cover-<theme>.svg and
templates/slide-<theme>.svg. The cover template has placeholders
{{TITLE_BLOCK}} {{SUBTITLE_BLOCK}} {{FOOTER}}. The slide template has one
{{CONTENT_BLOCK}} placeholder that this script fills differently per
`type`, plus {{FOOTER}} {{COUNTER}} {{INDEX}} {{TOTAL}}.

Auto-fit: font sizes step down until content fits the safe area above the
reserved footer band. If a slide still overflows at the smallest size, the
script prints a WARNING and exits 3 (non-fatal) so the copy can be
shortened.

Example:
    python3 render_svg.py images.json --out medium/images/my-article
    python3 render_svg.py images.json --out out/ --theme dark-code --only cover
    python3 render_svg.py images.json --out out/ --only 1
"""
import argparse
import os
import sys
from xml.sax.saxutils import escape

import images as SCHEMA

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.normpath(os.path.join(HERE, "..", "templates"))
DEFAULT_THEME = "clean-minimal"

# --- Cover canvas -----------------------------------------------------------
COVER_W, COVER_H = 1500, 750
COVER_MARGIN = 90
COVER_FOOTER_BAND = 90
COVER_TITLE_STEPS = [88, 76, 66, 58, 50]
COVER_SUBTITLE_STEPS = [34, 30, 28, 26, 24]

# --- Slide canvas (shared by quote/callout/stat/code) ----------------------
SLIDE_W, SLIDE_H = 1600, 900
SLIDE_MARGIN = 110
SLIDE_FOOTER_BAND = 120

QUOTE_STEPS = [60, 52, 46, 40, 34]
QUOTE_ATTR_STEPS = [30, 28, 26, 24, 22]

CALLOUT_LABEL_SIZE = 28
CALLOUT_TEXT_STEPS = [64, 56, 48, 42, 36]

STAT_NUMBER_STEPS = [180, 150, 130, 110, 96]
STAT_LABEL_STEPS = [40, 36, 32, 30, 28]

CODE_STEPS = [34, 30, 28, 26, 24]
CODE_BADGE_SIZE = 26

CHAR_W_FACTOR = 0.55
CODE_CHAR_W_FACTOR = 0.62  # monospace is wider per character


def chars_per_line(font_size, width, factor=CHAR_W_FACTOR):
    return max(8, int(width / (font_size * factor)))


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


def wrap_code(text, cpl):
    """Wrap code preserving existing line breaks; only splits lines too long."""
    lines = []
    for raw_line in text.split("\n"):
        if len(raw_line) <= cpl or cpl <= 0:
            lines.append(raw_line)
            continue
        remaining = raw_line
        while len(remaining) > cpl:
            lines.append(remaining[:cpl])
            remaining = remaining[cpl:]
        lines.append(remaining)
    return lines


def text_block(cls, lines, x, start_y, line_height, size, anchor=None, preserve=False):
    if not lines:
        return f'<text class="{cls}" x="{x}" y="{start_y}" font-size="{size}"></text>'
    attrs = f'class="{cls}" x="{x}" y="{start_y}" font-size="{size}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if preserve:
        attrs += ' xml:space="preserve"'
    parts = [f"<text {attrs}>"]
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(line) if line else " "}</tspan>')
    parts.append("</text>")
    return "".join(parts)


# --- Cover fit/build ---------------------------------------------------------

def fit_cover(title, subtitle):
    inner_w = COVER_W - 2 * COVER_MARGIN
    safe_h = COVER_H - COVER_MARGIN - COVER_FOOTER_BAND
    top = COVER_MARGIN + 60  # accent + gap before title

    for t_size, s_size in zip(COVER_TITLE_STEPS, COVER_SUBTITLE_STEPS):
        t_lines = wrap_text(title, chars_per_line(t_size, inner_w))
        s_lines = wrap_text(subtitle, chars_per_line(s_size, inner_w)) if subtitle else []
        t_lh = int(t_size * 1.12)
        s_lh = int(s_size * 1.3)
        gap = 40 if s_lines else 0
        used = top + len(t_lines) * t_lh + gap + len(s_lines) * s_lh
        if used <= safe_h:
            return t_size, s_size, t_lines, s_lines, False

    t_size, s_size = COVER_TITLE_STEPS[-1], COVER_SUBTITLE_STEPS[-1]
    t_lines = wrap_text(title, chars_per_line(t_size, inner_w))
    s_lines = wrap_text(subtitle, chars_per_line(s_size, inner_w)) if subtitle else []
    return t_size, s_size, t_lines, s_lines, True


def build_cover(template, cover):
    title = cover.get("title", "")
    subtitle = cover.get("subtitle", "")
    footer = cover.get("footer", "")

    t_size, s_size, t_lines, s_lines, overflow = fit_cover(title, subtitle)

    top = COVER_MARGIN + 60
    title_y = top + t_size
    title_lh = int(t_size * 1.12)
    subtitle_y = title_y + len(t_lines) * title_lh + (40 if s_lines else 0) + s_size
    subtitle_lh = int(s_size * 1.3)

    title_block = text_block("title", t_lines, COVER_MARGIN, title_y, title_lh, t_size)
    subtitle_block = text_block("subtitle", s_lines, COVER_MARGIN, subtitle_y, subtitle_lh, s_size)

    out = template
    out = out.replace("{{TITLE_BLOCK}}", title_block)
    out = out.replace("{{SUBTITLE_BLOCK}}", subtitle_block)
    out = out.replace("{{FOOTER}}", escape(footer))
    return out, overflow


# --- Slide type fit/build ----------------------------------------------------

def _slide_geometry():
    inner_w = SLIDE_W - 2 * SLIDE_MARGIN
    safe_h = SLIDE_H - SLIDE_MARGIN - SLIDE_FOOTER_BAND
    top = SLIDE_MARGIN + 50
    return inner_w, safe_h, top


def fit_quote(quote, attribution):
    inner_w, safe_h, top = _slide_geometry()
    for q_size, a_size in zip(QUOTE_STEPS, QUOTE_ATTR_STEPS):
        q_lines = wrap_text(quote, chars_per_line(q_size, inner_w))
        a_lines = wrap_text(attribution, chars_per_line(a_size, inner_w)) if attribution else []
        q_lh = int(q_size * 1.25)
        a_lh = int(a_size * 1.3)
        gap = 50 if a_lines else 0
        used = top + len(q_lines) * q_lh + gap + len(a_lines) * a_lh
        if used <= safe_h:
            return q_size, a_size, q_lines, a_lines, False
    q_size, a_size = QUOTE_STEPS[-1], QUOTE_ATTR_STEPS[-1]
    q_lines = wrap_text(quote, chars_per_line(q_size, inner_w))
    a_lines = wrap_text(attribution, chars_per_line(a_size, inner_w)) if attribution else []
    return q_size, a_size, q_lines, a_lines, True


def build_quote(img):
    quote = img.get("quote", "")
    attribution = img.get("attribution", "")
    q_size, a_size, q_lines, a_lines, overflow = fit_quote(quote, attribution)

    cx = SLIDE_W // 2
    _, _, top = _slide_geometry()
    mark_y = top
    q_y = mark_y + 70 + q_size
    q_lh = int(q_size * 1.25)
    a_y = q_y + len(q_lines) * q_lh + (50 if a_lines else 0) + a_size
    a_lh = int(a_size * 1.3)

    parts = [f'<text class="quote-mark" x="{cx}" y="{mark_y + 60}" text-anchor="middle">&#8220;</text>']
    parts.append(text_block("quote", q_lines, cx, q_y, q_lh, q_size, anchor="middle"))
    if a_lines:
        parts.append(text_block("attribution", a_lines, cx, a_y, a_lh, a_size, anchor="middle"))
    return "".join(parts), overflow


def fit_callout(text):
    inner_w, safe_h, top = _slide_geometry()
    label_lh = int(CALLOUT_LABEL_SIZE * 1.3)
    label_gap = 40
    for size in CALLOUT_TEXT_STEPS:
        lines = wrap_text(text, chars_per_line(size, inner_w))
        lh = int(size * 1.3)
        used = top + label_lh + label_gap + len(lines) * lh
        if used <= safe_h:
            return size, lines, False
    size = CALLOUT_TEXT_STEPS[-1]
    lines = wrap_text(text, chars_per_line(size, inner_w))
    return size, lines, True


def build_callout(img):
    text = img.get("text", "")
    label = img.get("label", "")
    size, lines, overflow = fit_callout(text)

    _, _, top = _slide_geometry()
    parts = []
    text_top = top
    if label:
        label_y = top + CALLOUT_LABEL_SIZE
        parts.append(text_block("label", [label.upper()], SLIDE_MARGIN, label_y,
                                 int(CALLOUT_LABEL_SIZE * 1.3), CALLOUT_LABEL_SIZE))
        text_top = label_y + 40
    lh = int(size * 1.3)
    text_y = text_top + size
    parts.append(text_block("callout-text", lines, SLIDE_MARGIN, text_y, lh, size))
    return "".join(parts), overflow


def fit_stat(number, label):
    inner_w, safe_h, top = _slide_geometry()
    for n_size, l_size in zip(STAT_NUMBER_STEPS, STAT_LABEL_STEPS):
        cpl = chars_per_line(n_size, inner_w)
        if len(number) <= cpl:
            n_lines = [number]
        else:
            continue  # number must not wrap; try a smaller size
        l_lines = wrap_text(label, chars_per_line(l_size, inner_w))
        n_lh = int(n_size * 1.05)
        l_lh = int(l_size * 1.3)
        gap = 40
        used = top + len(n_lines) * n_lh + gap + len(l_lines) * l_lh
        if used <= safe_h:
            return n_size, l_size, n_lines, l_lines, False
    n_size, l_size = STAT_NUMBER_STEPS[-1], STAT_LABEL_STEPS[-1]
    n_lines = [number[: chars_per_line(n_size, inner_w)]]
    l_lines = wrap_text(label, chars_per_line(l_size, inner_w))
    return n_size, l_size, n_lines, l_lines, True


def build_stat(img):
    number = img.get("number", "")
    label = img.get("label", "")
    n_size, l_size, n_lines, l_lines, overflow = fit_stat(number, label)

    cx = SLIDE_W // 2
    _, _, top = _slide_geometry()
    n_y = top + n_size
    n_lh = int(n_size * 1.05)
    l_y = n_y + len(n_lines) * n_lh + 40 + l_size
    l_lh = int(l_size * 1.3)

    parts = [text_block("stat-number", n_lines, cx, n_y, n_lh, n_size, anchor="middle")]
    parts.append(text_block("stat-label", l_lines, cx, l_y, l_lh, l_size, anchor="middle"))
    return "".join(parts), overflow


def fit_code(code):
    inner_w, safe_h, top = _slide_geometry()
    badge_gap = 80
    for size in CODE_STEPS:
        cpl = chars_per_line(size, inner_w, factor=CODE_CHAR_W_FACTOR)
        lines = wrap_code(code, cpl)
        lh = int(size * 1.4)
        used = top + badge_gap + len(lines) * lh
        if used <= safe_h:
            return size, lines, False
    size = CODE_STEPS[-1]
    lines = wrap_code(code, chars_per_line(size, inner_w, factor=CODE_CHAR_W_FACTOR))
    return size, lines, True


def build_code(img):
    code = img.get("code", "")
    language = img.get("language", "")
    size, lines, overflow = fit_code(code)

    _, _, top = _slide_geometry()
    parts = []
    code_top = top
    if language:
        label = language.upper()
        badge_w = max(70, 22 * len(label))
        badge_h = CODE_BADGE_SIZE + 18
        badge_y = top
        parts.append(
            f'<rect class="lang-badge-bg" x="{SLIDE_MARGIN}" y="{badge_y}" '
            f'width="{badge_w}" height="{badge_h}" rx="6" ry="6"/>'
        )
        parts.append(
            f'<text class="lang-badge" x="{SLIDE_MARGIN + badge_w / 2}" '
            f'y="{badge_y + badge_h / 2 + CODE_BADGE_SIZE * 0.36}" '
            f'text-anchor="middle" font-size="{CODE_BADGE_SIZE}">{escape(label)}</text>'
        )
        code_top = badge_y + badge_h + 34
    lh = int(size * 1.4)
    code_y = code_top + size
    parts.append(text_block("code", lines, SLIDE_MARGIN, code_y, lh, size, preserve=True))
    return "".join(parts), overflow


TYPE_BUILDERS = {
    "quote": build_quote,
    "callout": build_callout,
    "stat": build_stat,
    "code": build_code,
}


def render_cover_svg(theme, cover):
    path = os.path.join(TEMPLATES_DIR, f"cover-{theme}.svg")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"cover template not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        template = fh.read()
    return build_cover(template, cover)


def render_slide_svg(theme, img, index, total):
    path = os.path.join(TEMPLATES_DIR, f"slide-{theme}.svg")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"slide template not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        template = fh.read()

    t = img["type"]
    content_block, overflow = TYPE_BUILDERS[t](img)
    footer = img.get("footer", "")
    counter = f"{index}/{total}"

    out = template
    out = out.replace("{{CONTENT_BLOCK}}", content_block)
    out = out.replace("{{FOOTER}}", escape(footer))
    out = out.replace("{{COUNTER}}", escape(counter))
    out = out.replace("{{INDEX}}", str(index))
    out = out.replace("{{TOTAL}}", str(total))
    return out, overflow


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render medium-imager cover + slide images to SVG (auto-fit, themed).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("images_json", help="Path to images.json file.")
    parser.add_argument("--out", required=True, help="Output directory for .svg files.")
    parser.add_argument("--theme", default=DEFAULT_THEME,
                         help=f"Theme name (default: {DEFAULT_THEME}).")
    parser.add_argument("--only", default=None,
                         help="Render only 'cover' or a 1-based inner image number (for previews).")
    args = parser.parse_args(argv)

    theme_dir_check = os.path.join(TEMPLATES_DIR, f"cover-{args.theme}.svg")
    if not os.path.isfile(theme_dir_check):
        print(f"error: unknown theme or missing template: {theme_dir_check}", file=sys.stderr)
        return 2

    try:
        slug, cover, images = SCHEMA.load_images(args.images_json)
    except (SCHEMA.SchemaError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    os.makedirs(args.out, exist_ok=True)
    total = len(images)
    written = []
    overflows = []

    render_cover = args.only in (None, "cover")
    if render_cover:
        svg, overflow = render_cover_svg(args.theme, cover)
        fname = os.path.join(args.out, f"{slug}-cover.svg")
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(svg)
        written.append(fname)
        if overflow:
            overflows.append("cover")

    skip_all_inner = args.only == "cover"
    only_n = None
    if args.only is not None and args.only != "cover":
        try:
            only_n = int(args.only)
        except ValueError:
            print(f"error: --only must be 'cover' or an integer, got {args.only!r}", file=sys.stderr)
            return 2

    for i, img in enumerate(images, start=1):
        if skip_all_inner:
            continue
        if only_n is not None and i != only_n:
            continue
        svg, overflow = render_slide_svg(args.theme, img, i, total)
        fname = os.path.join(args.out, f"{slug}-{i:02d}-{img['type']}.svg")
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(svg)
        written.append(fname)
        if overflow:
            overflows.append(i)

    if not written:
        print("No images written (check --only value).", file=sys.stderr)
        return 1
    for f in written:
        print(f"wrote {f}")
    print(f"\n{len(written)} SVG file(s) written to {args.out}")
    if overflows:
        print(
            f"WARNING: item(s) {overflows} still overflow at the smallest font "
            "size. Shorten the copy or split it.",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
