#!/usr/bin/env python3
"""Sync Antigravity skills from agent_skills repo to ~/.gemini/config/skills."""

import sys
from common import get_dest, parse_dry_run_args, sync_skills

if __name__ == "__main__":
    args = parse_dry_run_args("Sync Antigravity skills to ~/.gemini/config/skills")
    dest = get_dest("ANTIGRAVITY_SKILLS", ".gemini/config/skills")
    sys.exit(sync_skills("Antigravity", dest, args.dry_run))
