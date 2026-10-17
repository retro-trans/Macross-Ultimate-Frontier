"""Helpers for the remaining-text corpus work/translation/en/ui.json (built by build_ui.py).

  python tools/ui_slice.py show <N> [--context K]   rows of slice N (+K rows either side, '~')
  python tools/ui_slice.py check <N>|all            validate slice file(s) slices_ui/ui_NN.en.json
  python tools/ui_slice.py merge [--dry-run]        copy slice files into ui.json
  python tools/ui_slice.py export                   write ui.en.json (no Japanese, for git) and
                                                    ui_insert.json (one row per occurrence with
                                                    id/jp/ref/en, for build_iso.py --tr)

Slice file format (UTF-8, no Japanese anywhere):
  {"slice": N, "rows_in_slice": n, "rows_examined": n,
   "rows": [{"id": "u0001", "en": "...", "flags": [], "notes": ""}], "report": {...}}
Every row of the slice must be present, prefilled ones included (keep or correct them).

check: ids complete; no Japanese; en non-empty unless flagged 'unfinished'; placeholders
(%s %d %c %x %02d..., {x...}) preserved; the same number of line breaks (real newlines
for EBOOT/locate text, the two characters backslash-n for menu CSV text) unless the row
is flagged 'reflow'; every character encodable in Shift-JIS (cp932), because the game
stores text in Shift-JIS; max_bytes respected for strings that must stay in place; no
glossary 'avoid' spelling. Exit 1 on any error.
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work/translation/en/ui.json")
SLDIR = os.path.join(ROOT, "work/translation/en/slices_ui")
JP = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
PH = re.compile(r"%[0-9]*[sdcxX]|\{[a-z]")


def load():
    return json.load(open(WORK, encoding="utf-8"))


def is_csv(r):
    return r["occ"][0]["ref"]["file"].startswith("data/menu/")


def show(n, ctx):
    rows = load()["rows"]
    idx = [i for i, r in enumerate(rows) if r["slice"] == n]
    lo, hi = max(0, idx[0] - ctx), min(len(rows), idx[-1] + ctx + 1)
    for r in rows[lo:hi]:
        mark = " " if r["slice"] == n else "~"
        extra = []
        if "max_bytes" in r:
            extra.append("MAX_BYTES=%d" % r["max_bytes"])
        if len(r["occ"]) > 1:
            extra.append("x%d" % len(r["occ"]))
        print("%s%s | %s | %s | %s %s" % (mark, r["id"], r["group"], r["occ"][0]["id"], r["status"], " ".join(extra)))
        print("      JP: " + r["jp"].replace("\n", "<NL>"))
        if r["en"]:
            print("      EN: " + r["en"].replace("\n", "<NL>"))


def avoid_list():
    out = []
    for f in glob.glob(os.path.join(ROOT, "work/glossary/*.json")):
        if f.endswith("gaps.json"):
            continue
        for v in json.load(open(f, encoding="utf-8")).values():
            if isinstance(v, list):
                for e in v:
                    if isinstance(e, dict):
                        for a in e.get("avoid", []) or []:
                            if a and not JP.search(a) and a not in e.get("en", ""):
                                out.append((a, e.get("en", "")))
    return out


def check(n, rows, avoid):
    errs, warns = [], []
    path = os.path.join(SLDIR, "ui_%02d.en.json" % n)
    if not os.path.exists(path):
        return ["missing " + path], []
    s = json.load(open(path, encoding="utf-8"))
    if JP.search(json.dumps(s, ensure_ascii=False)):
        errs.append("Japanese characters in slice file")
    got = {t["id"]: t for t in s["rows"]}
    want = [r for r in rows if r["slice"] == n]
    for r in want:
        t = got.get(r["id"])
        if not t:
            errs.append("%s missing" % r["id"])
            continue
        if r["status"] == "not_text":  # never inserted (build_ui.py)
            continue
        en, jp, fl = t.get("en", ""), r["jp"], t.get("flags", [])
        if not en:
            if "unfinished" not in fl:
                errs.append("%s empty en" % r["id"])
            continue
        if sorted(PH.findall(jp)) != sorted(PH.findall(en)):
            errs.append("%s placeholders %s -> %s" % (r["id"], PH.findall(jp), PH.findall(en)))
        br = "\\n" if is_csv(r) else "\n"
        if jp.count(br) != en.count(br) and "reflow" not in fl:
            warns.append("%s line breaks %d -> %d (flag 'reflow' if deliberate)" % (r["id"], jp.count(br), en.count(br)))
        if is_csv(r) and "\n" in en:
            errs.append("%s real newline in CSV text (use backslash-n)" % r["id"])
        try:
            b = len(en.encode("cp932"))
            if "max_bytes" in r and b > r["max_bytes"]:
                errs.append("%s %d bytes > max %d: %r" % (r["id"], b, r["max_bytes"], en))
        except UnicodeEncodeError as e:
            errs.append("%s not Shift-JIS encodable: %r" % (r["id"], en[e.start:e.end]))
        for a, good in avoid:
            if re.search(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", en):
                errs.append("%s uses avoided '%s' (use '%s')" % (r["id"], a, good))
    extra = set(got) - {r["id"] for r in want}
    if extra:
        errs.append("ids not in slice: %s" % sorted(extra)[:5])
    return errs, warns


def main():
    cmd = sys.argv[1]
    if cmd == "show":
        ctx = int(sys.argv[sys.argv.index("--context") + 1]) if "--context" in sys.argv else 5
        show(int(sys.argv[2]), ctx)
    elif cmd == "check":
        rows = load()["rows"]
        avoid = avoid_list()
        nums = sorted({r["slice"] for r in rows}) if sys.argv[2] == "all" else [int(sys.argv[2])]
        bad = False
        for n in nums:
            e, w = check(n, rows, avoid)
            print("slice %02d: %d errors, %d warnings" % (n, len(e), len(w)))
            for x in e:
                print("  ERROR", x)
            for x in w:
                print("  warn ", x)
            bad |= bool(e)
        sys.exit(1 if bad else 0)
    elif cmd == "merge":
        d = load()
        by = {r["id"]: r for r in d["rows"]}
        n = 0
        for f in sorted(glob.glob(os.path.join(SLDIR, "ui_*.en.json"))):
            for t in json.load(open(f, encoding="utf-8"))["rows"]:
                r = by.get(t["id"])
                if r is None:
                    print("unknown id", t["id"], f)
                    continue
                if r["status"] == "not_text":  # never translated (build_ui.py)
                    continue
                if t.get("en") and (r["en"] != t["en"] or r["status"] != "done"):
                    n += 1
                r["en"], r["flags"], r["notes"] = t.get("en", ""), t.get("flags", []), t.get("notes", "")
                if r["en"]:
                    r["status"] = "done"
        print("updated %d rows; done %d/%d" % (n, sum(r["status"] == "done" for r in d["rows"]), len(d["rows"])))
        if "--dry-run" not in sys.argv:
            json.dump(d, open(WORK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    elif cmd == "apply":
        # python tools/ui_slice.py apply <fixes.en.json> [--apply]: {"fixes":[{"id","en","why"}]}
        fixes = {f["id"]: f for f in json.load(open(sys.argv[2], encoding="utf-8"))["fixes"]}
        go, n = "--apply" in sys.argv, 0
        for f in sorted(glob.glob(os.path.join(SLDIR, "ui_*.en.json"))):
            s = json.load(open(f, encoding="utf-8"))
            ch = False
            for t in s["rows"]:
                fx = fixes.get(t["id"])
                if fx and fx["en"] != t["en"]:
                    print("%s (%s): %s\n  - %r\n  + %r" % (t["id"], os.path.basename(f), fx.get("why", ""), t["en"], fx["en"]))
                    t["en"] = fx["en"]
                    t["notes"] = (t.get("notes", "") + " | review: " + fx.get("why", "")).strip(" |")
                    ch, n = True, n + 1
            if ch and go:
                json.dump(s, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("%d rows %s" % (n, "changed" if go else "would change (dry run)"))
    elif cmd == "export":
        d = load()
        safe = {"_meta": d["_meta"], "rows": [{k: v for k, v in r.items() if k != "jp"} for r in d["rows"]]}
        if JP.search(json.dumps(safe, ensure_ascii=False)):
            sys.exit("ERROR: Japanese left in export")
        json.dump(safe, open(WORK[:-5] + ".en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        ins = []
        for r in d["rows"]:
            if r["en"]:
                for o in r["occ"]:
                    if o.get("not_text"):
                        continue
                    ins.append({"id": o["id"], "jp": r["jp"], "ref": o["ref"], "en": r["en"]})
        json.dump({"rows": ins}, open(os.path.join(os.path.dirname(WORK), "ui_insert.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("wrote ui.en.json (%d rows) and ui_insert.json (%d occurrences)" % (len(safe["rows"]), len(ins)))


if __name__ == "__main__":
    main()
