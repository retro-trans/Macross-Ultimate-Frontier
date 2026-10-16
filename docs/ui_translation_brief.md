# UI and remaining-text translation brief (v0.3.0)

Read `BASE_RULES.md` and `docs/translation_brief.md` first. Their rules on names, gender, placeholders and full strength apply here too. This page adds what is different for the remaining text: menus, system messages, help lines, skills, titles, unlock messages, gallery labels, song credits, unit/weapon names, unit descriptions, pilot profiles, pack descriptions and mission unit names.

## Work file and output

- `work/translation/en/ui.json`: **one row per distinct Japanese string**. A row lists every place the string occurs (`occ`), so you translate it once. Rows are in the game's own order, so nearby rows are the same menu or list: use them for context.
- `python tools/ui_slice.py show <N> --context 10` prints your slice. `~` marks context rows and `<NL>` a real newline. `MAX_BYTES=n` marks a string that must stay in place (the pilot table and a few fixed buffers). `xK` means the string is used K times.
- Some rows are prefilled. `status: tm` means copied from the dialogue translation; `status: rule` means a gallery label built by a script ("Zero: Capture 029"). Review them: keep them, or correct them if they are wrong.
- Write `work/translation/en/slices_ui/ui_NN.en.json` (NN = your slice, two digits) with Python `json.dump(..., ensure_ascii=False, indent=1)`. Include **every** row of your slice, prefilled ones too:

```json
{"slice": 3, "rows_in_slice": 189, "rows_examined": 189,
 "rows": [{"id": "u0412", "en": "...", "flags": [], "notes": ""}],
 "report": {"uncertain": [], "missing_glossary": [], "unfinished": []}}
```

- No Japanese anywhere in the slice file. It is committed to git.
- Then run `python tools/ui_slice.py check <N>` and fix every ERROR.
- Flags: `uncertain`, `name_missing`, `unfinished`, and `reflow`. Use `reflow` when you deliberately change the number of line breaks.

## Character set

The game stores text in **Shift-JIS**. Use plain ASCII wherever you can. These are also allowed and are kept as they are: `…` `☆` `♪` `×` `○` `△` `□` `→` `←` `↑` `↓` and the special icon glyphs such as `⑳` (it draws the "Duo" logo after "Memory Stick"; write "Memory Stick⑳"). Do not use `é`, `ō`, em dash `—` or other characters that are not in Shift-JIS; the checker rejects them. Use `-` or `--` instead of a dash.

## Style for UI text

- **Concise.** Menu labels, buttons, unit and skill names are short Title Case ("Save Data", "Tune Points", "Partner"). The boxes are small, and BASE_RULES says not to hesitate to abbreviate: "Pts", "HP", "SP", "Lv.", "No.", "Atk", "Def". System messages and help lines are full sentences in plain language ("Save the data?", "Do not remove the Memory Stick or turn off the power.").
- **Consistency.** The same Japanese term must get the same English across the whole game. Before inventing a term, check `work/glossary/terms.json` (game_system, skills, songs, works) and `mecha.json`.
- **Unit names** follow `mecha.json` and its `conventions`. `（一条機）` / `一条機` means the pilot's personal unit: "VF-1J Valkyrie (Hikaru)". Packs: "Super Pack", "Armored Pack" and the others in the list.
- **The first line of a unit description** (`ms_ext.csv`) or pack description (`pack_ext.csv`) is its display name: use the mecha.json name.
- **Pilot profiles** (`pilot_ext.csv`) end with the voice actor, `（ＣＶ：name）`. Write `(CV: Given Family)` with the standard romanised name of the real person ("(CV: Yuichi Nakamura)"). If you are not sure of a reading, flag `uncertain`.
- **Song credits:** `作品` → "Series", `歌` → "Vocals", `作詞` → "Lyrics", `作曲` → "Music", `編曲` → "Arrangement". Real people's names are romanised given name first ("Yoko Kanno"). Artist names written in Latin letters stay as they are ("May'n", "Gabriela Robin", "FIRE BOMBER"). Song titles follow terms.json `songs`.
- **Pilot table** (`MAX_BYTES`): names as in characters.json `en`, short form if it does not fit. Skill and title names there must also fit.
- **Mission unit names** (`locate` rows) are labels such as `柿崎 速雄/VF-1A(HK)`. Translate the Japanese name and keep the part after `/` exactly as it is ("Hayao Kakizaki/VF-1A(HK)").
- **Placeholders and codes** stay exactly as they are: `%s %d %02d %c`, `{l...}`, `{k%s}`, `{p%s}`, `{c%s}`, `{t［%s］}`, `{s［%s］}`. The full-width brackets inside a code, `［` `］`, also stay. Translate only the words inside or around the code.
- **Test or debug strings** ("実験用ミッション03", AI profile labels like "ザコ用射撃１格闘１攻撃力２"): translate them plainly ("Test Mission 03", "Grunt: Shot 1 Melee 1 Atk 2"). They are harmless.

## Report

Rows examined vs rows in slice, your uncertain calls, names or terms missing from the glossary, and the check result. No Japanese in the report.

## Text drawn into images (GIM textures)

`tools/gim.py` decodes the game's GIM textures to PNG. They are in `work/ui/gim_png/<folder>/` (gitignored): one PNG per texture, named after its path with `__` for `/` (a `.gfp` pack adds `_NN`), plus contact sheets `_sheet_NNN.png` (24 per sheet, with file names). Use the Read tool to view a PNG.

Job: find **every** texture that shows Japanese, transcribe the Japanese exactly, and give the English for the redraw.

- Look at every contact sheet in your folders, and open the full PNG of every texture that might contain Japanese, since thumbnails are small.
- Report Japanese only: kana and kanji, and full-width text that reads as Japanese. Ignore English text already in the art ("ATTENTION", "YES"), the official series logos (the "マクロス7" and "MACROSSⅡ" title logos are kept as they are), and pictures with no text.
- Black/white or on/off variants (`_b` / `_w`, `_on` / `_off`) are separate textures. List each one, with the same English.
- English must fit the drawn area. Give the texture size and keep the English as short as the Japanese box allows ("Mission Suspended" or "Suspend"). For buttons and labels, match the glossary and UI terms (`work/translation/en/ui.en.json` has the menu text already translated; reuse its wording for the same term).
- Write `work/translation/en/images/img_<group>.json` (this file may contain Japanese and is gitignored):

```json
{"group": "...", "folders": ["menu_system", "..."], "sheets_viewed": 12, "textures_with_japanese": 31,
 "rows": [{"png": "menu_system/common_p_m_2d_b.gim.png", "file": "data/menu/system/common_p_m_2d_b.gim",
           "size": [128, 16], "jp": "２Ｄ表示切替", "en": "2D Display", "kind": "button label",
           "style": "white bold on transparent", "notes": "", "flags": []}]}
```

  `file` is the path in `work/source/dat/` (for `.gfp`, add `#NN`). `kind` is one of: button label, menu title, banner, caption, message, map label, cockpit HUD, other. `style` is a short description of how the text is drawn, for the redraw. Use the flag `uncertain` when you can't read the Japanese for sure.
