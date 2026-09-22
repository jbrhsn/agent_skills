#!/usr/bin/env python3
"""Sync IBM Bob skills from agent_skills repo to ~/.bob/skills."""

import sys
from common import get_dest, parse_args, sync_skills

if __name__ == "__main__":
    args = parse_args("Sync IBM Bob skills to ~/.bob/skills")
    dest = get_dest("BOB_SKILLS", ".bob/skills")
    sf = [s.strip() for s in args.skills.split(",") if s.strip()] if args.skills else None
    sys.exit(sync_skills("IBM Bob", dest, args.dry_run, args.verify, skills_filter=sf))

