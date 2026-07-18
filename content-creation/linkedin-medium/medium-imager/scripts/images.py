#!/usr/bin/env python3
"""Shared schema loader/validator for medium-imager's images.json.

Not a CLI entry point on its own — imported by spec.py and render_svg.py so
both stay in sync on validation rules.

Schema (canonical path: medium/images/<slug>/images.json):

    {
      "slug": "my-article",
      "cover": {"title": "...", "subtitle": "...", "footer": "..."},
      "images": [
        {"type": "quote", "quote": "...", "attribution": "...", "footer": "..."},
        {"type": "callout", "text": "...", "label": "...", "footer": "..."},
        {"type": "stat", "number": "73%", "label": "...", "footer": "..."},
        {"type": "code", "code": "...", "language": "python", "footer": "..."}
      ]
    }

Field rules per type:
    cover:   title (required), subtitle (optional), footer (optional)
    quote:   quote (required), attribution (optional), footer (optional)
    callout: text (required), label (optional), footer (optional)
    stat:    number (required), label (required), footer (optional)
    code:    code (required), language (optional), footer (optional)

`index`/`total` for inner images are auto-filled from array position; do not
include them in the JSON.
"""
import json

VALID_TYPES = ("quote", "callout", "stat", "code")

REQUIRED_FIELDS = {
    "quote": ["quote"],
    "callout": ["text"],
    "stat": ["number", "label"],
    "code": ["code"],
}

MAX_IMAGES = 10


class SchemaError(ValueError):
    pass


def _require(obj, field, where):
    val = obj.get(field)
    if not isinstance(val, str) or not val.strip():
        raise SchemaError(f"{where}: missing or empty required field '{field}'")


def load_images(path):
    """Load and validate images.json. Returns (slug, cover, images)."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    slug = data.get("slug")
    if not isinstance(slug, str) or not slug.strip():
        raise SchemaError("top-level 'slug' is required and must be a non-empty string")

    cover = data.get("cover")
    if not isinstance(cover, dict):
        raise SchemaError("top-level 'cover' object is required")
    _require(cover, "title", "cover")

    images = data.get("images", [])
    if not isinstance(images, list):
        raise SchemaError("'images' must be a list (may be empty)")
    if len(images) > MAX_IMAGES:
        raise SchemaError(
            f"'images' has {len(images)} entries; max supported is {MAX_IMAGES} "
            "(split into more than one run if you need more)"
        )

    for i, img in enumerate(images, start=1):
        where = f"images[{i}]"
        if not isinstance(img, dict):
            raise SchemaError(f"{where}: must be an object")
        t = img.get("type")
        if t not in VALID_TYPES:
            raise SchemaError(
                f"{where}: 'type' must be one of {VALID_TYPES}, got {t!r}"
            )
        for field in REQUIRED_FIELDS[t]:
            _require(img, field, f"{where} (type={t})")

    return slug, cover, images
