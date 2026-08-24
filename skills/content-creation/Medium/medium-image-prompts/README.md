# medium-image-prompts

Companion to `medium-article`. Reads a finished, edited article and writes
`image-prompts.md` — one hero prompt plus three to five in-article prompts, each
with placement, aspect ratio, negative prompt, alt text, and caption.

Service-agnostic: prompts are plain prose with no tool-specific flags. Aspect
ratio is a separate field you translate to whatever your generator expects.

## Layout

```
medium-image-prompts/
├── SKILL.md
├── references/
│   ├── style-tracks.md            # visual system per piece type, read at style lock
│   └── prompt-craft.md            # prompt structure, negatives, failure modes
└── assets/
    └── image-prompts-template.md
```

## Install

Same paths as `medium-article` — symlink into `.claude/skills/` and
`.agents/skills/` to cover Claude Code, OpenCode, and Antigravity.

```bash
cp -r medium-image-prompts ~/skills/
ln -s ~/skills/medium-image-prompts ~/.claude/skills/medium-image-prompts
ln -s ~/skills/medium-image-prompts ~/.agents/skills/medium-image-prompts
```

Restart the agent session afterward.

## Use

```
articles/iceberg-compaction/
├── source.md
├── medium_article.md ← after your editing pass
└── image-prompts.md  ← produced here
```

Run it only once the article is final. Placement and subject matter are derived
from what the sections actually say, so prompts generated from a draft go stale
the moment you restructure.

## House style

**White seamless background on every image, always.** Medium's reading surface is
white, so images dissolve into the page instead of sitting in a grey box. The
skill states this explicitly in every prompt and puts shadows, gradients, and
vignettes in the negative — models drift toward adding them.

**Everything else varies by article.** The skill classifies the piece and picks a
visual track from `references/style-tracks.md`: object series for listicles,
isometric process art for tutorials, tension-and-resolution for post-mortems, a
single bold metaphor for opinion pieces, line-art structure for explainers,
human-scale moments for experience reports. It then locks one accent colour, one
rendering style, and one perspective, and repeats those clauses verbatim across
the set so the images read as a series.

## What it won't prompt for

- **Text of any kind.** Image models render lettering badly; labels go in captions.
- **Logos and brand marks.** Generic forms instead.
- **Real or identifiable people.** Abstracted figures only.
- **Charts, graphs, dashboards, or terminal output.** A generated chart shows
  invented numbers, and Medium treats fabricated figures as a rules violation.
  Where the article needs one, the skill flags a `[user-supplied]` slot and says
  what it should show rather than filling it with decoration.

## Notes

Medium requires AI-generated images to be captioned as such. The output file
carries a reminder; how you apply it is your call.

Generated art is decoration. It does not replace the architecture diagram or
screenshot a technical piece actually needs — Medium's guidelines favour images
that carry information, and the skill is built to flag those moments rather than
paper over them.
