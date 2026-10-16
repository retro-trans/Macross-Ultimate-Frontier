"""Replace glossary 'avoid' spellings with the canonical English in translations.

Usage: python tools/fix_names.py [--apply]
Without --apply this is a dry run: it prints every row it would change, with
before/after, so the change can be read before it touches the data.
Matching is case-sensitive and whole-word. Run AFTER agent fixes are merged
(BASE_RULES: agents first, name script last).
"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work/translation/en/dialogue.json")
JP = re.compile(r"[぀-ヿ㐀-鿿]")


def pairs():
    out = []
    for f in glob.glob(os.path.join(ROOT, "work/glossary/*.json")):
        if f.endswith("gaps.json"):
            continue
        for v in json.load(open(f, encoding="utf-8")).values():
            if not isinstance(v, list):
                continue
            for e in v:
                if isinstance(e, dict) and e.get("en"):
                    for a in e.get("avoid", []) or []:
                        # skip variants that are part of the canonical form (e.g. Milia inside Milia Fallyna)
                        if a and not JP.search(a) and a not in e["en"]:
                            out.append((a, e["en"]))
    return sorted(out, key=lambda p: -len(p[0]))


def main():
    apply = "--apply" in sys.argv
    d = json.load(open(WORK, encoding="utf-8"))
    n = 0
    for r in d["rows"]:
        en = r["en"]
        for a, good in pairs():
            en = re.sub(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", good, en)
        if en != r["en"]:
            n += 1
            print("row %d %s\n  - %s\n  + %s" % (r["row"], r["id"], r["en"], en))
            if apply:
                r["en"] = en
    print("%d rows %s" % (n, "changed" if apply else "would change"))
    if apply and n:
        json.dump(d, open(WORK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
