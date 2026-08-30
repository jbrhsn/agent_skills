# Voice

Read this before writing, not during the audit. Voice is not a polish pass; it is
a set of decisions made in the first paragraph and held for 2,000 words.

The target is not "good writing." It is prose that reads as though a specific
engineer sat down and explained a specific thing they did. Fluent, well-organized,
faultlessly balanced prose is exactly what a Medium editor rejects on sight.

---

## Where voice comes from

**The source file is the style guide.** Extracting the register is its own step —
see `voice-inference.md`, read at workflow step 1, which covers the signals, the
voice card, and the calibration checks. In short: note how the user actually
writes — sentence length, whether they swear, whether they use contractions,
whether they hedge or state flatly, what they find funny. Match it. If `source.md`
is terse and profane, the article is terse and profane.

**Keep their sentences.** When a line in `source.md` says the thing well, use it
verbatim. Do not "improve" it into neutrality. A slightly awkward sentence in the
writer's own cadence beats a smooth one in nobody's.

**Keep the opinions sharp.** If the source says a tool is bad, the article says
the tool is bad. Do not soften into "may not be the right fit for every team."
Balance is not the same as hedging, and hedging reads as machine output.

**Specificity carries voice.** "It took three days" is a voice. "This process can
be time-consuming" is an absence of one.

---

## Banned phrasings

Not stylistic preferences. These are the strings editors search for.

**Vocabulary:** delve, unlock, harness, leverage (as a verb), robust, seamless,
seamlessly, elevate, empower, navigate (figuratively), realm, landscape (as in
"the AI landscape"), tapestry, testament, crucial, vital, pivotal, game-changer,
revolutionize, cutting-edge, state-of-the-art, foster, underscore, myriad,
plethora, embark, journey (figuratively), dive deep, deep dive as a noun in the
body text.

**Openers:** "In today's fast-paced world", "In the ever-evolving landscape of",
"Have you ever wondered", "Picture this", "Let's face it", "We've all been there",
"In an era where", "As technology continues to advance."

**Connectives:** "Moreover", "Furthermore", "Additionally" at the head of a
paragraph, "It's worth noting that", "It's important to remember that",
"That said" used more than once, "At the end of the day."

**Closers:** (the article still needs a real ending — see `closing-and-cta.md`)
"In conclusion", "To sum up", "The bottom line is", "Only time will
tell", "One thing is certain", "The future of X is bright", "Happy coding!",
"What are your thoughts? Let me know in the comments."

**Constructions:**

- `It's not X — it's Y.` And its relatives: `This isn't just X. It's Y.`
- `X isn't about A. It's about B.`
- The three-item parallel list where all three items are the same length and
  grammatical shape. One tricolon in an article is rhetoric; four is a tell.
- The rhetorical question as a section transition. `So what does this mean for
  your pipeline?`
- `Here's the thing:` / `Here's the kicker:` / `But here's where it gets
  interesting:`
- Em-dash used more than roughly twice per thousand words.
- The single-sentence dramatic paragraph deployed for emphasis more than once or
  twice in a piece. It works. It stops working when every fourth paragraph does it.
- Section headers that read like prompt instructions: "Understanding the
  Fundamentals", "Key Takeaways", "Best Practices", "Common Pitfalls", "Why This
  Matters", "Final Thoughts".

**Layout:** the bolded-lead bullet stack (`**Scalability:** The system scales
well.`) repeated down the page. If content genuinely enumerates, use a plain list
or write it as prose.

---

## Rhythm

Uniform sentence length is the most reliable machine signature and the hardest to
notice while writing.

Deliberately break it. A three-word sentence after a thirty-word one. A fragment.
A sentence that runs long because the thought is genuinely complicated and
chopping it would falsify the idea. Then a short one to land it.

The same applies to paragraphs. Mostly one to three sentences, but not
mechanically — a five-sentence paragraph is fine when one idea genuinely needs
the room, and the variation is what makes the short ones land.

Read the draft aloud mentally. If it has the cadence of a well-formatted report,
rewrite the affected sections. Swapping individual banned words out of
machine-rhythm prose does not fix it; it produces machine-rhythm prose with an
unusual vocabulary.

---

## Technical register

For the data engineering and AI pieces, which is most of them:

- Assume the reader knows what a DAG, an embedding, and a container are. Do not
  define the basics. Do define anything genuinely niche, in a clause, once.
- Name versions. "Spark 3.5", not "recent versions of Spark."
- Show real output — actual error text, actual query plans, actual numbers — over
  described output.
- Numbers over adjectives. "Cut p99 from 1.4s to 310ms", not "significantly
  faster."
- Explain the tradeoff, not just the choice. Any senior reader's first question is
  what it cost.
- Do not sell. The reader is evaluating whether the approach applies to their
  system, not being persuaded.

---

## Last check

Before presenting, scan for the tells above. Three or more means the voice pass
failed. Rewrite the affected sections rather than substituting words.

Then run the calibration checks in `voice-inference.md`. The one that decides it:
would a reader who knows the user recognize this as theirs?
If the honest answer is "it reads like a competent article about the topic," it
is not finished.
