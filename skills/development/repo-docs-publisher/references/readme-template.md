# README.md template

```markdown
# <Project Name>

<One-line tagline describing what it does>

<Badges: build status, license, version, language — only include badges for things that actually exist>

## Description

<2-4 sentences: what problem this solves, who it's for, key capabilities.>

## Table of Contents
<!-- Include only if the README is long enough to need navigation -->
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

\`\`\`bash
<actual install command detected from repo, e.g. npm install / pip install -e .>
\`\`\`

## Usage

<Minimal quick-start example — enough to get something working in a few lines.>

\`\`\`<language>
<short example>
\`\`\`

For full usage details, configuration options, and troubleshooting, see [HOW_TO_USE.md](./HOW_TO_USE.md).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get set up, run tests, and submit changes.

<!-- Include the next two lines only if these files were generated (Phase 7) -->
Please also read our [Code of Conduct](./CODE_OF_CONDUCT.md).
To report a security vulnerability, see [SECURITY.md](./SECURITY.md).

## License

<Project Name> is licensed under the <License Name> — see [LICENSE](./LICENSE) for details.
```

## Badge guidance

Only propose badges for things Phase 1 actually detected:
- Build status badge → only if `.github/workflows/` (or other CI config) exists
- License badge → once a license is chosen/detected
- Package version badge → only if published to a registry (npm, PyPI, crates.io) — check manifest for registry-publish signals, don't assume
- Language/version badge (e.g. "Node >= 18") → from `engines` field or similar

Standard badge source: https://shields.io — use its standard badge URL patterns rather than inventing custom badge image URLs.