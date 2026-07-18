#!/usr/bin/env python3
"""Rasterize medium-imager SVG files to PNG (the actual Medium-uploadable asset).

Medium does not accept raw SVG uploads, so PNG is the real deliverable for
this skill (unlike carousel-builder's optional PDF step). This script treats
'cairosvg' as a REQUIRED dependency: if it's missing, it prints install
instructions and exits non-zero rather than degrading gracefully.

Rasterizes every <slug>-cover.svg and <slug>-NN-<type>.svg file found in the
input directory (or a single file / filtered subset via --only) to PNG at
the given scale (default 2.0x for retina-sharp images).

If cairosvg is missing, the script prints an install hint and exits non-zero
(PNG is the required deliverable — it does NOT degrade to success). With
--install-missing, it instead creates a local .venv with uv, installs
cairosvg into it, then re-runs this script with the venv Python. An env-var
guard (MEDIUM_IMAGER_UV_BOOTSTRAPPED) prevents infinite re-exec loops.

Example:
    python3 svg_to_png.py medium/images/my-article
    python3 svg_to_png.py medium/images/my-article --only cover
    python3 svg_to_png.py medium/images/my-article --only 1 --scale 2.0
    python3 svg_to_png.py medium/images/my-article --install-missing
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

INSTALL_HINT = (
    "medium-imager requires 'cairosvg' to rasterize SVG to PNG (Medium does\n"
    "not accept raw SVG uploads), and it is not installed.\n"
    "  Install it with:  uv pip install cairosvg\n"
    "                (or) pip install cairosvg\n"
    "No PNG files were written. The SVG source files are still valid, but\n"
    "PNG is the deliverable this skill considers 'done'."
)


def find_svgs(svg_dir, only):
    all_svgs = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    if only is None:
        return all_svgs
    if only == "cover":
        return [f for f in all_svgs if f.endswith("-cover.svg")]
    # numeric --only N: match "-NN-" in filename
    try:
        target = f"-{int(only):02d}-"
    except ValueError as exc:
        raise ValueError(f"--only must be 'cover' or an integer, got {only!r}") from exc
    return [f for f in all_svgs if target in os.path.basename(f)]


def venv_python():
    return os.path.join(os.getcwd(), ".venv", "Scripts" if os.name == "nt" else "bin", "python")


def install_with_uv():
    if shutil.which("uv") is None:
        print("error: uv is not installed or not on PATH", file=sys.stderr)
        return 1
    python = venv_python()
    commands = []
    if not os.path.exists(python):
        commands.append(["uv", "venv", ".venv"])
    commands.append(["uv", "pip", "install", "--python", python, "cairosvg"])
    for command in commands:
        result = subprocess.run(command)
        if result.returncode:
            return result.returncode
    return 0


def rerun_with_venv(argv):
    python = venv_python()
    if not os.path.exists(python):
        print(f"error: expected venv Python at {python}", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["MEDIUM_IMAGER_UV_BOOTSTRAPPED"] = "1"
    return subprocess.run([python, os.path.abspath(__file__), *argv], env=env).returncode


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Rasterize medium-imager SVGs to PNG via cairosvg (required dependency).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("svg_dir", help="Directory containing .svg files.")
    parser.add_argument("--only", default=None,
                         help="Rasterize only 'cover' or a 1-based inner image number.")
    parser.add_argument("--scale", type=float, default=2.0,
                         help="Rasterization scale (default 2.0 -> retina-sharp PNGs).")
    parser.add_argument("--install-missing", action="store_true",
                         help="Use uv to create .venv and install cairosvg if missing. Ask the user before using this flag.")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.svg_dir):
        print(f"error: {args.svg_dir} is not a directory", file=sys.stderr)
        return 2

    try:
        svgs = find_svgs(args.svg_dir, args.only)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not svgs:
        print(f"No matching .svg files found in {args.svg_dir} (only={args.only})", file=sys.stderr)
        return 1

    try:
        import cairosvg  # type: ignore  # noqa: F401
    except ImportError:
        if args.install_missing and not os.environ.get("MEDIUM_IMAGER_UV_BOOTSTRAPPED"):
            print("cairosvg missing; creating .venv with uv and installing cairosvg...")
            sys.stdout.flush()
            rc = install_with_uv()
            if rc:
                return rc
            rerun_args = [a for a in (argv or sys.argv[1:]) if a != "--install-missing"]
            return rerun_with_venv(rerun_args)
        print(INSTALL_HINT, file=sys.stderr)
        return 1

    written = []
    for svg_path in svgs:
        png_path = os.path.splitext(svg_path)[0] + ".png"
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=args.scale)
        written.append(png_path)

    for f in written:
        print(f"wrote {f}")
    print(f"\n{len(written)} PNG file(s) written to {args.svg_dir} (scale {args.scale}x)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
