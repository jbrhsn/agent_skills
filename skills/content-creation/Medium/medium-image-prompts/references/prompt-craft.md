# Prompt craft

Prompts must work in any image service. Write them as plain descriptive prose. Keep tool-specific syntax — `--ar`, `::`, weights, seeds — out of the prompt body; aspect ratio is a separate field the user translates.

---

## Structure

Each prompt runs in this order. Consistency across the set is what keeps the images looking related.

1. **Subject** — the one thing in frame, stated concretely.
2. **Composition** — placement, scale in frame, negative space.
3. **Style** — the locked rendering style, verbatim from the article's style lock.
4. **Colour** — the locked accent, named precisely, plus what stays neutral.
5. **Background** — the white seamless statement, verbatim, every time.
6. **Lighting / finish** — flat and even, or the track's equivalent.

Target 40–70 words. Shorter loses control of the style; longer and most models start dropping clauses, usually the ones at the end — which is why background and style go in the middle, not last.

**Example:**

> A single stylised bell shape rendered in flat vector illustration, centred with generous space around it, uniform 2px black outlines, no shading, filled with deep slate blue accent on otherwise neutral greys, isolated on a pure white seamless background with no shadow, gradient, or vignette, flat even lighting, minimal editorial style.

The clauses that repeat across the set — style, colour, background, lighting — should be copied word for word between prompts. Rephrasing them is what causes a set to drift.

---

## Negative prompts

Supply one per image. Some services ignore it; the ones that use it benefit significantly. Base list, extended per image:

```
text, letters, words, watermark, signature, logo, brand marks, UI chrome,
charts, graphs, plotted data, numbers, gradient background, coloured background,
drop shadow, vignette, photorealism, cluttered composition, multiple focal
points, human faces, extra fingers, borders, frames
```

Add per track: for line-art tracks, add `heavy shading, 3D render`. For isometric tracks, add `perspective distortion, tilted horizon`.

---

## Failure modes worth pre-empting

**Text creeps in.** Models add labels to anything that resembles a diagram or an interface. State "no text or labels" inside the prompt body as well as in the negative — the negative alone often isn't enough for diagram-like subjects.

**The white background stops being white.** Models drift toward soft grey gradients and drop shadows to make a subject "sit" on the surface. Say "pure white seamless background, no shadow, no gradient, no vignette" explicitly. If the service still adds a shadow, tell the user to regenerate rather than accept it — a shadowed image looks like a pasted rectangle on Medium's white page.

**Composition drift across the set.** Fix scale in frame explicitly: "centred, occupying roughly 60% of the frame." Without it, image one is a close-up and image four is a wide shot.

**Metaphor literalism.** Prompting "a broken pipeline" produces a damaged industrial pipe. Describe the visual form directly — "a continuous line that fractures at its midpoint" — rather than naming the concept and hoping.

**Accidental brands.** Models insert recognisable logos into anything technical. Name the generic form you want and put brand marks in the negative.

---

## Aspect ratios

- **Hero / cover:** 16:9. Generate at 1600×900 or larger; Medium wants a cover at least 1200px wide and will downscale cleanly.
- **In-article:** 3:2, or 16:9 if the subject is wide. Keep every in-article image at the same ratio — mixed ratios break the rhythm of the page.
- **Diagram-like subjects:** 4:3 is acceptable if the content genuinely needs the vertical room, but use it for all images in the set or none.

---

## Alt text

Not optional. Medium's guidelines call out alt text explicitly, and it is the part most often skipped.

Describe what the image shows, not that it is an illustration. One sentence, under about 125 characters, no "image of" or "illustration depicting".

Weak: *An illustration representing monitoring.* Better: *A stylised alarm bell in blue on white, isolated and centred.*

## Captions

Short and useful. A caption should add context, name what the reader is looking at, or carry the credit — not restate the alt text.

Medium requires AI-generated images to be captioned as such. Provide a caption for each image and note the requirement once at the top of the file; the user decides how to apply it.
