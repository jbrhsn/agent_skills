---
name: remotion-infographics
description: Create or revise short Remotion infographic animations for article and social-post ideas, including a final-frame hero PNG. Use when a content piece needs an animated explanatory visual, not a static illustration or a full narrative video.
---

# Remotion Infographics

Create a clear, reusable Remotion scene from the content material the user names. The result should explain one idea visually and work as an article embed or social video.

## Establish the message

Read the relevant source, article, and post drafts before designing. Identify:

- the one claim the animation must make;
- the audience and destination;
- the concepts that need visual structure rather than more prose;
- factual wording that must remain attributed or qualified.

Do not invent statistics, product behavior, customer stories, or personal experience. Keep visible text concise, accurate, and free of raw URLs. Follow repository copy constraints, including any prohibition on em dashes.

## Choose the scene

Honor the requested duration and aspect ratio. If the user does not specify them, use a 16:9 1920 by 1080 composition at 30 fps and keep the scene between 10 and 20 seconds.

Use a visual sequence that fits the material. For an argument or explainer, a useful progression is:

1. State the claim.
2. Animate the model, contrast, or relationship that explains it.
3. Reveal the practical implications.
4. Close with a concise takeaway that can stand alone as the final frame.

Avoid decorative motion that does not clarify the point. Build readable hierarchy, adequate contrast, and safe spacing for social crops. Prefer code-native shapes, typography, and diagrams. Use external images or generated assets only when they add information the scene cannot express more clearly.

## Build in the content folder

Create or update a self-contained `remotion-infographic/` folder beside the relevant article or post. Do not create a shared root video project unless the user asks.

For a new project, include:

- `src/index.ts` that registers the Remotion root;
- `src/Root.tsx` with the composition dimensions, frame rate, and duration;
- one or more scene components;
- `package.json` with development, render, typecheck, and hero-frame scripts;
- `README.md` with the composition details and render commands;
- `.gitignore` for `node_modules/`, `out/`, and Remotion caches when those artifacts should remain local.

If a project already exists, inspect its composition and preserve the existing naming and structure unless the user requests a redesign.

## Render and verify

Install or update dependencies only when needed and within the user's project scope. Request approval before a network download or any action that needs elevated access.

Render the video into `out/`. Always render the final composition frame as a PNG for the article hero image. The final frame is `durationInFrames - 1`, not `durationInFrames`.

Provide a script such as:

```json
"render:hero": "remotion still src/index.ts <composition-id> out/<name>-hero.png --frame=<last-frame>"
```

Run type checking and render the MP4. Inspect at least one representative still when visual layout matters. Use ffprobe or an equivalent check to verify the final video dimensions, frame rate, and duration. Do not claim visual verification if the render was not inspected.

## Deliver

Report the project path, MP4 path, hero PNG path, dimensions, duration, and checks that passed. Explain any remaining limitation, such as platform-specific crop requirements or unverified font availability. Drafting and rendering do not authorize publishing or uploading the video.
