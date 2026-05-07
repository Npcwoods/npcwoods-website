#!/usr/bin/env python3
"""Generate AVIF + WebP variants of hero/headshot images.

Input: paths to source images under /tmp/hero-opt/
Output: <name>-<width>.avif, <name>-<width>.webp, <name>-<width>.jpg (fallback)
in the output directory. Idempotent — skips variants that already exist unless
--force is passed.

Sizes generated:
  - chris-headshot.jpg (hero): 640, 960, 1280 wide
  - chris-woods-headshot.png (avatar, used sitewide in small sizes): 80, 160, 320 wide

Targets:
  - AVIF: quality 55 → typically 30-50% smaller than WebP
  - WebP: quality 78 → typically 25-35% smaller than JPG
  - JPG:  quality 82 (progressive) — fallback for old browsers
"""

from pathlib import Path
from PIL import Image
import pillow_avif  # noqa: F401 — registers AVIF codec
import sys
import argparse

VARIANTS = {
    "chris-headshot.jpg":       [640, 960, 1280],
    "chris-woods-headshot.png": [80, 160, 320, 640],
}


def save_variant(img: Image.Image, out_base: Path, width: int, force: bool):
    ratio = width / img.width
    size = (width, round(img.height * ratio))
    resized = img.resize(size, Image.LANCZOS)
    # strip alpha for JPEG output, keep for AVIF/WebP (they support it)
    flat = resized
    if resized.mode in ("RGBA", "LA", "P"):
        flat = Image.new("RGB", resized.size, (255, 255, 255))
        flat.paste(resized, mask=resized.split()[-1] if resized.mode in ("RGBA", "LA") else None)

    avif = out_base.with_name(f"{out_base.stem}-{width}.avif")
    webp = out_base.with_name(f"{out_base.stem}-{width}.webp")
    jpg = out_base.with_name(f"{out_base.stem}-{width}.jpg")

    if force or not avif.exists():
        resized.save(avif, "AVIF", quality=55)
    if force or not webp.exists():
        resized.save(webp, "WEBP", quality=78, method=6)
    if force or not jpg.exists():
        flat.save(jpg, "JPEG", quality=82, progressive=True, optimize=True)

    sizes = {p.suffix: p.stat().st_size for p in (avif, webp, jpg)}
    print(f"  {width}w  avif={sizes['.avif']/1024:5.1f}K  "
          f"webp={sizes['.webp']/1024:5.1f}K  jpg={sizes['.jpg']/1024:5.1f}K")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="/tmp/hero-opt",
                    help="directory containing source images")
    ap.add_argument("--out", default="/tmp/hero-opt/out",
                    help="directory to write variants to")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for filename, widths in VARIANTS.items():
        source = src / filename
        if not source.exists():
            print(f"[skip] {filename} not in {src}")
            continue
        print(f"[{filename}]")
        img = Image.open(source)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        out_base = out / filename
        for w in widths:
            if w > img.width:
                print(f"  {w}w skipped (source only {img.width}w)")
                continue
            save_variant(img, out_base, w, args.force)


if __name__ == "__main__":
    main()
