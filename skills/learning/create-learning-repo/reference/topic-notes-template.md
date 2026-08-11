<!--
============================================================
TOPIC NOTES TEMPLATE — Adaptive Menu (not a fixed running order)
============================================================
VERSION: 3.1 (2026-08-11)

HOW TO USE THIS TEMPLATE
This file is a MENU, not a running order. Nothing below is a required
section. You choose which sections this specific topic genuinely needs,
you choose the order that teaches it best, and you may invent sections
that are not listed here if the topic calls for them. A section that
does not serve the topic should simply be left out — do not keep an empty
heading and do not write "not applicable" filler.

THE THREE HARD REQUIREMENTS
These are the ONLY non-negotiables in this template. Everything else is
a suggestion. Each one is measurable — HOW TO MEASURE below gives the
exact method and the number you must record.

  1. COVERAGE — Before you write, enumerate the topic's sub-concepts in
     the Coverage Plan comment block below. Before you submit, verify that
     every sub-concept you enumerated is actually explained in the body.
     Adaptive structure is allowed; skipping material is not.

  2. PROSE FLOOR — The explanatory body of the note, taken as a whole,
     must be a MINIMUM of 800 words of genuine explanation. This floor
     applies to the document overall, not to any individual section.
     "Genuine" means each sentence adds a mechanism, a reason, a
     consequence, a constraint, a name, or a number. Padding, hedging,
     restating the title, or repeating an earlier sentence in new words
     is a VIOLATION of this requirement, not a way to satisfy it.
     RECIPE 1 lists exactly what counts and how to count it.

  3. READING LEVEL + PROSE-FIRST — Write for a bright 14-year-old.
     - Short sentences. One idea per sentence.
     - Plain everyday words in place of formal ones wherever possible.
     - Every acronym is expanded the FIRST time it appears.
     - Every piece of jargon is defined inline, in plain words, the FIRST
       time it appears — in the same sentence or the one right after.
     - Prose paragraphs carry the explanation. Bulleted and numbered lists
       must NOT be used as a substitute for explaining something. Lists
       are allowed only for genuine enumerations: a parameter table, a
       checklist, a list of links, a set of options being compared.
     - Never write a heading like "How does it work?" or "Key concepts".
       Name every sub-heading after the actual domain concept it discusses.
     RECIPES 2 and 3 give the scans that verify this.

DO NOT START WRITING YET. The next comment block is a step-by-step
authoring procedure. Read it and follow it in order. Run the Final
Self-Audit at the bottom of this file before you submit; do not submit
with a failing row.
============================================================
-->

<!--
============================================================
HOW TO AUTHOR THIS FILE — FOLLOW THESE PHASES IN ORDER
============================================================
Read this block before anything else. Do the phases in order. Do not jump
straight to writing prose. Each phase ends with something written down.

--- PHASE 0 — ORIENT BEFORE WRITING ANYTHING ---
0.1 Open the stub file you are filling in. Read its title, its metadata
    line, and anything already in it. Keep the title's scope; do not
    widen or narrow it on your own.
0.2 Read this whole template once, top to bottom, before drafting.
0.3 List the other topic notes in the same parent chapter or module
    folder. Open every one that is already authored. Write down (a) the
    voice they use, and (b) which sub-concepts they already explain, so
    you do not repeat their content.
0.4 Look for `AGENTS.md` in the repo root and for
    `templates/authoring-guidelines.md`. If either exists, read it. Where
    it disagrees with this template, IT WINS. Record that in the
    Adaptation Note.
0.5 In your working notes — NOT in the file — write out the list of
    sections available to you from the SUGGESTED SECTIONS MENU below,
    plus any section you already suspect this topic needs.
0.6 Name the sources you will use. If you have no authoritative source
    for this topic, go to PHASE 6 now.

--- PHASE 1 — BUILD THE COVERAGE PLAN ---
1.1 Ask: what must a reader hold in their head to genuinely understand
    this topic? Write one line per distinct idea.
1.2 Name each item as a NOUN PHRASE describing the actual thing. Vague
    buckets are not items.
      ✗ "Basics"   ✗ "Key concepts"   ✗ "How it works"   ✗ "Advanced use"
      ✓ "The two-stage sequence that produces the result"
      ✓ "The setting that controls how long an entry survives"
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
1.4 Count your items and act on the count.
      | Count | What it means | Do this |
      |-------|---------------|---------|
      | 0-2 | The topic is not decomposed yet | Return to 1.3 and sweep again |
      | 3 | Thin, but possible for a narrow topic | Justify each item, then proceed |
      | 4-8 | Normal shape for one topic note | Proceed |
      | 9-10 | Large — check whether two topics are hiding here | Proceed only if it is genuinely one topic |
      | 11+ | This is two or more topic notes | STOP — see PHASE 6 |
    This range is guidance for decomposing, not a section quota.
1.5 Write the items into the COVERAGE PLAN block below as unchecked rows.
    Leave "explained in:" blank for now — you fill it in during PHASE 4.
1.6 Write the DELIBERATELY OUT OF SCOPE lines: things a reader might
    expect to find here that belong in another note. One reason each.

--- PHASE 2 — CHOOSE SECTIONS FROM THE MENU ---
2.1 Read the SUGGESTED SECTIONS MENU below once.
2.2 Apply these rules. Each left-hand cell is a yes/no question about
    THIS topic. Answer it, then act.
      | If this is true of the topic | Then include |
      |------------------------------|--------------|
      | It has a process, flow, pipeline, or ordered stages | a diagram |
      | It has settings, knobs, limits, or sizes a reader chooses | a parameters table |
      | A practitioner faces a real decision with consequences | a worked example |
      | There is a competing approach the reader will meet | trade-offs / alternatives |
      | There is code or configuration a reader would actually write | an implementation snippet |
      | Readers reliably get it wrong, or a wrong intuition is tempting | common pitfalls |
      | It is abstract or counter-intuitive and has a true everyday analogy | a plain-language opening |
      | One mechanism is much harder than the rest | a deep dive |
      | It introduces terms the reader will meet again later | key definitions |
      | It is assessed, or the reader must be able to DO something after | learning objectives and self-check questions |
      | An authoritative source exists | further reading |
2.3 For every menu section not selected above: include it only if you can
    already NAME the genuine content that would go in it. If you cannot
    name that content, do not include it.
2.4 A section you cannot fill with genuine content is OMITTED. Delete the
    heading entirely and record the omission in the ADAPTATION NOTE with
    a reason specific to this topic. Never keep an empty heading. Never
    write "not applicable", "this varies", or invented filler to fill it.
2.5 If this topic needs a section the menu does not list, invent it, name
    it after the thing it contains, and record it in the Adaptation Note.
2.6 Decide the running order: put first whatever makes the SECOND section
    easier to read. Write your one-line reason straight into the
    Adaptation Note now, while you still remember it.

--- PHASE 3 — DRAFT SECTION BY SECTION, CHECKING AS YOU GO ---
DO NOT draft the whole file and audit it at the end. Fixing one section
while it is in front of you is reliable. Auditing a finished 900-word
file is not — you will skim it and tick boxes you did not check.

For EACH section, in order, complete 3.1 to 3.4 before starting the next.
3.1 Re-read that section's "Include: / Skip:" entry in the menu below.
3.2 Write the section.
3.3 Check that section NOW, against these seven tests. Fix what fails
    before moving on.
      a. The heading is named after a real domain concept, not a generic
         label like "Overview" or "How does it work?".
      b. Every sentence adds a mechanism, a reason, a consequence, a
         constraint, a name, or a number. Delete any sentence that does
         not. Restating the heading is not a sentence that adds anything.
      c. No sentence runs longer than about 25 words. Split the ones that
         do, one idea per sentence.
      d. Every acronym used here is expanded in full the FIRST time it
         appears anywhere in the file.
      e. Every jargon term used here is defined in plain words, in the
         same sentence or the very next one, on first use.
      f. The explanation sits in paragraphs, not in bullets.
      g. If this section contains a diagram, table, or snippet, the prose
         around it says what the reader should take away from it.
3.4 Count the words of explanatory prose in this section (see HOW TO
    MEASURE, RECIPE 1). Add it to a running total in your working notes.
    You will need that total for the audit.

--- PHASE 4 — MAP THE COVERAGE PLAN TO THE BODY ---
Do this as an explicit cross-reference, item by item. Do not do it from
memory.
4.1 Take Coverage Plan item 1. Search the body for the specific paragraph
    or sub-heading that explains it.
4.2 Found it → write that sub-heading name after "explained in:" and mark
    the row [x].
4.3 Not found → this is a GAP. Choose exactly one resolution:
      a. Write the missing explanation now, then go back to 4.2; or
      b. Delete the item from the Coverage Plan and write one line saying
         why it does not belong in this note.
    Marking a row [x] without naming a location is a failed audit row.
4.4 Repeat 4.1 to 4.3 for every remaining item, including the last one.
4.5 Now check in the other direction. Any body section that maps to no
    Coverage Plan item is either off-topic — cut it — or a sub-concept
    you forgot to plan, in which case add it to the plan and map it.
4.6 Write the number of items mapped into the audit table Evidence
    column, in the form "n of n mapped".

--- PHASE 5 — RUN THE FINAL SELF-AUDIT MECHANICALLY ---
5.1 Go to HOW TO MEASURE THE THREE HARD REQUIREMENTS below. Run all three
    recipes. They each produce a number. Write the numbers down.
5.2 Go to the FINAL SELF-AUDIT table at the bottom of this file.
5.3 For each row: perform the check, then write the measured value or the
    specific evidence into the Evidence column, then mark Pass.
5.4 A row you cannot fill with real evidence is a FAILING row. Fix the
    note, then re-run that row.
5.5 Search the finished file for these strings and remove every hit that
    is not inside authoring guidance: TODO, TBD, STUB, FIXME, and any
    remaining square-bracket placeholder from this template.
5.6 Do not submit with a failing row.

--- PHASE 6 — STOP CONDITIONS ---
Stopping and asking a human is CORRECT, EXPECTED behaviour. Inventing
content so you can finish is a FAILURE of the task, not a rescue of it.
A note that is honestly incomplete is more useful than one that is
confidently wrong.

STOP and ask when any of these is true:
  | Situation | Why you must not guess |
  |-----------|------------------------|
  | A Coverage Plan item is not supported by any source you have | Anything you write for it would be fabricated |
  | The topic is really two or more topics (PHASE 1, 11+ items) | Splitting is a scope decision, not yours to make silently |
  | You cannot reach the 800-word floor with genuine explanation | The only ways to close the gap are padding or invention, and both are violations |
  | A required fact — a name, number, limit, default, or version — is in no available source | A plausible-sounding number is still a made-up number |
  | The stub's title contradicts the parent chapter or `AGENTS.md` | The scope conflict must be resolved by the human |

HOW TO STOP: do not submit a filled-in file. Say plainly (a) which item or
fact is missing, (b) which sources you checked, and (c) what you need in
order to continue. Then wait. Do not fill the gap with an invention.
============================================================
-->

<!--
============================================================
HOW TO MEASURE THE THREE HARD REQUIREMENTS
============================================================
The three hard requirements are measurable. Measure them; do not judge
them by feel. Each recipe produces a number that you write into the
Evidence column of the Final Self-Audit.

--- RECIPE 1 — THE 800-WORD PROSE FLOOR ---
COUNTS: words inside explanatory prose paragraphs anywhere in the body;
prose captions under a diagram or table; prose inside a <details> answer
that explains WHY an answer is right.
DOES NOT COUNT: the `# Title`, every heading and sub-heading, the metadata
line, anything inside an HTML comment (including this template and the
Coverage Plan), fenced code blocks and diagrams, every table cell,
bulleted and numbered list items, the Further Reading list, the Adaptation
Note, and the Final Self-Audit table.

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
  S1. LONG-SENTENCE SCAN. Go through the body one sentence at a time.
      Count the words in any sentence that looks long. Over about 25
      words → split it into two, one idea each. Record how many you split.
  S2. ACRONYM SCAN. Find every token of two or more capital letters in a
      row. For each, find its FIRST occurrence in the file and check it is
      written out in full there, with a plain-words gloss if the full form
      is still opaque. Not expanded → fix it. Record how many acronyms you
      found and how many you fixed.
  S3. JARGON SCAN. Mark every term in the body a 14-year-old would not
      know. For each, look at that sentence and the next for a plain-words
      definition. Missing → add it there. Record how many terms you marked
      and how many needed a definition added.
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
  R4. To fix a FAIL: rewrite one offending list as a paragraph that states
      each point AND why it is true. Then recount.
  R5. Write "P = n, L = n" into the Evidence column of audit row 6.
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
to genuinely know this topic. Follow PHASE 1 of the authoring procedure
above — it tells you how to enumerate them and what to do about the count.
Be specific — name the actual mechanisms, stages, parameters, failure
modes, and neighbouring concepts, not vague buckets. Do not trim the list
to make the writing easier.

STEP 2 (after writing): Follow PHASE 4 above. Mark each one [x] and name
where in the body it is explained. Every sub-concept must be explained
somewhere. If one is not, either write it or delete it from the plan and
say why. A row marked [x] with no location named is a failed audit row.

SUB-CONCEPTS TO COVER:
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [Sub-concept] — explained in: [sub-heading name]
- [ ] [add as many rows as the topic actually needs]

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

Why each section was chosen (PHASE 2 rules in action):
  | Coverage item | Section | Menu rule that selected it |
  |---------------|---------|----------------------------|
  | Lever-and-cable path | From Your Hand To The Wheel Rim | Ordered stages → diagram + main explanation |
  | Pad-and-rim friction | Why Rubber On Metal Slows You Down | Core mechanism → main explanation |
  | Pad clearance | Setting The Gap Between Pad And Rim | A setting a reader chooses → parameters table |
  | Brake fade | When Braking Stops Working | A known failure mode → pitfalls |
  | Rim versus disc | Why Discs Replaced Rims On Wet-Weather Bikes | Competing approach → trade-offs |

What to copy from it: every item is a noun phrase naming a real thing;
every item points at ONE named sub-heading; every sub-heading is named
after the concept, never "Overview"; sections came from the PHASE 2 rules,
not habit; and no section exists without a coverage item behind it. There
is no code snippet, because a reader would write none for this topic — so
it was omitted and logged in the Adaptation Note.
============================================================
-->

<!--
============================================================
SUGGESTED SECTIONS MENU — PICK, ORDER, AND RENAME FREELY
============================================================
Each entry says when it earns its place and when to skip it. Include the
ones that teach THIS topic. Put them in whatever order makes the topic
easiest to follow — for some topics an analogy comes first, for others a
diagram or a worked example is the best possible opening.

TL;DR
  Include: almost always — a few sentences saying what this is, why it
  matters, and the one thing to remember.
  Skip: if the topic is so short that the summary would repeat the body.

PLAIN-LANGUAGE OPENING (ELI5-style)
  Include: when the concept is abstract, counter-intuitive, or has a good
  everyday analogy. Map the analogy onto the real mechanism piece by
  piece, then say where the analogy stops being true.
  Skip: when the topic is already concrete and mechanical, where an
  analogy would add a layer of indirection instead of removing one.

LEARNING OBJECTIVES
  Include: when the topic is assessed, or when the reader benefits from
  knowing what they should be able to DO afterwards. Use action verbs
  (implement, diagnose, compare, configure, trace, justify).
  Skip: for short supporting or background topics.

VISUAL OVERVIEW / DIAGRAMS
  Include: when there is a flow, a pipeline, an architecture, a decision
  branch, or a before/after state worth seeing. Put each diagram in a
  plain fenced code block using box-drawing characters, give it a
  domain-specific title, and add a caption saying what the reader should
  learn from it — not what it depicts.
  Skip: when the topic is purely definitional and a diagram would just be
  boxes containing the same words as the prose.

MAIN EXPLANATION (with domain-named sub-headings)
  Include: always — this is the note. Break it into as many
  `### [Domain Concept]` sub-headings as the topic genuinely has. Name
  each after the real thing being discussed. Write paragraphs.
  Skip: never.

DEEP DIVE
  Include: when one mechanism is much harder or more consequential than
  the rest and deserves slow, careful treatment on its own.
  Skip: when the topic has no single hard centre, or when the depth
  already lives naturally inside the main explanation.

TRADE-OFFS / ALTERNATIVE APPROACHES
  Include: when a practitioner has a real choice to make, or when there
  is a competing approach the reader will encounter. Say what each option
  costs and what it buys.
  Skip: when there is genuinely only one way to do the thing.

WHERE IT APPEARS IN THE REAL WORLD
  Include: when naming concrete products, services, commands, or entry
  points makes the concept findable and usable. Be specific enough that
  the reader could go and look at the real thing.
  Skip: when the topic is a pure fundamental with no particular product
  surface, or when specifics would date the note badly.

KEY PARAMETERS TABLE
  Include: when the topic has settings or knobs. Give each one a concrete
  decision rule with a number, threshold, or explicit condition — not
  "depends on your use case".
  Skip: when nothing is configurable. Leave the section out entirely
  rather than writing an empty table.

WORKED EXAMPLE
  Include: when following one realistic scenario end to end teaches more
  than describing the steps abstractly. A second example earns its place
  only if it is genuinely different — a different constraint, a different
  conclusion, or a diagnosis of something going wrong.
  Skip: when the topic is definitional, or when the example would just
  re-narrate the explanation.

IMPLEMENTATION SNIPPETS
  Include: when there is code or configuration a reader would actually
  write. Each snippet opens with a comment naming the real problem it
  solves. Snippets must be syntactically valid for their language. An
  anti-pattern paired with its corrected version is often the single most
  useful snippet you can write.
  Skip: when the topic is conceptual or governance-related and code would
  be invented for the sake of having code.

COMMON PITFALLS & MISCONCEPTIONS
  Include: when readers reliably get this wrong. For each one, say why
  the wrong intuition is tempting, then state the correct mental model as
  a rule. This is one of the few places a list is appropriate — but each
  entry still needs real explanation, not a label.
  Skip: when the topic has no established failure modes yet.

KEY DEFINITIONS
  Include: when the topic introduces terms the reader will meet again.
  Define them as they are used HERE, not as a generic dictionary would.
  Remember: terms must already be defined inline on first use in the
  prose — this section is a lookup table, not a substitute for that.
  Skip: when everything was already defined plainly in the body and a
  table would only repeat it.

SUMMARY / QUICK RECALL
  Include: when the reader will want a fast scan before a test or a
  meeting. Each line states a fact or rule, not a topic label.
  Skip: for very short notes where the TL;DR already does this job.

SELF-CHECK QUESTIONS
  Include: when the topic is assessed or has decisions worth rehearsing.
  Mix straightforward recall with questions that ask the reader to apply
  or compare. Put answers in a <details> block and explain WHY the right
  answer is right and why the most tempting wrong answer fails.
  Skip: for background notes that carry no decisions.

FURTHER READING
  Include: whenever authoritative sources exist. Official documentation
  only — no third-party blogs, aggregators, or video.
  Skip: only if no official source exists, which is rare.

INVENT YOUR OWN
  If this topic needs a section that is not on this list — a history of
  how the approach evolved, a glossary of confusingly-similar names, a
  troubleshooting flow, a comparison table against a predecessor — write
  it. Name it after the thing it actually contains.
============================================================
-->

<!--
============================================================
VOICE AND PROSE-QUALITY ILLUSTRATIONS
============================================================
These examples come from domains unrelated to whatever this note is
about. They exist to show TONE and PROSE QUALITY, not subject matter.

--- Reading level ---
✗ "Latency is inversely correlated with throughput under saturation
   conditions, necessitating architectural mitigation."
✓ "When a system gets too busy, each request starts waiting in line, so
   answers come back more slowly. Waiting time is called latency."
   (Short sentences. The jargon word is defined the moment it appears.)

--- Acronyms expanded on first use ---
✗ "Requests are routed through the CDN before reaching origin."
✓ "Requests first go to a CDN — a Content Delivery Network, which is a
   set of servers spread around the world that keep copies of your files
   close to your users."

--- Prose carries the explanation, not lists ---
✗ "Reasons a cache helps: - Faster  - Cheaper  - Less load"
✓ "A cache keeps a copy of an answer you already worked out, so the next
   person who asks gets it straight away. That makes the reply faster,
   because nobody has to redo the work. It also makes it cheaper, because
   the expensive step ran once instead of a thousand times."
   (Same points, but the reader learns the mechanism behind each.)

--- Sub-headings named after the domain concept ---
✗ ### How does it work?   ✗ ### Key Concepts   ✗ ### Considerations
✓ ### Why Cold Caches Are Slower Than No Cache At All
✓ ### What Happens When Two Writers Race
   (A reader scanning the headings alone should learn the topic's shape.)

--- Explanation vs restatement (the prose floor is about the ✓ column) ---
✗ "Retry logic is important because retries matter for reliability, and
   reliable systems retry when they need to."  (says nothing new)
✓ "If a request fails because a server was briefly busy, trying again a
   moment later usually works. But if every client retries at the same
   instant, they arrive together and overwhelm the server a second time.
   So retries are spaced out by a growing delay."
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
topic made the section unhelpful.

SECTIONS OMITTED FROM THE MENU:
- [Section name] — [one-line reason specific to this topic]
- [Section name] — [one-line reason specific to this topic]

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
Get the numbers from HOW TO MEASURE THE THREE HARD REQUIREMENTS above.

| # | Check | Evidence — record the measured value or specific finding | Pass? |
|---|-------|--------------------------------------------------------|-------|
| 1 | Every sub-concept listed in the Coverage Plan is genuinely explained in the body | Items mapped: [n] of [n]. Gaps resolved by writing: [n]; by removal with reason: [n] | |
| 2 | The explanatory body reaches the 800-word floor with real explanation — no padding, hedging, or restatement | Prose word count (RECIPE 1, summed per paragraph): [number] | |
| 3 | A bright 14-year-old could follow it: short sentences, plain words, one idea at a time | Sentences over ~25 words found: [n]; split: [n]; remaining: [n] | |
| 4 | Every acronym is expanded the first time it appears | Acronyms found: [n]; already expanded: [n]; fixed: [n] | |
| 5 | Every piece of jargon is defined inline, in plain words, the first time it appears | Jargon terms marked: [n]; definitions added: [n] | |
| 6 | The explanation is carried by prose paragraphs; lists appear only for genuine enumerations | P = [n] paragraphs, L = [n] explanation lists; verdict: [pass/fail from RECIPE 3] | |
| 7 | Every sub-heading is named after a real domain concept — no generic headings | Headings checked: [n]; generic headings renamed: [n] | |
| 8 | Every diagram, table, and snippet included actually earns its place and is explained in the surrounding prose | Diagrams: [n], tables: [n], snippets: [n]; each explained in prose: [yes/no] | |
| 9 | The Adaptation Note records each omitted section with a topic-specific reason | Sections omitted: [n]; reasons written: [n]; sections invented: [n] | |
| 10 | No TODO, TBD, STUB, placeholder text, or leftover square-bracket template markers remain | Searched for TODO/TBD/STUB/FIXME/`[`; hits outside comments: [n] | |
| 11 | Every external link is official documentation, fetched live, with a *verified YYYY-MM-DD* date | Links: [n]; fetched live: [n]; non-official rejected: [n] | |
| 12 | Nothing is invented — no made-up product names, parameters, figures, quotes, or URLs | Every name/number/limit traced to a source: [yes/no]; facts dropped for lack of a source: [n] | |
============================================================
-->

---

## Version History

- **v1.0** (2024): Original template — baseline section structure and minimum lengths.
- **v2.0** (2026-08-10): Rigid enforcement pass — per-section word counts, compliance examples, distinctness gates, and a 44-row Completeness Self-Audit with fixed counts.
- **v3.0** (2026-08-11): Adaptive rewrite.
  - Replaced the fixed section order with a Suggested Sections Menu; the author now picks, reorders, renames, and invents sections to fit the topic.
  - Removed every fixed count and per-section word budget (learning objectives, diagrams, snippet angles, pitfalls, definitions, summary bullets, self-check questions and their cognitive distribution, touchpoint rows, parameter rows).
  - Deleted the 44-row Completeness Self-Audit; replaced it with a 12-row outcome-based Final Self-Audit.
  - Added the COVERAGE RATCHET: an up-front Coverage Plan of sub-concepts, verified as explained before submission.
  - Added the PROSE FLOOR: 800 words minimum of genuine explanation across the body as a whole, with padding explicitly disallowed.
  - Added the READING LEVEL requirement: written for a bright 14-year-old, acronyms expanded and jargon defined inline on first use.
  - Kept and made central the prose-first mandate and the ban on generic sub-headings; retained Deep Dive and Trade-offs as suggested sections.
  - Reframed the compliant/non-compliant example pairs to illustrate voice, readability, and prose quality instead of hitting counts, and made them domain-neutral.
  - Added the Adaptation Note as the accountability replacement for deleted mandatory counts.
- **v3.1** (2026-08-11): Procedure pass — converts judgement into mechanical steps so a small model can follow the template without inferring the process. No requirement changed; the adaptive menu, the three hard requirements, the Adaptation Note, and source hygiene are all preserved as-is.
  - Added a phased AUTHORING PROCEDURE block ahead of the H1: Phase 0 orient, Phase 1 build the Coverage Plan, Phase 2 choose sections by decision table, Phase 3 draft-and-check section by section, Phase 4 map coverage to body, Phase 5 run the audit mechanically, Phase 6 stop conditions.
  - Added HOW TO MEASURE recipes giving an observable method for each hard requirement: a per-paragraph word count for the 800-word floor, three scans (long sentences, acronyms, jargon) for reading level, and a paragraph-to-list ratio for prose-first.
  - Added a compact WORKED MICRO-EXAMPLE of Coverage Plan → body mapping, drawn from an unrelated everyday domain and labelled as illustration only.
  - Added an Evidence column to the 12-row Final Self-Audit so each row records a measured value or specific finding; a tick without evidence is now a failed row.
  - Made stopping an explicit, expected outcome, with named stop conditions and a required way to report them, so an author asks rather than fabricates.
  - Added an Adaptation Note line for local rules that overrode this template.
