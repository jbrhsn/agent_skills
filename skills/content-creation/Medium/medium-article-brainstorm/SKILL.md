---
name: medium-article-brainstorm
description: Turn example Medium headlines into researched article ideas, each scaffolded as its own folder with a source.md the user writes from. Use this whenever the user pastes headings/subheadings and asks for similar topics, says "brainstorm ideas", "give me N article ideas", "what can I write about", or asks for a pillar-cluster or a post series. Also use when the user wants existing rough ideas expanded into writable briefs. Trigger even if the user does not say the word "skill" or "brainstorm" — a pasted list of headlines plus any request for more topics is enough. This is only for Medium specific brainstorming.
---

# Article Brainstorm

Produce article ideas the user can actually write, then scaffold one folder per idea containing a `source.md` brief. The user writes the article themselves; this skill only produces the seed.

## Hard rules

- **Never draft the article.** `source.md` is a brief: idea, heading, subheading, short description, 3–5 bullet outline. Nothing more. Do not write intros, paragraphs, or sample prose.
- **Never invent the user's experience.** Every idea must be anchored to something the user actually said in the interview or in `profile.md`. If an idea is attractive but unanchored, either drop it or mark it clearly (see Anchoring).
- **Do not claim performance data.** Medium engagement numbers are not public or searchable. You infer *patterns* from the user's pasted examples. Say "fits the pattern", never "this will perform well" or "this is trending on Medium".
- **Ask where to write.** If the user has not given an output directory, ask before creating anything. Never guess.
- **Every session produces fresh ideas.** Do not scan existing folders to dedupe. Just do not repeat ideas within the same session.

## Workflow

### 1. Read profile.md

Look for `profile.md` at the repo root. If it exists, read it. If not, create it later in step 3 — do not create an empty one now.

This tells you what you already know about the user so you do not ask it again.

### 2. Parse the pasted examples

The user pastes example headings/subheadings directly into chat. They are not stored anywhere and are for this session only.

Read them for **pattern**, not topic. Extract:

- **Structural form** — number list, "How I…", contrarian claim, confession, before/after, tool comparison, "X is dead"
- **The promise** — what the reader is told they will get
- **The tension** — what makes it clickable: a stake, a taboo, a reversal, a specific cost
- **Specificity markers** — named tools, real numbers, timeframes, first-person stakes
- **Voice** — blunt, technical, personal, snarky

State the pattern back to the user in 3–4 lines before you interview. This gives them a chance to correct you cheaply, before you spend tokens on research.

### 3. Interview

Ask in **batches of 3–5 questions**. Numbered, short, answerable in a line each. Never one at a time. Never more than five in a batch.

Skip anything already answered in `profile.md`. Only probe the gaps.

Typically two batches, three at most. Cover:

- Domain and day job — what they build, with what stack
- Concrete war stories: migrations, outages, failed rewrites, tools abandoned, things they changed their mind about
- Opinions they hold that their peers do not
- Who they are writing for
- Anything they explicitly refuse to write about

Ask for **specifics over categories**. "Which database migration went badly and what broke?" beats "what's your backend experience?" Vague answers produce generic ideas.

After the interview, write the new information into `profile.md` (see Profile maintenance).

### 4. Research

Use the built-in web fetch/search. If no search capability is available in this session, stop and tell the user — do not fake research from memory.

Aim for 4–8 fetches. You are looking for:

- What has already been written to death on each candidate angle — so you can find the unoccupied slot
- Current facts, versions, dates, numbers that make a heading concrete
- Live debates in the user's domain the user has a real position on

Do not fetch to pad a citation list. `source.md` has no citations field; research exists to make the *idea* sharp and current, not to decorate the brief.

### 5. Confirm scope

Confirm before writing files:

- **How many ideas.** Use the number the user gave. If they gave none, ask.
- **Where.** Use the path the user gave. If none, ask. Never guess.
- **Shape.** Standalone ideas, or a series/cluster (see Series mode).

If the user asked for N ideas but only M are genuinely anchored, write M and say why. Do not pad to hit a number — padding is how generic ideas get in.

### 6. Write the folders

One folder per idea, at the given path. Folder name is a plain lowercase slug, hyphenated, short — ideally under about 60 characters:

```
how-i-moved-from-linux-to-mac-in-a-weekend/
  source.md
why-i-stopped-using-orms/
  source.md
```

No numeric prefixes, no dates, no batch folder, no top-level index — unless it is a series.

### 7. Report back

List what you created as a short bulleted list of folder names with the heading for each. Do not paste the full `source.md` contents back into chat; the user will open the files.

## source.md format

Exactly these five sections. Nothing else.

```markdown
# <Idea in one line>

## Heading
<The proposed article title.>

## Subheading
<The proposed Medium subtitle. One line.>

## Description
<2–4 sentences: what the article argues, who it's for, and what makes it
distinct from what already exists on this topic.>

## Outline
- <point 1>
- <point 2>
- <point 3>
- <point 4 (optional)>
- <point 5 (optional)>

## Your angle
<One or two lines naming the specific experience of the user's this draws on.
Quote or paraphrase what they told you. This is the reminder of why only they
can write this one.>
```

"Your angle" is the sixth section and is deliberately short — it is a pointer back to the interview, not an expansion. Keep the whole file under roughly 40 lines.

## Series mode

Trigger a series when the user says "series", "cluster", "pillar", "multi-part", or similar.

You may also **propose** a series when the ideas you generated naturally form one — a pillar with dependent spokes, or a sequential narrative. Propose it in one sentence and wait for a yes. Never restructure the output on your own initiative.

Layout:

```
<series-slug>/
  README.md
  01-<slug>/
    source.md
  02-<slug>/
    source.md
  03-<slug>/
    source.md
```

Child folders inside a series **do** carry numeric prefixes, because publishing order is part of the point.

`README.md` contains:

```markdown
# <Series title>

## The idea
<2–4 sentences: the through-line and why these belong together.>

## How they connect
<For a pillar-cluster: which piece is the pillar and what each spoke owns,
including which spokes link back. For a sequential series: what each part
assumes the reader already read.>

## Publishing order
1. <slug> — <one line>
2. <slug> — <one line>
3. <slug> — <one line>

## Tracker
| # | Slug | Status |
|---|------|--------|
| 1 | <slug> | not started |
| 2 | <slug> | not started |
```

Pillar-cluster and sequential-series are different shapes — a pillar is a hub whose spokes stand alone, a series is a chain where part 3 assumes part 2. Ask which one the user means if it is ambiguous.

## profile.md maintenance

Lives at repo root. It is a long-lived context file, so **size is a first-class constraint**. Target under 150 lines. It should never become a transcript.

Structure:

```markdown
# Author Profile

## Domain
<stack, role, years, what they actually build>

## Experiences
- <one line per war story: what happened, what broke, what changed>

## Opinions
- <one line per position they hold>

## Audience
<who they write for>

## Avoid
<topics they refuse>

## Log
<!-- raw answers since last compaction; compacted when this exceeds ~40 lines -->
```

Rules:

- Append raw interview answers to `## Log` only.
- **When `## Log` exceeds ~40 lines, compact it**: fold the log into the structured sections above as one-line bullets, then empty the log. This is a deterministic trigger — check it at the end of every session, do not wait to be asked.
- When compacting, merge duplicates and drop anything superseded. Prefer specific facts over general claims: "migrated 40GB Postgres to Aurora, 6h downtime" survives; "experienced with databases" does not.
- Never delete `## Avoid`.
- If the file is missing, create it after the first interview.

## Anchoring

Rank candidate ideas by how much of the user's own material they carry.

- **Anchored** — draws on a named experience or stated opinion. Ship these first.
- **Adjacent** — plausibly within their expertise but not something they described. Ship only to fill a gap, and open "Your angle" with `Needs your input:` naming what you need from them.
- **Unanchored** — topically relevant but they have no stake. Drop it. Do not ship it flagged; a flagged idea the user cannot write is just a folder they will delete.

If you cannot reach the requested count with anchored and adjacent ideas, deliver fewer and say what extra experience would unlock more. Fewer good briefs beat a full quota of generic ones.