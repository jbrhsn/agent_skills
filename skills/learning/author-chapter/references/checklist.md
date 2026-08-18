# Final audit

Run every item against the finished file before delivering. For each failure, fix the file — do not note it as a limitation and move on. Where a check can be done mechanically (searching for a term's first use, counting sections), do it mechanically rather than by impression.

## Coverage

- [ ] Every concept from the inventory has a section in the file. Compare the two lists item by item.
- [ ] All four tiers are present and populated. Tier 0 has at least three concepts; Tier 3 is not thinner than Tier 1.
- [ ] The scratch inventory has been deleted from the file.
- [ ] Nothing is a placeholder: no "TODO", no "similarly for the rest", no "and so on" standing in for content, no section that promises detail it never delivers.

## Per-concept integrity

- [ ] Every concept block opens with the problem, not the definition.
- [ ] Every concept has a worked example with real values, code, or data — not a restated description.
- [ ] Every concept has a named trap written in the learner's voice.
- [ ] Every concept has a stated tradeoff.
- [ ] Every Tier 3 concept names a concrete failure mode with a symptom.
- [ ] Every analogy is bounded — its breaking point is stated.
- [ ] No concept has two competing analogies.

## Vocabulary

- [ ] Take every technical term in the file and find its first occurrence. Each is defined at or before that point, in plain language. This is the check that most often fails; do it properly.
- [ ] No concept is used before its prerequisites are taught. Walk the dependency order.
- [ ] The glossary contains every term defined in the module.
- [ ] Every deliberate simplification ("for now, think of it as...") is paid off later in the document. Search for them.

## Learning scaffolding

- [ ] Every part ends with a checkpoint whose answers are folded in `<details>`.
- [ ] Checkpoint questions require prediction, transfer, or diagnosis — none can be answered by copying the nearest paragraph.
- [ ] Part 3 has real exercises with full worked solutions.
- [ ] Part 4 has case studies drawn from real systems and open-ended design drills.
- [ ] Difficulty climbs without steps; hard transitions are signposted.
- [ ] The Whole Picture section reassembles the material rather than listing the headings again.
- [ ] Spaced Recall lists questions without answers and points back to sections.

## Prose

- [ ] No section opens with "In this section we will..." or similar filler.
- [ ] No reasoning is delivered as bullet points where prose is needed.
- [ ] No hollow intensifiers standing in for evidence.
- [ ] Nothing condescending: nothing is called easy or simple.
- [ ] Second person, present tense, concrete before abstract.

## Mechanics

- [ ] Code blocks are complete, language-tagged, and show their output.
- [ ] Mermaid diagrams are syntactically valid and each is followed by a sentence telling the reader what to look at.
- [ ] Heading levels are consistent and the document outline is navigable.
- [ ] Version-sensitive claims are either verified or flagged as needing a docs check — no invented version numbers, benchmark figures, or dates.
- [ ] Filename is a lowercase hyphenated slug of the topic.

## The final read

Read the Before You Start section, then ask: does the file actually deliver every capability it promised there? If not, fix the file rather than weakening the promise.
