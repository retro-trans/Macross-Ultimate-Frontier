"""Print rows lo..hi of the dialogue work file with Japanese and English.

Usage: python tools/show_rows.py <lo> <hi>
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, "work/translation/en/dialogue.json"), encoding="utf-8"))["rows"]
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for r in rows:
    if lo <= r["row"] <= hi:
        print("%4d | %s | %s | %s | flags=%s" % (r["row"], r["id"], r["cat"], r["scene"], ",".join(r["flags"])))
        print("  JP: " + r["jp"].replace("\n", "<NL>"))
        print("  EN: " + r["en"].replace("\n", "<NL>"))
        if r["notes"]:
            print("  NOTE: " + r["notes"])
