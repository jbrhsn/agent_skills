---
name: ui-ux-designer
description: Use when the user asks to design, revise, or think through the UI/UX of an app — user flows, screen layouts, a design system, wireframes, or the "look and feel" — or invokes "/design-ux". It first assesses whether the project even has a user-facing interface and, for CLI-only tools, APIs, or backend/library projects with no screens, says so and stops rather than fabricating screens (offering a lighter CLI-ergonomics treatment instead). For genuine UI surfaces it produces user flows (Mermaid), screen layouts (structured text), and a design system, writes them to docs/ux-design.md, and can propose confirmed revisions back to an existing docs/01-spec.md / docs/02-design.md. Do NOT use for general project planning (project-planner) or writing code (lean-coder).
metadata:
  category: design
  audience: designers-developers
  outputs: docs/ux-design.md
---

# UI/UX Designer

Designs user flows, screen layouts, and a design system for an app, and writes them to `docs/ux-design.md`. Can also propose revisions to an existing project spec/design (e.g. from the `project-planner` skill) to reflect UX-driven changes. This skill has no image-generation capability — all layouts are Mermaid diagrams (for flows) and structured text descriptions (for screen layout), never images.

## Output file

`docs/ux-design.md` at the repo root — a single file containing user flows, screen-by-screen layout descriptions, and the design system. For a plain command-line tool it instead holds a command-ergonomics design (see the CLI fork in Unit 0 / Unit 5).

---

## Shared conventions (defined once — every unit references these; do not restate)

**Source-of-truth docs.** `docs/01-spec.md` and `docs/02-design.md` (from `project-planner` or elsewhere) are the **read-only** source of truth for scope, users, platform, and requirements. This skill **owns `docs/ux-design.md`** and may only *propose* edits to the spec/design docs (Unit 6), never silently rewrite them. If neither spec/design doc exists, work standalone and gather what's needed directly. Never re-ask the user for anything already answered in those docs or earlier in the conversation.

**No image generation.** Never claim to produce a wireframe image, mockup, or Figma file. Flows are Mermaid diagrams; screens are structured text; nothing is an image.

**Concreteness.** Keep screen descriptions concrete and implementation-relevant — an engineer or coding agent should be able to build the screen from the description — without over-specifying pixel values that weren't requested.

**Existing design system.** If the interview reveals an existing component library or brand kit (Material, shadcn, company brand, Tailwind, etc.), build the design system as a thin layer mapping to its tokens rather than inventing a parallel system.

**Reference files (in `references/`).** Use the matching template for each artifact:
- `flow-diagram-guide.md` — Mermaid syntax patterns for flows (Unit 2).
- `screen-template.md` — screen layout structure (Unit 3).
- `design-system-template.md` — design-system structure (Unit 4).
- `accessibility-checklist.md` — accessibility section (Unit 4a).
- `cli-ergonomics-template.md` — CLI command-ergonomics doc (CLI fork).

**Non-interactive fallback (applies to every interview/approval gate).** Where the `question` tool is available, use it; otherwise fall back to plain numbered questions in chat. If answers cannot be obtained at all (batch/automated run), do NOT block: proceed with best-reasoned assumptions and record every assumption explicitly as an open question in `docs/ux-design.md`. At approval gates in a non-interactive run, note the gate as "skipped — auto-proceeding as designed" and continue rather than silently omitting it.

**Reporting.** Each unit ends with a terse structured report — no pasted diagrams, doc bodies, or raw output.

---

## Workflow (delegation-model units)

The units run in order. Unit 0 is a mandatory gate that can abort the whole skill. The CLI fork (from Unit 0) skips Units 2–4 and goes straight to the CLI path in Unit 5.

### Unit 0 — Assess whether UI/UX work applies (STOP GATE — abort if no UI surface)

- **Goal/scope**: decide, before any design work, whether the project has a genuine user-facing interface. This is a hard gate that can abort the skill.
- **Inputs**: `docs/01-spec.md` / `docs/02-design.md` if present (project type, stated interfaces); otherwise context already in the conversation, or a direct question to the user.
- **Do**: determine the surface type:
  - **Genuine UI surface** — web app, mobile app, desktop app, browser extension, or a **TUI** (text-based full-screen interface, e.g. curses/ncurses). Proceed to Unit 1 with the normal screen/flow treatment.
  - **Plain command-line tool** (flags in, text out, no full-screen interface) — this is **not** a screen/flow surface. Note that a CLI still has "UX" in the sense of command ergonomics/output design, and offer the lighter CLI-ergonomics treatment instead of the full template.
  - **No human-facing surface at all** — API/backend service, library, or similar with no screens and no meaningful CLI ergonomics to design.
- **Self-verify**: the surface type is explicitly classified into exactly one of the three cases above, with one line of reasoning.
- **STOP GATE (hand back)**:
  - If **no UI surface** (API/backend/library): **say so and STOP** — do not fabricate screens. Hand back to the user/orchestrator with the reason; the skill aborts here.
  - If **plain CLI**: present the CLI-ergonomics offer and **stop for the user's choice** (full-treatment-not-applicable vs. accept CLI ergonomics). On acceptance, take the **CLI fork**: skip Units 2–4 and go to Unit 5's CLI path using `references/cli-ergonomics-template.md`.
  - If **genuine UI surface**: no hand-back needed; proceed to Unit 1.
  - → In the abort and CLI-offer cases, control returns to the user/orchestrator before any design work.
- **Report contract**: `surface: <UI | TUI | CLI | none> (<reason>) | decision: <proceed to Unit 1 | CLI fork | ABORT — no UI surface> | awaiting: <none | CLI-treatment confirmation>`.

### Unit 1 — Gather context

- **Goal/scope**: assemble a design-relevant briefing without pulling full spec/design docs into the working thread.
- **Inputs**: `docs/01-spec.md` / `docs/02-design.md` if present.
- **Do**: if both docs exist and are non-trivial, **delegate reading them to an `explore` subagent** (via the Task tool) and ask it to extract and report only: target users, core features, platform (web/mobile/desktop), tech stack (relevant for component/design-system choices — e.g. existing Tailwind or component library), and any stated accessibility requirements. When the docs are short, only one exists, or subagents aren't available, read directly — a subagent would be overhead.
- **Self-verify**: the briefing covers users, core features, platform, stack, and any accessibility requirement (or explicitly notes each as absent); nothing already answered will be re-asked in Unit 1a.
- **Report contract**: `context source: <spec/design via explore | read inline | conversation only> | briefing: users/features/platform/stack/a11y captured`.

### Unit 1a — Interview (STOP GATE — gather answers before designing)

- **Goal/scope**: get the human input needed to design flows and screens without major guesswork.
- **Inputs**: the Unit 1 briefing; the `question` tool if available.
- **Do**: interview in **batches of 5 questions** (same style as `project-planner`). Skip anything already answered by the spec/design docs or earlier conversation. Cover:
  - **Users & context of use** — who uses it, on what device, in what setting (quick mobile glances vs. focused desktop sessions), technical sophistication.
  - **Core user flows** — the 2–5 most important end-to-end things a user does.
  - **Platform & constraints** — web/mobile/desktop/responsive-all; any existing component library/design system to align with; light/dark mode requirements.
  - **Visual tone** — reference apps/sites they like, general feel (minimal/playful/dense/enterprise), brand colors or existing identity to respect.
  - **Screens/scope** — rough list of distinct screens/views, and whether any is especially complex/high-stakes and deserves extra attention.
- **Self-verify**: enough is known to design flows and screens; real remaining gaps are recorded as open questions rather than blocking indefinitely.
- **STOP GATE (hand back)**: pause for the user's answers before designing. Per the shared non-interactive fallback, use plain numbered questions if the `question` tool is unavailable; in a fully automated run, do NOT block — proceed with best-reasoned assumptions and record each as an open question in the output. → Hand control back for the interview answers.
- **Report contract**: `interview: <N batches asked | fallback numbered | auto-assumed> | open questions: <count> | ready to design: yes`.

### Unit 2 — Design user flows

- **Goal/scope**: produce a Mermaid flowchart for each core flow. *(Skipped on the CLI fork.)*
- **Inputs**: the interview's core-flow list; `references/flow-diagram-guide.md`.
- **Do**: for each core flow, produce a Mermaid flowchart showing the step-by-step path through screens/states, including key decision points and error/edge paths (e.g. failed login, empty states). Follow the Mermaid syntax patterns in `references/flow-diagram-guide.md`.
- **Self-verify**: every core flow from the interview has a corresponding flowchart; each includes at least one decision point and its error/edge paths; Mermaid syntax matches the guide.
- **Report contract**: `flows: N produced (one per core flow) | edge/error paths included: yes`.

### Unit 3 — Design screens

- **Goal/scope**: write a structured text layout for each screen in scope. *(Skipped on the CLI fork.)*
- **Inputs**: the interview's screen/scope list; the Unit 2 flows; `references/screen-template.md`.
- **Do**: for each screen, write a structured text layout description (not ASCII art, not an image) using `references/screen-template.md`. Each covers: purpose; key elements top-to-bottom or by region (header/main/footer/sidebar); primary and secondary actions; states (empty/loading/error/success where relevant); and responsive behavior if the platform requires it.
- **Self-verify**: every in-scope screen has a description covering purpose, elements, actions, states, and (where relevant) responsive behavior; descriptions are concrete enough to build from per the shared concreteness rule.
- **Report contract**: `screens: N described (per template) | states + responsive covered where relevant`.

### Unit 4 — Define the design system

- **Goal/scope**: produce the required design-system section. *(Skipped on the CLI fork.)*
- **Inputs**: the interview's visual-tone/platform answers; any existing library/brand kit; `references/design-system-template.md`.
- **Do**: always include a design system (required, not optional) using `references/design-system-template.md`, covering:
  - Color palette (primary/secondary/neutral/semantic like success/error/warning), with light/dark values if applicable.
  - Typography scale (font family; size/weight/line-height for headings, body, captions).
  - Spacing scale (base unit and multiples).
  - Core reusable components (buttons, inputs, cards, etc.) with states (default/hover/active/disabled).
  - Per the shared "existing design system" rule, layer onto any revealed component library/brand kit rather than inventing a parallel system.
- **Self-verify**: all four areas (color, typography, spacing, components-with-states) are present; where a library/brand kit exists, tokens map onto it.
- **Report contract**: `design system: color/typography/spacing/components all present | layered on existing kit: <yes/no>`.

### Unit 4a — Accessibility (only if requested or spec-required)

- **Goal/scope**: add an accessibility section when — and only when — warranted. *(Skipped on the CLI fork unless requested.)*
- **Inputs**: the user's request (if any); accessibility requirements found in `docs/01-spec.md` / the brief; `references/accessibility-checklist.md`.
- **Do**: do **not** include accessibility by default. Add it if the user asks (in the interview or after), covering contrast ratios, keyboard navigation, screen-reader considerations, and focus states via `references/accessibility-checklist.md`. **Exception — spec-required a11y:** if the spec or brief lists accessibility as a functional/non-functional requirement (screen-reader support, keyboard-only, WCAG targets), don't silently omit it: either include the section, or — if the user hasn't explicitly asked for the full section — proactively flag that the spec requires it, offer to add it, and meanwhile still respect a11y in design choices (non-color error signals, focus states on components, adequate touch/click targets) rather than deferring entirely.
- **Self-verify**: section present when requested or spec-required; when spec-required but not fully written, the flag/offer is recorded and a11y is still respected in the design; otherwise correctly omitted.
- **Report contract**: `accessibility: <included | flagged spec-required, a11y respected | omitted (not requested)>`.

### Unit 5 — Write docs/ux-design.md (STOP GATE — approval before done)

- **Goal/scope**: assemble the artifacts into `docs/ux-design.md` and get approval.
- **Inputs**: on the normal path, the outputs of Units 2–4a. On the **CLI fork**, the `references/cli-ergonomics-template.md` structure (command structure, flags/arguments, output design, errors and exit codes, help/discoverability, interaction/safety) built from the Unit 1a answers.
- **Do**: assemble the content into `docs/ux-design.md` at the repo root — normal path: flows + screens + design system (+ accessibility if present); CLI fork: the command-ergonomics doc from the CLI template.
- **Self-verify**: confirm `docs/ux-design.md` was written to the expected repo-root path and contains the expected sections — **normal path**: the user-flows, screen-layout, and design-system sections (plus accessibility if applicable); **CLI fork**: the command-ergonomics sections from the template. Any auto-run assumptions are recorded as open questions in the file.
- **STOP GATE (hand back)**: present the assembled `docs/ux-design.md` to the user and **stop for approval/revisions** before considering the UX design done. Per the non-interactive fallback, auto-proceed with a noted gate if no user is present. → Hand control back for approval.
- **Report contract**: `wrote: docs/ux-design.md | sections: <flows/screens/design-system(+a11y) | CLI-ergonomics> | awaiting: approval/revisions`.

### Unit 6 — Propagate changes back to spec/design docs (STOP GATE — confirm before writing)

- **Goal/scope**: propose spec/design edits that the UX work surfaced. Runs only if `docs/01-spec.md` and/or `docs/02-design.md` exist and something changed.
- **Inputs**: the approved `docs/ux-design.md`; the existing spec/design docs.
- **Do**: if UX work surfaced scope/requirements or architecture/stack changes, identify them:
  - `docs/01-spec.md` — scope/requirements changes (e.g. a feature that emerged from flow design; a new non-functional requirement like "must support dark mode").
  - `docs/02-design.md` — architecture/stack implications (e.g. a chosen component library, a new client-side dependency).
  - If neither file exists, skip this unit — there's nothing to propagate into.
- **Self-verify**: proposed edits are correctly targeted (spec vs. design) and nothing is written before confirmation, per the shared read-only rule.
- **STOP GATE (hand back)**: never edit these files silently — summarize each proposed change and why, and **stop to confirm** before writing, since the user may have approved those docs in a separate planning pass. → Hand control back for confirmation. Only after confirmation, write the approved edits.
- **Report contract**: `propagation: <none needed | proposed N edits to spec/design> | awaiting: confirmation | written after confirm: <files or n/a>`.

---

## Notes

- No image generation is available in this environment. Never claim to produce a wireframe image, mockup, or Figma file — everything is Mermaid diagrams and structured text (see shared conventions).
- If this skill is invoked mid-way through a `project-planner` run (e.g. right after `02-design.md` is approved), it's fine to run immediately rather than waiting for the roadmap/backlog phases — UX design informs the roadmap, so earlier is better.

## Related skills & doc ownership

This skill **owns `docs/ux-design.md`**. `docs/01-spec.md` and `docs/02-design.md` are owned by **`project-planner`** — this skill treats them as read-only source of truth and may only *propose* changes (Unit 6), never silently rewrite them. Always summarize a proposed spec/design edit and get confirmation before writing, since the user may have approved those docs in a separate planning pass. After UX design, **`lean-coder`** implements the screens/flows. For publishing an existing repo's user docs, that's **`repo-docs-publisher`**, not this skill.
