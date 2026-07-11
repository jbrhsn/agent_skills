#!/usr/bin/env python3
"""Convert generated carousel SVG files to PNG.

Tries to use cairosvg if installed. If cairosvg is unavailable, this script
degrades gracefully: it prints clear instructions and exits 0 (SVGs remain
valid output). It never hard-fails the carousel workflow.

Example:
    python3 svg_to_png.py linkedin/carousels/my-carousel
    python3 svg_to_png.py linkedin/carousels/my-carousel --out png_out
"""
import argparse
import glob
import os
import sys

INSTALL_HINT = (
    "PNG conversion needs 'cairosvg', which is not installed.\n"
    "  Install it with:  uv pip install cairosvg   (or)   pip install cairosvg\n"
    "Alternatively, open the .svg files in a browser or a vector tool\n"
    "(Inkscape, Figma, Illustrator) and export them to PNG.\n"
    "The SVG files are already valid, postable output on their own."
)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert carousel SVGs to PNG using cairosvg (optional dependency).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("svg_dir", help="Directory containing .svg files.")
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory for .png files (defaults to svg_dir).",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Output scale factor (default 1.0 -> 1080x1350).",
    )
    args = parser.parse_args(argv)

    if not os.path.isdir(args.svg_dir):
        print(f"error: {args.svg_dir} is not a directory", file=sys.stderr)
        return 2

    svgs = sorted(glob.glob(os.path.join(args.svg_dir, "*.svg")))
    if not svgs:
        print(f"No .svg files found in {args.svg_dir}", file=sys.stderr)
        return 1

    try:
        import cairosvg  # type: ignore
    except ImportError:
        print(INSTALL_HINT)
        # Graceful degrade: not an error for the overall skill.
        return 0

    out_dir = args.out or args.svg_dir
    os.makedirs(out_dir, exist_ok=True)

    for svg_path in svgs:
        base = os.path.splitext(os.path.basename(svg_path))[0]
        png_path = os.path.join(out_dir, base + ".png")
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            scale=args.scale,
        )
        print(f"wrote {png_path}")

    print(f"\n{len(svgs)} PNG file(s) written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
