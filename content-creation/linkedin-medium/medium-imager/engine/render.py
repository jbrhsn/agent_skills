#!/usr/bin/env python3
"""Medium-imager render CLI: image spec -> numbered PNG files.

Modes:
  Manual: --spec <path> (YAML/JSON) -> validate -> render
  Auto:   --draft <path> --auto -> parse -> emit placement proposal -> confirm -> render
  
Pipeline:
  1. Verify uv on PATH.
  2. Load + validate spec (manual) or draft (auto).
  3. Load + validate theme; run WCAG contrast check (warn, not fatal).
  4. Emit design spec.
  5. --spec-only exits after step 4.
  6. --only <cover|N> renders single preview.
  7. Playwright screenshots per image.
  8. Write numbered PNGs to medium/images/<slug>/.

Examples:
  uv run python -m engine.render --spec images.yaml --spec-only
  uv run python -m engine.render --spec images.yaml --only cover
  uv run python -m engine.render --draft article.md --auto
  uv run python -m engine.render --spec images.yaml --theme techdocs_mono
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SCHEMA_PATH = os.path.join(HERE, "spec_schema.json")

# Allow running as a script (python engine/render.py) or module (-m engine.render).
if __package__ in (None, ""):
    sys.path.insert(0, ROOT)
    from engine import layout_engine, theme_loader, draft_parser, placement_engine  # type: ignore
else:
    from . import layout_engine, theme_loader, draft_parser, placement_engine


def check_uv() -> bool:
    return shutil.which("uv") is not None


def slugify(text: str) -> str:
    import re
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "medium-article"


def load_spec(path: str) -> dict:
    """Load a spec file (YAML or JSON).
    
    Args:
        path: Path to spec file. YAML (.yaml, .yml) is preferred; JSON also supported.
        
    Returns:
        Parsed spec dict.
        
    Raises:
        FileNotFoundError: If spec file does not exist.
        ValueError: If file cannot be parsed as YAML or JSON.
    """
    with open(path, "r", encoding="utf-8") as fh:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(fh) or {}
        
        # Try JSON parsing with helpful error message
        content = fh.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"failed to parse {path!r} as JSON: {e.msg}\n"
                f"Ensure the file is valid JSON, or rename it with .yaml/.yml extension for YAML parsing."
            ) from e


def validate_spec(spec: dict) -> None:
    """Validate spec against spec_schema.json."""
    import jsonschema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(spec), key=lambda e: list(e.absolute_path))
    if not errors:
        return
    msgs = []
    for e in errors:
        loc = list(e.absolute_path)
        where = "spec"
        if len(loc) >= 1 and loc[0] == "images":
            where = f"image {loc[1] + 1}" + (f" field '{loc[-1]}'" if len(loc) > 2 else "")
        elif loc:
            where = " -> ".join(str(p) for p in loc)
        msgs.append(f"  [{where}] {e.message}")
    raise ValueError("spec failed validation:\n" + "\n".join(msgs))


def build_spec(spec: dict, theme: dict, is_cover: bool = True) -> dict:
    """Build a design spec (canvas dims, per-image lint, contrast, etc.)."""
    images = spec.get("images", [])
    meta = spec.get("meta", {})
    
    per_image = []
    all_warnings: list[str] = []
    
    # Cover spec
    cover_ratio = meta.get("cover", {}).get("ratio")
    if is_cover:
        cover_preset = layout_engine.resolve_cover_ratio(cover_ratio)
        cover_warns = layout_engine.lint_image(meta.get("cover", {}), 0, cover_ratio)
        all_warnings.extend(cover_warns)
        per_image.append({"index": 0, "type": "cover", "warnings": cover_warns})
    
    # Per-image specs
    for i, img in enumerate(images, start=1):
        img_type = img.get("type")
        warns = layout_engine.lint_image(img, i, cover_ratio)
        all_warnings.extend(warns)
        per_image.append({"index": i, "type": img_type, "warnings": warns})
    
    # Contrast check
    report, contrast_pass = theme_loader.contrast_report(theme)
    
    slug = meta.get("slug") or slugify(meta.get("title", "article"))
    
    return {
        "slug": slug,
        "theme": theme.get("name"),
        "cover_ratio": cover_ratio or "wide",
        "image_count": len(images),
        "fonts": layout_engine.bundled_families(),
        "contrast_report": report,
        "contrast_pass": contrast_pass,
        "images": per_image,
        "warnings": all_warnings,
    }


def print_spec(spec: dict) -> None:
    """Print the design spec in human-readable format."""
    print("MEDIUM-IMAGER DESIGN SPEC")
    print(f"  title:   {spec.get('slug')}")
    print(f"  theme:   {spec['theme']}")
    print(f"  images:  {spec['image_count']} + 1 cover")
    print(f"  fonts:   {', '.join(spec['fonts']) or '(none bundled — run uv sync!)'}")
    print("  " + spec["contrast_report"].replace("\n", "\n  "))
    print("  per-image:")
    for s in spec["images"]:
        flag = "  <-- OVERFLOW RISK" if s["warnings"] else ""
        print(f"    image {s['index']:>2}: {s['type']}{flag}")
    if spec["warnings"]:
        print("\n  WARNINGS:", file=sys.stderr)
        for w in spec["warnings"]:
            print(f"    - {w}", file=sys.stderr)


def proposals_to_spec(proposals: list[dict], front_matter: dict) -> dict:
    """Convert placement proposals to a valid spec dict.
    
    Args:
        proposals: list of proposal dicts from placement_engine.generate_proposal()
        front_matter: parsed YAML front-matter from the draft
    
    Returns:
        A spec dict ready for validate_spec() and render_pngs()
    
    The conversion strategy:
    - Extract cover proposal (always first and type='cover')
    - All other proposals become images in order
    - Use title from front_matter or generate a fallback
    - Use theme from front_matter or default to 'clean_minimal'
    
    Raises:
        ValueError: if no proposals, no cover proposal, or no title found
    """
    if not proposals:
        raise ValueError(
            "No proposals to render.\n"
            "Ensure the draft has:\n"
            "  - A YAML front-matter with 'title', or an H1 heading\n"
            "  - At least one section: blockquotes, code blocks, tables, or headings"
        )
    
    # Extract and validate cover
    cover_proposal = None
    image_proposals = []
    
    for p in proposals:
        if p["type"] == "cover":
            cover_proposal = p
        else:
            image_proposals.append(p)
    
    if not cover_proposal:
        raise ValueError(
            "No cover proposal found.\n"
            "Ensure the draft has:\n"
            "  - A YAML front-matter with 'title', or\n"
            "  - An H1 heading (# Title)"
        )
    
    # Build meta
    title = front_matter.get("title") or cover_proposal.get("content", {}).get("title")
    if not title or not title.strip():
        raise ValueError(
            "No title found for cover image.\n"
            "Provide one of:\n"
            "  - YAML front-matter with 'title: ...'\n"
            "  - An H1 heading (# Title)"
        )
    
    meta = {
        "title": title.strip(),
        "slug": slugify(title),
        "theme": front_matter.get("theme", "clean_minimal"),
        "cover": {
            "subtitle": cover_proposal.get("content", {}).get("subtitle"),
            "ratio": front_matter.get("cover", {}).get("ratio", "wide"),
        },
    }
    
    # Remove None subtitle to keep spec clean
    if meta["cover"]["subtitle"] is None:
        del meta["cover"]["subtitle"]
    
    # Build images from proposals
    images = []
    for proposal in image_proposals:
        img_type = proposal["type"]
        content = proposal.get("content", {})
        
        # Convert proposal content to spec-compliant image.
        # Note: All data comes directly from AST extraction, so we trust it's well-formed.
        # TODO: future enhancements
        #   - Allow user to review/edit proposals before rendering (--review-proposals flag)
        #   - Add --skip-low-confidence to filter out 'low' confidence proposals
        #   - Support mdit_py_plugins.tables for Markdown table detection
        
        if img_type == "section_divider":
            images.append({"type": "section_divider", "label": content.get("label", "")})
        
        elif img_type == "quote_block":
            img = {"type": "quote_block", "quote": content.get("quote", "")}
            if content.get("attribution"):
                img["attribution"] = content["attribution"]
            images.append(img)
        
        elif img_type == "stat_callout":
            img = {
                "type": "stat_callout",
                "value": content.get("value", ""),
                "label": content.get("label", ""),
            }
            if content.get("context"):
                img["context"] = content["context"]
            images.append(img)
        
        elif img_type == "comparison_table":
            images.append({
                "type": "comparison_table",
                "title_left": content.get("title_left", ""),
                "title_right": content.get("title_right", ""),
                "rows": content.get("rows", []),
            })
        
        elif img_type == "code_card":
            img = {"type": "code_card", "code": content.get("code", "")}
            if content.get("language"):
                img["language"] = content["language"]
            images.append(img)
        
        elif img_type == "linear_flow":
            images.append({
                "type": "linear_flow",
                "steps": content.get("steps", []),
            })
        
        elif img_type == "branch_2way":
            images.append({
                "type": "branch_2way",
                "left_label": content.get("left_label", ""),
                "right_label": content.get("right_label", ""),
                "left_items": content.get("left_items", []),
                "right_items": content.get("right_items", []),
            })
        
        elif img_type == "stage_cycle":
            images.append({
                "type": "stage_cycle",
                "stages": content.get("stages", []),
            })
    
    return {
        "meta": meta,
        "images": images,
    }


def render_pngs(spec: dict, theme: dict, cover_ratio: str | None, out_dir: str,
                 only: int | str | None, scale: float, slug: str | None = None) -> list[str]:
    """Render spec to PNG files via Playwright."""
    from playwright.sync_api import sync_playwright
    
    env = layout_engine.make_env()
    font_face_css = layout_engine.build_font_face_css()
    meta = spec.get("meta", {})
    images = spec.get("images", [])
    
    os.makedirs(out_dir, exist_ok=True)
    written: list[str] = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Render cover
        if only is None or only == "cover" or (isinstance(only, int) and only == 0):
            cover_preset = layout_engine.resolve_cover_ratio(cover_ratio)
            page = browser.new_page(
                viewport={"width": cover_preset["width"], "height": cover_preset["height"]},
                device_scale_factor=scale,
            )
            html = layout_engine.render_html(
                env, meta.get("cover", {}), theme, cover_ratio, 1, len(images) + 1,
                font_face_css, is_cover=True
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
                
                use_slug = slug or meta.get("slug", "article")
                out_name = f"{use_slug}-cover.png"
                out_path = os.path.join(out_dir, out_name)
                page.locator("#canvas").screenshot(path=out_path)
                written.append(out_path)
            finally:
                os.unlink(tmp_path)
            page.close()
        
        # Render images
        for i, img in enumerate(images, start=1):
            if only is not None and only != i:
                continue
            
            img_type = img.get("type")
            
            # Determine canvas size
            inline_preset = {
                "width": layout_engine.INLINE_WIDTH,
                "height": layout_engine.INLINE_HEIGHT_PRESETS.get(img_type, 600),
            }
            
            page = browser.new_page(
                viewport={"width": inline_preset["width"], "height": inline_preset["height"]},
                device_scale_factor=scale,
            )
            
            html = layout_engine.render_html(
                env, img, theme, cover_ratio, i + 1, len(images) + 1,
                font_face_css, is_cover=False
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
                
                use_slug = slug or meta.get("slug", "article")
                out_name = f"{use_slug}-{i:02d}-{img_type}.png"
                out_path = os.path.join(out_dir, out_name)
                page.locator("#canvas").screenshot(path=out_path)
                written.append(out_path)
            finally:
                os.unlink(tmp_path)
            page.close()
        
        browser.close()
    
    return written


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a Medium-imager spec to numbered PNG image files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--spec", default=None,
                        help="Path to manual image spec (YAML or JSON). Mutually exclusive with --draft.")
    parser.add_argument("--draft", default=None,
                        help="Path to a Markdown draft for auto-placement. Mutually exclusive with --spec.")
    parser.add_argument("--auto", action="store_true",
                        help="Use auto-placement mode (requires --draft). Emits a proposal for user confirmation.")
    parser.add_argument("--theme", default=None,
                        help="Theme name or path. Overrides spec's meta.theme.")
    parser.add_argument("--out", default=None,
                        help="Output directory (default: medium/images/<slug>).")
    parser.add_argument("--only", default=None,
                        help="Render only 'cover' or an image N (1-based); use for previews.")
    parser.add_argument("--scale", type=float, default=2.0,
                        help="PNG rasterization scale (default 2.0 = retina).")
    parser.add_argument("--spec-only", action="store_true",
                        help="Emit the design spec and exit without rendering.")
    args = parser.parse_args(argv)
    
    if not check_uv():
        print(
            "error: `uv` is not on PATH. This skill requires uv.\n"
            "Install it: curl -LsSf https://astral.sh/uv/install.sh | sh\n"
            "Then: uv sync && uv run playwright install chromium",
            file=sys.stderr,
        )
        return 2
    
    # Load spec
    try:
        if args.spec:
            spec = load_spec(args.spec)
            validate_spec(spec)
        elif args.draft and args.auto:
            with open(args.draft, "r", encoding="utf-8") as fh:
                draft_text = fh.read()
            front_matter, ast = draft_parser.parse_draft(draft_text)
            proposals = placement_engine.generate_proposal(front_matter, ast)
            
            # Print proposals for user review
            print("AUTO-PLACEMENT PROPOSAL (auto-confirming for rendering):")
            for p in proposals:
                conf_mark = "✓" if p["confidence"] == "high" else "?"
                print(f"  [{conf_mark}] {p['type']}: {p['reason']}")
            
            # Convert proposals to spec (auto-confirm for now)
            spec = proposals_to_spec(proposals, front_matter)
            validate_spec(spec)
            print(f"\nGenerated spec for: {spec['meta']['title']}")
            print(f"  {len(spec['images'])} images to render")
        else:
            print("error: provide either --spec or (--draft --auto)", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    
    # Load theme
    try:
        theme_ref = args.theme or spec["meta"].get("theme", "clean_minimal")
        theme = theme_loader.load_theme(theme_ref)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    
    # Build spec
    try:
        cover_ratio = spec["meta"].get("cover", {}).get("ratio")
        spec_report = build_spec(spec, theme)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    
    # Print spec
    print_spec(spec_report)
    if not spec_report["contrast_pass"]:
        print("\nWARNING: theme fails WCAG AA contrast (see above).", file=sys.stderr)
    
    if args.spec_only:
        return 0
    
    # Determine output directory
    if args.out:
        out_dir = args.out
    else:
        slug = spec_report["slug"]
        out_dir = os.path.join("medium", "images", slug)
    
    # Render PNGs
    try:
        parse_only = None
        if args.only:
            if args.only.lower() == "cover":
                parse_only = "cover"
            else:
                try:
                    parse_only = int(args.only)
                except ValueError:
                    print(f"error: --only must be 'cover' or an integer, got {args.only!r}", file=sys.stderr)
                    return 1
        
        pngs = render_pngs(spec, theme, cover_ratio, out_dir, parse_only, args.scale, slug=spec_report["slug"])
    except Exception as e:
        print(f"error during render: {e}", file=sys.stderr)
        return 1
    
    for p in pngs:
        print(f"wrote {p}")
    print(f"\n{len(pngs)} PNG file(s) written to {out_dir}")
    
    if spec_report["warnings"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
