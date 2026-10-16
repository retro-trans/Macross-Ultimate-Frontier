"""Merge translated slice files into the dialogue work file.

Usage: python tools/merge_slices.py [--dry-run]
Reads work/translation/en/slices/slice_NN.en.json and copies en/flags/notes
into work/translation/en/dialogue.json by id. Prints what would change.
"""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work/translation/en/dialogue.json")


def main():
    dry = "--dry-run" in sys.argv
    d = json.load(open(WORK, encoding="utf-8"))
    byid = {r["id"]: r for r in d["rows"]}
    changed = new = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "work/translation/en/slices/slice_*.en.json"))):
        s = json.load(open(f, encoding="utf-8"))
        for t in s["rows"]:
            r = byid.get(t["id"])
            if r is None:
                print("unknown id", t["id"], "in", os.path.basename(f))
                continue
            if r["en"] != t.get("en", ""):
                if r["en"]:
                    changed += 1
                    if changed <= 10:
                        print("row %d: %r -> %r" % (r["row"], r["en"][:60], t["en"][:60]))
                else:
                    new += 1
            r["en"], r["flags"], r["notes"] = t.get("en", ""), t.get("flags", []), t.get("notes", "")
    done = sum(1 for r in d["rows"] if r["en"])
    print("new %d, changed %d, translated %d/%d" % (new, changed, done, len(d["rows"])))
    if not dry:
        json.dump(d, open(WORK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", WORK)


if __name__ == "__main__":
    main()
