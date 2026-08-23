# Structure and Format

How the body is built, shaped, and de-slopped. Read this at workflow step 4.

## Contents
- [Post anatomy](#post-anatomy)
- [Length](#length)
- [Visual shape](#visual-shape)
- [Emphasis, emojis, symbols](#emphasis-emojis-symbols)
- [Body patterns](#body-patterns)
- [The close](#the-close)
- [Killing AI tells](#killing-ai-tells)
- [Output file rules](#output-file-rules)

---

## Post anatomy

Four zones. Each has exactly one job. Formatting exists to serve the job, not to look busy.

| Zone | Lines | Job |
|---|---|---|
| Hook | 1–2 | Stop the scroll, survive the fold |
| Re-hook | 3–5 | Convert the "see more" click into a committed read |
| Value | body | Pay the promise — the reason dwell time exists |
| Close | last 2–4 | Land the takeaway, open a real conversation |

The value section is the only zone where the post earns anything. Hook and close are packaging. If the value section can be replaced with a generic paragraph anyone could have written, the post has no reason to exist and no amount of formatting fixes it.

## Length

**Target 1,200–1,600 characters.** Shorter posts work when the idea is genuinely small; longer posts lose readers before the close and drag dwell-time-per-view down.

Three notes on counting:
- Line breaks count as characters. A post using aggressive single-line paragraphs has meaningfully less reading content than its raw count suggests.
- The 3,000-character cap is not a target. Nothing rewards using it.
- **Never pad to reach the band.** A tight 900-character post beats a 1,400-character post with 500 characters of filler, because filler is where readers scroll away.

Report the final count to the user.

## Visual shape

The feed is a skim environment. Readers decide in roughly two seconds based on **shape before content** — a dense block reads as effort before a single word is processed.

- **1–3 sentences per block**, then a blank line.
- **Double line breaks between blocks.** Single breaks don't create enough visual air on mobile.
- **Vary block length.** Uniform three-line blocks read as machine-generated. A one-line block after a three-line block creates emphasis without any formatting.
- **One-line paragraphs are a rhythm tool.** Use them for the sentence that matters most. Use them everywhere and they stop meaning anything.
- **Lists:** manual dashes or arrows, three to five items, only when the content is genuinely enumerable. A list of forced parallel items reads worse than the prose it replaced.

## Emphasis, emojis, symbols

**Bold: one phrase maximum, often zero.** LinkedIn has no real bold — creators paste Unicode mathematical characters, which screen readers mangle and search indexing skips. Never bold a term that matters for discoverability. Structure should carry emphasis; bold is a last resort.

**Emojis: two maximum.** Acceptable as section markers or a single tonal beat. Not acceptable as bullet points on every line, and not acceptable if `source.md` shows an author who doesn't use them. Zero emojis is always a valid answer.

**Avoid decorative separators.** Lines of `━━━` or `▬▬▬` are a 2021 tell. White space does the same job without the costume.

## Body patterns

Choose the one that matches what `source.md` actually contains.

**Problem → misdiagnosis → real cause → rule.** Strongest default for technical content. Ends on a generalizable rule, which is what earns saves.

**Story → turn → lesson.** For genuine incidents. The turn must be a real surprise; if the ending was obvious from the setup, use a different pattern.

**Claim → evidence → objection → response.** For contrarian positions. Naming the strongest counterargument is what separates a defensible take from a hot take, and it reliably produces substantive comments because the audience arrives already engaged with the objection.

**Framework/checklist.** Highest save rate. Only use it when the source genuinely contains a repeatable process — inventing steps to fill a framework is transparent.

**Before → after → what changed.** For results with real numbers. Requires actual numbers from `source.md`.

## The close

Two components:

**Takeaway.** One line compressing the post into something quotable. Not a summary — a distillation. If it reads like "So in conclusion, X is important", cut it and end on the last substantive line instead.

**A real question.** The bar: could a knowledgeable person answer it in a paragraph, and could two knowledgeable people disagree?

- ❌ "Thoughts?" / "Agree?" / "What do you think?" — answerable with one word, produces exactly the generic comments the ranker discounts.
- ❌ "Comment YES if you've been there." — bait, actively suppressed.
- ✅ "If you've shipped agents to production, what broke first for you — the model or the plumbing?" — specific, experience-gated, genuinely contested.

A closing question is optional. A post ending on a strong takeaway beats one bolted to a limp question.

## Killing AI tells

This is the highest-value pass in the entire workflow. The source material is human; the draft is not. Readers detect LLM prose fast, and a post that reads as machine-written loses credibility regardless of how good the underlying idea is.

**Banned phrasings — delete on sight:**

- "In today's fast-paced world" / "In an era of" / "Now more than ever"
- "It's not just X — it's Y" (the single most recognizable LLM construction)
- "Here's the thing:" / "Here's the kicker:" / "But here's what nobody tells you:"
- "Let that sink in."
- "game-changer", "delve", "leverage" (as a verb), "unlock", "harness", "seamless", "robust", "landscape", "realm", "testament to"
- "The results speak for themselves."
- "I'm excited to share" / "humbled to announce"
- "This is a masterclass in..."
- "And that's when it hit me."

**Structural tells:**

- **Triadic rhythm everywhere.** Three-item lists, three-clause sentences, three-beat paragraphs. Occasionally fine; as a default rhythm it's a signature. Break at least one triad into two or four.
- **Em-dash saturation.** More than one or two per post reads machine-written. Convert most to periods or commas.
- **Uniform paragraph length.** Vary deliberately.
- **Symmetrical antithesis.** "Not X, but Y" repeated across the post.
- **Perfect grammar with zero contractions.** Most people write "don't", not "do not".
- **Summary that restates instead of advancing.** Human writers usually end on the last new idea, not on a recap.

**Positive moves that restore a human voice:**

- Keep one concrete detail that serves no argumentative purpose — the specific tool name, the actual time on the clock, the exact error message. Fabricated detail is forbidden, but detail already present in `source.md` is the strongest anti-AI signal available.
- Let one sentence run long and one run to two words.
- Keep an idiosyncratic word choice from `source.md` even if a smoother synonym exists.
- Allow a mild hedge where the author is genuinely unsure. LLM prose is uniformly confident; people aren't.

Final check: read the draft aloud. If it doesn't sound like the person who wrote `source.md` would say it, it isn't finished.

## Output file rules

`linkedin_post.md` contains **the post body and nothing else** — it gets pasted straight into the composer.

- No YAML frontmatter.
- No markdown headings (`#`), no markdown bold (`**`) — LinkedIn renders neither. If a bolded phrase is genuinely warranted, use Unicode bold characters so it survives the paste.
- No title line, no "Here's your post:", no commentary, no character count inside the file.
- Preserve exact line breaks. The blank lines are load-bearing formatting.
- Hashtags, if any, on a final line after a blank line.
