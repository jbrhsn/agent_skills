---
name: content-fact-checker
description: Critically evaluate source.md or an initial draft, research factual claims on the web, and refine weak or broad claims with specific evidence and attribution while preserving the author's core message, opinions, voice, and tone.
---

# Content Fact Checker

Use this skill when the user wants source.md, an initial draft, article brief, essay, or post validated and refined through factual research without turning it into a different piece of writing. Accept a supplied file or pasted draft; do not require a particular filename.

## Core outcome

Improve reliability and clarity while preserving the author's original argument, personal perspective, intended audience, voice, tone, and level of ambition. Do not silently replace the author's thesis with a stronger or more fashionable thesis.

## Workflow

1. Read the complete source draft and any applicable repository instructions. Identify the author's central message, supporting ideas, personal experiences, tone, and intended deliverable.
2. Critically evaluate every claim, including implied comparisons, vague quantities, broad generalizations, statistics, forecasts, causal claims, and factual premises embedded in opinions or advice. Separate externally checkable assertions from opinions, interpretation, and firsthand experience; preserve the latter while checking any attached factual premise. Read [references/claim-audit.md](references/claim-audit.md) for claim categories and revision decisions.
3. Research externally checkable claims on the web, prioritizing central, weak, broad, numerical, time-sensitive, and consequential assertions. Search for supporting and conflicting evidence rather than only confirmation. Inspect the underlying sources instead of relying on search snippets or repeated summaries. Prefer primary sources, official reports, original research, and clearly described surveys. Record direct links, publication and data dates, population, geography, methodology, and limitations when they affect interpretation. Check supplied citations too; a citation's presence does not establish validity.
4. Build an internal claim check before rewriting: original claim, supported/partially supported/unsupported/contradicted/unverified/personal-editorial status, evidence and limitations, and proposed treatment. Distinguish a failed search from evidence disproving a claim. If browsing or a relevant source is unavailable, disclose the verification gap and leave affected claims explicitly unverified. Never invent a source, statistic, quote, experience, or causal explanation.
5. Refine weak or broad claims into specific, evidence-supported statements using the smallest faithful correction. Where relevant, specify who, what, where, when, the comparison baseline, and the measured result. Add facts or statistics only when they directly support the existing idea and match its scope; specificity need not be numerical. Preserve the source's uncertainty and distinguish correlation from causation. If evidence is insufficient, qualify or omit a nonessential assertion and report the change; do not disguise an unsupported factual assertion as an opinion or substitute another unsupported generalization.
6. Resolve internal contradictions at the narrowest point when the author's intended meaning is clear. If evidence contradicts a central factual premise, or resolving a contradiction would require choosing the author's position, flag the conflict and offer a sourced correction for author review. Continue independent refinements, but do not silently change the thesis, claim the contradicted premise is validated, or remove a core idea to make the draft pass.
7. Refine the prose in the author's existing style. Retain first-person language, examples, rhythm, directness, and practical advice unless they create a factual or logical problem. Do not make the draft sound like a research report.
8. Attribute researched facts and statistics by default. Preserve a requested citation style; otherwise add numbered inline references such as `[1]` immediately after supported claims and end with a compact numbered reference list containing direct links. Attribute survey findings, forecasts, and disputed findings in the prose where needed to establish scope. Keep personal observations and ordinary advice uncited unless they rely on an external claim. If the requested publishing format excludes citations or URLs, put claim-to-source mappings in separate research notes or the existing publishing notes.
9. Verify that every inline reference maps to one source, every retained numerical assertion is supported or explicitly flagged as unverified, and no source is cited for a claim it does not actually establish. Compare the revision with the original for changes in meaning, opinions, tone, certainty, and scope. State evidence limitations in the draft where needed to avoid misleading readers and summarize unresolved gaps in the handoff.

## Non-negotiable boundaries

- Do not change the author's core message, opinions, voice, tone, style, or intended audience. Preserve disagreement and personal judgments; evaluate their factual premises without treating preferences as empirical claims.
- Do not convert uncertainty into certainty. Avoid absolutes such as “always,” “never,” “everyone,” and “no longer” unless the evidence genuinely supports them.
- Do not treat a vendor survey, self-reported adoption statistic, or forecast as universal fact. Identify who was surveyed and what the result measures.
- Do not use research to erase the author's lived experience. Distinguish firsthand experience from generalization.
- Do not add URLs to a publishable post body when repository instructions prohibit them. Put sources in numbered references or a separate research-notes section.
- Follow applicable repository style rules, including the repository's zero-em-dash constraint when present.
- If the evidence cannot support a claim, say so and use the treatment above according to whether it is incidental or central to the author's message. Do not fabricate a supporting citation or imply the draft is fully validated while material gaps remain.

## Deliverable

When editing is requested, update the requested source file or return the refined pasted draft, with attribution and a concise change summary covering material corrections, qualifications, added evidence, and unresolved claims. For unresolved central claims, include the original assertion, conflicting or missing evidence, and a proposed correction for author review. Follow requested output paths and existing publishing-note conventions; do not create extra files by default. When the user asks only for critique, return the claim audit and suggested corrections without modifying files.
