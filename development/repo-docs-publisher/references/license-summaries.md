# License selection guidance

Used in Phase 3 when no `LICENSE` file already exists. This file gives **practical summaries only**, to help the user choose — it does not contain the legal text itself. Never reproduce license text from memory; always fetch the canonical, current text for whichever license is chosen (see "Getting the actual text" below).

## Common options — practical summary

- **MIT**: Very permissive. Anyone can use, modify, and distribute, including commercially, as long as the original license/copyright notice is included. Simplest, most common choice for small/medium open-source projects.
- **Apache-2.0**: Permissive, similar to MIT, but adds an explicit patent grant and requires stating changes made to the code. Common for larger projects or anything patent-sensitive.
- **BSD-3-Clause**: Permissive, similar to MIT, with an added clause preventing use of the project's name/contributors' names to promote derived products without permission.
- **GPL-3.0**: Copyleft — derivative works must also be open-sourced under GPL. Good fit if the goal is ensuring downstream modifications stay open.
- **Unlicense / public domain dedication**: Effectively no restrictions at all. Rare choice; usually only for truly trivial utilities.

If the user is unsure, MIT is the most common default for general-purpose open-source projects with no strong copyleft preference.

## Getting the actual text

Once a license is chosen:
- Fetch the current, official text (e.g. from https://choosealicense.com or the SPDX license list) rather than reproducing it from training data, since exact legal wording matters and must not be paraphrased, shortened, or reconstructed from memory.
- Fill in the placeholder fields the license requires (typically `[year]` and `[fullname]`/copyright holder) with values confirmed by the user.
- Write the complete, unmodified license text to the `LICENSE` file.