<!--
============================================================
CHAPTER PODCAST TEMPLATE  (99-podcast.md)
============================================================
HARD RULES — read before writing a single line

1. AUTHORED LAST. A DERIVED artifact. Do not write it until every topic note
   in this chapter folder (01-*.md, 02-*.md, ...) is complete. If a sibling
   note is still a stub, STOP and author that note first.

2. COVERS EVERY TOPIC. One conversational segment for every numbered topic
   file in this chapter, at a high level. None may be skipped, even short ones.

3. NO NEW FACTS. Every claim, number, name, and definition spoken here must
   already appear in a sibling topic note. You are retelling, not
   researching. Analogies are the one thing you may invent — an analogy is
   a way of explaining, not a new fact.

4. CONVERSATIONAL, NOT A LECTURE. This is two people talking. If a turn runs
   longer than roughly six sentences without the other speaker saying
   anything, it has stopped being a conversation.

5. NO CODE BLOCKS. This is spoken audio; nobody reads a fenced code block out
   loud. Describe anything technical in words — what it does and what it
   looks like, in a sentence.

VOICE: written for a bright 14-year-old. Short sentences, everyday words.
Expand every acronym on first use, out loud — e.g. "an Application
Programming Interface, an API, which is just an agreed way for two programs
to talk to each other." Any unavoidable term gets defined in plain words
immediately, in the same turn.

LENGTH: aim for 12–20 minutes of spoken material, roughly 1,500–2,500 words
of dialogue. Scale with the number of topics.

STRUCTURE IS A MENU. The flow below is the suggested shape; adapt it. Do not
drop: a hook, one segment per topic, a "how it connects" segment, a wrap-up.
============================================================
SPEAKER CONVENTION — do not improvise on this
============================================================
Exactly two speakers, both generic ROLE labels:

  **Host:**    Asks the questions a smart beginner would ask. Curious, not
               expert. Interrupts, asks "wait, why does that matter?",
               paraphrases answers back, admits confusion out loud.

  **Expert:**  Explains. Reaches for everyday analogies. Avoids jargon; when
               a term is unavoidable, defines it in plain words in the same
               breath. Answers the question actually asked, then stops.

RULES:
  - Bold the label at the start of every turn: `**Host:**` / `**Expert:**`
  - Use these exact two labels for the ENTIRE transcript. Never switch to
    "Interviewer," "Guest," "Speaker 1," or a first name partway through.
  - Do NOT invent person names, and never use the name of a real person,
    celebrity, or author. Generic role labels only. No third speaker or
    narrator.
  - You may rename the pair once, globally, if a different generic pairing
    fits better (e.g. **Host:** / **Guide:**) — then use it everywhere.
============================================================
-->

<!--
============================================================
HOW TO AUTHOR THIS FILE — FOLLOW THE PHASES IN ORDER
============================================================
Do the phases in order. Do not start drafting dialogue until Phase 2 is
done. Keep a scratch "working notes" area for Phases 1 and 2.

------------------------------------------------------------
PHASE 0 — VERIFY YOU ARE ALLOWED TO START
------------------------------------------------------------
1. List the chapter folder. Read the ACTUAL filenames. Do not work from
   memory or from the chapter title.
2. Write down every numbered topic file you found: 01-*.md, 02-*.md, ...
3. Open each one and decide: complete, or stub? It is a STUB if any of these
   is true:
     - the file is empty;
     - the file is a single HTML comment line;
     - the file is only an H1 heading (with or without a metadata line);
     - the file contains placeholder brackets like [Topic Title] or the
       words TODO / TBD / STUB;
     - there is too little written to retell in a spoken segment.
4. DECISION RULE:
     - All numbered topic notes complete  -> continue to Phase 1.
     - One or more is a stub              -> STOP. Do not write this file.
5. If you stopped: report the exact filenames that are stubs, and say that
   99-podcast.md cannot be authored until they are written. THIS IS THE
   EXPECTED, CORRECT BEHAVIOUR. It is not a failure and it is not something
   to work around by writing a shorter transcript, by skipping that topic's
   segment, or by filling the gap from your own knowledge. Stopping here is
   the right answer.

------------------------------------------------------------
PHASE 1 — READ EVERY SIBLING TOPIC NOTE IN FULL
------------------------------------------------------------
Read them. In full. Not the headings — the whole note. You cannot retell a
note you have skimmed.

For EACH numbered topic note, fill in this row in your working notes:

  | # | topic title (as the note words it) | the ONE intuition a listener
    needs | one everyday analogy that would explain it | the most common
    misunderstanding this note corrects |

Rules for filling the row:
  - Title: copy the wording the topic note uses, so a listener can match the
    segment to the note.
  - Intuition: ONE sentence, the "why," not the mechanics. If you cannot say
    it in one sentence you have not understood it yet — re-read the note.
  - Analogy: from ordinary daily life. This is the one thing you may invent.
  - Misunderstanding: it must be stated in the note, or be a wrong reading
    the note explicitly corrects. Do not invent one.

THIS INVENTORY IS THE SEGMENT PLAN. One row = one `###` segment. The number
of rows MUST equal the number of `###` segments in the finished transcript,
and both MUST equal the number of numbered topic files. Write the number
down now; you will check it again in Phase 4.

------------------------------------------------------------
PHASE 2 — PLAN THE SEGMENT ORDER AND THE HAND-OFFS
------------------------------------------------------------
1. Decide the segment order. Default: file order (01, 02, 03...). Only
   depart from file order if a topic is plainly a prerequisite for an
   earlier-numbered one; if you depart, note the reason.
2. For every BOUNDARY between consecutive segments, write ONE line in your
   working notes saying how the conversation gets from one topic to the
   next. With 4 segments there are 3 boundaries. Use this shape:
     After <Topic A>, the Host asks <question> which opens <Topic B>,
     because <the specific thing A left unresolved>.
3. Test each hand-off line: does it name something specific from Topic A
   that leads into Topic B? "Next let's talk about B" FAILS. Rewrite it.
4. Without these lines the transcript reads as disconnected blocks with
   headings between them, which is the single most common defect here.

------------------------------------------------------------
PHASE 3 — DRAFT SEGMENT BY SEGMENT, NOT ALL AT ONCE
------------------------------------------------------------
Write ONE segment. Check it. Then start the next. Repeat.

After finishing each segment, verify all FOUR of these before moving on:
  1. The Host asks the beginner's question about this topic — an actual
     question, in plain words.
  2. The Expert explains the INTUITION (the why), not parameters, syntax, or
     edge cases.
  3. At least ONE everyday analogy is present. Point at the sentence.
  4. The common misunderstanding is named out loud, AND the correct way to
     think about it is given right after.
If a segment misses any of the four, fix that segment now. Do not carry on
and plan to fix it later.

WHY ONE AT A TIME: checking a single 6-turn segment against four criteria is
reliable and takes seconds. Auditing a finished 2,000-word transcript
against the same four criteria across every segment is not reliable — you
will skim it and pass it. Check as you go.

------------------------------------------------------------
PHASE 4 — MECHANICAL DIALOGUE CHECKS
------------------------------------------------------------
These are counting tasks. Do them literally, on the finished draft. Write
each number down.

1. SEGMENT COUNT. Count `###` headings under Topic Segments. Compare to the
   number of numbered topic files and to your Phase 1 row count. All three
   must be the SAME number. Also make the metadata "Topics covered: [N]"
   equal to that number.
2. TURN COUNTS. For EACH segment, count `**Host:**` turns and `**Expert:**`
   turns. The Host must appear at least 3 times in every segment. Any
   segment with 1 or 2 Host turns is a monologue — add real questions or
   interruptions.
3. TURN LENGTH. Find every turn longer than roughly six sentences. For each,
   split it: cut it in two and put a Host reaction, paraphrase, or question
   in the middle. Record how many you split.
4. CODE FENCES. Search the whole file for a line starting with three
   backtick characters. The transcript body must contain ZERO fenced code
   blocks. Expected count: 0. Anything technical is described in words.
5. LABEL DRIFT. Search for these strings and confirm ZERO hits:
   "Guest", "Interviewer", "Speaker 1", "Speaker 2", "Narrator", "Moderator".
   Then confirm the two labels you used are byte-identical everywhere,
   including the bold markers and the colon: `**Host:**` and `**Expert:**`.
   No first names. No real people. If you renamed the pair, the new pair
   must appear everywhere with zero occurrences of the old pair.
6. ANALOGY COUNT. Count the segments containing at least one everyday
   analogy. That count must equal the segment count.

------------------------------------------------------------
PHASE 5 — VERIFY NO NEW FACTS
------------------------------------------------------------
1. Go through the transcript and underline every specific claim: every
   number, date, name, version, threshold, definition, and cause-and-effect
   claim.
2. For EACH one, name the sibling note it came from:
     "<spoken claim>" -> came from <filename>
3. Any claim you cannot trace has two allowed outcomes:
     a) CUT it; or
     b) add it to the correct topic note first, as a separate piece of work,
        then retell it here.
4. There is no third outcome. Inventing the fact here is a FAILURE of this
   file's job. This transcript retells notes that exist; it does not
   research.
5. THE ONE EXCEPTION: ANALOGIES. You may invent an everyday analogy, because
   an analogy is an explanation device, not a new fact about the subject.
   The analogy must not smuggle in a claim — if the analogy asserts
   something about the real subject that no note says, that part is a new
   fact and must go.
6. Vague unsourced softeners ("most people agree...", "it's widely known
   that...") count as new facts. Cut them.

------------------------------------------------------------
PHASE 6 — STOP CONDITIONS
------------------------------------------------------------
STOP and ask, rather than guessing, if ANY of these is true:
1. A numbered topic note is a stub, empty, or too thin to retell.
   -> Name the files. Do not write this transcript.
2. A topic's intuition cannot be explained without a fact that no sibling
   note contains.
   -> Say which topic, and which missing fact. Do not supply it yourself and
      do not skip the segment — every topic needs a segment.
3. Two sibling notes contradict each other on something the Expert would
   have to say out loud.
   -> Report the contradiction. Do not silently pick a side.
In every one of these cases, stopping and reporting is the correct outcome.
============================================================
-->

# [Chapter Title] — Podcast Transcript

**Section:** [Section] | **Module:** [Module] | **Approx. length:** [X min spoken] | **Topics covered:** [N]

<!-- "Topics covered" must equal the number of numbered topic files in this
     chapter, and must equal the number of ### segments below. -->

---

<!--
============================================================
WHAT GOOD DIALOGUE SOUNDS LIKE
============================================================
Both illustrations below are from an UNRELATED everyday domain (bicycle
gears) on purpose. Do not assume this chapter's subject. They show the shape
of a good exchange, nothing more.

✓ COMPLIANT — genuine back-and-forth, analogy, plain words, short turns:

  **Host:** So why does a bike even need gears? It has one chain and one
  set of pedals.
  **Expert:** Think about pushing a heavy box across a room. You can shove
  it hard and fast for a short burst, or lean in and push slowly but
  steadily for a long time. Gears let your legs choose which one they're
  doing.
  **Host:** Wait — so the gear doesn't make the bike stronger, it just
  changes which kind of effort I'm using?
  **Expert:** Exactly right. The energy in your legs is the same either
  way. The gear decides whether it becomes speed or climbing power.
  **Host:** Okay, so what's the thing people get wrong about this?
  **Expert:** People assume the hardest gear is the best gear. On a steep
  hill it's the worst one — you'll grind to a stop.

  Why it works: the Host interrupts and paraphrases; the Expert uses one
  everyday analogy and stays under six sentences per turn; the common
  misunderstanding is named out loud; no jargon.

✗ NON-COMPLIANT — a dense jargon monologue, no analogy, no conversation:

  **Host:** Can you explain gears?
  **Expert:** Certainly. A drivetrain's gear ratio is the quotient of the
  chainring tooth count and the cog tooth count, which determines the
  mechanical advantage available at the rear hub. Cadence optimisation
  requires selecting a ratio such that torque demand remains within the
  rider's aerobic envelope, subject to gradient and rolling resistance.
  Derailleur indexing further constrains the discrete ratio set available.
  **Host:** Interesting.

  Why it fails: one giant undefined-jargon monologue, no analogy, no genuine
  question from the Host, and the Host's reply adds nothing. A lecture
  wearing a transcript costume.
============================================================
-->

## Cold Open

<!-- 3–6 turns. Do NOT start with "welcome to the show." Open on the PROBLEM
     this chapter solves: the Host describes a frustration or puzzle in plain
     words, the Expert names it as the thing they're about to unpack. The
     listener should feel "yes, that is exactly the thing I don't get." -->

**Host:** [Pose the problem, in plain words, as a real frustration or puzzle.]

**Expert:** [Name the problem and hint that there is a clean way to think about it.]

**Host:** [React. Ask the obvious follow-up.]

---

## What We'll Cover

<!-- 2–4 turns. A quick spoken roadmap: the topics, in order, in one clause
     each. Conversational — the Expert listing them out loud, not an agenda. -->

**Host:** [Ask what ground they're going to cover.]

**Expert:** [Name each topic in one clause, in the order the segments follow.]

---

## Topic Segments

<!-- ONE `###` segment per numbered topic file, in file order. Name the topic
     in the same words the topic note uses, so a listener can match them up.

     Each segment should do FOUR things, in whatever order feels natural:
       1. The Host asks the beginner's question about this topic.
       2. The Expert explains the INTUITION — the why, not the mechanics.
          Skip parameters, syntax and edge cases; the topic note has those.
       3. At least ONE everyday analogy, from ordinary life.
       4. The most common misunderstanding, named plainly, with the correct
          way to think about it.

     Aim for 5–9 turns per segment; the Host must speak at least three times.
     A segment where the Host speaks once is a monologue — rewrite it. Hand
     off between segments in dialogue rather than jumping into the header. -->

### [Topic 1 Title]

**Host:** [The beginner's question about this topic.]

**Expert:** [The intuition, in plain words, with an everyday analogy.]

**Host:** [Interrupt — paraphrase it back, or ask why it matters.]

**Expert:** [Confirm or correct the paraphrase. Add the next piece.]

**Host:** [Ask what people usually get wrong here.]

**Expert:** [Name the common misunderstanding and give the right mental model.]

### [Topic 2 Title]

**Host:** [Hand off from the previous topic, then ask the beginner's question.]

**Expert:** [Intuition + everyday analogy.]

**Host:** [Clarifying interruption.]

**Expert:** [Answer, then the common misunderstanding.]

### [Topic 3 Title]

<!-- Repeat this pattern until every numbered topic file has its own segment.
     Delete any unused placeholder segments. -->

**Host:** [...]

**Expert:** [...]

---

## How It All Fits Together

<!-- 4–8 turns. This is where the transcript earns its place next to the
     topic notes: the Expert says out loud how the topics lean on each other
     — what depends on what, what motivates what, where two are competing
     answers to the same question. Only use connections the topic notes
     support. The Host should try to summarise the chain and get gently
     corrected or confirmed. -->

**Host:** [Try to summarise how the pieces relate, in the listener's words.]

**Expert:** [Confirm the right parts, correct the rest, and name the real dependencies.]

**Host:** [Follow up on the one connection that is least obvious.]

**Expert:** [Explain it plainly.]

---

## Wrap-Up

<!-- 3–5 turns. The Expert names the two or three things worth remembering —
     stated as rules or ideas, not as topic titles. The Host closes by
     pointing back at the chapter's topic notes for the detail. End on the
     last spoken line; do not add a written summary afterwards, that is what
     00-intro.md is for. -->

**Host:** [Ask for the things worth remembering.]

**Expert:** [Two or three ideas, stated as rules, in plain words.]

**Host:** [Close — point listeners to the chapter's topic notes for the detail.]

---

<!-- ============================================================
     SELF-CHECK — run before saving.
     Every row needs RECORDED EVIDENCE, not a "yes." Fill in the Evidence
     column with the actual number, filename, or quoted line. A ticked row
     with no evidence written next to it COUNTS AS A FAILED ROW.
     ============================================================

     | Check                                                            | Evidence to record                                       |
     | ---------------------------------------------------------------- | -------------------------------------------------------- |
     | Phase 0 run: folder listed, every sibling note opened            | number of files listed; number of numbered topic notes    |
     | No sibling topic note is a stub                                  | "checked N notes, 0 stubs" (else you must have STOPPED)   |
     | Phase 1 done: every topic note read in full                      | number of notes read in full, and their exact filenames   |
     | Segment count equals topic count                                 | ### segment count = N; numbered topic files = N; same?    |
     | Metadata "Topics covered: N" matches                             | the two numbers                                           |
     | Phase 2 done: a hand-off line exists for every boundary          | number of boundaries; number of hand-off lines            |
     | Genuine back-and-forth — Host speaks 3+ times per segment        | Host turn count per segment, e.g. "S1:4 S2:3 S3:5"        |
     | No turn runs longer than roughly six sentences                   | number of over-long turns found; number split             |
     | At least one everyday analogy in every topic segment             | analogy count = N; segment count = N; same?               |
     | Each topic segment names a common misunderstanding               | number of segments naming one (must equal segment count)  |
     | No fact here is absent from the sibling topic notes              | number of claims traced; each one's source filename       |
     | Analogies invented, but assert nothing the notes do not say      | list the analogies used                                   |
     | Same two generic role labels throughout; no real/invented names  | the two exact label strings; hits for Guest/Interviewer/   |
     |                                                                  | Speaker 1/Narrator/Moderator (must be 0)                  |
     | No code blocks anywhere; code described in words if referenced   | count of fenced blocks in the transcript body (must be 0) |
     | Every acronym expanded and every term defined in plain words     | list the acronyms and where each is expanded out loud     |
     | Cold Open opens on the PROBLEM, not "welcome to the show"        | quote the first Host line                                 |
     | A bright 14-year-old could follow it read aloud                  | longest sentence length anywhere, in words                |
     | Length is in range                                               | word count of dialogue (target 1,500–2,500)               |
     | No TODO, TBD, STUB, or placeholder brackets remain               | searched for "TODO", "TBD", "STUB", "[" — hits found: N    |

     If any row cannot be filled with real evidence, go back and do that
     phase. Do not save the file with an empty Evidence cell.
============================================================ -->
