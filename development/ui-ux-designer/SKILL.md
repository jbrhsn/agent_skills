---
name: ui-ux-designer
description: Designs the UI and UX for an app — user flows, screen layouts, and a design system — and writes them to docs/ux-design.md. Use whenever the user asks to design, revise, or think through UI/UX, screens, user flows, wireframes, layouts, or the "look and feel" of an app, or invokes "/design-ux". Also use to revise an existing docs/01-spec.md / docs/02-design.md based on UX decisions. First assesses whether the project even has a user-facing interface — for CLI tools, APIs, or backend-only services it says so and stops rather than fabricating screens. Do NOT use for general project planning (project-planner) or writing code (lean-coder).
metadata:
  category: design
  audience: designers-developers
  outputs: docs/ux-design.md
---

# UI/UX Designer

Designs user flows, screen layouts, and a design system for an app, and writes them to `docs/ux-design.md`. Can also revise an existing project spec/design (e.g. from the `project-planner` skill) to reflect UX-driven changes. This skill has no image-generation capability — all layouts are represented as Mermaid diagrams (for flows) and structured text descriptions (for screen layout), never as images.

## Output file

`docs/ux-design.md` at the repo root — a single file containing user flows, screen-by-screen layout descriptions, and the design system.

If `docs/01-spec.md` and/or `docs/02-design.md` exist (from `project-planner` or elsewhere), this skill reads them first and treats them as the source of truth for scope and users. If they don't exist, it works standalone and asks for what it needs directly.

## Workflow

### Phase 0: Assess whether UI/UX work applies

Before anything else, determine whether the project has a user-facing interface at all:

- If `docs/01-spec.md` / `docs/02-design.md` exist, read them for project type and stated interfaces.
- Otherwise ask the user directly, or infer from context already in the conversation.
- If the project is clearly CLI-only, an API/backend service with no UI, a library, or similar with no human-facing screens, **say so and stop** — don't fabricate screens for a project that doesn't have any. It's fine to note that a CLI still has "UX" in the sense of command ergonomics/output design; ask the user if they want that lighter-weight treatment instead of full screen/flow design, and adapt scope accordingly rather than forcing the full template. If they accept the CLI treatment, **use `references/cli-ergonomics-template.md`** (command structure, flags, output/error design, exit codes, help) to write `docs/ux-design.md` — skip Phases 3-5, which are screen/flow-specific, and go straight to that template.
- A **TUI** (text-based full-screen interface, e.g. curses/ncurses apps) counts as a genuine user-facing surface — proceed to Phase 1 with the normal screen/flow treatment. A plain command-line tool (flags in, text out, no full-screen interface) does not; it takes the CLI-ergonomics path above.
- If there's a genuine user-facing surface (web app, mobile app, desktop app, browser extension, even a TUI), proceed to Phase 1.

### Phase 1: Gather context

- If `docs/01-spec.md` and `docs/02-design.md` exist, **delegate reading them to an `explore` subagent** (via the Task tool) instead of pulling both full docs into the main thread — you only need the design-relevant briefing, not the raw docs, in your working context. Ask the subagent to extract and report: target users, core features, platform (web/mobile/desktop), tech stack (relevant for component/design-system choices, e.g. if they're already using Tailwind or a component library), and any stated accessibility requirements (needed for Phase 6). When the docs are short, only one exists, or subagents aren't available, just read it directly — a subagent would be overhead.
- Don't re-ask the user for anything already answered in those docs.

The interview (Phase 2), flow/screen/design-system work (Phases 3–5), and approval (Phase 7) stay in this primary session — subagents here are only for the read-heavy context gathering in this phase.

### Phase 2: Interview

Interview the user in **batches of 5 questions**, same style as `project-planner`, using the `question` tool where available (or plain numbered questions in chat if that tool isn't available in this environment). Skip anything already answered by the spec/design docs or earlier in the conversation. Cover:

- **Users & context of use**: who's using it, on what device, in what setting (quick mobile glances vs. focused desktop sessions), technical sophistication
- **Core user flows**: the 2-5 most important things a user does in this app, end to end
- **Platform & constraints**: web/mobile/desktop/responsive-all; any existing component library or design system to align with (e.g. Material, shadcn, company brand kit); light/dark mode requirements
- **Visual tone**: reference apps/sites they like, general feel (minimal/playful/dense/enterprise), any brand colors or existing identity to respect
- **Screens/scope**: rough list of distinct screens or views needed, and whether any screen is especially complex/high-stakes and deserves extra design attention

Proceed once you have enough to design flows and screens without major guesswork; note real gaps as open questions rather than blocking indefinitely.

**When the `question` tool is unavailable** (non-interactive environment, or the user is not present to answer): fall back to plain numbered questions in your reply. If you also cannot get answers at all (batch/automated run), do NOT block — proceed by designing with your best-reasoned assumptions, and record every assumption explicitly as open questions in `docs/ux-design.md` so the user can correct them later.

### Phase 3: Design user flows

For each core flow identified in the interview, produce a Mermaid flowchart showing the step-by-step path through screens/states, including key decision points and error/edge paths (e.g. failed login, empty states).

Use `references/flow-diagram-guide.md` for Mermaid syntax patterns for this.

### Phase 4: Design screens

For each screen in scope, write a structured text layout description — not ASCII art, not an image. Use `references/screen-template.md`. Each screen description covers: purpose, key elements top-to-bottom (or by region: header/main/footer/sidebar), primary and secondary actions, states (empty/loading/error/success where relevant), and responsive behavior if the platform requires it.

### Phase 5: Define the design system

Always include a design system section — this is required, not optional. Use `references/design-system-template.md`. Covers:

- Color palette (primary/secondary/neutral/semantic colors like success/error/warning), with light/dark mode values if applicable
- Typography scale (font family, size/weight/line-height for headings, body, captions)
- Spacing scale (base unit and multiples)
- Core reusable components (buttons, inputs, cards, etc.) with states (default/hover/active/disabled)

If the interview revealed an existing component library or brand kit, build the design system as a thin layer on top of it (map to its tokens) rather than inventing a parallel system from scratch.

### Phase 6: Accessibility (only if requested)

Do not include an accessibility section by default. If the user asks for it (during the interview or afterward), add a section covering contrast ratios, keyboard navigation, screen-reader considerations, and focus states, using `references/accessibility-checklist.md`.

**Exception — when the source spec makes accessibility a requirement:** if `docs/01-spec.md` (or the user's brief) lists accessibility as a functional or non-functional requirement (e.g. screen-reader support, keyboard-only operation, WCAG targets), don't silently omit it. Either include the accessibility section, or — if the user hasn't explicitly asked for the full section — proactively flag that the spec requires accessibility, offer to add the section, and in the meantime still respect a11y in your design choices (state non-color error signals, focus states on components, adequate touch/click targets) rather than deferring them entirely.

### Phase 7: Write docs/ux-design.md

Assemble Phases 3-6 into `docs/ux-design.md`. Present it to the user and get approval/revisions before considering the UX design done.

### Phase 8: Propagate changes back to spec/design docs

If `docs/01-spec.md` and/or `docs/02-design.md` exist and the UX work surfaced changes to scope, requirements, or architecture (e.g. a flow revealed a missing feature, a screen implies a new API endpoint, a design system choice implies a new frontend dependency), tell the user what changed and why, then:

- Update `docs/01-spec.md` if scope/requirements changed (e.g. add a feature that emerged from flow design, note a new non-functional requirement like "must support dark mode").
- Update `docs/02-design.md` if architecture/stack implications emerged (e.g. a component library choice, a new client-side dependency).
- Never edit these files silently — always summarize the proposed change and confirm before writing, since they may have been approved by the user in a separate planning pass.
- If neither file exists, skip this phase — there's nothing to propagate into.

## Notes

- No image generation is available in this environment. Never claim to produce a wireframe image, mockup, or Figma file — everything is Mermaid diagrams and structured text.
- Keep screen descriptions concrete and implementation-relevant (an engineer or coding agent should be able to build the screen from the description) without over-specifying pixel values that weren't requested.
- If this skill is invoked mid-way through a `project-planner` run (e.g. right after `02-design.md` is approved), it's fine to run immediately rather than waiting for the roadmap/backlog phases — UX design informs the roadmap, so earlier is better.

## Related skills & doc ownership

This skill **owns `docs/ux-design.md`**. `docs/01-spec.md` and `docs/02-design.md` are owned by **`project-planner`** — this skill treats them as read-only source of truth and may only *propose* changes (Phase 8), never silently rewrite them. Always summarize a proposed spec/design edit and get confirmation before writing, since the user may have approved those docs in a separate planning pass. After UX design, **`lean-coder`** implements the screens/flows. For publishing an existing repo's user docs, that's **`repo-docs-publisher`**, not this skill.