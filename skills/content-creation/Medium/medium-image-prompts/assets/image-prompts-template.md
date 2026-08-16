# Image prompts: <article title>

**Source:** `<file the prompts were generated from>`
**Piece type:** <listicle / tutorial / case study / opinion / explainer / experience>
**Note:** Medium requires AI-generated images to be captioned as AI-generated.

## Style lock

Repeat these verbatim in every prompt. If you regenerate a single image later,
reuse this block so it matches the set.

- **Rendering:** <e.g. flat vector illustration, uniform 2px black outlines, no shading>
- **Accent colour:** <precise name or hex — e.g. deep slate blue #33475B>
- **Neutrals:** <e.g. black outlines, light grey fills>
- **Perspective / scale:** <e.g. straight-on, subject centred at ~60% of frame>
- **Background:** pure white seamless, no shadow, no gradient, no vignette
- **Lighting:** flat and even

## Base negative prompt

Append the per-image additions where noted.

```
text, letters, words, watermark, signature, logo, brand marks, UI chrome,
charts, graphs, plotted data, numbers, gradient background, coloured background,
drop shadow, vignette, photorealism, cluttered composition, multiple focal
points, human faces, borders, frames
```

---

## Hero

**Conveys:** <the article's central claim, in one line>
**Aspect ratio:** 16:9 — generate at 1600×900 or larger

**Prompt**

```
<40–70 words, self-contained, style/colour/background clauses verbatim from the lock>
```

**Negative additions:** <track-specific additions, or "none">

**Alt text:** <one sentence, content-descriptive, under ~125 chars>

**Caption:** <short and useful; carries the AI disclosure if the user wants it there>

---

## Image 1

**Placement:** after the section "<section heading>"
**Conveys:** <what this image does for the reader at this point>
**Aspect ratio:** 3:2

**Prompt**

```
<prompt>
```

**Negative additions:**

**Alt text:**

**Caption:**

---

## Image 2

<same block>

---

## Image 3

<same block>

---

<!-- Images 4 and 5 only if the article genuinely supports them. -->

## User-supplied slots

Places where a generated illustration would be the wrong call and a real visual
is needed. Leave empty if none.

| Placement | What it should show | Why generated art won't do |
|---|---|---|
| after "<section>" | <e.g. the actual query plan before and after> | real numbers; a generated chart would be fabricated data |

## Set check

- [ ] Every prompt names the white seamless background
- [ ] Style, colour, and perspective clauses are identical across prompts
- [ ] No prompt requests text, logos, real people, or plotted data
- [ ] All in-article images share one aspect ratio
- [ ] Hero represents the argument, not the topic
- [ ] Every image has alt text and a caption
