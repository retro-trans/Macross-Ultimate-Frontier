# Refit brief: make overflowing lines fit (v0.5.x)

Read `BASE_RULES.md` first. The rules in "When translating dialogue" about compressing apply here: **compress the meaning or abbreviate, but never drop the end of a sentence.** If a line still does not fit, keep your best attempt and flag it. Keep the voice, the facts, the names (glossary) and the full force of the line.

## Your inputs

- Work list: `work/translation/en/review/refit_work_<group>.en.json`. `keys` are dialogue row numbers (integers) or UI row ids (`u0815`).
- See the Japanese and the current English:
  - Dialogue rows: `python tools/show_rows.py <lo> <hi>`.
  - UI rows: `python tools/ui_slice.py show <slice> --context 0`. The UI row id is in the output, and `work/translation/en/ui.json` gives the slice of an id.
- Measure: `python tools/fit_line.py <key> "<english>"`. It prints px against the limit per line, characters against max_chars, and OK or OVER. `python tools/fit_line.py --info <key>` shows the type, size and limits.
- Limits are in `docs/text_limits.md`. The main ones:
  - **mission_story** (briefing story): **2 lines at most**. Line 1 is at most 429 px and line 2 at most 415 px, at size 11. **Each line is at most 79 characters**: the game copies each line into an 80-byte slot and corrupts memory past it. The line break is the two characters backslash + n. Keep exactly one break, so two lines, unless one line holds everything.
  - **narration**: one row is one screen line, at most 468 px at size 12, and anything wider is cut off. You may move words between rows **of the same sentence** to balance them, but then you must refit and output **every** row you touched. Never merge or split rows.
  - **fes_tutorial**: up to 3 lines, each at most 309 px at size 14, with real newlines. Keep the newline count unless a line becomes empty.
  - **mission_objective**: 2 lines, at most 214 px each, at size 10. **eboot_objective / fes_objective**: at most 212 px at size 10. **eboot_help**: at most 312 px at size 12, one line.
  - **ms_desc** (unit description): line 1 is the unit name, then 2 lines, at most 434 px each at size 14. **pilot_desc**: 3 lines, at most 434 px each. These limits are the width of the original Japanese, not measured in game, so treat them as the target.
  - **Lists** (titles, bonus conditions, labels): one line, limit as reported. Several lists have unmeasured boxes. Where a limit is absurdly small for any English, such as 14–42 px, do not mangle the name: keep the shortest sensible form and flag it as `box_unmeasured`.
- Placeholders (`%s %d {..}`) stay. `%s` counts as 10 wide characters.

## Techniques, in order of preference

1. Tighter wording: drop filler ("We will now", "in order to", "Please"). Use "Destroy X" rather than "Proceed to destroy X".
2. Shorter synonyms: "eliminate" becomes "wipe out", "Anti-U.N. Forces" becomes "Anti-U.N." when the line already names them once, "U.N. Forces" becomes "U.N.".
3. Standard abbreviations: Lt., Capt., HQ, &, No., approx.
4. Restructure: merge clauses and cut repetition between the two lines (the objective line often repeats the story).

Never cut the end of a sentence. Never change who does what to whom. Keep the names spelt as in the glossary. Use the agreed term forms, for example "Annihilate all enemies" when that is the full line.

## Output

Write `work/translation/en/review/refit_<group>.fixes.en.json`. It must not contain Japanese.

```json
{"fixes": [{"row": 412, "en": "<full new English for the row>", "why": "refit: <what was compressed>"},
           {"id": "u0815", "en": "...", "why": "..."}],
 "unfit": [{"key": 413, "reason": "..."}]}
```

Dialogue rows use `"row"`; UI rows use `"id"`. Then run `python tools/fit_line.py --batch work/translation/en/review/refit_<group>.fixes.en.json` until it reports **0 still over**, or list the rest in `unfit`.

For titles (shop titles): the same title text also appears as a UI row. If you change one, find the same English in `work/translation/en/ui.en.json` and fix that row the same way.

Do not edit any other file.
