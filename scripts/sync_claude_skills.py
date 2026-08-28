#!/usr/bin/env python3
"""Sync Claude Code skills from agent_skills repo to ~/.claude/skills."""

import sys
from common import get_dest, parse_args, sync_skills

if __name__ == "__main__":
    args = parse_args("Sync Claude Code skills to ~/.claude/skills")
    dest = get_dest("CLAUDE_SKILLS", ".claude/skills")
    sys.exit(sync_skills("Claude Code", dest, args.dry_run, args.verify))

