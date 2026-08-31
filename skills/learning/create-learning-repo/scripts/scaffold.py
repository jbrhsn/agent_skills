#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Scaffold a goal-based learning repository from a plan file.

Usage:
    uv run scaffold.py plan.yaml [--out ./repo] [--dry-run] [--force]
    python3 scaffold.py plan.json ...      # works too; YAML needs PyYAML installed

Every chapter gets the same six files. The profile decides the tier ladder and the
labels inside those files — never their names. Creates stubs only: the brief tells
the learner what to write and how deep, and never writes it for them.
"""

import argparse
import json
import os
import re
import sys

MAX_TIERS = 4

# ---------- profiles ----------
# A profile is data: a tier ladder, plus label overrides for the five slot files.
# The four rungs always occupy the same positions - foundation, working, systemic,
# frontier - which is why one set of tier prompts serves every profile.

PROFILES = {
    "technical": {
        "tiers": [
            ("Junior", "You use it correctly when someone tells you to."),
            ("Senior", "You choose it under real constraints and know what it costs."),
            ("Architect", "You place it in a whole system and defend the trade-off."),
            ("Expert", "You know where the consensus is wrong, and can show why."),
        ],
    },
    "craft": {
        "tiers": [
            ("Beginner", "You follow the form and produce something competent."),
            ("Practitioner", "You make deliberate choices and can justify each one."),
            ("Voice", "The work is recognisably yours and still serves the reader."),
            ("Authority", "You shift how other practitioners think about the form."),
        ],
        "files": {
            "examples": {"item": "Specimen",
                         "framing": "Work by people better than you. Study it before you imitate it."},
            "practice": {"item": "Exercise"},
            "interview": {"title": "Hard Questions",
                          "framing": "What a sharp editor or peer would push back on."},
        },
    },
    "practice": {
        "tiers": [
            ("Aware", "You can name the mechanism and spot it in your own week."),
            ("Consistent", "You run it reliably without needing motivation."),
            ("Adaptive", "You adjust it when your context breaks the default."),
            ("Designer", "You build systems others can run, and know their failure modes."),
        ],
        "files": {
            "examples": {"item": "Case",
                         "framing": "Real systems - yours or other people's - seen close up."},
            "practice": {"item": "Experiment", "count": 3,
                         "slots": ["Hypothesis", "Setup", "Run for", "What actually happened",
                                   "Keep, adjust, or drop"],
                         "framing": "You cannot read your way to a habit. Run it and record what happened."},
            "interview": {"title": "Hard Questions", "count": 8,
                          "framing": "What someone would challenge your system with - "
                                     "including you, three months in, when it stops working."},
        },
    },
    "exam": {
        "tiers": [
            ("Recall", "You state it cold, under time pressure."),
            ("Applied", "You use it on a clean, well-posed question."),
            ("Scenario", "You find it inside a messy, multi-step problem."),
            ("Edge", "You handle the distractors and boundary cases examiners actually use."),
        ],
        "files": {
            "practice": {"item": "Drill", "count": 5,
                         "slots": ["Question type", "My attempt", "Where I lost time", "Fix"],
                         "framing": "Timed drills in the exam's own question format."},
            "interview": {"title": "Examiner Questions", "count": 15,
                          "framing": "Questions in the exam's phrasing, including the ones "
                                     "designed to catch you out."},
            "quizzies": {"count": 15},
            "thought_leadership": {"count": 2,
                                   "framing": "Optional for an exam goal - fill it only if you "
                                              "intend to write publicly. Teaching a topic is still "
                                              "the fastest way to find the holes in it."},
        },
    },
}

# ---------- the six files ----------
# learning.md is bespoke. The other five are the same renderer with different labels.

FILES = [
    {"stem": "learning", "title": "{chapter}"},
    {
        "stem": "examples", "title": "Examples", "item": "Example", "count": 3,
        "slots": ["Source", "Why it works", "What to take from it", "My annotation"],
        "framing": "Worked specimens you study and pull apart. Not your own work - that is practice.md.",
    },
    {
        "stem": "practice", "title": "Practice", "item": "Task", "count": 4,
        "slots": ["Task", "Tier", "What done looks like", "What I actually did", "What broke"],
        "hints": {"Tier": "{tiers}"},
        "framing": "Tasks you do, not read. Each one should be small enough to finish in a sitting.",
    },
    {
        "stem": "interview", "title": "Interview Questions", "item": "Q", "count": 12,
        "slots": ["Type", "Answer", "Follow-up they'd ask"],
        "hints": {"Type": "recall | applied | design | debugging"},
        "framing": "Questions someone else puts to you, at your target level. "
                   "Mix recall, applied, and judgement.",
    },
    {
        "stem": "thought_leadership", "title": "Thought Leadership", "item": "Idea", "count": 4,
        "slots": ["Angle", "Hook", "Audience", "Platform", "Evidence I have"],
        "hints": {"Angle": "The non-obvious claim. If it summarises the docs, discard it.",
                  "Platform": "LinkedIn post | Medium article | talk | internal writeup",
                  "Evidence I have": "A benchmark, incident, migration, or artefact you can point to."},
        "framing": "Public-writing angles. Ship only what you have actually done or verified.",
    },
    {
        "stem": "quizzies", "title": "Quizzies", "item": "Q", "count": 10,
        "slots": ["Question", "My answer, from memory", "Verified?", "Revisit on"],
        "hints": {"Verified?": "yes | no - check against a source, not against your own notes"},
        "framing": "Self-assessment. Write the questions early, answer them later with the "
                   "notes closed. A question you can already answer is not worth a slot.",
    },
]

# Tier prompts by ladder position, deliberately domain-neutral.
TIER_PROMPTS = [
    "What each topic *is*, in your own words, plus the vocabulary you need to read anything "
    "else about it. Write a three-sentence explanation with no jargon - if you can't, you "
    "don't have it yet.",
    "How you actually use it under real constraints. What it costs, where it breaks, and the "
    "mistakes you personally made getting here.",
    "How it fits into a whole system. What you would choose instead, and the trade-off you "
    "would defend out loud to someone who disagrees.",
    "Where the received wisdom is incomplete, contested, or wrong - and the evidence you have "
    "for saying so. Nothing here should be findable in the docs.",
]


# ---------- plan loading ----------

def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def load_plan(path):
    if not os.path.isfile(path):
        die(f"Plan file not found: {path}")
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            die("PyYAML not installed. Run this script with `uv run scaffold.py` (which "
                "installs it), or convert the plan to plan.json and rerun.")
        return yaml.safe_load(raw)
    return json.loads(raw)


def resolve_profile(plan):
    name = str(plan.get("profile") or "technical").strip().lower()
    if name == "custom":
        tiers = parse_tiers(plan.get("tiers"))
        if not tiers:
            die("profile: custom requires a top-level `tiers:` list of [name, definition] pairs.")
        return name, {"tiers": tiers, "files": {}}
    if name not in PROFILES:
        die(f"unknown profile: {name}. Known: {', '.join(sorted(PROFILES))}, custom.")
    return name, PROFILES[name]


def parse_tiers(raw):
    tiers = []
    for t in raw or []:
        if isinstance(t, (list, tuple)) and len(t) >= 2:
            tiers.append((str(t[0]), str(t[1])))
        elif isinstance(t, dict) and t.get("name"):
            tiers.append((str(t["name"]), str(t.get("definition") or "")))
        elif isinstance(t, str):
            tiers.append((t, ""))
    return tiers


def text(v):
    """Collapse a plan scalar to one clean line - YAML `>` blocks arrive with newlines."""
    return " ".join(str(v).split()) if v else ""


def parse_topics(raw):
    out = []
    for t in raw or []:
        if isinstance(t, dict):
            out.append({"name": text(t.get("name")) or "Untitled",
                        "covers": [text(c) for c in (t.get("covers") or [])],
                        "depth": text(t.get("depth"))})
        else:
            out.append({"name": text(t), "covers": [], "depth": ""})
    return out


def validate(plan):
    errs, warns = [], []
    if not isinstance(plan, dict):
        die("Plan must be a mapping at the top level.")
    for key in ("repo_name", "goal", "sections"):
        if not plan.get(key):
            errs.append(f"missing required field: {key}")
    for si, sec in enumerate(plan.get("sections") or [], 1):
        loc = f"section {si}"
        if not sec.get("name"):
            errs.append(f"{loc}: missing name")
        if not sec.get("arc"):
            warns.append(f"{loc} ({sec.get('name', '?')}): no `arc` - chapters will not say "
                         f"where they sit in the section's story")
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
                nm = ch.get("name")
                if not nm:
                    errs.append(f"{cloc}: missing name")
                if not (ch.get("topics") or []):
                    errs.append(f"{cloc}: needs at least one topic")
                if not ch.get("purpose"):
                    errs.append(f"{cloc} ({nm or '?'}): missing `purpose` - a chapter with no "
                                f"stated purpose produces a stub nobody knows how to fill")
                for field in ("depth", "style", "serves"):
                    if not ch.get(field):
                        warns.append(f"{cloc} ({nm or '?'}): no `{field}`")
    if errs:
        die("invalid plan:\n  - " + "\n  - ".join(errs))
    return warns


# ---------- naming ----------

def slug(value):
    s = str(value).lower().strip()
    s = re.sub(r"[&/]+", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-") or "untitled"


def uniquify(name, used):
    if name not in used:
        used.add(name)
        return name
    n = 2
    while f"{name}-{n}" in used:
        n += 1
    used.add(f"{name}-{n}")
    return f"{name}-{n}"


# ---------- rendering ----------

def yq(v):
    if v is None:
        return '""'
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(yq(str(i)) for i in v) + "]"
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def frontmatter(ctx, stem):
    """The same key set in all six files, so tooling never special-cases one."""
    pairs = [
        ("title", ctx["titles"][stem]),
        ("section", ctx["section"]),
        ("module", ctx["module"]),
        ("chapter", ctx["chapter"]),
        ("position", f"{ctx['pos']} of {ctx['pos_total']}"),
        ("profile", ctx["profile_name"]),
        ("tiers", [t[0] for t in ctx["tiers"]]),
        ("serves", ctx["serves"]),
        ("builds_on", ctx["builds_on"]),
        ("enables", ctx["enables"]),
        ("prev", ctx["prev"]),
        ("next", ctx["next"]),
        ("status", "todo"),
        ("tier_reached", "none"),
        ("tags", []),
    ]
    return "---\n" + "\n".join(f"{k}: {yq(v)}" for k, v in pairs) + "\n---"


def breadcrumb(ctx):
    lines = [f"> {ctx['section']} › {ctx['module']} · chapter {ctx['pos']} of {ctx['pos_total']}"]
    if ctx["section_arc"]:
        lines.append(f"> **Section arc:** {ctx['section_arc']}")
    if ctx["module_arc"]:
        lines.append(f"> **Module arc:** {ctx['module_arc']}")
    if ctx["serves"]:
        lines.append(f"> **This chapter serves:** {ctx['serves']}")
    return "\n".join(lines)


def nav(ctx, stem):
    sibs = " · ".join(
        f"[{s.replace('_', ' ')}]({s}.md)" for s in (f["stem"] for f in ctx["files"]) if s != stem
    )
    out = f"**This chapter:** {sibs}"
    if ctx["prev_rel"]:
        out += f"\n**Previous:** [{ctx['prev']}]({ctx['prev_rel']})"
    if ctx["next_rel"]:
        out += f"\n**Next:** [{ctx['next']}]({ctx['next_rel']})"
    return out


def brief_block(ctx):
    """The full brief - learning.md only. Says what to write and how deep; never writes it."""
    paras = [
        "## Brief",
        "<!-- Written by the planner from the approved plan. Read it before you write anything\n"
        "     below. Do not edit it while learning - amend PLAN.md and re-scaffold instead. -->",
        f"**Purpose:** {ctx['purpose']}",
    ]
    for label, value in (("Depth required", ctx["depth"]), ("Style", ctx["style"]),
                         ("Assumes you already have", ", ".join(ctx["builds_on"])),
                         ("Unblocks later", ", ".join(ctx["enables"]))):
        if value:
            paras.append(f"**{label}:** {value}")

    topics = ["**Topics to cover:**", ""]
    for i, t in enumerate(ctx["topics"], 1):
        line = f"{i}. **{t['name']}**"
        if t["covers"]:
            line += " — " + ", ".join(t["covers"])
        topics.append(line)
        if t["depth"]:
            topics.append(f"   *Depth:* {t['depth']}")
    paras.append("\n".join(topics))
    return "\n\n".join(paras)


def brief_lite(ctx, spec):
    """Two lines, derived - so every file knows its own job without extra authoring."""
    names = ", ".join(t["name"] for t in ctx["topics"])
    out = f"**This file's job:** {spec['framing']}\n\n**Topics in scope:** {names}"
    if ctx["depth"]:
        out += f"\n\n**Depth target:** {ctx['depth']}"
    return out


def learning_stub(ctx):
    tier_sections = []
    for i, (name, definition) in enumerate(ctx["tiers"]):
        scope = ctx["tier_scope"].get(name.lower(), "")
        head = f"## {name}" + (f" — {definition}" if definition else "")
        body = f"**Scope here:** {scope}" if scope else \
            "**Scope here:** <!-- What this tier means for this chapter specifically. -->"
        tier_sections.append(f"{head}\n\n{body}\n\n<!-- {TIER_PROMPTS[i]} -->")

    return f"""{frontmatter(ctx, 'learning')}

# {ctx['chapter']}

{breadcrumb(ctx)}

{brief_block(ctx)}

{(chr(10) * 2).join(tier_sections)}

## Sources

<!-- Links you actually read. -->

---

{nav(ctx, 'learning')}
"""


def slot_stub(ctx, spec):
    stem = spec["stem"]
    hints = spec.get("hints") or {}
    tier_names = " | ".join(t[0].lower() for t in ctx["tiers"])
    count = ctx["counts"].get(stem, spec["count"])

    blocks = []
    for i in range(1, count + 1):
        lines = [f"## {spec['item']} {i}", ""]
        for s in spec["slots"]:
            hint = hints.get(s, "").replace("{tiers}", tier_names)
            lines.append(f"**{s}:**" + (f" <!-- {hint} -->" if hint else ""))
        blocks.append("\n".join(lines))

    return f"""{frontmatter(ctx, stem)}

# {ctx['titles'][stem]}

{breadcrumb(ctx)}

{brief_lite(ctx, spec)}

{chr(10).join(chr(10) + b for b in blocks).lstrip()}

---

{nav(ctx, stem)}
"""


# ---------- root files ----------

def bullets(title, items):
    if not items:
        return ""
    return f"\n## {title}\n" + "".join(f"- {i}\n" for i in items)


def meta_lines(plan):
    out = ""
    for label, key in (("Target", "target"), ("Level", "level"), ("Horizon", "horizon")):
        if plan.get(key):
            out += f"- **{label}:** {plan[key]}\n"
    return out


def readme(plan, profile_name, tiers, files, tree):
    ladder = " → ".join(f"**{n}**" for n, _ in tiers)
    defs = "\n".join(f"- **{n}** — {d}" for n, d in tiers if d)
    file_list = "\n".join(f"  {f['stem'] + '.md':<24}{f.get('framing', 'Tiered explanation of every topic in the chapter.')}"
                          for f in files)
    return f"""# {plan['repo_name']}

{str(plan['goal']).strip()}

{meta_lines(plan)}
## How this repo is organised

```
section/            numbered, broad area
  module/           numbered within its section
    chapter/        a coherent unit of study - always the same six files
{file_list}
```

Every file is a **stub**. Each one opens with a brief saying what belongs in it and how deep to go; writing the rest is the work.

## The ladder — `{profile_name}` profile

{ladder}

{defs}

`learning.md` has one section per rung. You are not finished with a chapter when you have written something under every heading — you are finished when the rung named in `tier_reached` is one you could defend out loud.

## Tracking

Every file carries the same frontmatter: `status` (`todo` → `learning` → `drafted` → `mastered`) and `tier_reached` (`none` → the top rung you can defend). `builds_on`, `enables`, `prev`, and `next` say how the chapter connects to the rest — follow them rather than reading the tree top to bottom.

## Files

- `PLAN.md` — the source of truth for scope, exclusions, and structure. Amend it and re-scaffold; don't hand-edit the tree.
- `progress.md` — tracker.
{bullets("Out of scope", plan.get("excluded"))}
## Structure

```
{tree}
```
"""


def plan_md(plan, profile_name, tiers, tree):
    return f"""# Plan

## Goal

{str(plan['goal']).strip()}

{meta_lines(plan)}
- **Profile:** {profile_name}
- **Ladder:** {" → ".join(n for n, _ in tiers)}
{bullets("Out of scope", plan.get("excluded"))}{bullets("Assumptions", plan.get("assumptions"))}{bullets("Research notes", plan.get("research_notes"))}
## Structure

```
{tree}
```

<!-- Amend this file when scope changes, then re-run the scaffolder. It is the
     source of truth; the folder tree is downstream of it. -->
"""


def progress_md(chapters, files):
    rows = "\n".join(
        f"| {c['section']} | {c['module']} | {c['chapter']} | {len(c['topics'])} | none | todo |"
        for c in chapters
    )
    checklist = ""
    for c in chapters:
        checklist += f"\n### {c['section']} › {c['module']} › {c['chapter']}\n"
        for f in files:
            checklist += f"- [ ] {f['stem']}.md\n"
        checklist += "  <details><summary>topics in learning.md</summary>\n\n"
        for t in c["topics"]:
            checklist += f"  - [ ] {t['name']}\n"
        checklist += "  </details>\n"

    return f"""# Progress

Status: `todo` → `learning` → `drafted` → `mastered`. Tier reached: the top rung you could defend out loud, not the last heading you typed under.

| Section | Module | Chapter | Topics | Tier reached | Status |
|---|---|---|---|---|---|
{rows}

## Chapter checklist
{checklist}"""


# ---------- writing ----------

class Writer:
    def __init__(self, dry_run, force):
        self.dry_run, self.force = dry_run, force
        self.files = self.dirs = 0
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


def chapter_files(profile):
    """Merge the profile's label overrides onto the six base specs."""
    overrides = profile.get("files") or {}
    return [dict(base, **overrides.get(base["stem"], {})) for base in FILES]


def clamp(v, lo, hi, default=None):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return default if default is not None else lo


def collect(plan, out, files):
    """Pass one: lay out every chapter and its path, so prev/next can be resolved."""
    chapters, tree = [], [f"{os.path.basename(out.rstrip('/')) or 'repo'}/"]
    sec_used = set()

    for si, sec in enumerate(plan["sections"], 1):
        sec_dir = uniquify(f"{si:02d}-{slug(sec['name'])}", sec_used)
        tree.append(f"├── {sec_dir}/")
        mod_used = set()
        for mi, mod in enumerate(sec.get("modules") or [], 1):
            mod_dir = uniquify(f"{mi:02d}-{slug(mod['name'])}", mod_used)
            tree.append(f"│   ├── {mod_dir}/")
            ch_used = set()
            chaps = mod.get("chapters") or []
            for ci, ch in enumerate(chaps, 1):
                ch_dir = uniquify(slug(ch["name"]), ch_used)
                tree.append(f"│   │   ├── {ch_dir}/")
                for f in files:
                    tree.append(f"│   │   │   ├── {f['stem']}.md")
                chapters.append({
                    "section": sec["name"], "module": mod["name"], "chapter": ch["name"],
                    "section_arc": text(sec.get("arc")), "module_arc": text(mod.get("arc")),
                    "path": os.path.join(out, sec_dir, mod_dir, ch_dir),
                    "pos": ci, "pos_total": len(chaps),
                    "purpose": text(ch.get("purpose")), "depth": text(ch.get("depth")),
                    "style": text(ch.get("style")), "serves": text(ch.get("serves")),
                    "builds_on": [str(x) for x in (ch.get("builds_on") or [])],
                    "enables": [str(x) for x in (ch.get("enables") or [])],
                    "topics": parse_topics(ch.get("topics")),
                    "tier_scope": {str(k).lower(): text(v)
                                   for k, v in (ch.get("tiers") or {}).items()},
                    "legacy_counts": {"interview": ch.get("interview_questions"),
                                      "thought_leadership": ch.get("thought_leadership_ideas")},
                })
    return chapters, "\n".join(tree)


def build(plan, out, writer, profile_name, profile, files):
    chapters, tree = collect(plan, out, files)
    tiers = profile["tiers"][:clamp(plan.get("tier_count", MAX_TIERS), 2, MAX_TIERS, MAX_TIERS)]
    plan_counts = {str(k): v for k, v in (plan.get("counts") or {}).items()}
    titles_base = {f["stem"]: f.get("title", f["stem"]) for f in files}

    for i, c in enumerate(chapters):
        prev_c = chapters[i - 1] if i else None
        nxt_c = chapters[i + 1] if i + 1 < len(chapters) else None
        counts = {}
        for f in files[1:]:
            raw = c["legacy_counts"].get(f["stem"]) or plan_counts.get(f["stem"])
            counts[f["stem"]] = clamp(raw, 1, 20, f["count"]) if raw is not None else f["count"]

        ctx = dict(c)
        ctx.update({
            "profile_name": profile_name, "tiers": tiers, "files": files, "counts": counts,
            "titles": {s: c["chapter"] if s == "learning" else f"{t} — {c['chapter']}"
                       for s, t in titles_base.items()},
            "prev": prev_c["chapter"] if prev_c else "",
            "next": nxt_c["chapter"] if nxt_c else "",
            "prev_rel": os.path.relpath(os.path.join(prev_c["path"], "learning.md"),
                                        c["path"]) if prev_c else "",
            "next_rel": os.path.relpath(os.path.join(nxt_c["path"], "learning.md"),
                                        c["path"]) if nxt_c else "",
        })

        writer.mkdir(c["path"])
        writer.write(os.path.join(c["path"], "learning.md"), learning_stub(ctx))
        for spec in files[1:]:
            writer.write(os.path.join(c["path"], f"{spec['stem']}.md"), slot_stub(ctx, spec))

    writer.write(os.path.join(out, "README.md"),
                 readme(plan, profile_name, tiers, files, tree))
    writer.write(os.path.join(out, "PLAN.md"), plan_md(plan, profile_name, tiers, tree))
    writer.write(os.path.join(out, "progress.md"), progress_md(chapters, files))
    return tree, chapters


def main():
    ap = argparse.ArgumentParser(description="Scaffold a learning repo from a plan file.")
    ap.add_argument("plan", help="path to plan.yaml or plan.json")
    ap.add_argument("--out", help="output directory (default: ./<repo_name>)")
    ap.add_argument("--dry-run", action="store_true", help="print the tree, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args()

    plan = load_plan(args.plan)
    warns = validate(plan)
    profile_name, profile = resolve_profile(plan)
    files = chapter_files(profile)
    out = args.out or os.path.join(".", slug(plan["repo_name"]))

    writer = Writer(args.dry_run, args.force)
    tree, chapters = build(plan, out, writer, profile_name, profile, files)

    print(tree)
    print()
    n_mod = sum(len(s.get("modules") or []) for s in plan["sections"])
    n_top = sum(len(c["topics"]) for c in chapters)
    print(f"{'would create' if args.dry_run else 'created'}: profile {profile_name}, "
          f"{len(plan['sections'])} sections, {n_mod} modules, {len(chapters)} chapters, "
          f"{n_top} topics, {writer.files} files in {out}")
    if warns:
        print(f"\n{len(warns)} thin brief(s) - the stub will be vaguer than it should be:")
        for w in warns[:10]:
            print(f"  {w}")
        if len(warns) > 10:
            print(f"  ... and {len(warns) - 10} more")
    if writer.skipped:
        print(f"\nskipped {len(writer.skipped)} existing file(s); use --force to overwrite:")
        for p in writer.skipped[:10]:
            print(f"  {p}")


if __name__ == "__main__":
    main()
