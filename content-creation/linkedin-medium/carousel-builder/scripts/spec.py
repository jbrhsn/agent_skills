#!/usr/bin/env python3
"""Emit a carousel design spec for the review-first preview step.

Reads a slides JSON file and prints a human-readable design spec plus a
machine-readable JSON block: canvas size, palette, font stack, slide count,
per-slide fit result (chosen font sizes / line counts / overflow flag). Use
this to show the user WHAT will be rendered before rendering everything.

Example:
    python3 spec.py linkedin/carousels/my-carousel/slides.json --path linkedin/carousels/my-carousel --render svg
"""
import argparse
import json
import sys

import render_svg as R  # shared layout constants + fit logic


def build_spec(slides_json_path, out_path, render_path):
    slug, slides = R.load_slides(slides_json_path)
    total = len(slides)
    per_slide = []
    overflows = []
    for i, slide in enumerate(slides, start=1):
        t_size, b_size, t_lines, b_lines, overflow = R.fit_slide(
            slide.get("title", ""), slide.get("body", "")
        )
        per_slide.append({
            "index": i,
            "title_font": t_size,
            "body_font": b_size,
            "title_lines": len(t_lines),
            "body_lines": len(b_lines),
            "overflow": overflow,
        })
        if overflow:
            overflows.append(i)
    return {
        "slug": slug,
        "slide_count": total,
        "render_path": render_path,
        "output_dir": out_path,
        "canvas": {"width": R.CANVAS_W, "height": R.CANVAS_H, "margin": R.MARGIN,
                   "footer_band": R.FOOTER_BAND},
        "palette": {"bg": R.BG, "accent": R.ACCENT, "title": R.TITLE_COLOR,
                    "body": R.BODY_COLOR, "footer": R.FOOTER_COLOR},
        "font_stack": R.FONT_STACK,
        "slides": per_slide,
        "overflows": overflows,
    }


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Emit a carousel design spec (for review-first preview).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("slides_json", help="Path to slides JSON file.")
    p.add_argument("--path", default="(unset)", help="Planned output directory.")
    p.add_argument("--render", default="svg", choices=["svg", "html"],
                   help="Planned render path.")
    p.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = p.parse_args(argv)

    spec = build_spec(args.slides_json, args.path, args.render)

    if args.json:
        print(json.dumps(spec, indent=2))
        return 0

    print("CAROUSEL DESIGN SPEC")
    print(f"  slug:        {spec['slug']}")
    print(f"  slides:      {spec['slide_count']}")
    print(f"  render path: {spec['render_path']}")
    print(f"  output dir:  {spec['output_dir']}")
    print(f"  canvas:      {spec['canvas']['width']}x{spec['canvas']['height']} "
          f"(margin {spec['canvas']['margin']}, footer band {spec['canvas']['footer_band']})")
    print(f"  palette:     {spec['palette']}")
    print(f"  font:        {spec['font_stack']}")
    print("  per-slide fit:")
    for s in spec["slides"]:
        flag = "  <-- OVERFLOW" if s["overflow"] else ""
        print(f"    slide {s['index']:>2}: title {s['title_font']}px "
              f"({s['title_lines']} ln) / body {s['body_font']}px "
              f"({s['body_lines']} ln){flag}")
    if spec["overflows"]:
        print(f"\n  WARNING: slides {spec['overflows']} overflow — shorten copy "
              "or split them before rendering all.", file=sys.stderr)
        return 3
    print("\n  JSON:")
    print(json.dumps(spec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
