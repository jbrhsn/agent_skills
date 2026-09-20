---
name: medium-article-writer
description: Draft, revise, and package Medium articles or long-form blog posts while preserving the author's message and voice. For drafting, research and compare five title, hook, and structure proposals for author confirmation, then deliver the article and publishing guidelines.
---

# Medium Article Writer

Develop a complete, useful article in the author's intended voice. Adapt the work to the requested audience, scope, language, and genre; do not assume every author is an engineer or every article requires a personal story.

## Source and brief

Read the named source and existing draft. Use `source.md` by convention, but accept supplied text, alternate filenames, or a research brief. Preserve the original unless the user explicitly asks to edit it. Distinguish the author's writing from quotations, linked sources, examples, and machine-generated notes.

Identify the thesis, reader promise, key evidence, lived experience, uncertainties, and desired voice. Read [voice inference](references/voice-inference.md) and [structure options](assets/article-structures.md) when shaping a substantial piece. For complex work, use [the brief template](assets/brief-template.md) to organize the proposal in the conversation and retain useful decisions in `medium_publish.md` after confirmation; do not create a third brief file unless requested.

Treat the author's message, ideas, voice, and style as fixed constraints. Alternatives may change the opening and order of presentation, but must preserve substance, emphasis, qualifications, and attribution. Ask about consequential ambiguity or missing first-hand facts rather than inventing experience or dropping an idea to fit a popular format.

## Propose, research, and confirm before drafting

1. Generate exactly five distinct proposals, each pairing a candidate title and opening hook with a brief article outline, including its ending. These are planning options, not five complete articles. Fit the requested genre and scope; do not impose a narrative on a tutorial or invent a provocative thesis.
2. Then research the web for evidence of performing Medium titles, openings, and article structures relevant to the audience, topic, genre, and purpose. Prefer transparent studies and comparable articles with visible results; use author analytics if supplied. Inspect sources rather than relying on search snippets. Record links, dates, available metrics, and limits such as sample, publication exposure, audience size, and observation window. Distinguish measured performance from creator advice and isolated examples; claps or comments alone do not establish readership, completion, or a causal effect of the title or structure.
3. Compare all five proposals against the supported patterns and recommend the closest fit that fully preserves the author's message, ideas, voice, and style. Explain why its title, hook, and structure fit both the source and the evidence, why alternatives fit less well, and how confident the recommendation is. Never trade fidelity for predicted engagement or copy another article's distinctive structure or expression. If web access or credible performance evidence is unavailable, disclose the gap and label the recommendation as editorial judgment.
4. Present the five proposals, source-linked findings, and recommendation. Ask for author confirmation and suggestions, then wait before writing the full article or either output file. The author may approve, choose another option, or refine the proposal. Incorporate suggestions and resolve any remaining material ambiguity before drafting. Do not treat silence as confirmation or leave selection to the author without a recommendation.

Apply this review to new drafts and substantial rewrites. Make narrow edits to existing articles or publishing notes directly without restarting the process. An already confirmed direction in the current conversation does not need repeated approval.

## Evidence and drafting

Research may verify existing claims or supply relevant background and examples within the requested scope. Attribute external evidence; never turn someone else's result into the author's experience. Do not invent benchmarks, quotations, sources, incidents, credentials, or product use. Clearly label illustrative examples.

Verify changing or consequential facts against suitable primary sources, checking date, version, locale, and context. User-provided assertions are not automatically verified. If evidence is unavailable, qualify or remove an unsupported peripheral claim transparently; ask when the central argument depends on it. Do not leave unresolved essential claims hidden in publish-ready prose.

After author confirmation, write from the agreed title, hook, and structure, incorporating suggestions. Save `medium_article.md` containing only the article, including its title and body, for the folder workflow, or use the explicitly requested path/inline format. Make the title's promise match the article. Explain mechanisms, examples, tradeoffs, and limitations to the degree the reader needs. Length and formatting follow purpose. Follow [voice and revision guidance](references/voice-and-antislop.md), then [closing guidance](references/closing-and-cta.md) when useful.

For technical tutorials, identify environment assumptions and validate executable examples when feasible; distinguish tested code from illustrative or untested code. For health/finance/legal content, verify consequential guidance, distinguish general information from personal advice, and avoid unsupported promises. Do not force every such article into first-person memoir.

## Review and package

Use [the editorial audit](references/do-and-avoid.md) to fix substantive weaknesses and check meaningful source material survived. Avoid fabricated specificity and plagiarism; links do not justify copying another author's structure or expression.

For a full folder workflow, deliver exactly two Markdown files beside the source or in the requested output folder: `medium_article.md` and `medium_publish.md`. Create the latter from [the template](assets/publish-template.md), including the confirmed direction, proposal comparison and research rationale, recommended subtitle and tags, image recommendations and placement, sources and unresolved checks, and publishing guidance. Include a publishing time/window with audience timezone and evidence or a clearly labeled experimental assumption; state missing audience information rather than inventing precision. A recommendation of no subtitle, tags, or images is valid when explained. Keep editorial notes outside the article. Omit unnecessary packaging for an explicitly inline request or narrow edit. Alt text for uncreated images is provisional and needs checking against the actual asset.

Read [Medium mechanics](references/medium-mechanics.md) when packaging for Medium, especially AI disclosure and monetization rules. Writing style is not proof of human authorship or distribution eligibility; do not optimize to conceal AI involvement. Report actual readiness and any required author review. Drafting does not authorize publication or submission.
