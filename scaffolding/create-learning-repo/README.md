# create-learning-repo

> Scaffold a structured, phased learning repository for any topic or certification — complete with folder hierarchy, template files, and blank stubs — ready to populate.

---

## When to use

**Trigger phrases** — say one of these to activate this skill:

```
"Create a learning repo for Kubernetes"
"Build a study guide for AWS Solutions Architect"
"Set up a knowledge base to learn LangGraph"
"Scaffold a certification prep repo for CKA"
"I want to become an expert in system design — create a learning repo"
```

**Conditions where this skill applies:**
- You want to build a structured, long-form learning repository from scratch
- You're preparing for a certification exam and want organized study materials
- You want a scaffold you can populate over time, not instant content

**Do NOT use this skill when:**
- You want to add content to an *existing* learning repo (that's authoring, not scaffolding)
- You want a quick summary or cheat sheet — this creates folder structures and files, not prose

---

## How it works

This skill runs in 5 phases:

| Phase | Name | What happens |
|---|---|---|
| 0 | Intake | 5 questions about topic, goal, level, time budget, seed URLs |
| 1 | Research | Live web fetches of official docs, exam blueprints, changelogs |
| 2 | Structure | Full folder + file tree designed and presented for approval |
| 3 | Templates | All template files generated in full and presented for approval |
| 4 | Delivery | Every directory and file created on disk (stubs + populated templates) |
| 5 | Git init | First-commit guide printed; repo is ready |

Each phase ends with a confirmation gate — the agent shows you output and waits before proceeding.

---

## Example

**You say:**
```
Create a learning repo for the Databricks Data Engineer Associate certification.
I want to pass the exam and get a job. I'm a beginner with 80 hours to invest.
```

**Agent does:**
```
Phase 0: Asks 5 intake questions (topic, goal, level, hours, seed URLs)

Phase 1: Fetches Databricks exam blueprint, official docs, and changelog.
         Produces research summary with domains, weightings, skill progression.

Phase 2: Designs folder tree — 5 sections, 14 modules, 42 chapters.
         Maps each section to exam domains. Estimates hours per chapter.
         Presents tree for your approval.

Phase 3: Generates chapter-notes-template.md, module-readme-template.md,
         section-readme-template.md, authoring-guidelines.md,
         interview-prep-template.md (because job goal detected).

Phase 4: Creates all 60+ files and directories. Templates fully written.
         All other files are blank stubs with a single placeholder comment.

Phase 5: Prints git commit command. Repo is ready to populate.
```

**Result:**
A fully scaffolded repo on disk — correct folder hierarchy, numbered sections, exam-domain annotations, and filled-in template files in `templates/`. You start populating stubs immediately using the templates as guides.

---

## Customization

**To change the chapter file types generated:**
Edit Phase 0's intent logic in `SKILL.md`. Add a new row to the intent table mapping a new goal type to a new file type (e.g. `"blog-post-template.md"` for public writing goals).

**To adjust chapter sizing:**
In Phase 2 of `SKILL.md`, change the target of `1.5–3 hours per chapter` to match your preferred granularity.

**To add a custom research source:**
In Phase 1 Step 1, add your URL to the parallel WebFetch list. Label it "custom seed".

**To install globally** (available in all your projects):
```bash
cp -r agent_skills/scaffolding/create-learning-repo ~/.config/opencode/skills/
```

**To install per-project** (available only in the current project):
```bash
cp -r agent_skills/scaffolding/create-learning-repo .opencode/skills/
```

---

## Related skills

| Skill | How it complements this one |
|---|---|
| [scaffolding/init-session](../init-session/README.md) | Use at the start of every authoring session to reload context from the handoff log before populating stubs |
| [scaffolding/end-session](../end-session/README.md) | Use at the end of each authoring session to write a handoff log that preserves your progress |
| [documentation/readme-writer](../../documentation/readme-writer/README.md) | Use to populate the root README stub once the repo structure is finalized |

---

## Known limitations

- **Certification blueprints drift:** Vendors like AWS, Databricks, and GCP update exam objectives frequently. If you use the repo more than 6 months after creation, verify the current official exam guide before authoring.
- **Content is not authored:** This skill creates the skeleton only. Every stub except `templates/` is a blank placeholder — populating them is your work.
- **Hour estimates are approximations:** The skill targets 1.5–3 hrs per chapter, but actual study time varies by prior experience and depth of material.
- **Live fetch may fail:** If WebFetch can't reach an official URL, the skill provides copy-paste AI query stubs as fallback, but you'll need to run those manually and feed back the results.
