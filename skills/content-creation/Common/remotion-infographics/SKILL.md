---
name: remotion-infographics
description: Create or revise 10- to 30-second Remotion infographic videos from articles or social-post ideas, delivering an MP4 and a final-frame hero PNG. Use for concise visual explanations with researched engagement patterns, theme and palette selection, and complete local rendering.
---

# Remotion Infographics

Turn the supplied article, source.md, draft, or idea into one valuable visual explanation. Deliver a complete Remotion project, a 10- to 30-second MP4, and a PNG of its final frame. Preserve the author's core message, opinions, voice, factual scope, and uncertainty while improving visual clarity and pacing. Explicit user duration or format requests override defaults.

## Understand and research

Read the relevant source and repository instructions. Identify the audience, destination, single takeaway, supporting evidence, and concepts best explained through motion. Ask for missing source material when necessary; do not fabricate statistics, product behavior, experiences, or claims to strengthen a hook. Keep visible copy concise and free of raw URLs; retain necessary qualifications and short source credits, with full links in project notes.

Read [references/retention-and-styles.md](references/retention-and-styles.md) before designing. Research current platform guidance and recent relevant examples for the audience, region, and destination on each new project. Prefer examples from the last 30–90 days when available, recording publication dates, observation date, links, and the actual evidence available. Inspect the source or video itself when possible; distinguish observed visual patterns from descriptions you could not verify. Use platform trend tools and original creator examples, not unsupported lists of viral formulas. Adapt storytelling patterns without copying another creator's script or branding.

Separate platform guidance, creator experience, observed popularity, and measured retention. Likes, views, ad recall, and click-through rates do not establish organic retention or causation. Recommend a pattern based on content fit and evidence, with limitations; never promise virality or invent a performance ranking. If current research is inaccessible, disclose that and offer established styles as design options, not verified current trends.

## Confirm the creative direction

Ask the user for a visual theme and color scheme unless already supplied. To make the decision concrete, present at least five distinct style options from the reference, adapted to the article, and recommend one. For each, briefly give the opening hook, visual treatment, intended attention mechanism, and fit or tradeoff. Offer two or three palettes with hex colors and background/text/accent roles, or apply the user's brand palette. Do not claim universal psychological meanings for colors.

Include the recommended duration, aspect ratio, audio approach, and a compact timed storyboard showing the hook, explanation, practical payoff, and final hero composition. Explain the research behind the recommendation with direct source links and identify design hypotheses separately. Ask for approval or revisions to the theme, palette, and direction before implementation. Continue independent research while waiting, but do not treat silence as approval. Existing approval, a supplied complete direction, or explicit delegation to choose is sufficient; do not repeat the gate for routine revisions within that direction.

Default to 20 seconds at 30 fps. Use 1080 × 1920 for vertical social feeds and 1920 × 1080 for article embeds; honor supplied platform requirements. If the destination is unknown, include it in the creative-direction question. Use one approved master aspect ratio for both deliverables; additional crops are optional and require layout adaptation, not stretching.

## Design for attention and understanding

- Make the first frame meaningful. Show the central tension, result, or useful question immediately; avoid an opening logo slate or slow title reveal.
- Use a truthful curiosity gap and resolve it. Reveal value throughout, rather than withholding the answer until a final CTA.
- Aim for a meaningful visual development every 1–3 seconds as a starting heuristic, not a mandatory cut rate. Use highlights, diagram steps, comparisons, and camera reframing to direct attention. Hold dense evidence longer and remove content that cannot be read comfortably.
- Give each beat one focal point and one explanatory job. Pair related text and graphics spatially; retain enough visual continuity to make relationships understandable. Choose the mechanism that fits this video: contrast for comparisons, progressive reveal for processes, expectation and resolution for misconceptions, or a worked example for abstract ideas.
- Prefer a small number of useful facts and a concrete implication over a compressed article summary. Ensure chart axes, units, baselines, and animated values remain honest. Do not show invented intermediate values as observations.
- Keep the explanation understandable muted. If using narration, add accurate synchronized captions; use music and effects only when they support the content and rights permit use in the exported file. A platform's trending sound is not automatically licensed for an external MP4.
- Reserve the final 2–3 seconds for a settled, self-contained hero composition with a takeaway and the essential diagram or evidence. Make the exact last frame complete and readable without the preceding animation. Do not end on black, a transition, a CTA-only card, or a loop reset. An optional loop must preserve this ending.

## Initialize the local project

After the creative direction is confirmed, create or update `remotion-infographic/` beside the relevant content. Use it as the Remotion working directory. Inspect an existing project before editing and preserve unrelated files, dependencies, and outputs. Do not create a shared root project or nested Git repository by default.

Before generating artifacts, update the containing repository's `.gitignore` without replacing existing rules or duplicating entries. Add the requested legacy-name rules and the actual working-folder rules:

```gitignore
# Local Remotion infographic workspaces
**/remotion-graphic
**/remotion-graphic/*
**/remotion-infographic/
**/remotion-infographic/*
```

The two names differ: the `remotion-graphic` rules alone do not ignore `remotion-infographic/`. If there is no Git repository, put these rules in the content folder's `.gitignore`; do not initialize Git just for this task. Check representative paths with `git check-ignore -v --no-index` when Git is available. Ignore rules do not remove tracked files; report any tracked workspace files without unstaging or deleting them automatically.

Read [references/remotion-production.md](references/remotion-production.md) for setup, deterministic animation, render commands, and verification. Include the composition, source components, TypeScript configuration, package scripts, lockfile, and a concise project `README.md`. Keep the approved brief, storyboard, research links and limitations, asset credits, and reproduction commands in that README rather than scattering extra deliverables. Keep dependencies and caches local to the project. Use available permissions for required installation and rendering; request escalation only when the environment requires it.

## Render, inspect, and deliver

Complete implementation and render both outputs after approval; do not stop at a storyboard, scaffold, or commands for the user to run. Default paths are `remotion-infographic/out/infographic.mp4` and `remotion-infographic/out/infographic-hero.png`. Render the hero from the same composition and props at `durationInFrames - 1`; never substitute a separately designed poster.

Run type checking, render the MP4 and PNG, inspect the opening, a dense beat, transitions, and the final still, and review playback when supported. Verify mobile-size readability, safe areas, contrast, factual labels, timing, asset loading, and audio/caption alignment when present. Check actual media metadata and confirm the hero matches the last composition frame. Fix observed defects and rerender affected outputs. If execution is blocked, report the exact blocker and what remains unverified; do not claim the artifacts exist or were watched.

Deliver links to the MP4, hero PNG, and editable project, plus dimensions, frame rate, duration, selected style and palette, and checks performed. State whether verification covered stills only or playback as well. Publishing or uploading requires separate authorization. If analytics are later supplied, use them to refine the hook or a specific confusing beat; retention improvement remains unmeasured until real audience data exists.
