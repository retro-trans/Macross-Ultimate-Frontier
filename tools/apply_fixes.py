"""Apply reviewed translation fixes to the slice files, then re-merge.

Usage: python tools/apply_fixes.py <fixes.json> [--apply]
fixes.json: {"fixes": [{"row": 123, "en": "...", "why": "..."},
                       {"jp_same_as_row": 656, "en": "...", "why": "..."}]}
 - "row" fixes one row.
 - "jp_same_as_row" fixes every row whose Japanese is identical to that row's.
 - "replace": {"old": "...", "new": "...", "cat": "quote"} does a literal
   substring replacement in every row (optionally only one category).
Dry run by default: prints before/after for every row it touches.
The slice files are the source of truth (merge_slices.py copies them into the
work file), so fixes are written there and then merged.
"""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work/translation/en/dialogue.json")


def main():
    apply = "--apply" in sys.argv
    fixes = json.load(open(sys.argv[1], encoding="utf-8"))["fixes"]
    rows = json.load(open(WORK, encoding="utf-8"))["rows"]
    byrow = {r["row"]: r for r in rows}
    target = {}  # id -> (new en, why)
    for f in fixes:
        if "row" in f:
            target[byrow[f["row"]]["id"]] = (f["en"], f.get("why", ""))
        elif "jp_same_as_row" in f:
            jp = byrow[f["jp_same_as_row"]]["jp"]
            for r in rows:
                if r["jp"] == jp:
                    target[r["id"]] = (f["en"], f.get("why", ""))
        elif "replace" in f:
            rp = f["replace"]
            for r in rows:
                cur = target.get(r["id"], (r["en"], ""))[0]
                if (not rp.get("cat") or r["cat"] == rp["cat"]) and rp["old"] in cur:
                    target[r["id"]] = (cur.replace(rp["old"], rp["new"]), f.get("why", ""))
    byid = {r["id"]: r for r in rows}
    n = 0
    files = sorted(glob.glob(os.path.join(ROOT, "work/translation/en/slices/slice_*.en.json")))
    for path in files:
        s = json.load(open(path, encoding="utf-8"))
        touched = False
        for t in s["rows"]:
            if t["id"] in target and t["en"] != target[t["id"]][0]:
                new, why = target[t["id"]]
                print("row %d (%s): %s\n  - %r\n  + %r" % (byid[t["id"]]["row"], os.path.basename(path), why, t["en"], new))
                t["en"] = new
                if why:
                    t["notes"] = (t.get("notes", "") + " | review: " + why).strip(" |")
                touched = True
                n += 1
        if touched and apply:
            json.dump(s, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%d rows %s" % (n, "changed" if apply else "would change (dry run)"))


if __name__ == "__main__":
    main()
