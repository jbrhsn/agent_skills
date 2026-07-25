#!/usr/bin/env python3
"""Layout engine: fill Jinja2 slide templates with slide data + theme tokens.

Responsibilities:
  - Resolve format presets (square / portrait / landscape) to canvas dims and a
    proportionally-scaled safe margin.
  - Build the local @font-face CSS block from bundled WOFF2 files (file:// refs)
    so rendering is deterministic regardless of the host machine's fonts.
  - Provide an icon() helper that inlines flat/line SVGs using currentColor so
    they inherit theme colors (marked safe to prevent HTML escaping).
  - Run a per-field character-budget lint per slide type and warn on likely
    overflow (actual fitting is handled by a JS auto-fit measurement pass in
    render.py that scales content until it fits the safe zone).
  - Render templates/{type}.html into a self-contained HTML string.

Requires jinja2 (installed via uv).
"""
from __future__ import annotations

import glob
import os
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
FONTS_DIR = os.path.join(ROOT, "assets", "fonts")
ICONS_DIR = os.path.join(ROOT, "assets", "icons")

FORMAT_PRESETS = {
    "square": {"width": 1080, "height": 1080},
    "portrait": {"width": 1080, "height": 1350},
    "landscape": {"width": 1920, "height": 1080},
}
BASE_WIDTH = 1080
BASE_MARGIN = 80

# Character budgets per (slide type, field). Warn when exceeded — content is
# likely to overflow the box even at the smallest theme font size.
CHAR_BUDGETS = {
    "title": {"headline": 90, "subheadline": 160, "kicker": 40},
    "comparison": {"title_left": 48, "title_right": 48, "_item": 60},
    "quote": {"quote": 240, "attribution": 60},
    "stat_grid": {"heading": 60, "_label": 40, "_detail": 60},
    "numbered_phase": {"title": 48, "body": 320, "callout_label": 40, "callout_body": 200},
    "process_loop": {"heading": 60, "_label": 32, "_detail": 60},
    "list_steps": {"heading": 60, "_item": 90},
    "cta": {"headline": 90, "subtext": 160, "action": 80},
}


def resolve_format(fmt: str) -> dict:
    if fmt not in FORMAT_PRESETS:
        raise ValueError(
            f"unknown format {fmt!r}; choose one of {', '.join(FORMAT_PRESETS)}"
        )
    preset = dict(FORMAT_PRESETS[fmt])
    scale = preset["width"] / BASE_WIDTH
    preset["margin"] = round(BASE_MARGIN * scale)
    preset["name"] = fmt
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
    """Emit @font-face rules for every bundled font, keyed by family name.

    The CSS font-family used in themes must match the folder name under
    assets/fonts/ (e.g. 'Space Grotesk' -> assets/fonts/Space Grotesk/).
    """
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


def lint_slide(slide: dict, index: int) -> list[str]:
    """Return human-readable overflow warnings for one slide (never fatal).
    
    Checks include:
    - Character budgets for text fields (warn if likely to overflow)
    - Icon name validation (warn if icon doesn't exist)
    """
    stype = slide.get("type")
    budgets = CHAR_BUDGETS.get(stype, {})
    warnings: list[str] = []
    available_icons = bundled_icons()

    for field, limit in budgets.items():
        if field.startswith("_"):
            continue
        val = slide.get(field)
        if isinstance(val, str) and len(val) > limit:
            warnings.append(
                f"slide {index} ({stype}): '{field}' is {len(val)} chars "
                f"(budget {limit}); may overflow — shorten or split."
            )

    # List-like fields share a per-item budget under the '_item'/'_label' keys.
    item_limit = budgets.get("_item")
    if item_limit:
        for key in ("items", "items_left", "items_right"):
            for i, it in enumerate(slide.get(key, []) or []):
                if isinstance(it, str) and len(it) > item_limit:
                    warnings.append(
                        f"slide {index} ({stype}): {key}[{i}] is {len(it)} chars "
                        f"(budget {item_limit}); may overflow."
                    )
    
    # Validate icon field if present
    icon_name = slide.get("icon")
    if icon_name and icon_name not in available_icons:
        warnings.append(
            f"slide {index} ({stype}): icon '{icon_name}' not found. "
            f"Valid icons: {', '.join(available_icons)}."
        )
    
    return warnings


def render_html(env: Environment, slide: dict, theme: dict, preset: dict,
                meta: dict, index: int, total: int, font_face_css: str) -> str:
    template = env.get_template(f"{slide['type']}.html")
    return template.render(
        slide=slide,
        theme=theme,
        colors=theme["colors"],
        fonts=theme["fonts"],
        decoration=theme.get("decoration", {}),
        canvas=preset,
        meta=meta,
        index=index,
        total=total,
        counter=f"{index}/{total}",
        footer=slide.get("footer", meta.get("footer", "")),
        font_face_css=Markup(font_face_css),  # Mark safe to prevent escaping
    )
