"""Redraw the Japanese text in game textures in English (docs/image_redraw.md).

Usage:
  python tools/redraw_images.py [--out <overlay>] [--preview <dir>] [--only <substr>] [--no-sheets]
                                [--version <0.x.y>]

Inputs:
  work/translation/en/images/img_{menu_a,menu_b,script,art}.json   rows: file, size, en, style, notes
  work/ui/redraw_layout.json   where each text goes and how it is drawn (styles + per-texture items)
  work/source/dat/<file>       original GIM textures

Outputs:
  <overlay>/data/...gim        re-encoded textures (default work/output/redraw/overlay), for
                               muf_archive.py repack --overlay
  <preview>/                   before/after contact sheets + report.json (default work/ui/redraw_preview)

img_logos.json is never read: official series logos are kept (decision 2026-10-15).

Per texture, every item first erases its box (erase mode), then every item draws its
text. Text is drawn 4x supersampled from Noto Sans JP / Noto Serif JP (SIL OFL 1.1),
fitted to the box (see fit(): a small shrink, then a light squeeze, then the short
forms from the row notes, then a hard squeeze), and the result is quantized back to
the texture's own palette size by tools/gim.py. Tip cards are typeset as a whole
(tipcard()); gallery thumbnails are shrunk from the redrawn stills.
Specs with "keep" are left as they are; specs with "hold" get a preview only.
An item's own "text" may contain {version}, filled from --version (build_iso.py passes the
build version): the title screen shows the build version and the group name this way.
"""
import argparse
import fnmatch
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gim  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = ["menu_a", "menu_b", "script", "art"]
FONTS = {  # SIL Open Font License 1.1
    "sans": r"C:\Windows\Fonts\NotoSansJP-VF.ttf",
    "serif": r"C:\Windows\Fonts\NotoSerifJP-VF.ttf",
}
SS = 4  # supersampling factor
VERSION = "dev"  # --version, for {version} in an item's "text"

DEFAULT_STYLE = {
    "font": "sans", "weight": 700, "size": 13, "min_size": 8, "xscale_min": 0.72, "tracking": 0,
    "color": [255, 255, 255, 255], "gradient": None, "outline": None, "glow": None, "shadow": None,
    "italic": 0.0, "align": "center", "valign": "center", "line_gap": 1.15, "caps": False,
    "wrap": False, "max_lines": 1, "dx": 0, "dy": 0, "ss": SS, "bold_px": 0, "opacity": 1.0,
    "line_px": None, "shrink_first": 0.86, "soft_xscale": 0.84,
}

_font_cache = {}


def font(name, size, weight):
    key = (name, size, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(FONTS.get(name, name), size)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]


# ---------------------------------------------------------------- rows / layout

def load_rows():
    by_file = {}
    for g in GROUPS:
        d = json.load(open(os.path.join(ROOT, "work/translation/en/images/img_%s.json" % g), encoding="utf-8"))
        for i, r in enumerate(d.get("rows", [])):
            r = dict(r, group=g, index=i)
            by_file.setdefault(r["file"], []).append(r)
    return by_file


def load_layout(path):
    return json.load(open(path, encoding="utf-8"))


def items_for(layout, path, rows):
    """The item list for one texture: the first matching rule, overridden by the
    per-file entry (its "set" keys are merged into the rule's)."""
    spec = None
    for rule in layout.get("rules", []):
        pats = rule["match"] if isinstance(rule["match"], list) else [rule["match"]]
        if any(fnmatch.fnmatch(path, p) for p in pats):
            spec = dict(rule)
            break
    own = layout.get("files", {}).get(path)
    if own is not None:
        spec = dict(spec or {})
        merged = dict(spec.get("set", {}))
        merged.update(own.get("set", {}))
        spec.update(own)
        spec["set"] = merged
    if spec is None:
        return None, {}
    items = spec.get("items") or [{}]
    return items, spec


def style_of(layout, item, spec, row=None):
    st = dict(DEFAULT_STYLE)
    names = []
    for src in (spec, item):
        if "style" in src:
            names += src["style"] if isinstance(src["style"], list) else [src["style"]]
    # "style_by_row": {"red": "rat_red", ...} picks a preset from the row's style words
    for word, name in spec.get("style_by_row", {}).items():
        if row is not None and row["style"].lower().startswith(word):
            names.append(name)
            break
    for n in names:
        st.update(layout["styles"][n])
    for src in (spec.get("set", {}), item):
        for k, v in src.items():
            if k in DEFAULT_STYLE:
                st[k] = v
    return st


# ---------------------------------------------------------------- erasing

def rgba(a):
    return np.asarray(a, np.float32)


def erase(arr, box, mode, opt):
    """arr: float32 HxWx4 (straight alpha). Erase box in place."""
    H, W = arr.shape[:2]
    x, y, w, h = box
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    if mode == "keep":
        return
    if mode == "clear":
        arr[y0:y1, x0:x1] = 0
    elif mode == "fill":
        arr[y0:y1, x0:x1] = rgba(opt["color"])
    elif mode in ("plate", "vplate"):
        # linear interpolation across the box from the pixels just outside it
        if mode == "plate":
            a = arr[y0:y1, x0 - 1] if x0 > 0 else None
            b = arr[y0:y1, x1] if x1 < W else None
            a = b if a is None else a
            b = a if b is None else b
            t = (np.arange(x1 - x0, dtype=np.float32) + 1) / (x1 - x0 + 1)
            arr[y0:y1, x0:x1] = a[:, None] * (1 - t)[None, :, None] + b[:, None] * t[None, :, None]
        else:
            a = arr[y0 - 1, x0:x1] if y0 > 0 else None
            b = arr[y1, x0:x1] if y1 < H else None
            a = b if a is None else a
            b = a if b is None else b
            t = (np.arange(y1 - y0, dtype=np.float32) + 1) / (y1 - y0 + 1)
            arr[y0:y1, x0:x1] = a[None] * (1 - t)[:, None, None] + b[None] * t[:, None, None]
    elif mode == "row":
        # every row takes the colour of a sample column (for plates with a vertical gradient)
        sx = opt.get("sample_x", x0 - 1 if x0 > 0 else x1)
        arr[y0:y1, x0:x1] = arr[y0:y1, sx][:, None]
    elif mode == "col":
        sy = opt.get("sample_y", y0 - 1 if y0 > 0 else y1)
        arr[y0:y1, x0:x1] = arr[sy, x0:x1][None]
    elif mode == "copy":
        sx, sy = opt["from"]
        arr[y0:y1, x0:x1] = arr[sy + (y0 - y):sy + (y1 - y), sx + (x0 - x):sx + (x1 - x)].copy()
    elif mode == "inpaint":
        mask = np.zeros((H, W), bool)
        mask[y0:y1, x0:x1] = True
        if "color" in opt:  # only pixels near the text colour (plus a margin)
            c = rgba(opt["color"])[:3]
            near = (np.abs(arr[:, :, :3] - c).max(2) <= opt.get("tol", 60)) & (arr[:, :, 3] > 0)
            m2 = np.zeros((H, W), bool)
            m2[y0:y1, x0:x1] = near[y0:y1, x0:x1]
            g = opt.get("grow", 1)
            if g:
                m2 = np.asarray(Image.fromarray(m2.astype(np.uint8) * 255).filter(
                    ImageFilter.MaxFilter(2 * g + 1))) > 0
            mask = m2 & mask
        inpaint(arr, mask, opt.get("iters", 0))
    elif mode == "frost":
        r = opt.get("blur", 6)
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
        bl = np.asarray(im.filter(ImageFilter.GaussianBlur(r)), np.float32)
        dark = opt.get("dark", 0.5)
        tint = rgba(opt.get("tint", [0, 0, 0]))[:3]
        feather = opt.get("feather", 6)
        m = np.zeros((H, W), np.float32)
        m[y0:y1, x0:x1] = 1
        if feather:
            m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(feather)), np.float32) / 255
            m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], opt.get("core", 0.0))
        out = bl.copy()
        out[:, :, :3] = bl[:, :, :3] * (1 - dark) + tint * dark
        arr[:] = arr * (1 - m[:, :, None]) + out * m[:, :, None]
    else:
        raise ValueError("unknown erase mode " + mode)


def inpaint(arr, mask, iters=0):
    """Fill masked pixels from their unmasked neighbours (onion-peel diffusion)."""
    H, W = mask.shape
    known = ~mask
    a = arr.copy()
    a[mask] = 0
    rem = mask.copy()
    k = 0
    while rem.any():
        acc = np.zeros_like(a)
        cnt = np.zeros((H, W), np.float32)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            sk = np.zeros((H, W), bool)
            sa = np.zeros_like(a)
            ys = slice(max(0, dy), H + min(0, dy))
            yd = slice(max(0, -dy), H + min(0, -dy))
            xs = slice(max(0, dx), W + min(0, dx))
            xd = slice(max(0, -dx), W + min(0, -dx))
            sk[yd, xd] = known[ys, xs]
            sa[yd, xd] = a[ys, xs]
            acc += sa * sk[:, :, None]
            cnt += sk
        new = rem & (cnt > 0)
        if not new.any():
            break
        a[new] = acc[new] / cnt[new][:, None]
        known = known | new
        rem = rem & ~new
        k += 1
    for _ in range(iters):  # smooth the filled area
        b = a.copy()
        b[1:-1, 1:-1] = (a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:]) / 4
        a[mask] = b[mask]
    arr[mask] = a[mask]


# ---------------------------------------------------------------- text

def measure(text, st, size):
    f = font(st["font"], size * st["ss"], st["weight"])
    w = f.getlength(text) + st["tracking"] * st["ss"] * max(0, len(text) - 1)
    return w / st["ss"]


def fit(texts, box, st):
    """Pick text, lines, size and xscale: (lines, size, xscale, overflow, text index).

    Two passes, each over every candidate text in order (the translation, then its
    fallbacks): 1) shrink the font a little (to shrink_first x size) without
    squeezing, then squeeze lightly (down to soft_xscale) at any size down to
    min_size; 2) squeeze hard (down to xscale_min). So a short form is preferred
    to a hard squeeze, and the full text to a short form when it fits pass 1."""
    bw, bh = box[2], box[3]
    floor = max(st["min_size"], int(st["size"] * st["shrink_first"] + 0.999))
    soft = max(st["xscale_min"], st["soft_xscale"])
    passes = [[(s, 1.0) for s in range(st["size"], floor - 1, -1)] +
              [(s, soft) for s in range(st["size"], st["min_size"] - 1, -1)],
              [(s, st["xscale_min"]) for s in range(st["size"], st["min_size"] - 1, -1)]]
    cands = []
    for text in texts:
        if st["caps"]:
            text = text.upper()
        variants = [text.split("\n")]
        if st["wrap"] and "\n" not in text:
            words = text.split(" ")
            for k in range(1, len(words)):
                variants.append([" ".join(words[:k]), " ".join(words[k:])])
        cands.append((text, variants))
    for plan in passes:
        for ti, (text, variants) in enumerate(cands):
            for size, squeeze in plan:
                for lines in variants:
                    if len(lines) > max(st["max_lines"], len(text.split("\n"))):
                        continue
                    lh = st["line_px"] or size * st["line_gap"]
                    if size * 0.75 + lh * (len(lines) - 1) > bh + 2 and len(lines) > 1:
                        continue
                    w = max(measure(l, st, size) for l in lines) + abs(st["italic"]) * size
                    if w <= bw:
                        return lines, size, 1.0, False, ti
                    if squeeze < 1 and w * squeeze <= bw:
                        return lines, size, bw / w, False, ti
    lines = cands[-1][1][0]
    size = st["min_size"]
    w = max(measure(l, st, size) for l in lines)
    return lines, size, max(bw / w, 0.3), True, len(texts) - 1


def mask_layer(img, r, kind):
    if r <= 0:
        return img
    if kind == "max":
        n = int(round(r)) * 2 + 1
        return img.filter(ImageFilter.MaxFilter(n))
    return img.filter(ImageFilter.GaussianBlur(r))


def draw_text(arr, box, lines, size, xscale, st):
    """Composite the text into arr (float32 RGBA) inside box."""
    ss = st["ss"]
    x, y, bw, bh = box
    pad = 2 + int(max((st["outline"] or {}).get("width", 0), (st["glow"] or {}).get("radius", 0) * 2,
                      abs((st["shadow"] or {}).get("dx", 0)) + abs((st["shadow"] or {}).get("dy", 0))) + 1)
    cw, ch = bw + 2 * pad, bh + 2 * pad
    # supersampled canvas, horizontally pre-stretched by 1/xscale
    sw, sh = int(round(cw * ss / xscale)), ch * ss
    m = Image.new("L", (sw, sh), 0)
    d = ImageDraw.Draw(m)
    f = font(st["font"], size * ss, st["weight"])
    cap_top, cap_bot = f.getbbox("H")[1], f.getbbox("H")[3]
    cap = cap_bot - cap_top
    lh = (st["line_px"] or size * st["line_gap"]) * ss
    total = cap + lh * (len(lines) - 1)
    if st["valign"] == "top":
        top = pad * ss
    elif st["valign"] == "bottom":
        top = (pad + bh) * ss - total
    else:
        top = (pad * ss + (bh * ss - total) / 2)
    top += st["dy"] * ss
    for i, line in enumerate(lines):
        lw = (f.getlength(line) + st["tracking"] * ss * max(0, len(line) - 1))
        inner = bw * ss / xscale
        if st["align"] == "left":
            lx = 0
        elif st["align"] == "right":
            lx = inner - lw
        else:
            lx = (inner - lw) / 2
        lx += pad * ss / xscale + st["dx"] * ss / xscale
        ly = top + i * lh - cap_top
        if st["tracking"]:
            cx = lx
            for ch_ in line:
                d.text((cx, ly), ch_, font=f, fill=255)
                cx += f.getlength(ch_) + st["tracking"] * ss
        else:
            d.text((lx, ly), line, font=f, fill=255)
    if st["bold_px"]:
        m = mask_layer(m, st["bold_px"] * ss / 2, "max")
    if st["italic"]:
        sh_ = st["italic"]
        m = m.transform(m.size, Image.AFFINE, (1, sh_, -sh_ * sh / 2, 0, 1, 0), Image.BICUBIC)
    layers = []  # (mask at 1x, colour or gradient)

    def down(img):
        return np.asarray(img.resize((cw, ch), Image.BOX), np.float32) / 255

    fill = down(m)
    if st["glow"]:
        g = st["glow"]
        gm = mask_layer(m, g.get("spread", 0) * ss, "max") if g.get("spread") else m
        gm = down(gm.filter(ImageFilter.GaussianBlur(g["radius"] * ss)))
        layers.append((np.clip(gm * g.get("strength", 1.5), 0, 1), g["color"]))
    if st["shadow"]:
        s = st["shadow"]
        sm = Image.new("L", m.size, 0)
        sm.paste(mask_layer(m, s.get("width", 0) * ss, "max"), (int(s.get("dx", 1) * ss / xscale), int(s.get("dy", 1) * ss)))
        if s.get("blur"):
            sm = sm.filter(ImageFilter.GaussianBlur(s["blur"] * ss))
        layers.append((down(sm), s["color"]))
    if st["outline"]:
        o = st["outline"]
        om = mask_layer(m, o["width"] * ss, "max")
        if o.get("blur"):
            om = om.filter(ImageFilter.GaussianBlur(o["blur"] * ss))
        layers.append((down(om), o["color"]))
    if st["gradient"]:
        g0, g1 = rgba(st["gradient"][0]), rgba(st["gradient"][1])
        yy = (np.arange(ch, dtype=np.float32) - pad) / max(1, bh - 1)
        # gradient runs over the text's cap height, not the whole box
        t0 = (top / ss - pad) / bh
        t1 = (top + total) / ss / bh - pad / bh
        t = np.clip((yy - t0) / max(1e-3, t1 - t0), 0, 1)
        col = g0[None, :] * (1 - t)[:, None] + g1[None, :] * t[:, None]
        layers.append((fill, col[:, None, :] * np.ones((1, cw, 1), np.float32)))
    else:
        layers.append((fill, st["color"]))
    H, W = arr.shape[:2]
    X0, Y0 = x - pad, y - pad
    sx0, sy0 = max(0, -X0), max(0, -Y0)
    sx1, sy1 = min(cw, W - X0), min(ch, H - Y0)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    dst = arr[Y0 + sy0:Y0 + sy1, X0 + sx0:X0 + sx1]
    clip = st.get("clip")
    for a, col in layers:
        a = a[sy0:sy1, sx0:sx1] * st["opacity"]
        col = rgba(col)
        if col.ndim == 3:
            col = col[sy0:sy1, sx0:sx1]
            ca = a * col[:, :, 3] / 255
            crgb = col[:, :, :3]
        else:
            ca = a * col[3] / 255
            crgb = col[None, None, :3]
        da = dst[:, :, 3] / 255
        oa = ca + da * (1 - ca)
        with np.errstate(invalid="ignore", divide="ignore"):
            rgb = (crgb * ca[:, :, None] + dst[:, :, :3] * (da * (1 - ca))[:, :, None]) / oa[:, :, None]
        rgb = np.where(oa[:, :, None] > 0, rgb, dst[:, :, :3])
        dst[:, :, :3] = rgb
        dst[:, :, 3] = oa * 255
    if clip:  # keep the drawing inside the box
        pass


# ---------------------------------------------------------------- per texture

def text_for(item, rows, spec=None):
    """Candidate texts: the translation (or the item's "text"), then its fallbacks.
    "prefer_replace": [[old, new], ...] on the spec puts a spelled-out form first
    (row notes such as "spell out 'Forward' if it fits")."""
    r = rows[item.get("row", 0)]
    if "text" in item:
        t = item["text"].replace("{version}", VERSION)
    else:
        t = r["en"]
        if "line" in item:
            t = t.split("\n")[item["line"]]
    out = [t] + list(item.get("fallbacks", []))
    pref = t
    for a, b in (spec or {}).get("prefer_replace", []):
        pref = pref.replace(a, b)
    return ([pref] if pref != t else []) + out


def share_choices(layout, by_file):
    """For items with the same "share" key, the first candidate text that fits all of them."""
    need = {}
    for path, rows in by_file.items():
        items, spec = items_for(layout, path, rows)
        for it in items or []:
            grp = it.get("share")
            if not grp:
                continue
            W, H = rows[0]["size"]
            st = style_of(layout, it, spec, rows[it.get("row", 0)])
            box = it.get("box", spec.get("box", [0, 0, W, H]))
            need[grp] = max(need.get(grp, 0), fit(text_for(it, rows, spec), box, st)[4])
    choice = dict(layout.get("shared_text", {}))
    choice.update(need)
    return choice


def tipcard(arr, rows, it, layout, spec):
    """Loading-screen tip card: typeset the whole message into the right-hand panel.

    The old strokes (bright pixels inside the area) are inpainted, then a soft dark,
    slightly blurred shade is laid under both the old and the new lines so no trace of
    the Japanese glow shows, and the English is drawn with the same white + blue glow.
    Line roles: line 0 speaker, next title_lines lines the title, the last sig lines
    the sign-off (right-aligned); headings (lines starting with a box or bullet glyph)
    are outdented, "- " lines are bullets, other body lines are continuation lines."""
    H, W = arr.shape[:2]
    st = style_of(layout, it, spec, rows[0])
    x0, y0, x1, y1 = it["area"]
    lines = rows[it.get("row", 0)]["en"].split("\n")
    tl, sig = it.get("title_lines", 1), it.get("sig", 1)
    speaker, title, body, sign = lines[0], lines[1:1 + tl], lines[1 + tl:len(lines) - sig], lines[len(lines) - sig:]
    heads = tuple(it.get("heads", "■●"))
    indent = it.get("indent", 9)

    def ind(k):
        t = body[k]
        if t.startswith(heads) or t.startswith("★"):
            return 0
        if t.startswith("- "):
            return 4
        return 4 + indent

    colon = it.get("colon_x")
    body_top = y0 + it.get("body_top", 34 + 13 * (tl - 1))
    body_bot = y1 - 15 * sig - 2
    chosen = None
    for size in range(st["size"], st["min_size"] - 1, -1):
        pitch = min(it.get("pitch_max", size + 3), (body_bot - body_top) / max(1, len(body)))
        if pitch < size * 1.12:
            continue
        ok = True
        for k, t in enumerate(body):
            avail = (x1 - x0) - ind(k)
            if colon and ":" in t:
                key, val = t.split(":", 1)
                if measure(key + ":", st, size) * st["xscale_min"] > colon - x0 or measure(val, st, size) * st["xscale_min"] > x1 - colon - 2:
                    ok = False
            elif measure(t, st, size) * st["xscale_min"] > avail:
                ok = False
        if ok:
            chosen = (size, pitch)
            break
    if chosen is None:
        size = st["min_size"]
        chosen = (size, (body_bot - body_top) / max(1, len(body)))
    size, pitch = chosen
    # spread what is left over as paragraph gaps before bullets and headings
    starts = [k for k in range(1, len(body)) if body[k].startswith(heads + ("- ", "★"))]
    spare = (body_bot - body_top) - pitch * len(body)
    gap = min(pitch * 0.7, spare / len(starts)) if starts and spare > 0 else 0
    ys, y = [], body_top
    for k in range(len(body)):
        if k in starts:
            y += gap
        ys.append(y)
        y += pitch
    placed = []  # (text, box, size, extra style)
    placed.append((speaker, [x0 + 4, y0, x1 - x0, size + 2], size - 1, {"align": "left"}))
    for k, t in enumerate(title):
        placed.append((t, [x0, y0 + size + 3 + k * (size + 4), x1 - x0, size + 4], size + 1, {"align": "left" if tl > 1 else "center", "weight": 800}))
    for k, t in enumerate(body):
        y = ys[k]
        if colon and ":" in t:
            key, val = t.split(":", 1)
            placed.append((key + ":", [x0, y, colon - x0, size + 3], size, {"align": "right"}))
            placed.append((val.strip(), [colon + 3, y, x1 - colon - 3, size + 3], size, {"align": "left"}))
        else:
            placed.append((t, [x0 + ind(k), y, x1 - x0 - ind(k), size + 3], size, {"align": "left"}))
    for k, t in enumerate(sign):
        placed.append((t, [x0, y1 - 15 * (sig - k), x1 - x0, size + 3], size, {"align": "right"}))
    # new text on its own layer
    layer = np.zeros_like(arr)
    rep = []
    for t, box, sz, extra in placed:
        s2 = dict(st, **extra)
        lines_, size_, xs, over, _ = fit([t], box, dict(s2, size=sz, min_size=max(6, sz - 2)))
        draw_text(layer, [int(round(v)) for v in box], lines_, size_, xs, s2)
        rep.append({"text": t, "size": size_, "xscale": round(xs, 3), "overflow": over})
    # old strokes: bright pixels in the area
    lum = arr[:, :, :3] @ np.array([0.3, 0.59, 0.11], np.float32)
    core = np.zeros((H, W), bool)
    ax0, ay0, ax1, ay1 = [int(v) for v in it.get("erase_area", it["area"])]
    core[ay0:ay1, ax0:ax1] = lum[ay0:ay1, ax0:ax1] > it.get("bright", 200)
    # only bright pixels next to the blue glow are lettering (not white art)
    glow = (arr[:, :, 2] - arr[:, :, 0] > 50) & (arr[:, :, 2] > 140)
    near = np.asarray(Image.fromarray(glow.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
    core &= near
    cm = Image.fromarray(core.astype(np.uint8) * 255)
    inpaint(arr, np.asarray(cm.filter(ImageFilter.MaxFilter(3))) > 0, 2)
    shade_src = np.maximum(np.asarray(cm, np.float32) / 255, (layer[:, :, 3] > 25).astype(np.float32))
    sm = Image.fromarray((shade_src * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * it.get("shade_grow", 4) + 1))
    sm = np.asarray(sm.filter(ImageFilter.GaussianBlur(it.get("shade_blur", 4))), np.float32) / 255
    sm = np.clip(sm * 1.3, 0, 1) * it.get("shade", 0.62)
    blurred = np.asarray(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").filter(ImageFilter.GaussianBlur(2)), np.float32)
    tint = np.array(it.get("tint", [6, 14, 40]), np.float32)
    arr[:, :, :3] = arr[:, :, :3] * (1 - sm[:, :, None]) + (tint * 0.6 + blurred[:, :, :3] * 0.4) * sm[:, :, None]
    # composite the text layer
    la = layer[:, :, 3:4] / 255
    arr[:, :, :3] = layer[:, :, :3] * la + arr[:, :, :3] * (1 - la)
    return rep


def redraw(path, rows, layout, shared_choice):
    b = open(os.path.join(ROOT, "work/source/dat", path), "rb").read()
    before = gim.decode(b)
    items, spec = items_for(layout, path, rows)
    if items is None:
        return None, before, [{"file": path, "error": "no layout"}]
    if spec.get("keep"):
        return None, before, [{"file": path, "kept": spec["keep"]}]
    arr = np.asarray(before, np.float32).copy()
    W, H = before.size
    report = []
    jobs = []
    for it in items:
        if it.get("keep"):
            report.append({"file": path, "row": "%s:%d" % (rows[it.get("row", 0)]["group"], rows[it.get("row", 0)]["index"]),
                           "kept": it["keep"]})
            continue
        if "area" in it:  # tip card: erases and draws by itself (tipcard)
            continue
        st = style_of(layout, it, spec, rows[it.get("row", 0)])
        box = it.get("box", spec.get("box", [0, 0, W, H]))
        ebox = it.get("erase_box", box)
        emode = it.get("erase", spec.get("erase", "clear"))
        eopt = it.get("erase_opt", spec.get("erase_opt", {}))
        modes = emode if isinstance(emode, list) else [emode]
        for m_ in modes:  # one mode, or a list of modes applied in turn
            mo, op = (m_["mode"], m_) if isinstance(m_, dict) else (m_, eopt)
            for eb in (ebox if ebox and isinstance(ebox[0], list) else [ebox]):
                erase(arr, eb, mo, op)
        if it.get("no_text"):
            continue
        jobs.append((it, st, box))
    for it in items:
        if "area" in it:
            for r in tipcard(arr, rows, it, layout, spec):
                report.append(dict(r, file=path, row="%s:%d" % (rows[0]["group"], rows[0]["index"])))
    for it, st, box in jobs:
        texts = text_for(it, rows, spec)
        grp = it.get("share")
        if grp and grp in shared_choice:
            texts = texts[shared_choice[grp]:] if isinstance(shared_choice[grp], int) else [shared_choice[grp]] + texts
        if texts[0] == "" or it.get("blank"):
            report.append({"file": path, "text": "", "box": box})
            continue
        lines, size, xs, over, _ = fit(texts, box, st)
        if "force_size" in it:
            size = it["force_size"]
        draw_text(arr, box, lines, size, xs, st)
        report.append({"file": path, "row": "%s:%d" % (rows[it.get("row", 0)]["group"], rows[it.get("row", 0)]["index"]),
                       "text": "\n".join(lines), "size": size, "xscale": round(xs, 3), "overflow": over,
                       "box": box, "fallback": "\n".join(lines) != (texts[0].upper() if st["caps"] else texts[0])})
    after = Image.fromarray(np.clip(np.round(arr), 0, 255).astype(np.uint8), "RGBA")
    return after, before, report


def thumbnail(src_im, old):
    """Gallery thumbnail: the whole redrawn 480x272 still shrunk to the thumbnail size
    (the originals are made the same way), keeping the old thumbnail's alpha."""
    th = src_im.convert("RGB").resize(old.size, Image.LANCZOS).convert("RGBA")
    th.putalpha(old.getchannel("A"))
    return th


# ---------------------------------------------------------------- shared text

VARIANTS = [  # (regex on the file name, what the variants are)
    (r"^(.*)_([bw])\.gim$", "_b / _w: black and white copies of one label (cursor on / off)"),
    (r"^(.*)_(on|off)\.gim$", "_on / _off"),
    (r"^(menu_0\d)(_light)?\.gim$", "shop menu item: normal / _light (highlighted)"),
    (r"^con_(font|window)_(\d\d)_?(.*)\.gim$", "control config: con_font (grey) / con_window (white on black) with the same label"),
]


def shared_report(by_file, layout):
    """Which textures carry the same English: variant pairs, identical texts, mission
    title cards, thumbnails. Written to <preview>/shared_text.json."""
    import re
    groups = {}
    for path, rows in by_file.items():
        name = os.path.basename(path)
        for rx, what in VARIANTS:
            m = re.match(rx, name)
            if m:
                key = (what, os.path.dirname(path), m.group(1) if "con_" not in rx else m.group(2) + (m.group(3) or "").replace("_", ""))
                groups.setdefault(key, []).append(path)
                break
    variants = [{"kind": k[0], "files": sorted(v), "en": sorted({by_file[f][0]["en"] for f in v})}
                for k, v in sorted(groups.items()) if len(v) > 1]
    same = {}
    for path, rows in by_file.items():
        for r in rows:
            for t in r["en"].split("\n"):
                same.setdefault(t.strip().lower(), set()).add(path)
    same_text = {t: sorted(v) for t, v in sorted(same.items()) if len(v) > 1 and t}
    titles = {p: r[0]["en"] for p, r in by_file.items() if re.search(r"fesrat_m/.*_title\.gim$", p)}
    dup_titles = {}
    for p, t in titles.items():
        dup_titles.setdefault(t, []).append(p)
    return {
        "variant_pairs": variants,
        "on_off_pairs": [v for v in variants if v["kind"].startswith("_on")],
        "same_english": same_text,
        "mission_title_cards": {"count": len(titles), "same_style": "white heavy gothic, 36 px, dark edge (style 'title')",
                                "repeated_titles": {t: sorted(v) for t, v in dup_titles.items() if len(v) > 1}},
        "thumbnails": layout.get("thumbnails", {}),
    }


# ---------------------------------------------------------------- sheets

def contact_sheets(pairs, out, per=None):
    from PIL import ImageDraw as D
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.startswith("sheet_") and f.endswith(".png"):
            os.remove(os.path.join(out, f))
    W, MAXH = 1000, 1600
    bg = (92, 92, 104, 255)
    sheet, x, y, rowh, n = None, 0, 0, 0, 0
    names = []

    def flush():
        nonlocal sheet, n
        if sheet is not None:
            p = os.path.join(out, "sheet_%03d.png" % n)
            sheet.crop((0, 0, W, y + rowh + 4)).convert("RGB").save(p)
            names.append(p)
            n += 1
        sheet = None

    for label, before, after in pairs:
        big = max(before.width, before.height)
        sc = 1 if before.width > 240 or before.height > 120 else (2 if before.width > 70 or big > 50 else 3)
        if 2 * before.width * sc + 10 > W:
            sc = 1
        bi = before.resize((before.width * sc, before.height * sc), Image.NEAREST)
        ai = after.resize((after.width * sc, after.height * sc), Image.NEAREST)
        side = bi.width * 2 + 6 <= W
        w = (bi.width * 2 + 8 if side else bi.width + 4)
        h = (bi.height if side else bi.height * 2 + 4) + 14
        w = max(w, min(W, 6 * len(label) + 4))
        if sheet is None:
            sheet, x, y, rowh = Image.new("RGBA", (W, MAXH), bg), 0, 0, 0
        if x + w > W:
            x, y, rowh = 0, y + rowh + 4, 0
        if y + h > MAXH:
            flush()
            sheet, x, y, rowh = Image.new("RGBA", (W, MAXH), bg), 0, 0, 0
        d = D.Draw(sheet)
        d.text((x + 2, y), label, fill=(255, 255, 0))
        sheet.alpha_composite(bi, (x + 2, y + 13))
        if side:
            sheet.alpha_composite(ai, (x + 6 + bi.width, y + 13))
        else:
            sheet.alpha_composite(ai, (x + 2, y + 15 + bi.height))
        x += w + 6
        rowh = max(rowh, h)
    flush()
    return names


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "work/output/redraw/overlay"))
    ap.add_argument("--preview", default=os.path.join(ROOT, "work/ui/redraw_preview"))
    ap.add_argument("--layout", default=os.path.join(ROOT, "work/ui/redraw_layout.json"))
    ap.add_argument("--only", help="only files whose path contains this")
    ap.add_argument("--no-sheets", action="store_true")
    ap.add_argument("--no-write", action="store_true", help="previews only, no GIMs")
    ap.add_argument("--version", default="dev", help="build version for {version} in item texts")
    a = ap.parse_args()
    global VERSION
    VERSION = a.version
    layout = load_layout(a.layout)
    by_file = load_rows()
    shared = share_choices(layout, by_file)
    pairs, report, done, errs, held = [], [], {}, [], {}
    files = sorted(by_file)
    # thumbnails last: they shrink redrawn stills
    thumbs = layout.get("thumbnails", {})
    for path in files:
        if a.only and a.only not in path:
            continue
        if path in thumbs:
            continue
        after, before, rep = redraw(path, by_file[path], layout, shared)
        report += rep
        if after is None:
            errs += [r for r in rep if "error" in r]
            if any("kept" in r for r in rep):
                pairs.append((path.replace("data/", "") + " (kept)", before, before))
            continue
        spec = items_for(layout, path, by_file[path])[1]
        if spec.get("hold"):
            held[path] = spec["hold"]
            report.append({"file": path, "held": spec["hold"]})
        done[path] = after
        pairs.append((path.replace("data/", "") + (" (held)" if spec.get("hold") else ""), before, after))
    for path, src in thumbs.items():
        if path not in by_file or (a.only and a.only not in path and a.only not in src):
            continue
        b = open(os.path.join(ROOT, "work/source/dat", path), "rb").read()
        before = gim.decode(b)
        after = done.get(src)
        if after is None:
            after = redraw(src, by_file[src], layout, shared)[0]
        if after is None:  # the still is kept as it is, so is its thumbnail
            pairs.append((path.replace("data/", "") + " (kept)", before, before))
            report.append({"file": path, "kept": "thumbnail of a kept still"})
            continue
        th = thumbnail(after, before)
        done[path] = th
        pairs.append((path.replace("data/", "") + " (from %s)" % os.path.basename(src), before, th))
        report.append({"file": path, "thumbnail_of": src})
    # encode
    if not a.no_write:
        for path, im in done.items():
            if path in held:
                continue
            b = open(os.path.join(ROOT, "work/source/dat", path), "rb").read()
            nb = gim.encode(b, im)
            o = os.path.join(a.out, path)
            os.makedirs(os.path.dirname(o), exist_ok=True)
            open(o, "wb").write(nb)
    # quantized look in the previews
    qpairs = []
    for label, before, after in pairs:
        path = "data/" + label.split(" (")[0]
        if not a.no_write and path in done and path not in held:
            nb = open(os.path.join(a.out, path), "rb").read()
            after = gim.decode(nb)
        qpairs.append((label, before, after))
    os.makedirs(a.preview, exist_ok=True)
    if not a.only:
        json.dump(report, open(os.path.join(a.preview, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(shared_report(by_file, layout), open(os.path.join(a.preview, "shared_text.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    if not a.no_sheets:
        names = contact_sheets(qpairs, a.preview if not a.only else os.path.join(a.preview, "_only"))
        print("sheets:", len(names))
    over = [r for r in report if r.get("overflow")]
    fb = [r for r in report if r.get("fallback")]
    print("textures %d (held %d, kept as art %d), items %d, fallbacks %d, overflow %d, no layout %d" % (
        len(done), len(held), len([r for r in report if "kept" in r]), len([r for r in report if "text" in r]),
        len(fb), len(over), len(errs)))
    for p_, why in held.items():
        print("  HELD (not written)", p_, "-", why)
    for r in over:
        print("  OVERFLOW", r["file"], repr(r["text"]))
    for e in errs[:40]:
        print("  NO LAYOUT", e["file"])


if __name__ == "__main__":
    main()
