"""Measure candidate English against its on-screen box (wraps tools/check_widths.py).

Usage:
  python tools/fit_line.py <key> "<english>"        one candidate
  python tools/fit_line.py --batch <fixes.json>      every fix in a fix file
  python tools/fit_line.py --info <key>              type, size, limits, Japanese width

<key> is a dialogue row number ("412"), a UI row id ("u0815", checked at every place
it is used), or an occurrence id ("mission_ext:MA_010:strStory", "eboot:38F6A0").
Fix files use the apply_fixes / ui_slice apply format:
  {"fixes": [{"row": 412, "en": "..."}, {"id": "u0815", "en": "..."}]}

Line breaks: real newlines, or the two characters backslash-n in CSV text.
Output per line: px / limit, characters / max_chars, and OK or OVER (width, lines,
chars, unencodable). "soft" means the limit is only the Japanese width (box unknown).
Exit code 1 if anything is over.
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_widths as cw  # noqa: E402

SRC = cw.Source()
LIM = cw.Limits(cw.load_json(cw.LIMITS), SRC)
DIA = {r["row"]: r["id"] for r in json.load(open(os.path.join(ROOT, "work/translation/en/dialogue.json"), encoding="utf-8"))["rows"]}
UI = {r["id"]: [o["id"] for o in r["occ"]] for r in json.load(open(os.path.join(ROOT, "work/translation/en/ui.json"), encoding="utf-8"))["rows"]}


def occ_ids(key):
    key = str(key)
    if key.isdigit():
        return [DIA[int(key)]]
    if key in UI:
        return UI[key]
    return [key]


def measure(oid, en):
    """List of (line no, type, px, limit, chars, max_chars, issues, soft) for one occurrence."""
    if oid not in SRC.type:
        return None
    jp = cw.jp_lines(SRC.jp[oid])
    lines = cw.split_lines(en)
    lts = SRC.line_types(oid, max(len(lines), len(jp)))
    per, out = {}, []
    for i, line in enumerate(lines):
        lt = lts[i]
        per[lt] = per.get(lt, 0) + 1
        label, size, limit, max_lines, soft = LIM.for_line(oid, lt, per[lt], jp[i] if i < len(jp) else None)
        w, bad = cw.line_width(line, size, LIM.placeholders)
        mc = LIM.types.get(label, {}).get("max_chars")
        n = len(cw.expand(line, LIM.placeholders))
        issues = [k for k, v in (("width", w > limit), ("lines", per[lt] > max_lines),
                                 ("chars", bool(mc) and n > mc), ("unencodable", bool(bad))) if v]
        out.append((i + 1, label, size, w, limit, n, mc, issues, soft))
    return out


def report(key, en):
    ok = True
    for oid in occ_ids(key):
        m = measure(oid, en)
        if m is None:
            print("  %s: not in the source dumps (not measurable)" % oid)
            continue
        for ln, label, size, w, limit, n, mc, issues, soft in m:
            ok &= not issues
            print("  %-34s L%d %-18s %5.1f/%-5.1f px  %3d%s chars  %s%s" % (
                oid[:34], ln, label[:18], w, limit, n, ("/%d" % mc) if mc else "", "OVER " + ",".join(issues) if issues else "OK",
                " (soft)" if soft else ""))
    return ok


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "--info":
        for oid in occ_ids(a[1]):
            t = SRC.type.get(oid)
            print(oid, "type:", t, "| jp:", SRC.jp.get(oid, "")[:60].replace("\n", "/"))
            m = measure(oid, SRC.jp.get(oid, "x"))
            if m:
                for ln, label, size, w, limit, n, mc, issues, soft in m:
                    print("  L%d %s size %d limit %.1f px max_chars %s soft %s" % (ln, label, size, limit, mc, soft))
        return
    if a[0] == "--batch":
        fixes = json.load(open(a[1], encoding="utf-8"))["fixes"]
        bad = 0
        for f in fixes:
            key = f.get("row", f.get("id"))
            print("%s:" % key)
            if not report(key, f["en"]):
                bad += 1
        print("%d of %d fixes still over" % (bad, len(fixes)))
        sys.exit(1 if bad else 0)
    sys.exit(0 if report(a[0], a[1]) else 1)


if __name__ == "__main__":
    main()
