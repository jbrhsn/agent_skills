# end-session

Maintains project memory plus the current session and two previous sessions in `.agent_docs/handoff.md`, then creates a local Git commit for session changes. Pair with [init-session](../init-session/README.md) to resume. Use for wrapping up, checkpoints, and context resets; checkpoints do not stop ongoing work.

See [SKILL.md](SKILL.md) for memory selection and Python execution guidance. Python commands use `uv run`. If uv is absent, the agent asks for installation confirmation before installing it; file tools remain available while installation is pending or declined.

## Helper contract

Resolve the script from the installed skill directory. Run from any project subdirectory or specify `--repo-root`:

```bash
uv run /absolute/path/to/end-session/scripts/handoff_write.py --repo-root /absolute/project --input payload.json --dry-run
uv run /absolute/path/to/end-session/scripts/handoff_write.py --repo-root /absolute/project --input payload.json
```

The stdlib-only helper requires Python 3.8+ via uv. Input may also arrive on stdin. Example payload:

```json
{
  "snapshot": "Invoice parser service. Entry: app/main.py. Roadmap: docs/plan.md. Test: uv run pytest -q.",
  "learnings": ["Select vendor strategy by issuer VAT number; filenames are unreliable."],
  "last_session": ["2026-09-18: Added OCR fallback in app/ocr.py; scanned fixture passes. Retry configuration remained open."],
  "previous_session": ["2026-09-17: Added vendor A strategy and fixture; parser tests passed."],
  "current_session": {
    "date": "2026-09-19",
    "focus": "Vendor B parsing",
    "done": ["Added VendorBStrategy in app/vendors.py and a scanned invoice fixture."],
    "decisions": ["Reuse the OCR fallback for scanned vendor B invoices."],
    "verification": ["uv run pytest -q tests/test_vendors.py: 8 passed; full suite not run."],
    "open_items": [{"text": "Move the 3s retry backoff into configuration; next edit app/config.py.", "done": false}]
  }
}
```

`current_session` is required and replaces the complete current record. Its date defaults to today. Snapshot and learnings are preserved when omitted; provided learnings replace the whole list. Merge durable knowledge and carry unresolved project work into the new payload before writing.

For a distinct new session, the default rotation moves Current Session into Last Session and Last Session into Previous Session. Optional `last_session` and `previous_session` lists replace those records with agent-written compact summaries. Omission retains the outgoing concrete records rather than dropping history. Supply summaries to keep a large file compact; the helper does not perform semantic compression or impose a token cap.

Use `--checkpoint` on repeated saves of the same session, including before compaction; history then remains in place. This flag does not merge current-session deltas. After resuming the same task through a context reset, continue using checkpoint mode if that session was already saved. On a genuinely new session, rotate once. Dates alone do not identify sessions.

The five canonical headings appear in the [template](assets/handoff_template.md). Existing custom sections are preserved. Legacy four-section handoffs are accepted; missing history stays empty until enough sessions have been recorded. The helper archives the entire outgoing handoff to `.agent_docs/archive/session-<timestamp>.md` before atomic replacement, aborting if archiving fails. Archives preserve recorded snapshots, not omitted conversation history. `--dry-run` writes nothing. Exit codes: 0 success, 1 invalid input, 2 filesystem failure.

Read archives only for relevant older evidence. Keep the main file compact by deduplicating and correcting durable facts, retaining actionable project state, and linking detailed references. Choose whether to commit `.agent_docs/` according to project conventions; this skill does not change ignore rules.

## Git commit

The agent commits the session's relevant changes after saving memory; the Python helper does not execute Git. This also applies to checkpoints unless the user asks for a memory-only save or no commit. The agent reviews the commit scope, preserves unrelated edits and staging, follows project checks and commit-message conventions, and reports the resulting hash. Incomplete work can be recorded as a checkpoint with outstanding validation clearly documented.

Ignored memory stays local while eligible project changes are committed. A clean tree produces no empty commit, and a non-Git project receives only the saved memory. Commit blockers are reported without bypassing hooks or changing identity. Pushing and amending require a separate request. See [SKILL.md](SKILL.md) for the complete workflow.
