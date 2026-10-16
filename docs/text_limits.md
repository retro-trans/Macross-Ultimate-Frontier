# Text limits and the width check (2026-10-15)

`tools/check_widths.py` measures every translated English line in pixels with
the variable-width font (`docs/vwf.md`) and flags the lines that do not fit
their on-screen box.

```bash
python tools/check_widths.py limits
```

```bash
python tools/check_widths.py
```

The first command writes `work/ui/text_limits.json` from the Japanese source
dumps in `work/source/text/` (run `tools/dump_text.py` and
`tools/dump_eboot.py` first). The second command reads
`work/translation/en/*.en.json` (or the files you name), writes
`work/ui/width_report.md` and `work/ui/width_report.json`, and exits with 1
if any line is over. `--all` also lists the lines that fit, and `--out DIR`
writes the report somewhere else. Inputs need only `id` and `en`, so new UI
translation files can be checked the same way.

## How a line is measured

- ASCII 0x20–0x7E uses the VWF advance from `work/output/vwf/vwf_widths.json`.
  At font size s the advance is `s - round((14 - adv) * s / 14)`.
- Every double-byte character (kana, kanji, full-width Latin, `○ × △ □ ☆ …`)
  is s px wide.
- A character Shift-JIS cannot encode (for example `ō`) is reported as
  `unencodable`. The game cannot show it.
- `{x...}` codes count as their contents. `%s` counts as 10 double-byte
  characters (a player or partner name; the longest default name is 10) and
  `%d` as `999`. Both are set in `placeholders` in the limits file.
- Lines break at a real newline and at the CSV's literal `\n`.

## How a limit is set

The limit of a text type is its widest original Japanese line, at the size the
game draws that type. The unpatched game drew double-byte characters at s px
and single-byte at 0.75 × s px. Where the in-game box is known, it is recorded
with `box` (x, y, w, h in native 480×272 px), `evidence` and
`confirmed: true`. Where the box is wider than the Japanese ever used,
`limit_override` sets the real box width.

Hand-set fields (`size`, `limit_override`, `line_limits`, `max_lines_override`,
`box`, `confirmed`, `evidence`, `note`) survive a rerun of `limits`.

Unconfirmed types keep size 14. The VWF advance scales with the size, so the
verdict for those types changes only by rounding once the real size is known.

EBOOT strings:

- The narration and the help bar have their own types.
- The mission records (0xB0 bytes each, vaddr 0x2DA000–0x2E6000) are typed by
  field: +0x00, +0x04 and +0xAC are objectives, +0x3C–0x44 are bonus
  conditions, and +0x9C is the mission name.
- Other strings in a pointer list share the list's limit (`eboot_list:<vaddr>`).
  A list is a field across a struct array, or a run of 4 or more pointers.
- Strings in no list are held to their own Japanese width. The report marks
  these as `soft`, because the real box may be wider.

## Boxes measured in game

Measured in PPSSPP 1.20.4 on the original disc. Labelled screenshots are in
`work/output/ui_screens/`. That folder is gitignored because the screenshots
show Japanese script.

| Type | Where | Size | Box (x, y, w, h) | Limit |
| --- | --- | --- | --- | --- |
| `eboot_help` | Bottom help bar, centred | 12 | 95, 236, 290, 16 | 312 (Japanese max; the frame is 290 inside, and text far too wide scrolls) |
| `narration` | Era prologue/epilogue, centred, up to 5 lines | 12 | 6, 190, 468, 80 | 468 (screen 480) |
| `mission_story` | Campaign mission screen, 2 lines | 11 | 7, 196, 465, 28 | line 1: 429, line 2: 415 (the launch button starts at x=424) |
| `mission_objective` | Mission list, "Mission Information" panel, 2 lines | 10 | 248, 134, 214, 26 | 214 (the box; the Japanese max is 190) |
| `fes_objective`, `eboot_objective` | Orange objective strip (mission list and pause screen) | 10 | 248, 118, 212, 13 | 212 (the box; the Japanese max is 160) |
| `fes_tutorial` | Tutorial "Information" box at the top, centred, up to 3 lines (v0.2.0 build) | 14 | 84, 22, 309, 48 | 309 (the frame inside; the Japanese max is 308) |

Not confirmed yet, so these keep the Japanese maximum at size 14:

- the shop and ID-card lists (`nn_*`)
- unit, pilot and pack descriptions
- mission names, bonus conditions and the other EBOOT lists

The player name box on the character screen is size 12. The default names are
up to 10 characters.

## What the game does with text that is too long (v0.2.0 test build)

Seen in PPSSPP 1.20.4 with the English inserted. Screenshots, with the boxes
drawn on (`*_labelled.png`), are in `work/ui/screens_0.2.0/`; the boxes are
listed in `screens.json` there.

| Type | Too wide | Other limit |
| --- | --- | --- |
| `mission_story` | The line is squeezed horizontally to fit the panel. It stays on screen but gets narrower. | **79 characters per line.** Each line is copied into an 80-character slot without a bounds check. MA_010 line 1 has 92 characters: the game showed its first 80, then all of line 2 on the same row, and line 2 again below. A long last line writes past its slot into memory the game uses for something else. |
| `narration` | Centred; anything beyond the 480 px screen is cut off at both edges. | |
| `fes_tutorial` | Centred; the text runs past the frame on both sides, over the 3D view. Not cut. | |
| `mission_objective` | Not seen yet (the lines tested fitted). | |

The width checker agrees with the screen to within 3 px (tutorial: 373
predicted, 372 measured; narration: 425 and 422.5).

`check_widths.py` takes a `max_chars` field per type in `text_limits.json`
(set to 79 for `mission_story`) and reports a line over it as `chars`.

## Result on the 0.2.0 dialogue (1,187 rows, 1,776 lines)

503 lines are over (rerun with the v0.2.0 boxes):

| Type | Over | Rows |
| --- | --- | --- |
| `mission_story` | 323 of 432 lines: 289 too wide and over 79 characters, 16 only too wide, 18 only over 79 characters | 198 of 216 missions |
| `narration` | 56 of 223 (51 of them wider than the 480 px screen, so cut) | 56 |
| `nn_title` | 44 of 300: 43 too wide (box not confirmed), 1 unencodable (`ō`, inserted as `ou`) | 44 |
| `mission_objective` | 40 of 389 | 40 |
| `fes_tutorial` | 39 of 341 | 34 |
| `fes_objective` | 1 of 91 | 1 |

The briefing stories are the main problem. The English runs up to 1.8 times
the box and up to 140 characters per line, and the panel shows two lines.
Lines over 79 characters corrupt the display (and line 2 overwrites memory
past its slot), so these have to be reworded before a release, or the
line-copy routine patched to allow longer slots (not investigated). Per
BASE_RULES nothing has been cut: the list is in `work/ui/width_report.md`.
