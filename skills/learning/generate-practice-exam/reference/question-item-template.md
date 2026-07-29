# Question Item Template

The canonical format for a single exam/drill question. The `generate-practice-exam` skill uses this for every item. Fill the bracketed placeholders; keep the structure.

Every question must be **grounded in authored content** and every option must be **plausible** — wrong options are real misconceptions (drawn from the source chapter's Pitfalls section wherever possible), never throwaways. No "all of the above" / "none of the above" filler.

---

## Single-choice item

```
[N]. [Scenario-first stem: a realistic situation that requires applying the concept,
     not a bare definition lookup — except for recall questions.]

   - A. [Option]
   - B. [Option]
   - C. [Option]
   - D. [Option]
```

**Inline answer form (drill default):**

```
   <details><summary>Answer</summary>

   **Correct: [letter].** [One sentence on why it is right, tied to the source concept.]

   - **[wrong letter]** — [why this distractor is wrong / what misconception it reflects].
   - **[wrong letter]** — [why wrong].
   - **[wrong letter]** — [why wrong].

   *Review if missed: [relative/path/to/source-chapter.md]*

   </details>
```

---

## Multi-select item

```
[N]. **Which TWO** [stem]?

   - A. [Option]
   - B. [Option]
   - C. [Option]
   - D. [Option]
   - E. [Option]
```

**Inline answer form:**

```
   <details><summary>Answer</summary>

   **Correct: [letter] and [letter].**
   - **[correct letter]** — [why it qualifies].
   - **[correct letter]** — [why it qualifies].

   Why the most tempting wrong answer fails:
   - **[wrong letter]** — [why it is wrong despite looking right].

   *Review if missed: [relative/path/to/source-chapter.md]*

   </details>
```

---

## Rules for every item

- **Traceable:** the stem maps to a specific authored concept, definition, worked example, or pitfall. Introduce no facts absent from the source.
- **Cognitive level:** tag internally as recall / application / analysis so the domain mix can be enforced.
- **Distractors from pitfalls:** prefer wrong options that mirror the misconceptions the source chapter warns about.
- **Rationale covers all options:** state why the correct answer is right AND why each significant distractor is wrong. One-word rationales are non-compliant.
- **Multi-select:** always phrase as "Which TWO" / "Which THREE" and provide 5 options.
- **No duplication:** do not restate an existing Self-Check question verbatim — change the scenario or angle.
- **Review pointer:** in drill mode, end every answer with a relative-path pointer to the source chapter. Omit in full-mock mode (the answer key carries rationale instead).
