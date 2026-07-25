#!/usr/bin/env python3
"""Pygments-based code highlighting for medium-imager code cards.

Wraps Pygments to turn code + language into syntax-highlighted HTML that
matches the theme's Pygments style. Unknown/missing language → TextLexer (plain).

Requires pygments (installed via uv).
"""
from __future__ import annotations

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from markupsafe import Markup


def get_lexer(code: str, language: str | None):
    """Get a Pygments lexer for the given language, or guess/fallback."""
    if language:
        try:
            return get_lexer_by_name(language)
        except Exception:
            pass
    # Try to guess from content
    try:
        return guess_lexer(code)
    except Exception:
        pass
    # Fall back to plain text
    return TextLexer()


def highlight_code(code: str, language: str | None, pygments_style: str = "default") -> tuple[str, str]:
    """Highlight code and return (html_fragment, css_string).
    
    Args:
        code: the source code string
        language: optional language tag (e.g. 'python', 'bash', 'javascript')
        pygments_style: Pygments style name (e.g. 'monokai', 'github-dark', 'default')
    
    Returns:
        (html_fragment, css_string): the highlighted HTML and its CSS rules
    """
    lexer = get_lexer(code, language)
    formatter = HtmlFormatter(style=pygments_style, noclasses=True)
    html = highlight(code, lexer, formatter)
    # Extract CSS from formatter (if needed for styled output)
    css = formatter.get_style_defs(".highlight")
    return html, css
