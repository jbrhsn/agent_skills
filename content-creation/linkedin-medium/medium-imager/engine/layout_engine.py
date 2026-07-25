#!/usr/bin/env python3
"""Layout engine: fill Jinja2 image templates with image data + theme tokens.

Responsibilities:
  - Resolve cover ratio presets (wide/square/16:9) to canvas dims.
  - Define inline image width (1400px fixed) and per-type height presets.
  - Build local @font-face CSS block from bundled WOFF2 files (file:// refs).
  - Provide a Jinja2 environment with bundled icons as inline SVG via currentColor.
  - Run per-field character-budget lint per image type and warn on overflow.
  - Render templates/{type}.html into self-contained HTML strings.

Requires jinja2 (installed via uv).
"""
from __future__ import annotations

import glob
import os
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from . import code_highlight

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
FONTS_DIR = os.path.join(ROOT, "assets", "fonts")
ICONS_DIR = os.path.join(ROOT, "assets", "icons")

# Cover canvas presets: width fixed at 1200, height varies by ratio
COVER_RATIOS = {
    "wide": {"width": 1200, "height": 680, "name": "wide (1.76:1)"},
    "square": {"width": 1200, "height": 1200, "name": "square (1:1)"},
    "16:9": {"width": 1280, "height": 720, "name": "16:9"},
}
DEFAULT_COVER_RATIO = "wide"

# In-article images: width fixed at 1400, height varies per type
INLINE_WIDTH = 1400
INLINE_HEIGHT_PRESETS = {
    "section_divider": 200,
    "stat_callout": 500,
    "quote_block": 600,
    "comparison_table": 800,
    "code_card": 600,
    "linear_flow": 700,
    "branch_2way": 700,
    "stage_cycle": 700,
}

# Character budgets per (image type, field) for overflow lint
CHAR_BUDGETS = {
    "section_divider": {"label": 60},
    "stat_callout": {"value": 40, "label": 80, "context": 150},
    "quote_block": {"quote": 300, "attribution": 80},
    "comparison_table": {"title_left": 40, "title_right": 40, "_row_cell": 60},
    "code_card": {"code": 2000},
    "linear_flow": {"_step": 80},
    "branch_2way": {"left_label": 40, "right_label": 40, "_item": 60},
    "stage_cycle": {"_stage": 60},
}

# Code line-count soft max (warning threshold)
CODE_MAX_LINES = 25


def resolve_cover_ratio(ratio: str | None) -> dict:
    """Resolve a cover ratio to canvas dimensions."""
    r = ratio or DEFAULT_COVER_RATIO
    if r not in COVER_RATIOS:
        raise ValueError(
            f"unknown cover ratio {r!r}; choose one of {', '.join(COVER_RATIOS)}"
        )
    preset = dict(COVER_RATIOS[r])
    preset["ratio_key"] = r
    return preset


def _font_family_files() -> dict[str, list[str]]:
    """Map a family name (folder under assets/fonts) to its woff2 files."""
    families: dict[str, list[str]] = {}
    if not os.path.isdir(FONTS_DIR):
        return families
    for entry in sorted(os.listdir(FONTS_DIR)):
        fam_dir = os.path.join(FONTS_DIR, entry)
        if os.path.isdir(fam_dir):
            files = sorted(glob.glob(os.path.join(fam_dir, "*.woff2")))
            if files:
                families[entry] = files
    return families


_WEIGHT_RE = re.compile(
    r"(thin|100|extralight|200|light|300|regular|400|medium|500|"
    r"semibold|600|bold|700|extrabold|800|black|900)", re.I
)
_WEIGHT_MAP = {
    "thin": 100, "extralight": 200, "light": 300, "regular": 400, "medium": 500,
    "semibold": 600, "bold": 700, "extrabold": 800, "black": 900,
}


def _weight_from_filename(path: str) -> int:
    stem = os.path.splitext(os.path.basename(path))[0].lower()
    m = _WEIGHT_RE.search(stem)
    if not m:
        return 400
    token = m.group(1).lower()
    if token.isdigit():
        return int(token)
    return _WEIGHT_MAP.get(token, 400)


def build_font_face_css() -> str:
    """Emit @font-face rules for every bundled font, keyed by family name."""
    rules = []
    for family, files in _font_family_files().items():
        for path in files:
            weight = _weight_from_filename(path)
            uri = "file://" + path.replace(os.sep, "/")
            rules.append(
                "@font-face{"
                f"font-family:'{family}';"
                f"src:url('{uri}') format('woff2');"
                f"font-weight:{weight};font-style:normal;font-display:block;"
                "}"
            )
    return "\n".join(rules)


def bundled_families() -> list[str]:
    return list(_font_family_files().keys())


def bundled_icons() -> list[str]:
    """Return list of available icon names from assets/icons/."""
    if not os.path.isdir(ICONS_DIR):
        return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(ICONS_DIR)
                  if f.endswith(".svg"))


def icon_svg(name: str) -> Markup:
    """Return the inline SVG for an icon by name (uses currentColor), marked safe."""
    path = os.path.join(ICONS_DIR, f"{name}.svg")
    if not os.path.isfile(path):
        return Markup("")
    with open(path, "r", encoding="utf-8") as fh:
        return Markup(fh.read())


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["icon"] = icon_svg
    return env


def lint_image(image: dict, index: int, cover_ratio: str | None = None) -> list[str]:
    """Return human-readable overflow warnings for one image (never fatal).
    
    Checks include:
    - Character budgets for text fields (warn if likely to overflow)
    - Code line count (warn if likely to need two images)
    """
    img_type = image.get("type")
    budgets = CHAR_BUDGETS.get(img_type, {})
    warnings: list[str] = []

    for field, limit in budgets.items():
        if field.startswith("_"):
            continue
        val = image.get(field)
        if isinstance(val, str) and len(val) > limit:
            warnings.append(
                f"image {index} ({img_type}): '{field}' is {len(val)} chars "
                f"(budget {limit}); may overflow — shorten or split."
            )

    # Row-cell budget for comparison_table
    row_limit = budgets.get("_row_cell")
    if row_limit:
        for i, row in enumerate(image.get("rows", []) or []):
            for j, cell in enumerate(row or []):
                if isinstance(cell, str) and len(cell) > row_limit:
                    warnings.append(
                        f"image {index} ({img_type}): row {i} cell {j} is {len(cell)} chars "
                        f"(budget {row_limit}); may overflow."
                    )

    # Step/item budget for multi-item types
    step_limit = budgets.get("_step")
    if step_limit:
        for i, step in enumerate(image.get("steps", []) or []):
            if isinstance(step, str) and len(step) > step_limit:
                warnings.append(
                    f"image {index} ({img_type}): step {i} is {len(step)} chars "
                    f"(budget {step_limit}); may overflow."
                )

    item_limit = budgets.get("_item")
    if item_limit:
        for key in ("left_items", "right_items"):
            for i, item in enumerate(image.get(key, []) or []):
                if isinstance(item, str) and len(item) > item_limit:
                    warnings.append(
                        f"image {index} ({img_type}): {key}[{i}] is {len(item)} chars "
                        f"(budget {item_limit}); may overflow."
                    )

    # Stage budget
    stage_limit = budgets.get("_stage")
    if stage_limit:
        for i, stage in enumerate(image.get("stages", []) or []):
            if isinstance(stage, str) and len(stage) > stage_limit:
                warnings.append(
                    f"image {index} ({img_type}): stage {i} is {len(stage)} chars "
                    f"(budget {stage_limit}); may overflow."
                )

    # Code line count warning
    if img_type == "code_card":
        code = image.get("code", "")
        lines = len(code.splitlines())
        if lines > CODE_MAX_LINES:
            warnings.append(
                f"image {index} (code_card): {lines} lines (over {CODE_MAX_LINES} suggest). "
                f"Consider splitting into two cards or trimming."
            )

    return warnings


def render_html(env: Environment, image: dict, theme: dict, cover_ratio: str | None,
                index: int, total: int, font_face_css: str, is_cover: bool = False) -> str:
    """Render an image spec to HTML using a Jinja2 template."""
    if is_cover:
        ratio_preset = resolve_cover_ratio(cover_ratio)
        template = env.get_template("cover.html")
        return template.render(
            image=image,
            theme=theme,
            colors=theme["colors"],
            fonts=theme["fonts"],
            decoration=theme.get("decoration", {}),
            canvas=ratio_preset,
            index=index,
            total=total,
            counter=f"{index}/{total}",
            font_face_css=Markup(font_face_css),
        )
    else:
        img_type = image.get("type")
        template = env.get_template(f"{img_type}.html")
        preset = {
            "width": INLINE_WIDTH,
            "height": INLINE_HEIGHT_PRESETS.get(img_type, 600),
        }
        
        # Prepare context for rendering
        context = {
            "image": image,
            "theme": theme,
            "colors": theme["colors"],
            "fonts": theme["fonts"],
            "decoration": theme.get("decoration", {}),
            "canvas": preset,
            "index": index,
            "total": total,
            "counter": f"{index}/{total}",
            "font_face_css": Markup(font_face_css),
        }
        
        # If this is a code_card, integrate syntax highlighting
        if img_type == "code_card":
            code = image.get("code")
            language = image.get("language")
            if code:
                pygments_style = theme.get("pygments_style", "default")
                try:
                    highlighted_html, highlight_css = code_highlight.highlight_code(
                        code, language, pygments_style
                    )
                    context["highlighted_html"] = Markup(highlighted_html)
                    context["highlight_css"] = highlight_css
                except Exception:
                    # Graceful fallback: if highlighting fails, pass nothing
                    # and template will render plain code
                    pass
        
        return template.render(**context)
