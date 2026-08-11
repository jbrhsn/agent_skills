# Quality Gate — Fallback Authoring Contract

This file is the **built-in authoring contract** for the `author-chapter` skill. It is used only when the target repo has no `templates/` + `AGENTS.md` to derive rules from (i.e. a loose Markdown folder), and only after the user confirms.

When a repo's own template and `AGENTS.md` exist, **those take precedence** — this file is the fallback, not the override.

It doubles as the checklist the skill runs as its mandatory pre-write gate (Unit U3). No file is written until every row of the applicable checklist is ✓.

The model here is **fully adaptive**. Structure adapts to the topic; sections are suggestions. There are exactly **three hard requirements** — Coverage, Prose Floor, and Reading Level — and no other fixed counts.

---

## How to use this file

Match the target filename to its artifact type, then run only that artifact's gate plus the Universal Rules.

| Filename pattern | Artifact type | Rubric |
|---|---|---|
| `00-intro.md`, `intro.md` | Chapter intro — overview + how the topics interconnect. **Derived.** Authored **last**. | [Chapter intro gate](#gate--chapter-intro) |
| `NN-<slug>.md` (e.g. `01-<topic-slug>.md`) | Topic note — 2–6 per chapter. Authored **first**. | [Topic note gate](#gate--topic-note) |
| `interview-prep.md` | Interview preparation. Authored alongside the topic notes. | [Interview-prep gate](#gate--interview-prep) |
| `thought-leadership.md` | Thought-leadership essay. Authored alongside the topic notes. | [Thought-leadership gate](#gate--thought-leadership) |
| `99-podcast.md`, `podcast.md` | Two-speaker conversational transcript covering all topics. **Derived.** Authored **last**. | [Podcast gate](#gate--podcast) |
| anything unrecognised | Treat as a topic note. | [Topic note gate](#gate--topic-note) |

**Derived artifacts** (`00-intro.md`, `99-podcast.md`) may only be authored once **every** topic note in the chapter is complete and non-stub, and must introduce **no fact absent from the sibling topic notes**. They synthesise; they do not add.

---

## Universal rules (apply to EVERY artifact)

### Reading level and prose-first
- Write for a **bright 14-year-old**. Short sentences. One idea per sentence.
- Plain everyday words in place of formal ones wherever a plain word exists.
- **Prose paragraphs carry the explanation.** A bulleted or numbered list must never stand in for explaining something. Lists are for genuine enumerations only: a parameter table, a checklist, a list of links, a set of options being compared.
- Explain *why*, not just *what*. Every sentence must add a mechanism, a reason, a consequence, a constraint, a name, or a number.

### Jargon and acronyms
- Every acronym is expanded the **first** time it appears.
- Every piece of jargon is defined **inline, in plain words**, the first time it appears — in the same sentence or the one right after.
- A later definitions table does not excuse an undefined term in the prose above it.

### Adaptive structure
- **No fixed section order and no required section list.** The author chooses which sections the topic needs and the order that teaches it best, and may invent sections the menu does not list.
- Every sub-heading is named after the **real domain concept** it discusses. Generic headings ("How does it work?", "Key Concepts", "Important Considerations", "Overview") are non-compliant.
- Never leave an empty heading and never write "not applicable" filler. Omit the section instead.

### Source hygiene
- Official documentation only — no third-party blogs, Medium, YouTube, forums, aggregators, or AI-generated summaries.
- Format every external link as `[Title](url) — *verified YYYY-MM-DD*`, verified live this session.
- Quote exam or certification objectives **verbatim** — never paraphrase them.
- Never invent a URL, document title, product name, parameter, figure, or verification date.

### No placeholders, no filler
- Zero `TODO`, `TBD`, `STUB`, placeholder text, or leftover square-bracket template markers.
- No filler — every sentence earns its space.

---

## The three hard requirements (topic notes)

These are the only surviving numeric or structural floors in this contract.

1. **Coverage.** Before writing, enumerate the topic's sub-concepts in a **Coverage Plan** (an HTML comment block that stays in the finished file so the gate can read it back). Name actual mechanisms, stages, parameters, failure modes, and neighbouring concepts — not vague buckets. Before writing the file, verify every enumerated sub-concept is genuinely explained in the body. Adaptive structure is allowed; skipping material is not.
2. **Prose floor.** The explanatory body, **taken as a whole**, must reach a minimum of **800 words** of genuine explanation. This floor applies to the document overall, never per section. Padding, hedging, restating the title, or repeating an earlier sentence in new words is a **violation** of this requirement, not a way to satisfy it. The count excludes the metadata line, diagrams, code, tables, HTML comments, and the link list.
3. **Reading level / prose-first.** As set out in the Universal Rules above: bright 14-year-old, short sentences, acronyms expanded and jargon defined inline on first use, explanation carried by prose rather than by lists.

---

## Suggested sections (menu, not mandate)

A menu, not a running order. The author chooses **which** sections to include and **in what order**, and records a one-line, topic-specific reason in an **Adaptation Note** for each menu section it omits. "Not needed" is not an acceptable reason — say what about *this* topic made the section unhelpful.

| Section | Earns its place when | Skip when |
|---|---|---|
| **TL;DR** | The reader benefits from knowing up front what this is, why it matters, and the one thing to remember. | The note is short enough that the summary would restate the body. |
| **Plain-language opening (ELI5)** | The concept is abstract or counter-intuitive and a good everyday analogy exists; map it onto the mechanism piece by piece, then say where the analogy stops being true. | The topic is already concrete and mechanical, so an analogy adds indirection instead of removing it. |
| **Learning objectives** | The topic is assessed, or the reader gains from knowing what they should be able to *do* afterwards. Use action verbs. | It is a short supporting or background topic. |
| **Visual overview / diagrams** | There is a flow, pipeline, architecture, decision branch, or before/after state worth seeing. Each diagram gets a domain-specific title and a caption saying what to learn from it. | The topic is purely definitional and the diagram would be boxes containing the prose's own words. |
| **Main explanation** (domain-named sub-headings) | Always — this is the note. Break it into as many `### [Domain Concept]` sub-headings as the topic genuinely has. | Never. |
| **Deep dive** | One mechanism is far harder or more consequential than the rest and deserves slow treatment on its own. | The topic has no single hard centre, or the depth already sits naturally in the main explanation. |
| **Trade-offs / alternatives** | A practitioner has a real choice, or a competing approach will be encountered. Say what each option costs and buys. | There is genuinely only one way to do the thing. |
| **Where it appears in the real world** | Naming concrete surfaces, commands, or entry points makes the concept findable and usable. | The topic is a pure fundamental with no product surface, or specifics would date the note badly. |
| **Key parameters table** | The topic has settings or knobs, each with a concrete decision rule. | Nothing is configurable — omit the section rather than write an empty table. |
| **Worked example** | Following one realistic scenario end to end teaches more than describing the steps abstractly. | The topic is definitional, or the example would re-narrate the explanation. |
| **Implementation snippets** | There is code or configuration a reader would actually write. | The topic is conceptual and code would be invented for the sake of having code. |
| **Common pitfalls & misconceptions** | Readers reliably get this wrong; say why the wrong intuition is tempting, then give the correct mental model as a rule. | The topic has no established failure modes. |
| **Key definitions** | The topic introduces terms the reader will meet again, defined as used *here*. | Everything was already defined plainly inline and a table would only repeat it. |
| **Summary / quick recall** | The reader will want a fast scan before a test or a meeting; each line states a fact or rule, not a topic label. | The note is short and the TL;DR already does this job. |
| **Self-check questions** | The topic is assessed or has decisions worth rehearsing. | It is a background note carrying no decisions. |
| **Further reading** | Authoritative official sources exist. | No official source exists, which is rare. |

If the topic needs a section this menu does not list — an evolution history, a glossary of confusingly-similar names, a troubleshooting flow — write it, and name it after what it contains.

---

## Gate — topic note

Run for `NN-<slug>.md` and any unrecognised filename. Outcome-based: judge whether the effect was achieved, not whether a count was hit.

- [ ] **Coverage:** a Coverage Plan enumerating the topic's sub-concepts exists, and every sub-concept listed is genuinely explained in the body
- [ ] **Prose floor:** the explanatory body as a whole reaches at least 800 words of real explanation — no padding, hedging, or restatement inflating it
- [ ] **Reading level:** a bright 14-year-old could follow it — short sentences, plain words, one idea at a time
- [ ] Every acronym is expanded on first use, and every piece of jargon is defined inline in plain words on first use
- [ ] The explanation is carried by prose paragraphs; lists appear only for genuine enumerations
- [ ] Every sub-heading is named after a real domain concept — no generic headings
- [ ] The Adaptation Note records each omitted menu section with a reason specific to this topic
- [ ] Any diagram, table, or snippet included earns its place and is explained in the surrounding prose
- [ ] Any code snippet opens with a comment naming the real-world problem it solves, and is syntactically valid for its language
- [ ] Any parameter table gives actionable decision rules — a threshold, number, or explicit condition — not a restatement of the parameter name
- [ ] Any self-check answer explains why the correct answer is right **and** why the most tempting wrong answers fail
- [ ] Every external link is official documentation, fetched live, formatted with a `*verified YYYY-MM-DD*` date
- [ ] Nothing is invented — no made-up product names, parameters, figures, quotes, or URLs
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder / leftover bracket markers remain

---

## Gate — chapter intro

Run for `00-intro.md` / `intro.md`. **Derived artifact — authored last.**

- [ ] Every topic file in the chapter is represented, each with a working relative link and a plain-language description of what it covers
- [ ] The "how the topics connect" explanation is genuine prose that explains dependencies and motivation — why one topic sets up another — rather than restating the topic list
- [ ] A suggested reading order is given, with a reason for that order
- [ ] **No fact appears that is absent from the sibling topic notes** — the intro synthesises, it does not introduce new material
- [ ] **Every sibling topic note was complete and non-stub before this file was authored**
- [ ] Reading level: bright 14-year-old, short sentences, prose carries the explanation
- [ ] Every acronym expanded and every piece of jargon defined inline on first use
- [ ] Any external link is official documentation with a `*verified YYYY-MM-DD*` date
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder markers remain

---

## Gate — podcast

Run for `99-podcast.md` / `podcast.md`. **Derived artifact — authored last.** This is spoken audio on the page.

- [ ] Every topic in the chapter has its own clearly delineated segment
- [ ] The dialogue is genuine back-and-forth — speakers question, push back, and build on each other — not a monologue split across two labels
- [ ] Speaker labels are consistent throughout and are generic role labels (e.g. Host / Guest), never invented real-person names
- [ ] At least one everyday analogy appears in each topic segment
- [ ] Jargon is defined out loud in plain words on first use; acronyms are expanded when first spoken
- [ ] **No code blocks** anywhere — nothing that cannot be spoken aloud
- [ ] **No fact appears that is absent from the sibling topic notes**
- [ ] **Every sibling topic note was complete and non-stub before this file was authored**
- [ ] The listening level suits a bright teenager — conversational sentences, no dense clauses
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder markers remain

---

## Gate — interview prep

Run for `interview-prep.md`.

- [ ] The questions are realistic for the stated target role and seniority — the kind actually asked, not trivia
- [ ] Each answer gives substance a candidate could actually say out loud, not a topic label or a pointer to go read something
- [ ] Answers explain the reasoning behind the answer, so the candidate can handle a follow-up rather than reciting
- [ ] Weak-answer traps and red flags are specific to this subject matter, not generic interview advice ("be confident", "use STAR")
- [ ] Everything is grounded in the chapter's actual content — no claims the topic notes do not support
- [ ] Reading level: bright 14-year-old, short sentences, prose carries the explanation
- [ ] Every acronym expanded and every piece of jargon defined inline on first use
- [ ] Any external link is official documentation with a `*verified YYYY-MM-DD*` date
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder markers remain

---

## Gate — thought leadership

Run for `thought-leadership.md`.

- [ ] The opening makes a specific, non-obvious claim in its first lines
- [ ] The opening does **not** begin with a throat-clearing cliché — e.g. "In today's world", "As X continues to evolve", "Now more than ever"
- [ ] Claims are specific and defensible; nothing rests on an unfalsifiable generality
- [ ] At least one concrete example or number anchors the argument
- [ ] The strongest counterargument is stated fairly and then answered — not strawmanned or ignored
- [ ] The piece has a clear original angle: a reader could say what *this* author thinks that others do not
- [ ] The reader is left with a concrete takeaway — something to do, decide, or stop doing
- [ ] Reading level: bright 14-year-old, short sentences, prose carries the argument
- [ ] Every acronym expanded and every piece of jargon defined inline on first use
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder markers remain

---

## Deterministic checks

Run these mechanically before the gate is declared PASS. Keyed by artifact type.

| Check | Applies to | How |
|---|---|---|
| Residual placeholder markers | all | Grep for `TODO`, `TBD`, `STUB`, and unfilled `[bracket]` template markers. Must be zero. |
| Prose floor | topic note | Word-count the explanatory body — excluding the metadata line, HTML comments, fenced blocks, tables, and the link list — and compare against 800. Under the floor is a hard fail; padding to clear it is also a fail. |
| Unexpanded acronyms | all | Scan for all-caps tokens of two or more letters and confirm each has an expansion earlier in the file than its first bare use. |
| Prose-to-list ratio | all | Estimate the share of the explanatory body that is list lines versus paragraph lines. A list-dominated body fails the prose-first rule and must be rewritten as paragraphs. |
| Coverage Plan reconciliation | topic note | Read the Coverage Plan back out of the file and confirm each enumerated sub-concept maps to a real section of the body. |
| Speaker labels | podcast | Confirm speaker-label lines are present, that exactly the same two labels are used throughout, and that both are generic role labels. |
| Zero code fences | podcast | Count fenced code blocks. Must be zero. |
| Siblings non-stub | intro, podcast | Read every sibling topic note in the chapter and confirm none is still a stub or partially authored. |
| Relative links resolve | intro, podcast | For every relative link, confirm the target file exists on disk. |
| External URLs live | all | Re-fetch each external URL; confirm it is reachable and that its content matches the citation title and claim. |

Any failing check blocks the write. Fix it, then re-run the whole gate — not just the failing row.
