# Glossary vs game text (first check, 2026-10-15)

`tools/glossary_check.py` matched glossary v0.1.0 against the names in the
dumped game text (`tools/dump_text.py`). The full list, with the text ids where
each name was seen, is in `work/glossary/gaps.json`. This page lists the
points to act on. Names stay in Japanese here because no English form has been
decided yet.

What the check covered: the 5 menu-text CSVs, the mission-script objectives
and the mission unit lists. It did not cover the EBOOT (encrypted) or text
drawn in images, so "not in the text" does not prove a name is unused.

| | exact | variant | partial | gap |
| --- | --- | --- | --- | --- |
| characters | 72 | 26 | 18 | 52 |
| mecha / packs | 105 | 125 | 12 | 22 |
| organizations (mined from prose, noisy) | 11 | 4 | 8 | 16 |
| objects / places (mission unit lists) | 0 | 0 | 1 | 19 |

## 1. Spellings where the game differs from the glossary

The glossary's Japanese form is not the one the game uses. Check the English
spelling too.

| Game | Glossary | Note |
| --- | --- | --- |
| ギリアム・アングレート | ギリアム・アングリット | The game's reading. Fix the glossary's `ja`. |
| ボドル・ザー / ボドルザー | ゴル・ボドルザー | Mission text splits the name differently. Add as aliases. |
| ミリア・ファリーナ | ミリア・ファリーナ・ジーナス | Pre-marriage name, used for SDF-era Milia (25×). It needs its own English form or an alias. |
| Ａｚ－１３０Ａ パンツァーゾルン | Az-130 パンツァーゾルン | The game uses the model code Az-130**A**. |
| ゴーストＸ－９ / ゴーストＶ－９ | X-9 ゴースト / AIF-9V ゴーストV9 | Word order differs. Decide the English form. |
| シャイアンⅡ | ADR-03-MK-III シャイアン | A separate unit (Cheyenne II) is missing. |
| マクロス ダイダロスタイプ | ダイダロスタイプ | |

## 2. Characters missing from the glossary

Named people (seen in mission unit lists, briefings or the shop):

- カナリア・ベルシュタイン (8×, also カナリア 4×)
- トーマ・シュン, マンフレート・ブランド, フィジカ・S・ファルクラム,
  マシュー・ラングレー, マリア・ベラスケス・ホイリー, ヘンリー・ギリアム,
  スージー・ニュートレット
- イリーナ 早川, オルテック, マシューズ, ディック, モーリー (Macross 7 missions)
- スコット, 神楢, ネピアス (shown together as one unit, Macross 7)
- カリバ, オイグル, テムジン, クロレ, ガビグラ, マルヤマ, ジュン
- シモン, ヨハネ, ペテロ (Macross F missions)
- Full Zentradi designations: ミリア639, ワレラ25258, ロリー28356,
  コンダ88333, カムジン03350, ブリタイ７０１８. The glossary has only the
  short forms.
- Cameo units in `me_170` / `me_180`: さくたろう, アツゴロウ, 西岡編集長,
  バサラ佐藤, ブンブン丸, カミカゼ長田, 浜村通信. These look like
  magazine-staff cameos (the org list also has 編集戦隊デンゲキＶ). Research
  needed.

Short forms and ranks the game uses: add them as Japanese aliases so
translators map them to the right English short name. マックス, マックス艦長,
早瀬, 早瀬中尉, 一条, ミンメイ, ランカ, シェリル, アルト, ミハエル, ガムリン,
ミレーヌ, レイ, ビヒーダ, カムジン, カイフン, ミリア.

Not people, but missing as terms: ゼントラーディ兵士, 民間人, エイフォス /
エイフォスの欠片, 青い風, アスカⅡ / 空母アスカⅡ.

## 3. Mecha and objects missing

汎用空母, ミサイル駆逐艦, キャッツアイ, 連絡シャトル, 宇宙空母アームド,
空戦ポッド, バトルポッド, 重攻撃機, 反応弾, ＶＦ－２５ 一般機, 巨大ランカ,
ミンメイ人形, バジュラ空母, バジュラ女王, バジュラ大型母艦, plus the
generic mission objects (基地, 工場, コンテナ, ジェネレーター, マイクローン装置,
ターゲット, 捜索ポイント, 回収地点, パーツBOX, 反応エンジン).

## 4. Organizations, operations and terms missing

ブリタイ艦隊, 反統合軍 (the game also writes 反統合同盟軍), サジタリウス小隊,
第１１７調査船団, 私設特務軍, ゾラ星パトロール隊 (glossary: ゾラ・パトロール),
イリーナ隊, スピリチア・ファーム・プロジェクト, スーパー・ノヴァ計画,
オペレーションスターゲイザー, ミンメイ・アタック, バトロイド・アタック,
スピリチア再生種族, 巨大異星人艦隊 / 地上部隊.

The game says 統合軍 (54×) far more often than the full 地球統合軍, and
ゼントラーディ軍 / メルトランディ軍 / マルドゥーク軍 rather than the bare
names.

## 5. Glossary entries never seen in the dumped text

33 characters (among them マオ・ノーム, エキセドル・フォルモ, クローディア・ラサール,
ヴァネッサ・レイアード, 松浦ナナセ, レオン・三島, エルモ・クリダニク) and 8 units
(ゴルグ・ガンツ・チャーツ, バジュラクィーン, 空母級バジュラ艦...). They may appear
in the EBOOT or in images only. Re-check them once those are dumped. See
`*_unused_glossary` in `gaps.json`.
