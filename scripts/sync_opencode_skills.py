#!/usr/bin/env python3
"""Sync OpenCode skills from agent_skills repo to ~/.config/opencode/skills."""

import sys
from common import get_dest, parse_args, sync_skills

if __name__ == "__main__":
    args = parse_args("Sync OpenCode skills to ~/.config/opencode/skills")
    dest = get_dest("OPENCODE_SKILLS", ".config/opencode/skills")
    sf = [s.strip() for s in args.skills.split(",") if s.strip()] if args.skills else None
    sys.exit(sync_skills("OpenCode", dest, args.dry_run, args.verify, skills_filter=sf))

