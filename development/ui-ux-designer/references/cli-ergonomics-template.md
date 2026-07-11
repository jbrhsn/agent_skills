# CLI ergonomics template

Use this ONLY when Phase 0 determined the project is a command-line tool (no
graphical/TUI surface) AND the user accepted the lighter-weight
command-ergonomics treatment instead of full screen/flow design. Write the
result to `docs/ux-design.md` using the structure below instead of the
flow/screen/design-system templates. No screens, no Mermaid flowcharts, no
color palette — a CLI's "UX" is its command surface and output design.

```markdown
# CLI UX: <Tool Name>

> Command ergonomics and output design. No graphical UI.

## 1. Command Structure
- **Invocation model:** single command with flags, OR subcommand-based
  (`tool <verb> [args]`) — state which and why.
- **Command tree:** list commands/subcommands, each with a one-line purpose.

| Command | Purpose | Key flags/args |
|---------|---------|----------------|
| `tool convert <in> <out>` | ... | `--format`, `--force` |

## 2. Flags & Arguments
- Naming conventions (long `--flag`, short `-f`, consistency across commands).
- Positional vs optional; sensible defaults; required-vs-optional clarity.
- Reading from stdin / writing to stdout where idiomatic (pipe-friendliness).

## 3. Output Design
- **Default (human) output:** what success looks like; use of color/symbols
  (and respect `NO_COLOR` / non-TTY → plain output).
- **Machine output:** `--json` / `--quiet` for scripting; stable, parseable.
- **Progress/verbosity:** `-v/-vv`, `--quiet`; where progress indicators appear.

## 4. Errors & Exit Codes
- Error message style (what failed + how to fix + which flag/arg).
- Exit-code convention (0 success; distinct non-zero codes per failure class).
- Behavior on partial failure.

## 5. Help & Discoverability
- `--help`/`-h` at top level and per subcommand; `--version`.
- Example-driven help; man page or shell-completion plans if relevant.

## 6. Interaction & Safety
- Interactive prompts vs fully non-interactive (`--yes` to bypass confirmations).
- Destructive-action confirmations and `--dry-run` where applicable.
- Idempotency / re-run safety.

## 7. Open Questions
- <anything unresolved to confirm with the user>
```

## Guidance

- Keep it concrete enough that an engineer could implement the CLI's interface
  (flag names, exit codes, output shapes) from this doc.
- Respect established CLI conventions (POSIX/GNU flag style, `NO_COLOR`,
  stdout-for-data/stderr-for-logs, `-` as stdin) rather than inventing new ones.
- If the tool later grows a TUI, that's a separate full screen/flow design pass.
