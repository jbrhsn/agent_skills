---
name: medium-article-writer
description: Draft, revise, and package Medium articles or long-form blog posts from notes, source material, or a defined brief. Use for tutorials, explainers, arguments, case studies, and experience reports that need coherent structure, voice, and factual support.
---

# Medium Article Writer

Develop a complete, useful article in the author's intended voice. Adapt the work to the requested audience, scope, language, and genre; do not assume every author is an engineer or every article requires a personal story.

## Source and brief

Read the named source and existing draft. Use `source.md` by convention, but accept supplied text, alternate filenames, or a research brief. Preserve the original unless the user explicitly asks to edit it. Distinguish the author's writing from quotations, linked sources, examples, and machine-generated notes.

Identify the thesis, reader promise, key evidence, lived experience, uncertainties, and desired voice. Read [voice inference](references/voice-inference.md) and [structure options](assets/article-structures.md) when shaping a substantial piece. For complex work, capture a concise `medium_brief.md` using [the template](assets/brief-template.md); a small edit needs no separate brief.

Proceed on reasonable editorial choices. Ask only about material ambiguity, missing first-hand facts essential to the piece, or a change that would reverse the author's position or remove explicitly requested content. Review gates apply when requested, not automatically before every draft. Record consequential omissions and why; normal editing does not require approval for each cut.

## Evidence and drafting

Research may verify existing claims or supply relevant background and examples within the requested scope. Attribute external evidence; never turn someone else's result into the author's experience. Do not invent benchmarks, quotations, sources, incidents, credentials, or product use. Clearly label illustrative examples.

Verify changing or consequential facts against suitable primary sources, checking date, version, locale, and context. User-provided assertions are not automatically verified. If evidence is unavailable, qualify or remove an unsupported peripheral claim transparently; ask when the central argument depends on it. Do not leave unresolved essential claims hidden in publish-ready prose.

Write `medium_article.md` for the folder workflow, or use the requested path/inline format. Make the title's promise match the article. Explain mechanisms, examples, tradeoffs, and limitations to the degree the reader needs. Length and formatting follow purpose. Follow [voice and revision guidance](references/voice-and-antislop.md), then [closing guidance](references/closing-and-cta.md) when useful.

For technical tutorials, identify environment assumptions and validate executable examples when feasible; distinguish tested code from illustrative or untested code. For health/finance/legal content, verify consequential guidance, distinguish general information from personal advice, and avoid unsupported promises. Do not force every such article into first-person memoir.

## Review and package

Use [the editorial audit](references/do-and-avoid.md) to fix substantive weaknesses and check meaningful source material survived. Avoid fabricated specificity and plagiarism; links do not justify copying another author's structure or expression.

For a full article request, create concise `medium_publish.md` from [the template](assets/publish-template.md) with useful title alternatives, subtitle/tags, sources and unresolved checks, image directions, and relevant publishing notes. Omit unnecessary packaging for a narrow edit. Alt text for uncreated images is provisional and needs checking against the actual asset.

Read [Medium mechanics](references/medium-mechanics.md) when packaging for Medium, especially AI disclosure and monetization rules. Writing style is not proof of human authorship or distribution eligibility; do not optimize to conceal AI involvement. Report actual readiness and any required author review. Drafting does not authorize publication or submission.
