"""Validate a translated slice file against the dialogue work file.

Usage: python tools/check_slice.py <slice_no>   (or 'all')
Checks: every id of the slice present once; no Japanese characters; en not
empty unless flagged unfinished; the same number of line breaks of the
right kind (literal backslash-n for CSV rows, real newline for FES rows) is
reported when it differs; placeholders (%s %d {..}) preserved; no glossary
'avoid' spelling present (case-sensitive, whole word).
Exit code 1 if any hard error.
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, "work/translation/en/dialogue.json"), encoding="utf-8"))["rows"]
JP = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
PH = re.compile(r"%[sd]|\{[a-z]")

avoid = []
for f in glob.glob(os.path.join(ROOT, "work/glossary/*.json")):
    if f.endswith("gaps.json"):
        continue
    d = json.load(open(f, encoding="utf-8"))
    for v in d.values():
        if isinstance(v, list):
            for e in v:
                if isinstance(e, dict):
                    for a in e.get("avoid", []) or []:
                        if a and not JP.search(a):
                            avoid.append((a, e.get("en", "")))


def check(n):
    errs, warns = [], []
    path = os.path.join(ROOT, "work/translation/en/slices/slice_%02d.en.json" % n)
    if not os.path.exists(path):
        return ["missing file " + path], []
    s = json.load(open(path, encoding="utf-8"))
    want = [r for r in rows if (n - 1) * 80 < r["row"] <= n * 80]
    got = {}
    for t in s.get("rows", []):
        if t["id"] in got:
            errs.append("duplicate id " + t["id"])
        got[t["id"]] = t
    if JP.search(json.dumps(s, ensure_ascii=False)):
        errs.append("Japanese characters present in slice file")
    for r in want:
        t = got.get(r["id"])
        if not t:
            errs.append("row %d %s missing" % (r["row"], r["id"]))
            continue
        en, jp = t.get("en", ""), r["jp"]
        if not en and "unfinished" not in t.get("flags", []):
            errs.append("row %d empty en without 'unfinished' flag" % r["row"])
        if not en:
            continue
        if sorted(PH.findall(jp)) != sorted(PH.findall(en)):
            errs.append("row %d placeholders differ: %s vs %s" % (r["row"], PH.findall(jp), PH.findall(en)))
        if jp.count("\\n") != en.count("\\n"):
            warns.append("row %d literal \\n count %d -> %d" % (r["row"], jp.count("\\n"), en.count("\\n")))
        if jp.count("\n") != en.count("\n"):
            warns.append("row %d newline count %d -> %d" % (r["row"], jp.count("\n"), en.count("\n")))
        for a, good in avoid:
            if re.search(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", en) and a not in good:
                errs.append("row %d uses avoided spelling '%s' (use '%s')" % (r["row"], a, good))
    extra = set(got) - {r["id"] for r in want}
    if extra:
        errs.append("ids not in this slice: %s" % sorted(extra)[:5])
    return errs, warns


def main():
    arg = sys.argv[1]
    nums = range(1, (len(rows) + 79) // 80 + 1) if arg == "all" else [int(arg)]
    bad = False
    for n in nums:
        errs, warns = check(n)
        print("slice %02d: %d errors, %d warnings" % (n, len(errs), len(warns)))
        for e in errs:
            print("  ERROR", e)
        for w in warns:
            print("  warn ", w)
        bad |= bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
