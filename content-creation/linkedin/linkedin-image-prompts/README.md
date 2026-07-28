# linkedin-image-prompts

Generate image-generation prompts for a finished LinkedIn post or article — either a single hero image or a full carousel slide deck, chosen based on the post's actual structure. Produces **prompt text only**; it does not call any image API or render anything.

---

## Trigger phrases

| Input | Example |
|---|---|
| Visuals for a post | "generate image prompts for this post", "give me slide ideas for this" |
| Carousel request | "turn this into a carousel" |

Not for actually rendering images/PDFs — this is a prompt-writing skill, not a rendering pipeline.

---

## What it does

- **Reads the finished post** (typically `linkedin_post.md`), asking for the file if none is given.
- **Decides single image vs. carousel** based on structure: 4+ distinct beats/steps/sections favors a carousel (proven the highest-engagement LinkedIn format — roughly 585% better than text-only per 2026 data); a short single-insight post favors one hero image. States the reasoning and confirms with the user rather than deciding silently.
- **For carousels:** breaks the post into 6–9 slides (the sweet spot for swipe-through), enforces one idea per slide, designs a cover slide that makes a promise and a final slide with a clear takeaway + CTA. Prefers a case-study arc (problem → approach → result) when the content supports it.
- **For single images:** writes one detailed hero-image prompt tied to the post's hook/core claim.
- **Per slide/image**, writes: text overlay content, a detailed image-generation prompt (composition, style, color/mood, text placement), and a one-line rationale.
- **Flags mobile-readability risk** — LinkedIn is mostly viewed on a 6-inch screen; overlay text that's too long for that is called out.

---

## Input

A file path to the finished post/article. If not given, ask — or propose an obvious single candidate (e.g. a lone `linkedin_post.md` in the folder) for the user to confirm.

## Output

`image_prompts.md`, written in the **same directory as the source post**. Never silently overwrites — offers overwrite, `-v2`, or a new name.

---

## Workflow

1. Read the source post.
2. Decide carousel vs. single image, state reasoning, confirm with the user.
3. Generate the slide/image breakdown (Step 2a carousel / Step 2b single image in `SKILL.md`).
4. Present the full prompt set for a quick sanity check.
5. Write `image_prompts.md`, confirm the exact path.

---

## Limitations

- Produces prompt text only — no image rendering, no API calls, no file output beyond the markdown prompts.
- Requires a finished post as input; does not draft post copy (that's `linkedin-post-writer`).
- Format decision (carousel vs. single image) is a recommendation the user must confirm, not an automatic choice.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global — available in all projects (Linux/macOS)
cp -r content-creation/linkedin/linkedin-image-prompts ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin/linkedin-image-prompts .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin\linkedin-image-prompts "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a named section |
| **Cursor** | Paste into `.cursor/rules/linkedin-image-prompts.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your opening message |

---

## Companion skills

- **`linkedin-post-writer`** — produces the `linkedin_post.md` this skill reads from.
- **`linkedin-post-reviewer`** — refined posts can also be fed into this skill for updated visuals.
