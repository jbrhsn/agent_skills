#!/usr/bin/env python3
"""Draft parser: converts a Markdown draft to a structural AST + extracts front-matter.

Uses markdown-it-py to parse the draft into tokens, then walks the token stream
to extract headings, paragraphs, blockquotes, tables, code blocks, and lists.
Also parses optional YAML front-matter at the top for title/theme/cover.photo.

Requires markdown-it-py (installed via uv).
"""
from __future__ import annotations

import re
import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token


class DraftParseError(ValueError):
    pass


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Extract YAML front-matter (if present) and return (meta, remaining_text).
    
    Front-matter must be at the very start, between --- markers:
        ---
        title: My Article
        theme: editorial_serif
        ---
        # Rest of content...
    """
    if not text.startswith("---"):
        return {}, text

    end_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not end_match:
        return {}, text

    fm_text = end_match.group(1)
    remaining = text[end_match.end():]
    
    try:
        meta = yaml.safe_load(fm_text) or {}
        return meta, remaining
    except yaml.YAMLError:
        return {}, text


def parse_draft(text: str) -> tuple[dict, dict]:
    """Parse a Markdown draft and return (front_matter, structural_ast).
    
    Returns:
        (front_matter, ast) where:
        - front_matter: optional YAML metadata (title, theme, cover)
        - ast: {
            title: str,
            paragraphs: [str],
            blockquotes: [str],
            headings: [{level, text}],
            tables: [{rows: [[cells]]}],
            code_blocks: [{language, code}],
            lists: [{type: 'unordered'|'ordered', items: [str]}],
          }
    """
    front_matter, remaining = parse_front_matter(text)
    
    md = MarkdownIt()
    tokens = md.parse(remaining)
    
    ast = {
        "title": None,
        "paragraphs": [],
        "blockquotes": [],
        "headings": [],
        "tables": [],
        "code_blocks": [],
        "lists": [],
    }
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Heading
        if token.type == "heading_open":
            level = int(token.tag[1])
            # Next token is inline with the heading text
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                text = tokens[i + 1].content.strip()
                if level == 1 and not ast["title"]:
                    ast["title"] = text
                ast["headings"].append({"level": level, "text": text})
            i += 2
            continue
        
        # Blockquote
        if token.type == "blockquote_open":
            # Collect text from nested inline tokens until blockquote_close
            quote_parts = []
            i += 1
            while i < len(tokens) and tokens[i].type != "blockquote_close":
                if tokens[i].type == "inline":
                    quote_parts.append(tokens[i].content.strip())
                i += 1
            if quote_parts:
                ast["blockquotes"].append("\n".join(quote_parts))
            i += 1
            continue
        
        # Code block (fence)
        if token.type == "fence":
            lang = token.info.strip() if token.info else ""
            code = token.content
            ast["code_blocks"].append({"language": lang, "code": code})
            i += 1
            continue
        
        # Table
        if token.type == "table_open":
            table_rows = []
            i += 1
            while i < len(tokens) and tokens[i].type != "table_close":
                if tokens[i].type == "tr_open":
                    row_cells = []
                    i += 1
                    while i < len(tokens) and tokens[i].type != "tr_close":
                        if tokens[i].type in ("th_open", "td_open"):
                            # Next token should be inline
                            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                                row_cells.append(tokens[i + 1].content.strip())
                            i += 3  # skip open, inline, close
                            continue
                        i += 1
                    if row_cells:
                        table_rows.append(row_cells)
                i += 1
            if table_rows:
                ast["tables"].append({"rows": table_rows})
            continue
        
        # Bullet/ordered list
        if token.type in ("bullet_list_open", "ordered_list_open"):
            list_type = "unordered" if token.type == "bullet_list_open" else "ordered"
            list_items = []
            i += 1
            while i < len(tokens) and tokens[i].type != "bullet_list_close" and tokens[i].type != "ordered_list_close":
                if tokens[i].type == "list_item_open":
                    # Collect inline content
                    i += 1
                    while i < len(tokens) and tokens[i].type != "list_item_close":
                        if tokens[i].type == "inline":
                            list_items.append(tokens[i].content.strip())
                        i += 1
                i += 1
            if list_items:
                ast["lists"].append({"type": list_type, "items": list_items})
            continue
        
        # Paragraph (plain text)
        if token.type == "paragraph_open":
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                text = tokens[i + 1].content.strip()
                if text:
                    ast["paragraphs"].append(text)
            i += 3  # paragraph_open, inline, paragraph_close
            continue
        
        i += 1
    
    return front_matter, ast
