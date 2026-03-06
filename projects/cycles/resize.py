#!/usr/bin/env python3
"""Export resized web copies of photos using macOS sips. Originals are never modified."""

import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(BASE, "cycles_export")
OUTPUT_DIR = os.path.join(BASE, "photos-web")
MAX_EDGE = 1500


def resize_photos():
    if not os.path.isdir(PHOTOS_DIR):
        print(f"Error: '{PHOTOS_DIR}' not found.")
        return

    subdirs = sorted(
        d for d in os.listdir(PHOTOS_DIR)
        if os.path.isdir(os.path.join(PHOTOS_DIR, d))
    )

    total = 0
    for subdir in subdirs:
        src_dir = os.path.join(PHOTOS_DIR, subdir)
        dst_dir = os.path.join(OUTPUT_DIR, subdir)
        os.makedirs(dst_dir, exist_ok=True)

        for filename in sorted(os.listdir(src_dir)):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                continue

            src = os.path.join(src_dir, filename)
            dst = os.path.join(dst_dir, filename)

            subprocess.run(
                ["sips", "--resampleHeightWidthMax", str(MAX_EDGE), src, "--out", dst],
                check=True,
                capture_output=True,
            )
            src_size = os.path.getsize(src)
            dst_size = os.path.getsize(dst)
            print(f"  {subdir}/{filename}: {src_size // 1024}KB → {dst_size // 1024}KB")
            total += 1

    print(f"\nDone. {total} photo(s) exported to photos-web/.")


if __name__ == "__main__":
    resize_photos()
