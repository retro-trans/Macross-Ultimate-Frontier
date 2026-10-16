"""Pre-translate formulaic gallery labels in work/translation/en/ui.json by rule.

Usage: python tools/prefill_rules.py [--apply]
Pattern: <work>：<kind><number>, e.g. ゼロ：キャプチャ０２９ -> "Zero: Capture 029".
Also bare <kind><number> (戦術指南書３ -> "Tactics Manual 3", オペレーター２ ...).
Only rows still "todo" are filled; they get status "rule" so a translator reviews
them. Dry run by default: prints a sample and the count.
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work/translation/en/ui.json")

WORKS = {"ゼロ": "Zero", "初代": "SDF", "愛おぼ": "DYRL", "ＦＢ": "FB2012", "プラス": "Plus",
         "７": "Macross 7", "Ｄ７": "D7", "Ｆ": "Frontier", "Ⅱ": "Macross II", "マクロス": "Macross",
         "オリジナル": "Original", "その他": "Other"}
KINDS = {"キャプチャ": "Capture", "エピローグ": "Epilogue", "プロローグ": "Prologue", "クロニクル": "Chronicle",
         "機体": "Unit", "キャラ": "Character", "戦術指南書": "Tactics Manual", "オペレーター": "Operator"}
FW = str.maketrans("０１２３４５６７８９", "0123456789")
PAT = re.compile(r"^(?:(%s)：)?(%s)([０-９0-9]*)$" % ("|".join(map(re.escape, sorted(WORKS, key=len, reverse=True))),
                                                  "|".join(map(re.escape, KINDS))))


def rule(jp):
    m = PAT.match(jp)
    if not m:
        return None
    w, k, n = m.groups()
    en = KINDS[k] + ((" " + n.translate(FW)) if n else "")
    return (WORKS[w] + ": " + en) if w else en


def main():
    apply = "--apply" in sys.argv
    d = json.load(open(WORK, encoding="utf-8"))
    hits = []
    for r in d["rows"]:
        if r["status"] == "todo":
            en = rule(r["jp"])
            if en:
                hits.append((r, en))
    for r, en in hits[:: max(1, len(hits) // 15)]:
        print(r["row"], r["jp"], "->", en)
    print(len(hits), "rows", "filled" if apply else "would be filled (dry run)")
    if apply:
        for r, en in hits:
            r["en"], r["status"], r["notes"] = en, "rule", "prefilled by tools/prefill_rules.py"
        json.dump(d, open(WORK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
