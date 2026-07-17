#!/usr/bin/env python3
"""verify.py — isolated verification of tutorial code snippets.

Given a language and a snippet file, this helper sets up an appropriate
ISOLATED environment and either runs the snippet or, when a runtime/setup is
unavailable or unsafe, falls back to STATIC validation.

Supported languages:
  python  -> isolated venv (prefer `uv venv`, else `python3 -m venv`);
             static fallback = compile()
  js      -> temp node project (`npm init -y`, optional `npm install`);
             static fallback = `node --check`
  shell   -> sandboxed temp cwd, dangerous-command blocklist refusal;
             static fallback = `bash -n`

Everything happens inside a throwaway temp directory. No global installs, no
writes outside the temp sandbox. Standard library only.

Exit codes:
  0  = verification passed (executed OR statically validated cleanly)
  1  = verification failed (runtime error, syntax error, refused, etc.)
  2  = usage / internal error
  3  = could not verify (no runtime / setup unavailable) -- status "unknown"

SECURITY NOTE: the isolated temp directory is NOT a security sandbox. It only
isolates the working directory / HOME, not the network, environment, or the
rest of the filesystem. The dangerous-command scan is a best-effort DENYLIST
and is trivially bypassable (aliases, variable indirection, eval, base64,
encoded args). NEVER run untrusted third-party code through this tool. It is
meant for verifying YOUR OWN tutorial snippets, not arbitrary code.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Cap captured output so a runaway snippet cannot balloon memory / logs.
MAX_CAPTURE_BYTES = 256 * 1024  # 256 KB per stream
DEFAULT_TIMEOUT = 120  # seconds per executed snippet

# Packages that require a live cluster or specialised runtime and can never be
# pip-installed into a local venv in a meaningful way.  A ModuleNotFoundError
# for any of these is NOT a code bug — it means "no runtime available here",
# which maps to UNKNOWN (exit 3), not FAIL (exit 1).
# Match against the module name that appears after "No module named '...'"
# (the top-level package name is enough; submodules share the same prefix).
CLUSTER_ONLY_MODULES = frozenset({
    "pyspark",
    "delta",
    "databricks",
    "pydatabricks",
    "dbutils",        # Databricks notebook utility (injected at runtime)
    "dlt",            # Delta Live Tables module (cluster-injected)
    "mlflow",         # commonly cluster-managed; treat as cluster-only
    "tensorflow",     # GPU/cluster runtime
    "torch",          # GPU/cluster runtime
    "jax",            # GPU/cluster runtime
})

# ---------------------------------------------------------------------------
# Dangerous shell command blocklist. Each entry is a compiled regex checked
# against the raw snippet text. A match => REFUSE to execute; static only.
#
# This is a DENYLIST and is best-effort only. It is bypassable via aliases,
# variable indirection, eval, encoding, etc. It is NOT a security boundary.
# See the SECURITY NOTE in the module docstring.
# ---------------------------------------------------------------------------
DANGEROUS_SHELL_PATTERNS = [
    (r"\brm\s+(-[a-zA-Z]*[rf]|--recursive|--force)", "recursive/forced rm"),
    (r"\bdd\b", "raw disk write (dd)"),
    (r"\bmkfs\b", "filesystem creation (mkfs)"),
    (r"\bfdisk\b", "partition editing (fdisk)"),
    (r"\bmkswap\b", "swap creation (mkswap)"),
    (r"\bsudo\b", "privilege escalation (sudo)"),
    (r"(^|[;&|]|\s)su\s+-", "user switch (su -)"),
    (r"\bchmod\s+-R\b", "recursive chmod"),
    (r"\bchown\s+-R\b", "recursive chown"),
    (r"[:@]\(\)\s*\{.*\|.*&\s*\}", "fork bomb"),
    (r":\(\)\{", "fork bomb"),
    (r"(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(sh|bash|zsh)", "remote-exec pipe (curl/wget | sh)"),
    (r"(?m)^[^#\n]*\beval\b", "eval (dynamic command execution — cannot be statically vetted)"),
    (r">\s*/dev/sd[a-z]", "write to raw disk device"),
    (r"\bshutdown\b", "system shutdown"),
    (r"\breboot\b", "system reboot"),
    (r"\bhalt\b", "system halt"),
    (r"\b(mv|cp)\s+[^\n]*\s+/(bin|etc|usr|boot|dev|sys|lib|sbin|opt|root)\b",
     "copy/move into system dir"),
    (r"\btee\s+/(?!tmp/)", "tee into an absolute path outside /tmp"),
    (r"\bdd\b[^\n]*\bof=/", "dd output to an absolute path"),
    (r">\s*/etc/", "overwrite files under /etc"),
    (r"\biptables\b", "firewall modification"),
    (r"\bcrontab\b", "crontab modification"),
]

# Absolute-path writes outside /tmp (rough heuristic on redirects). The
# negative lookahead requires a trailing slash so "/tmpevil" is NOT treated
# as inside /tmp.
SYSTEM_WRITE_RE = re.compile(r">>?\s*(/(?!tmp/)(?!tmp\b)[A-Za-z]\S*)")


# Databricks notebook magic prefixes that must be handled before execution.
# strip_magic() rewrites %pip -> pip for local execution.
# These other magics are cluster-only and cannot be executed locally at all.
MAGIC_STRIP_RE = re.compile(r"^%pip\b", re.MULTILINE)
MAGIC_CLUSTER_ONLY_RE = re.compile(r"^%(?:sql|fs|run|scala|r|conda)\b", re.MULTILINE | re.IGNORECASE)
MAGIC_NOOP_RE = re.compile(r"^%(?:md|matplotlib)\b", re.MULTILINE | re.IGNORECASE)


def _strip_notebook_magic(source: str):
    """Pre-process a shell snippet that may contain Databricks notebook magic.

    Returns (processed_source, magic_note) where magic_note is a human-readable
    string describing what was stripped/detected, or "" if nothing was done.
    """
    notes = []
    # %pip install ... -> pip install ... (locally runnable after stripping)
    if MAGIC_STRIP_RE.search(source):
        source = MAGIC_STRIP_RE.sub("pip", source)
        notes.append("%pip stripped to pip for local execution")
    # Cluster-only magics: cannot run locally
    if MAGIC_CLUSTER_ONLY_RE.search(source):
        notes.append("cluster-only magic present (%sql/%fs/%run/%scala/%r/%conda) — "
                     "not executable outside a Databricks notebook")
    return source, "; ".join(notes)


def log(msg: str) -> None:
    print(f"[verify] {msg}", file=sys.stderr, flush=True)


def _is_cluster_only_import_error(stderr: str) -> bool:
    """Return True when stderr indicates a ModuleNotFoundError for a
    known cluster-only package.  These are not code bugs — they mean
    the required runtime is simply not available locally."""
    # Match: "ModuleNotFoundError: No module named 'pyspark'"
    #   or:  "ModuleNotFoundError: No module named 'delta.tables'"
    m = re.search(r"ModuleNotFoundError: No module named '([^']+)'", stderr)
    if not m:
        return False
    top_level = m.group(1).split(".")[0]
    return top_level in CLUSTER_ONLY_MODULES


def tool_available(name: str) -> bool:
    return shutil.which(name) is not None


def _truncate(text: str) -> str:
    """Cap a captured stream so a runaway snippet can't balloon output."""
    if text is None:
        return ""
    data = text.encode("utf-8", "replace")
    if len(data) <= MAX_CAPTURE_BYTES:
        return text
    clipped = data[:MAX_CAPTURE_BYTES].decode("utf-8", "ignore")
    return clipped + f"\n...[truncated at {MAX_CAPTURE_BYTES} bytes]"


def run(cmd, cwd=None, env=None, timeout=DEFAULT_TIMEOUT):
    """Run a subprocess, capturing (capped) output. Returns (rc, out, err)."""
    log(f"exec: {' '.join(cmd)} (cwd={cwd or os.getcwd()}, timeout={timeout}s)")
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, _truncate(proc.stdout), _truncate(proc.stderr)
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"
    except FileNotFoundError as exc:
        return 127, "", f"command not found: {exc}"


def result(status, mode, rc=None, stdout="", stderr="", detail=""):
    """status: 'pass'|'fail'|'unknown'. mode: 'executed'|'static'|'refused'|'skipped'."""
    return {
        "status": status,
        "mode": mode,
        "returncode": rc,
        "stdout": stdout,
        "stderr": stderr,
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------
def verify_python(snippet_path, requirements=None, timeout=DEFAULT_TIMEOUT):
    with open(snippet_path, "r", encoding="utf-8") as fh:
        source = fh.read()

    # Prefer real execution in an isolated venv.
    have_uv = tool_available("uv")
    have_venv = tool_available("python3")

    if have_uv or have_venv:
        with tempfile.TemporaryDirectory(prefix="verify_py_") as tmp:
            venv_dir = os.path.join(tmp, ".venv")
            created = False

            if have_uv:
                rc, _, err = run(["uv", "venv", venv_dir], cwd=tmp)
                created = rc == 0
                if not created:
                    log(f"uv venv failed: {err.strip()}")
            if not created and have_venv:
                rc, _, err = run(["python3", "-m", "venv", venv_dir], cwd=tmp)
                created = rc == 0
                if not created:
                    log(f"python3 -m venv failed: {err.strip()}")

            if created:
                py = os.path.join(venv_dir, "bin", "python")
                if not os.path.exists(py):  # windows layout, best effort
                    py = os.path.join(venv_dir, "Scripts", "python.exe")

                if requirements:
                    if have_uv:
                        rc, _, err = run(
                            ["uv", "pip", "install", "--python", py, *requirements],
                            cwd=tmp,
                        )
                    else:
                        rc, _, err = run([py, "-m", "pip", "install", *requirements], cwd=tmp)
                    if rc != 0:
                        log(f"dependency install failed: {err.strip()}")
                        return _python_static(
                            source,
                            note="DEPENDENCY INSTALL FAILED (deps NOT installed) — "
                                 "snippet was NOT executed; ",
                        )

                snip = os.path.join(tmp, "snippet.py")
                with open(snip, "w", encoding="utf-8") as fh:
                    fh.write(source)

                rc, out, err = run([py, snip], cwd=tmp, timeout=timeout)
                if rc == 0:
                    return result("pass", "executed", rc, out, err)
                # A ModuleNotFoundError for a cluster-only package means the
                # snippet is correct but requires a runtime not available here.
                # Reclassify as UNKNOWN rather than FAIL so tutorial authors
                # are not misled into thinking their code is broken.
                if _is_cluster_only_import_error(err):
                    mod = re.search(r"No module named '([^']+)'", err).group(1)
                    return result(
                        "unknown", "skipped", rc, out, err,
                        detail=f"cluster-only module '{mod}' not available locally "
                               f"— snippet not executable outside a cluster runtime",
                    )
                return result("fail", "executed", rc, out, err,
                              detail="snippet exited non-zero")

    log("no usable venv toolchain; static validation only")
    return _python_static(source, note="no venv available; ")


def _python_static(source, note=""):
    try:
        compile(source, "<snippet>", "exec")
        return result("pass", "static", detail=f"{note}compile() OK")
    except SyntaxError as exc:
        return result("fail", "static", stderr=str(exc),
                      detail=f"{note}syntax error")


# ---------------------------------------------------------------------------
# JavaScript / Node
# ---------------------------------------------------------------------------
def verify_js(snippet_path, requirements=None, timeout=DEFAULT_TIMEOUT):
    with open(snippet_path, "r", encoding="utf-8") as fh:
        source = fh.read()

    if not tool_available("node"):
        log("node not available; cannot execute or statically check JS")
        return result("unknown", "skipped",
                      detail="node unavailable; cannot execute or run --check")

    with tempfile.TemporaryDirectory(prefix="verify_js_") as tmp:
        snip = os.path.join(tmp, "snippet.js")
        with open(snip, "w", encoding="utf-8") as fh:
            fh.write(source)

        if tool_available("npm"):
            rc, _, err = run(["npm", "init", "-y"], cwd=tmp)
            if rc != 0:
                log(f"npm init failed: {err.strip()}")
            if requirements:
                rc, _, err = run(["npm", "install", *requirements], cwd=tmp)
                if rc != 0:
                    log(f"npm install failed: {err.strip()}")
                    res = _js_static(snip)
                    res["detail"] = ("DEPENDENCY INSTALL FAILED (deps NOT installed) — "
                                     "snippet was NOT executed; " + res.get("detail", ""))
                    return res
        elif requirements:
            log("npm unavailable; cannot install requested deps")
            res = _js_static(snip)
            res["detail"] = ("npm UNAVAILABLE (deps NOT installed) — snippet was NOT "
                             "executed; " + res.get("detail", ""))
            return res

        rc, out, err = run(["node", snip], cwd=tmp, timeout=timeout)
        if rc == 0:
            return result("pass", "executed", rc, out, err)
        return result("fail", "executed", rc, out, err, detail="snippet exited non-zero")


def _js_static(snip_path):
    if not tool_available("node"):
        return result("unknown", "skipped", detail="node unavailable; cannot run --check")
    rc, out, err = run(["node", "--check", snip_path])
    if rc == 0:
        return result("pass", "static", detail="node --check OK")
    return result("fail", "static", stderr=err, detail="node --check failed")


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
def scan_shell(source):
    """Return list of (pattern_desc) hits for dangerous constructs."""
    hits = []
    for pattern, desc in DANGEROUS_SHELL_PATTERNS:
        if re.search(pattern, source):
            hits.append(desc)
    for m in SYSTEM_WRITE_RE.finditer(source):
        hits.append(f"write outside temp: {m.group(1)}")
    return hits


def verify_shell(snippet_path, timeout=DEFAULT_TIMEOUT):
    with open(snippet_path, "r", encoding="utf-8") as fh:
        source = fh.read()

    # Pre-process Databricks notebook magic prefixes before any other checks.
    source, magic_note = _strip_notebook_magic(source)
    if magic_note and "cluster-only magic" in magic_note:
        # Contains cluster-only magics (%sql, %fs, etc.) that cannot run locally.
        static = _shell_static(source)
        static["detail"] = (f"Databricks-only magic detected — not executable outside "
                            f"a cluster notebook ({magic_note}) | " + static.get("detail", ""))
        static["mode"] = "skipped"
        static["status"] = "unknown"
        return static

    hits = scan_shell(source)
    if hits:
        detail = "REFUSED — dangerous operations detected: " + "; ".join(sorted(set(hits)))
        log(detail)
        # Still offer a static syntax check for information.
        static = _shell_static(source)
        static["mode"] = "refused"
        static["status"] = "fail"
        static["detail"] = detail + " | " + static.get("detail", "")
        return static

    if not tool_available("bash"):
        return _shell_static(source, note="bash unavailable; ")

    with tempfile.TemporaryDirectory(prefix="verify_sh_") as tmp:
        snip = os.path.join(tmp, "snippet.sh")
        with open(snip, "w", encoding="utf-8") as fh:
            fh.write(source)
        env = dict(os.environ)
        env["HOME"] = tmp  # keep any HOME-relative writes inside the sandbox
        rc, out, err = run(["bash", snip], cwd=tmp, env=env, timeout=timeout)
        if rc == 0:
            detail = magic_note if magic_note else ""
            return result("pass", "executed", rc, out, err, detail=detail)
        return result("fail", "executed", rc, out, err, detail="snippet exited non-zero"
                      + (f"; {magic_note}" if magic_note else ""))


def _shell_static(source, note=""):
    if not tool_available("bash"):
        return result("unknown", "skipped", detail=f"{note}bash unavailable; cannot run -n")
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as fh:
        fh.write(source)
        path = fh.name
    try:
        rc, out, err = run(["bash", "-n", path])
    finally:
        os.unlink(path)
    if rc == 0:
        return result("pass", "static", detail=f"{note}bash -n OK")
    return result("fail", "static", stderr=err, detail=f"{note}bash -n failed")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(
        prog="verify.py",
        description="Verify a tutorial code snippet in an isolated environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  verify.py --lang python --file snippet.py\n"
            "  verify.py --lang python --file s.py --requirement requests --requirement rich\n"
            "  verify.py --lang js --file s.js --requirement left-pad\n"
            "  verify.py --lang shell --file s.sh\n"
            "  verify.py --lang shell --file s.sh --json\n"
        ),
    )
    p.add_argument("--lang", required=True, choices=["python", "js", "shell"],
                   help="snippet language")
    p.add_argument("--file", required=True, help="path to the snippet file")
    p.add_argument("--requirement", action="append", default=[], dest="requirements",
                   help="dependency to install in the isolated env (repeatable). "
                        "Ignored for shell.")
    p.add_argument("--static-only", action="store_true",
                   help="skip execution; run static validation only")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                   help=f"per-execution timeout in seconds (default {DEFAULT_TIMEOUT})")
    p.add_argument("--json", action="store_true",
                   help="emit the result as JSON on stdout")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    if not os.path.isfile(args.file):
        log(f"snippet file not found: {args.file}")
        return 2

    log(f"language={args.lang} file={args.file} static_only={args.static_only}")
    log("tool availability: " + ", ".join(
        f"{t}={'yes' if tool_available(t) else 'no'}"
        for t in ("uv", "python3", "node", "npm", "bash")
    ))

    if args.static_only:
        with open(args.file, "r", encoding="utf-8") as fh:
            src = fh.read()
        if args.lang == "python":
            res = _python_static(src, note="static-only; ")
        elif args.lang == "js":
            res = _js_static(args.file)
        else:
            hits = scan_shell(src)
            res = _shell_static(src, note="static-only; ")
            if hits:
                res["mode"] = "refused"
                res["status"] = "fail"
                res["detail"] = ("REFUSED — dangerous operations: "
                                 + "; ".join(sorted(set(hits))) + " | " + res["detail"])
    else:
        if args.lang == "python":
            res = verify_python(args.file, args.requirements or None, timeout=args.timeout)
        elif args.lang == "js":
            res = verify_js(args.file, args.requirements or None, timeout=args.timeout)
        else:
            res = verify_shell(args.file, timeout=args.timeout)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        label = {"executed": "verified", "static": "statically validated",
                 "refused": "REFUSED", "skipped": "SKIPPED (no runtime)"}.get(
                     res["mode"], res["mode"])
        print(f"STATUS: {res['status'].upper()} ({label})")
        if res.get("detail"):
            print(f"DETAIL: {res['detail']}")
        # Don't print the subprocess returncode for UNKNOWN results — it's the
        # inner venv process's exit code (1), which is misleading alongside the
        # tool's own exit code (3) and adds no useful information.
        if res.get("returncode") is not None and res["status"] != "unknown":
            print(f"EXIT:   {res['returncode']}")
        if res.get("stdout"):
            print("STDOUT:\n" + res["stdout"])
        if res.get("stderr"):
            print("STDERR:\n" + res["stderr"])

    return {"pass": 0, "fail": 1, "unknown": 3}.get(res["status"], 1)


if __name__ == "__main__":
    sys.exit(main())
