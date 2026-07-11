# editorial-reviewer

Runs a finished LinkedIn post/article or Medium article through a structured editorial pass and returns **2-3 labeled edited variants** for the user to choose, mix, or reject. This skill is **review-first**: it presents options, then STOPS. Nothing is written until the user picks.

---

## Trigger phrases

| Input | Example |
|---|---|
| Review / polish finished text | "review this post", "edit this", "polish this", "tighten this up", "sharpen the point" |
| Ask for alternate angles | "make it more contrarian", "give me a tighter hook", "give me variants", "give me 4 versions" |
| Pasted text or a file | Paste the piece directly, or point to a file in `drafts/`, `linkedin/`, or `medium/` |

Runs standalone on any pasted text or file, and also naturally receives output handed off from `platform-adapter`.

Do **not** use it to expand a raw idea into an outline (that is `seed-expander`), build a full draft from scratch (that is `draft-builder`), reshape a draft for a specific platform (that is `platform-adapter`), build carousels (that is `carousel-builder`), or verify tutorial/code steps (that is `tutorial-verifier`).

---

## What it does

- **Detects platform and type first.** Reads the pasted text or file and infers whether it is a LinkedIn piece (short, punchy, first-person, no subheadings) or a Medium article (long-form, subheadings, section structure). If the platform is unclear, it ASKS before proceeding.
- **Diagnoses against 5 dimensions.** Gives a brief, per-dimension read of what is strong and what is weak before producing variants.
- **Produces 2-3 labeled variants.** Each variant emphasizes different review dimensions, carries a short editorial-angle label, and includes a one-line diagnostic of what changed and why.
- **Runs a per-platform mechanical/formatting pass.** LinkedIn variants get short lines, generous whitespace, a strong first 1-2 lines, and scannable breaks; Medium variants get clear subheadings, logical section structure, and readable paragraph length, so every variant is platform-ready.
- **Uses voice material when available.** If a cwd-relative `voice-tone/` folder exists, it reads it to judge voice authenticity and keep edits sounding like the user. If a voice-tone folder is expected but missing, it asks how to proceed rather than guessing.
- **Stops before writing.** Presents all variants and diagnostics, then STOPS and asks the user to choose, mix, or reject. It never picks for the user and never auto-writes.
- **Writes only the chosen version.** After the user picks, it confirms the target folder (`linkedin/` or `medium/`, cwd-relative), asks how to proceed if that folder is missing, writes the chosen or mixed version, and confirms the exact path back. Before writing the chosen version, it runs a voice-compliance gate: scans against the voice-tone profile's avoided words/phrases and punctuation, auto-fixes mechanical violations, and flags judgment calls.
- **Iterates on request.** The chosen variant can be fed back in as new input for another fresh round of variants.
- **Persists standing style rules.** If you state a standing style rule during review (for example, no em-dashes), it offers to persist that rule to `voice-tone/profile.md` so every skill inherits it.

---

## Review dimensions

Every piece is evaluated against these five dimensions, and different variants deliberately emphasize different ones:

| # | Dimension | Question it answers |
|---|---|---|
| 1 | **Hook strength** | Does the opening earn the next line? |
| 2 | **Clarity / tightness** | Is filler cut, phrasing tightened, the point sharpened? |
| 3 | **Contrarian angle** | Is there a sharper, more differentiated take? |
| 4 | **Voice authenticity** | Does it still sound like the user (per `voice-tone/`)? Explicitly scans each variant against the voice profile's avoided words/phrases and punctuation, auto-fixing mechanical bans and flagging judgment calls. |
| 5 | **Scannability** | Is it easy to skim on the target platform? |

---

## Variants output

Default is 2-3 numbered variants, each with a short editorial-angle label and a one-line "what changed and why" diagnostic. Each variant also reports a "voice check:" line stating passed / N auto-fixed / M flagged against the profile's avoided list. Typical shapes:

- **Variant 1 (Tighter hook):** rewrites the opening for immediate pull.
- **Variant 2 (More contrarian):** pushes a sharper, differentiated take.
- **Variant 3 (Safer / more polished):** cleaner, lower-risk, broadly shareable.

If the user asks for a specific number (e.g. "give me 4"), that count is honored.

---

## Workflow

1. **Intake + detect platform/type**: read the text/file; infer LinkedIn vs Medium; ask if unclear.
2. **Analyze against the 5 dimensions**: a short per-dimension diagnostic of strengths and weaknesses.
3. **Produce 2-3 labeled variants**: numbered, angle-labeled, each with a one-line change diagnostic.
4. **Mechanical / formatting pass**: apply the per-platform formatting so each variant is platform-ready.
5. **Mandatory review-first STOP**: present everything, then STOP; the user chooses, mixes, or rejects. Nothing is written.
6. **Write the chosen version**: only after the pick: confirm the target folder, ask if it is missing (never auto-create), write the chosen/mixed version, and report the exact path; runs the voice-compliance gate before writing.

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Finished piece | Yes | Pasted text, or a file in `drafts/`, `linkedin/`, or `medium/` to review |
| Platform / type | If unclear | LinkedIn vs Medium; the skill asks when it cannot infer it |
| `voice-tone/` material | Optional | Voice/tone reference (samples or `profile.md`) used to judge voice authenticity |
| Variant count | Optional | Overrides the 2-3 default when the user requests a specific number |

---

## Outputs

- A short per-dimension diagnostic of the piece's strengths and weaknesses.
- **2-3 labeled, platform-formatted variants**, each with a one-line "what changed and why" and a "voice check:" line reporting passed / N auto-fixed / M flagged against the profile's avoided list.
- Only after the user chooses: the chosen (or mixed) version written to `linkedin/` or `medium/` (cwd-relative), with the exact path confirmed.

---

## Limitations

- **Review-first, never auto-writes.** It always STOPS after presenting variants and never picks, approves, or replaces the user's text on its own.
- **Never auto-creates folders.** If the target folder is missing, it asks how to proceed.
- **Never silently overwrites.** If the target file exists, it asks to overwrite, write a `-v2` (then `-v3`...) variant, or pick a new name.
- **Does not author from scratch.** It reviews and edits finished pieces; it is not for expanding ideas, drafting, or platform reshaping.
- **Tracker updates are optional.** After writing, the skill ASKS in one line whether to update the `content-log.json`/`content-log.md` tracker; a missing tracker never blocks the skill.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global: available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/editorial-reviewer ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/editorial-reviewer .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\editorial-reviewer "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/editorial-reviewer.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the review task |

---

## Companion skills

Part of the LinkedIn/Medium content suite. Pipeline order: `seed-expander` -> `draft-builder` -> `platform-adapter` -> {`carousel-builder`, `tutorial-verifier`} -> **`editorial-reviewer`**.

- **`seed-expander`**: expands a raw idea into structured angles/outline
- **`draft-builder`**: turns an expanded seed into a full draft
- **`platform-adapter`**: reshapes a draft for LinkedIn or Medium
- **`carousel-builder`**: builds LinkedIn carousels
- **`tutorial-verifier`**: verifies tutorial/code steps before publishing
- **`voice-profiler`**: produces the optional `voice-tone/profile.md` this skill reads for voice authenticity
- **`content-tracker`**: optional cross-session pipeline tracker that can record the reviewed status

`editorial-reviewer` is the final polish stage before a piece is posted.
