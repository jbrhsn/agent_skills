---
name: hooks-drafter
description: Use when the user wants to generate, score, or sharpen opening hooks for a LinkedIn post or Medium article. Applies research-grounded hook engineering — curiosity gap theory, four psychological levers, five hook types, platform-specific mechanics, a 7-dimension scoring rubric, and a naturalness check. Produces scored variants and stops for the user to choose. Trigger on "draft hooks for X", "write me some hooks", "evaluate this hook", "generate hook variants", "make this hook stronger".
---

# Hooks Drafter

Generate, score, and select high-performing opening hooks for LinkedIn posts or Medium articles. This is a **cross-cutting skill** — it can be used standalone before any drafting work, or called at any point to generate and evaluate hooks for existing content.

This skill produces **text output only**. It writes no files. The selected hook is returned as clean text for the user to paste wherever it's needed.

## When to use

- User wants to generate hook variants for a topic or idea before drafting.
- User has an existing hook and wants it evaluated and scored.
- User is mid-session writing content and wants deeper hook engineering.
- This skill generates opening hooks only — full post or article body writing is outside its scope.
- Carousel slide titles are outside this skill's scope.

## Platform detection

LinkedIn and Medium have different hook mechanics. Before generating anything:
- If the user specifies a platform, proceed with its rules.
- If unclear, ASK which platform before generating variants.
- Wrong-platform hooks will underperform — do not guess.

## Voice handling

This skill does **not** require `voice-tone/`. If `voice-tone/profile.md` is present at cwd, the naturalness check (Step 4) can optionally reference its "Avoided Words & Phrases" section to flag banned patterns in the top variants. If absent, skip silently. A missing voice profile never blocks hook generation.

---

## Hook framework (apply to every session)

### The curiosity gap — core mechanism

All effective hooks exploit the gap between what a reader knows and what they want to know. The key insight from information-gap theory: curiosity follows an **inverted-U curve tied to reader confidence**.

- **Too vague** → reader has no reference point, can't form a guess, feels nothing.
- **Too complete** → gap is already closed, no pull.
- **Sweet spot** → reader has just enough to form a confident-but-incomplete guess. That incomplete guess creates the pull.

Do not write hooks that withhold information. Write hooks that give a **specific, concrete partial answer** — enough that the reader's brain fills in a guess, and then wants to confirm or correct it. Pure-tease "you won't believe" hooks have decayed through pattern recognition; audiences discount them.

### The four levers (independent, compound when combined)

Apply at least two levers to every hook variant. Combining three or more amplifies the effect.

**Lever 1 — Specificity**
Replace every vague quantifier ("many," "huge," "fast," "a lot") with a real number or concrete detail. Odd numbers outperform even numbers (~20% higher CTR) because they read as actual findings rather than rounded marketing figures. "I lost 23 pounds in 9 weeks" beats "I lost weight fast" — specificity is both a credibility signal and a curiosity-gap precision tool.

**Lever 2 — Negativity bias**
A hook framed around a mistake, failure, myth busted, or risk avoided consistently outperforms the same insight framed as a win or tip. Research on a large headline dataset found: presence of one negative word increases CTR by ~2.3%, while positive language decreases CTR by ~1.0%. Test both framings before choosing — "The mistake that cost me $10k" usually beats "How I saved $10k" pointing to the same content.

**Lever 3 — Emotional arousal + low dominance**
The hook should (1) spike alertness — surprise, tension, a stark claim — and (2) leave exactly one specific thing unresolved. Not everything unresolved (that's over-vague); one thing. High arousal + one unresolved element is the structural formula behind most high-performing hooks.

**Lever 4 — Curiosity gap precision**
Target moderate reader confidence: specific enough to be credible, incomplete enough to demand resolution. Vague = low confidence = no itch. Complete = high confidence = no gap. The sweet spot is a claim the reader can half-answer but not fully resolve without reading.

### The five hook types

Each type exploits a different psychological trigger. Rotate them — audiences develop pattern blindness to any type used repeatedly.

| Type | Mechanism | Strength |
|---|---|---|
| **Contrarian** | State a belief the reader holds, then contradict it | Strongest: creates cognitive dissonance, a harder forcing function than curiosity alone |
| **Data / surprising number** | Lead with a specific stat counter to expectation | High: combines Lever 1 (specificity) + Lever 3 (arousal) automatically |
| **Story-in-motion** | Open mid-scene, no setup or throat-clearing | High: bypasses sales resistance — a story doesn't feel like it's trying to persuade |
| **Problem-naming** | Name the reader's specific pain more precisely than they'd name it themselves | High: works on relevance and recognition, not curiosity — different pull mechanism |
| **Question** | Ask a question the reader silently answers | Medium: ~1.8x engagement on LinkedIn; weaker on Medium; use for tone flexibility, not maximum pull |

**Rotation rule:** if the user's last 2–3 posts used the same hook type, force a different type for this piece. Predictable opening formats lose pull even with readers who like your content.

**Third-person Story-in-motion note:** when the author writes in third-person voice (no "I/we/our"), Story-in-motion hooks must be grounded in a documented source (attributed case study, official blog post, public report) and cited accordingly, or constructed as a clearly illustrative scenario and flagged `[UNVERIFIED]` before being handed to the draft-builder step. An uncited third-person scenario ("A team saw costs drop by 70%…") is a factual claim — treat it as such.

---

## Platform-specific mechanics

### LinkedIn hook mechanics

LinkedIn is a **discrete UI trigger**: only the first 2–3 lines are visible before the "see more" button, and ~65% of users decide to expand based solely on those lines. The "see more" click is also an algorithmic signal — weak hooks don't just cost this reader, they cap distribution in the first 30 minutes when the algorithm decides whether to push the post wider.

| Rule | Constraint |
|---|---|
| Character limit | Only first ~210–235 characters visible in feed |
| Line length | Each hook line under ~10 words; ~49 characters per line |
| Fold placement | Hook must stand alone and create tension before the "see more" cut |
| No emojis | Visual noise before the reader has committed; remove from hook lines |
| No throat-clearing | "Hi everyone", "Happy Tuesday", "Today I want to share", "Excited to announce" — cut on sight, every time |
| Hook under 10 words | Hooks under 10 words per line outperform longer hooks by ~40% |

### Medium hook mechanics

Medium hook is a **three-part package**: title + subtitle + image. CTR > 8% is strong, but CTR alone is not the goal — Medium's payout and algorithmic distribution are tied to read ratio (% who finish), not clicks. A title that overpromises produces a click and then an immediate bounce, which is visible in stats and suppresses future distribution.

| Rule | Constraint |
|---|---|
| Title job | Creates the curiosity gap — specific enough to be credible, incomplete enough to pull |
| Subtitle job | Adds new information (a stake, outcome, or constraint) — must NOT repeat the title in different words |
| Subtitle length | Under ~15 words — longer gets truncated in previews |
| Honesty requirement | The gap must be genuinely closed by the content — overselling is punished mechanically, not just ethically |
| Question hooks | Weaker on Medium than LinkedIn — skip as a variant type for Medium sessions |

---

## Hook evaluation rubric

Score every variant against all 7 dimensions before presenting to the user. PASS or FAIL per dimension. A FAIL on **Payoff honesty** is a hard disqualifier — do not present that variant; replace it.

| Dimension | Pass criteria |
|---|---|
| **1. Gap precision** | Specific enough to form a guess; incomplete enough to need resolution. Not fully vague, not fully complete |
| **2. Specificity** | Contains a real number, concrete detail, or named specific — no "many", "huge", "fast", "significant" |
| **3. Type clarity** | Clearly one of the five types; not a muddled blend that exploits no mechanism cleanly |
| **4. Platform fit** | Respects platform mechanics: line length + no emoji + no throat-clearing (LinkedIn); title/subtitle relationship (Medium) |
| **5. Throat-clearing free** | No "I wanted to share", "Hi everyone", "Today I", "In today's post", "Excited to announce", or equivalent |
| **6. Payoff honesty** | The implicit promise the hook makes is deliverable by the actual content. HARD DISQUALIFIER if failed |
| **7. Rotation** | Different type from the user's last 2–3 hooks, if post history was shared |

### Naturalness check (authenticity gate)

After the rubric, apply to every top-ranked variant: *"Could a stranger who has never met this person have written this exact line?"*

If yes → too generic. Generate a replacement that is more specific to the user's actual experience, angle, or content. Report that a replacement was generated and why. This check cannot be skipped — generic hooks that pass the rubric but fail authenticity will underperform with an established audience.

---

## Workflow

### Step 1 — Intake
Read the input: topic, idea, existing hook to evaluate, or source draft. Confirm the target platform (ask if unclear). If the user provides an existing hook to evaluate rather than generate new variants, skip to Step 3 directly.

### Step 2 — Generate variants
- **LinkedIn**: generate 5 variants, one per type (Contrarian, Data/number, Story-in-motion, Problem-naming, Question). Label each with its type.
- **Medium**: generate 4 variants (skip Question — weakest on Medium): Contrarian, Data/number, Story-in-motion, Problem-naming. Label each. Also generate 3 subtitle variants for the top hook.
- Apply the four levers across variants — each variant should use at least two levers. Note which levers each variant employs.

Do NOT score yet — proceed to Step 3.

### Step 3 — Score each variant
Run the 7-dimension rubric on every variant. Report a PASS/FAIL per dimension in a compact table under each variant. If any variant fails **Payoff honesty**, replace it immediately with a new variant before presenting. Highlight the top 1–2 variants and note their strongest lever combination in one line.

### Step 4 — Naturalness check
Apply the naturalness check to the top 1–2 variants. If a top variant fails (a stranger could have written it), generate one replacement variant that is more specific to the user's actual content or experience. Report if a replacement was generated and why.

### Step 5 — Mandatory stop
Present all variants with:
- The hook text
- Rubric scorecard (7 dimensions, PASS/FAIL)
- Lever combination note
- Naturalness check result

STOP. Ask the user to:
- Pick one variant as-is
- Pick one and request a specific tweak
- Reject all and provide direction for a new round

Do NOT write any file. Do NOT proceed without explicit user choice.

### Step 6 — Finalize (optional)
If the user picks and requests a tweak, apply it, re-run the rubric on the final version, confirm all 7 dimensions pass, and deliver the final hook as clean, pasteable text.

One iteration maximum per session unless the user explicitly asks for more rounds.

---

## No files written — ever

This skill produces text output only. No files are created or modified at any point. There is no persist step. The selected hook is returned as clean text.

## Handoff

This skill produces clean, pasteable hook text. The selected hook is a complete deliverable — paste it as the opening of any post, article, or draft.

## Conventions

These are shared assumptions so the content skills interoperate. Each skill
still works standalone. None of these require another skill to be present.

- **Folders** (all cwd-relative): `drafts/`, `linkedin/`, `medium/`,
  `archive/`, `voice-tone/`. Never auto-create: ask the user if missing.
- **Slug**: lowercase, hyphenated, derived from the working title. Reused as
  the filename stem across skills so a piece is traceable.
- **Filenames**: `drafts/<slug>.md`, `linkedin/<slug>-<type>.md`,
  `medium/<slug>-<type>.md`, carousels at `linkedin/carousels/<slug>/`.
- **Overwrite policy**: never silently overwrite an existing file. If the
  target exists, ask the user: overwrite, write a `-v2` (then `-v3`...)
  variant, or pick a new name.
- **Status values** (if a tracker file like `content-log.md` or
  `content-log.json` exists at cwd): `idea` -> `drafted` -> `reviewed` ->
  `posted` -> `archived`. If such a tracker exists, after writing or moving a
  file ASK the user in one line whether to update it to the new status.
  Absence of a tracker must never block the skill.
