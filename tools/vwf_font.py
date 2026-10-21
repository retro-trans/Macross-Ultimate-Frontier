"""Variable-width English glyphs for the 14 px game font (gpsp3_font14.fnt).

Glyphs are drawn at 4x (a 56x56 px cell) from an outline font, then
box-filtered down to the game's 14x14 cell and quantised to its four alpha
levels (2 bpp). Every glyph's pen sits LEFT = 1 px into its cell (placement()); the
patched printer advances by the true, fractional advance and draws each glyph at
its exact sub-pixel position. At 14 px a quarter pixel either way is allowed for
the sharpest result; the 4x glyph uses the exact position.

Font file layout (see docs/vwf.md): a 448 px wide 4 bpp atlas, 32 cells of
14x14 per row. Every nibble holds two 2 bpp glyphs: bits 0-1 = even glyph
number, bits 2-3 = odd glyph number; cell = glyph >> 1.

Usage (normally called from tools/vwf_build.py):
  python tools/vwf_font.py --preview out.png
"""

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

CELL = 14
SCALE = 4
BIG = CELL * SCALE
ATLAS_W = 448
FIRST, LAST = 0x20, 0x7F  # ASCII range covered by the width table (96 codes)
# alpha of the four 2 bpp levels, from the font descriptor in the EBOOT
LEVELS = np.array([0x00, 0x5C, 0xC2, 0xFE]) / 255.0

DEFAULT_FONT = r"C:\Windows\Fonts\NotoSansJP-VF.ttf"  # SIL Open Font License 1.1
DEFAULT_WEIGHT = 600
CAP_TOP = 1       # first row of capitals (game full-width Latin: row 1)
BASELINE = 11     # first row below the baseline -> caps occupy rows 1..10
SPACE_ADVANCE = 4
# The menu CSVs have no quoting, so a cell cannot hold an ASCII comma or double
# quote. No game string uses '|' or '`' (docs/vwf.md), so their slots draw a
# comma and a double quote instead; tools/insert_text.py writes them in CSVs.
ALIASES = {"|": ",", "`": '"'}


def load_font(path, weight, size, index=0):
    f = ImageFont.truetype(path, size, index=index)
    try:
        axes = f.get_variation_axes()
        f.set_variation_by_axes([weight if a.get("name", b"") in (b"Weight", "Weight") else a["default"]
                                 for a in axes])
    except (OSError, AttributeError):
        pass
    return f


def fit_size(path, weight, index=0):
    """Pick the 4x pixel size whose capital 'H' is (BASELINE-CAP_TOP)*4 tall."""
    want = (BASELINE - CAP_TOP) * SCALE
    best = None
    for size in range(40, 90):
        f = load_font(path, weight, size, index)
        top, bottom = f.getbbox("H", anchor="ls")[1], f.getbbox("H", anchor="ls")[3]
        h = bottom - top
        if best is None or abs(h - want) < abs(best[1] - want):
            best = (size, h)
    return best[0]


PAD = 2  # px of room left of the pen, for glyphs with a negative left bearing


def render_char(font, ch, phase):
    """Coverage of `ch` at 4x with the pen at x = PAD*4 + phase, baseline fixed."""
    img = Image.new("L", (BIG + 16 + PAD * SCALE, BIG), 0)
    d = ImageDraw.Draw(img)
    d.text((PAD * SCALE + phase, BASELINE * SCALE), ch, font=font, fill=255, anchor="ls")
    return np.asarray(img, dtype=np.float64) / 255.0


def downsample(cov):
    h, w = cov.shape
    w4 = w // SCALE * SCALE
    return cov[:, :w4].reshape(h // SCALE, SCALE, w4 // SCALE, SCALE).mean(axis=(1, 3))


def quantise(a):
    # nearest alpha level, with a slight boost so 1 px strokes keep full weight
    a = np.clip(a * 1.15, 0, 1)
    return np.abs(a[..., None] - LEVELS[None, None, :]).argmin(axis=-1).astype(np.uint8)


LEFT = 1  # px between the pen and the glyph's origin in every cell (room for j's overhang)


def placement(font, ch):
    """Integer advance, true advance (px) and the pen position inside the cell (4x px).

    Every glyph's pen sits LEFT px into its cell. The patched printer advances by
    the true (fractional) advance and draws each glyph at its exact sub-pixel
    position (docs/vwf.md), so the glyph needs no rounding shift. The integer
    advance is still used by the string-width, truncation and glyph-array code."""
    a4 = font.getlength(ch)
    advance = max(1, min(CELL, int(round(a4 / SCALE))))
    return advance, a4 / SCALE, LEFT * SCALE


def cell_cov(font, ch, pen4):
    """4x coverage of `ch` with its pen at x = pen4 (4x px) from the cell's left edge."""
    cov = render_char(font, ch, pen4 % SCALE)
    start = (PAD - pen4 // SCALE) * SCALE   # render column that becomes the cell's column 0
    return cov[:, start:start + BIG]


def build_glyph(font, ch, with_pos=False):
    """Return (2 bpp 14x14 array, advance in px[, pen position in 4x px])."""
    if ch == " ":
        z = np.zeros((CELL, CELL), np.uint8)
        return (z, SPACE_ADVANCE, LEFT * SCALE) if with_pos else (z, SPACE_ADVANCE)
    advance, _, pen4 = placement(font, ch)
    best = None
    # at 1x the ink snaps to whole pixels anyway: allow a quarter pixel either way
    # for the sharpest result (the spacing error stays under a quarter pixel)
    for p4 in (pen4, pen4 - 1, pen4 + 1):
        q = quantise(downsample(cell_cov(font, ch, p4)))
        a = LEVELS[q]
        score = (a * a).sum() / max(a.sum(), 1e-6) - (0.002 if p4 != pen4 else 0)
        if best is None or score > best[0]:
            best = (score, q)
    q = best[1]
    cols = np.where(q.max(axis=0) > 0)[0]
    if cols.size and cols.max() + 1 > CELL:
        print("warning: %r is %d px wide, clipped to %d" % (ch, cols.max() + 1, CELL), file=sys.stderr)
    out = np.zeros((CELL, CELL), np.uint8)
    out[:, :min(CELL, q.shape[1])] = q[:, :CELL]
    return (out, advance, pen4) if with_pos else (out, advance)


def build_hd_glyph(font, ch, pen4):
    """The same glyph at 4x (a 56x56 2 bpp cell), at its exact pen position."""
    if ch == " ":
        return np.zeros((BIG, BIG), np.uint8)
    cov = cell_cov(font, ch, pen4)
    out = np.zeros((BIG, BIG), np.uint8)
    q = np.abs(cov[..., None] - LEVELS[None, None, :]).argmin(axis=-1).astype(np.uint8)
    out[:, :q.shape[1]] = q
    return out


def build_set(path=DEFAULT_FONT, weight=DEFAULT_WEIGHT, index=0, hd=False):
    """Glyphs and advances for ASCII 0x20-0x7F. With hd=True also the 4x cells."""
    size = fit_size(path, weight, index)
    font = load_font(path, weight, size, index)
    glyphs, widths, hd_glyphs, true_adv = [], [], [], []
    for c in range(FIRST, LAST + 1):
        ch = chr(c) if c < 0x7F else "\u2026"  # 0x7F (DEL) slot holds an ellipsis
        ch = ALIASES.get(ch, ch)
        g, w, pen4 = build_glyph(font, ch, with_pos=True)
        glyphs.append(g)
        widths.append(w)
        true_adv.append(float(SPACE_ADVANCE) if ch == " " else placement(font, ch)[1])
        if hd:
            hd_glyphs.append(build_hd_glyph(font, ch, pen4))
    info = {"font": os.path.basename(path), "index": index, "weight": weight, "size_4x": size,
            "true_advance": true_adv}
    return (glyphs, widths, info, hd_glyphs) if hd else (glyphs, widths, info)


# ------------------------------------------------------------- 4x page

HD_PER_ROW = ATLAS_W // BIG   # 8 cells of 56 px in a 448 px row
HD_ROWS_PX = 512              # the page is bound as a 512x512 texture (bufw 448)


def hd_page(hd_glyphs):
    """4 bpp page with the main atlas's two-layer packing: local glyph L sits in
    cell L >> 1, in bits 0-1 for even L and bits 2-3 for odd L."""
    img = np.zeros((HD_ROWS_PX, ATLAS_W), np.uint8)
    for L, g in enumerate(hd_glyphs):
        r, c = divmod(L >> 1, HD_PER_ROW)
        ys, xs = slice(r * BIG, r * BIG + BIG), slice(c * BIG, c * BIG + BIG)
        img[ys, xs] |= (g << 2) if L & 1 else g
    return write_atlas(img)


def hd_preview(path, hd_glyphs, widths, samples):
    """Sample lines drawn from the 4x cells at 4x advances (what PPSSPP shows at 4x)."""
    rows = []
    for s in samples:
        total = sum(widths[ord(c) - FIRST] for c in s) * SCALE
        canvas = np.zeros((BIG, total + BIG), np.float64)
        x = 0
        for c in s:
            a = LEVELS[hd_glyphs[ord(c) - FIRST]]
            canvas[:, x:x + BIG] = np.maximum(canvas[:, x:x + BIG], a)
            x += widths[ord(c) - FIRST] * SCALE
        rows.append(canvas[:, :x])
    w = max(r.shape[1] for r in rows) + 32
    img = np.zeros((len(rows) * (BIG + 16) + 16, w, 3), np.float64)
    img[:] = (0.10, 0.14, 0.22)
    for i, r in enumerate(rows):
        y = 16 + i * (BIG + 16)
        a = r[:, :, None]
        img[y:y + BIG, 16:16 + r.shape[1]] = img[y:y + BIG, 16:16 + r.shape[1]] * (1 - a) + a
    Image.fromarray((img * 255).astype(np.uint8)).save(path)


# ------------------------------------------------------------- atlas access

def read_atlas(data):
    d = np.frombuffer(data, np.uint8)
    px = np.empty(d.size * 2, np.uint8)
    px[0::2] = d & 15
    px[1::2] = d >> 4
    return px.reshape(-1, ATLAS_W)


def write_atlas(img):
    px = img.reshape(-1)
    return ((px[1::2] << 4) | px[0::2]).astype(np.uint8).tobytes()


def cell_slice(g):
    cell = g >> 1
    r, c = divmod(cell, ATLAS_W // CELL)
    return slice(r * CELL, r * CELL + CELL), slice(c * CELL, c * CELL + CELL)


def get_glyph(img, g):
    ys, xs = cell_slice(g)
    sub = img[ys, xs]
    return (sub >> 2) & 3 if g & 1 else sub & 3


def put_glyph(img, g, a):
    ys, xs = cell_slice(g)
    sub = img[ys, xs]
    if g & 1:
        img[ys, xs] = (sub & 3) | (a << 2)
    else:
        img[ys, xs] = (sub & 12) | a


# ------------------------------------------------------------- preview

def render_line(text, glyphs, widths, other=None):
    """Lay out `text` like the patched game: advance = width table."""
    x = 0
    total = sum(widths[ord(c) - FIRST] for c in text)
    canvas = np.zeros((CELL, total + CELL), np.float64)
    for c in text:
        g = glyphs[ord(c) - FIRST]
        a = LEVELS[g]
        canvas[:, x:x + CELL] = np.maximum(canvas[:, x:x + CELL], a)
        x += widths[ord(c) - FIRST]
    return canvas[:, :x]


def preview(path, glyphs, widths, samples, zoom=3):
    rows = []
    for s in samples:
        line = render_line(s, glyphs, widths)
        rows.append(line)
    w = max(r.shape[1] for r in rows) + 8
    img = np.zeros((len(rows) * (CELL + 4) + 4, w, 3), np.float64)
    img[:] = (0.10, 0.14, 0.22)  # dark blue, like the game's windows
    for i, r in enumerate(rows):
        y = 4 + i * (CELL + 4)
        a = r[:, :, None]
        img[y:y + CELL, 4:4 + r.shape[1]] = img[y:y + CELL, 4:4 + r.shape[1]] * (1 - a) + a
    out = Image.fromarray((img * 255).astype(np.uint8))
    out.resize((out.width * zoom, out.height * zoom), Image.NEAREST).save(path)


SAMPLES = [
    "The quick brown fox jumps over the lazy dog.",
    "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!",
    "Hikaru Ichijo, Roy Focker, Max & Milia Jenius",
    "VF-1J Valkyrie (Hikaru)  VF-25F Messiah (Alto)",
    "Destroy the enemy forces. Time: 03:45 / 100%",
    "\"Don't you know? Ranka Lee's song's coming!\"",
    "0123456789 +-*/=<>?@#$%^_[]{}|~`;:,.'\u2026",
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", default=DEFAULT_FONT)
    ap.add_argument("--weight", type=int, default=DEFAULT_WEIGHT)
    ap.add_argument("--index", type=int, default=0, help="face index in a .ttc collection")
    ap.add_argument("--preview", help="write a preview PNG")
    ap.add_argument("--hd-preview", help="write a preview PNG of the 4x cells")
    ap.add_argument("--json", help="write the width table as JSON")
    args = ap.parse_args()
    glyphs, widths, info, hd = build_set(args.font, args.weight, args.index, hd=True)
    print(info, "widths:", widths)
    samples = [s.replace("\u2026", chr(0x7F)) for s in SAMPLES]
    if args.preview:
        preview(args.preview, glyphs, widths, samples)
    if args.hd_preview:
        hd_preview(args.hd_preview, hd, widths, samples)
    if args.json:
        json.dump({"info": info, "widths": widths}, open(args.json, "w"), indent=1)


if __name__ == "__main__":
    main()
