#!/usr/bin/env python3
"""Emit a medium-imager design spec for the review-first preview step.

Reads images.json and prints a human-readable design spec plus a
machine-readable JSON block: canvases, theme, image count, and per-image
auto-fit result (font sizes / line counts / overflow flag). Use this to show
the user WHAT will be rendered before rendering everything.

Example:
    python3 spec.py medium/images/my-article/images.json --path medium/images/my-article
    python3 spec.py images.json --theme dark-code --json
"""
import argparse
import json
import os
import sys

import images as SCHEMA
import render_svg as R


def build_spec(images_json_path, out_path, theme):
    cover_template = os.path.join(R.TEMPLATES_DIR, f"cover-{theme}.svg")
    slide_template = os.path.join(R.TEMPLATES_DIR, f"slide-{theme}.svg")
    for path in (cover_template, slide_template):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"template not found: {path}")

    slug, cover, imgs = SCHEMA.load_images(images_json_path)

    t_size, s_size, t_lines, s_lines, cover_overflow = R.fit_cover(
        cover.get("title", ""), cover.get("subtitle", "")
    )
    cover_spec = {
        "title_font": t_size,
        "subtitle_font": s_size,
        "title_lines": len(t_lines),
        "subtitle_lines": len(s_lines),
        "overflow": cover_overflow,
    }

    per_image = []
    overflows = []
    if cover_overflow:
        overflows.append("cover")

    for i, img in enumerate(imgs, start=1):
        t = img["type"]
        if t == "quote":
            q_size, a_size, q_lines, a_lines, overflow = R.fit_quote(
                img.get("quote", ""), img.get("attribution", "")
            )
            detail = {"quote_font": q_size, "attribution_font": a_size,
                       "quote_lines": len(q_lines), "attribution_lines": len(a_lines)}
        elif t == "callout":
            size, lines, overflow = R.fit_callout(img.get("text", ""))
            detail = {"text_font": size, "text_lines": len(lines)}
        elif t == "stat":
            n_size, l_size, n_lines, l_lines, overflow = R.fit_stat(
                img.get("number", ""), img.get("label", "")
            )
            detail = {"number_font": n_size, "label_font": l_size, "label_lines": len(l_lines)}
        elif t == "code":
            size, lines, overflow = R.fit_code(img.get("code", ""))
            detail = {"code_font": size, "code_lines": len(lines)}
        else:
            overflow = False
            detail = {}
        entry = {"index": i, "type": t, "overflow": overflow}
        entry.update(detail)
        per_image.append(entry)
        if overflow:
            overflows.append(i)

    return {
        "slug": slug,
        "image_count": len(imgs),
        "output_dir": out_path,
        "theme": theme,
        "cover_canvas": {"width": R.COVER_W, "height": R.COVER_H, "margin": R.COVER_MARGIN,
                         "footer_band": R.COVER_FOOTER_BAND},
        "slide_canvas": {"width": R.SLIDE_W, "height": R.SLIDE_H, "margin": R.SLIDE_MARGIN,
                         "footer_band": R.SLIDE_FOOTER_BAND},
        "cover": cover_spec,
        "images": per_image,
        "overflows": overflows,
    }


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Emit a medium-imager design spec (for review-first preview).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("images_json", help="Path to images.json file.")
    p.add_argument("--path", default="(unset)", help="Planned output directory.")
    p.add_argument("--theme", default=R.DEFAULT_THEME,
                   help=f"Planned theme (default: {R.DEFAULT_THEME}).")
    p.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = p.parse_args(argv)

    try:
        spec = build_spec(args.images_json, args.path, args.theme)
    except (SCHEMA.SchemaError, ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(spec, indent=2))
        return 3 if spec["overflows"] else 0

    print("MEDIUM-IMAGER DESIGN SPEC")
    print(f"  slug:        {spec['slug']}")
    print(f"  images:      {spec['image_count']} inner + 1 cover")
    print(f"  output dir:  {spec['output_dir']}")
    print(f"  theme:       {spec['theme']}")
    print(f"  cover canvas: {spec['cover_canvas']['width']}x{spec['cover_canvas']['height']} "
          f"(margin {spec['cover_canvas']['margin']}, footer band {spec['cover_canvas']['footer_band']})")
    print(f"  slide canvas: {spec['slide_canvas']['width']}x{spec['slide_canvas']['height']} "
          f"(margin {spec['slide_canvas']['margin']}, footer band {spec['slide_canvas']['footer_band']})")
    c = spec["cover"]
    flag = "  <-- OVERFLOW" if c["overflow"] else ""
    print(f"  cover fit:   title {c['title_font']}px ({c['title_lines']} ln) / "
          f"subtitle {c['subtitle_font']}px ({c['subtitle_lines']} ln){flag}")
    print("  per-image fit:")
    for s in spec["images"]:
        flag = "  <-- OVERFLOW" if s["overflow"] else ""
        print(f"    image {s['index']:>2} [{s['type']:>7}]: {s}{flag}")
    if spec["overflows"]:
        print(f"\n  WARNING: item(s) {spec['overflows']} overflow — shorten copy "
              "or split them before rendering all.", file=sys.stderr)
        return 3
    print("\n  JSON:")
    print(json.dumps(spec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
