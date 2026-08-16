# Structures

Skeletons, not templates. Pick the one that matches the piece, then break it
wherever the material calls for something else. A structure followed too visibly
reads as a form filled in.

Section counts assume 1,500–2,500 words. Scale down for shorter pieces by
merging, not by shrinking every section proportionally.

---

## Tutorial / how-to

The reader has a job to do. They will skim to the code, then come back for the
reasoning if the code looks credible.

1. **The problem, concretely.** What broke or what wasn't possible. Two or three
   paragraphs, with the specific conditions — scale, versions, constraints.
2. **Why the obvious approach fails.** This is what separates a real tutorial from
   documentation. Name what was tried first.
3. **The approach.** State it before implementing it, so the reader can decide
   whether to keep going.
4. **Implementation, in stages.** Each stage: what it does, the code, what to
   verify before moving on.
5. **What broke while doing it.** Real errors, real fixes. The most-copied section
   of any tutorial.
6. **Limits.** Where this stops working and what to use instead.
7. **Takeaway.** The decision rule, or the checklist.

## Case study / post-mortem

Strongest format available to a practitioner, because nobody else can write it.

1. **The situation and the stakes.** Numbers up front — scale, cost, latency,
   headcount.
2. **What we did first, and why it was reasonable.** No hindsight smugness. The
   reader is currently making the same call.
3. **How it failed.** Specific symptoms, specific numbers, specific timeline.
4. **Diagnosis.** How the real cause was found — the debugging path, not just the
   conclusion.
5. **The fix, and its cost.** Every fix has a bill. Name it.
6. **Results.** Before and after, measured.
7. **What transfers.** Which parts generalize and which were particular to this
   system.

## Opinion / argument

1. **The claim, in the first hundred words.** No build-up.
2. **What earns the right to make it.** Experience, briefly.
3. **The strongest case for the other side.** Made honestly. Skipping this is why
   most opinion pieces read as noise.
4. **Why it still fails.** Evidence, specifics.
5. **What follows if the claim is right.** Practical consequence.
6. **Where the claim doesn't hold.** Boundaries make an argument credible.

## Explainer

1. **The question, framed as something the reader has hit.** Not "What is X?" but
   the situation where not knowing X hurts.
2. **The short answer**, in a paragraph, for readers who only need that.
3. **The mechanism.** How it actually works, one layer at a time.
4. **A worked example** with real values.
5. **Common misunderstandings**, drawn from real conversations, not invented ones.
6. **When it matters in practice.**

## Experience report

1. **Where things stood.** Situation and constraint.
2. **The decision** and what it was weighed against.
3. **What happened**, chronologically, with the parts that went badly intact.
4. **What surprised you.** The reason to write it at all.
5. **What you'd do differently.**

---

## Mode adjustments

### Writing about writing

The reader is a writer, and the credibility test is whether the piece is itself
well written. Rules tighten, not loosen.

- Every claim needs the writer's own numbers or outcomes attached. Generic craft
  advice is the most saturated category on the platform.
- Avoid prescribing to the reader. Report what worked for the user and let the
  reader extract the rule.
- Steer away from Medium-meta topics — earnings, the algorithm, Boost. Those are
  capped at Network Distribution by policy no matter how good the piece is.

### Personal finance / budgeting

The user is not a licensed advisor. Framing is the whole risk here.

- **Experience only.** What the user did, what it cost, what happened, what they'd
  change. Never what the reader should do.
- Strip prescriptive second person: "you should open a…", "the best account for
  you is…", "invest in…". Rewrite into first-person report.
- No projected returns, no yield promises, no "this will save you X."
- Keep specific numbers — they are the value — but attach them to the user's own
  situation, with the context that makes them non-transferable.
- Name jurisdiction and date when tax, rates, or products are involved. These go
  stale and vary by country.
- No product recommendations or affiliate framing. Medium treats unverified
  financial claims as a rules violation.

A useful test: could a reader lose money by following this piece as instructions?
If yes, the framing is wrong, not the content.
