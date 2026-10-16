"""Translate the internal (designer-only) unit-list labels in data/locate/*.csv.

Usage: python tools/build_internal_labels.py [--dry-run]
These 51 distinct labels (216 rows) are demo, portrait and dummy entries ("デモ用バサラ",
"顔絵用ランカ", "削除"). They are probably never shown, but they sit in the display-name
column, so they get plain English too. Writes work/translation/en/internal_labels.json
(rows with id/jp/ref/en for insert_text.py; gitignored) and internal_labels.en.json
(no Japanese).
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNAL = re.compile(r"デモ用|顔絵用|ダミー|^削除$|テスト|予定")
NAMES = {"艦長マックス": "Captain Max", "シビル": "Sivil", "バサラ": "Basara", "ファイターバトル７": "Fighter Battle 7",
         "MSバトル７": "Battle 7 (Unit)", "ビヒーダ": "Veffidas", "ギギル": "Gigile", "オクトス": "Octos", "鳥の人": "Bird Human",
         "空母アスカ": "Carrier Asuka", "プロトモンスター": "Prototype Monster", "ターゲット": "Target", "ガムリン": "Gamlin",
         "ドッカー": "Docker", "マックス": "Max", "ゼントラ兵１": "Zentradi Soldier 1", "ゼントラ兵２": "Zentradi Soldier 2",
         "ゼントラ兵1": "Zentradi Soldier 1", "ゼントラ兵2": "Zentradi Soldier 2", "ゼントラ兵3": "Zentradi Soldier 3",
         "ゼントラ兵4": "Zentradi Soldier 4", "ゼントラ兵5": "Zentradi Soldier 5", "クォーター": "Macross Quarter", "ルカ": "Luca",
         "ブレラ": "Brera", "バジュラ艦": "Vajra Ship", "ミハエル": "Michael", "アルト": "Alto", "ブレラ１（バトロイド）": "Brera 1 (Battroid)",
         "ブレラ２（ファイター）": "Brera 2 (Fighter)", "バジュラ大型母艦": "Large Vajra Mothership", "ピクシー小隊": "Pixie Team",
         "オズマ": "Ozma", "アスカ": "Asuka", "シェリル": "Sheryl", "ランカ": "Ranka", "シェリルパイスー": "Sheryl (Pilot Suit)",
         "ランカパイスー": "Ranka (Pilot Suit)"}
FIXED = {"デモ用": "Demo", "削除": "Deleted", "フェイス用ダミー": "Face Dummy", "シェリル用ダミー": "Sheryl Dummy",
         "デモ用兼ランカダミー": "Demo / Ranka Dummy", "ジェフリー用ダミー": "Jeffrey Dummy", "カメラ用ダミー": "Camera Dummy",
         "顔絵用ダミー": "Portrait Dummy", "顔絵用ダミー(シェリル)": "Portrait Dummy (Sheryl)", "顔絵用ダミー（グレイス）": "Portrait Dummy (Grace)",
         "D・イーター用ダミー": "D-Eater Dummy", "主砲範囲テスト": "Main Gun Range Test", "搭乗者ミュン予定": "Pilot: Myung (Planned)",
         "フォールドデモ用ファイターバトル７": "Fold Demo: Fighter Battle 7"}


def en_for(jp):
    if jp in FIXED:
        return FIXED[jp]
    for pre, tag in (("デモ用", "Demo: "), ("顔絵用", "Portrait: ")):
        if jp.startswith(pre) and jp[len(pre):] in NAMES:
            return tag + NAMES[jp[len(pre):]]
    return None


def main():
    loc = json.load(open(os.path.join(ROOT, "work/source/text/locate_names.json"), encoding="utf-8"))
    rows, missing = [], set()
    for x in loc:
        if not INTERNAL.search(x["jp"]):
            continue
        en = en_for(x["jp"])
        if en is None:
            missing.add(x["jp"])
            continue
        rows.append({"id": "locate:" + x["id"], "jp": x["jp"], "en": en,
                     "ref": {"file": x["source"], "row": x["row"], "col": x["col"], "key": x["key"]}})
    print("rows %d, distinct %d, untranslated %d" % (len(rows), len({r["jp"] for r in rows}), len(missing)))
    for m in sorted(missing):
        print("  missing", m)
    if "--dry-run" in sys.argv or missing:
        for r in rows[:8]:
            print(" ", r["jp"], "->", r["en"])
        return
    out = os.path.join(ROOT, "work/translation/en/internal_labels.json")
    json.dump({"rows": rows}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"rows": [{k: v for k, v in r.items() if k != "jp"} for r in rows]},
              open(out[:-5] + ".en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", out, "and .en.json")


if __name__ == "__main__":
    main()
