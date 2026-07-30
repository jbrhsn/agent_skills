# Screen template

Use this structure for each screen in `docs/ux-design.md`. No ASCII art, no images — structured text only.

```markdown
### Screen: <Screen Name>

**Purpose**: One sentence — what this screen is for and when a user lands here.

**Layout** (top to bottom, or by region for complex/multi-pane screens):
- Header: <contents, e.g. logo, nav, user avatar>
- Main:
  - <element 1 — e.g. "Search bar, full width">
  - <element 2 — e.g. "Grid of result cards, 3 columns on desktop / 1 on mobile">
- Footer / sidebar (if applicable): <contents>

**Primary action**: <the one main thing a user does here, e.g. "Submit search">
**Secondary actions**: <other available actions, e.g. "Filter", "Sort", "Save">

**States**:
- Empty: <what shows when there's no data yet>
- Loading: <what shows while fetching>
- Error: <what shows on failure, and recovery action>
- Success/populated: <default populated view, if not already covered by Layout>

**Responsive behavior** (if platform requires): how layout adapts between breakpoints (e.g. mobile stacks vertically, desktop uses a 2-column split).

**Notes**: anything else relevant — e.g. this screen reuses the `Card` component from the design system, or has a modal variant.
```

## Guidance

- Describe in enough detail that a developer or coding agent could build the screen without guessing, but don't invent pixel-level specs (exact px values, hex codes inline here) — those live in the design system doc and get referenced, not restated per screen.
- Reference design-system components by name (e.g. "uses `PrimaryButton`") once the design system section exists, rather than describing button styling per screen.
- Every screen that appears as a node in a flow diagram (Unit 2) should have a corresponding entry here with a matching name.