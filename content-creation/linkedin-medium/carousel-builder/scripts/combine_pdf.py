#!/usr/bin/env python3
"""Combine carousel SVG files into a single multi-page PDF.

Rasterizes each .svg to a PNG page (via cairosvg), then bundles all pages into
a single PDF (via Pillow). Preferred path is: cairosvg + Pillow, both optional
add-ons for the carousel skill.

Degrades gracefully unless --install-missing is supplied:
  - If cairosvg/Pillow is missing: print a uv install hint, exit 0.
  - With --install-missing: create .venv with uv, install cairosvg + pillow,
    then re-run this script with the venv Python.

The SVG files remain valid, postable output on their own regardless.

Example:
    python3 combine_pdf.py linkedin/carousels/my-carousel
    python3 combine_pdf.py linkedin/carousels/my-carousel --out out/deck.pdf --scale 2.0
"""
import argparse
import glob
import io
import os
import shutil
import subprocess
import sys

INSTALL_HINT_FULL = (
    "PDF combine needs 'cairosvg' (SVG rasterizer) and 'Pillow' (PDF writer),\n"
    "which are not installed.\n"
    "  Recommended:  uv venv .venv && uv pip install --python .venv/bin/python cairosvg pillow\n"
    "The SVG files are already valid, postable output on their own."
)


def default_out_path(svg_dir, slug):
    return os.path.join(svg_dir, f"{slug}.pdf")


def infer_slug(svg_paths):
    """Infer the carousel slug from filenames like '<slug>-01.svg'."""
    if not svg_paths:
        return "carousel"
    base = os.path.splitext(os.path.basename(svg_paths[0]))[0]
    # strip trailing "-NN"
    if "-" in base and base.rsplit("-", 1)[-1].isdigit():
        return base.rsplit("-", 1)[0]
    return base or "carousel"


def combine_with_pillow(svgs, out_pdf, scale):
    import cairosvg  # type: ignore
    from PIL import Image  # type: ignore

    pages = []
    for svg_path in svgs:
        png_bytes = cairosvg.svg2png(url=svg_path, scale=scale)
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        pages.append(img)

    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)) or ".", exist_ok=True)
    first, rest = pages[0], pages[1:]
    first.save(
        out_pdf,
        format="PDF",
        save_all=True,
        append_images=rest,
        resolution=150.0,
    )
    return out_pdf


def missing_deps():
    missing = []
    try:
        import cairosvg  # noqa: F401
    except ImportError:
        missing.append("cairosvg")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("pillow")
    return missing


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
    commands.append(["uv", "pip", "install", "--python", python, "cairosvg", "pillow"])
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
    env["CAROUSEL_PDF_UV_BOOTSTRAPPED"] = "1"
    return subprocess.run([python, os.path.abspath(__file__), *argv], env=env).returncode


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Combine carousel SVGs into a single multi-page PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("svg_dir", help="Directory containing .svg files.")
    parser.add_argument("--out", default=None,
                        help="Output PDF path (default: <svg_dir>/<slug>.pdf).")
    parser.add_argument("--scale", type=float, default=1.0,
                        help="Rasterization scale for PNG pages (default 1.0 -> 1080x1350).")
    parser.add_argument("--install-missing", action="store_true",
                        help="Use uv to create .venv and install cairosvg+pillow if missing. Ask the user before using this flag.")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.svg_dir):
        print(f"error: {args.svg_dir} is not a directory", file=sys.stderr)
        return 2

    svgs = sorted(glob.glob(os.path.join(args.svg_dir, "*.svg")))
    if not svgs:
        print(f"No .svg files found in {args.svg_dir}", file=sys.stderr)
        return 1

    slug = infer_slug(svgs)
    out_pdf = args.out or default_out_path(args.svg_dir, slug)

    missing = missing_deps()
    if missing:
        if args.install_missing and not os.environ.get("CAROUSEL_PDF_UV_BOOTSTRAPPED"):
            print(f"Missing PDF dependencies: {', '.join(missing)}")
            print("Creating .venv with uv and installing cairosvg + pillow...")
            sys.stdout.flush()
            rc = install_with_uv()
            if rc:
                return rc
            rerun_args = [a for a in (argv or sys.argv[1:]) if a != "--install-missing"]
            return rerun_with_venv(rerun_args)
        print(INSTALL_HINT_FULL)
        return 0

    pdf_path = combine_with_pillow(svgs, out_pdf, args.scale)
    print(f"wrote {pdf_path}")
    print(f"\ncombined {len(svgs)} slide(s) into {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
