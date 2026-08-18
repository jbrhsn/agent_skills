# Pedagogy

The rules here come from how people actually learn hard material. Each one exists because a specific failure is common without it.

## Manage the load, don't reduce the depth

A beginner can hold about three or four new things at once. Depth is not the problem — *simultaneous* novelty is. So:

- Introduce one new idea per block. If a block needs two, split it.
- Reuse a single running example across the whole module wherever possible. A reader who already knows the example can spend all their attention on the new concept rather than re-parsing a new scenario. Introduce it early, name it, and keep returning to it.
- Delay precision when precision costs load. It is fine to say "for now, think of it as X" and then, two sections later, "here is where that picture was incomplete." State plainly when you are doing this, and always come back and pay it off. Never leave a simplification standing at the end of the module.

## Worked examples before independent practice

Beginners learn far more from studying a fully worked solution than from struggling with a problem they lack the tools for. So: mechanics, then a full worked example, then a checkpoint question, and only in Part 3 onward genuine open exercises. As the reader climbs the tiers, fade the support — Tier 3 drills should give a scenario and a reference answer, not a procedure.

## Retrieval beats rereading

Checkpoints are not decoration. A question the reader has to answer from memory does more for retention than a paragraph of summary. Write checkpoint questions that cannot be answered by pattern-matching the nearest paragraph — ask for prediction ("what happens if..."), for transfer ("where else would this apply"), or for diagnosis ("this system is slow, which of these is the likely cause").

Fold answers in `<details><summary>Answer</summary>...</details>` so the reader has to choose to look.

## Analogies: one, and bounded

A good analogy maps structure, not vibes. "An index is like the index at the back of a book — it stores where things are, not the things themselves, so it costs space and must be updated when the book changes" maps three properties at once. "An index is like a superpower" maps nothing.

Every analogy is immediately bounded: name one place it breaks. Unbounded analogies are the single largest source of durable misconceptions, because the reader keeps extending them past their range.

Do not stack analogies. Two competing metaphors for one concept leave the reader unsure which to reason with.

## Misconceptions are content, not warnings

The "trap" section exists because learners construct wrong models actively — you cannot prevent that by being clear, only by naming the wrong model and dismantling it. Write the trap in the learner's own voice ("so it just caches everything, right?"), acknowledge why it's a reasonable inference, then show the specific case where it produces a wrong prediction. A concrete counterexample beats a correction.

## The architect tier is about judgement, not more facts

What separates a practitioner from an architect is not extra API surface. It is:

- **Tradeoff fluency.** Every design choice bought something and sold something. Name both sides.
- **Failure prediction.** What breaks first, at what load, with what symptom, and what the misleading symptom is.
- **Alternative literacy.** What else could have been chosen, and the conditions under which it wins. If a topic has no live alternatives, that itself is worth explaining.
- **Cost awareness.** Time, money, memory, operational burden, team knowledge. Solutions have prices beyond correctness.
- **Historical context.** Why the current design carries scars. Most odd behaviour in mature systems is an old constraint fossilised.

If a Tier 3 section could be written without knowing any real system, it is not Tier 3 yet.

## Pacing

Difficulty should climb steadily, never step. If a section requires a leap, insert a bridging paragraph that makes the leap explicit: "This next part is harder. It builds on X and Y, so if either feels shaky, reread section N first."

Signpost transitions between parts: recap what the reader can now do, and state what the next part adds and why it's the natural next thing to want.

## Honesty

Say when something is genuinely hard. Say when experts disagree. Say when a convention is arbitrary rather than principled — learners waste enormous effort looking for the deep reason behind an accident of history. Say when you are simplifying, and say when you'd check the docs rather than trust memory.
