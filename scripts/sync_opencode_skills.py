#!/usr/bin/env python3
"""Sync OpenCode skills from agent_skills repo to ~/.config/opencode/skills."""

import sys
from common import get_dest, parse_dry_run_args, sync_skills

if __name__ == "__main__":
    args = parse_dry_run_args("Sync OpenCode skills to ~/.config/opencode/skills")
    dest = get_dest("OPENCODE_SKILLS", ".config/opencode/skills")
    sys.exit(sync_skills("OpenCode", dest, args.dry_run))
