# Style tracks

One track per article. Pick at step 2, lock the variables, repeat them in every
prompt.

White seamless background is constant across all tracks. What changes is
subject logic, rendering style, and accent colour.

---

## Listicle

The set is a series of objects, one per item. Coherence matters more here than
anywhere else, because the reader sees them in sequence and any drift reads as
sloppiness.

**Rendering:** flat vector illustration, uniform 2px line weight, single accent
colour, no shading. Or fine single-weight line art if the items are abstract.

**Subject logic:** one central object per image, isolated, centred, same scale in
frame every time. If item three is "monitoring" and item four is "alerting", the
objects must be visually distinct — a bell and a gauge, not two dashboards.

**Hero:** the collection. All the item objects arranged in a loose grid or arc on
white, same style, smaller scale.

**Trap:** items that aren't visually distinguishable. If three of five list items
would produce near-identical images, drop to three images and place them at the
items that differ.

---

## Tutorial / how-to

Images should feel procedural — the reader is doing something in a sequence.

**Rendering:** isometric illustration, 30-degree projection, flat colour with
minimal shading. Or clean technical line drawing if the subject is a system
rather than an activity.

**Subject logic:** state changes and mechanisms. Something entering a process and
leaving it altered. Connected components with directional flow. Keep it abstract
enough that it doesn't pretend to be a real architecture diagram — generic blocks,
pipes, containers, nodes, arrows.

**Hero:** the whole process in one frame, simplified to three or four stages.

**Trap:** this track drifts toward looking like a real diagram. If it starts
carrying information the reader might act on, it needs to be a real diagram the
user draws, not a generated one. Flag it as `[user-supplied]`.

---

## Case study / post-mortem

The article has a shape: things were fine, things broke, things were fixed. The
images should carry that arc.

**Rendering:** soft 3D clay render or paper-cut layered illustration. Slightly
more tactile than the other tracks, because the story is about consequence.

**Subject logic:** tension and resolution. A structure under load. A break in a
continuous line. Something overloaded, then rebalanced. Two colours are justified
here — one for the failure state, one for the resolved state — and this is the one
track where a second accent earns its place.

**Hero:** the failure moment, not the fix. The fix is the payoff; the cover sells
the problem.

---

## Opinion / argument

One idea, stated visually. Restraint is the whole game.

**Rendering:** bold flat vector, high contrast, generous negative space. Large
simple shapes.

**Subject logic:** a single visual metaphor for the claim. Divergence, subtraction,
an odd one out, a tool being set down, a path not taken. Do not illustrate the
subject matter — illustrate the position.

**Hero:** the metaphor at its cleanest. Often this article type only needs a hero
plus two in-article images. Three weak conceptual illustrations dilute a strong
one.

**Trap:** the metaphor pile-up. One clear idea per image. A lightbulb and a maze
and a fork in the road in the same frame conveys nothing.

---

## Explainer

The reader wants a mental model.

**Rendering:** fine line art or technical blueprint style, single accent on white,
thin consistent strokes.

**Subject logic:** structure and relationship — layers, nesting, flow, scale
comparison, transformation. Abstract geometric forms rather than literal objects.

**Hero:** the whole mechanism as one legible shape.

---

## Experience report

Human-scale and narrative. The least abstract track.

**Rendering:** loose line illustration with a single accent wash, or minimal
editorial illustration. Slightly imperfect linework suits this one.

**Subject logic:** moments and objects rather than systems. A desk at a specific
hour. A hand mid-action. An object that carries the story. Abstracted figures
only — no faces, no identifiable people.

**Hero:** the emotional centre of the piece, not its topic.

---

## Accent colour

One colour per article. Choose for subject and mood, not brand:

- **Deep blue / slate** — infrastructure, storage, systems, reliability
- **Warm amber / ochre** — failure, cost, warning, retrospection
- **Teal** — data movement, transformation, pipelines
- **Muted violet** — models, inference, anything ML-flavoured
- **Forest green** — growth, results, resolution, money
- **Coral** — opinion and argument pieces that want a bit of heat

Name the colour precisely in every prompt — "deep slate blue" or a hex value, not
"blue". Vague colour words drift across generations, and drift is what breaks a
series.

For the post-mortem track, pair a warm accent for the failure state with a cool
one for the resolution, and use them consistently in that role.
