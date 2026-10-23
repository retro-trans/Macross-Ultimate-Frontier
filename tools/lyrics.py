"""Timed song lyrics for missions: song list, templates, and the file tails (docs/lyrics.md).

Usage:
  python tools/lyrics.py list [--all] [--md]
  python tools/lyrics.py templates [--dir DIR] [--all] [--only ID[,ID...]]
  python tools/lyrics.py check [--dir DIR] [--widths vwf_widths.json]
  python tools/lyrics.py build --out OUT [--dir DIR] [--widths ...] [--placeholder]

DIR defaults to work/translation/en/lyrics (gitignored: song lyrics are
copyrighted, so the filled files stay on your machine).

list       the songs the game can play, from the EBOOT's BGM table (0x377D00:
           name, credits, volume per bgmNN.at3) with each file's length and
           loop. Without --all only the tracks with vocals.
templates  writes DIR/<song_id>.json for each song that has no file yet:
           song id, title, file, length, loop, and an empty "lines" list.
           Existing files are never overwritten.
check      reads every DIR/*.json and reports bad times, overlaps, and lines
           that are too wide or too long.
build      writes OUT/bgmNN.at3 = the original file + a lyrics tail, for every
           song with at least one line (tools/build_iso.py --lyrics puts them on
           the disc). --placeholder writes test lines instead
           ("bgm03 line 1 at 0:02") for every BGM file, no lyrics needed.

The tail (read by the EBOOT patch tools/lyrics_patch.py):

    ... RIFF file ... | zero pad to 4 | blob | u32 blob_len | "LYR1"
    blob = u32 loop_start, u32 loop_end, u32 count,
           count x (u32 start, u32 end, u32 text offset), texts (NUL-terminated)

with times in samples. A song file is loaded whole when it plays, so the tail
costs a few KB of the song's own buffer and no extra read.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BGM_DIR = os.path.join(ROOT, "work", "source", "iso", "PSP_GAME", "USRDIR", "data", "sound", "bgm")
ISO_DIR = "PSP_GAME/USRDIR/data/sound/bgm"
EBOOT = os.path.join(ROOT, "work", "source", "eboot", "EBOOT.dec.bin")
UI_EN = os.path.join(ROOT, "work", "translation", "en", "ui.en.json")
LYRICS_DIR = os.path.join(ROOT, "work", "translation", "en", "lyrics")
WIDTHS = os.path.join(ROOT, "work", "output", "vwf", "vwf_widths.json")

BGM_TABLE, BGM_COUNT = 0x377D00, 93    # 16 bytes each: name ptr, u8 id, u8 flags, s16 order, u32 volume, credits ptr
TEXT_OFF = 0xA0                        # file offset of vaddr 0
# Game-original song skills: the credits name no singer, but they are songs.
SKILL_SONGS = {79: "Song skill (Sara)", 80: "Song skill (Ishtar)", 81: "Song skill (Myung)"}

SIZE, BOX_W = 12, 290                  # tools/lyrics_patch.py CONFIG
MAX_LINES = 3
MAX_BLOB = 0xF000                      # sanity limit per song
DEFAULT_HOLD = 6.0                     # a line without "end_sec" lasts until the next line, at most this long


# ---------------------------------------------------------------- song list

def at3_info(path):
    b = open(path, "rb").read()
    info = {"size": len(b)}
    i = 12
    while i + 8 <= len(b):
        cid = b[i:i + 4]
        n = struct.unpack_from("<I", b, i + 4)[0]
        d = b[i + 8:i + 8 + n]
        if cid == b"fmt ":
            info["rate"] = struct.unpack_from("<I", d, 4)[0]
        elif cid == b"fact":
            info["samples"] = struct.unpack_from("<I", d)[0]
        elif cid == b"smpl" and struct.unpack_from("<I", d, 28)[0]:
            info["loop"] = struct.unpack_from("<II", d, 44)
        elif cid == b"data":
            break
        i += 8 + n + (n & 1)
    return info


def songs(all_tracks=False):
    """[{id, num, title, credits, vocal, file, ...}] from the EBOOT table and the bgm folder."""
    eb = open(EBOOT, "rb").read()
    en = {}
    if os.path.exists(UI_EN):
        for r in json.load(open(UI_EN, encoding="utf-8"))["rows"]:
            for o in r["occ"]:
                if o["id"].startswith("eboot:") and r.get("en"):
                    en[int(o["id"][6:], 16)] = r["en"]

    def text(va):
        return en.get(va + TEXT_OFF, "").replace("\n", " / ") if va else ""

    first = {}                         # identical files: the first id carries the lyrics
    for p in sorted(glob.glob(os.path.join(BGM_DIR, "bgm*.at3"))):
        first.setdefault(hashlib.md5(open(p, "rb").read()).hexdigest(), os.path.basename(p)[:-4])
    out = []
    for n in range(BGM_COUNT):
        name, num, flags, order, vol, cred = struct.unpack_from("<IBBhII", eb, BGM_TABLE + TEXT_OFF + 16 * n)
        path = os.path.join(BGM_DIR, "bgm%02d.at3" % n)
        if not os.path.exists(path):
            continue
        credits = re.sub(r"\s+", " ", text(cred)).strip()
        vocal = "Vocals:" in credits or "Lyrics:" in credits or n in SKILL_SONGS
        if not (vocal or all_tracks):
            continue
        a = at3_info(path)
        rate = a.get("rate", 44100)
        title = text(name) or "(no name)"
        plays = ("song skill" if "Skill:" in title or n in SKILL_SONGS else
                 "song weapon / SPA of a unit" if "Song Weapon" in title or "Song SPA" in title else
                 "mission BGM" if flags & 1 else "other")
        s = {"song_id": "bgm%02d" % n, "title": title, "credits": credits, "vocal": vocal, "plays": plays,
             "file": "%s/bgm%02d.at3" % (ISO_DIR, n),
             "duration_sec": round(a.get("samples", 0) / rate, 2), "rate": rate}
        if "loop" in a:
            s["loop_start_sec"], s["loop_end_sec"] = (round(x / rate, 2) for x in a["loop"])
        same = first[hashlib.md5(open(path, "rb").read()).hexdigest()]
        if same != s["song_id"]:
            s["same_as"] = same
        if n in SKILL_SONGS:
            s["note"] = SKILL_SONGS[n] + "; the credits name no singer, vocals not checked."
        out.append(s)
    return out


def mmss(sec):
    return "%d:%05.2f" % (sec // 60, sec % 60)


def cmd_list(a):
    rows = songs(a.all)
    if a.md:
        print("| Song id | Title | Plays as | Length | Loop | Same recording as |")
        print("| --- | --- | --- | --- | --- | --- |")
        for s in rows:
            loop = "%s-%s" % (mmss(s["loop_start_sec"]), mmss(s["loop_end_sec"])) if "loop_start_sec" in s else "none"
            print("| %s | %s | %s | %s | %s | %s |" % (s["song_id"], s["title"].replace("|", "/"), s["plays"],
                                                      mmss(s["duration_sec"]), loop, s.get("same_as", "")))
    else:
        for s in rows:
            print("%-6s %8s  %s%s" % (s["song_id"], mmss(s["duration_sec"]), s["title"],
                                     "" if s["vocal"] else "  (instrumental)"))
    print("%d tracks" % len(rows), file=sys.stderr)


# ---------------------------------------------------------------- templates

HELP = ("Fill in 'lines' in play order. start_sec / end_sec are seconds from the start of the file "
        "(a number like 12.5, or a string like \"1:02.5\"). end_sec may be left out: the line then lasts "
        "until the next line starts (at most %g s). Use \\n in 'text' for a second line. "
        "A file with 'same_as' is the same recording as that song: leave its 'lines' empty and it "
        "shows that song's lines. See docs/lyrics.md." % DEFAULT_HOLD)


def cmd_templates(a):
    os.makedirs(a.dir, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    made = kept = 0
    for s in songs(a.all):
        if only and s["song_id"] not in only:
            continue
        path = os.path.join(a.dir, s["song_id"] + ".json")
        if os.path.exists(path):
            kept += 1
            continue
        t = {"_help": HELP}
        t.update({k: v for k, v in s.items() if k not in ("vocal", "rate")})
        t["duration"] = mmss(s["duration_sec"])
        t["lines"] = []
        with open(path, "w", encoding="utf-8") as f:
            json.dump(t, f, ensure_ascii=False, indent=2)
            f.write("\n")
        made += 1
    print("%d templates written, %d existing files kept -> %s" % (made, kept, a.dir))


# ---------------------------------------------------------------- lines -> tail

ADV = None


def load_widths(path):
    global ADV
    if ADV is None:
        if not os.path.exists(path):
            sys.exit("no VWF widths at %s (run tools/vwf_build.py, or pass --widths)" % path)
        ADV = json.load(open(path, encoding="utf-8"))["advance"]


def width(s):
    """Pixel width at SIZE, the way the game scales the VWF advances (docs/vwf.md)."""
    w = 0
    for ch in s:
        o = ord(ch)
        w += SIZE - round((14 - ADV[o - 0x20]) * SIZE / 14) if 0x20 <= o < 0x80 else SIZE
    return w


def wrap(text):
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            cand = word if not line else line + " " + word
            if line and width(cand) > BOX_W:
                out.append(line)
                line = word
            else:
                line = cand
        out.append(line)
    return out


ASCII_FIX = {"…": "\x7f", "—": "-", "–": "-", "‘": "'", "’": "'", "“": '"', "”": '"', " ": " ",
             "♪": "*", "～": "~"}


def encode(text):
    text = "".join(ASCII_FIX.get(c, c) for c in text)
    if "{" in text:
        raise ValueError("'{' starts a colour code in the game's text routine")
    return text.encode("cp932")


def seconds(v):
    if isinstance(v, (int, float)):
        return float(v)
    m = re.fullmatch(r"\s*(?:(\d+):)?(\d+(?:\.\d+)?)\s*", str(v))
    if not m:
        raise ValueError("bad time %r (use 12.5 or \"1:02.5\")" % v)
    return int(m.group(1) or 0) * 60 + float(m.group(2))


def timed_lines(doc):
    """[(start_s, end_s, text)] from a lyrics file, with problems as ValueError."""
    raw = doc.get("lines") or []
    rows = []
    for i, ln in enumerate(raw):
        if not isinstance(ln, dict) or not str(ln.get("text", "")).strip():
            continue
        st = ln.get("start_sec", ln.get("start"))
        if st is None:
            raise ValueError("line %d has no start_sec" % (i + 1))
        en = ln.get("end_sec", ln.get("end"))
        rows.append([seconds(st), None if en is None else seconds(en), str(ln["text"]).strip(), i + 1])
    rows.sort(key=lambda r: r[0])
    for k, r in enumerate(rows):
        if r[1] is None:
            nxt = rows[k + 1][0] if k + 1 < len(rows) else r[0] + DEFAULT_HOLD
            r[1] = min(nxt, r[0] + DEFAULT_HOLD)
        if r[1] <= r[0]:
            raise ValueError("line %d ends before it starts" % r[3])
    return rows


def blob_of(rows, rate, loop):
    texts, entries = b"", []
    head = 12 + 12 * len(rows)
    for st, en, text, _ in rows:
        entries.append((round(st * rate), round(en * rate), head + len(texts)))
        texts += encode("\n".join(wrap(text))) + b"\0"
    blob = struct.pack("<III", loop[0], loop[1], len(rows))
    blob += b"".join(struct.pack("<III", *e) for e in entries) + texts
    blob += b"\0" * (-len(blob) % 4)
    return blob


def tail_for(orig_size, blob):
    return b"\0" * (-orig_size % 4) + blob + struct.pack("<I", len(blob)) + b"LYR1"


def check_doc(doc, sid, problems, warn):
    rows = timed_lines(doc)
    dur = doc.get("duration_sec")
    for k, (st, en, text, i) in enumerate(rows):
        lines = wrap(text)
        if len(lines) > MAX_LINES:
            problems.append("%s line %d wraps to %d lines (at most %d): %r" % (sid, i, len(lines), MAX_LINES, text))
        for ln in lines:
            if width(ln) > BOX_W:
                problems.append("%s line %d: a word is wider than the box (%d px > %d)" % (sid, i, width(ln), BOX_W))
        try:
            encode(text)
        except (ValueError, UnicodeEncodeError) as e:
            problems.append("%s line %d: %s" % (sid, i, e))
        if dur and st >= dur:
            warn.append("%s line %d starts at %s, after the end of the file (%s)" % (sid, i, mmss(st), mmss(dur)))
        if k + 1 < len(rows) and en > rows[k + 1][0] + 1e-6:
            warn.append("%s line %d overlaps the next line (only the first is shown)" % (sid, i))
    return rows


def lyric_files(d):
    """[(song id, document)]; a file with no lines and "same_as" takes that song's lines."""
    docs = {}
    for p in sorted(glob.glob(os.path.join(d, "bgm*.json"))):
        sid = os.path.splitext(os.path.basename(p))[0]
        if re.fullmatch(r"bgm\d\d", sid):
            try:
                docs[sid] = json.load(open(p, encoding="utf-8"))
            except json.JSONDecodeError as e:
                docs[sid] = ValueError("%s is not valid JSON: %s" % (os.path.basename(p), e))
    out = []
    for sid, doc in docs.items():
        if isinstance(doc, dict) and not doc.get("lines") and doc.get("same_as") in docs:
            src = docs[doc["same_as"]]
            if isinstance(src, dict):
                doc = dict(doc, lines=src.get("lines") or [])
        out.append((sid, doc))
    return out


def cmd_check(a):
    load_widths(a.widths)
    problems, warn, n_lines, n_songs = [], [], 0, 0
    for sid, doc in lyric_files(a.dir):
        try:
            if isinstance(doc, Exception):
                raise doc
            rows = check_doc(doc, sid, problems, warn)
        except ValueError as e:
            problems.append("%s: %s" % (sid, e))
            continue
        if rows:
            n_songs += 1
            n_lines += len(rows)
    for w in warn:
        print("warning:", w)
    for p in problems:
        print("ERROR:", p)
    print("%d songs with lyrics, %d lines, %d errors, %d warnings" % (n_songs, n_lines, len(problems), len(warn)))
    return 1 if problems else 0


def placeholder_rows(sid, dur):
    rows, t, n = [], 2.0, 1
    while t + 1 < dur:
        rows.append([t, min(t + 4.5, dur), "%s line %d at %s" % (sid, n, "%d:%02d" % (t // 60, t % 60)), n])
        t += 6.0
        n += 1
    return rows


def cmd_build(a):
    load_widths(a.widths)
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    if a.placeholder:
        for p in sorted(glob.glob(os.path.join(BGM_DIR, "bgm*.at3"))):
            sid = os.path.splitext(os.path.basename(p))[0]
            info = at3_info(p)
            jobs.append((sid, placeholder_rows(sid, info.get("samples", 0) / info.get("rate", 44100))))
    else:
        problems, warn = [], []
        for sid, doc in lyric_files(a.dir):
            try:
                if isinstance(doc, Exception):
                    raise doc
                rows = check_doc(doc, sid, problems, warn)
            except ValueError as e:
                problems.append("%s: %s" % (sid, e))
                continue
            if rows:
                jobs.append((sid, rows))
        for w in warn:
            print("warning:", w)
        if problems:
            for p in problems:
                print("ERROR:", p)
            sys.exit("lyrics have errors; fix them or run tools/lyrics.py check")
    written = []
    for sid, rows in jobs:
        src = os.path.join(BGM_DIR, sid + ".at3")
        if not os.path.exists(src):
            print("no file for", sid)
            continue
        data = open(src, "rb").read()
        info = at3_info(src)
        loop = info.get("loop", (0, 0))
        blob = blob_of(rows, info.get("rate", 44100), loop)
        if len(blob) > MAX_BLOB:
            sys.exit("%s: %d bytes of lyrics, more than %d" % (sid, len(blob), MAX_BLOB))
        open(os.path.join(a.out, sid + ".at3"), "wb").write(data + tail_for(len(data), blob))
        written.append(sid)
    print("%d song files with lyrics -> %s" % (len(written), a.out))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--all", action="store_true")
    p.add_argument("--md", action="store_true")
    p = sub.add_parser("templates")
    p.add_argument("--dir", default=LYRICS_DIR)
    p.add_argument("--all", action="store_true")
    p.add_argument("--only", default="")
    p = sub.add_parser("check")
    p.add_argument("--dir", default=LYRICS_DIR)
    p.add_argument("--widths", default=WIDTHS)
    p = sub.add_parser("build")
    p.add_argument("--out", required=True)
    p.add_argument("--dir", default=LYRICS_DIR)
    p.add_argument("--widths", default=WIDTHS)
    p.add_argument("--placeholder", action="store_true")
    a = ap.parse_args()
    sys.exit({"list": cmd_list, "templates": cmd_templates, "check": cmd_check, "build": cmd_build}[a.cmd](a))


if __name__ == "__main__":
    main()
