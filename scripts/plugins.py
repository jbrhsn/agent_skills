#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Plugin discovery and agent composition.

Base agents in `agents/` are canonical. A plugin may ship *overlays* that add
frontmatter keys and append a titled prose section to a base agent, plus
net-new agents that have no base counterpart. Composition happens in memory at
sync time — nothing composed is ever written back into the repo.
"""

import json
from pathlib import Path

import yaml

from common import REPO_ROOT

PLUGINS_DIR = REPO_ROOT / "plugins"
AGENTS_DIR = REPO_ROOT / "agents"
MANIFEST_NAME = ".agent_skills_manifest.json"


# --- Discovery ---------------------------------------------------------------


def discover_plugins() -> dict[str, dict]:
    """Load every plugins/*/plugin.json, keyed by plugin name."""
    found = {}
    for manifest in sorted(PLUGINS_DIR.glob("*/plugin.json")):
        data = json.loads(manifest.read_text())
        data["root"] = manifest.parent
        found[data["name"]] = data
    return found


def select_plugins(names: list[str]) -> list[dict]:
    """Resolve plugin names to manifests, sorted for deterministic composition."""
    available = discover_plugins()
    unknown = [n for n in names if n not in available]
    if unknown:
        raise ValueError(f"Unknown plugin(s): {', '.join(unknown)}. Available: {', '.join(available) or 'none'}")
    return [available[n] for n in sorted(names)]


def validate(plugin: dict) -> None:
    """Fail loudly if a manifest points at files that do not exist."""
    root, name = plugin["root"], plugin["name"]
    base_names = {p.name for p in base_agents()}
    for rel in plugin.get("runtime", []):
        if not (root / rel).is_file():
            raise ValueError(f"[{name}] runtime file missing: {rel}")
    for rel in plugin.get("agents", {}).get("new", []):
        if not (root / "agents" / rel).is_file():
            raise ValueError(f"[{name}] new agent missing: agents/{rel}")
    for rel in plugin.get("agents", {}).get("overlays", []):
        if not (root / "agents" / "overlays" / rel).is_file():
            raise ValueError(f"[{name}] overlay missing: agents/overlays/{rel}")
        if rel not in base_names:
            raise ValueError(f"[{name}] overlay '{rel}' targets no base agent in agents/")


def base_agents() -> list[Path]:
    return sorted(p for p in AGENTS_DIR.glob("*/*.md") if p.name != "README.md")


def runtime_files(plugins: list[dict]) -> list[tuple[str, Path]]:
    """(owning plugin name, source path) for every runtime file to install."""
    return [(p["name"], p["root"] / rel) for p in plugins for rel in p.get("runtime", [])]


# --- Frontmatter -------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")


def deep_merge(dst: dict, src: dict, owner: str, provenance: dict, path: str = "") -> None:
    """Recursively merge src into dst, erroring when two plugins disagree."""
    for key, value in src.items():
        full = f"{path}.{key}" if path else key
        # setdefault, not get: recurse even on first write so nested leaves get
        # provenance recorded — otherwise a later plugin overwrites them silently.
        if isinstance(value, dict) and isinstance(dst.setdefault(key, {}), dict):
            deep_merge(dst[key], value, owner, provenance, full)
            continue
        prior = provenance.get(full)
        if prior and prior[0] != owner and prior[1] != value:
            raise ValueError(
                f"Plugin conflict on '{full}': "
                f"'{prior[0]}' sets {prior[1]!r}, '{owner}' sets {value!r}. Resolve before syncing."
            )
        dst[key] = value
        provenance[full] = (owner, value)


# --- Composition -------------------------------------------------------------


def compose_agents(plugins: list[dict]) -> dict[str, str]:
    """Return {filename: content} for the full agent set given selected plugins."""
    overlays: dict[str, list[tuple[str, Path]]] = {}
    for plugin in plugins:
        for rel in plugin.get("agents", {}).get("overlays", []):
            overlays.setdefault(rel, []).append((plugin["name"], plugin["root"] / "agents" / "overlays" / rel))

    composed = {}
    for base in base_agents():
        if base.name not in overlays:
            composed[base.name] = base.read_text()  # verbatim: no yaml round-trip
            continue
        fm, body = split_frontmatter(base.read_text())
        delta, provenance, sections = {}, {}, []
        for owner, path in overlays[base.name]:
            over_fm, over_body = split_frontmatter(path.read_text())
            deep_merge(delta, over_fm, owner, provenance)
            if over_body.strip():
                sections.append(over_body.strip())
        deep_merge(fm, delta, "<composed>", {})
        # width: keep long description strings on one line rather than folding them
        dumped = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False, allow_unicode=True, width=4096)
        composed[base.name] = f"---\n{dumped}---\n" + "\n\n".join([body.rstrip(), *sections]) + "\n"

    for plugin in plugins:
        for rel in plugin.get("agents", {}).get("new", []):
            composed[rel] = (plugin["root"] / "agents" / rel).read_text()
    return composed


# --- Install manifest --------------------------------------------------------


def install(dest: Path, files: dict[str, str], dry_run: bool = False) -> tuple[int, int]:
    """Write `files` to dest, prune stale manifest-owned files, update the manifest.

    Shared by every sync script that installs a composed/translated agent set
    (OpenCode, Claude Code, ...). Returns (synced, skipped).
    """
    dest.mkdir(parents=True, exist_ok=True)
    synced, skipped = 0, 0
    for filename, content in sorted(files.items()):
        if dry_run:
            print(f"→ Would sync: {filename}")
            synced += 1
            continue
        try:
            (dest / filename).write_text(content)
            print(f"✓ {filename}")
            synced += 1
        except OSError as e:
            print(f"✗ {filename}: {e}")
            skipped += 1

    for stale in prune(dest, set(files), dry_run):
        print(f"{'→ Would remove' if dry_run else '🗑  Removed'} (no longer synced): {stale}")
    if not dry_run:
        write_manifest(dest, list(files))
    return synced, skipped


def write_manifest(dest: Path, files: list[str]) -> None:
    payload = {"version": 1, "note": "Written by agent_skills sync. Lists files it owns.", "files": sorted(files)}
    (dest / MANIFEST_NAME).write_text(json.dumps(payload, indent=2) + "\n")


def prune(dest: Path, keep: set[str], dry_run: bool = False) -> list[str]:
    """Remove files this tooling wrote previously that are no longer selected.

    Only files named in our own manifest are eligible — never anything the user
    or another tool put in these shared config directories.
    """
    manifest = dest / MANIFEST_NAME
    try:
        owned = json.loads(manifest.read_text()).get("files", []) if manifest.is_file() else []
    except (json.JSONDecodeError, OSError):
        owned = []
    stale = [f for f in owned if f not in keep and (dest / f).is_file()]
    if not dry_run:
        for name in stale:
            (dest / name).unlink()
    return stale
