#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Scaffold a goal-based learning repository from a plan file.

Usage:
    uv run scaffold.py plan.yaml [--out ./repo] [--dry-run] [--force]
    python3 scaffold.py plan.json ...      # works too; YAML needs PyYAML installed

Every chapter gets the selected files (learning, examples, practice by default).
The profile decides the tier ladder and activity labels. Creates stubs only: the brief tells
the learner what to write and how deep, and never writes it for them.
"""

import argparse
import json
import os
import re
import sys

MAX_TIERS = 4
DEFAULT_FILES = ["learning", "examples", "practice"]

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
            "practice": {"item": "Experiment", "count": 2,
                         "slots": ["Hypothesis", "Setup", "Run for", "What actually happened",
                                   "Keep, adjust, or drop"],
                         "framing": "You cannot read your way to a habit. Run it and record what happened."},
            "interview": {"title": "Hard Questions", "count": 3,
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
            "practice": {"item": "Drill", "count": 3,
                         "slots": ["Question type", "My attempt", "Where I lost time", "Fix"],
                         "framing": "Timed drills in the exam's own question format."},
            "interview": {"title": "Examiner Questions", "count": 3,
                          "framing": "Questions in the exam's phrasing, including the ones "
                                     "designed to catch you out."},
            "quizzies": {"count": 5},
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
        "stem": "examples", "title": "Examples", "item": "Example", "count": 2,
        "slots": ["Source", "Why it works", "What to take from it", "My annotation"],
        "framing": "Worked examples or specimens to study, with sources or original-example labels.",
    },
    {
        "stem": "practice", "title": "Practice", "item": "Task", "count": 2,
        "slots": ["Task", "Tier", "What done looks like", "What I actually did", "What broke"],
        "hints": {"Tier": "{tiers}"},
        "framing": "Tasks you do, not read. Each one should be small enough to finish in a sitting.",
    },
    {
        "stem": "interview", "title": "Interview Questions", "item": "Q", "count": 3,
        "slots": ["Question", "Type", "Answer", "Follow-up they'd ask"],
        "hints": {"Type": "recall | applied | design | debugging"},
        "framing": "Questions someone else puts to you, at your target level. "
                   "Mix recall, applied, and judgement.",
    },
    {
        "stem": "thought_leadership", "title": "Thought Leadership", "item": "Idea", "count": 1,
        "slots": ["Angle", "Hook", "Audience", "Platform", "Evidence I have"],
        "hints": {"Angle": "A useful claim or synthesis for the intended audience.",
                  "Platform": "LinkedIn post | Medium article | talk | internal writeup",
                  "Evidence I have": "A benchmark, incident, migration, or artefact you can point to."},
        "framing": "Public-writing angles. Ship only what you have actually done or verified.",
    },
    {
        "stem": "quizzies", "title": "Quizzies", "item": "Q", "count": 3,
        "slots": ["Question", "My answer, from memory", "Verified?", "Revisit on"],
        "hints": {"Verified?": "yes | no - check against a source, not against your own notes"},
        "framing": "Self-assessment. Write the questions early, answer them later with the "
                   "notes closed. Put model answers separately when useful.",
    },
]

# Tier prompts by ladder position, deliberately domain-neutral.
TIER_PROMPTS = [
    "What each topic *is*, in your own words, plus the vocabulary you need to read anything "
    "else about it. A short plain-language explanation is a useful starting point.",
    "How you actually use it under real constraints. What it costs, where it breaks, and the "
    "mistakes to watch for. Distinguish real experience from illustrative cases.",
    "How it fits into a whole system. What you would choose instead, and the trade-off you "
    "would defend out loud to someone who disagrees.",
    "Where the received wisdom is incomplete, contested, or wrong - and the evidence you have "
    "for saying so. Established knowledge and open questions can both belong here.",
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
        if not 1 <= len(tiers) <= MAX_TIERS or any(not n.strip() or not d.strip() for n, d in tiers):
            die("profile: custom requires 1-4 `tiers:` entries with nonempty names and definitions.")
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

    def required_string(obj, key, loc):
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            errs.append(f"{loc}: `{key}` must be a nonempty string")

    def children(obj, key, loc):
        items = obj.get(key)
        if not isinstance(items, list) or not items or any(not isinstance(x, dict) for x in items):
            errs.append(f"{loc}: `{key}` must be a nonempty list of mappings")
            return []
        return items

    for key in ("repo_name", "goal"):
        required_string(plan, key, "plan")
    if not text(plan.get("goal_check")):
        warns.append("plan: no `goal_check` - define how the learner will demonstrate the overall goal")
    chapters = []
    for si, sec in enumerate(children(plan, "sections", "plan"), 1):
        loc = f"section {si}"
        required_string(sec, "name", loc)
        if not sec.get("arc"):
            warns.append(f"{loc} ({sec.get('name', '?')}): no `arc` - chapters will not say "
                         f"where they sit in the section's story")
        mods = children(sec, "modules", loc)
        for mi, mod in enumerate(mods, 1):
            mloc = f"{loc}/module {mi}"
            required_string(mod, "name", mloc)
            chaps = children(mod, "chapters", mloc)
            for ci, ch in enumerate(chaps, 1):
                cloc = f"{mloc}/chapter {ci}"
                nm = ch.get("name")
                required_string(ch, "name", cloc)
                required_string(ch, "purpose", cloc)
                topics = ch.get("topics")
                if not isinstance(topics, list) or not topics:
                    errs.append(f"{cloc}: `topics` must be a nonempty list")
                else:
                    for topic in topics:
                        if isinstance(topic, dict):
                            required_string(topic, "name", f"{cloc}/topic")
                            covers = topic.get("covers", [])
                            if not isinstance(covers, list) or any(not isinstance(x, str) for x in covers):
                                errs.append(f"{cloc}/topic: `covers` must be a list of strings")
                        elif not isinstance(topic, str) or not topic.strip():
                            errs.append(f"{cloc}: each topic must be a name or mapping with a name")
                for field in ("depth", "serves", "completion_check"):
                    if not text(ch.get(field)):
                        warns.append(f"{cloc} ({nm or '?'}): no `{field}`")
                for field in ("builds_on", "enables"):
                    refs = ch.get(field, [])
                    if not isinstance(refs, list) or any(not isinstance(x, str) or not x.strip() for x in refs):
                        errs.append(f"{cloc}: `{field}` must be a list of chapter names")
                chapters.append(ch)
    if errs:
        die("invalid plan:\n  - " + "\n  - ".join(errs))

    positions = {}
    for i, ch in enumerate(chapters):
        positions.setdefault(ch["name"], []).append(i)
    for i, ch in enumerate(chapters):
        for field in ("builds_on", "enables"):
            for name in ch.get(field, []):
                matches = positions.get(name, [])
                if len(matches) != 1:
                    kind = "unknown" if not matches else "ambiguous"
                    errs.append(f"{ch['name']}: `{field}` references {kind} chapter {name!r}")
                elif matches[0] == i or (field == "builds_on" and matches[0] > i) or (field == "enables" and matches[0] < i):
                    direction = "earlier" if field == "builds_on" else "later"
                    errs.append(f"{ch['name']}: `{field}` must reference a chapter appearing {direction}: {name!r}")
    if errs:
        die("invalid dependencies:\n  - " + "\n  - ".join(errs))
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
    """The same key set in all selected files, so tooling never special-cases one."""
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
    return "\n>\n".join(lines)


def nav(ctx, stem):
    sibs = " · ".join(
        f"[{s.replace('_', ' ')}]({s}.md)" for s in (f["stem"] for f in ctx["files"]) if s != stem
    )
    out = f"**This chapter:** {sibs}" if sibs else ""
    if ctx["prev_rel"]:
        out += f"\n\n**Previous:** [{ctx['prev']}]({ctx['prev_rel']})"
    if ctx["next_rel"]:
        out += f"\n\n**Next:** [{ctx['next']}]({ctx['next_rel']})"
    return out


def brief_block(ctx):
    """The full brief - learning.md only. Says what to write and how deep; never writes it."""
    paras = [
        "## Brief",
        "<!-- Chapter assignment from the plan. Adapt when scope changes, keeping the machine-readable "
        "plan and PLAN.md consistent. Preserve existing learner work. -->",
        f"**Purpose:** {ctx['purpose']}",
    ]
    for label, value in (("Depth required", ctx["depth"]), ("Style", ctx["style"]),
                         ("Assumes you already have", ", ".join(ctx["builds_on"])),
                         ("Unblocks later", ", ".join(ctx["enables"])),
                         ("Completion check", ctx["completion_check"]),
                         ("Estimated effort", ctx["effort"])):
        if value:
            paras.append(f"**{label}:** {value}")

    topics = ["**Topics to cover:**", ""]
    for i, t in enumerate(ctx["topics"], 1):
        line = f"{i}. **{t['name']}**"
        if t["covers"]:
            line += " — " + ", ".join(t["covers"])
        topics.append(line)
        if t["depth"]:
            topics[-1] += f" *Depth:* {t['depth']}"
    paras.append("\n".join(topics))
    return "\n\n".join(paras)


def brief_lite(ctx, spec):
    """Compact assignment, with the full coverage contract one link away."""
    names = ", ".join(t["name"] for t in ctx["topics"])
    out = (f"**This file's job:** {spec['framing']}\n\n**Chapter purpose:** {ctx['purpose']}"
           f"\n\n**Topics in scope:** {names}")
    if ctx["depth"]:
        out += f"\n\n**Depth target:** {ctx['depth']}"
    if ctx["completion_check"]:
        out += f"\n\n**Completion check:** {ctx['completion_check']}"
    return out + "\n\nBefore filling this file, read the [full chapter brief](learning.md#brief) for topic coverage, depth, and prerequisites. Keep this activity within that assignment."


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
        blocks.append("\n\n".join(line for line in lines if line))

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
    return f"\n## {title}\n\n" + "".join(f"- {i}\n" for i in items)


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

{text(plan['goal'])}

{meta_lines(plan)}
## How this repo is organised

```
section/            numbered, broad area
  module/           numbered within its section
    chapter/        a coherent unit of study - selected chapter files
{file_list}
```

Every generated file starts as a **stub**. Its brief guides the content and depth. Adapt the prompts to your goal, and fill the material yourself or with an agent; keep model answers separate from your own attempts.

## The ladder — `{profile_name}` profile

{ladder}

{defs}

Start with the linked roadmap in `PLAN.md`, then follow chapter order. `learning.md` has one section per selected rung. Use each chapter's completion check to decide when to move on; filled headings and activity slots alone do not demonstrate the capability. Where an older plan lacks a check, define one from its goal and depth before studying.

## Tracking

Every file carries the same frontmatter: `status` (`todo` → `learning` → `drafted` → `mastered`) and `tier_reached` (`none` → the top rung you can defend). `builds_on`, `enables`, `prev`, and `next` say how the chapter connects to the rest — follow them rather than reading the tree top to bottom.

## Files

- `PLAN.md` — linked roadmap with chapter assignments and completion checks. Keep it consistent with the input plan.yaml or plan.json when changing scope. Prefer targeted edits once files contain learner work; `--force` replaces files and resets generated progress. Changing the selected files does not delete old files.
- `progress.md` — tracker.
{bullets("Out of scope", plan.get("excluded"))}
## Structure

```
{tree}
```
"""


def table_cell(value):
    return text(value).replace("|", "&#124;")


def roadmap(chapters, out):
    rows = ["| Chapter | Purpose | Coverage and depth | Prerequisites | Completion check | Effort |",
            "|---|---|---|---|---|---|"]
    for c in chapters:
        path = os.path.relpath(os.path.join(c["path"], "learning.md"), out)
        topics = []
        for t in c["topics"]:
            entry = t["name"]
            if t["covers"]:
                entry += ": " + ", ".join(t["covers"])
            if t["depth"]:
                entry += f" (depth: {t['depth']})"
            topics.append(entry)
        coverage = "; ".join(topics)
        if c["depth"]:
            coverage += f". Chapter depth: {c['depth']}"
        cells = [f"[{c['chapter']}]({path})", c["purpose"], coverage,
                 ", ".join(c["builds_on"]) or "None specified",
                 c["completion_check"] or "Not specified — define before study",
                 c["effort"] or "Not estimated"]
        rows.append("| " + " | ".join(table_cell(x) for x in cells) + " |")
    return "\n".join(rows)


def plan_md(plan, profile_name, tiers, tree, chapters, out):
    return f"""# Plan

## Goal

{text(plan['goal'])}

**Goal check:** {text(plan.get('goal_check')) or 'Not specified — define how to demonstrate the goal before study.'}

{meta_lines(plan)}
- **Profile:** {profile_name}
- **Ladder:** {" → ".join(n for n, _ in tiers)}
{bullets("Out of scope", plan.get("excluded"))}{bullets("Assumptions", plan.get("assumptions"))}{bullets("Research notes", plan.get("research_notes"))}
## Roadmap

Read in this order. Completion checks describe evidence of learning; the files start as briefs, not completed lessons. Effort estimates, when supplied, include study and practice and depend on starting knowledge.

{roadmap(chapters, out)}

## Structure

```
{tree}
```

<!-- Keep this summary and the input plan.yaml or plan.json consistent when scope changes. The scaffolder reads that input, not PLAN.md. Preserve existing learner work when updating files. -->
"""


def progress_md(chapters, files):
    rows = "\n".join(
        f"| {c['section']} | {c['module']} | {c['chapter']} | {len(c['topics'])} | none | todo |"
        for c in chapters
    )
    checklist = ""
    for c in chapters:
        checklist += f"\n### {c['section']} › {c['module']} › {c['chapter']}\n\n"
        if c["completion_check"]:
            checklist += f"- [ ] Demonstrate: {c['completion_check']}\n"
        for f in files:
            checklist += f"- [ ] {f['stem']}.md\n"
        checklist += "\n<details><summary>Topics in learning.md</summary>\n\n"
        for t in c["topics"]:
            checklist += f"- [ ] {t['name']}\n"
        checklist += "\n</details>\n"

    return f"""# Progress

Status: `todo` → `learning` → `drafted` → `mastered`. Mark mastery from the chapter completion check; file checkboxes track material, not demonstrated learning. Tier reached records the level demonstrated.

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


def chapter_files(profile, plan):
    """Select known files in canonical order, always retaining learning.md."""
    selected = plan.get("chapter_files", DEFAULT_FILES)
    known = {f["stem"] for f in FILES}
    if (not isinstance(selected, list) or not selected
            or any(not isinstance(s, str) or s not in known for s in selected)
            or len(set(selected)) != len(selected) or "learning" not in selected):
        die("`chapter_files` must be a list of unique file stems including learning; "
            f"choose from {', '.join(sorted(known))}")
    overrides = profile.get("files") or {}
    return [dict(base, **overrides.get(base["stem"], {})) for base in FILES if base["stem"] in selected]


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
                    "completion_check": text(ch.get("completion_check")), "effort": text(ch.get("effort")),
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
    default_tiers = len(profile["tiers"]) if profile_name == "custom" else 2
    tiers = profile["tiers"][:clamp(plan.get("tier_count", default_tiers), 1, MAX_TIERS, default_tiers)]
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
    writer.write(os.path.join(out, "PLAN.md"), plan_md(plan, profile_name, tiers, tree, chapters, out))
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
    files = chapter_files(profile, plan)
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
