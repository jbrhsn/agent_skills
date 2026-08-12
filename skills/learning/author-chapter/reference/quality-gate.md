# Quality Gate — Fallback Authoring Contract

This file is the **built-in authoring contract** for the `author-chapter` skill. It is used only when the target repo has no `templates/` + `AGENTS.md` to derive rules from (i.e. a loose Markdown folder), and only after the user confirms.

When a repo's own template and `AGENTS.md` exist, **those take precedence** — this file is the fallback, not the override.

It doubles as the checklist the skill runs as its mandatory pre-write gate (Unit U3). No file is written until every row of the applicable checklist is ✓.

The model here is **fully adaptive**. Structure adapts to the topic; sections are suggestions. There are exactly **four hard requirements** — Coverage, Prose Floor, Reading Level, and Source Fidelity — and no other fixed counts.

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

## The four hard requirements (topic notes)

These are the only surviving numeric or structural floors in this contract.

1. **Coverage.** Before writing, enumerate the topic's sub-concepts in a **Coverage Plan** (an HTML comment block that stays in the finished file so the gate can read it back). Name actual mechanisms, stages, parameters, failure modes, and neighbouring concepts — not vague buckets. Before writing the file, verify every enumerated sub-concept is genuinely explained in the body. Adaptive structure is allowed; skipping material is not. If the subject is a **closed enumerable set**, coverage means *every member of that set*.
2. **Prose floor.** The explanatory body, **taken as a whole**, must reach a minimum of **800 words** of genuine explanation. This floor applies to the document overall, never per section. Padding, hedging, restating the title, or repeating an earlier sentence in new words is a **violation** of this requirement, not a way to satisfy it. The count excludes the metadata line, diagrams, code, tables, HTML comments, and the link list.
3. **Reading level / prose-first.** As set out in the Universal Rules above: bright 14-year-old, short sentences, acronyms expanded and jargon defined inline on first use, explanation carried by prose rather than by lists.
4. **Source fidelity.** The note carries the exact substance a practitioner needs. Every exact proper name, designation, term of art, or identifier is spelled as the authoritative source spells it (a statute section, a species name, a place name, a rank, a field name). Every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states, the note states too. Every artifact whose **REQUIRED-IF trigger** fired is actually present. An analogy may *illustrate* a mechanism but may **never substitute** for naming the real thing, stating a real number, or enumerating a set. Graded **independently** of requirement 2: artifacts neither count toward the 800-word floor nor against it, so adding one can never reduce compliance with requirement 2.

### REQUIRED-IF triggers T1–T11 (binding, not suggestions)

Each row is a yes/no question about *this* topic. The author must record an explicit yes/no for **all eleven** in the Adaptation Note, including every no. If the condition is true, the artifact is **required**.

| ID | REQUIRED IF this is true of the topic | Then this is REQUIRED |
|---|---|---|
| T1 | It has ordered stages — a sequence, a flow, a life cycle (a fermentation, a court appeal route, a processing pipeline) | a diagram |
| T2 | It has settings a reader chooses — limits, sizes, quantities, grades, proportions (an oven temperature, a gear ratio, a configurable value) | a parameters table |
| T3 | A practitioner faces a real decision with consequences | a worked example |
| T4 | There is a competing approach the reader will meet | trade-offs / alternatives |
| T5 | There is a concrete artifact, procedure, worked calculation, or template the reader would actually produce or follow (a step sequence, a dosage calculation, a citation format, a piece of code or configuration) | a concrete example of it |
| T6 | Readers reliably get it wrong, or a wrong intuition is tempting | common pitfalls |
| T7 | It is abstract or counter-intuitive and has a true everyday analogy | a plain-language opening |
| T8 | One mechanism is much harder than the rest | a deep dive |
| T9 | It introduces terms the reader will meet again later | key definitions |
| T10 | It is assessed, or the reader must be able to DO something after | learning objectives and self-check questions |
| T11 | An authoritative source exists | further reading |

A "no" is valid only if it is true of the topic. "No" because the artifact is effort is a failing row.

### Closed-enumerable-set ratchet

A **closed enumerable set** is a subject whose members are a finite, documented list. Answer YES if any cue applies: the subject *is* such a list (permitted values; status or result codes; selectable options; lifecycle or workflow states; error categories; supported units; allowed roles; taxonomic ranks; statutory articles or amendments; treaty signatories, dynasties, or named historical periods; musical modes or key signatures; grammatical cases; classification tiers, official grades, or rankings); the source documents it *as* a list a reader could count; or a reader would reasonably ask "what are all of them?".

If YES, all four are mandatory: extract the **complete** member list from the authoritative source before writing; record the source URL, the retrieval date (`YYYY-MM-DD`), and the **source member count**; render **every** member as one row in **one** complete table using the source's own spelling; and confirm **source count == Coverage Plan count == table row count**.

**Do not widen the set.** Only what the source lists as a member is a member. A closely related setting, control, or neighbouring concept that *influences* the set is **not** a member of it — naming one as a member is a factual error, and a common one, because the neighbour usually sits on the same source page as the list. Check membership against the source's own list, not against the page it appears on. Genuine neighbours go in "deliberately out of scope" or a "commonly confused with" note.

If the counts disagree, or no source lets you confirm the member count, **stop and ask** — do not submit.

### Omission-justification blocklist (categories, not strings)

Every omission of a trigger artifact must cite the **trigger ID** it answered no to, plus a reason naming something **specific about this topic** that makes the artifact impossible or actively misleading. A reason falling into any category below is **rejected**, and a rejected reason fails the gate exactly as a blank row would.

| # | Rejected category | Why it fails |
|---|---|---|
| B1 | Impossibility asserted without naming the source checked | Reports the author's own ignorance as a property of the subject. Name the source read and what it did not contain. |
| B2 | Something else already carries it (an analogy, "it is in the prose") | An analogy cannot enumerate a set or state a real quantity, and prose cannot replace a required artifact. If it truly exists elsewhere, name the sub-heading holding it — then it is not an omission. |
| B3 | The artifact would have to be invented | Fails whenever the source in fact holds a real one — a real ratio, ruling, measurement, or procedure. If a reader genuinely never produces such a thing, say what they do **instead**. |
| B4 | "This subject has nothing selectable or variable", unproven | Fails unless demonstrated: say which source was checked for quantities, thresholds, grades, or permitted values, and what it stated. |
| B5 | Any reason about the author's own convenience — effort, time, uncertainty, length | The requirement is about the subject, never about the author. |
| B6 | Catch-all: boilerplate | Any reason that would read **identically** in a note on a completely different topic is boilerplate, and boilerplate is rejected. |

### Scaffolding survival manifest

Exactly **three** scaffolding comment blocks may remain in a finished topic note: **Coverage Plan**, **Adaptation Note**, **Final Self-Audit** — each filled in, each still inside an HTML comment. Every other scaffolding block must be **deleted outright**, not trimmed or summarised: the template header and its requirements list, the authoring phases, the "how to measure" recipes, the worked micro-example, the suggested sections menu, the voice and prose-quality illustrations, the source-hygiene guidance block, the survival manifest itself, and the version history. A `## Version History` heading must not appear in a finished note.

---

## Suggested sections (menu, not mandate)

A menu, not a running order. The author chooses **which** sections to include and **in what order**, and records a one-line, topic-specific reason in an **Adaptation Note** for each menu section it omits. "Not needed" is not an acceptable reason — say what about *this* topic made the section unhelpful, and expect the reason to be tested against categories B1–B6. **Where a T1–T11 trigger fired, the matching entry is not optional.**

| Section | Earns its place when | Skip when |
|---|---|---|
| **TL;DR** | The reader benefits from knowing up front what this is, why it matters, and the one thing to remember. | The note is short enough that the summary would restate the body. |
| **Plain-language opening (ELI5)** | The concept is abstract or counter-intuitive and a good everyday analogy exists; map it onto the mechanism piece by piece, then say where the analogy stops being true. | The topic is already concrete and mechanical, so an analogy adds indirection instead of removing it. |
| **Learning objectives** | The topic is assessed, or the reader gains from knowing what they should be able to *do* afterwards. Use action verbs. | It is a short supporting or background topic. |
| **Visual overview / diagrams** | There is a flow, life cycle, succession or classification tree, timeline, cross-section, decision branch, or before/after state worth seeing. Each diagram gets a domain-specific title and a caption saying what to learn from it. | The topic is purely definitional and the diagram would be boxes containing the prose's own words. |
| **Main explanation** (domain-named sub-headings) | Always — this is the note. Break it into as many `### [Domain Concept]` sub-headings as the topic genuinely has. | Never. |
| **Deep dive** | One mechanism is far harder or more consequential than the rest and deserves slow treatment on its own. | The topic has no single hard centre, or the depth already sits naturally in the main explanation. |
| **Trade-offs / alternatives** | A practitioner has a real choice, or a competing approach will be encountered. Say what each option costs and buys. | There is genuinely only one way to do the thing. |
| **Where it appears in the real world** | Naming concrete instances makes the concept findable — a named place, institution, documented case, published edition or ruling, or a tool or entry point. | The topic is a pure fundamental with no concrete surface, or specifics would date the note badly. |
| **Key parameters table** | The topic has settings, quantities, thresholds, grades, or proportions a reader chooses, each with a concrete decision rule — a number, threshold, or explicit condition. | The source states nothing selectable — omit the section rather than write an empty table. |
| **Worked example** | Following one realistic scenario end to end teaches more than describing the steps abstractly. | The topic is definitional, or the example would re-narrate the explanation. |
| **Concrete example of the artifact** | There is something concrete the reader would actually produce or follow — a numbered step sequence, a dosage or ratio calculation, a citation format, a filled-in form, a piece of code or configuration. If it is code or configuration it must also be syntactically valid. | The reader never produces or follows anything concrete here, so the artifact would be invented for its own sake. |
| **Common pitfalls & misconceptions** | Readers reliably get this wrong; say why the wrong intuition is tempting, then give the correct mental model as a rule. | The topic has no established failure modes. |
| **Key definitions** | The topic introduces terms the reader will meet again, defined as used *here*. | Everything was already defined plainly inline and a table would only repeat it. |
| **Summary / quick recall** | The reader will want a fast scan before a test or a meeting; each line states a fact or rule, not a topic label. | The note is short and the TL;DR already does this job. |
| **Self-check questions** | The topic is assessed or has decisions worth rehearsing. | It is a background note carrying no decisions. |
| **Further reading** | Authoritative official sources exist. | No official source exists, which is rare. |

If the topic needs a section this menu does not list — an evolution history, a glossary of confusingly-similar names, a troubleshooting flow — write it, and name it after what it contains.

---

## Gate — topic note

Run for `NN-<slug>.md` and any unrecognised filename. Outcome-based: judge whether the effect was achieved, not whether a count was hit. Rows G8, G9, G10, and G11 are **two-sided** — they fail both when something present is wrong *and* when something required is absent. "There are none" is never by itself a pass for a two-sided row. Every row needs **evidence**: a measured number, a name, or a location. A tick with no evidence is a failed row.

- [ ] **G1 — Coverage:** a Coverage Plan enumerating the topic's sub-concepts exists, and every sub-concept listed is genuinely explained in the body, each marked with the sub-heading that explains it. *Evidence: n of n mapped.*
- [ ] **G2 — Prose floor:** the explanatory body as a whole reaches at least 800 words of real explanation — no padding, hedging, or restatement inflating it. *Evidence: the counted total.*
- [ ] **G3 — Reading level:** a bright 14-year-old could follow it — short sentences, plain words, one idea at a time. *Evidence: sentences over ~25 words found, split, remaining.*
- [ ] **G4 — Jargon:** every acronym is expanded on first use, and every piece of jargon is defined inline in plain words on first use. *Evidence: found / fixed counts.*
- [ ] **G5 — Prose-first:** the explanation is carried by prose paragraphs; lists appear only for genuine enumerations. *Evidence: paragraph count vs explanation-list count.*
- [ ] **G6 — Headings:** every sub-heading is named after a real domain concept — no generic headings.
- [ ] **G7 — Trigger completeness:** the Adaptation Note records an explicit yes or no for **every one** of the eleven triggers **T1–T11**, none skipped, and every "yes" names the section that satisfies it. *Evidence: triggers answered n of 11; yes n, each naming a section n of n; no n.*
- [ ] **G8 — Artifacts, two-sided:** every artifact **present** (diagram, table, worked example, concrete artifact or snippet) earns its place and has prose around it saying what to take away, **and** every artifact **required** by a trigger answered yes is actually delivered. Triggers fired must equal artifacts delivered. **A note containing zero artifacts FAILS unless every one of T1–T11 is a no whose reason survives G10.** *Evidence: present per kind; triggers fired n, delivered n (must be equal).*
- [ ] **G9 — Enumerable-set completeness, two-sided:** state whether the topic's subject is a closed enumerable set. If **yes**, the note records the source, the retrieval date, and the **source member count**, renders one table row per member using the source's own spelling, and **source count == Coverage Plan count == table row count**. Any mismatch, or a member count that cannot be confirmed from a source, is a **FAIL**. Also confirm **no member was added that the source does not list as a member** — a related or influencing item is not a set member. If **no**, the note must say in one line why this subject has no finite member list. *Evidence: yes/no; if yes, the three counts plus source and date.*
- [ ] **G10 — Omission reasons:** every omitted trigger artifact cites its trigger ID and gives a reason specific to **this** topic that survives the blocklist categories B1–B6 above. A reason in any blocklisted category, or one that would read identically in a note on a completely different topic, is a **FAIL**. *Evidence: omissions n; each citing a T-number n of n; reasons rejected and rewritten n.*
- [ ] **G11 — Source fidelity, two-sided:** every exact proper name, designation, term of art, or identifier is spelled as the source spells it, **and** every quantity, date, threshold, limit, unit, range, and closed set of permitted values the source states for this topic is present in the note. No analogy stands in for a real name, a real number, or a set. **Every subject has names and stated values, so this row is never satisfied by a bare "N/A" — it requires counts.** *Evidence: names checked against the source n, mismatches fixed n; source-stated values n, present in note n; untraceable facts dropped n (must be 0).*
- [ ] **G12 — Scaffolding survival:** exactly the three surviving blocks remain — Coverage Plan, Adaptation Note, Final Self-Audit — each filled in, and **no non-surviving block leaked** (template header and requirements list, authoring phases, how-to-measure recipes, worked micro-example, sections menu, voice illustrations, source-hygiene guidance block, the survival manifest itself, version history). No `## Version History` heading appears.
- [ ] **G13 — Parameter tables (quality side of G8):** any parameters table present gives actionable decision rules — a threshold, number, or explicit condition — not a restatement of the parameter name. Whether one is *required* is decided by G8 via T2.
- [ ] **G14 — Concrete artifacts (quality side of G8):** any concrete artifact present is introduced by naming the real problem it solves; if it is code or configuration, it is syntactically valid for its language. Whether one is *required* is decided by G8 via T5.
- [ ] **G15 — Self-check answers (quality side of G8):** any self-check answer present explains why the correct answer is right **and** why the most tempting wrong answers fail. Whether they are *required* is decided by G8 via T10.
- [ ] **G16 — Links:** every external link is official documentation, fetched live, formatted with a `*verified YYYY-MM-DD*` date.
- [ ] **G17 — Nothing invented:** no made-up names, designations, figures, quantities, quotes, or URLs; every name and number traces to a source actually retrieved.
- [ ] **G18 — No placeholders:** zero `TODO` / `TBD` / `STUB` / placeholder / leftover bracket markers remain.

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
- [ ] No template scaffolding leaked — no authoring instructions, phase blocks, menus, audit tables, or `## Version History` heading
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
- [ ] No template scaffolding leaked — no authoring instructions, phase blocks, menus, audit tables, or `## Version History` heading
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
- [ ] No template scaffolding leaked — no authoring instructions, phase blocks, menus, audit tables, or `## Version History` heading
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
- [ ] No template scaffolding leaked — no authoring instructions, phase blocks, menus, audit tables, or `## Version History` heading
- [ ] Zero `TODO` / `TBD` / `STUB` / placeholder markers remain

---

## Deterministic checks

Run these mechanically before the gate is declared PASS. Keyed by artifact type. The `Audit row` column maps each check to the numbered row of the topic-note template's 15-row Final Self-Audit, so the two never drift apart.

| Check | Applies to | Audit row | How |
|---|---|---|---|
| Coverage Plan reconciliation | topic note | 1 | Read the Coverage Plan back out of the file and confirm each enumerated sub-concept maps to a named section of the body, and each mapped row names its location. Record `n of n mapped`. |
| Prose floor | topic note | 2 | Word-count the explanatory body — excluding the metadata line, HTML comments, fenced blocks, tables, list items, and the link list — and compare against 800. Under the floor is a hard fail; padding to clear it is also a fail. |
| Long-sentence scan | all | 3 | Count sentences over about 25 words. Split each into one idea per sentence; record found / split / remaining. |
| Unexpanded acronyms | all | 4 | Scan for all-caps tokens of two or more letters and confirm each has an expansion earlier in the file than its first bare use. |
| Undefined jargon | all | 5 | Mark every term a 14-year-old would not know and confirm a plain-words definition sits in that sentence or the next. Record marked / fixed. |
| Prose-to-list ratio | all | 6 | Count explanatory paragraphs `P` and explanation lists `L` (excluding the link list, parameters and definitions tables, checklists, compared options, and self-check questions). `L = 0` or `P >= 3 x L` passes; otherwise fail. Any list whose items *are* the explanation of a mechanism fails at any ratio. |
| Generic headings | all | 7 | Grep the headings for generic labels ("Overview", "Key Concepts", "How does it work", "Considerations", "Introduction"). Must be zero. |
| Artifact delivery, two-sided | topic note | 8 | Count artifacts present by kind and confirm each has explanatory prose around it. Then count triggers answered yes in the Adaptation Note and count how many of those artifacts are in the body. **The two numbers must be equal.** Zero artifacts passes only when zero triggers fired. |
| Omission-reason blocklist | topic note | 9 | For each omission, confirm it cites a trigger ID and test its reason against categories B1–B6. Any match, or a reason that would read identically for a different topic, blocks the write. |
| Residual placeholder markers | all | 10 | Grep for `TODO`, `TBD`, `STUB`, `FIXME`, and unfilled `[bracket]` template markers. Must be zero outside surviving scaffolding. |
| External URLs live | all | 11 | Re-fetch each external URL; confirm it is reachable, official, carries a `*verified YYYY-MM-DD*` date, and that its content matches the citation title and claim. |
| Traceability | all | 12 | Confirm every name, quantity, date, and limit traces to a source actually retrieved. Untraceable facts must be dropped; the untraceable count must be 0. |
| Enumerable-set counts | topic note | 13 | Read the Coverage Plan's enumerable-set answer. If yes: confirm a source URL and retrieval date are recorded, read off the source member count, count the Coverage Plan members, count the table rows, and confirm **all three are equal**. Then check each rendered row against the source's own list and reject any row for an item the source does not list as a member. An unconfirmable count is a fail. If no: confirm a one-line reason is recorded. |
| Source fidelity counts | all | 14 | Count the exact proper names, designations, and terms of art used and check each character by character against the source; count the quantities, dates, thresholds, limits, units, and permitted-value sets the source states and how many appear in the note. Record both pairs of numbers. A bare "N/A" is not an acceptable value. |
| Trigger answers complete | topic note | 15 | Count explicit yes/no answers in the Adaptation Note. Must be 11 of 11. Every yes must name a section; every no must carry a non-blocklisted reason. |
| Scaffolding leak | topic note | — | Confirm exactly three surviving comment blocks (Coverage Plan, Adaptation Note, Final Self-Audit) and grep for any non-surviving block marker (authoring phases, how-to-measure recipes, worked micro-example, sections menu, voice illustrations, survival manifest, version history). Also grep for a `## Version History` heading. Any hit is a fail. |
| Speaker labels | podcast | — | Confirm speaker-label lines are present, that exactly the same two labels are used throughout, and that both are generic role labels. |
| Zero code fences | podcast | — | Count fenced code blocks. Must be zero. |
| Siblings non-stub | intro, podcast | — | Read every sibling topic note in the chapter and confirm none is still a stub or partially authored. |
| Relative links resolve | intro, podcast | — | For every relative link, confirm the target file exists on disk. |

Any failing check blocks the write. Fix it, then re-run the whole gate — not just the failing row.
