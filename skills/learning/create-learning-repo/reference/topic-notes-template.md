<!--
============================================================
TOPIC NOTES TEMPLATE — Adaptive Menu (not a fixed running order)
============================================================
VERSION: 4.0 (2026-08-12)

HOW TO USE THIS TEMPLATE
This file is a MENU, not a running order. You choose which sections this
topic genuinely needs, you choose the order that teaches it best, and you
may invent sections not listed here. A section that does not serve the
topic is left out entirely — no empty heading, no "not applicable" filler.

THE FOUR HARD REQUIREMENTS
These are the ONLY non-negotiables. Everything else is a suggestion. Each
one is measurable — HOW TO MEASURE below gives the exact method and the
number you must record.

  1. COVERAGE — Before you write, enumerate the topic's sub-concepts in
     the Coverage Plan comment block below. Before you submit, verify that
     every sub-concept you enumerated is actually explained in the body.
     Adaptive structure is allowed; skipping material is not. If the
     topic's subject is a CLOSED ENUMERABLE SET, coverage means EVERY
     member of that set — see PHASE 1.7.

  2. PROSE FLOOR — The explanatory body, taken as a whole, must be a
     MINIMUM of 800 words of genuine explanation. The floor applies to the
     document overall, not to any individual section. "Genuine" means each
     sentence adds a mechanism, a reason, a consequence, a constraint, a
     name, or a number. Padding, hedging, restating the title, or repeating
     an earlier sentence in new words is a VIOLATION of this requirement,
     not a way to satisfy it. RECIPE 1 says what counts and how to count.

  3. READING LEVEL + PROSE-FIRST — Write for a bright 14-year-old. Short
     sentences, one idea each. Plain everyday words in place of formal
     ones wherever possible. Every acronym is expanded, and every piece of
     jargon is defined inline in plain words, the FIRST time it appears —
     in the same sentence or the one right after. Prose paragraphs carry
     the explanation; lists must NOT substitute for explaining something,
     and are allowed only for genuine enumerations (a parameters table, a
     checklist, a list of links, a set of options being compared). Never
     write a heading like "How does it work?" or "Key concepts" — name
     every sub-heading after the actual domain concept it discusses.
     RECIPES 2 and 3 give the scans that verify this.

  4. SOURCE FIDELITY — The note must carry the exact substance a
     practitioner needs, not just a feel for the topic.
     - Every exact proper name, designation, term of art, or identifier is
       spelled as the authoritative source spells it — a statute section,
       a species name, a date, a place name, a field or parameter name. No
       paraphrased, prettified, or guessed names.
     - Every quantity, date, threshold, limit, unit, range, or closed set
       of permitted values the source states, the note states too.
     - Every artifact whose REQUIRED-IF trigger fired in PHASE 2.2 is
       actually present (diagram, table, worked example, ...).
     - An analogy may ILLUSTRATE a mechanism. An analogy may NEVER
       SUBSTITUTE for naming the real thing, stating a real number, or
       enumerating a set. "It works like a queue at a shop" does not
       replace the real name of the thing that sets the queue's size.
     RECIPE 4 gives the counts you must record. This requirement is graded
     INDEPENDENTLY of requirement 2: artifacts neither count toward the
     800-word prose floor nor against it, so adding one can never reduce
     compliance with requirement 2. If a table replaced prose the reader
     still needed, write the prose back.

WHAT SURVIVES INTO THE FINISHED FILE
Exactly three scaffolding blocks are still in the file when you hand it
in. Delete every other scaffolding block outright — do not leave a trimmed
or summarised version.

  SURVIVE (keep, filled in, still inside HTML comments):
    1. COVERAGE PLAN   2. ADAPTATION NOTE   3. FINAL SELF-AUDIT

  DO NOT SURVIVE (delete these blocks entirely before submitting):
    - this header block, including these four requirements and this
      manifest
    - HOW TO AUTHOR THIS FILE (all phases)
    - HOW TO MEASURE THE FOUR HARD REQUIREMENTS (all recipes)
    - WORKED MICRO-EXAMPLE
    - SUGGESTED SECTIONS MENU
    - VOICE AND PROSE-QUALITY ILLUSTRATIONS
    - FURTHER READING — SOURCE HYGIENE (the guidance block only; the
      Further Reading section you wrote stays)
    - VERSION HISTORY
  Also delete the placeholder `## [Your first section ...]` heading and
  every square-bracket placeholder you did not replace.

DO NOT START WRITING YET. The next comment block is a step-by-step
authoring procedure. Follow it in order. Run the Final Self-Audit at the
bottom of this file before you submit; do not submit with a failing row.
============================================================
-->

<!--
============================================================
HOW TO AUTHOR THIS FILE — FOLLOW THESE PHASES IN ORDER
============================================================
Read this block before anything else. Do the phases in order. Do not jump
straight to writing prose. Each phase ends with something written down.

--- PHASE 0 — ORIENT BEFORE WRITING ANYTHING ---
0.1 Open the stub you are filling in. Read its title and metadata line.
    Keep the title's scope; do not widen or narrow it on your own.
0.2 Read this whole template once, top to bottom, before drafting.
0.3 Open every already-authored topic note in the same parent chapter or
    module folder. Write down (a) the voice they use, and (b) which
    sub-concepts they already explain, so you do not repeat their content.
0.4 Read `AGENTS.md` in the repo root and
    `templates/authoring-guidelines.md` if they exist. Where either
    disagrees with this template, IT WINS — record that in the Adaptation
    Note.
0.5 In your working notes — NOT in the file — list the menu sections you
    suspect this topic needs and name the sources you will use. If you have
    no authoritative source for this topic, go to PHASE 6 now.

--- PHASE 1 — BUILD THE COVERAGE PLAN ---
1.1 Ask: what must a reader hold in their head to genuinely understand
    this topic? Write one line per distinct idea.
1.2 Name each item as a NOUN PHRASE describing the actual thing; vague
    buckets are not items.
      ✗ "Basics"   ✗ "Key concepts"   ✗ "How it works"
      ✓ "The two-stage sequence that produces the result"
      ✓ "The failure you get when the two stages run out of order"
1.3 Sweep these five kinds of item deliberately. Add every one that
    applies to this topic.
      | Kind | Ask yourself |
      |------|--------------|
      | Mechanism | What actually causes the outcome, step by step? |
      | Stages | What happens first, next, last? |
      | Parameters | What can be set, tuned, chosen, or sized? |
      | Failure modes | What breaks, and what does it look like? |
      | Confusable neighbours | What is this routinely mistaken for? |
1.4 Count your items and act on the count. This is guidance for
    decomposing, not a section quota.
      | Count | What it means | Do this |
      |-------|---------------|---------|
      | 0-2 | The topic is not decomposed yet | Return to 1.3 and sweep again |
      | 3 | Thin, but possible for a narrow topic | Justify each item, then proceed |
      | 4-8 | Normal shape for one topic note | Proceed |
      | 9-10 | Large — two topics may be hiding here | Proceed only if it is genuinely one topic |
      | 11+ | This is two or more topic notes | STOP — see PHASE 6 |
1.5 Write the items into the COVERAGE PLAN block below as unchecked rows.
    Leave "explained in:" blank for now — you fill it in during PHASE 4.
1.6 Write the DELIBERATELY OUT OF SCOPE lines: things a reader might
    expect to find here that belong in another note. One reason each.
1.7 ENUMERABLE-SET COMPLETENESS RATCHET. Ask one question and answer it
    in the Coverage Plan: IS THIS TOPIC'S SUBJECT A CLOSED ENUMERABLE
    SET? A closed enumerable set is a subject whose members are a finite,
    documented list.
    Recognition cues — any one of these means answer YES:
      - the subject IS one of these kinds of list: permitted values;
        status or result codes; selectable options or flags; lifecycle or
        workflow states; error categories; supported units; allowed
        roles; taxonomic ranks; legal articles, amendments, or statutory
        subsections; named historical periods, dynasties, or treaty
        signatories; musical modes or key signatures; grammatical cases
        or verb conjugations; classification tiers; official grades,
        classes, or grand cru rankings;
      - the source documents the subject AS a list, so a reader could
        count its members;
      - a reader would reasonably ask "what are all of them?".
    IF THE ANSWER IS YES, all four of these are MANDATORY:
      (a) BEFORE writing any prose, open the authoritative source and
          extract the COMPLETE member list. Not the common ones. Not the
          ones you happen to remember. All of them.
      (b) Record in the Coverage Plan: the source URL, the retrieval date
          (YYYY-MM-DD), and the SOURCE MEMBER COUNT — the number of
          members that source lists.
      (c) Render EVERY member in ONE complete table in the body, one row
          per member, with the member's exact name as the source spells
          it. A member mentioned only in passing in prose does not
          satisfy this; it must have a row.
      (d) Verify three numbers are equal: source member count == members
          listed in your Coverage Plan == rows in your table. Write all
          three into audit row 13.
    If the three numbers do not match, or you cannot confirm the member
    count from a source, STOP — see PHASE 6.
    WARNING — DO NOT WIDEN THE SET. Only what the source lists as a member
    is a member. A closely related setting, control, or neighbouring
    concept that INFLUENCES the set is NOT a member of it. Naming such a
    neighbour as a member is a factual error that teaches the reader
    something false, and it is a common one: the neighbour usually appears
    on the same page as the list, so it feels like it belongs. Check
    membership against the source's own list, not against the page it
    appears on. Genuine neighbours belong in DELIBERATELY OUT OF SCOPE or
    in a "commonly confused with" note.
    IF THE ANSWER IS NO, write "Enumerable set: no — [one line saying why
    this subject has no finite member list]" in the Coverage Plan.

--- PHASE 2 — CHOOSE SECTIONS FROM THE MENU ---
2.1 Read the SUGGESTED SECTIONS MENU below once.
2.2 BINDING REQUIRED-IF TRIGGERS. Each row is a yes/no question about
    THIS topic. These are NOT suggestions. If the condition is true, the
    artifact is REQUIRED, not recommended. You must record an explicit
    yes/no for EVERY trigger T1-T11 in the Adaptation Note — all eleven,
    including the ones you answer no.
      | ID | REQUIRED IF this is true of the topic | Then this is REQUIRED |
      |----|---------------------------------------|-----------------------|
      | T1 | It has ordered stages — a sequence, a flow, a life cycle (a process pipeline, a fermentation, a court appeal route) | a diagram |
      | T2 | It has settings a reader chooses — limits, sizes, quantities, grades (a knob, an oven temperature, a gear ratio) | a parameters table |
      | T3 | A practitioner faces a real decision with consequences | a worked example |
      | T4 | There is a competing approach the reader will meet | trade-offs / alternatives |
      | T5 | There is a concrete artifact, procedure, worked calculation, or template the reader would actually produce or follow (a step sequence, a dosage calculation, a citation format, a piece of code or configuration) | a concrete example of it |
      | T6 | Readers reliably get it wrong, or a wrong intuition is tempting | common pitfalls |
      | T7 | It is abstract or counter-intuitive and has a true everyday analogy | a plain-language opening |
      | T8 | One mechanism is much harder than the rest | a deep dive |
      | T9 | It introduces terms the reader will meet again later | key definitions |
      | T10 | It is assessed, or the reader must be able to DO something after | learning objectives and self-check questions |
      | T11 | An authoritative source exists | further reading |
    A "no" answer is only valid if it is true of the topic. Answering no
    because the artifact is effort is a failed audit row. PHASE 2.4 gives
    the rules your reason must satisfy.
2.3 For every menu section not selected above: include it only if you can
    already NAME the genuine content that would go in it. If you cannot
    name that content, do not include it.
2.4 A section you cannot fill with genuine content is OMITTED. Delete the
    heading entirely and record the omission in the ADAPTATION NOTE.
    Never keep an empty heading. Never write "not applicable", "this
    varies", or invented filler to fill it.
    EVERY omission of a trigger artifact must cite the TRIGGER ID it
    answered no to, plus a reason. A valid reason names something
    SPECIFIC ABOUT THIS TOPIC that makes the artifact impossible or
    actively misleading — not merely inconvenient or extra work.
      ✓ "T2 no — the source documents no settings for this; the only
         values are fixed by the specification and cannot be chosen."
      ✓ "T1 no — the three parts act simultaneously, so any diagram would
         imply an order that does not exist."
    BLOCKLIST — CATEGORIES of rejected justification. A rejected reason is
    a FAILING audit row, exactly as if you had left the row blank.
      ✗ IMPOSSIBILITY ASSERTED WITHOUT A SOURCE CHECK. Fails because you
        are reporting your own ignorance as a property of the subject.
        Name the source you read and what it did not contain.
      ✗ SOMETHING ELSE ALREADY CARRIES IT ("an analogy covers it",
        "integrated into the prose"). Fails because an analogy cannot
        enumerate a set or state a real quantity, and prose cannot replace
        a required artifact. If it truly exists elsewhere, name the
        sub-heading that holds it — then it is not an omission at all.
      ✗ THE ARTIFACT WOULD HAVE TO BE INVENTED. Fails whenever the source
        in fact contains a real one — a real ratio, a real ruling, a real
        measurement, a real procedure. If a reader would genuinely never
        produce such a thing, say what they do INSTEAD.
      ✗ "THIS SUBJECT HAS NOTHING SELECTABLE OR VARIABLE." Fails unless
        you demonstrate it: say which source you checked for quantities,
        thresholds, grades, or permitted values, and what it stated.
      ✗ ANY REASON ABOUT YOUR OWN CONVENIENCE — effort, time, uncertainty,
        length. Fails because the requirement is about the subject, never
        about the author.
    Any reason that would read identically in a note on a completely
    different topic is boilerplate, and boilerplate is rejected.
2.5 If this topic needs a section the menu does not list, invent it, name
    it after the thing it contains, and record it in the Adaptation Note.
2.6 Decide the running order: put first whatever makes the SECOND section
    easier to read. Write your one-line reason straight into the
    Adaptation Note now, while you still remember it.

--- PHASE 3 — DRAFT SECTION BY SECTION, CHECKING AS YOU GO ---
DO NOT draft the whole file and audit it at the end. Fixing one section
while it is in front of you is reliable; auditing a finished file is not —
you will skim it and tick boxes you did not check.

For EACH section, in order, complete 3.1 to 3.4 before starting the next.
3.1 Re-read that section's "Include: / Skip:" entry in the menu below.
3.2 Write the section.
3.3 Check that section NOW against these six tests, and fix what fails
    before moving on.
      a. The heading names a real domain concept, not a generic label.
      b. Every sentence adds a mechanism, reason, consequence, constraint,
         name, or number. Delete any sentence that adds none of these.
      c. No sentence runs longer than about 25 words.
      d. Every acronym is expanded in full and every jargon term defined in
         plain words on FIRST use anywhere in the file — same sentence or
         the very next one.
      e. The explanation sits in paragraphs, not in bullets.
      f. Every diagram, table, or other artifact has prose around it saying
         what the reader should take away from it.
3.4 Count this section's explanatory prose words (RECIPE 1) into a running
    total in your working notes, for the audit.

--- PHASE 4 — MAP THE COVERAGE PLAN TO THE BODY ---
Do this as an explicit cross-reference, item by item, not from memory.
4.1 Take Coverage Plan item 1. Search the body for the specific paragraph
    or sub-heading that explains it.
4.2 Found it → write that sub-heading name after "explained in:" and mark
    the row [x]. Marking [x] without naming a location is a failed row.
4.3 Not found → this is a GAP. Choose exactly one resolution: write the
    missing explanation now and return to 4.2, or delete the item and say
    in one line why it does not belong in this note.
4.4 Repeat for every remaining item, including the last one.
4.5 Check the other direction: a body section mapping to no Coverage Plan
    item is either off-topic — cut it — or a sub-concept you forgot to
    plan, so add it to the plan and map it.
4.6 Write "n of n mapped" into the audit Evidence column.

--- PHASE 5 — RUN THE FINAL SELF-AUDIT MECHANICALLY ---
5.1 Run all four recipes in HOW TO MEASURE THE FOUR HARD REQUIREMENTS
    below, including RECIPE 4 (SOURCE FIDELITY). Write the numbers down.
5.2 For each row of the FINAL SELF-AUDIT table: perform the check, write
    the measured value or specific evidence into the Evidence column, then
    mark Pass. A row you cannot fill with real evidence is a FAILING row —
    fix the note, then re-run that row.
5.3 Search the finished file for TODO, TBD, STUB, FIXME, and any leftover
    square-bracket placeholder, and remove every hit outside authoring
    guidance.
5.4 Do not submit with a failing row.

--- PHASE 6 — STOP CONDITIONS ---
Stopping to ask a human is CORRECT, EXPECTED behaviour. Inventing content
so you can finish is a FAILURE of the task. A note that is honestly
incomplete is more useful than one that is confidently wrong.

STOP and ask when any of these is true:
  | Situation | Why you must not guess |
  |-----------|------------------------|
  | A Coverage Plan item is not supported by any source you have | Anything you write for it would be fabricated |
  | The topic is really two or more topics (PHASE 1, 11+ items) | Splitting is a scope decision, not yours to make silently |
  | You cannot reach the 800-word floor with genuine explanation | The only ways to close the gap are padding or invention, and both are violations |
  | A required fact — a name, quantity, date, limit, or edition — is in no available source | A plausible-sounding number is still a made-up number |
  | The subject is a closed enumerable set (PHASE 1.7) and no source lets you confirm the member count | A partial list read as complete teaches the reader that the missing members do not exist |
  | The enumerable-set counts disagree: source count, plan count, and table rows are not all equal | One of the three is wrong, and guessing which is how members go missing |
  | The stub's title contradicts the parent chapter or `AGENTS.md` | The scope conflict must be resolved by the human |

HOW TO STOP: do not submit a filled-in file. Say plainly (a) which item or
fact is missing, (b) which sources you checked, and (c) what you need in
order to continue. Then wait. Do not fill the gap with an invention.
============================================================
-->

<!--
============================================================
HOW TO MEASURE THE FOUR HARD REQUIREMENTS
============================================================
The four hard requirements are measurable. Measure them; do not judge them
by feel. Each recipe produces a number for the Final Self-Audit's Evidence
column.

--- RECIPE 1 — THE 800-WORD PROSE FLOOR ---
COUNTS: words inside explanatory prose paragraphs anywhere in the body;
prose captions under a diagram or table; prose inside a <details> answer
that explains WHY an answer is right.
DOES NOT COUNT: the `# Title`, every heading and sub-heading, the metadata
line, anything inside an HTML comment (including this template and the
Coverage Plan), fenced code blocks and diagrams, every table cell,
bulleted and numbered list items, the Further Reading list, the Adaptation
Note, and the Final Self-Audit table.
WHY THAT IS NOT A REASON TO SKIP ARTIFACTS: artifacts are excluded because
this recipe measures PROSE only; they are measured separately by RECIPE 4
against requirement 4. Never drop a required artifact to protect this
number, and never treat a table as progress toward it.

HOW TO COUNT — do this, do not estimate:
  M1. List your explanatory paragraphs in order: P1, P2, P3, ...
  M2. Count the words in each one. Write them down: "P1 = 74", "P2 = 118".
  M3. Add them up. That sum is your prose-floor number.
  M4. Sum is 800 or more → go to M5. Under 800 → you are NOT finished and
      you must NOT pad. Return to the Coverage Plan: usually a sub-concept
      got one line where it needed a paragraph, a mechanism was asserted
      without its cause, or a consequence was named without saying who it
      hurts and when. Explain more; do not restate.
  M5. Write the actual sum into the Evidence column of audit row 2.
  Writing a number you did not compute is a failed row.

--- RECIPE 2 — READING LEVEL FOR A BRIGHT 14-YEAR-OLD ---
Three mechanical scans. Run all three. Each produces counts.
  S1. LONG-SENTENCE SCAN. Read the body one sentence at a time and count
      the words in any that looks long. Over about 25 words → split it in
      two, one idea each. Record how many you split.
  S2. ACRONYM SCAN. Find every token of two or more capital letters in a
      row. Check its FIRST occurrence in the file writes it out in full,
      with a plain-words gloss if the full form is still opaque. Record how
      many acronyms you found and how many you fixed.
  S3. JARGON SCAN. Mark every term a 14-year-old would not know. Check that
      sentence and the next for a plain-words definition, and add one where
      it is missing. Record how many you marked and how many you fixed.
Write these counts into the Evidence column of audit rows 3, 4, and 5.

--- RECIPE 3 — THE PROSE-FIRST RATIO ---
  R1. Count the explanatory prose paragraphs in the body. Call it P.
  R2. Count the bulleted or numbered lists inside the explanation. Call it
      L. Do NOT count as L: the Further Reading list, a parameters table,
      a definitions table, a checklist, a list of options being compared,
      or the self-check questions.
  R3. Apply the rule:
      | Result | Verdict |
      |--------|---------|
      | L = 0 | Pass |
      | P is at least 3 x L | Pass — prose is carrying the explanation |
      | P is less than 3 x L | FAIL — the explanation is living in bullets |
      | Any list whose items ARE the explanation of a mechanism | FAIL, whatever the ratio |
  R4. To fix a FAIL: rewrite one offending list as a paragraph stating each
      point AND why it is true. Then recount.
  R5. Write "P = n, L = n" into the Evidence column of audit row 6.

--- RECIPE 4 — SOURCE FIDELITY ---
Four counts. All four go into the Evidence column, as numbers.
  F1. NAME COUNT. List every exact proper name, designation, term of art,
      or identifier you used — a statute section, a species name, a date, a
      place name, a field or parameter name — written the way the source
      writes it. Call the total I. Then check each one character by
      character against the source. Record "I = n, mismatches fixed = n".
      If I = 0 for a topic whose source names things, the note is
      describing the topic from the outside; go back and name them.
  F2. STATED-VALUES COUNT. List every quantity, date, threshold, limit,
      unit, range, and closed set of permitted values the source states
      for this topic. Call it N. Then count how many of those N appear in
      the note. Record "N = n stated by source, n present in note".
      Anything present but not in a source is an invention — delete it.
  F3. TRIGGER DELIVERY COUNT. From the Adaptation Note, count the
      triggers answered yes. Call it Y. Count how many of those Y
      artifacts are actually in the body. Record "triggers fired = n,
      delivered = n". These two numbers MUST be equal. If they are not,
      either write the missing artifact or change the answer to no with a
      reason that survives the PHASE 2.4 blocklist.
  F4. TRACEABILITY. Confirm every name from F1 and every value from F2
      traces to a source you actually retrieved. Record how many you could
      not trace, and drop each one. That count must be 0.
  Write F1-F4 into the Evidence column of audit rows 8 and 14.
============================================================
-->

# [Topic Title]

**Section:** [Section] | **Module:** [Module] | **Est. time:** [X hrs] | **Exam mapping:** [Domain/objective or "Supporting content"]

---

<!--
============================================================
COVERAGE PLAN — AUTHOR FILLS THIS IN BEFORE WRITING THE BODY
============================================================
This block is authoring scaffolding. It stays inside an HTML comment so
the learner never sees it, but it remains in the finished file so the
quality gate can read it back.

STEP 1 (before writing): List every sub-concept a reader must understand
to genuinely know this topic. Follow PHASE 1 above — it says how to
enumerate them and what to do about the count. Name the actual mechanisms,
stages, parameters, failure modes, and neighbouring concepts, not vague
buckets. Do not trim the list to make the writing easier.

STEP 2 (after writing): Follow PHASE 4 above. Mark each one [x] and name
where in the body it is explained. A row marked [x] with no location named
is a failed audit row.

SUB-CONCEPTS TO COVER:
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [add as many rows as the topic actually needs]

ENUMERABLE SET (from PHASE 1.7 — answer this, do not delete it):
- Is this topic's subject a closed enumerable set? [yes / no]
- If NO: [one line saying why this subject has no finite member list]
- If YES, all four lines are required:
  - Source: [url] — retrieved [YYYY-MM-DD]
  - SOURCE MEMBER COUNT: [n]
  - Members, exactly as the source names them: [name, name, name, ...]
  - Counts match: source [n] == plan [n] == table rows [n]

DELIBERATELY OUT OF SCOPE (and why, one line each):
- [Adjacent concept the reader might expect] — [why it belongs elsewhere]
============================================================
-->

<!--
============================================================
WORKED MICRO-EXAMPLE — COVERAGE PLAN MAPPED TO THE BODY
============================================================
ILLUSTRATION ONLY, FROM AN UNRELATED EVERYDAY DOMAIN. The topic below is
"how a bicycle rim brake works". It has NOTHING to do with the subject of
this repo. Copy the SHAPE of the mapping, never the content.

Filled-in Coverage Plan (5 items — normal shape):
- [x] The lever-and-cable path from hand to wheel — explained in: From Your Hand To The Wheel Rim
- [x] Friction between pad and rim as what removes speed — explained in: Why Rubber On Metal Slows You Down
- [x] Pad clearance, and how it changes lever travel — explained in: Setting The Gap Between Pad And Rim
- [x] Brake fade when the rim gets hot or wet — explained in: When Braking Stops Working
- [x] Rim brakes versus disc brakes, routinely confused — explained in: Why Discs Replaced Rims On Wet-Weather Bikes

DELIBERATELY OUT OF SCOPE:
- Wheel truing — it is a wheel-maintenance topic, not a braking mechanism.

ENUMERABLE SET: no — "how a rim brake works" is a mechanism, not a finite
documented list of members. (A note titled "Brake Pad Compound Types"
WOULD be an enumerable set, and would need every compound in one table.)

Why each section was chosen (PHASE 2.2 triggers in action):
  | Coverage item | Section | Trigger that required it |
  |---------------|---------|--------------------------|
  | Lever-and-cable path | From Your Hand To The Wheel Rim | T1 yes — ordered stages → diagram |
  | Pad-and-rim friction | Why Rubber On Metal Slows You Down | core mechanism → main explanation |
  | Pad clearance | Setting The Gap Between Pad And Rim | T2 yes — a setting a reader chooses → parameters table |
  | Brake fade | When Braking Stops Working | T6 yes — a known failure mode → pitfalls |
  | Rim versus disc | Why Discs Replaced Rims On Wet-Weather Bikes | T4 yes — competing approach → trade-offs |

What to copy from it: every item is a noun phrase naming a real thing
pointing at ONE named sub-heading; every sub-heading is named after the
concept, never "Overview"; sections came from the PHASE 2.2 triggers, not
habit; no section exists without a coverage item behind it. Its Adaptation
Note logs "T5 yes — the pad-alignment procedure is the concrete thing a
reader follows; the numbered steps and the hex-key sizes are in Setting The
Gap Between Pad And Rim." That names something specific and true about THIS
topic, which is why it passes where a blocklisted "it would have to be
invented" would not.
============================================================
-->

<!--
============================================================
SUGGESTED SECTIONS MENU — PICK, ORDER, AND RENAME FREELY
============================================================
Each entry says when it earns its place and when to skip it. Include the
ones that teach THIS topic, in whatever order makes it easiest to follow —
for some topics an analogy comes first, for others a diagram or a worked
example is the best possible opening. Where a PHASE 2.2 trigger fired, the
matching entry is not optional.

TL;DR
  Include: almost always — a few sentences saying what this is, why it
  matters, and the one thing to remember.
  Skip: if the topic is so short the summary would repeat the body.

PLAIN-LANGUAGE OPENING (ELI5-style)
  Include: when the concept is abstract or counter-intuitive and has a
  good everyday analogy. Map the analogy onto the real mechanism piece by
  piece, then say where the analogy stops being true.
  Skip: when the topic is already concrete and mechanical, so an analogy
  would add a layer of indirection instead of removing one.

LEARNING OBJECTIVES
  Include: when the topic is assessed, or the reader benefits from knowing
  what they should be able to DO afterwards. Use action verbs (implement,
  diagnose, compare, configure, trace, justify).
  Skip: for short supporting or background topics.

VISUAL OVERVIEW / DIAGRAMS
  Include: when a shape is worth seeing — a flow, pipeline, architecture,
  or decision branch; a genealogy or succession chart; a timeline; a
  cross-section; a cycle; a classification tree; a before/after state. Put
  each diagram in a plain fenced code block using box-drawing characters,
  give it a domain-specific title, and caption what the reader should LEARN
  from it, not what it depicts.
  Skip: when the topic is purely definitional and a diagram would just be
  boxes containing the same words as the prose.

MAIN EXPLANATION (with domain-named sub-headings)
  Include: always — this is the note. Break it into as many
  `### [Domain Concept]` sub-headings as the topic genuinely has, each
  named after the real thing discussed. Write paragraphs.
  Skip: never.

DEEP DIVE
  Include: when one mechanism is much harder or more consequential than
  the rest and deserves slow treatment on its own.
  Skip: when the topic has no single hard centre, or the depth already
  lives naturally inside the main explanation.

TRADE-OFFS / ALTERNATIVE APPROACHES
  Include: when a practitioner has a real choice, or a competing approach
  the reader will meet. Say what each option costs and what it buys.
  Skip: when there is genuinely only one way to do the thing.

WHERE IT APPEARS IN THE REAL WORLD
  Include: when naming concrete instances makes the concept findable — a
  named place, institution, or documented case; a published edition or
  ruling; a tool, product, service, command, or entry point. Specific
  enough that the reader could go and look at the real thing.
  Skip: for a pure fundamental with no concrete surface, or when the
  specifics would date the note badly.

KEY PARAMETERS TABLE
  Include: when the topic has settings, quantities, thresholds, grades, or
  proportions a reader chooses (in software, knobs). Give each one a
  concrete decision rule with a number, threshold, or explicit condition —
  not "depends on your use case".
  Skip: when the source states nothing selectable. Leave the section out
  entirely rather than writing an empty table.

WORKED EXAMPLE
  Include: when following one realistic scenario end to end teaches more
  than describing the steps abstractly. A second example earns its place
  only if it is genuinely different — a different constraint, conclusion,
  or a diagnosis of something going wrong.
  Skip: when the topic is definitional, or the example would just
  re-narrate the explanation.

CONCRETE EXAMPLE OF THE ARTIFACT (the thing a reader produces or follows)
  Include: when there is a concrete artifact, procedure, worked
  calculation, checklist, or template the reader would actually produce or
  follow — a numbered step sequence, a dosage or ratio calculation, a
  citation format, a filled-in form, a piece of code or configuration.
  Introduce each one by naming the real problem it solves. An anti-pattern
  paired with its corrected version is often the most useful example you
  can write. If the artifact IS code or configuration, it must also be
  syntactically valid.
  Skip: when the reader never produces or follows anything concrete here,
  and the artifact would be invented for the sake of having one.

COMMON PITFALLS & MISCONCEPTIONS
  Include: when readers reliably get this wrong. For each, say why the
  wrong intuition is tempting, then state the correct mental model as a
  rule. One of the few places a list is appropriate — but each entry still
  needs real explanation, not a label.
  Skip: when the topic has no established failure modes yet.

KEY DEFINITIONS
  Include: when the topic introduces terms the reader will meet again.
  Define them as they are used HERE, not as a dictionary would. Terms must
  ALSO be defined inline on first use in the prose; this is a lookup
  table, not a substitute for that.
  Skip: when everything was already defined plainly in the body.

SUMMARY / QUICK RECALL
  Include: when the reader will want a fast scan before a test or meeting.
  Each line states a fact or rule, not a topic label.
  Skip: for very short notes where the TL;DR already does this job.

SELF-CHECK QUESTIONS
  Include: when the topic is assessed or has decisions worth rehearsing.
  Mix recall with questions that ask the reader to apply or compare. Put
  answers in a <details> block and explain WHY the right answer is right
  and why the most tempting wrong answer fails.
  Skip: for background notes that carry no decisions.

FURTHER READING
  Include: whenever authoritative sources exist. Official documentation
  only — no third-party blogs, aggregators, or video.
  Skip: only if no official source exists, which is rare.

INVENT YOUR OWN
  If this topic needs a section not on this list — a history of how the
  approach evolved, a glossary of confusingly-similar names, a
  troubleshooting flow, a comparison against a predecessor — write it, and
  name it after the thing it actually contains.
============================================================
-->

<!--
============================================================
VOICE AND PROSE-QUALITY ILLUSTRATIONS
============================================================
These five pairs are drawn on purpose from ordinary everyday domains —
baking, gardening, the body, public transport, weather — so they can never
be mistaken for this note's subject. They show TONE and PROSE QUALITY only.

--- Reading level (baking) ---
✗ "Dough structure degrades proportionally with hydration in excess of
   flour saturation, necessitating mechanical remediation."
✓ "Add too much water to dough and it turns sloppy, so it spreads instead
   of rising. Bakers call the water-to-flour ratio the hydration."
   (Short sentences, one idea each. The jargon word is defined the moment
   it appears, not in a glossary at the end.)

--- Acronyms expanded on first use (gardening) ---
✗ "Feed the beds with a balanced NPK in early spring."
✓ "Feed the beds with a balanced NPK feed — nitrogen, phosphorus and
   potassium, the three nutrients plants use most, named by their letters
   on the periodic table."

--- Prose carries the explanation, not bullets (the body) ---
✗ "Why a warm-up helps: - fewer injuries  - better performance  - feels
   easier"
✓ "A warm-up raises the temperature inside your muscles, and warm muscle
   stretches further before it tears, so pulls become less likely. The
   gentle effort also widens the blood vessels feeding the working limbs,
   so oxygen arrives faster and the first hard minute stops feeling like a
   wall."
   (Same three points, but now the reader learns the mechanism behind each
   one instead of reading a label for it.)

--- Sub-headings named after the domain concept (public transport) ---
✗ ### How does it work?   ✗ ### Key Concepts   ✗ ### Considerations
✓ ### Why One Late Train Delays The Three Behind It
   (A reader scanning the headings alone should learn the topic's shape.)

--- Explanation vs restatement (weather) — the prose floor is the ✓ column ---
✗ "Frost warnings matter because frost is important for crops, and crops
   that matter get frost warnings."  (says nothing new)
✓ "On a clear, still night the ground radiates its heat straight out to
   the sky, with no cloud to hold any of it in. The air just above the
   soil can then fall below freezing even after a mild afternoon. Water
   inside the plant's cells freezes, expands, and splits the cell walls,
   which is why the leaves look scorched by morning."
============================================================
-->

## [Your first section — chosen from the menu, named for this topic]

<!-- Write the note here, in the order and shape this topic needs.
     Use `##` for top-level sections and `###` for sub-headings inside
     the main explanation. Name every heading after a real domain concept.
     Delete this placeholder heading once you have real sections. -->

<!--
============================================================
FURTHER READING — SOURCE HYGIENE
============================================================
Official vendor/standards/project documentation only. No third-party
blogs, Medium, YouTube, forum posts, or AI-generated summaries.

Verify every URL live before you write it down. If a fetch fails or
redirects somewhere unexpected, do not include the link.

Required format, one per line:
  - [Title](url) — *verified YYYY-MM-DD* — [one-line description]

Never invent a URL, a document title, or a verification date.
============================================================
-->

<!--
============================================================
ADAPTATION NOTE — AUTHOR FILLS THIS IN
============================================================
This replaces the fixed section counts that earlier versions of this
template enforced. It is the accountability record for an adaptive
structure: you may omit anything, but you must say what you omitted and
why. A reason like "not needed" is not acceptable — say what about THIS
topic made the section unhelpful. Reasons are checked against the PHASE
2.4 BLOCKLIST; a blocklisted or boilerplate reason is a FAILING row.

TRIGGER ANSWERS (PHASE 2.2 — all eleven, none skipped):
- T1 diagram: [yes → in section X / no → reason]
- T2 parameters table: [yes → in section X / no → reason]
- T3 worked example: [yes → in section X / no → reason]
- T4 trade-offs: [yes → in section X / no → reason]
- T5 concrete example of the artifact: [yes → in section X / no → reason]
- T6 common pitfalls: [yes → in section X / no → reason]
- T7 plain-language opening: [yes → in section X / no → reason]
- T8 deep dive: [yes → in section X / no → reason]
- T9 key definitions: [yes → in section X / no → reason]
- T10 objectives + self-check: [yes → in section X / no → reason]
- T11 further reading: [yes → in section X / no → reason]

SECTIONS OMITTED FROM THE MENU (cite the trigger ID where one applies):
- [Section name] — [T-number answered no] — [one-line reason specific to this topic]
- [Section name] — [T-number answered no] — [one-line reason specific to this topic]

SECTIONS INVENTED FOR THIS TOPIC (if any):
- [Section name] — [what it does that no menu section covered]

ORDER CHOSEN, AND WHY:
- [One or two lines on why this running order teaches the topic best]

LOCAL RULES THAT OVERRODE THIS TEMPLATE (from PHASE 0.4, if any):
- [Rule from AGENTS.md or authoring-guidelines.md] — [what you did differently]
============================================================
-->

<!--
============================================================
FINAL SELF-AUDIT — RUN BEFORE SUBMITTING
============================================================
Outcome-based, not count-based. Answer honestly. If any row is No, fix
the note before submitting it. Do not submit with a failing row.

EVERY ROW NEEDS EVIDENCE. Fill the Evidence column with the actual
measured value or the specific thing you found — a number, a name, a
location. "Yes", "done", "OK", and "verified" are NOT evidence.
A row with a tick and no evidence is treated as a FAILED ROW.
Get the numbers from HOW TO MEASURE THE FOUR HARD REQUIREMENTS above.
Rows 8, 13, and 14 are TWO-SIDED: they fail both when something present
is wrong AND when something required is missing. "There are none" is not
a pass for them; it is only a pass if no trigger required one.

| # | Check | Evidence — record the measured value or specific finding | Pass? |
|---|-------|--------------------------------------------------------|-------|
| 1 | Every sub-concept listed in the Coverage Plan is genuinely explained in the body | Items mapped: [n] of [n]. Gaps resolved by writing: [n]; by removal with reason: [n] | |
| 2 | The explanatory body reaches the 800-word floor with real explanation — no padding, hedging, or restatement | Prose word count (RECIPE 1, summed per paragraph): [number] | |
| 3 | A bright 14-year-old could follow it: short sentences, plain words, one idea at a time | Sentences over ~25 words found: [n]; split: [n]; remaining: [n] | |
| 4 | Every acronym is expanded the first time it appears | Acronyms found: [n]; already expanded: [n]; fixed: [n] | |
| 5 | Every piece of jargon is defined inline, in plain words, the first time it appears | Jargon terms marked: [n]; definitions added: [n] | |
| 6 | The explanation is carried by prose paragraphs; lists appear only for genuine enumerations | P = [n] paragraphs, L = [n] explanation lists; verdict: [pass/fail from RECIPE 3] | |
| 7 | Every sub-heading is named after a real domain concept — no generic headings | Headings checked: [n]; generic headings renamed: [n] | |
| 8 | TWO-SIDED. Every artifact PRESENT earns its place and is explained in the surrounding prose, AND every artifact REQUIRED by a fired trigger is present. Zero artifacts passes only if zero triggers fired | Present — diagrams: [n], tables: [n], concrete examples/artifacts: [n]; each explained in prose: [n of n]. Required (RECIPE 4 F3) — triggers fired: [n], delivered: [n] (must be equal) | |
| 9 | Every omission cites its trigger ID and gives a reason that is specific to THIS topic and survives the PHASE 2.4 blocklist | Omissions: [n]; each citing a T-number: [n of n]; reasons checked against blocklist: [n]; blocklisted reasons rewritten: [n]; sections invented: [n] | |
| 10 | No TODO, TBD, STUB, placeholder text, or leftover square-bracket template markers remain | Searched for TODO/TBD/STUB/FIXME/`[`; hits outside comments: [n] | |
| 11 | Every external link is official documentation, fetched live, with a *verified YYYY-MM-DD* date | Links: [n]; fetched live: [n]; non-official rejected: [n] | |
| 12 | Nothing is invented — no made-up product names, parameters, figures, quotes, or URLs | Every name/number/limit traced to a source: [yes/no]; facts dropped for lack of a source: [n] | |
| 13 | TWO-SIDED. Enumerable-set ratchet (PHASE 1.7): if the subject is a closed enumerable set, every member has a row in one complete table and the three counts are equal | Enumerable set: [yes/no]. If yes — source [n] == plan [n] == table rows [n]; source URL + retrieval date recorded: [yes/no]. If no — "N/A, not an enumerable set" plus: [why this subject has no finite member list] | |
| 14 | TWO-SIDED. SOURCE FIDELITY (requirement 4): every exact proper name, designation, or term of art spelled as the source spells it, plus every quantity, date, threshold, limit, unit, and closed set of permitted values the source states; no analogy standing in for a real name, a real number, or a set. Every subject has names and dates, so this row is never "N/A" | RECIPE 4 — I = [n] names/designations checked character by character, mismatches fixed: [n]; N = [n] source-stated quantities/dates/limits/units/permitted values, present in note: [n]; untraceable facts dropped: [n] (must be 0) | |
| 15 | Every trigger T1-T11 has an explicit yes/no answer recorded in the Adaptation Note, and every "yes" names the section that satisfies it | Triggers answered: [n] of 11; answered yes: [n], each naming a section: [n of n]; answered no: [n], each with a non-blocklisted reason: [n of n] | |
============================================================
-->

<!--
============================================================
VERSION HISTORY — TEMPLATE SCAFFOLDING, DELETE WITH THE REST
============================================================
- v1.0 (2024): Baseline section structure and minimum lengths.
- v2.0 (2026-08-10): Rigid enforcement pass — per-section word counts and a 44-row fixed-count Completeness Self-Audit.
- v3.0 (2026-08-11): Adaptive rewrite — Suggested Sections Menu replaced the fixed order, all fixed counts removed, Coverage Plan + 800-word prose floor + reading-level requirements and the Adaptation Note added.
- v3.1 (2026-08-11): Procedure pass — phased authoring block, HOW TO MEASURE recipes, worked micro-example, Evidence column on every audit row, stop conditions. No requirement changed.
- v4.0 (2026-08-12): Fidelity + genericity pass.
  - Added a FOURTH hard requirement, SOURCE FIDELITY: exact proper names,
    designations and terms of art as the source spells them, plus every
    quantity, date, threshold, limit, unit and closed set of permitted
    values it states, plus the artifacts the triggers fired for. An
    analogy may never substitute for a real name, number, or set. Graded
    independently of the prose floor; RECIPE 1 unchanged.
  - Added the closed-enumerable-set ratchet (PHASE 1.7), binding
    REQUIRED-IF triggers T1-T11, RECIPE 4, a two-sided artifact audit row,
    the omission BLOCKLIST, and the survival manifest; moved this history
    inside a comment.
  - GENERICITY: the template now reads as domain-neutral for history,
    craft, law, science, and music as well as software. T5 and the menu's
    artifact entry cover procedures, calculations, and templates, not only
    code; parameters, diagram kinds, and real-world instances are phrased
    domain-first; the voice illustrations use everyday domains; audit row
    14 is SOURCE FIDELITY and is answerable for any subject.
============================================================
-->
