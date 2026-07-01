#!/usr/bin/env python3
"""
Generate a product thumbnail for the Dulzumat website.

All product thumbnails must be:
  - 620x620 px, JPEG, ~60-150 KB
  - Subject centered using centroid (not bounding box) to account for
    asymmetric shadows/edges in camera photos
  - ~20px white-space margin around the subject on all sides
  - Background filled with the photo's own background colour when
    the crop extends beyond the original frame

IMPORTANT — consistency rule:
  The thumbnail and the main product image must use the SAME canvas crop
  so the white border around the subject looks identical in the category
  listing and on the product detail page. Run this script once for the
  thumbnail (620x620), then reuse the same canvas_side value to generate
  the main image at 1200x1200. See CLAUDE.md for reference canvas sizes.

Usage:
    python3 scripts/make-thumbnail.py <source_image> <output_thumb>

Example:
    python3 scripts/make-thumbnail.py ~/Downloads/DSC01238.jpg \
        static/images/products/pasteles-barca-de-avellana-thumb.jpg
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

# ── tuneable parameters ────────────────────────────────────────────
THUMB_SIZE = 620          # output px (square)
MARGIN_PX  = 20          # white-space margin around subject in output px
BG_DIFF_THRESHOLD = 20   # pixels with max-channel diff > this = subject
# ──────────────────────────────────────────────────────────────────


def make_thumbnail(src_path: str, dst_path: str) -> None:
    img = Image.open(src_path)
    arr = np.array(img).astype(float)
    w, h = img.size

    # ── detect background colour from the four corners ──────────────
    bg = np.mean([
        arr[:20, :20],
        arr[:20, -20:],
        arr[-20:, :20],
        arr[-20:, -20:],
    ], axis=(0, 1, 2))
    bg_color = tuple(int(round(c)) for c in bg)

    # ── find subject mask ──────────────────────────────────────────
    diff = np.abs(arr - bg).max(axis=2)
    mask = diff > BG_DIFF_THRESHOLD
    if not mask.any():
        raise ValueError("No subject found — try lowering BG_DIFF_THRESHOLD")

    ys, xs = np.where(mask)

    # Use centroid as visual center (bounding-box center is skewed by
    # shadows/edges that extend asymmetrically from the main subject)
    cx, cy = int(xs.mean()), int(ys.mean())

    # Bounding box used only to size the canvas
    sw = xs.max() - xs.min()   # subject width in original px
    sh = ys.max() - ys.min()   # subject height in original px

    # ── compute canvas size ────────────────────────────────────────
    # Scale so that the wider subject dimension leaves MARGIN_PX on each side
    scale      = sw / (THUMB_SIZE - 2 * MARGIN_PX)
    pad_orig   = round(MARGIN_PX * scale)
    canvas_side = sw + 2 * pad_orig      # square canvas in original px

    # ── crop box centered on centroid ─────────────────────────────
    left   = cx - canvas_side // 2
    top    = cy - canvas_side // 2
    right  = left + canvas_side
    bottom = top  + canvas_side

    # ── build canvas (fill OOB areas with background colour) ───────
    canvas = Image.new("RGB", (canvas_side, canvas_side), bg_color)
    src_l, src_t = max(0, left),  max(0, top)
    src_r, src_b = min(w, right), min(h, bottom)
    canvas.paste(
        img.crop((src_l, src_t, src_r, src_b)),
        (src_l - left, src_t - top),
    )

    # ── resize and save ────────────────────────────────────────────
    result = canvas.resize((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
    result.save(dst_path, "JPEG", quality=92)

    size_kb = Path(dst_path).stat().st_size // 1024
    print(f"Saved {dst_path}  ({THUMB_SIZE}x{THUMB_SIZE}px, {size_kb} KB)")
    print(f"  centroid: ({cx},{cy})  canvas: {canvas_side}px  pad: {pad_orig}px")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    make_thumbnail(sys.argv[1], sys.argv[2])
