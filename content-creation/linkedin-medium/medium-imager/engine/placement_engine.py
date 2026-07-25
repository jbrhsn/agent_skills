#!/usr/bin/env python3
"""Placement engine: generate placement proposals from draft AST.

Walks a structural AST (from draft_parser) and produces a human-readable,
confidence-tagged placement proposal: an ordered list of suggested images,
each with (position, type, content, confidence).

Confidence tags: 'high' (deterministic structural signal) or 'low' (heuristic/prose).
"""
from __future__ import annotations

import re


def detect_stat(text: str) -> tuple[str, bool]:
    """Detect if a paragraph contains a stat-worthy claim.
    
    Returns (stat_text, is_high_confidence).
    High confidence: starts with a percentage or large number, ends in period, short.
    Low confidence: percentage buried in prose.
    """
    # Pattern: percentage, "X of Y", large-magnitude number
    stat_patterns = [
        r"^(\d+%)",  # starts with %
        r"^([\d,]+[KMB]?)",  # large number (K=thousands, M=millions, B=billions)
        r"(\d+\s+out of\s+\d+)",  # "X out of Y"
        r"(\d+\s+to\s+\d+%)",  # "X to Y%"
    ]
    
    for pattern in stat_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            # High confidence if short, ends in period, and stat is at the start
            is_high = text.endswith(".") and len(text) < 200 and m.start() < 5
            return text, is_high
    
    return None, False


def generate_proposal(front_matter: dict, ast: dict) -> list[dict]:
    """Generate a placement proposal from a draft AST.
    
    Returns an ordered list of proposals:
        {
            position: int (for ordering),
            type: str (image type),
            content: dict (image spec fields),
            confidence: 'high' | 'low',
            reason: str,
        }
    """
    proposals = []
    position = 0
    
    # 1. Cover (always, high confidence)
    cover_title = front_matter.get("title") or ast.get("title")
    cover_subtitle = None
    if ast.get("paragraphs"):
        cover_subtitle = ast["paragraphs"][0]
    
    if cover_title:
        proposals.append({
            "position": position,
            "type": "cover",
            "content": {
                "title": cover_title,
                "subtitle": cover_subtitle,
            },
            "confidence": "high",
            "reason": f"Cover from front-matter/H1 title + first paragraph",
        })
        position += 1
    
    # 2. Section dividers before each H2/H3 (high confidence)
    for heading in ast.get("headings", []):
        if heading["level"] >= 2:
            proposals.append({
                "position": position,
                "type": "section_divider",
                "content": {"label": heading["text"]},
                "confidence": "high",
                "reason": f"H{heading['level']} section heading",
            })
            position += 1
    
    # 3. Quote blocks (high confidence, directly from blockquotes)
    for bq in ast.get("blockquotes", []):
        proposals.append({
            "position": position,
            "type": "quote_block",
            "content": {"quote": bq},
            "confidence": "high",
            "reason": "Markdown blockquote",
        })
        position += 1
    
    # 4. Comparison tables (high confidence, directly from tables)
    for table in ast.get("tables", []):
        rows = table.get("rows", [])
        if rows and len(rows) >= 2:
            # Assume first row is headers
            if len(rows[0]) >= 2:
                proposals.append({
                    "position": position,
                    "type": "comparison_table",
                    "content": {
                        "title_left": rows[0][0],
                        "title_right": rows[0][1],
                        "rows": rows[1:],
                    },
                    "confidence": "high",
                    "reason": "Markdown table",
                })
                position += 1
    
    # 5. Code cards (high confidence, directly from code blocks, but default to native)
    for cb in ast.get("code_blocks", []):
        proposals.append({
            "position": position,
            "type": "code_card",
            "content": {
                "code": cb["code"],
                "language": cb["language"],
            },
            "confidence": "high",
            "reason": "Fenced code block (kept as Medium native by default; request image explicitly)",
        })
        position += 1
    
    # 6. Stats (low confidence, heuristic)
    for para in ast.get("paragraphs", []):
        stat_text, is_high = detect_stat(para)
        if stat_text:
            confidence = "high" if is_high else "low"
            proposals.append({
                "position": position,
                "type": "stat_callout",
                "content": {
                    "value": re.match(r"[\d%K,. ]+", stat_text).group(0).strip(),
                    "label": para,  # full text as label
                },
                "confidence": confidence,
                "reason": f"Statistic detected in paragraph ({'high' if is_high else 'low'} confidence)",
            })
            position += 1
    
    # 7. Diagrams: only if explicitly marked or structured as numbered steps
    for cb in ast.get("code_blocks", []):
        lang = cb.get("language", "").lower()
        if lang in ("diagram", "mermaid", "flow"):
            proposals.append({
                "position": position,
                "type": "linear_flow",
                "content": {"steps": ["Step placeholder"]},
                "confidence": "low",
                "reason": f"Explicit {lang} code block (requires manual spec)",
            })
            position += 1
    
    return proposals
