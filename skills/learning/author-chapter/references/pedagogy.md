# Pedagogy

The rules here come from how people actually learn hard material. Each one exists because a specific failure is common without it.

## Give the answer first, then earn it

Withholding the conclusion to build suspense is a device from fiction, and it fails here. A reader who knows where the explanation is going can slot each new piece into a frame that already exists; a reader who doesn't has to hold everything in suspension until the payoff arrives, and most of them stop before it does.

So the chapter opens with its takeaway and each unit opens with its claim. This costs nothing pedagogically — stating a conclusion is not the same as justifying it, and a one-line claim is not yet understood. It only changes what the reader does with the next thousand words.

Then keep teaching problem-first underneath. The order inside a unit is still: here is what goes wrong without this, here is the idea, here is one real instance. The takeaway sits above that structure, it does not replace it.

## Mark the vital few

Not everything in a chapter is equally load-bearing, and pretending otherwise is a failure of teaching, not neutrality. A reader facing twelve equally-weighted units cannot allocate attention, so they either read all of it shallowly or none of it.

Decide which units make the reader functional and put those in the core path. Everything else is real but postponable. Say plainly that finishing the core path is a legitimate stopping point — a reader who is told they may stop is far likelier to come back than one who quit at unit four feeling they failed.

Be honest about the split. If two thirds of the chapter is core, you have not made the judgement, and the reader is back where they started.

## Let the reader stop

People learn this material in short sittings, interrupted, over weeks. A unit is the size of one sitting, so it has to survive being the last thing read for a while.

That means each unit ends somewhere stable — an idea completed, not a cliffhanger — and begins without requiring the previous one to be fresh. Name what you are building on rather than assuming recall: "back when we found that indexes have to be updated on every write" costs six words and saves a reread. Signpost forward at the seams so the reader knows what they are returning for.

## Manage the load, don't reduce the depth

A beginner can hold about three or four new things at once. Depth is not the problem — *simultaneous* novelty is. So:

- Introduce one new idea per block. If a block needs two, split it.
- Reuse a single running example across the whole module wherever possible. A reader who already knows the example can spend all their attention on the new concept rather than re-parsing a new scenario. Introduce it early, name it, and keep returning to it.
- Delay precision when precision costs load. It is fine to say "for now, think of it as X" and then, two sections later, "here is where that picture was incomplete." State plainly when you are doing this, and always come back and pay it off. Never leave a simplification standing at the end of the module.

## Worked examples before independent practice

Beginners learn far more from studying a fully worked solution than from struggling with a problem they lack the tools for. So: mechanics, then a full worked example, then a question they answer themselves — and only once they are off the lower rungs, genuinely open exercises. As the reader climbs the ladder, fade the support: a top-rung drill gives a scenario and a reference answer, not a procedure.

## Retrieval beats rereading

The closing question of a unit is not decoration. A question the reader has to answer from memory does more for retention than a paragraph of summary. Write questions that cannot be answered by pattern-matching the nearest paragraph — ask for prediction ("what happens if..."), for transfer ("where else would this apply"), or for diagnosis ("this is slow, which of these is the likely cause").

This is also why `quizzies.md` ships with its answers blank, and why filling them in would be a disservice rather than a favour.

Fold answers in `<details><summary>Answer</summary>...</details>` so the reader has to choose to look.

## Analogies: one, and bounded

A good analogy maps structure, not vibes. "An index is like the index at the back of a book — it stores where things are, not the things themselves, so it costs space and must be updated when the book changes" maps three properties at once. "An index is like a superpower" maps nothing.

Every analogy is immediately bounded: name one place it breaks. Unbounded analogies are the single largest source of durable misconceptions, because the reader keeps extending them past their range.

Do not stack analogies. Two competing metaphors for one concept leave the reader unsure which to reason with.

## Misconceptions are content, not warnings

The "trap" section exists because learners construct wrong models actively — you cannot prevent that by being clear, only by naming the wrong model and dismantling it. Write the trap in the learner's own voice ("so it just caches everything, right?"), acknowledge why it's a reasonable inference, then show the specific case where it produces a wrong prediction. A concrete counterexample beats a correction.

## The top rung is about judgement, not more facts

Whatever the ladder calls it — Architect, Authority, Designer, Edge — the top rung is never more surface area. It is:

- **Tradeoff fluency.** Every design choice bought something and sold something. Name both sides.
- **Failure prediction.** What breaks first, at what load, with what symptom, and what the misleading symptom is.
- **Alternative literacy.** What else could have been chosen, and the conditions under which it wins. If a topic has no live alternatives, that itself is worth explaining.
- **Cost awareness.** Time, money, memory, operational burden, team knowledge. Solutions have prices beyond correctness.
- **Historical context.** Why the current design carries scars. Most odd behaviour in mature systems is an old constraint fossilised.

If a top-rung unit could be written without knowing any real system, real practitioner, or real attempt, it is not top-rung yet. `domains.md` says what that means in your field — the shape holds everywhere, but "what breaks at scale" is a load figure for infrastructure, a life event for a habit system, and an audience it stops working on for a piece of writing.

## Pacing

Difficulty should climb steadily, never step. If a section requires a leap, insert a bridging paragraph that makes the leap explicit: "This next part is harder. It builds on X and Y, so if either feels shaky, reread section N first."

Signpost transitions between sections: recap what the reader can now do, and state what the next one adds and why it's the natural next thing to want. The seam between the core path and Going deeper is the most important of these — it is where you tell the reader they have arrived somewhere real.

## Honesty

Say when something is genuinely hard. Say when experts disagree. Say when a convention is arbitrary rather than principled — learners waste enormous effort looking for the deep reason behind an accident of history. Say when you are simplifying, and say when you'd check the docs rather than trust memory.
