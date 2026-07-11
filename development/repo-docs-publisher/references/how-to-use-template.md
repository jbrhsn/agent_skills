# HOW_TO_USE.md template

The detailed usage doc. README.md stays a quick-start + overview and links here;
this file holds the depth. Don't duplicate the README's quick-start — expand on it.
Every command, path, config key, and flag must be verified from the repo (Phase 1),
never invented.

```markdown
# How to Use <Project Name>

Detailed usage guide. For a quick overview and installation, see the [README](./README.md).

## Prerequisites

<Runtime/tooling versions and system requirements detected from the repo, e.g. "Node >= 18", "Python 3.11+", any external services.>

## Installation

<Full install steps — more detail than the README quick-start: from-source build, optional extras, platform notes.>

\`\`\`bash
<actual install/build commands detected from repo>
\`\`\`

## Configuration

<!-- Include only if the repo actually has configuration -->
<Config file(s), environment variables, and CLI flags — list the real keys/vars found in the repo with their purpose and defaults. Never invent config that doesn't exist.>

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| <env var / flag / key> | <type> | <default> | <what it does> |

## Usage / Common Workflows

<Walk through the main things a user does, end to end, with real runnable examples.>

### <Workflow / command 1>
\`\`\`<language or shell>
<example>
\`\`\`
<what it does and expected output>

### <Workflow / command 2>
\`\`\`<language or shell>
<example>
\`\`\`

## Troubleshooting

<Common problems and fixes. Seed from known error messages, FAQ-style issues, or gotchas evident in the code/issues. If none are known, a short "Common issues" stub is fine — don't fabricate errors.>

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| <symptom> | <cause> | <resolution> |

## See Also

- [README](./README.md) — overview and quick start
- [CONTRIBUTING](./CONTRIBUTING.md) — for contributors
```

## Guidance

- This is where depth lives; keep the README lean and pointing here.
- Only include the **Configuration** and **Troubleshooting** sections if the repo
  has real content for them — an empty config table is worse than omitting it.
- Tailor the workflow examples to the actual entry points and commands detected
  in Phase 1 (CLI subcommands, library API, HTTP endpoints, etc.).
