# Global Agent Guidelines

Standing instructions for every agent session in this workspace. Sourced from
the agent_skills repo (`agents/ANTIGRAVITY_AGENTS.md`) and kept in sync via
`uv run scripts/sync_all.py` — edit there, not here.

## Coding, review, and debugging

Before writing, editing, reviewing, or debugging any code, load the
`lean-coder` skill and the matching per-language reference guide it points to.
This is mandatory for coding work, not optional.

## Execution & verification standards

- Implement complete units of work end-to-end: make the change, then verify it
  yourself before reporting back.
- Verify using whatever the project actually supports (test suite, build,
  lint, or diff inspection). If no automated tooling exists, verify by manual
  inspection against the stated requirements and say so explicitly.
- Never claim success without having actually checked.
- Report a clear, concise summary: files changed, verification method and
  result, pass/fail status.

## Task decomposition & planning

- Decompose complex requests into clear, independent units of work.
- Keep execution targeted and modular; avoid sweeping unverified edits across
  unrelated components.
- Confirm verification results before declaring a multi-step task complete.
