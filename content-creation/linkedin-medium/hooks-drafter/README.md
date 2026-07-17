# hooks-drafter

Generates, scores, and selects high-performing opening hooks for LinkedIn posts or Medium articles. Applies research-grounded hook engineering: curiosity gap theory (inverted-U confidence curve), four independent psychological levers (specificity, negativity bias, arousal+low-dominance, gap precision), five typed hook patterns, platform-specific character and fold mechanics, a 7-dimension scoring rubric with a hard disqualifier, and a naturalness check that rejects generic variants a stranger could have written. Produces text output only — no files written.

---

## Trigger phrases

| Input | Example |
|---|---|
| Generate hooks | "draft hooks for X", "write me some hooks", "give me 5 hooks for this" |
| Evaluate an existing hook | "evaluate this hook", "score this hook", "is this hook good" |
| Sharpen a hook | "make this hook stronger", "sharpen my opening line", "give me hook variants" |

Do **not** use it to write the full post body (use `linkedin-writer` or `medium-writer`), for carousel slide titles (use `carousel-builder`), or for generating raw content ideas (use `seed-expander`).

---

## What it does

- **Detects platform (mandatory).** LinkedIn and Medium have different hook mechanics; asks which platform if unclear before generating anything.
- **Handles two entry paths.** If the user provides an existing hook to evaluate, goes directly to scoring (Step 3). If the user provides a topic or idea, generates fresh variants first.
- **Generates typed variants.** LinkedIn: 5 variants (one per type — Contrarian, Data/number, Story-in-motion, Problem-naming, Question). Medium: 4 variants (same set minus Question, which is weakest there) plus 3 subtitle variants for the top hook.
- **Applies four levers per variant.** Each variant uses at least two of: specificity, negativity bias, arousal+low-dominance, curiosity-gap precision. Notes which levers each variant employs.
- **Scores every variant on 7 dimensions.** PASS/FAIL per dimension. A FAIL on Payoff honesty is a hard disqualifier — that variant is replaced before being shown.
- **Applies a naturalness check to top variants.** Asks: "Could a stranger who has never met this person have written this?" If yes, generates a more specific replacement and reports why.
- **Mandatory stop after scoring.** Presents all variants + scorecards and stops. Nothing proceeds until the user picks.
- **Optional single-iteration refinement.** If the user picks a variant and requests a tweak, applies it, re-runs the rubric on the result, and delivers the final hook as clean pasteable text.

---

## Hook framework applied

| Framework element | Mechanic |
|---|---|
| Curiosity gap sweet spot | Inverted-U curve: too vague = no itch; too complete = no pull; sweet spot = reader forms a confident-but-incomplete guess |
| Specificity lever | Real numbers replace vague quantifiers; odd numbers outperform even (~20% higher CTR); specificity is both credibility and gap precision |
| Negativity bias lever | Mistake/failure/myth framing beats equivalent win/tip framing; one negative word ≈ +2.3% CTR vs positive language ≈ −1.0% |
| Arousal + low dominance | Hook spikes alertness (surprise, tension, stark claim) AND leaves exactly one specific thing unresolved |
| Hook type rotation | 5 types (Contrarian, Data/number, Story-in-motion, Problem-naming, Question); rotate to prevent pattern blindness |
| LinkedIn fold mechanics | First ~210–235 chars visible; each line under ~49 chars / ~10 words; no emojis; no throat-clearing; "see more" click = algorithmic signal |
| Medium title/subtitle | Title creates gap; subtitle adds new information (stake/outcome/constraint), never repeats the title; CTR without read-through is worthless |
| Payoff honesty (hard gate) | Hook's implicit promise must be deliverable by the actual content — oversell is a hard disqualifier, not just a deduction |

---

## Workflow

| Step | What happens |
|---|---|
| **1. Intake** | Read input (topic, idea, existing hook, or draft); confirm platform; if existing hook provided, skip to Step 3 |
| **2. Generate variants** | LinkedIn: 5 typed variants; Medium: 4 typed variants + 3 subtitles for top hook; note levers used per variant |
| **3. Score variants** | Run 7-dimension rubric on every variant; replace any Payoff-honesty FAIL before presenting; highlight top 1–2 with lever note |
| **4. Naturalness check** | Apply to top 1–2 variants; replace any generic variant; report if replacement was generated and why |
| **5. Mandatory stop** | Present all variants + scorecards + naturalness check; STOP for user to pick, tweak, or reject |
| **6. Finalize (optional)** | Apply requested tweak; re-run rubric; deliver final hook as clean pasteable text; one iteration maximum |

---

## Inputs

| Input | Required | Description |
|---|---|---|
| Topic, idea, or draft content | Yes | What the hook is for — a rough idea, bullets, a full draft, or an existing hook to evaluate |
| Target platform | Yes | LinkedIn or Medium; skill asks if unclear before generating |
| Recent post history | Optional | Last 2–3 post types, for the rotation check (Dimension 7 of the rubric) |
| `voice-tone/profile.md` | Optional | If present, naturalness check references "Avoided Words & Phrases" to flag banned patterns; absence never blocks the skill |

---

## Outputs

- **Typed hook variants** (5 for LinkedIn, 4 for Medium) with lever annotations.
- **3 subtitle variants** (Medium sessions only) for the top-ranked hook.
- **7-dimension rubric scorecard** per variant (PASS/FAIL per dimension).
- **Naturalness check result** per top variant, with replacement noted if triggered.
- **Final hook** as clean, pasteable text after user selection — no formatting, no file write.

---

## Limitations

- **Text output only. No files written.** Ever. There is no persist step.
- **LinkedIn and Medium only.** Hook mechanics for other platforms (Twitter/X, newsletters, etc.) are not encoded.
- **Platform must be confirmed.** The skill asks before generating — wrong-platform hooks underperform and will not be guessed at.
- **Question type skipped for Medium.** It is the weakest type there; Medium sessions get 4 variants instead of 5.
- **Payoff honesty is non-negotiable.** A hook that overpromises relative to the actual content is replaced, not tweaked.
- **One refinement iteration maximum** per session by default. Ask explicitly for additional rounds.
- **Naturalness check is subjective.** The check applies heuristics, not a definitive test — the user's judgment on what sounds "like them" is the final word.
- **Does not write the full post.** Use `linkedin-writer` or `medium-writer` to build the body around the selected hook.

---

## Install

Run from the **repo root** (`agent_skills/`):

```bash
# Global, available in all projects (Linux/macOS)
cp -r content-creation/linkedin-medium/hooks-drafter ~/.config/opencode/skills/

# Per-project only
cp -r content-creation/linkedin-medium/hooks-drafter .opencode/skills/

# Windows (PowerShell)
Copy-Item -Recurse content-creation\linkedin-medium\hooks-drafter "$env:USERPROFILE\.config\opencode\skills\"
```

### Other platforms

| Platform | How to use |
|---|---|
| **Claude Code** | Copy the content below the frontmatter into `CLAUDE.md` under a `## Workflows` section |
| **Cursor** | Paste into `.cursor/rules/hooks-drafter.mdc`, set rule type to `Agent Requested` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` under a clearly labelled heading |
| **ChatGPT / Claude (web)** | Paste the full skill content as your first message before the hook task |

---

## Companion skills

`hooks-drafter` is a cross-cutting support skill used at any point in the pipeline where a hook needs engineering or evaluation:

- **`linkedin-writer`**: calls `hooks-drafter` at Step 2 when deeper hook engineering is needed; selected hook plugs into the linkedin-writer session at the hook-selection gate
- **`medium-writer`**: calls `hooks-drafter` at Step 3 when deeper hook engineering is needed; selected hook (+ subtitle) plugs into the medium-writer session
- **`draft-builder`**: hook selected here can be pasted as the opening of a platform-neutral source draft
- **`editorial-reviewer`**: hook evaluation rubric overlaps with the reviewer's Hook strength dimension — use `hooks-drafter` when a more granular hook breakdown is needed than the reviewer provides
- **`voice-profiler`**: if `voice-tone/profile.md` exists, the naturalness check references its Avoided Words list; run `voice-profiler` once to make this check more precise
- **`seed-expander`**: produces angle stubs; `hooks-drafter` can be run against any stub's angle to pre-engineer the hook before `draft-builder` builds the body
