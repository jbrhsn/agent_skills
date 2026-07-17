# Hook Writing Guide

A self-contained reference for writing high-performing opening hooks for LinkedIn posts
and Medium articles. This guide is used by both the hooks-drafter skill (standalone hook
engineering) and the linkedin-writer and medium-writer skills (integrated hook steps).
No skill dependency is required — load this guide and apply it directly.

---

## The curiosity gap — core mechanism

All effective hooks exploit the gap between what a reader knows and what they want to know.
The key insight from information-gap theory: curiosity follows an **inverted-U curve tied to
reader confidence**.

- **Too vague** → reader has no reference point, can't form a guess, feels nothing.
- **Too complete** → gap is already closed, no pull.
- **Sweet spot** → reader has just enough to form a confident-but-incomplete guess. That
  incomplete guess creates the pull.

Do not write hooks that withhold information. Write hooks that give a **specific, concrete
partial answer** — enough that the reader's brain fills in a guess, and then wants to
confirm or correct it. Pure-tease "you won't believe" hooks have decayed through pattern
recognition; audiences discount them.

---

## The four levers (independent, compound when combined)

Apply at least two levers to every hook variant. Combining three or more amplifies the effect.

**Lever 1 — Specificity**
Replace every vague quantifier ("many," "huge," "fast," "a lot") with a real number or
concrete detail. Odd numbers outperform even numbers (~20% higher CTR) because they read as
actual findings rather than rounded marketing figures. "I lost 23 pounds in 9 weeks" beats
"I lost weight fast" — specificity is both a credibility signal and a curiosity-gap precision
tool.

**Lever 2 — Negativity bias**
A hook framed around a mistake, failure, myth busted, or risk avoided consistently outperforms
the same insight framed as a win or tip. Research on a large headline dataset found: presence
of one negative word increases CTR by ~2.3%, while positive language decreases CTR by ~1.0%.
Test both framings before choosing — "The mistake that cost me $10k" usually beats "How I
saved $10k" pointing to the same content.

**Lever 3 — Emotional arousal + low dominance**
The hook should (1) spike alertness — surprise, tension, a stark claim — and (2) leave exactly
one specific thing unresolved. Not everything unresolved (that's over-vague); one thing. High
arousal + one unresolved element is the structural formula behind most high-performing hooks.

**Lever 4 — Curiosity gap precision**
Target moderate reader confidence: specific enough to be credible, incomplete enough to demand
resolution. Vague = low confidence = no itch. Complete = high confidence = no gap. The sweet
spot is a claim the reader can half-answer but not fully resolve without reading.

---

## The five hook types

Each type exploits a different psychological trigger. Rotate them — audiences develop pattern
blindness to any type used repeatedly.

| Type | Mechanism | Strength |
|---|---|---|
| **Contrarian** | State a belief the reader holds, then contradict it | Strongest: creates cognitive dissonance, a harder forcing function than curiosity alone |
| **Data / surprising number** | Lead with a specific stat counter to expectation | High: combines Lever 1 (specificity) + Lever 3 (arousal) automatically |
| **Story-in-motion** | Open mid-scene, no setup or throat-clearing | High: bypasses sales resistance — a story doesn't feel like it's trying to persuade |
| **Problem-naming** | Name the reader's specific pain more precisely than they'd name it themselves | High: works on relevance and recognition, not curiosity — different pull mechanism |
| **Question** | Ask a question the reader silently answers | Medium: ~1.8x engagement on LinkedIn; weaker on Medium; use for tone flexibility, not maximum pull |

**Rotation rule:** if the user's last 2–3 posts used the same hook type, force a different
type for this piece. Predictable opening formats lose pull even with readers who like your
content.

**Third-person Story-in-motion note:** when the author writes in third-person voice (no
"I/we/our"), Story-in-motion hooks must be grounded in a documented source (attributed case
study, official blog post, public report) and cited accordingly, or constructed as a clearly
illustrative scenario and flagged `[UNVERIFIED]` before being handed to the draft-builder
step. An uncited third-person scenario ("A team saw costs drop by 70%…") is a factual claim
— treat it as such.

---

## Platform-specific mechanics

### LinkedIn hook mechanics

LinkedIn is a **discrete UI trigger**: only the first 2–3 lines are visible before the "see
more" button, and ~65% of users decide to expand based solely on those lines.

| Rule | Constraint |
|---|---|
| Character limit | Only first ~210–235 characters visible in feed |
| Line length | Each hook line under ~10 words; ~49 characters per line |
| Fold placement | Hook must stand alone and create tension before the "see more" cut |
| No emojis | Visual noise before the reader has committed; remove from hook lines |
| No throat-clearing | "Hi everyone", "Happy Tuesday", "Today I want to share", "Excited to announce" — cut on sight |
| Hook under 10 words | Hooks under 10 words per line outperform longer hooks by ~40% |

### Medium hook mechanics

Medium hook is a **three-part package**: title + subtitle + image. CTR > 8% is strong, but
CTR alone is not the goal — Medium's payout and algorithmic distribution are tied to read ratio,
not clicks.

| Rule | Constraint |
|---|---|
| Title job | Creates the curiosity gap — specific enough to be credible, incomplete enough to pull |
| Subtitle job | Adds new information (a stake, outcome, or constraint) — must NOT repeat the title |
| Subtitle length | Under ~15 words — longer gets truncated in previews |
| Honesty requirement | The gap must be genuinely closed by the content — overselling is punished mechanically |
| Question hooks | Weaker on Medium than LinkedIn — skip as a variant type for Medium sessions |

---

## Hook evaluation rubric

Score every variant against all 7 dimensions. PASS or FAIL per dimension. A FAIL on
**Payoff honesty** is a hard disqualifier — replace that variant before presenting.

| Dimension | Pass criteria |
|---|---|
| **1. Gap precision** | Specific enough to form a guess; incomplete enough to need resolution |
| **2. Specificity** | Contains a real number, concrete detail, or named specific — no vague qualifiers |
| **3. Type clarity** | Clearly one of the five types; not a muddled blend |
| **4. Platform fit** | Respects platform mechanics: line length + no emoji + no throat-clearing (LinkedIn); title/subtitle relationship (Medium) |
| **5. Throat-clearing free** | No "I wanted to share", "Hi everyone", "Today I", "In today's post", "Excited to announce" |
| **6. Payoff honesty** | The implicit promise the hook makes is deliverable by the actual content. HARD DISQUALIFIER if failed |
| **7. Rotation** | Different type from the user's last 2–3 hooks, if post history was shared |

---

## Naturalness check (authenticity gate)

After the rubric, apply to every top-ranked variant:
*"Could a stranger who has never met this person have written this exact line?"*

If yes → too generic. Generate a replacement that is more specific to the user's actual
experience, angle, or content. This check cannot be skipped — generic hooks that pass the
rubric but fail authenticity will underperform with an established audience.

---

## Generating variants: quick reference

**For LinkedIn:** generate 5 variants, one per type (Contrarian, Data/number,
Story-in-motion, Problem-naming, Question). Label each with its type and note which two+
levers it uses.

**For Medium:** generate 4 variants (skip Question — weakest on Medium): Contrarian,
Data/number, Story-in-motion, Problem-naming. Also generate 3 subtitle variants for the top
hook.

Write each variant as 1–3 lines. Score all with the 7-dimension rubric. Apply the naturalness
check to the top 1–2. Present all variants with scores; let the user pick.
