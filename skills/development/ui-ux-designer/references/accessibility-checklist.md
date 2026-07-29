# Accessibility checklist

Only used when the user explicitly asks for an accessibility section (Phase 6). Add a section to `docs/ux-design.md` covering:

```markdown
## Accessibility

### Color & Contrast
- Text/background contrast meets WCAG AA (4.5:1 normal text, 3:1 large text/UI components) — call out any palette colors from the design system that need adjustment to pass.
- Color is never the sole indicator of state (e.g. errors also use icon/text, not just red).

### Keyboard Navigation
- All interactive elements reachable via Tab, in a logical order matching visual layout.
- Visible focus states defined for every interactive component (link this to the design system's component states).
- Modals/dialogs trap focus and return it on close; Escape closes overlays.

### Screen Readers
- Meaningful alt text planned for informative images; decorative images marked appropriately.
- Form inputs have associated labels (not placeholder-only).
- Dynamic content changes (toasts, loading states) use appropriate live-region announcements.

### Motion & Interaction
- Respect reduced-motion preference for any planned animations/transitions.
- Touch targets sized appropriately for mobile (44x44pt minimum as a reference point).
```

## Guidance

- Keep this concrete and tied back to the specific screens/components already designed — don't produce a generic WCAG essay disconnected from the actual app.
- Flag specific conflicts if found (e.g. a chosen color pairing in the design system fails contrast) rather than just listing the rule.