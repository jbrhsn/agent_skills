# Bash fallback

Use only when Python is unavailable. Slower and easier to get wrong — prefer `scripts/scaffold.py`.

## Rules to preserve

- Sections and modules get zero-padded numeric prefixes (`01-`); module numbering restarts inside each section. Chapters get plain slugs.
- Slugify: lowercase, non-alphanumeric → `-`, collapse repeats, trim.
- Every chapter gets its topic files **plus** `interview.md` and `thought_leadership.md`.
- Root gets `README.md`, `PLAN.md`, `progress.md`.
- Never overwrite an existing file without asking.

## Pattern

```bash
ROOT="python-senior-data-engineer"
CH="$ROOT/01-python-core/01-data-structures/builtin-collections"
mkdir -p "$CH"

write() {  # write <path> ; body on stdin ; refuses to clobber
  [ -e "$1" ] && { echo "skip (exists): $1"; cat >/dev/null; return; }
  cat > "$1"
}

write "$CH/lists-and-arrays.md" <<'EOF'
---
title: Lists and arrays
section: Python Core
module: Data Structures
chapter: Builtin Collections
status: todo
confidence: 0
tags: []
---

# Lists and arrays

> **Why this matters:** <!-- Where does this show up in real systems, and what breaks without it? -->

## Mental model
<!-- Explain it in three sentences with no jargon. -->

## Core concepts
<!-- The ideas you must recall cold. -->

## Hands-on
<!-- Smallest runnable example, then break it deliberately. -->

## Gotchas and trade-offs
<!-- Cost, limits, failure modes, when NOT to use this. -->

## Recall check
<!-- Three questions you should answer without notes. -->

## Sources
EOF
```

Use `references/templates.md` verbatim for `interview.md`, `thought_leadership.md`, and the root files. Generate interview slots with a loop:

```bash
{ printf '## Q%d.\n**Type:** <!-- recall | applied | design | debugging -->\n**Answer:**\n**Follow-up they'"'"'d ask:**\n\n' $(seq 1 12); } >> "$CH/interview.md"
```

Verify at the end with `find "$ROOT" -type d -mindepth 3 -maxdepth 3 -exec sh -c 'ls "$1" | grep -q interview.md || echo "MISSING interview.md: $1"' _ {} \;`
