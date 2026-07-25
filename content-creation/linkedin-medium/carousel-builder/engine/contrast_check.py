#!/usr/bin/env python3
"""WCAG AA contrast validation for theme color tokens.

Computes the WCAG 2.x contrast ratio between text and background colors and
checks them against AA thresholds:
  - normal/body text : >= 4.5:1
  - large text       : >= 3.0:1  (>= 24px, or >= 18.66px bold)

A theme that fails is reported loudly (not fatal) so the user can fix the
palette before shipping a deck that is hard to read on mobile.

Stdlib only.
"""
from __future__ import annotations

BODY_MIN = 4.5
LARGE_MIN = 3.0


def _hex_to_rgb(value: str) -> tuple[float, float, float]:
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError(f"invalid hex color: {value!r}")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _channel(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    r, g, b = _hex_to_rgb(hex_color)
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_theme(colors: dict) -> list[dict]:
    """Return a list of contrast findings for a theme's color tokens.

    Each finding: {pair, fg, bg, ratio, min, level, passes}. `level` is
    'body' (4.5:1) or 'large' (3.0:1). Missing tokens are skipped silently.
    """
    bg = colors.get("background")
    surface = colors.get("surface", bg)
    findings: list[dict] = []

    def add(pair: str, fg_key: str, on: str, level: str) -> None:
        fg = colors.get(fg_key)
        if not fg or not on:
            return
        ratio = round(contrast_ratio(fg, on), 2)
        minimum = BODY_MIN if level == "body" else LARGE_MIN
        findings.append({
            "pair": pair, "fg": fg, "bg": on, "ratio": ratio,
            "min": minimum, "level": level, "passes": ratio >= minimum,
        })

    if bg:
        add("text_primary on background", "text_primary", bg, "large")
        add("text_secondary on background", "text_secondary", bg, "body")
        add("accent_positive on background", "accent_positive", bg, "large")
        add("accent_negative on background", "accent_negative", bg, "large")
    if surface:
        add("text_primary on surface", "text_primary", surface, "large")
        add("text_secondary on surface", "text_secondary", surface, "body")
    return findings


def format_report(theme_name: str, findings: list[dict]) -> tuple[str, bool]:
    """Return (human-readable report, all_pass)."""
    lines = [f"Contrast check ({theme_name}):"]
    all_pass = True
    for f in findings:
        mark = "PASS" if f["passes"] else "FAIL"
        if not f["passes"]:
            all_pass = False
        lines.append(
            f"  [{mark}] {f['pair']}: {f['ratio']}:1 "
            f"(need {f['min']}:1 for {f['level']} text)"
        )
    if not findings:
        lines.append("  (no comparable color tokens found)")
    return "\n".join(lines), all_pass
