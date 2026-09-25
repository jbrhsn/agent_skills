# Bash fallback

Use when shell creation is useful and the standard helper is unavailable or unsuitable. For the standard layout, prefer `uv run scripts/scaffold.py`, and note that plain `python3` works too if `uv` is missing (convert the plan to JSON if PyYAML isn't installed).

## Standard-layout compatibility

- Sections and modules get zero-padded numeric prefixes (`01-`); module numbering restarts inside each section. Chapters get plain slugs.
- Slugify: lowercase, non-alphanumeric → `-`, collapse repeats, trim.
- Every chapter gets the selected files, always including `learning.md`. Default: `learning.md`, `examples.md`, `practice.md`; add interview, recall, and writing files when relevant.
- Selected files carry the **same frontmatter key set** — see `templates.md`.
- `prev`/`next` follow plan order across module and section boundaries, not just within a module.
- Root gets `README.md`, a linked `PLAN.md` roadmap, and `progress.md`. Include goal and chapter completion checks and link only to selected files.
- Inspect existing files and preserve learner work. Make authorized targeted edits; ask only when replacement would exceed the request or discard work without authorization.

## Pattern

```bash
ROOT="python-senior-data-engineer"
CH="$ROOT/01-python-core/01-data-structures/builtin-collections"
mkdir -p "$CH"

write() {  # write <path> ; body on stdin ; refuses to clobber
  [ -e "$1" ] && { echo "skip (exists): $1"; cat >/dev/null; return; }
  cat > "$1"
}

write "$CH/learning.md" <<'EOF'
---
title: "Builtin Collections"
section: "Python Core"
module: "Data Structures"
chapter: "Builtin Collections"
position: "1 of 2"
profile: "technical"
tiers: ["Junior", "Senior"]
serves: "The coding screen's first fifteen minutes."
builds_on: []
enables: ["Complexity and Trade-offs"]
prev: ""
next: "Complexity and Trade-offs"
status: "todo"
tier_reached: "none"
tags: []
---

# Builtin Collections

> Python Core › Data Structures · chapter 1 of 2
>
> **Section arc:** Rebuild the fluency an interviewer assumes you never lost.
>
> **Module arc:** From what the builtins are to why CPython made them that way.
>
> **This chapter serves:** The coding screen's first fifteen minutes.

## Brief

<!-- Chapter assignment from the plan. Adapt when scope changes, keeping the machine-readable plan and PLAN.md consistent. Preserve existing learner work. -->

**Purpose:** Interviewers open with collections because the answers reveal whether you think about memory or only about syntax.

**Depth required:** Far enough to explain the CPython layout and benchmark a claim.

**Completion check:** Choose collections for an unfamiliar lookup task, implement it, and explain time and memory trade-offs.

**Topics to cover:**

1. **Dictionaries** — hashing, collision handling, insertion order
2. **Lists and arrays** — over-allocation, amortised append

## Junior — You use it correctly when someone tells you to.

**Scope here:** Pick the right collection for a stated requirement.

<!-- What each topic *is*, in your own words, plus the vocabulary you need to read anything else about it. A short plain-language explanation is a useful starting point. -->

## Sources

<!-- Links you actually read. -->
EOF
```

The following illustrates slot rendering only; it is not a complete generator. Create full files with metadata, briefs, and navigation before using this output. Do not append these examples to existing learner files. Slots and counts are in `templates.md`:

```bash
slots() {  # slots <item> <count> <slot>...
  item="$1"; count="$2"; shift 2
  for i in $(seq 1 "$count"); do
    printf '\n## %s %d\n\n' "$item" "$i"
    for s in "$@"; do printf '**%s:**\n\n' "$s"; done
  done
}

slots Example 2 Source "Why it works" "What to take from it" "My annotation"
slots Task 2 Task Tier "What done looks like" "What I actually did" "What broke"
```

Verify at the end that no chapter is short a selected file (adjust the list to the plan):

```bash
find "$ROOT" -mindepth 3 -maxdepth 3 -type d | while read -r d; do
  for f in learning examples practice; do
    [ -e "$d/$f.md" ] || echo "MISSING $f.md: $d"
  done
done
```
