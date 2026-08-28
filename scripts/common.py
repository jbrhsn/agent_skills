"""Shared utilities and constants for agent_skills sync scripts."""

import argparse
import fnmatch
import hashlib
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUSIONS = {
    ".venv",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
    ".git",
    "*.egg-info",
    "dist",
    "build",
}


def file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def is_excluded(path: Path) -> bool:
    """Check if any path component matches EXCLUSIONS."""
    return any(
        any(fnmatch.fnmatch(part, pattern) for pattern in EXCLUSIONS)
        for part in path.parts
    )


def get_dest(env_var: str, default_relpath: str) -> Path:
    """Get destination directory, respecting environment variable overrides."""
    val = os.environ.get(env_var)
    return Path(val).expanduser() if val else Path.home() / default_relpath


def discover_skills() -> list[Path]:
    """Find all skill directories containing a SKILL.md file, sorted by name."""
    return sorted((p.parent for p in (REPO_ROOT / "skills").glob("**/SKILL.md")), key=lambda p: p.name)


def verify_skills(target_name: str, dest_dir: Path) -> int:
    """Verify exact checksum and file parity between source skills and destination."""
    print(f"\n🔎 Verifying {target_name} skills parity...")
    skills = discover_skills()
    source_names = {s.name for s in skills}
    dest_names = {d.name for d in dest_dir.iterdir() if d.is_dir()} if dest_dir.exists() else set()

    failures = []
    extra_dirs = dest_names - source_names
    if extra_dirs:
        failures.append(f"Extra unknown skill directories in destination: {', '.join(sorted(extra_dirs))}")

    for src in skills:
        name = src.name
        dest = dest_dir / name
        if not dest.exists():
            failures.append(f"{name}: missing in destination")
            continue

        src_files = {
            f.relative_to(src): file_hash(f)
            for f in src.rglob("*")
            if f.is_file() and not is_excluded(f)
        }
        dest_files = {
            f.relative_to(dest): file_hash(f)
            for f in dest.rglob("*")
            if f.is_file() and not is_excluded(f)
        }

        missing = set(src_files.keys()) - set(dest_files.keys())
        extra = set(dest_files.keys()) - set(src_files.keys())
        mismatches = {
            rel for rel in set(src_files.keys()) & set(dest_files.keys())
            if src_files[rel] != dest_files[rel]
        }

        errors = []
        if missing:
            errors.append(f"missing files: {sorted(str(f) for f in missing)}")
        if extra:
            errors.append(f"extra files: {sorted(str(f) for f in extra)}")
        if mismatches:
            errors.append(f"checksum mismatches: {sorted(str(f) for f in mismatches)}")

        if errors:
            failures.append(f"{name}: " + "; ".join(errors))
        else:
            print(f"✓ {name} ({len(src_files)} files, SHA256 verified)")

    if failures:
        print(f"\n✗ {target_name} skills verification failed:")
        for line in failures:
            print(f"  - {line}")
        return 1

    print(f"✅ All {len(skills)} {target_name} skills verified (100% parity)")
    return 0


def sync_skills(target_name: str, dest_dir: Path, dry_run: bool = False, verify: bool = False) -> int:
    """Sync all discovered skills to target destination."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    skills = discover_skills()

    print(f"🔄 Syncing {target_name} skills...")
    print(f"  Source:      {REPO_ROOT}")
    print(f"  Destination: {dest_dir}\n")

    if dry_run:
        print("🔍 DRY RUN MODE (no files will be modified)\n")

    synced, skipped = 0, 0
    for src in skills:
        name = src.name
        dest = dest_dir / name
        if dry_run:
            print(f"→ Would sync: {name}")
            synced += 1
            continue

        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*EXCLUSIONS))
            print(f"✓ {name}")
            synced += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            skipped += 1

    mode_str = "🔍 DRY RUN: No files were modified" if dry_run else "✅ Sync complete!"
    print(f"\n{mode_str}\n  Synced:  {synced} skills\n  Skipped: {skipped} skills\n")
    print(f"📍 {target_name} skills: {dest_dir}")
    print(f"   Installed: {len(list(dest_dir.glob('*')))}/{len(skills)} skills")

    if skipped:
        return 1
    return verify_skills(target_name, dest_dir) if verify and not dry_run else 0


def parse_args(description: str) -> argparse.Namespace:
    """Parse common CLI arguments for sync scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    parser.add_argument("--verify", action="store_true", help="Verify checksum and file parity after syncing")
    return parser.parse_args()


# Backward compatibility alias
parse_dry_run_args = parse_args

