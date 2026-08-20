#!/usr/bin/env python3
"""Scaffold a goal-based learning repository from a plan file.

Usage:
    python3 scaffold.py plan.yaml [--out ./repo] [--dry-run] [--force]

Creates stub files only. Never writes learning content.
"""

import argparse
import json
import os
import re
import sys

DEFAULT_INTERVIEW_QUESTIONS = 12
DEFAULT_TL_IDEAS = 4


# ---------- plan loading ----------

def load_plan(path):
    if not os.path.isfile(path):
        die(f"Plan file not found: {path}")
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            die("PyYAML not installed. Either `pip install pyyaml` or convert the "
                "plan to JSON and rerun with plan.json.")
        return yaml.safe_load(raw)
    return json.loads(raw)


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate(plan):
    errs = []
    if not isinstance(plan, dict):
        die("Plan must be a mapping at the top level.")
    for key in ("repo_name", "goal", "sections"):
        if not plan.get(key):
            errs.append(f"missing required field: {key}")
    for si, sec in enumerate(plan.get("sections") or [], 1):
        loc = f"section {si}"
        if not sec.get("name"):
            errs.append(f"{loc}: missing name")
        mods = sec.get("modules") or []
        if not mods:
            errs.append(f"{loc}: needs at least one module")
        for mi, mod in enumerate(mods, 1):
            mloc = f"{loc}/module {mi}"
            if not mod.get("name"):
                errs.append(f"{mloc}: missing name")
            chaps = mod.get("chapters") or []
            if not chaps:
                errs.append(f"{mloc}: needs at least one chapter")
            for ci, ch in enumerate(chaps, 1):
                cloc = f"{mloc}/chapter {ci}"
                if not ch.get("name"):
                    errs.append(f"{cloc}: missing name")
                if not (ch.get("topics") or []):
                    errs.append(f"{cloc}: needs at least one topic")
    if errs:
        die("invalid plan:\n  - " + "\n  - ".join(errs))


# ---------- naming ----------

def slug(text):
    s = str(text).lower().strip()
    s = re.sub(r"[&/]+", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "untitled"


def uniquify(name, used):
    if name not in used:
        used.add(name)
        return name
    n = 2
    while f"{name}-{n}" in used:
        n += 1
    used.add(f"{name}-{n}")
    return f"{name}-{n}"


# ---------- templates ----------

def fm(pairs):
    lines = ["---"]
    for k, v in pairs:
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def topic_stub(topic, section, module, chapter):
    return f"""{fm([
        ("title", topic),
        ("section", section),
        ("module", module),
        ("chapter", chapter),
        ("status", "todo"),
        ("confidence", 0),
        ("tags", "[]"),
    ])}

# {topic}

> **Why this matters:** <!-- Where does this show up in real systems, and what breaks without it? One or two sentences, written after you understand it. -->

## Mental model
<!-- Explain it in three sentences with no jargon. If you can't, you don't have it yet. -->

## Core concepts
<!-- The ideas you must recall cold. Bullets, not prose. -->

## Hands-on
<!-- Smallest runnable example. Then break it deliberately and record what happened. -->

## Gotchas and trade-offs
<!-- Cost, limits, failure modes, and when NOT to use this. -->

## Recall check
<!-- Three questions you should answer without notes. Write them now, answer them later. -->

## Sources
<!-- Links you actually read. -->
"""


def interview_stub(count, section, module, chapter):
    head = f"""{fm([
        ("title", f"Interview Questions — {chapter}"),
        ("section", section),
        ("module", module),
        ("chapter", chapter),
        ("status", "todo"),
    ])}

# Interview Questions — {chapter}

<!-- Fill each slot with a question you'd actually be asked at your target level.
     Mix recall, applied, and design/judgement questions. Answer in your own words. -->
"""
    slots = "".join(
        f"""
## Q{i}.
**Type:** <!-- recall | applied | design | debugging -->
**Answer:**
**Follow-up they'd ask:**
"""
        for i in range(1, count + 1)
    )
    return head + slots


def tl_stub(count, section, module, chapter):
    head = f"""{fm([
        ("title", f"Thought Leadership — {chapter}"),
        ("section", section),
        ("module", module),
        ("chapter", chapter),
        ("status", "todo"),
    ])}

# Thought Leadership — {chapter}

<!-- Ideas for public writing that demonstrate real understanding.
     Ship only what you've actually done or verified. -->
"""
    slots = "".join(
        f"""
## Idea {i}
**Angle:** <!-- The non-obvious claim. If it's a summary of the docs, discard it. -->
**Hook:**
**Audience:**
**Platform:** <!-- LinkedIn post | Medium article | conference talk | internal writeup -->
**Evidence I have:** <!-- Benchmark, incident, code, or migration you can point to. -->
**Status:** idea
"""
        for i in range(1, count + 1)
    )
    return head + slots


def readme(plan, tree_lines):
    def block(title, items):
        if not items:
            return ""
        return f"\n## {title}\n" + "".join(f"- {i}\n" for i in items)

    meta = ""
    for label, key in (("Target", "target"), ("Level", "level"), ("Horizon", "horizon")):
        if plan.get(key):
            meta += f"- **{label}:** {plan[key]}\n"

    return f"""# {plan['repo_name']}

{str(plan['goal']).strip()}

{meta}
## How this repo is organised

```
section/            numbered, broad area
  module/           numbered within its section
    chapter/        a coherent unit of study
      topic.md            one file per topic
      interview.md        questions to answer from memory
      thought_leadership.md   public-writing angles
```

Every file is a **stub**. Nothing here is filled in for you — writing it is the work.

## Using the status fields

Each file's frontmatter carries `status` (`todo` → `learning` → `drafted` → `mastered`) and topic files add `confidence` (0–5, self-rated after a recall check). Update them as you go and mirror the chapter status in `progress.md`.

## Files

- `PLAN.md` — the source of truth for scope, exclusions, and structure.
- `progress.md` — tracker.
{block("Out of scope", plan.get("excluded"))}
## Structure

```
{tree_lines}
```
"""


def plan_md(plan, tree_lines):
    def block(title, items):
        if not items:
            return ""
        return f"\n## {title}\n" + "".join(f"- {i}\n" for i in items) + "\n"

    meta = ""
    for label, key in (("Target", "target"), ("Level", "level"), ("Horizon", "horizon")):
        if plan.get(key):
            meta += f"- **{label}:** {plan[key]}\n"

    return f"""# Plan

## Goal

{str(plan['goal']).strip()}

{meta}{block("Out of scope", plan.get("excluded"))}{block("Assumptions", plan.get("assumptions"))}{block("Research notes", plan.get("research_notes"))}## Structure

```
{tree_lines}
```

<!-- Amend this file when scope changes, then re-run the scaffolder. It is the
     source of truth; the folder tree is downstream of it. -->
"""


def progress_md(chapters):
    rows = "\n".join(
        f"| {c['section']} | {c['module']} | {c['chapter']} | {len(c['topics'])} | todo |"
        for c in chapters
    )
    checklist = ""
    for c in chapters:
        checklist += f"\n### {c['section']} › {c['module']} › {c['chapter']}\n"
        for t in c["topics"]:
            checklist += f"- [ ] {t}\n"
        checklist += "- [ ] interview.md\n- [ ] thought_leadership.md\n"

    return f"""# Progress

Status values: `todo` → `learning` → `drafted` → `mastered`.

| Section | Module | Chapter | Topics | Status |
|---|---|---|---|---|
{rows}

## Topic checklist
{checklist}"""


# ---------- writing ----------

class Writer:
    def __init__(self, dry_run, force):
        self.dry_run = dry_run
        self.force = force
        self.files = 0
        self.dirs = 0
        self.skipped = []

    def mkdir(self, path):
        self.dirs += 1
        if not self.dry_run:
            os.makedirs(path, exist_ok=True)

    def write(self, path, content):
        if os.path.exists(path) and not self.force:
            self.skipped.append(path)
            return
        self.files += 1
        if not self.dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


def build(plan, out, writer):
    tree = [f"{os.path.basename(out.rstrip('/'))}/"]
    chapters = []
    sec_used = set()

    writer.mkdir(out)

    for si, sec in enumerate(plan["sections"], 1):
        sec_name = sec["name"]
        sec_dir = uniquify(f"{si:02d}-{slug(sec_name)}", sec_used)
        sec_path = os.path.join(out, sec_dir)
        writer.mkdir(sec_path)
        tree.append(f"├── {sec_dir}/")

        mod_used = set()
        for mi, mod in enumerate(sec["modules"], 1):
            mod_name = mod["name"]
            mod_dir = uniquify(f"{mi:02d}-{slug(mod_name)}", mod_used)
            mod_path = os.path.join(sec_path, mod_dir)
            writer.mkdir(mod_path)
            tree.append(f"│   ├── {mod_dir}/")

            ch_used = set()
            for ch in mod["chapters"]:
                ch_name = ch["name"]
                ch_dir = uniquify(slug(ch_name), ch_used)
                ch_path = os.path.join(mod_path, ch_dir)
                writer.mkdir(ch_path)
                tree.append(f"│   │   ├── {ch_dir}/")

                topics = [str(t) for t in ch["topics"]]
                t_used = set()
                for topic in topics:
                    fname = uniquify(slug(topic), t_used) + ".md"
                    writer.write(
                        os.path.join(ch_path, fname),
                        topic_stub(topic, sec_name, mod_name, ch_name),
                    )
                    tree.append(f"│   │   │   ├── {fname}")

                q = clamp(ch.get("interview_questions", DEFAULT_INTERVIEW_QUESTIONS), 10, 15)
                writer.write(
                    os.path.join(ch_path, "interview.md"),
                    interview_stub(q, sec_name, mod_name, ch_name),
                )
                ideas = clamp(ch.get("thought_leadership_ideas", DEFAULT_TL_IDEAS), 1, 10)
                writer.write(
                    os.path.join(ch_path, "thought_leadership.md"),
                    tl_stub(ideas, sec_name, mod_name, ch_name),
                )
                tree.append("│   │   │   ├── interview.md")
                tree.append("│   │   │   └── thought_leadership.md")

                chapters.append({
                    "section": sec_name, "module": mod_name,
                    "chapter": ch_name, "topics": topics,
                })

    tree_str = "\n".join(tree)
    writer.write(os.path.join(out, "README.md"), readme(plan, tree_str))
    writer.write(os.path.join(out, "PLAN.md"), plan_md(plan, tree_str))
    writer.write(os.path.join(out, "progress.md"), progress_md(chapters))
    return tree_str, chapters


def clamp(v, lo, hi):
    try:
        v = int(v)
    except (TypeError, ValueError):
        return lo
    return max(lo, min(hi, v))


def main():
    ap = argparse.ArgumentParser(description="Scaffold a learning repo from a plan file.")
    ap.add_argument("plan", help="path to plan.yaml or plan.json")
    ap.add_argument("--out", help="output directory (default: ./<repo_name>)")
    ap.add_argument("--dry-run", action="store_true", help="print the tree, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    plan = load_plan(args.plan)
    validate(plan)
    out = args.out or os.path.join(".", slug(plan["repo_name"]))

    writer = Writer(args.dry_run, args.force)
    tree, chapters = build(plan, out, writer)

    print(tree)
    print()
    n_sec = len(plan["sections"])
    n_mod = sum(len(s["modules"]) for s in plan["sections"])
    n_top = sum(len(c["topics"]) for c in chapters)
    mode = "would create" if args.dry_run else "created"
    print(f"{mode}: {n_sec} sections, {n_mod} modules, {len(chapters)} chapters, "
          f"{n_top} topics, {writer.files} files in {out}")
    if writer.skipped:
        print(f"skipped {len(writer.skipped)} existing file(s); use --force to overwrite:")
        for p in writer.skipped[:10]:
            print(f"  {p}")


if __name__ == "__main__":
    main()
