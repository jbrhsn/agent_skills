# platform-adapter

Takes one platform-neutral source draft and reshapes it into platform- and type-specific versions for LinkedIn and/or Medium, following the content-type matrix. It re-cuts the same core idea per platform, not a different piece, adapting voice by content type AND platform, and writes the results into `linkedin/` and `medium/`.

---

## Trigger phrases

| Input | Example |
|---|---|
| Adapt for LinkedIn | "adapt for LinkedIn", "make a LinkedIn version" |
| Make a Medium version | "make a Medium version", "turn this into a Medium deep dive" |
| Format for posting | "format this for posting", "give me both" |

Do **not** use it to generate ideas (use `seed-expander`), to build the source draft itself (use `draft-builder`), to render carousel images (use `carousel-builder`, since this skill emits slide copy only), to execute tutorial code (use `tutorial-verifier`), or to produce edited variants (use `editorial-reviewer`).

---

## What it does

- **Reads the source draft and confirms expected outputs.** Before generating anything, asks the user what outputs they expect (LinkedIn and/or Medium types, carousel copy, tutorial) and stops for the answer, then determines the best-fit content-type from the draft's substance. A step-by-step with code becomes a Tutorial, a numbered structure a Listicle, a single sharp insight a Short, a layered argument a Long/Article. If the type is ambiguous, it asks rather than guesses.
- **Offers LinkedIn format options.** Because the user prefers a mix of formats, it MUST present the 2-3 LinkedIn format menu (Short Post, Long Post, Carousel outline) and get an explicit selection BEFORE generating any LinkedIn file, never defaulting to a single format.
- **Reshapes rather than rewrites.** Re-cuts the SAME core idea per platform, applying the platform tone rules and the matrix constraints (length, formatting). It does not write a different piece.
- **Adapts voice per platform.** Reads `voice-tone/` if present; voice adapts by both content type and platform.
- **Applies platform formatting.** LinkedIn Short/Long get line-break and scannability formatting; LinkedIn Article and Medium Long get headers/subheadings; Medium Tutorial gets steps plus fenced code blocks (without claiming the code is verified); LinkedIn Carousel gets structured slide copy emitted as JSON for `carousel-builder`.
- **Review-first (mandatory stop).** Presents all generated versions/options and stops. The user picks, tweaks, or rejects before anything is written.
- **Runs a voice-compliance gate before writing.** Before persisting any platform file, it scans the generated text against the `voice-tone/` profile's avoided words/phrases and punctuation rules, auto-fixes mechanical violations, and flags judgment calls for you. Skips silently if no voice-tone exists.
- **Persists after approval.** Writes LinkedIn versions to `linkedin/<slug>-<type>.md`, Medium versions to `medium/<slug>-<type>.md`, and carousel slide JSON to `linkedin/carousels/<slug>/slides.json`, then confirms the paths.

---

## Content-type matrix

| Platform | Type | Length | Notes |
|---|---|---|---|
| LinkedIn | Short Post | 100-300 w | Hook-heavy, line-break formatted |
| LinkedIn | Long Post | 600-1200 w | Narrative, native feed, no images |
| LinkedIn | Article | 1000+ w | Native publishing, headers/images |
| LinkedIn | Carousel | 8-12 slides | Slide COPY only here; images via carousel-builder |
| Medium | Short Article | 3-5 min | Punchy, single-insight |
| Medium | Long Article | 8-12 min | Deep dive, multiple sections |
| Medium | Tutorial | varies | Code blocks, step-by-step |
| Medium | Listicle | varies | Numbered/structured list |

---

## Platform tone rules

- **LinkedIn**: more direct, personal, first-person; short punchy lines with deliberate line breaks and whitespace; a strong scroll-stopping hook in the first 1-2 lines; scannable.
- **Medium**: more considered and essayistic; real subheadings; longer paragraphs allowed; title + subtitle + section structure.

---

## Workflow

| Step | What happens |
|---|---|
| **1. Read source + confirm expected outputs** | Read the draft; ask the user which outputs they expect (LinkedIn and/or Medium types, carousel copy, tutorial) and stop for their answer; detect the best-fit content-type per target (ask if ambiguous); present the 2-3 LinkedIn format menu before generating any LinkedIn file |
| **2. Produce the versions** | Re-cut the same core idea per platform, applying tone rules and matrix constraints; emit carousel copy as JSON; structure tutorials with code blocks but do not claim verification |
| **3. Review-first (stop)** | Present all versions/options and stop; user picks, tweaks, or rejects |
| **4. Persist** | Write to `linkedin/<slug>-<type>.md`, `medium/<slug>-<type>.md`, and `linkedin/carousels/<slug>/slides.json`; confirm the paths; runs the voice-compliance gate before writing |

Carousel slide copy is emitted in the JSON schema `carousel-builder` expects:

```json
{"slug":"<slug>","slides":[{"title":"...","body":"...","footer":"@handle"}]}
```

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Source draft | Yes | A platform-neutral draft (from `draft-builder` or the user's own) read from `drafts/` |
| Target platform(s) | Yes | LinkedIn, Medium, or both; asked at the start |
| Content-type | Optional | Auto-detected from the draft; the skill asks when ambiguous |
| `linkedin/` / `medium/` folders | For persistence | Output folders; the skill asks how to proceed if a needed one is missing |
| `voice-tone/` folder | Optional | Voice samples + style instructions; voice adapts per platform and type |

---

## Outputs

- **2-3 LinkedIn format options** and/or the requested Medium version(s), re-cut from the same core idea and formatted per platform.
- **LinkedIn versions** at `linkedin/<slug>-<type>.md` and **Medium versions** at `medium/<slug>-<type>.md`.
- **Carousel slide copy** as JSON at `linkedin/carousels/<slug>/slides.json` (input for `carousel-builder`).
- **A confirmation** of the written paths.

---

## Limitations

- **Reshapes, never re-conceives.** It re-cuts the source draft; it does not write a different piece.
- **Emits carousel copy only.** It never renders images; that is `carousel-builder`.
- **Never claims tutorial code is verified.** Medium Tutorials are structured with code blocks but handed off to `tutorial-verifier` for actual execution.
- **Never silently creates folders** and **never silently overwrites.** It asks how to proceed if a needed output folder is missing or a target file exists.
- **Stops for review** before writing anything.
- **Tracker updates are prompted, not automatic.** If a `content-log.md`/`content-log.json` tracker exists, the skill asks in one line whether to update it after writing; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global: available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/platform-adapter ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/platform-adapter .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\platform-adapter "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/platform-adapter.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the content task |

---

## Companion skills

`platform-adapter` is the third stage of the LinkedIn/Medium content pipeline: **seed-expander → draft-builder → platform-adapter → {carousel-builder, tutorial-verifier} → editorial-reviewer**, with `voice-profiler` and `content-tracker` as cross-cutting support.

- **`draft-builder`**: produces the source draft this skill reshapes (the previous stage)
- **`carousel-builder`**: renders the carousel slide JSON this skill emits into SVG/HTML/PNG slides
- **`tutorial-verifier`**: runs and verifies the code in tutorial versions this skill produces
- **`editorial-reviewer`**: produces 2-3 edited variants of any version to choose from
- **`seed-expander`**: generates the ideas at the start of the pipeline
- **`voice-profiler`**: builds the `voice-tone/` profile this skill reads to adapt voice
- **`content-tracker`**: tracks each piece's status across the pipeline
