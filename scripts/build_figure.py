#!/usr/bin/env python3
"""Compile a standalone TikZ figure, measure it, render it, and report problems.

Why this exists: a figure that compiles is not a figure that reads correctly, and
a figure whose bounding box silently grew to 25 cm looks fine in the PDF viewer
but shrinks every other element when it is scaled into the column. This script
makes both failures visible.

Usage
    python build_figure.py figures/fig.tex
    python build_figure.py figures/fig.tex --target-width 14.8 --dpi 300

Exit codes
    0  compiled, checks clean
    1  compile failed
    2  compiled but a check failed (canvas size, overfull boxes)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PT_PER_CM = 72.0 / 2.54


def which(*names: str) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, errors="replace"
    )


def page_size_cm(pdf: Path, pdfinfo: str) -> tuple[float, float] | None:
    out = run([pdfinfo, str(pdf)], pdf.parent).stdout
    match = re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)\s+pts", out)
    if not match:
        return None
    return float(match.group(1)) / PT_PER_CM, float(match.group(2)) / PT_PER_CM


def overfull_boxes(log_text: str) -> list[str]:
    return re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\).*", log_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path, help="path to the standalone .tex figure")
    parser.add_argument(
        "--target-width",
        type=float,
        default=None,
        help="intended printed width in cm; a canvas wider than this is flagged",
    )
    parser.add_argument("--dpi", type=int, default=300, help="preview raster dpi")
    parser.add_argument(
        "--no-600", action="store_true", help="skip the 600 dpi submission raster"
    )
    parser.add_argument(
        "--max-height", type=float, default=23.0, help="tallest allowed canvas, cm"
    )
    args = parser.parse_args()

    tex = args.tex.resolve()
    if not tex.exists():
        print(f"error: {tex} not found", file=sys.stderr)
        return 1

    pdflatex = which("pdflatex")
    if not pdflatex:
        print("error: pdflatex not on PATH (install MiKTeX or TeX Live)", file=sys.stderr)
        return 1

    stem = tex.stem
    pdf = tex.with_suffix(".pdf")

    print(f"compiling {tex.name}")
    result = run(
        [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex.name], tex.parent
    )
    log = tex.with_suffix(".log")
    log_text = log.read_text(errors="replace") if log.exists() else ""

    if result.returncode != 0 or not pdf.exists():
        print("\ncompile FAILED\n", file=sys.stderr)
        for line in log_text.splitlines():
            if line.startswith("!") or "Emergency stop" in line:
                print(f"  {line}", file=sys.stderr)
        tail = result.stdout.strip().splitlines()[-12:]
        print("\n".join(tail), file=sys.stderr)
        return 1

    problems: list[str] = []

    pdfinfo = which("pdfinfo")
    size = page_size_cm(pdf, pdfinfo) if pdfinfo else None
    if size:
        width, height = size
        print(f"canvas   {width:.2f} x {height:.2f} cm")
        if args.target_width:
            if width > args.target_width * 1.05:
                problems.append(
                    f"canvas is {width:.2f} cm wide but the target is "
                    f"{args.target_width:.2f} cm. Most likely a text node is missing "
                    f"text width and is stretching the bounding box."
                )
            elif width < args.target_width * 0.75:
                problems.append(
                    f"canvas is only {width:.2f} cm wide against a "
                    f"{args.target_width:.2f} cm target; the figure will be scaled up "
                    f"and its line widths will grow with it."
                )
        if height > args.max_height:
            problems.append(f"canvas is {height:.2f} cm tall, over the {args.max_height} cm limit.")
    else:
        print("canvas   unknown (pdfinfo unavailable)")

    wide = overfull_boxes(log_text)
    if wide:
        problems.append(
            f"{len(wide)} overfull box(es): "
            + ", ".join(f"{w}pt" for w in wide[:5])
            + ("" if len(wide) <= 5 else ", ...")
            + " — text is spilling past a node or line width."
        )

    pdftoppm = which("pdftoppm")
    if pdftoppm:
        for dpi, suffix in [(args.dpi, ""), (600, "_600dpi")]:
            if suffix and args.no_600:
                continue
            out = tex.parent / f"{stem}{suffix}"
            run([pdftoppm, "-png", "-r", str(dpi), "-singlefile", pdf.name, out.name],
                tex.parent)
            png = out.with_suffix(".png")
            if png.exists():
                px = ""
                try:
                    from PIL import Image

                    with Image.open(png) as im:
                        px = f"  {im.size[0]}x{im.size[1]} px"
                except Exception:
                    pass
                print(f"raster   {png.name}  {dpi} dpi{px}")
    else:
        print("raster   skipped (pdftoppm unavailable)")

    log.unlink(missing_ok=True)
    tex.with_suffix(".aux").unlink(missing_ok=True)

    if problems:
        print("\nchecks")
        for item in problems:
            print(f"  ! {item}")
        print(f"\nopen {stem}.png and inspect it before declaring the figure done.")
        return 2

    print("\nchecks   clean — open the PNG and inspect it anyway.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
