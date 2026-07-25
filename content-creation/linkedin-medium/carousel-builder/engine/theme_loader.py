#!/usr/bin/env python3
"""Load and validate carousel theme token files.

A theme is pure data (JSON): color tokens, a font stack, and decoration flags.
Themes can be referenced by built-in name (a file in themes/) or by an absolute
or cwd-relative path to a custom theme JSON.

Validation is intentionally light (themes are user-editable): required keys must
be present and colors must be parseable hex. Contrast is checked separately via
contrast_check.py and reported as a warning, never a hard failure.

Stdlib only.
"""
from __future__ import annotations

import json
import os

from . import contrast_check

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.normpath(os.path.join(HERE, "..", "themes"))

REQUIRED_COLOR_KEYS = [
    "background", "surface", "text_primary", "text_secondary",
    "accent_positive", "accent_negative", "accent_neutral",
]
REQUIRED_FONT_KEYS = ["heading", "body", "heading_weight", "body_weight"]


class ThemeError(ValueError):
    pass


def resolve_theme_path(theme: str) -> str:
    """Resolve a theme reference to a file path.

    A bare name (no path separator, no .json) maps to themes/<name>.json.
    Anything else is treated as a literal path (cwd-relative or absolute).
    """
    if os.sep in theme or theme.endswith(".json") or (os.altsep and os.altsep in theme):
        return os.path.abspath(theme)
    return os.path.join(THEMES_DIR, f"{theme}.json")


def load_theme(theme: str) -> dict:
    path = resolve_theme_path(theme)
    if not os.path.isfile(path):
        available = sorted(
            os.path.splitext(f)[0] for f in os.listdir(THEMES_DIR)
            if f.endswith(".json") and not f.startswith("_")
        )
        raise ThemeError(
            f"theme not found: {theme!r} (looked at {path}). "
            f"Built-in themes: {', '.join(available)}. "
            "For a custom theme, pass a path to your own theme JSON."
        )
    with open(path, "r", encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as e:
            raise ThemeError(f"theme {path} is not valid JSON: {e}") from e

    _validate(data, path)
    data["_path"] = path
    return data


def _validate(data: dict, path: str) -> None:
    colors = data.get("colors")
    if not isinstance(colors, dict):
        raise ThemeError(f"theme {path}: missing 'colors' object")
    missing = [k for k in REQUIRED_COLOR_KEYS if k not in colors]
    if missing:
        raise ThemeError(f"theme {path}: missing color token(s): {', '.join(missing)}")
    for key, val in colors.items():
        try:
            contrast_check._hex_to_rgb(val)
        except ValueError as e:
            raise ThemeError(f"theme {path}: color '{key}' is invalid: {e}") from e

    fonts = data.get("fonts")
    if not isinstance(fonts, dict):
        raise ThemeError(f"theme {path}: missing 'fonts' object")
    missing_f = [k for k in REQUIRED_FONT_KEYS if k not in fonts]
    if missing_f:
        raise ThemeError(f"theme {path}: missing font key(s): {', '.join(missing_f)}")


def contrast_report(data: dict) -> tuple[str, bool]:
    findings = contrast_check.check_theme(data["colors"])
    return contrast_check.format_report(data.get("name", "theme"), findings)
