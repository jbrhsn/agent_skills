#!/usr/bin/env python3
"""Carousel render CLI: deck spec -> numbered PNG slides (+ merged PDF).

Pipeline:
  1. Verify `uv` is on PATH. If missing, STOP and ask the user to install it
     (never silently fall back to pip/venv).
  2. Load + JSON-schema-validate the deck spec (fail fast with slide index +
     offending field).
  3. Load + validate the theme; run a WCAG AA contrast check (warn, not fatal).
  4. Resolve the format preset (square | portrait | landscape) to canvas dims.
  5. Per slide: run the character-budget lint, render templates/{type}.html via
     Jinja2 with slide data + theme tokens + canvas dims + local @font-face
     file:// refs into a temp HTML file.
  6. Playwright (headless Chromium) opens each HTML, waits for document.fonts.ready,
     screenshots the #canvas element at exact pixel dims (explicit deviceScaleFactor).
  7. Write numbered PNGs to <out>/<slug>/<format>/NN_<type>.png.
  8. Auto-merge PNGs into a single PDF (unless --no-pdf) via img2pdf.

Modes:
   --spec-only   Emit the design spec (canvas, theme, contrast, per-slide lint)
                 and exit WITHOUT rendering. Use for the review-first gate.
   --only N      Render only slide N (1-based). Use for a slide-1 preview.

Note: Content overflow is auto-scaled (min 0.7x) to guarantee everything fits
within bounds during rendering — text becomes smaller but never clips.

Examples:
  uv run python -m engine.render --deck examples/example_deck.yaml --spec-only
  uv run python -m engine.render --deck examples/example_deck.yaml --format portrait --only 1
  uv run python -m engine.render --deck examples/example_deck.yaml --theme dark_navy --out ./output
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SCHEMA_PATH = os.path.join(HERE, "deck_schema.json")

# Allow running as a script (python engine/render.py) or module (-m engine.render).
if __package__ in (None, ""):
    sys.path.insert(0, ROOT)
    from engine import layout_engine, theme_loader  # type: ignore
else:
    from . import layout_engine, theme_loader


def check_uv() -> bool:
    return shutil.which("uv") is not None


def slugify(text: str) -> str:
    import re
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "carousel"


def load_deck(path: str) -> dict:
    import yaml
    with open(path, "r", encoding="utf-8") as fh:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(fh)
        return json.load(fh)


def validate_deck(deck: dict) -> None:
    import jsonschema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(deck), key=lambda e: list(e.absolute_path))
    if not errors:
        return
    msgs = []
    for e in errors:
        loc = list(e.absolute_path)
        where = "deck"
        if len(loc) >= 2 and loc[0] == "slides":
            where = f"slide {loc[1] + 1}" + (f" field '{loc[-1]}'" if len(loc) > 2 else "")
        elif loc:
            where = " -> ".join(str(p) for p in loc)
        message = e.message
        # For a oneOf failure on a known slide type, surface the most specific
        # sub-error (e.g. the actual missing required field) instead of the
        # generic "is not valid under any of the given schemas".
        if e.context:
            stype = e.instance.get("type") if isinstance(e.instance, dict) else None
            best = None
            for sub in e.context:
                if stype and sub.schema.get("properties", {}).get("type", {}).get("const") == stype:
                    best = sub
                    break
            if best is not None:
                message = best.message
        msgs.append(f"  [{where}] {message}")
    raise ValueError("deck spec failed validation:\n" + "\n".join(msgs))


def build_spec(deck: dict, theme: dict, preset: dict) -> dict:
    slides = deck["slides"]
    per_slide = []
    all_warnings: list[str] = []
    for i, slide in enumerate(slides, start=1):
        warns = layout_engine.lint_slide(slide, i)
        all_warnings.extend(warns)
        per_slide.append({"index": i, "type": slide["type"], "warnings": warns})
    report, contrast_pass = theme_loader.contrast_report(theme)
    return {
        "title": deck["meta"]["title"],
        "slug": deck["meta"].get("slug") or slugify(deck["meta"]["title"]),
        "theme": theme.get("name"),
        "format": preset["name"],
        "canvas": {"width": preset["width"], "height": preset["height"], "margin": preset["margin"]},
        "slide_count": len(slides),
        "fonts": layout_engine.bundled_families(),
        "contrast_report": report,
        "contrast_pass": contrast_pass,
        "slides": per_slide,
        "warnings": all_warnings,
    }


def print_spec(spec: dict) -> None:
    print("CAROUSEL DESIGN SPEC")
    print(f"  title:   {spec['title']}")
    print(f"  slug:    {spec['slug']}")
    print(f"  theme:   {spec['theme']}")
    print(f"  format:  {spec['format']} "
          f"({spec['canvas']['width']}x{spec['canvas']['height']}, margin {spec['canvas']['margin']})")
    print(f"  slides:  {spec['slide_count']}")
    print(f"  fonts:   {', '.join(spec['fonts']) or '(none bundled — run font setup!)'}")
    print("  " + spec["contrast_report"].replace("\n", "\n  "))
    print("  per-slide:")
    for s in spec["slides"]:
        flag = "  <-- OVERFLOW RISK" if s["warnings"] else ""
        print(f"    slide {s['index']:>2}: {s['type']}{flag}")
    if spec["warnings"]:
        print("\n  WARNINGS:", file=sys.stderr)
        for w in spec["warnings"]:
            print(f"    - {w}", file=sys.stderr)


def _auto_fit_content(page, preset: dict) -> float:
    """Measure content and scale down if it overflows the safe zone."""
    safe_height = preset["height"] - 2 * preset["margin"]
    measure_js = f"""
    (() => {{
        const pad = document.querySelector('.pad');
        if (!pad) return 1.0;
        const scrollHeight = pad.scrollHeight;
        if (scrollHeight <= {safe_height}) return 1.0;
        return Math.max(0.7, {safe_height} / scrollHeight);
    }})()
    """
    fit_scale = 1.0
    for step_num in range(6):
        fit_scale = max(0.7, 1.0 - (0.05 * step_num))
        page.evaluate(f"document.documentElement.style.setProperty('--fit', '{fit_scale}')")
        page.wait_for_timeout(100)
        measured = page.evaluate(measure_js)
        if measured >= fit_scale:
            break
    return fit_scale


def render_pngs(deck: dict, theme: dict, preset: dict, out_dir: str,
                only: int | None, scale: float) -> list[str]:
    from playwright.sync_api import sync_playwright
    
    env = layout_engine.make_env()
    font_face_css = layout_engine.build_font_face_css()
    meta = deck["meta"]
    slides = deck["slides"]
    total = len(slides)
    os.makedirs(out_dir, exist_ok=True)

    written: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": preset["width"], "height": preset["height"]},
            device_scale_factor=scale,
        )
        for i, slide in enumerate(slides, start=1):
            if only is not None and i != only:
                continue
            html = layout_engine.render_html(
                env, slide, theme, preset, meta, i, total, font_face_css
            )
            with tempfile.NamedTemporaryFile(
                "w", suffix=".html", delete=False, encoding="utf-8"
            ) as tf:
                tf.write(html)
                tmp_path = tf.name
            try:
                page.goto("file://" + tmp_path)
                page.wait_for_selector("#canvas")
                page.evaluate("async () => { await document.fonts.ready; }")
                
                # Auto-fit: measure content and scale down if it overflows the safe zone
                fit_scale = _auto_fit_content(page, preset)
                
                out_name = f"{i:02d}_{slide['type']}.png"
                out_path = os.path.join(out_dir, out_name)
                page.locator("#canvas").screenshot(path=out_path)
                written.append(out_path)
            finally:
                os.unlink(tmp_path)
        browser.close()
    return written


def merge_pdf(pngs: list[str], out_pdf: str) -> None:
    import img2pdf
    with open(out_pdf, "wb") as fh:
        fh.write(img2pdf.convert(pngs))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a carousel deck spec to numbered PNG slides (+ PDF).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--deck", required=True, help="Path to deck spec (.yaml or .json).")
    parser.add_argument("--theme", default=None,
                        help="Theme name or path. Overrides meta.theme.")
    parser.add_argument("--format", default=None,
                        choices=list(layout_engine.FORMAT_PRESETS),
                        help="Canvas format. Overrides meta.format (default portrait).")
    parser.add_argument("--out", default=os.path.join(ROOT, "output"),
                        help="Output root directory (default: output/).")
    parser.add_argument("--only", type=int, default=None,
                        help="Render only slide N (1-based); use for slide-1 preview.")
    parser.add_argument("--scale", type=float, default=2.0,
                        help="deviceScaleFactor for retina-quality PNGs (default 2).")
    parser.add_argument("--spec-only", action="store_true",
                        help="Emit the design spec and exit without rendering.")
    parser.add_argument("--no-pdf", action="store_true",
                        help="Skip the automatic PNG->PDF merge.")
    args = parser.parse_args(argv)

    if not check_uv():
        print(
            "error: `uv` is not on PATH. This skill requires uv (per project policy;\n"
            "it never falls back to pip). Install it, then re-run:\n"
            "  curl -LsSf https://astral.sh/uv/install.sh | sh\n"
            "  # or: pipx install uv   /   brew install uv\n"
            "Then: uv sync && uv run playwright install chromium",
            file=sys.stderr,
        )
        return 2

    try:
        deck = load_deck(args.deck)
        validate_deck(deck)
    except Exception as e:  # noqa: BLE001 - surface a clean message
        print(f"error: {e}", file=sys.stderr)
        return 1

    theme_ref = args.theme or deck["meta"].get("theme")
    fmt = args.format or deck["meta"].get("format", "portrait")
    try:
        theme = theme_loader.load_theme(theme_ref)
        preset = layout_engine.resolve_format(fmt)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1

    spec = build_spec(deck, theme, preset)
    print_spec(spec)
    if not spec["contrast_pass"]:
        print("\nWARNING: theme fails WCAG AA contrast for some text pairs (see above).",
              file=sys.stderr)

    if args.spec_only:
        return 0

    out_dir = os.path.join(args.out, spec["slug"], preset["name"])
    try:
        pngs = render_pngs(deck, theme, preset, out_dir, args.only, args.scale)
    except Exception as e:  # noqa: BLE001
        print(f"error during render: {e}", file=sys.stderr)
        return 1

    for p in pngs:
        print(f"wrote {p}")
    print(f"\n{len(pngs)} PNG slide(s) written to {out_dir}")

    do_pdf = not args.no_pdf and args.only is None
    if do_pdf and pngs:
        out_pdf = os.path.join(out_dir, f"{spec['slug']}.pdf")
        try:
            merge_pdf(sorted(pngs), out_pdf)
            print(f"wrote {out_pdf}")
        except Exception as e:  # noqa: BLE001
            print(f"warning: PDF merge failed ({e}); PNGs are valid on their own.",
                  file=sys.stderr)
    elif args.only is not None:
        print("(slide-only preview: skipping PDF merge)")

    if spec["warnings"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
