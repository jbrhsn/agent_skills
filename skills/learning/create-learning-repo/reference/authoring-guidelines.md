# Authoring Guidelines & Quality Rubric

**Four requirements are hard and non-negotiable:** (1) **coverage**, (2) the **prose floor**, (3) **reading level + prose-first**, and (4) **source fidelity**. Each has its own section below. Everything else in this file is guidance. Where the on-disk template for an artifact states these in more detail, the template is the contract.

## Voice & Reading Level

Write like a good textbook aimed at a bright 14-year-old. The reader is smart but has not been taught this yet, so assume very little prior knowledge and build up from there.

- Short, direct sentences. One idea per sentence.
- Plain everyday words over technical register wherever a plain word exists.
- Expand every acronym the first time it appears: `Nitrogen, Phosphorus, Potassium (NPK)`, `Gross Domestic Product (GDP)`, `Application Programming Interface (API)`.
- Define every piece of jargon inline, in plain words, the first time it appears. Do not defer definitions to a glossary at the bottom.
- Active voice. "The judge sets the sentence", not "the sentence is set by the judge".
- Explain **why**, not only what. A reader who knows why can reason about cases you never covered.
- Warm and encouraging, never condescending. Not knowing something yet is normal; being talked down to is not.

Target register — a compliant vs non-compliant pair:

- ✓ "A thermostat has one job: keep the room at the temperature you asked for. It checks the current temperature, compares it to your target, and turns the heater on or off. That constant check-and-correct loop is called *feedback control*."
- ✗ "Thermostatic regulation leverages a closed-loop feedback control paradigm to minimise the delta between the measured process variable and the configured setpoint."

The ✗ version is not more correct. It is the same idea, made harder to reach.

## Prose-First Rule

Explanation is carried by **prose paragraphs** with real transitions between ideas — "because of that", "which means", "the problem with this is". The reader should be able to follow one continuous line of reasoning from the start of a section to its end.

**The rule, stated exactly:** a bulleted or numbered list must never be used **as a substitute for explaining something**. That is the whole target of this rule. Lists are appropriate for genuine enumerations: a table of settings, a checklist, a list of links, a set of discrete options being compared.

Why the rule exists: a run of bullets standing *in place of* an explanation looks organised but teaches nothing. The connective reasoning *between* the points — why point two follows from point one, why point three rules out point two — is exactly what the learner does not yet have and cannot infer. Bullets used that way delete it.

**What this rule does NOT do.** It does **not** discourage diagrams, tables, worked examples, or any other concrete artifact, and it never penalises adding one.

- Prose and artifacts are measured **separately**. The prose floor counts prose only. A diagram, a table, or a worked calculation neither adds to that count nor subtracts from it, so adding one can never move you further from meeting the floor.
- Artifacts required by the template's REQUIRED-IF triggers (T1–T11 — a diagram for ordered stages, a table of settings, a worked example, a concrete artifact, and so on) are **never in tension with prose-first**. Deliver every one that fired.
- The correct shape is **both**: the artifact shows the structure, and prose around it says what the reader should take away. A note whose settings live in a table *and* whose prose explains how to choose between them satisfies this rule fully.
- Suppressing a required artifact to protect a prose ratio is a **failure of this rule**, not compliance with it. If a table replaced prose the reader still needed, write the prose back — do not delete the table.

## Adaptive Structure

There is **no fixed section order and no required section list.**

- The author picks the sections this specific topic genuinely needs from the suggested menu in the template.
- The author may reorder those sections into whatever order teaches best.
- The author may invent a section the topic calls for that the template never anticipated.
- Sub-headings must be named after the actual domain concept being explained — never generic. `### Overview`, `### How does it work?`, `### Details` are all non-compliant. Name the thing.
- Whenever the author omits a suggested section, it records a one-line reason in the template's **Adaptation Note**. Omission is fine; silent omission is not.

## Completeness

Adaptive must not become thin. Two backstops:

1. **Coverage Plan (before writing).** Enumerate the topic's sub-concepts — every distinct idea a reader must hold to understand this topic. Write that list down in the template's Coverage Plan.
2. **Coverage check (after writing).** Verify that every enumerated sub-concept is genuinely explained in the body, not merely name-dropped.

There is a floor of **800 words of genuine explanatory prose** per topic note. Padding, restatement, and hedging do not count toward that floor, and are violations in their own right. If you cannot reach the floor with real content, the answer is to go deeper — another mechanism, a concrete consequence, an edge case, a worked case — never to repeat yourself in new words.

**Closed enumerable sets.** If the topic's subject is a finite documented list — the permitted grades in a classification, the states in a lifecycle, the sections of a statute, the modes in a musical system, the ranks in a taxonomy — coverage means **every member**, taken from the source, each with its own row in one complete table. A partial list read as complete teaches the reader that the missing members do not exist. Beware the near miss: something that merely *influences* the set is not a member of it, even when the source prints it on the same page.

## Source Fidelity

A note must carry the exact substance a practitioner needs, not just a feel for the topic.

- Every exact proper name, designation, term of art, or identifier is spelled the way the authoritative source spells it — a statute section, a species name, a date, a place name, a grade, a setting's name. No paraphrased, prettified, or guessed names.
- Every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states, the note states too.
- Every artifact a REQUIRED-IF trigger fired for is actually present.
- An analogy may **illustrate** a mechanism. An analogy may **never substitute** for naming the real thing, stating a real number, or enumerating a set. "It works like a queue at a shop" does not replace the real name of the thing that sets the queue's length.
- Anything present in the note but traceable to no source is an invention — delete it.

This requirement is graded **independently** of the prose floor. Adding the names, numbers, and artifacts it demands can never reduce compliance with any other requirement.

## Depth Calibration

- The **prose explanation and worked examples carry the teaching load.** This is where understanding is actually built, and it should dominate the note.
- **Diagrams, tables, concrete examples, and questions support that load.** They illustrate and test what the prose explained. They do not replace it — and equally, prose does not replace them where a trigger required one. Deliver both.
- Roughly: most of the authoring effort goes into explanation and worked examples, a smaller share into artifacts and visuals, a smaller share still into self-check questions — though the exact split depends on the topic.
- Do not invert these proportions. A note with ten worked examples and two sentences of explanation teaches nothing. Neither does one with 1,500 words of prose and no table of the settings the source documents.

## Per-Artifact Guidance

Each chapter holds five kinds of file. They share the voice rules above but have distinct jobs.

### Topic notes — `01-<topic-slug>.md` … (2–6 per chapter)

The primary teaching artifact. Prose-first. Each note fully explains its one topic, start to finish, for a reader who has not seen it before. All four requirements apply here most strictly: the Coverage Plan, the prose floor, reading level and domain-specific sub-headings, and source fidelity — exact names, stated quantities, and every artifact its triggers fired for.

### Chapter intro — `00-intro.md`

An overview of every topic in the chapter and, most importantly, **how those topics interconnect** — which one depends on another, which two are alternatives to each other, which order they are best learned in. This connective map is the reason the file exists; a bare list of topic titles is non-compliant.

Authored **last**. It is a derived artifact: it introduces **no fact absent from the sibling topic notes**.

### Podcast — `99-podcast.md`

A conversational two-speaker transcript that covers every topic in the chapter at a high level. It is spoken audio, so:

- Natural back-and-forth dialogue — questions, clarifications, pushback. Not two monologues.
- Consistent generic speaker role labels throughout (for example a host and an expert). Never invent named personalities.
- **No code blocks, tables, or diagrams.** Nothing that cannot be said aloud. Describe structure in words instead.
- Breadth over depth: the goal is orientation and recall, not first-time instruction.

Authored **last**. It is a derived artifact: it introduces **no fact absent from the sibling topic notes**.

### Interview prep — `interview-prep.md`

Role-targeted question and answer preparation. Questions must be the ones actually asked for the target role at the target level, and each answer must be a model answer a candidate could adapt — including what the interviewer is really probing for and what a weak answer looks like. Authored alongside the topic notes.

### Thought leadership — `thought-leadership.md`

One original, defensible argument in the author's own voice. It takes a position, supports it with reasoning and evidence, and honestly engages the strongest counter-argument. A neutral summary of the topic is non-compliant — that is what the topic notes are for. Authored alongside the topic notes.

## Authoring Order

Order is not optional:

1. **First:** all topic notes (`01-…`, `02-…`, …), plus `interview-prep.md` and `thought-leadership.md`. These are researched and written from sources.
2. **Last:** `00-intro.md` and `99-podcast.md` — and only once **every** topic note in the chapter is complete and non-stub.

Writing a derived artifact against unfinished topic notes guarantees drift between them. If any topic note in the chapter is still a stub, stop and finish it before touching the intro or the podcast.

## Source Hygiene

- **Official documentation only** — no third-party blogs, Medium, or YouTube.
- Cite the source URL and retrieval date for every specific document, reference work, ruling, standard, or change log entry you draw on.
- Citation format: `[Title](url) — *verified YYYY-MM-DD*`
- Verify every link is live, using webfetch, **before** writing from it.
- Flag fast-evolving features with: `> ⚠️ Fast-evolving: verify against current official docs before relying on this.`
- **Derived artifacts cite nothing new.** For `00-intro.md` and `99-podcast.md`, the source *is* the sibling topic notes. If a derived artifact needs a citation, that is a signal it is smuggling in a new fact — cut it or add it to the relevant topic note first.

## Blueprint Drift Warning

Published guidance, standards, objectives, and reference works are revised over time. If you are authoring more than 6 months after the repo was created, verify the current official source before writing. Do not assume the U1 research summary is still current.

## Quality Checklist

Run before marking any file complete:

- [ ] Reading level suits a bright 14-year-old — short sentences, plain words, nothing assumed
- [ ] Every acronym expanded on first use
- [ ] Every piece of jargon defined inline, in plain words, on first use
- [ ] Explanation carried by prose paragraphs with real transitions, not by bulleted lists standing in for explanation
- [ ] Sub-headings named after the actual domain concept — no generic headings
- [ ] Every sub-concept in the Coverage Plan is genuinely explained in the body
- [ ] 800-word explanatory prose floor met with real content — no padding or restatement
- [ ] Every artifact a REQUIRED-IF trigger fired for is present, and every artifact present is explained by the prose around it
- [ ] Exact names and every source-stated quantity, date, threshold, limit, and unit are present and spelled as the source spells them
- [ ] If the subject is a closed enumerable set, every member has its own row in one complete table, and the source count, plan count, and row count are equal
- [ ] Adaptation Note records a one-line reason for every omitted suggested section
- [ ] All links are official docs, each verified live with a retrieval date
- [ ] Derived artifacts (`00-intro.md`, `99-podcast.md`) introduce no fact absent from the topic notes, and were written after every topic note was complete — and `99-podcast.md` contains no code blocks, tables, or diagrams
- [ ] No `TODO`, `STUB`, or placeholder markers remain
- [ ] No filler — every sentence earns its space
