# Dialogue translation brief (v0.1.0)

Read `BASE_RULES.md` first. Its rules apply in full. This page adds what is specific to this game and this corpus.

## Input and output

- Work file: `work/translation/en/dialogue.json`. Each entry in `rows` has `row`, `id`, `cat`, `scene`, `ref` and `jp`.
- Your slice is 80 consecutive rows by `row` number. You may read the rows before and after your slice for context, and you must when a line's subject, speaker or addressee is unclear.
- **Do not edit `dialogue.json`.** Write only your slice file, `work/translation/en/slices/slice_NN.en.json`, as UTF-8 JSON:

```json
{"slice": 3, "rows_in_slice": 80, "rows_examined": 80,
 "rows": [
   {"id": "eboot:38F6A0", "en": "...", "flags": [], "notes": ""}
 ],
 "report": {"uncertain": ["row 172: ..."], "kept_omission": ["row 190: ..."],
            "missing_glossary": ["ビクター: used as 'Victor'"], "unfinished": []}}
```

- **No Japanese characters anywhere in a slice file.** The file is committed to git. Notes and reports must describe the Japanese in English. Name terms by their row number, and use romaji only when you must.
- `flags` values: `kept_omission` (you kept the source's dropped subject or verb), `uncertain` (a judgment call you want checked), `name_missing` (a name not in the glossary), `unfinished` (you could not translate the row). Leave `en` empty only for `unfinished`.

## The four kinds of text

| `cat` | What it is | How it appears |
| --- | --- | --- |
| `narration` | Prologue/epilogue narration for each era (EBOOT). One row = one line on screen; a sentence often runs over 2-4 rows. | Narrator voice: documentary, a little grand, past tense. Cut the English at the matching point when a sentence spans rows. One row in, one row out. |
| `briefing` | Mission select text: `strMission` (short objective) and `strStory` (the briefing). | Military briefing voice: crisp, imperative ("Destroy all enemy units."). `\n` (backslash-n, two characters) is a line break the game draws. Keep the same number of `\n` breaks where you can, placed at a natural point. Final wrapping is done at insertion once widths are measured, so do not cut words to fit. |
| `ingame` | Strings shown during missions: objectives and tutorial instructions (the `mt_*` files). Real newline characters are line breaks. | Objectives are imperative and short. Tutorial lines address the player directly ("Hold the L button to guard."). |
| `quote` | Player titles from the Nyan-Nyan shop (`NNSHOP_ITEM_5000-5299`). Some are epithets ("Rookie", "Ace"), many are famous character lines from the anime. | Epithets: short noun phrases in Title Case. Character lines: render them as that character would say them, in quotes-free form, at full force. Where a line has a well-known fan/official English rendering, use it: for example the Basara line "Listen to my song!" and Ranka's "Kira☆" ("キラッ☆"). |

The year in narration uses Western digits ("In July 1999, ..."). Use "A.D." only when the Japanese uses 西暦 at the start of an era's prologue ("A.D. 2040.").

## Line breaks (read carefully)

`python tools/show_slice.py <N>` prints your slice: rows marked `~` are context, and `<NL>` marks a real newline character.
- `briefing` rows contain the two characters backslash + n. Your `en` must contain the same two characters, which is `"\\n"` inside JSON.
- `ingame` rows with `<NL>` contain a real newline. Your `en` uses a real newline, which is `"\n"` inside JSON.
- Write your slice file with Python (`json.dump(..., ensure_ascii=False, indent=1)`) so escaping is correct. Then run `python tools/check_slice.py <N>`, which validates ids, line breaks, placeholders, and the absence of Japanese text and avoid-list names. Fix everything it reports.

## Text that must stay as it is

- Placeholders and codes: `%s`, `%d`, `{l...}`, `{k%s}`, `\n`, real newlines. `%s` in narration is the player's or partner's name. Do not give it a gender.
- Button symbols: ○ × △ □, and the words L button / R button (`Ｌボタン` → "L button").
- Full-width letters and digits become plain ASCII: `ＶＦ－２５Ｆ` → `VF-25F`, `ＳＰ` → `SP`, `３ブロック` → `3 blocks`.
- Commas and double quotes: write normal English. The CSV format cannot hold ASCII `,` or `"`, so the insertion tool converts them. You don't need to avoid them.

## Names

- `work/glossary/` is the authority: characters.json, organizations.json, locations.json, mecha.json, terms.json. Use `en`. Never use anything in an `avoid` list. The `ja_aliases` field maps the short forms the game uses (マックス, 早瀬中尉...) to the right person.
- Decided spellings that must not be reopened: Vrlitwhai Kridanik (the game writes ブリタイ), Quamzin Kravshera (カムジン), Milia Fallyna Jenius (ミリア; before her marriage, in the SDF era, she is "Milia Fallyna" or "Milia"), Jeffrey Wilder.
- Short forms: use the name the characters use ("Max", "Minmay", "Basara", "Alto", "Hikaru"). 統合軍 → "U.N. Forces"; 新統合軍 → "New U.N. Forces"; 反統合同盟(軍) → "Anti-U.N. Forces"; ゼントラーディ軍 → "Zentradi forces" / "the Zentradi".
- Unit names follow mecha.json. When a name is missing from the glossary, translate it as well as you can, flag the row `name_missing`, and list it in `report.missing_glossary`.

## Gender

Never infer gender from a name. Use the `gender` field in characters.json. For anyone not in the glossary, or for the player (`%s`, "the pilot"), use neutral wording.

## Quality bar (summary of BASE_RULES)

- Restore subjects and verbs that Japanese grammar drops, wherever the context settles them. Check who is asking whom before you pick an imperative.
- Translate at full strength. Do not soften threats, insults or crude lines.
- Write the full line first. Do not shorten in advance.
- Before each row, settle who is talking to whom and which line this one answers. Report any call that was not obvious in `report.uncertain`.
- Flag every row where you kept an omission (`kept_omission`).
- Report rows examined vs rows in your slice.
