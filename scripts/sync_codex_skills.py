#!/usr/bin/env python3
"""Sync skills to Codex and the ChatGPT desktop harness at ~/.agents/skills."""

import sys

from common import get_dest, parse_args, sync_skills


if __name__ == "__main__":
    args = parse_args("Sync skills to Codex and ChatGPT's ~/.agents/skills")
    dest = get_dest("CODEX_SKILLS", ".agents/skills")
    sys.exit(sync_skills("Codex / ChatGPT", dest, args.dry_run, args.verify))
