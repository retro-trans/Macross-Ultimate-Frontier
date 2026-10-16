# Dialogue translation (v0.2.0, 2026-10-15)

## What "dialogue" covers in this game

The in-mission radio conversations are **voice only**. No subtitle text exists
in the archives or in the decrypted EBOOT (the `.vad` files paired with the
voice clips are 48-byte lip-sync data). Every story or dialogue line the game
shows as text is in the work file below, and all of it is translated:

| Category | Source | Rows | What it is |
| --- | --- | --- | --- |
| `narration` | EBOOT 0x38F6A0–0x3927F0 | 223 | Prologue and epilogue narration for every era (SDF, DYRL, Zero, Plus, 7, Dynamite 7, Frontier) |
| `briefing` | `data/menu/text/mission_ext.csv` | 432 | Mission objective and briefing story for 216 missions, including Ranka/Sheryl tutorial briefings and Basara's speech |
| `ingame` | `data/script/*.fes` string pools | 232 | Objectives shown during missions and the tutorial instructions |
| `quote` | `data/menu/text/nn_ext.csv` 5000–5299 | 300 | Nyan-Nyan shop player titles; about half are famous character lines |
| **total** | | **1,187** | 1,187 translated, 0 unfinished |

Not covered here, and still to do: UI and menu text (the EBOOT menus, unit,
pilot and pack descriptions, the rest of `nn_ext.csv`), and text drawn into
GIM images.

## Files

- `work/translation/en/dialogue.json`: the work file, with Japanese (gitignored). It is rebuilt by `tools/build_dialogue.py`, which keeps the existing English.
- `work/translation/en/dialogue.en.json`: the committed copy without Japanese (`tools/strip_jp.py`).
- `work/translation/en/slices/slice_01..15.en.json`: translator output, 80 rows each. **These are the source of truth**; `tools/merge_slices.py` copies them into the work file.
- `work/translation/en/review/*.en.json`: the review fixes that were applied (consistency, names, four meaning-proofreading passes A–D, final).
- `docs/translation_brief.md`: the rules the translators followed.

## Process that was run

1. 15 translator agents, one per 80-row slice. Each reported rows examined against rows in its slice (all slices complete), its uncertain calls and missing names.
2. Consistency pass. Identical Japanese lines must have identical English: 9 groups (23 rows) were unified, including the stock objectives "Annihilate all enemies" and "Shoot down the enemy ace", and the repeated tutorial lines.
3. Name pass. Purple Flight, Love Drifts Away, the matching lisp in rows 923/1137, and the split of 新統合軍 "New U.N. Forces" from 新統合宇宙軍 "New U.N. Spacy".
4. Four meaning proofreaders covered all 1,187 rows (A 1–300, B 301–655, C 656–960, D 961–1187) and found 20 fixes. One more fix was made at review (row 429).
5. The name script `tools/fix_names.py` ran last, as BASE_RULES requires: 0 avoid-list spellings left.
6. `tools/check_slice.py all`: 0 errors. The one warning is row 601, where the source has a typo (a full-width "￥ｎ" instead of a line break) that the English replaces with a real break.

## Conventions that were set (also in the glossary)

- Speaker labels in briefings use `Name: "..."`. Continuation lines are indented with ASCII spaces under the opening quote; the indent may need tuning at insertion.
- Army-style ranks: Lieutenant (中尉), Captain (大尉), Major (少佐). Misa is "Lieutenant Hayase" and later "Captain Hayase"; Roy is "Major Focker" in the Zero briefings too.
- Tutorial terms: D-pad (directions capitalised: Up/Down/Left/Right), analog stick, Special Maneuvers, Charge Shot/Melee/Boost, multi-lock-on, lock-on level.
- Gavil's `<X>美` → "<X> Beauty!". Basara's line → "Listen to my song!!". Ranka → "Kira☆".
- Commas and double quotes are written normally. The CSV cannot hold ASCII `,` or `"`, so **the insertion tool must convert them**.

## Open points for review

- 132 rows still carry the translators' `uncertain` flag. The proofreaders checked them and accepted the choices; the notes on each row say what the call was.
- 1 row is flagged `kept_omission`: row 1104, "Ah... it's connected...", where the source leaves the subject unsaid.
- Speaker unknown: rows 922 "Gojappe" (romanised Ibaraki dialect), 1137/1138, and 1014/1018.
- Rows 970 and 1064 are both "Listen to my song!!" (Basara and Sheryl). The source lines differ only in the pronoun. They could be told apart if the shop list needs it.
- Row 746/855 says "until the boost gauge is full". This needs checking in game; it would be "runs out" if the gauge drains.
- Line widths are measured by `tools/check_widths.py` (`docs/text_limits.md`). With the boxes confirmed in the v0.2.0 build, 503 of 1,776 lines are over their box or the 79-character briefing line limit, most of them briefing stories. The list is in `work/ui/width_report.md`. No row has been refitted yet.
- Row 135 (`%s and %s`) is shared by two epilogues (see `docs/formats.md`).

## Insertion (v0.2.0 test build)

All 1,187 rows are in the game: `python tools/build_iso.py 0.2.0` makes
`work/output/Macross Ultimate Frontier (EN v0.2.0).iso` (`docs/build.md`). In
PPSSPP 1.20.4 it shows English briefings, mission objectives, tutorial lines
and the prologue narration; the epilogue text was checked through a debug ISO.
Screenshots: `work/ui/screens_0.2.0/`.

Before a release, the over-long lines must be reworded
(`work/ui/width_report.md`, summary in `docs/text_limits.md`). Most urgent:
briefing story lines over 79 characters (191 missions), which the game
corrupts on screen.
