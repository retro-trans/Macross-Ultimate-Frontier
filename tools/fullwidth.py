"""Turn the game's full-width Latin text (ＶＦ－２７, ＨＰ, Ｓ．Ｍ．Ｓ) into ASCII so it is
drawn with the proportional English font instead of the fixed-width Japanese glyphs.

Usage:
  python tools/fullwidth.py eboot <dump.json> <in EBOOT> <out EBOOT>
  python tools/fullwidth.py csv <out rows.json> [--src work/source/dat] [--skip <rows.json> ...]

Text that holds only full-width Latin (no kana or kanji) was never part of the
translation, so it kept the Japanese glyphs. Each character becomes its ASCII
form (full-width space -> space, ” -> "); characters without one (α, ×) stay.

eboot: every such string from the string dump (tools/dump_eboot.py) is rewritten in
place: ASCII is 1 byte per character instead of 2, so it always fits, and nothing
moves. Skipped: strings made only of digits, dashes and × (digit tables and "－－－"
placeholders the code may index or measure) and strings marked not_text.

csv: rows for tools/insert_text.py (id/jp/ref/en) for every such cell of the menu
text CSVs (data/menu/text/*.csv). Cells that also hold Japanese are translated
already, and cells that a --skip file (the build's --tr files) already sets are
left to it. Other CSVs (locate/*.csv and the rest) are data and are not touched.

The names occur only in the EBOOT and in these display CSVs (no other game file
holds them), so no lookup depends on the full-width spelling.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = re.compile("[぀-ゟ゠-ヺヽ-ヿ㐀-鿿]")   # kana and kanji (not ー ・)
FW = re.compile("[！-～]")
ONLY_TABLE = re.compile("[－０-９×　 ]+")
EXTRA = {"　": " ", "”": '"', "“": '"'}


def half(s):
    return "".join(chr(ord(c) - 0xFEE0) if "！" <= c <= "～" else EXTRA.get(c, c) for c in s)


def wanted(s):
    return bool(FW.search(s)) and not JP.search(s) and not ONLY_TABLE.fullmatch(s)


def do_eboot(dump, src, dst):
    data = bytearray(open(src, "rb").read())
    n = 0
    for e in json.load(open(dump, encoding="utf-8")):
        if not wanted(e["jp"]) or e.get("not_text") or e.get("tail_of"):
            continue
        old = e["jp"].encode("cp932")
        new = half(e["jp"]).encode("cp932")
        o = e["offset"]
        if data[o:o + len(old) + 1] != old + b"\0":
            continue  # translated and moved, or changed by an earlier step: leave it
        data[o:o + len(old) + 1] = new + bytes(len(old) + 1 - len(new))
        n += 1
    open(dst, "wb").write(data)
    print("%d full-width EBOOT strings now ASCII" % n)


def do_csv(out, src, skip=()):
    taken = set()
    for f in skip:
        j = json.load(open(f, encoding="utf-8"))
        for r in (j["rows"] if isinstance(j, dict) else j):
            ref = r.get("ref")
            if isinstance(ref, dict) and "col" in ref and r.get("en"):
                taken.add((ref["file"], ref["row"], ref["col"]))
    rows = []
    for path in sorted(glob.glob(os.path.join(src, "data", "menu", "text", "*.csv"))):
        rel = os.path.relpath(path, src).replace(os.sep, "/")
        name = os.path.splitext(os.path.basename(path))[0]
        lines = open(path, "rb").read().decode("cp932").split("\r\n")
        for i, line in enumerate(lines):
            cells = line.split(",")
            for c, cell in enumerate(cells):
                if c and wanted(cell) and (rel, i, c) not in taken:
                    rows.append({"id": "fw:%s:%s:col%d" % (name, cells[0], c), "jp": cell,
                                 "ref": {"file": rel, "row": i, "col": c, "key": cells[0], "field": "col%d" % c},
                                 "en": half(cell)})
    json.dump({"rows": rows}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%d full-width CSV cells -> %s" % (len(rows), out))


def main():
    a = sys.argv[1:]
    if a[:1] == ["eboot"] and len(a) == 4:
        do_eboot(*a[1:])
    elif a[:1] == ["csv"] and len(a) >= 2:
        src = a[a.index("--src") + 1] if "--src" in a else os.path.join(ROOT, "work", "source", "dat")
        skip, i = [], 0
        while "--skip" in a[i:]:
            i = a.index("--skip", i) + 1
            skip.append(a[i])
        do_csv(a[1], src, skip)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
