---
name: author-chapter
description: Write or revise substantial teaching material such as chapters, tutorials, guides, and learning modules, or populate learning-repository stubs. Adapt depth, format, and teaching approach to the learner and requested outcome. Use create-learning-repo for curriculum planning or scaffolding when that is the requested deliverable.
---

# Author Chapter

Turn a small note or brief into a complete learning chapter that helps the reader understand, explain, and practically use the topic. Completeness is relative to the learning goal, not every possible related subject. Match explicit requests for another audience, format, or depth; a short introduction need not promise expertise.

## How to use this guidance

Layouts, unit sizes, and individual teaching techniques are defaults to adapt, combine, or skip when another approach better serves the task. Establishing the assignment, covering the learning goal, and checking practical usability are still required for a complete module. The user's request, existing project conventions, and relevant evidence guide the result. Choose tools and writing strategy according to the work; this skill adds no approval gate or tool restriction.

Preserve factual accuracy and the learner's existing work. Distinguish illustrative examples from observed results, and never claim research, execution, or learner progress that did not happen.

## Understand the assignment

Before outlining or drafting, read the target stub if it exists and the relevant surrounding brief or conversation. Its purpose, topics, depth, prerequisites, and tier labels provide continuity. Keep existing metadata, navigation, and learner notes unless changing them is part of the task. If the brief is stale or conflicts with the request, update the affected brief and plan consistently within the authorized scope rather than mechanically following it.

- If the stub gives useful direction, combine it with the user's request to establish the topic and learning goal.
- If the stub is missing, empty, or only placeholders, use the topic and goal already supplied in the conversation or relevant brief. A missing file alone is not a reason to ask again.
- If either the topic or learning goal is still missing, ask only for what is missing before drafting: what should the chapter cover, and what should the learner be able to do afterward? A topic-only title does not establish the goal. Accept an everyday-language goal; no formal brief is required.

Unless the brief specifies otherwise, write for a curious 15-year-old new to the topic. Use respectful, familiar language without making the content childish or shallow. Explain unfamiliar terms, notation, and essential prerequisites; do not assume workplace experience or specialist background. Infer incidental choices reasonably and ask about other missing details only when they would materially change the result.

Use [file-types.md](references/file-types.md) for scaffolded or assessment files and [domains.md](references/domains.md) when domain-specific evidence or example choices matter. Read only the references useful to the task.

## Shape the material

For a complete module, make a compact internal coverage map before drafting: the capability the learner should gain, their assumed starting knowledge, the central concepts or mechanism, essential prerequisites and adjacent topics, a practical application, and important limitations. Teach missing essentials where they are needed; briefly explain relevant connections and defer optional enrichment. Do not treat the stub's headings as the full boundary of necessary teaching or expand into every related subject. This map guides coverage, not the chapter's visible headings.

Apply 80/20 as a prioritization heuristic: give the most attention to concepts and practical patterns that contribute most to the learner's stated goal. Teach their prerequisites fully. Include adjacent topics, additional examples, and edge cases when they enable application or prevent a meaningful misunderstanding; otherwise omit them or offer brief further-reading pointers. Do not enforce a numerical split, omit explicitly requested coverage, or compress explanations until they become difficult to follow.

Default to the flow of a well-written explanatory blog post: a meaningful opening, connected reasoning, topic-specific headings, and examples placed where they answer the reader's next question. When authoring a complete module from a note or stub, read one finished calibration example: [chapter-example.md](references/chapter-example.md) for a compact conceptual chapter, or [sql-window-functions-example.md](references/sql-window-functions-example.md) for a technical chapter with runnable examples and boundary cases. Each demonstrates coverage choices; do not load both unless useful. Use [structure.md](references/structure.md) when deciding how to organize long or scaffolded material. These references are not templates to copy.

A unit of roughly five minutes can support short study sessions, but neither unit counts nor reading times are limits. For a broad assignment, use sections, navigation, or multiple files as appropriate to the request. Do not stop solely because a chapter exceeds a size target. Keep a requested single-file deliverable intact; ask about a scope conflict only if it prevents meaningful completion.

## Check the facts that need checking

Research when the user requests it or when currency, uncertainty, attribution, or the stakes make verification necessary. Stable explanations can use established knowledge and provided material without a fixed search quota. Follow the environment's research requirements.

Prefer primary sources for APIs, versions, standards, exam formats, benchmarks, and other changing or consequential claims. Cite what was actually consulted near the supported claim or in a useful sources section. Distinguish a measured result from an illustrative calculation. If verification is unavailable, narrow or qualify the affected claim and continue with what can be supported.

## Write and revise

Choose an efficient writing approach: a single pass for a short piece, incremental drafting for a long chapter, or targeted edits for existing material. Revise earlier passages when doing so improves coherence or correctness.

Use concrete examples, explanations of unfamiliar terms, and practice that fits the audience. Motivation, misconceptions, trade-offs, and retrieval questions are valuable where they teach something; they need not appear in every unit. Original examples, labelled hypothetical scenarios, and attributed real examples can all be useful. [pedagogy.md](references/pedagogy.md), [voice.md](references/voice.md), and [examples.md](references/examples.md) offer techniques and calibration without prescribing a single teaching style.

For a complete module with a practical learning goal, demonstrate an application with the reasoning exposed, give the learner a meaningfully different case to attempt, and provide a way to assess their result. Use explained answers, expected behavior, success criteria, or troubleshooting guidance as appropriate; respect requests to withhold solutions. Supply the setup or materials needed for the attempt. Integrate these into the narrative or a useful practice section rather than repeating a fixed pattern for every concept.

For a scaffold, replace instructional placeholders as the content is completed. Preserve learner answer and reflection fields; put requested model answers in clearly separate sections. Set a previously unfinished file to `status: drafted` when the requested content is complete, without resetting existing progress or asserting mastery.

## Review and deliver

Review the draft against the learning goal and internal coverage map, factual support, prerequisite order, and usability. Trace the learner's path from the explanation to the independent attempt: can they follow it using the chapter and explicitly established prior knowledge, and can they assess the result? Repair missing steps, unexplained vocabulary, and essential connections. Check that transitions connect ideas and headings serve the topic rather than expose the authoring checklist. Use relevant checks from [checklist.md](references/checklist.md); formatting preferences are not completion gates. State material limitations honestly.

Check for unnecessary material as well as missing coverage: would removing this section, example, or caveat materially reduce the learner's ability to understand, apply, or correctly judge the topic? If not, cut or shorten it while preserving requested coverage and useful narrative connections. Keep repetition that provides needed practice or clarification; remove repetition that adds no learning value.

Deliver in the requested format and location. For a file-based standalone chapter without a specified filename, `<topic-slug>.md` is a reasonable default. Report what was written or changed and any remaining verification or coverage limits, at a length appropriate to the work.
