# Design system template

Use this structure for the design system section of `docs/ux-design.md`. Always required (per Phase 5) — never omit this section.

```markdown
## Design System

### Color Palette
| Token | Light mode | Dark mode | Usage |
|-------|-----------|-----------|-------|
| primary | #.... | #.... | Primary actions, links |
| secondary | #.... | #.... | Secondary actions |
| neutral-100...900 | #.... | #.... | Backgrounds, borders, text |
| success | #.... | #.... | Confirmations |
| warning | #.... | #.... | Caution states |
| error | #.... | #.... | Errors, destructive actions |

(Omit the dark mode column entirely if dark mode isn't in scope.)

### Typography
| Style | Font | Size | Weight | Line height | Usage |
|-------|------|------|--------|-------------|-------|
| H1 | ... | ... | ... | ... | Page titles |
| H2 | ... | ... | ... | ... | Section headers |
| Body | ... | ... | ... | ... | Default text |
| Caption | ... | ... | ... | ... | Metadata, hints |

### Spacing Scale
Base unit: <e.g. 4px>. Scale: 4, 8, 12, 16, 24, 32, 48, 64 (adjust to base unit).

### Core Components
For each: name, states, and where it's used.

#### Button
- Variants: primary, secondary, destructive, ghost
- States: default, hover, active, disabled, loading
- Sizing: sm/md/lg

#### Input
- States: default, focus, error, disabled
- Variants: text, textarea, select, etc. as needed

#### Card
- Structure: <e.g. optional image, title, body, action row>

(Add/remove components based on what the screens in Phase 4 actually use — don't pad with unused components.)
```

## Guidance

- If the interview revealed an existing component library or brand kit (e.g. shadcn/ui, Material Design, a company brand guide), map this design system onto those tokens/components rather than inventing colors and type scales from scratch. State explicitly which library is the base.
- If no existing system was named, propose a sensible, cohesive default (don't leave placeholders like `#....` in the final doc — pick real values) and note it's a starting point the user can adjust.
- Only define components that are actually used by screens designed in Phase 4.