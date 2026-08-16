---
name: medium-image-prompts
description: Read a finished article and generate ready-to-use image generation prompts for it — one hero/cover image plus three to five in-article images, each with placement, aspect ratio, negative prompt, alt text, and caption. Use this whenever the user asks for image prompts, cover art, hero images, article visuals, illustrations, or media for a blog post or Medium story, or says an article is finished and needs images. Also use when working in an article folder that contains a finished draft and the user mentions images, visuals, or artwork.
---

# Medium Image Prompts

Turn a finished article into a coherent set of image prompts the user can paste
into an image generation service. Output is a single file, `image-prompts.md`.

This runs **after** the article is written and edited. Do not generate prompts
from a draft, an outline, or a topic — read the actual final text, because
placement and subject matter come from what the sections actually say.

## Inputs

Work inside the article folder. Find the final article:

- If there is exactly one finished article file (typically `article.md`), use it.
- If several candidates exist, use the most recently modified and say which one
  you chose.
- If the user names a file, use that.

Read it end to end before writing any prompt.

## Output

One file: `image-prompts.md`, built from `assets/image-prompts-template.md`.

- **1 hero image** — the cover. 16:9.
- **3–5 in-article images** — placed at specific sections. 3:2 unless a diagram
  needs otherwise.

Fewer, stronger images beat five weak ones. If the article only supports three,
produce three and say why.

## Fixed constraints

Every prompt in every article must carry these:

**White background.** Pure white, seamless, no gradient, no vignette, no shadow
pooling at the edges. Medium's reading surface is white, so the image should
dissolve into the page rather than sit in a box. This is not negotiable per
article — it is the house style.

**No text.** Image models render lettering as garbage, and a misspelled word in a
cover image is worse than no image. Any label the user wants goes in the caption.

**No logos, brands, or trademarks.** Do not prompt for the Airflow logo, the AWS
icon, the Python logo, or any recognizable product mark. Use generic forms
instead — a directed graph rather than the Airflow logo, a stylized container
rather than the Docker whale.

**No real or identifiable people.** Abstracted figures, silhouettes, or hands only.

**No fabricated data.** Never prompt for a chart, dashboard, graph with plotted
values, or terminal output. A generated chart shows invented numbers, and Medium
treats fabricated figures as a rules violation. Real numbers belong in a real
screenshot or a real diagram the user makes.

## Workflow

### 1. Classify the article

Determine the piece type — listicle, tutorial/how-to, case study or post-mortem,
opinion, explainer, or experience report. This selects the visual system. See
`references/style-tracks.md`.

### 2. Choose the visual system

Pick one track from `references/style-tracks.md` and commit to it for the whole
set. Then lock three variables and repeat them verbatim in every prompt:

- **One accent colour**, chosen for the article's subject and mood. Everything
  else stays white, black, and grey. Two colours maximum, and the second only if
  the article genuinely has a before/after or A-versus-B structure.
- **One rendering style** — flat vector, fine line art, isometric, soft 3D clay,
  paper cut, technical blueprint.
- **One perspective and line weight.**

The set must read as a series. A hero in soft 3D followed by four flat vector
illustrations looks like four different articles.

State the locked choices at the top of `image-prompts.md` so the user can regenerate
any single image later and have it match.

### 3. Place the images

Walk the article and pick the moments that genuinely need a visual:

- The hero represents the article's central claim, not its topic. An article
  arguing that a vector database was the wrong choice gets an image about the
  wrong choice, not an image about databases.
- In-article images go where a reader's attention dips: after a dense technical
  passage, at a structural turn, at the start of a major section.
- For a listicle, one image per list item is the natural rhythm — but only if
  the items are visually distinguishable. Five near-identical illustrations are
  worse than two good ones.
- Do not place an image where a real screenshot, diagram, or code output belongs.
  Note that as a `[user-supplied]` slot in the file instead, and say what it
  should show.

### 4. Write the prompts

Follow `references/prompt-craft.md`. Each prompt is self-contained prose that
works in any image service — no service-specific flags in the prompt body.
Aspect ratio is a separate field so the user can translate it to whatever syntax
their tool uses.

For each image, supply: placement, what it conveys, the prompt, a negative
prompt, aspect ratio, alt text, and a caption.

### 5. Check the set

Before presenting:

- [ ] Does every prompt name the white seamless background explicitly?
- [ ] Does every prompt repeat the locked style, accent colour, and perspective?
- [ ] Is any prompt asking for text, a logo, a real person, or plotted data?
- [ ] Would the set read as one article if laid out side by side?
- [ ] Does the hero represent the argument rather than the subject?
- [ ] Does every image have alt text that describes content, not "illustration"?

## Notes to carry into the file

Medium requires AI-generated images to be captioned as such. Include a one-line
reminder at the top of `image-prompts.md`; the user decides how to handle it.

Generated art is decoration. It does not substitute for the diagram, screenshot,
or architecture sketch that a technical piece actually needs, and Medium's
guidelines favour images that carry information. Where the article has a moment
that wants a real visual, flag it rather than papering over it with an
illustration.

## Reference files

- `references/style-tracks.md` — the visual system per piece type, with accent
  colour guidance. Read at step 2.
- `references/prompt-craft.md` — prompt structure, negatives, and the failure
  modes worth pre-empting. Read at step 4.
- `assets/image-prompts-template.md` — output format.
