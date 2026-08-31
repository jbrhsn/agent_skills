# Bash fallback

Use only when Python is unavailable. Slower and much easier to get wrong — prefer `uv run scripts/scaffold.py`, and note that plain `python3` works too if `uv` is missing (convert the plan to JSON if PyYAML isn't installed).

## Rules to preserve

- Sections and modules get zero-padded numeric prefixes (`01-`); module numbering restarts inside each section. Chapters get plain slugs.
- Slugify: lowercase, non-alphanumeric → `-`, collapse repeats, trim.
- Every chapter gets **all six files**: `learning.md`, `examples.md`, `practice.md`, `interview.md`, `thought_leadership.md`, `quizzies.md`.
- All six carry the **same frontmatter key set** — see `references/templates.md`. Getting this wrong is the most likely failure of a hand-run; the keys are what make the repo navigable.
- `prev`/`next` follow plan order across module and section boundaries, not just within a module.
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

write "$CH/learning.md" <<'EOF'
---
title: "Builtin Collections"
section: "Python Core"
module: "Data Structures"
chapter: "Builtin Collections"
position: "1 of 2"
profile: "technical"
tiers: ["Junior", "Senior", "Architect", "Expert"]
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
> **Section arc:** Rebuild the fluency an interviewer assumes you never lost.
> **Module arc:** From what the builtins are to why CPython made them that way.
> **This chapter serves:** The coding screen's first fifteen minutes.

## Brief

<!-- Written by the planner from the approved plan. Read it before you write anything
     below. Do not edit it while learning - amend PLAN.md and re-scaffold instead. -->

**Purpose:** Interviewers open with collections because the answers reveal whether you think about memory or only about syntax.

**Depth required:** Far enough to explain the CPython layout and benchmark a claim.

**Topics to cover:**

1. **Dictionaries** — hashing, collision handling, insertion order
2. **Lists and arrays** — over-allocation, amortised append

## Junior — You use it correctly when someone tells you to.

**Scope here:** Pick the right collection for a stated requirement.

<!-- What each topic *is*, in your own words, plus the vocabulary you need to read anything
     else about it. Write a three-sentence explanation with no jargon - if you can't, you
     don't have it yet. -->

## Sources

<!-- Links you actually read. -->
EOF
```

The five slot files share one shape, so generate them in a loop rather than by hand. Slots and counts per file are in `references/templates.md`:

```bash
slots() {  # slots <item> <count> <slot>...
  item="$1"; count="$2"; shift 2
  for i in $(seq 1 "$count"); do
    printf '\n## %s %d\n\n' "$item" "$i"
    for s in "$@"; do printf '**%s:**\n' "$s"; done
  done
}

slots Q 12 Type Answer "Follow-up they'd ask" >> "$CH/interview.md"
slots Task 4 Task Tier "What done looks like" "What I actually did" "What broke" >> "$CH/practice.md"
```

Verify at the end that no chapter is short a file:

```bash
find "$ROOT" -mindepth 3 -maxdepth 3 -type d | while read -r d; do
  for f in learning examples practice interview thought_leadership quizzies; do
    [ -e "$d/$f.md" ] || echo "MISSING $f.md: $d"
  done
done
```
