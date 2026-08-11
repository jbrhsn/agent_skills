<!--
============================================================
CHAPTER INTRO TEMPLATE  (00-intro.md)
============================================================
READ THIS FIRST — THE THREE HARD RULES

1. AUTHORED LAST. This file is a DERIVED artifact. Do not write it until
   EVERY topic note in this chapter folder (01-*.md, 02-*.md, ...) is
   complete, plus interview-prep.md and thought-leadership.md. Its whole
   job is to synthesise notes that already exist. If any sibling note is
   still a stub, STOP and author that note first.

2. NO NEW FACTS. Every claim, number, name, and definition in this file
   must already appear in a sibling topic note in this same chapter. You
   are summarising and connecting, not researching. If you catch yourself
   introducing a fact that is not in the notes, either delete it or go add
   it to the proper topic note first.

3. LINKS MUST RESOLVE. Every relative link must point to a file that
   ACTUALLY EXISTS in this folder. Check the real filenames on disk; do not
   guess slugs.

STRUCTURE IS A MENU, NOT A CONTRACT. The sections below are the suggested
shape. Keep the ones that help this chapter; drop the ones that do not
apply; reorder if a different order reads better. The only sections you
should never drop are the topic map, "How the Topics Connect," and the
suggested reading order.

VOICE (whole file): write for a bright 14-year-old. Short sentences, plain
words. Expand every acronym on first use, e.g. "Application Programming
Interface (API)". Define jargon inline, in plain words, the moment you use
it. PROSE carries the explanation — bullets list things, they never replace
an explanation.

LENGTH: aim for a 5–10 minute read. This is an orientation, not a lesson.
============================================================
-->

<!--
============================================================
HOW TO AUTHOR THIS FILE — FOLLOW THE PHASES IN ORDER
============================================================
Do the phases in order. Do not skip ahead to writing prose. Keep a scratch
"working notes" area (a scratchpad, not a saved file) for Phases 1 and 2 —
you will copy from it in Phase 3.

------------------------------------------------------------
PHASE 0 — VERIFY YOU ARE ALLOWED TO START
------------------------------------------------------------
1. List the chapter folder. Read the ACTUAL filenames. Do not work from
   memory or from the chapter title.
2. Write down every numbered topic file you found: 01-*.md, 02-*.md, and so
   on. Also note interview-prep.md and thought-leadership.md.
3. Open each one and decide: complete, or stub? It is a STUB if any of these
   is true:
     - the file is empty;
     - the file is a single HTML comment line;
     - the file is only an H1 heading (with or without a metadata line);
     - the file contains placeholder brackets like [Topic Title] or the
       words TODO / TBD / STUB;
     - there is too little written to summarise in one honest sentence.
4. DECISION RULE:
     - All numbered topic notes complete  -> continue to Phase 1.
     - One or more is a stub              -> STOP. Do not write this file.
5. If you stopped: report the exact filenames that are stubs, and say that
   00-intro.md cannot be authored until they are written. THIS IS THE
   EXPECTED, CORRECT BEHAVIOUR. It is not a failure and it is not something
   to work around by guessing, by writing a thinner intro, or by filling the
   gaps from your own knowledge. Stopping here is the right answer.

------------------------------------------------------------
PHASE 1 — READ EVERY SIBLING TOPIC NOTE IN FULL
------------------------------------------------------------
Read them. In full. Not the headings, not the first paragraph — the whole
note. You cannot connect topics you have not read.

For EACH numbered topic note, add one row to your working notes using this
scaffold. Copy the filename from the folder listing in Phase 0; never retype
it from the title, and never invent a slug:

  | # | exact filename on disk | real H1 title | in one line, what it teaches |

Then do the same two extra rows for interview-prep.md and
thought-leadership.md.

This table IS the Topic Map section later. Count the rows. That count is the
number you put in "Topics:" in the metadata line (numbered topic files only).

------------------------------------------------------------
PHASE 2 — BUILD THE CONNECTION MAP BEFORE WRITING ANY PROSE
------------------------------------------------------------
This phase is the core of the file. Do it as a list, in working notes,
BEFORE you write a single sentence of "How the Topics Connect."

Method, mechanically:
1. Write out every PAIR of topics: 1-2, 1-3, 2-3, and so on. With 4 topics
   that is 6 pairs; with 5 topics, 10 pairs. Do not skip pairs.
2. For each pair, ask: does a REAL relationship appear in the notes? Use
   only these four relationship types as your vocabulary:
     DEPENDS ON — you cannot understand B until you know A.
     MOTIVATES  — A creates the problem that B exists to solve.
     CONTRASTS  — B is the other way of doing what A does.
     EXTENDS    — B is A applied to a harder case.
3. If yes, write ONE line in this exact shape:
     Topic A -[TYPE]-> Topic B : <what specifically carries over>
4. If no, write:
     Topic A / Topic B : INDEPENDENT — no relationship in the notes.

TEST FOR A GOOD ENTRY (apply to every line you wrote):
  - Does the line name WHAT specifically carries over — a named idea, term,
    constraint, or result from A that B reuses? If yes, keep it.
  - Does the line only say B "builds on" or "relates to" or "follows from"
    A? Then it FAILS. Rewrite it naming the specific thing, or mark the pair
    INDEPENDENT.

Saying two topics are INDEPENDENT is a legitimate and useful answer. Write
it down. A chapter where two topics genuinely do not touch is normal, and
telling the reader that saves them looking for a link that is not there.
Never invent a relationship to fill a line.

WORKED MICRO-EXAMPLE — ILLUSTRATION ONLY, FROM AN UNRELATED EVERYDAY DOMAIN
(bicycle maintenance). This is NOT your chapter's subject. Copy the SHAPE of
these lines, never the content:

  Checking Tyre Pressure -[MOTIVATES]-> Fixing a Puncture : a soft tyre is
    usually the first sign of a slow puncture, so the pressure check is what
    sends you looking for the hole.
  Removing the Wheel -[DEPENDS ON]-> Fixing a Puncture : you cannot patch
    the inner tube until the wheel is off, so the wheel-removal steps are a
    prerequisite for every patch.
  Patching a Tube -[CONTRASTS]-> Replacing a Tube : both fix the same flat
    tyre; you choose by whether the hole is small enough to seal and whether
    you are carrying a spare.
  Adjusting Brakes -[EXTENDS]-> Removing the Wheel : brake adjustment is
    the same cable-tension idea from wheel removal, applied to the harder
    case where the pads must also stay centred.
  Checking Tyre Pressure / Adjusting Brakes : INDEPENDENT — no relationship
    in the notes.

------------------------------------------------------------
PHASE 3 — DRAFT THE SECTIONS
------------------------------------------------------------
Now write, in this order, using the scaffolds further down this file:
1. Topic Map — paste in the Phase 1 table rows. Filenames from disk.
2. What This Chapter Is About — 2 to 4 prose paragraphs.
3. What You'll Learn Here — the arc, then capabilities. Every capability
   must be traceable to a specific Phase 1 row.
4. How the Topics Connect — turn each Phase 2 line into prose. One line
   becomes one or two sentences. Group related lines into paragraphs. If you
   marked a pair INDEPENDENT, say so plainly in a sentence.
5. Optional relationship diagram — draw the arrows from your Phase 2 lines.
6. Suggested Reading Order — the order plus the reason. The reason comes
   from your DEPENDS ON lines: a topic that others depend on goes earlier.
7. Optional sections — include only if you have real material. Otherwise
   delete the whole section. Do not write filler.
8. Metadata line — real summed numbers, real topic count.

------------------------------------------------------------
PHASE 4 — VERIFY LINKS MECHANICALLY
------------------------------------------------------------
1. Search your draft for every relative link, i.e. every "](./".
2. Make a list of the filenames inside those links.
3. For each one, confirm a file with that EXACT name exists in this chapter
   folder. Character by character. Compare against the Phase 0 listing.
4. Any link with no matching file: fix it to the real filename, or remove
   the link.
5. Count the links you checked. Write the number down; you need it for the
   self-check table.

A GUESSED SLUG IS THE MOST COMMON DEFECT IN THIS FILE. Writing
./02-error-handling.md when the file on disk is ./02-handling-errors.md
produces a broken link that looks perfectly fine in the source. Check every
one against disk.

------------------------------------------------------------
PHASE 5 — VERIFY NO NEW FACTS
------------------------------------------------------------
1. Go through the draft and underline every specific claim: every number,
   date, name, version, threshold, definition, and cause-and-effect claim.
2. For EACH one, name the sibling note it came from. Write it as:
     "<claim>" -> came from <filename>
3. Any claim you cannot trace to a sibling note has two allowed outcomes:
     a) CUT it from this file; or
     b) add it to the correct topic note first, as a separate piece of work,
        then cite that note here.
4. There is no third outcome. Inventing the fact here, or filling it in from
   your own knowledge, is a FAILURE of this file's job. This file summarises
   notes that exist; it does not research.
5. Vague, unsourced softeners ("this is widely considered...", "most
   practitioners agree...") count as new facts. Cut them.

------------------------------------------------------------
PHASE 6 — STOP CONDITIONS
------------------------------------------------------------
STOP and ask, rather than guessing, if ANY of these is true:
1. A numbered topic note is a stub, empty, or too thin to summarise.
   -> Name the files. Do not write this intro.
2. The chapter's topics have no discernible relationships at all — every
   pair in Phase 2 came out INDEPENDENT.
   -> Say so. "How the Topics Connect" cannot be honestly written, and that
      may mean the chapter's grouping needs review.
3. A fact you need for the intro appears in NO sibling note.
   -> Say which fact and which note you think should own it. Do not supply
      the fact yourself.
4. Two sibling notes contradict each other.
   -> Report the contradiction. Do not silently pick a side.
In every one of these cases, stopping and reporting is the correct outcome.
============================================================
-->

# [Chapter Title]

**Section:** [Section] | **Module:** [Module] | **Est. total time:** [X hrs across all topics] | **Topics:** [N]

<!-- Metadata line: "Est. total time" is the SUM of the est. times on the
     sibling topic notes, plus a little for interview-prep and
     thought-leadership. Add the real numbers; do not invent a round one.
     "Topics" is the count of numbered topic files (01-*, 02-*, ...). -->

---

## What This Chapter Is About

<!-- 2–4 short prose paragraphs, no bullets. Cover: what the whole chapter
     is about, said once and simply; why it matters — what a person can do
     afterwards that they could not before; what problem this chapter exists
     to solve. Do not list the topics yet; that is the topic map's job.
     Write it so someone who has never heard the chapter title could follow
     the first paragraph. -->

[Opening paragraph: the big idea of this chapter in plain words.]

[Second paragraph: why it matters, and what goes wrong for people who skip it.]

---

## What You'll Learn Here

<!-- The chapter's ARC — where you start, what you pick up along the way,
     where you end up. A short paragraph of prose first, then (optionally)
     3–6 short bullets naming the concrete capabilities.
     Every capability named here must be genuinely taught by one of the
     sibling topic notes. Do not promise anything the notes do not deliver. -->

[Prose paragraph describing the journey through this chapter, start to finish.]

By the end you should be able to:

- [Capability drawn from a topic note]
- [Capability drawn from a topic note]
- [Capability drawn from a topic note]

---

## Topic Map

<!-- One row per file in this chapter folder, in file order.
     - The link must be the REAL relative filename (e.g. ./01-my-topic.md).
     - The description is ONE line, plain language, no jargon. Say what the
       reader will be able to do or understand, not just restate the title.
     - Include interview-prep.md and thought-leadership.md as rows too.
     - Do NOT include this file (00-intro.md) or 99-podcast.md as rows;
       mention the podcast in the reading order instead. -->

| # | Topic | What it covers | Est. time |
|---|---|---|---|
| 1 | [Topic Title](./01-[topic-slug].md) | [One plain-language line.] | [X hrs] |
| 2 | [Topic Title](./02-[topic-slug].md) | [One plain-language line.] | [X hrs] |
| 3 | [Topic Title](./03-[topic-slug].md) | [One plain-language line.] | [X hrs] |
| — | [Interview Prep](./interview-prep.md) | [One plain-language line.] | [X min] |
| — | [Thought Leadership](./thought-leadership.md) | [One plain-language line.] | [X min] |

---

## How the Topics Connect

<!-- ★ THE MOST IMPORTANT SECTION IN THIS FILE. ★
     A learner can read a topic map anywhere. What they cannot get anywhere
     else is the SHAPE of the chapter — why these topics sit together, and
     how each one leans on the others.

     Write it as PROSE, several paragraphs, not a list. For each topic make
     at least one relationship explicit, and say WHY:
       DEPENDS ON — you cannot understand B until you know A, because...
       MOTIVATES  — A creates the problem that B exists to solve.
       CONTRASTS  — B is the other way of doing what A does; you pick on...
       EXTENDS    — C is A applied to a harder case.
     "Topic 2 builds on Topic 1" with no reason is not acceptable — say what
     specifically carries over. Only use relationships the notes support. If
     two topics are genuinely independent, say so plainly; that is useful. -->

[Paragraph explaining the first link in the chain: what the first topic sets up, and which later topic needs it.]

[Paragraph explaining the middle of the chapter: what motivates what, and where two topics offer competing answers to the same question.]

[Paragraph explaining where it all lands, and how the last topic pulls the earlier ones together.]

### [Optional] Topic Relationship Diagram

<!-- OPTIONAL but strongly encouraged — a picture of the dependencies is
     often worth three paragraphs. Rules: plain fenced code block with NO
     language tag; box-drawing characters only (──►  │  ├  └  ─  ┌  ┐  ┘);
     label arrows with the relationship where it fits; keep it small enough
     to read at a glance. Add a sentence or two underneath explaining the
     takeaway — a diagram with no caption is incomplete.

     EXAMPLE ONLY — shape to copy, from an unrelated everyday domain
     (baking). Replace it entirely with this chapter's real topics:

       Ingredients ──► Mixing ──► Baking ──► Cooling
                          │                    │
                          └──► Substitutions   └──► Storage
-->

```
[Topic 1] ──► [Topic 2] ──► [Topic 4]
                 │
                 ├──► [Topic 3]   (an alternative to Topic 2)
                 └──► [Topic 5]   (Topic 2 applied to a harder case)
```

[One or two sentences: what this diagram tells the reader about the chapter's shape.]

---

## Suggested Reading Order

<!-- The order, plus ONE line saying why that order. The "why" is the point
     of this section — an order with no reason is just the topic map again.
     If file order is already the best order, say that and explain why.
     If a different order reads better, say so and explain the trade-off.
     Mention where 99-podcast.md fits: some learners want the intuition
     first, others want it as a review afterwards. Say both are fine. -->

1. [Topic 1] — [why it goes first]
2. [Topic 2] — [why it follows]
3. [Topic 3] — [why it follows]
4. [Interview Prep] and [Thought Leadership] — [why these come after the topics]

**Why this order:** [One or two sentences in plain language.]

**About the podcast:** [Podcast Transcript](./99-podcast.md) walks through the whole chapter conversationally. Listen or read it before the topics if you want the big picture first, or afterwards to check what stuck. Either works.

---

## [Optional] Before You Start

<!-- OPTIONAL — include only if this chapter genuinely leans on earlier
     material. Name the specific idea the reader needs and where it was
     covered, in prose. Do not write a vague "you should know the basics."
     If there are no real prerequisites, delete this whole section rather
     than writing filler. -->

[Prose: what you should already be comfortable with, and where it was covered.]

---

## [Optional] How This Chapter Fits

<!-- OPTIONAL — one short paragraph looking backwards and one looking
     forwards. Name the previous and next chapter by title. Only claim
     things you can support from the chapter notes you have. If you do not
     know what comes next, delete this section rather than guessing. -->

[Paragraph: what the previous chapter set up that this one uses, and what this chapter unlocks for the next one.]

---

<!-- ============================================================
     SELF-CHECK — run before saving.
     Every row needs RECORDED EVIDENCE, not a "yes." Fill in the Evidence
     column with the actual number, filename, or quoted line. A ticked row
     with no evidence written next to it COUNTS AS A FAILED ROW.
     ============================================================

     | Check                                                        | Evidence to record                                      |
     | ------------------------------------------------------------ | ------------------------------------------------------- |
     | Phase 0 run: folder listed, every sibling note opened        | number of files listed; number of numbered topic notes   |
     | No sibling topic note is a stub                              | "checked N notes, 0 stubs" (else you must have STOPPED)  |
     | Phase 1 done: every topic note read in full                  | number of notes read in full, and their exact filenames  |
     | Phase 2 done: connection map built before prose              | number of pairs examined; number of map entries written  |
     | Every connection names WHAT carries over, not just "builds on"| quote one map entry as a sample                          |
     | Independent pairs stated plainly rather than faked           | number of pairs marked INDEPENDENT (may be 0)            |
     | No fact here is absent from the sibling topic notes          | number of claims traced; each one's source filename      |
     | Phase 4 done: every relative link checked against disk       | number of links verified; number fixed                   |
     | Topic map has one row per topic file, in file order          | row count vs numbered-file count (must be equal)         |
     | Metadata "Topics: N" equals the numbered-file count          | the two numbers                                          |
     | Metadata "Est. total time" is the real sum, not a round guess| the addends and the total                                |
     | "How the Topics Connect" is prose and names WHY, not just THAT| paragraph count; no bullet lists in that section         |
     | Reading order gives a reason, not just a sequence            | quote the "Why this order" sentence                       |
     | Every acronym is expanded on first use                       | list the acronyms used and where each is expanded         |
     | Jargon is defined inline in plain words                      | list the terms defined                                    |
     | A bright 14-year-old could follow the opening section        | longest sentence length in the opening, in words          |
     | Any diagram is in a plain fenced block with a caption        | fence has no language tag: yes/no; caption present: yes/no|
     | No TODO, TBD, STUB, or placeholder brackets remain           | searched for "TODO", "TBD", "STUB", "[" — hits found: N   |

     If any row cannot be filled with real evidence, go back and do that
     phase. Do not save the file with an empty Evidence cell.
============================================================ -->
