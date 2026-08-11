# Authoring Guidelines & Quality Rubric

## Voice & Reading Level

Write like a good textbook aimed at a bright 14-year-old. The reader is smart but has not been taught this yet, so assume very little prior knowledge and build up from there.

- Short, direct sentences. One idea per sentence.
- Plain everyday words over technical register wherever a plain word exists.
- Expand every acronym the first time it appears: `Application Programming Interface (API)`.
- Define every piece of jargon inline, in plain words, the first time it appears. Do not defer definitions to a glossary at the bottom.
- Active voice. "The scheduler picks a machine", not "a machine is selected by the scheduler".
- Explain **why**, not only what. A reader who knows why can reason about cases you never covered.
- Warm and encouraging, never condescending. Not knowing something yet is normal; being talked down to is not.

Target register — a compliant vs non-compliant pair:

- ✓ "A thermostat has one job: keep the room at the temperature you asked for. It checks the current temperature, compares it to your target, and turns the heater on or off. That constant check-and-correct loop is called *feedback control*."
- ✗ "Thermostatic regulation leverages a closed-loop feedback control paradigm to minimise the delta between the measured process variable and the configured setpoint."

The ✗ version is not more correct. It is the same idea, made harder to reach.

## Prose-First Rule

Explanation is carried by **prose paragraphs** with real transitions between ideas — "because of that", "which means", "the problem with this is". The reader should be able to follow one continuous line of reasoning from the start of a section to its end.

Bulleted lists must **not** be used as a substitute for explanation. Lists are appropriate only for genuine enumerations: a parameter table, a checklist, a list of links, a set of discrete options.

Why this rule exists: a page of bullets looks organised but teaches nothing. The connective reasoning *between* the points — why point two follows from point one, why point three rules out point two — is exactly what the learner does not yet have and cannot infer. Bullets delete it.

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

## Depth Calibration

- The **prose explanation and worked examples carry the teaching load.** This is where understanding is actually built, and it should dominate the note.
- **Snippets, diagrams, tables, and questions support that load.** They illustrate and test what the prose already explained; they never stand in for it.
- Roughly: most of the authoring effort goes into explanation and worked examples, a smaller share into snippets and visuals, a smaller share still into self-check questions — though the exact split depends on the topic.
- Do not invert these proportions. A chapter with 10 code examples and 2 sentences of explanation teaches nothing.

## Per-Artifact Guidance

Each chapter holds five kinds of file. They share the voice rules above but have distinct jobs.

### Topic notes — `01-<topic-slug>.md` … (2–6 per chapter)

The primary teaching artifact. Prose-first. Each note fully explains its one topic, start to finish, for a reader who has not seen it before. Everything in this document applies here most strictly: the Coverage Plan, the prose floor, domain-specific sub-headings, inline jargon definitions.

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
- Cite the source URL and retrieval date for every specific doc, API reference, or changelog entry.
- Citation format: `[Title](url) — *verified YYYY-MM-DD*`
- Verify every link is live, using webfetch, **before** writing from it.
- Flag fast-evolving features with: `> ⚠️ Fast-evolving: verify against current official docs before relying on this.`
- **Derived artifacts cite nothing new.** For `00-intro.md` and `99-podcast.md`, the source *is* the sibling topic notes. If a derived artifact needs a citation, that is a signal it is smuggling in a new fact — cut it or add it to the relevant topic note first.

## Blueprint Drift Warning

Exam objectives and API surfaces change over time. If you are authoring more than 6 months after the repo was created, verify the current official exam guide or documentation before writing. Do not assume the U1 research summary is still current.

## Quality Checklist

Run before marking any file complete:

- [ ] Reading level suits a bright 14-year-old — short sentences, plain words, nothing assumed
- [ ] Every acronym expanded on first use
- [ ] Every piece of jargon defined inline, in plain words, on first use
- [ ] Explanation carried by prose paragraphs with real transitions, not by bulleted lists
- [ ] Sub-headings named after the actual domain concept — no generic headings
- [ ] Every sub-concept in the Coverage Plan is genuinely explained in the body
- [ ] 800-word explanatory prose floor met with real content — no padding or restatement
- [ ] Adaptation Note records a one-line reason for every omitted suggested section
- [ ] All links are official docs, each verified live with a retrieval date
- [ ] Derived artifacts (`00-intro.md`, `99-podcast.md`) introduce no fact absent from the topic notes, and were written after every topic note was complete — and `99-podcast.md` contains no code blocks, tables, or diagrams
- [ ] No `TODO`, `STUB`, or placeholder markers remain
- [ ] No filler — every sentence earns its space
