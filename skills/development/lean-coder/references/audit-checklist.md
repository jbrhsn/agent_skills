# Repo over-engineering audit checklist

Used by the `/audit-repo` workflow to scan a codebase broadly for excess. Not a correctness, security, or style audit — this looks only at unnecessary complexity and bloat.

## What to look for

- **Reinvented standard library**: custom implementations of things the language/framework's stdlib or native features already provide (date formatting, deep-clone, debounce, simple string utilities, etc.).
- **Unnecessary dependencies**: packages installed for functionality that's a few lines of stdlib code, or that are used in exactly one trivial place.
- **Speculative abstractions**: interfaces, plugin systems, config layers, or generic base classes with only one concrete implementation and no near-term second use case.
- **Dead flexibility**: parameters, feature flags, or branches that are never exercised by any caller or are always called with the same value.
- **Duplicated logic**: near-identical code blocks across files that should be a shared function/component.
- **Oversized functions/files doing too much**: not a line-count rule by itself, but a signal to check if a function is doing several unrelated things that could be simpler if split or, more often, if some of it shouldn't exist at all.
- **Dead code**: unused exports, unreachable branches, commented-out code left in place, unused imports. (Caveat: an "unused" export may be a public API or consumed by another repo/package — verify it has no external consumers before recommending deletion.)
- **Deferred-debt comments**: search for `lazy:` markers left by this skill (or equivalent markers already in the codebase) to see what's been knowingly deferred and whether it's become relevant.

## What NOT to flag

- Validation, error handling, security checks, data-loss safety (confirmations, backups, transactions), accessibility code — these are never "bloat" even if they add lines.
- Genuine abstractions with 2+ real current use sites.
- Documentation/comments that follow the project's own conventions.
- Tests, even verbose ones — this audit is about production code paths, not test bloat (a separate concern).

## Output format

Rank findings by impact (biggest simplification opportunity first). One line per finding:

```
[file:line] <what to cut/simplify> — replace with <stdlib/native/existing equivalent>, saves ~<rough line estimate>
```

Group by category (reinvented stdlib, unnecessary deps, speculative abstractions, dead code, duplication) if the list is long enough to need it. Keep it a report — don't apply fixes unless asked.