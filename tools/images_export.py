"""Validate the image-text translation files and write the git-safe merged copy.

Usage: python tools/images_export.py
Reads work/translation/en/images/img_*.json (one per texture group; they hold the
Japanese transcription and are gitignored), checks that every row's source texture
exists under work/source/dat and that no English/notes/style field contains Japanese,
then writes work/translation/en/images.en.json without the "jp" field.
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JP = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
rows, groups, errs = [], [], []
for f in sorted(glob.glob(os.path.join(ROOT, "work/translation/en/images/img_*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    n_empty = 0
    for r in d.get("rows", []):
        src = r["file"].split("#")[0]
        if not os.path.exists(os.path.join(ROOT, "work/source/dat", src)):
            errs.append("%s: missing source %s" % (os.path.basename(f), r["file"]))
        for k in ("en", "notes", "style", "kind"):
            if JP.search(str(r.get(k, ""))):
                errs.append("%s: Japanese in %s of %s" % (os.path.basename(f), k, r["file"]))
        if not r.get("en"):
            n_empty += 1
        rows.append(dict({k: v for k, v in r.items() if k != "jp"}, group=d.get("group", os.path.basename(f))))
    groups.append({"group": d.get("group"), "folders": d.get("folders"), "sheets_viewed": d.get("sheets_viewed"),
                   "rows": len(d.get("rows", [])), "empty_en": n_empty,
                   "notes": d.get("notes", "") if not JP.search(str(d.get("notes", ""))) else "(see local file)"})
for g in groups:
    print("%-10s rows %4d  empty en %d  sheets %s" % (g["group"], g["rows"], g["empty_en"], g["sheets_viewed"]))
print("total rows", len(rows), "errors", len(errs))
for e in errs[:20]:
    print("  ERROR", e)
if errs:
    sys.exit(1)
out = {"_meta": {"version": "0.3.0", "groups": groups}, "rows": rows}
json.dump(out, open(os.path.join(ROOT, "work/translation/en/images.en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote work/translation/en/images.en.json")
