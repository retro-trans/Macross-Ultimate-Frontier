"""Print rows of the dialogue work file for a translator.

Usage: python tools/show_slice.py <slice_no> [--context N]
Prints row, id, cat, scene and the Japanese for the slice (80 rows), plus N
rows of context on either side (default 10), marked with '~'.
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, "work/translation/en/dialogue.json"), encoding="utf-8"))["rows"]
n = int(sys.argv[1]); ctx = int(sys.argv[sys.argv.index("--context") + 1]) if "--context" in sys.argv else 10
lo, hi = (n - 1) * 80 + 1, n * 80
for r in rows:
    if lo - ctx <= r["row"] <= hi + ctx:
        mark = " " if lo <= r["row"] <= hi else "~"
        print("%s%4d | %s | %s | %s\n      %s" % (mark, r["row"], r["id"], r["cat"], r["scene"], r["jp"].replace("\n", "<NL>")))
