"""Build the dialogue translation work file.

Collects every piece of story/dialogue text the game shows as text and writes
work/translation/en/dialogue.json (gitignored: it contains Japanese).

Sources:
  narration  EBOOT prologue/epilogue lines (one string per line), from the
             PPSSPP-decrypted EBOOT at work/source/eboot/EBOOT.dec.bin
  briefing   data/menu/text/mission_ext.csv  strMission + strStory
  ingame     data/script/*.fes Japanese strings (objectives, tutorial lines)
  quote      data/menu/text/nn_ext.csv NNSHOP_ITEM_5000-5299 (player titles,
             many of them famous character lines)

If the work file already exists, existing English ("en", "flags", "notes")
is carried over by id, so the file can be rebuilt safely.

Usage: python tools/build_dialogue.py [--dry-run]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "work", "source", "text")
EBOOT = os.path.join(ROOT, "work", "source", "eboot", "EBOOT.dec.bin")
OUT = os.path.join(ROOT, "work", "translation", "en", "dialogue.json")

NARR_START, NARR_END = 0x38F6A0, 0x3927F0
# Scene start offsets, named from their content. ASCII strings between scenes
# (cam_event_pr_mp_00 ...) are camera labels, not text, and are skipped.
NARR_SCENES = [
    (0x38F6A0, "prologue_sdf"), (0x38F9D4, "prologue_plus"), (0x38FC8C, "prologue_m7"),
    (0x38FF4C, "prologue_frontier"), (0x390134, "prologue_zero"), (0x3904B8, "prologue_dyrl"),
    (0x3907B0, "prologue_d7"), (0x390A9C, "epilogue_sdf_1"), (0x390E98, "epilogue_sdf_2"),
    (0x3910E8, "epilogue_plus"), (0x391614, "epilogue_m7"), (0x3919C0, "epilogue_frontier"),
    (0x391DFC, "epilogue_zero"), (0x392160, "epilogue_dyrl"), (0x3924F4, "epilogue_d7"),
]


def eboot_narration():
    b = open(EBOOT, "rb").read()
    rows, off = [], NARR_START
    while off < NARR_END:
        end = b.index(b"\0", off)
        raw = b[off:end]
        if raw and not all(c < 0x80 for c in raw):
            scene = [n for s, n in NARR_SCENES if s <= off][-1]
            rows.append({
                "id": "eboot:%06X" % off, "cat": "narration", "scene": scene,
                "ref": {"file": "EBOOT.BIN", "offset": off, "bytes": len(raw)},
                "jp": raw.decode("cp932"),
            })
        off = end + 1
        while off < NARR_END and b[off] == 0:
            off += 1
    return rows


def main():
    dry = "--dry-run" in sys.argv
    menu = json.load(open(os.path.join(TEXT, "menu_text.json"), encoding="utf-8"))
    fes = json.load(open(os.path.join(TEXT, "fes_strings.json"), encoding="utf-8"))

    rows = eboot_narration()

    for x in menu:
        if x["source"].endswith("mission_ext.csv") and x["field"] in ("strMission", "strStory") and x["jp"]:
            rows.append({"id": x["id"], "cat": "briefing", "scene": x["key"],
                         "ref": {"file": x["source"], "row": x["row"], "col": x["col"], "key": x["key"], "field": x["field"]},
                         "jp": x["jp"]})

    for x in fes:
        rows.append({"id": x["id"], "cat": "ingame", "scene": x["id"].split(":")[0],
                     "ref": {"file": x["source"], "offset": x["offset"], "pool_offset": x["pool_offset"], "bytes": x["bytes"]},
                     "jp": x["jp"]})

    for x in menu:
        m = re.match(r"NNSHOP_ITEM_(\d+)$", x["key"])
        if x["source"].endswith("nn_ext.csv") and m and 5000 <= int(m.group(1)) < 5300 and x["jp"]:
            rows.append({"id": x["id"], "cat": "quote", "scene": "titles",
                         "ref": {"file": x["source"], "row": x["row"], "col": x["col"], "key": x["key"]},
                         "jp": x["jp"]})

    old = {}
    if os.path.exists(OUT):
        for r in json.load(open(OUT, encoding="utf-8"))["rows"]:
            old[r["id"]] = r
    for i, r in enumerate(rows, 1):
        r["row"] = i
        o = old.get(r["id"], {})
        r["en"] = o.get("en", "")
        r["flags"] = o.get("flags", [])
        r["notes"] = o.get("notes", "")

    cats = {}
    for r in rows:
        cats[r["cat"]] = cats.get(r["cat"], 0) + 1
    print("rows", len(rows), cats, "carried over", sum(1 for r in rows if r["en"]))
    print("slices of 80:", (len(rows) + 79) // 80)
    if dry:
        for r in rows[:3] + rows[-3:]:
            print(r["row"], r["id"], r["cat"], r["scene"], r["jp"][:40].replace("\n", "/"))
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"_meta": {"version": "0.1.0", "slice_size": 80}, "rows": rows},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
