# Final audit

Run the universal section always. Then run the section for your domain and, if you are filling a scaffolded file, the one for that file type. Skip the rest — a check that does not apply to your field is worse than no check, because forcing it distorts the chapter.

Where a check can be done mechanically — searching for a term's first use, comparing two lists, counting rungs — do it mechanically rather than by impression. Audit in passes over sections; do not try to hold the whole file at once. Fix every failure in the file rather than reporting it as a limitation.

## Completeness — run first, and take it seriously

This is measured against the assignment, never against length.

- [ ] Every topic in the brief has been covered. Compare the two lists item by item, by name.
- [ ] Each topic is covered at the `depth` it was briefed for — not deeper, not thinner. A topic briefed for awareness does not get four units; one briefed for working command does not get a paragraph.
- [ ] Everything under each topic's `covers` appears somewhere in the file.
- [ ] Every rung on the ladder in the frontmatter is reached by at least one unit, and the rung names are used **verbatim** — no relabelling, no assuming four when there are three.
- [ ] The chapter delivers its stated `purpose`. Read the purpose line, then ask whether the file actually does that.
- [ ] Nothing is assumed that `builds_on` does not grant, and everything `enables` promises is set up.
- [ ] No placeholders: no "TODO", no "and so on", no "similarly for the rest", no section promising detail it never gives.
- [ ] The scratch inventory or working notes are not in the delivered file.
- [ ] In a scaffolded file: the frontmatter and `## Brief` block survive intact, `status` is `drafted`, and none of the stub's HTML-comment prompts or empty `**Scope here:**` lines remain.

## Universal

**Shape**

- [ ] The chapter opens with the one-minute takeaway, before any framing, in plain language.
- [ ] The mental model is present: one analogy, bounded, plus the connection to what came before.
- [ ] The core path is marked, and one line states that stopping at its end is a legitimate finish.
- [ ] The core/deeper split is discriminating — not everything is core.
- [ ] Every unit opens with a one-line bold takeaway that states its claim.
- [ ] Units carry a read-time estimate, and a contents block exists if the chapter runs past ~8 units.
- [ ] Each unit is self-contained enough to stop after.

**Per unit**

- [ ] Answers why it exists before how it works.
- [ ] Shows one real, specific, attributable thing, walked through with intermediate state visible.
- [ ] Names a trap in the learner's own voice, with a concrete counterexample.
- [ ] Names what the choice cost and what the alternative is.
- [ ] Ends with a question requiring prediction, transfer, or diagnosis — never recall of the nearest paragraph — with the answer folded in `<details>`.
- [ ] The obligations are answered, not printed as labels.

**Vocabulary**

- [ ] Take every term of art in the file and find its first occurrence. Each is defined at or before that point, in plain language. This is the check that most often fails; do it properly.
- [ ] Nothing is used before what it depends on is taught. Walk the order.
- [ ] Every deliberate simplification ("for now, think of it as…") is paid off later. Search for them.
- [ ] The glossary contains every term the chapter defined.

**Sourcing**

- [ ] If a search tool was available, it was used — at least once for the chapter and once per volatile topic.
- [ ] Every version number, price, limit, benchmark figure, date, and "what practitioners now do" claim is either sourced or explicitly flagged as unverified. No invented specifics.
- [ ] `## Sources` lists what was actually read, with dates and what each supports — not a reading list.
- [ ] If no search tool was available, the file says so in one line.

**Prose**

- [ ] No filler openers ("In this section we will explore…").
- [ ] No reasoning delivered as bullet points where prose is needed.
- [ ] No hollow intensifiers standing in for evidence.
- [ ] Nothing condescending, and nothing called easy or simple.
- [ ] Second person, present tense, concrete before abstract.
- [ ] No analogy left unbounded, and no unit carrying two competing analogies.

**Closing and mechanics**

- [ ] The whole picture reassembles the material rather than relisting headings.
- [ ] Spaced recall gives questions without answers, grouped by rung, pointing back at units.
- [ ] Heading levels are consistent and the outline is navigable.
- [ ] Mermaid diagrams are valid, and each is followed by a sentence saying what to look at.

## By domain

**`technical`**

- [ ] Code blocks are complete, language-tagged, and show their output.
- [ ] Numbers are derived where derivable, not just quoted; quoted benchmarks name hardware and version.
- [ ] Top-rung units name what breaks, at what scale, with what symptom — and the misleading symptom that shows first.
- [ ] No tutorial happy-path presented as the whole story.

**`craft`**

- [ ] Specimens are quoted and taken apart, not paraphrased or described.
- [ ] At least one before/after revision with every edit named.
- [ ] No grading by adjective — effects on the reader are stated concretely.
- [ ] Where practitioners genuinely disagree, both camps get their strongest case.

**`practice`**

- [ ] Examples are logged periods with what actually broke, not systems described only in their working state.
- [ ] Research is cited with its real limits stated; anecdote is labelled as anecdote.
- [ ] No outcome promised on a timeline.
- [ ] Top-rung units name where the system fails for someone with different constraints, and the recovery path.

**`exam`**

- [ ] Worked examples use the exam's real format and phrasing, with distractor elimination shown.
- [ ] Format and mark scheme are verified against the official source, or flagged as unverified.
- [ ] Anything beyond the syllabus is marked out of scope.

## By file type

Only for scaffolded files other than `learning.md`. The refusals are the point — see `file-types.md`.

- [ ] `quizzies.md`: questions only. Answer and verification slots left empty. No question answerable by pattern-matching a paragraph in `learning.md`.
- [ ] `practice.md`: tasks and success criteria only. No solutions. The learner's log slots left empty.
- [ ] `thought_leadership.md`: no invented evidence; each angle names what would be needed to publish it. No angle that merely restates the documentation.
- [ ] `examples.md`: specimens are real and attributed. The annotation slot is left empty.
- [ ] `interview.md`: model answers are spoken answers, not essays. Every question has its follow-up.

## The final read

Read the one-minute takeaway, then ask whether the chapter actually delivers what it promised there. If not, fix the file rather than weakening the promise.
