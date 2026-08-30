# Voice inference

Read this at workflow step 1, before the brief. It covers where the voice comes
from and how to hold it. `voice-and-antislop.md` covers what to keep out of the
prose. Both get read before drafting; this one first.

`source.md` is unpolished, which is what makes it the most honest sample of how
the user actually writes available anywhere. Mine it. The transformation this
skill performs is structural — reorganize the material, don't relocate the voice.

The Medium-specific problem is duration. A LinkedIn post is short enough that a
voice survives on inertia. Two thousand words does not: the register set in
paragraph three drifts toward neutral competence by paragraph forty, and the
drift is invisible while writing. That is why the card below exists, and why the
sustained-register check is at the end.

---

## Signals to extract

Read `source.md` for these specifically, before writing anything else.

**Formality.** Contractions present or absent? Slang, profanity, casual asides?
Someone who writes "yeah, this fell over immediately" and someone who writes "the
deployment failed during initialization" need different articles.

**Technical density.** Are domain terms used bare or explained on first use? This
reveals the assumed reader. Preserve the level. Flattening jargon insults the
actual audience; inflating it loses them.

**Sentence rhythm.** Long and clause-heavy, or clipped and declarative? The most
transferable signal, and the first thing lost in editing.

**Stance.** Confident and declarative, or hedged and exploratory? Someone who
wrote "I think this might be why" should not be published saying "This is exactly
why."

**Humor.** Present at all? Dry, self-deprecating, profane, absent? If it is
absent from the source, do not add any.

**First-person posture.** "I built" vs "we built" vs impersonal description.
Match it. Turning a solo project into "we" or a team effort into "I" is a
credibility problem, not a style choice.

**Idiosyncrasies.** Recurring phrases, an odd word used twice, a particular way
of framing a problem, how they swear, what they find funny. Highest-value things
in the file. When choosing between the user's odd word and a smoother synonym,
keep the odd word.

**Dictated sources.** If `source.md` reads as dictation — false starts,
run-ons, "so basically", "anyway" — the spoken rhythm is still the voice signal.
Keep the cadence and the word choices; drop only the disfluencies. Dictation
tends to carry the strongest voice in the folder.

## The voice card

Write these six lines before drafting and copy them into `medium_brief.md`. They
take a minute and they are what the sustained-register check is checked against.

- **Formality:** contractions? profanity? asides?
- **Stance:** flat assertion / hedged / somewhere between
- **Rhythm:** typical sentence length and whether it varies
- **Humor:** kind, or none
- **Posture:** I / we / impersonal
- **Keep verbatim:** the three to six lines from `source.md` that go in untouched

The last line matters most. Pick the sentences where the user said the thing
better than a rewrite would, and commit to shipping them as written. Not marked,
not set apart, not "improved" into neutrality. A slightly awkward sentence in the
writer's cadence beats a smooth one in nobody's.

## What to change

Structure, order, and compression are the actual work:

- Reorder so the piece earns the click in the first three paragraphs.
- Cut tangents and anything not serving the angle — subject to the omission rule
  in `SKILL.md`; experience does not get cut on your own authority.
- Tighten rambling sentences **without changing their register.**
- Fix genuine errors.
- Add connective tissue where the source jumped.

## What to preserve

- Vocabulary level and specific word choices.
- Sentence rhythm and typical length.
- Confidence level, including hedges where they are real.
- Humor, or its absence.
- Concrete details: tool names, versions, numbers, timestamps, error strings.
- Every strong opinion. If the source says a tool is bad, the article says the
  tool is bad. Softening into "may not be the right fit for every team" is the
  most common way a good piece is ruined, and hedging reads as machine output.

## Thin sources

Some `source.md` files are five bullets with no voice signal at all. Then:

- Default to plain, direct, technically literate prose — a competent practitioner
  explaining something to a peer. Not motivational, not corporate, not breezy.
- Do not invent personality, backstory, or anecdote to fill the gap.
- Say plainly in the response that the source was thin on voice signal, and offer
  to revise if the register is wrong.

A thin source is also a signal that the gap interview at step 2 should be run
rather than skipped.

---

## Calibration checks

Run all five at the self-audit. The first two are the ones in `SKILL.md`; the
rest catch what they miss.

1. **Substitution test.** Could this have been written by any of a hundred other
   people in this field? If yes, the voice got sanded off.
2. **Reverse test.** If the user read this cold, would they recognize it as
   theirs?
3. **Sustained-register check.** Read the last quarter of the article against the
   voice card, then against the first quarter. If the ending is more formal, more
   balanced, or more evenly cadenced than the opening, the voice drifted. Rewrite
   the tail; do not patch words into it.
4. **Escalation check.** Did the draft make any claim more confident than
   `source.md` made it? Walk it back to the source's level.
5. **Vocabulary check.** Does the article contain words the user never uses?
   Replace them with words from the source. Check that every line on the "keep
   verbatim" list actually survived into the file.
