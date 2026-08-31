# Domains

The unit obligations in `structure.md` are the same everywhere. What changes between domains is how you *satisfy* them — above all "show me one," which is the obligation most often botched by importing another field's idea of evidence.

These are not templates. Nothing here is a heading to copy. Each pack answers four questions: what counts as evidence, what a worked example looks like, what the top rung actually means, and what to never do.

Pick the pack matching the `profile` in the file's frontmatter. Standalone, infer it from the topic. When a chapter genuinely straddles two — "writing technical documentation" is craft and technical at once — take the evidence standard from the stricter one and the worked-example form from the one the reader will actually be doing.

## `technical` — programming, data, infrastructure, ML

**Evidence:** running code, measured numbers, a documented incident, a spec or RFC. A derivation the reader can reproduce with a pen beats a cited figure, because it teaches the model as well as the fact.

**A worked example is:** real values traced step by step with intermediate state shown. Code is complete, language-tagged, and shows its output. If you quote a benchmark, say the hardware and the version.

**Top rung means:** you can predict what breaks, at what scale, with what symptom — and which misleading symptom shows up first. Plus what you'd choose instead and the conditions under which it wins. A top-rung unit that could be written without knowing a real system isn't top-rung yet.

**Never:** invent version numbers, benchmark figures, or dates. Never present a tutorial happy-path as the whole story. Never let "best practice" stand without naming who says so and what it costs.

## `craft` — writing, blogging, design, speaking

**Evidence:** published work by named people, before/after revisions, and the reader's own reaction traced back to a specific choice on the page.

**A worked example is:** a real passage or artefact, quoted, then taken apart line by line — this word rather than that one, and what changes for the reader. Rewriting a weak version into a strong one and naming every edit teaches far more than describing the principle. Show the artefact; never paraphrase it.

**Top rung means:** you make choices that break the standard form on purpose, and can say what the form was protecting and why you can afford to lose it here. Judgement about audience, not more technique.

**Never:** grade with adjectives. "Powerful opening" teaches nothing — say what it does to the reader and how. Never present taste as rule; where practitioners genuinely disagree, say so and give both camps their strongest case. Never use a technical worked example as a stand-in for a craft one.

## `practice` — productivity, habits, fitness, money, health

**Evidence:** a logged period with real numbers, a named study with its actual limits stated, or a system someone ran for long enough to hit its failure mode. Anecdote is admissible if labelled as anecdote.

**A worked example is:** a specific week or month, with what was planned, what actually happened, and where it broke. The friction is the content. A system described only in its working state teaches nothing, because every system works on day three.

**Top rung means:** you can design a system for someone whose constraints differ from yours, and name in advance where it will fail for them — the life event, the schedule change, the motivation dip — and what the recovery path is.

**Never:** promise outcomes on a timeline. Never present research as more settled than it is — this field's literature is genuinely weak in places, and saying so is part of teaching it. Never write a unit whose advice assumes the reader's day already works.

## `exam` — certifications, licensing, academic exams

**Evidence:** the published syllabus, the official question format, released past papers, and the examiner's own wording.

**A worked example is:** a question in the exam's real format, worked through as you would under time — including how you eliminate distractors and where the clock actually goes. Mark the trap the question was built around.

**Top rung means:** you recognise the question type from its shape and know what it's testing before you finish reading it, including the boundary cases examiners reuse.

**Never:** teach beyond the syllabus without flagging it as out of scope — attention here is the scarce resource. Never invent the format or the mark scheme; if you cannot verify them, say so and point at the official source. Never optimise for elegance over the mark scheme.

## Anything else

For a `custom` profile, or standalone on a topic that fits none of the four, answer the same four questions explicitly before you write, and hold yourself to the answers. The general rule underneath all four packs: **evidence is whatever a practitioner in this field would accept from a stranger.** Ask what that is, and meet it.
