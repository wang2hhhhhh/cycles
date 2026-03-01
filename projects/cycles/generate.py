#!/usr/bin/env python3
"""Generate index.html for the Cycles photography project."""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(BASE, "photos-web")
OUTPUT_FILE = os.path.join(BASE, "index.html")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

STATEMENT = (
    "Nothing is new under the sun. History repeats itself in mysterious cycles.<br>"
    "From everyday repeating objects to relationship cycles — this project discovers<br>"
    "and consolidates the cycles I fantasize."
)

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cycles</title>
  <link rel="stylesheet" href="../../style.css">
  <style>
    .project-header {{
      padding: 48px 48px 36px;
    }}

    .project-title {{
      font-size: 13px;
      font-weight: 400;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: #111;
      margin-bottom: 16px;
    }}

    .statement {{
      font-size: 12px;
      line-height: 1.9;
      color: #888;
      max-width: 520px;
    }}

    main {{
      padding-bottom: 80px;
    }}

    .group {{
      margin-bottom: 60px;
    }}

    .group-label {{
      font-size: 11px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #888;
      padding: 0 48px 12px;
    }}

    .photo-row {{
      display: flex;
      overflow-x: auto;
      height: 60vh;
      gap: 4px;
      padding: 0 48px;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }}

    .photo-row::-webkit-scrollbar {{
      display: none;
    }}

    .photo-row img {{
      height: 100%;
      width: auto;
      display: block;
      flex-shrink: 0;
      object-fit: cover;
    }}
  </style>
</head>
<body>
  <nav>
    <a href="../../index.html" class="site-name">Jun</a>
    <div class="nav-links">
      <a href="../../index.html">Work</a>
      <a href="../../info.html">Info</a>
    </div>
  </nav>
  <div class="project-header">
    <p class="project-title">Cycles</p>
    <p class="statement">{statement}</p>
  </div>
  <main>
{groups}
  </main>
</body>
</html>
"""

GROUP_TEMPLATE = """\
    <section class="group">
      <p class="group-label">{label}</p>
      <div class="photo-row">
{images}
      </div>
    </section>"""

IMAGE_TEMPLATE = '        <img src="{src}" alt="{alt}" loading="lazy">'


def format_label(folder_name):
    name = re.sub(r"[-_]", " ", folder_name)
    return name.title()


def get_images(folder_path):
    files = []
    for f in os.listdir(folder_path):
        ext = os.path.splitext(f)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            files.append(f)
    return sorted(files)


def build_groups():
    groups = []
    try:
        subdirs = sorted(
            d for d in os.listdir(PHOTOS_DIR)
            if os.path.isdir(os.path.join(PHOTOS_DIR, d))
        )
    except FileNotFoundError:
        print(f"Error: '{PHOTOS_DIR}' directory not found.")
        return []

    for subdir in subdirs:
        folder_path = os.path.join(PHOTOS_DIR, subdir)
        images = get_images(folder_path)
        if not images:
            continue

        label = format_label(subdir)
        image_lines = []
        for img in images:
            src = f"photos-web/{subdir}/{img}"
            alt = os.path.splitext(img)[0]
            image_lines.append(IMAGE_TEMPLATE.format(src=src, alt=alt))

        groups.append(GROUP_TEMPLATE.format(
            label=label,
            images="\n".join(image_lines),
        ))

    return groups


def main():
    groups = build_groups()
    if not groups:
        print("No photo groups found. Nothing to generate.")
        return

    html = HTML_TEMPLATE.format(
        statement=STATEMENT,
        groups="\n".join(groups),
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE} with {len(groups)} group(s).")


if __name__ == "__main__":
    main()
