"""Draw the measured text boxes onto in-game screenshots (work/ui/screens_<version>/).

Usage:
  python tools/label_screens.py [work/ui/screens_0.2.0]

Reads screens.json in that folder: {"<png>": [{"type": ..., "box": [x, y, w, h], "label": ...}]}
with boxes in native 480x272 px, and writes <name>_labelled.png next to each screenshot.
"""
import json
import os
import sys

from PIL import Image, ImageDraw

COLORS = {"limit": (255, 60, 60), "screen": (255, 200, 0), "slot": (80, 200, 255)}


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else os.path.join("work", "ui", "screens_0.2.0")
    spec = json.load(open(os.path.join(folder, "screens.json"), encoding="utf-8"))
    for name, boxes in spec["screens"].items():
        im = Image.open(os.path.join(folder, name)).convert("RGB")
        k = im.width / 480
        d = ImageDraw.Draw(im)
        for b in boxes:
            x, y, w, h = b["box"]
            c = COLORS.get(b.get("kind", "limit"), (255, 60, 60))
            d.rectangle([x * k, y * k, (x + w) * k - 1, (y + h) * k - 1], outline=c, width=2)
            ty = y * k - 14 if y * k >= 16 else (y + h) * k + 2
            d.rectangle([x * k, ty, x * k + 7 * len(b["label"]) + 4, ty + 13], fill=(0, 0, 0))
            d.text((x * k + 2, ty), b["label"], fill=c)
        out = os.path.join(folder, name[:-4] + "_labelled.png")
        im.save(out)
        print("wrote", out)


if __name__ == "__main__":
    main()
