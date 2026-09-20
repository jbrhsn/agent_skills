---
name: linkedin-post-writer
description: Draft or revise LinkedIn posts while preserving the author's message and voice. For drafting, compare five hook-and-structure options against web research, recommend one for author confirmation, then deliver the post and publishing notes.
---

# LinkedIn Post Writer

Make the post useful to its intended professional audience and recognizable as the author's work. Clear substance and honest framing matter more than imitation of a feed formula.

## Read and choose

Read the named source and relevant existing draft. `source.md` is the default convention, not a required filename. A file's existence alone does not establish LinkedIn as the destination. If the platform is genuinely ambiguous, clarify it.

Identify the purpose, reader, central point, distinctive details, evidence, and voice. Use [voice guidance](references/voice-inference.md) for substantial rewrites or uncertain register. Preserve I/we attribution, uncertainty, and the author's intended position.

Treat the author's message, ideas, voice, and style as fixed constraints. Alternatives may change the opening and order of presentation, but must preserve the substance, emphasis, qualifications, and attribution. Ask about consequential ambiguity rather than inventing experience or dropping an idea to fit a popular format.

## Propose, research, and confirm before drafting

1. Generate exactly five distinct proposals, each pairing a candidate hook with a brief outline of the full post structure, including its close. These are planning options, not five complete posts. Use [hook options](references/hook-frameworks.md) and [structure guidance](references/structure-and-format.md) without forcing material into an unsuitable formula.
2. Then research the web for evidence of performing LinkedIn hooks and structures relevant to the author's audience, topic, format, and purpose. Prefer transparent studies and comparable posts with visible results; use author analytics if supplied. Inspect sources rather than relying on search snippets. Record links, dates, performance metrics, and relevant limits such as sample, audience size, or observation window. Distinguish measured performance from creator advice and isolated examples; high engagement alone does not prove the hook or structure caused it. See [distribution guidance](references/algorithm-mechanics.md).
3. Compare all five proposals with the supported patterns and recommend the closest fit that fully preserves the author's message, ideas, voice, and style. Explain why its hook and structure fit both the source and the evidence, why the alternatives fit less well, and how confident the recommendation is. Never trade fidelity for predicted engagement. If web access or credible performance evidence is unavailable, disclose the gap and label the recommendation as editorial judgment; do not claim to have identified the best-performing pattern.
4. Present the five proposals, source-linked research findings, and recommendation to the author. Ask for confirmation and suggestions, then wait before writing the full post or either output file. The author may approve, select another option, or refine the proposal. Incorporate suggestions; if they leave the intended direction unclear or materially change the proposed hook and structure, resolve that direction before drafting. Do not treat silence as confirmation or make the author choose without a recommendation.

Apply this review to new drafts and substantial rewrites. For a narrow edit to an existing post or publishing notes, make the requested change directly without restarting the selection process. An already confirmed direction in the current conversation does not need repeated approval.

## Draft and revise

After author confirmation, write from the agreed hook and structure, incorporating the author's suggestions. The opening should identify value or stakes and the body should deliver it. Direct announcements, concise advice, narratives, comparisons, and longer arguments can all fit; there is no mandatory character band or closing question.

Use sourced research when helpful and authorized; distinguish it from first-hand evidence. Never invent numbers, quotations, client stories, experiments, or personal accomplishments. Verify consequential or changing factual claims and keep citations close enough to inspect. Do not automatically move useful links out of the body based on an assumed reach penalty.

## Check and deliver

Check the post's meaning against the source, factual support, reader value, voice, accessibility, and requested length. Treat [distribution guidance](references/algorithm-mechanics.md) as evidence-aware advice, not a formula for virality.

After confirmation and drafting, deliver two Markdown files beside the source or in the author's requested output folder: `linkedin_post.md`, containing only the paste-ready post, and `linkedin_publish.md`, containing publishing notes using [the template](assets/post_notes_template.md). Include the selection rationale and research sources, a recommended publishing time with audience timezone and evidence or a clearly labeled experimental assumption, relevant hashtags and any suggested mentions, and checks before publishing. If timing depends on unknown audience geography, state the assumption or missing information rather than inventing precision. Include these publishing fields even when the appropriate recommendation is no tags or mentions. For an explicitly inline request or a narrowly scoped edit, deliver the requested artifact instead. Preserve unrelated edits and the original source.

Report paths and a measured character count when relevant. Flag unresolved factual issues; do not claim a post is ready while it contains essential unverified assertions. Preparing copy does not authorize publishing, scheduling, commenting, or messaging.
