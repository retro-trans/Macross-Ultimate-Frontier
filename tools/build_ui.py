"""Build the work file for all remaining Japanese text (everything except the dialogue corpus).

Usage: python tools/build_ui.py [--dry-run]

Sources:
  eboot   work/source/text/eboot_strings.json  (tools/dump_eboot.py): menus, system and
          save messages, help lines, skills, titles, unlock messages, gallery captions,
          song credits, unit/weapon names, the pilot table
  csv     work/source/text/menu_text.json: the rest of nn_ext.csv, ms_ext.csv (unit
          descriptions), pilot_ext.csv (pilot profiles), pack_ext.csv (pack descriptions)
  locate  work/source/text/locate_names.json: mission unit display names
Rows already in the dialogue work file are skipped.

Each distinct Japanese string becomes ONE row (translate once), with every place it
occurs listed in "occ". Rows are ordered by first occurrence, so neighbours give
context. English from the dialogue translation is prefilled where the Japanese is
identical (status "tm").

Skipped, never translated:
  - strings without kana/kanji (digits, symbols, full-width letters only), and the
    renderer's ASCII glyph map (eboot:347EEC)
  - one-character tails of a longer string (tail_of)
  - internal unit-list labels: デモ用 / 顔絵用 / ダミー / 削除 / テスト / 予定

Byte limits: EBOOT strings flagged in_place (pilot table) or inline_copy must be
rewritten in place, so "max_bytes" = capacity - 1 (Shift-JIS bytes; ASCII = 1).

Output: work/translation/en/ui.json (gitignored: contains Japanese).
Existing English/flags/notes are carried over by the Japanese text.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "work", "source", "text")
OUT = os.path.join(ROOT, "work", "translation", "en", "ui.json")
DIALOGUE = os.path.join(ROOT, "work", "translation", "en", "dialogue.json")
JPW = re.compile(r"[぀-ヿ㐀-鿿]")
INTERNAL = re.compile(r"デモ用|顔絵用|ダミー|^削除$|テスト|予定")
SKIP_IDS = {"eboot:347EEC"}
SLICE_CHARS, SLICE_ROWS = 4500, 320


def main():
    dry = "--dry-run" in sys.argv
    dia = json.load(open(DIALOGUE, encoding="utf-8"))["rows"]
    done = {r["id"] for r in dia}
    tm = {}
    for r in dia:
        if r["en"]:
            tm.setdefault(r["jp"], r["en"])

    occ = []  # (group, jp, occurrence dict)
    skipped = {"no_japanese": 0, "tail": 0, "internal": 0}
    for x in json.load(open(os.path.join(TEXT, "eboot_strings.json"), encoding="utf-8")):
        if x["id"] in done or x["id"] in SKIP_IDS:
            continue
        if x.get("tail_of"):
            skipped["tail"] += 1
            continue
        if not JPW.search(x["jp"]):
            skipped["no_japanese"] += 1
            continue
        o = {"id": x["id"], "ref": {"file": "EBOOT.BIN", "offset": x["offset"], "bytes": x["bytes"]}}
        if x.get("in_place") or x.get("inline_copy"):
            o["max_bytes"] = x["capacity"] - 1
        occ.append(("eboot@%04X" % (x["offset"] >> 12), x["jp"], o))
    for x in json.load(open(os.path.join(TEXT, "menu_text.json"), encoding="utf-8")):
        if x["id"] in done or not x["jp"]:
            continue
        if not JPW.search(x["jp"]):
            skipped["no_japanese"] += 1
            continue
        f = x["source"].split("/")[-1]
        grp = f
        if f == "nn_ext.csv":
            n = int(re.search(r"(\d+)$", x["key"]).group(1))
            grp = "nn_ext.csv:%d000" % (n // 1000)
        occ.append((grp, x["jp"], {"id": x["id"], "ref": {"file": x["source"], "row": x["row"], "col": x["col"], "key": x["key"], "field": x["field"]}}))
    for x in json.load(open(os.path.join(TEXT, "locate_names.json"), encoding="utf-8")):
        if INTERNAL.search(x["jp"]):
            skipped["internal"] += 1
            continue
        if not JPW.search(x["jp"]):
            skipped["no_japanese"] += 1
            continue
        occ.append(("locate", x["jp"], {"id": "locate:" + x["id"], "ref": {"file": x["source"], "row": x["row"], "col": x["col"], "key": x["key"]}}))

    rows, by_jp = [], {}
    for grp, jp, o in occ:
        if jp not in by_jp:
            by_jp[jp] = {"group": grp, "jp": jp, "occ": []}
            rows.append(by_jp[jp])
        r = by_jp[jp]
        r["occ"].append(o)
        if "max_bytes" in o:
            r["max_bytes"] = min(r.get("max_bytes", 9999), o["max_bytes"])

    old = {}
    if os.path.exists(OUT):
        old = {r["jp"]: r for r in json.load(open(OUT, encoding="utf-8"))["rows"]}
    sl, chars, n_in = 1, 0, 0
    for i, r in enumerate(rows, 1):
        if chars + len(r["jp"]) > SLICE_CHARS or n_in >= SLICE_ROWS:
            sl, chars, n_in = sl + 1, 0, 0
        chars += len(r["jp"])
        n_in += 1
        r["row"], r["slice"] = i, sl
        r["id"] = "u%04d" % i
        o = old.get(r["jp"], {})
        if o.get("en"):
            r["en"], r["flags"], r["notes"], r["status"] = o["en"], o.get("flags", []), o.get("notes", ""), o.get("status", "done")
        elif r["jp"] in tm:
            r["en"], r["flags"], r["notes"], r["status"] = tm[r["jp"]], [], "prefilled from dialogue translation", "tm"
        else:
            r["en"], r["flags"], r["notes"], r["status"] = "", [], "", "todo"

    groups = {}
    for r in rows:
        g = r["group"].split("@")[0].split(":")[0]
        groups[g] = groups.get(g, 0) + 1
    print("unique rows %d (occurrences %d), slices %d, chars %d" % (len(rows), len(occ), sl, sum(len(r["jp"]) for r in rows)))
    print("by source", groups, "skipped", skipped)
    print("prefilled from TM", sum(1 for r in rows if r["status"] == "tm"), "in-place limited", sum(1 for r in rows if "max_bytes" in r))
    if dry:
        for r in rows[:3] + rows[-3:]:
            print(r["row"], r["slice"], r["group"], len(r["occ"]), r.get("max_bytes"), r["jp"][:40].replace("\n", "/"))
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"_meta": {"version": "0.3.0", "slice_chars": SLICE_CHARS, "slice_rows": SLICE_ROWS}, "rows": rows},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
