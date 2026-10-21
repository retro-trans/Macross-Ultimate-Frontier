# Variable-width font (VWF)

English text in the game is written as single-byte ASCII. Unpatched, the game
draws each ASCII byte with a full-width glyph, squeezed to 80 % and spaced 75 %
of a cell apart: about 10 px per letter, whatever the letter. The VWF patch
gives ASCII its own proportional glyphs, drawn at 4x and downsampled, and a
per-character advance in every routine that draws, measures, centres or cuts
text.

Status (2026-10-15): it works in PPSSPP 1.20.4. The following were checked
in-game:
- The menu help bar (English from `mission_ext.csv`), centred correctly.
- Title-screen copyright digits mixed with Japanese.
- Menu values ("ON", "LIMIT"), centred.
- A lock-on label set to "Roy Focker" in a test build. This is the second
  text path, with the outline drawer.
- Japanese text unchanged.

The patch has not been tried on real hardware.

## Build

```bash
python tools/vwf_build.py
```

This reads the original decrypted EBOOT (`work/source/eboot/EBOOT.dec.bin`)
and the extracted font (`work/source/dat/data/extra/gpsp3_font14.fnt`). It
writes to `work/output/vwf/` (gitignored):

| File | What |
| --- | --- |
| `PSP_GAME/SYSDIR/EBOOT.BIN` | patched decrypted EBOOT (8 bytes longer: one new relocation) |
| `data/extra/gpsp3_font14.fnt` | font with the 96 English glyphs |
| `vwf_widths.json` | glyph slots, codes and advance per character |
| `vwf_preview.png` | sample lines laid out like the game does |

The patch checks every original instruction it replaces, so it must run on the
**original** EBOOT. Apply it before `tools/eboot_insert.py`, which accepts any
decrypted EBOOT through `--eboot`.

A test disc:

```bash
python tools/muf_archive.py repack work/source/dat work/output/vwf/USRDIR --base work/source/iso/PSP_GAME/USRDIR --overlay work/output/vwf
```

```bash
python tools/iso_patch.py "Macross Ultimate Frontier (Japan).iso" work/output/vwf_test.iso PSP_GAME/SYSDIR/EBOOT.BIN=work/output/vwf/PSP_GAME/SYSDIR/EBOOT.BIN PSP_GAME/USRDIR/fileset.dat=work/output/vwf/USRDIR/fileset.dat PSP_GAME/USRDIR/macross.dat=work/output/vwf/USRDIR/macross.dat PSP_GAME/USRDIR/macross.idx=work/output/vwf/USRDIR/macross.idx
```

The font sits in both `macross.dat` and `fileset.dat`; the overlay replaces
both copies. `iso_patch.py` leaves the rest of the image byte-identical, and
files that grow are appended at the end.

## The 14 px font

`data/extra/gpsp3_font14.fnt` (341,824 bytes, no header) is a 448 px wide
4 bpp texture: 32 cells of 14×14 per row, 109 rows. Each 4-bit pixel holds
**two** 2 bpp glyphs. Bits 0–1 belong to the even glyph number, bits 2–3 to the
odd one, and cell = glyph >> 1. The drawer picks the layer with the CLUT shift
(`sceGuClutMode(…, shift 0 or 2, mask 3)`). The 4-entry palette gives alpha
0x00, 0x5C, 0xC2, 0xFE on white.

Font descriptors in `.data` are 0x54 bytes each. The font table at 0x3FAD14
lists font14, then the small HUD fonts em, es, en. For font14 (0x3FAE20):

| Offset | Field |
| --- | --- |
| +0x00 | u16 flags: 1 = single-byte font, 0x20 = use the bearing table, 0x60 = +1 px per char, 0x10 = −1 px |
| +0x04 | path, cell width 14, cell height 14, 32 cells per row |
| +0x1C | → 17 s16: first glyph number of each code group |
| +0x20 | → 6,953 codes (Shift-JIS bytes in order, read with `lh`) |
| +0x24 | → bearing table, 96 × (s32 left, s32 right), for ASCII 0x20–0x7F (0 in the original) |

A glyph number is the index of the character's code in the +0x20 list. That
list is split into 16 groups by the low nibble of the trail byte. The lookup
searches the char's group linearly; a char that is not found becomes glyph 6
(□).

## How English is drawn after the patch

1. **Glyph slots.** ASCII maps to Shift-JIS through the table at 0x347E4C
   (96 entries, 0x20–0x7F). The patch points those entries at 96 consecutive
   codes of group 2 (glyph numbers **1210–1305**, codes 0x9F82…0xE772). They
   are rare kanji that no game string uses. The check covered every
   pointer-referenced EBOOT string and all CSV and FES text: 1,819 distinct
   characters. Our glyphs replace those kanji in the font. Full-width Latin,
   kana and all other glyphs are unchanged.
2. **Advance.** The game already has proportional spacing (flag 0x20 + bearing
   table) for its small HUD fonts. The patch turns it on for font14 with a new
   table: left = 0, right = 14 − advance. At size s the advance is
   s − round(right × s / 14), so scaled text keeps its proportions.
   From 0.7.7 text is placed at exact sub-pixel positions. The printer takes the
   true advance (integer table + byte correction), moves the whole-pixel pen by
   the rounded value and carries the remainder; the remainder is written to the
   font descriptor (+0x28, unused) and the sprite emitter shifts the glyph's
   texture u by that fraction of the cell. The string-width (centring) and
   truncation routines and the glyph-array path still use the integer table, so
   centred text can sit about a pixel off.
3. **Glyph-array text** (unit names on lock-on labels, via 0x158ECC and
   0x1586B8) has no proportional code. A 21-instruction helper at 0x1740F8
   computes the advance from the same table: glyph − 1210 = table index.

### Patches

All jumps are PC-relative branches, and no patched word carries a relocation.
The EBOOT is a relocatable PRX, so the loader would overwrite such a word.
`vwf_build.py` refuses both.

| Where | Change |
| --- | --- |
| 0x347E4C | ASCII → code table: 96 new codes |
| 0x3FAE20 | font14 flags \|= 0x20 |
| 0x3FAE44 | font14 +0x24 = 0x2A4CD4, plus a new R_MIPS_32 relocation (see below) |
| 0x2A4CCC | width table: guard entry (index −1, single-byte kana) + 96 entries |
| 0x1740F8 | helper: `t7 = advance(glyph t7, size t8, font t9)` |
| 0x159B84 | printer: single-byte advance → the existing bearing-table code (0x15984C), instead of size × 0.75 |
| 0x159D18, 0x15A0AC | printer: single-byte glyph drawn at full cell width (was × 0.8) |
| 0x159ED4 | printer: `(` and `[` drawn at the pen (they were shifted half a cell left) |
| 0x1598C8, 0x159144, 0x1593C0 | printer, width, truncation: space uses the table (4 px) instead of size / 4 |
| 0x159C2C/34, 0x158FD0/DC | `` ` `` and `{|}~` use the ASCII table like the rest |
| 0x15917C | string width (0x1590A8, used for right-align and centring): single-byte chars use the table |
| 0x1594FC | line truncation (0x15937C): same |
| 0x158818, 0x158840, 0x15885C | glyph-array drawer: full-width glyph, font pointer saved at sp+0x2C |
| 0x158868–0x158888 | glyph-array drawer: advance from the helper |
| 0x1598A8–0x1598B4, 0x159A74–0x159A80 | printer, both advance blocks (0.7.7): `bal` to 0x157560, which takes R from the byte table at 0x158D54 for the 14 px font (exact advance), rounds L + R − carry once and keeps the remainder |
| 0x1595BC | printer prologue (0.7.7): carry (sp+0x448) and sub-pixel offset (desc+0x28) = 0, via 0x1574FC |
| 0x157FB4–0x157FB8 | emitter 0x157F10 (0.7.7): `bal` to 0x15750C, which moves texture u by round(offset × cellW / size) texels (u ≥ 0) |
| 0x158D54 | 96 signed bytes: (integer − true advance) × 64 per ASCII glyph, in the unused converter 0x158D0C |
| 0x15E6D4, 0x15E708/7CC/848/8B8/924/998 | shadowed-text emitter 0x15E644 (help bars, record screens; 0.7.7): after the lookup, k = round(offset × cellW / width) is kept at its sp+0x18; each of the six passes' `seh $t1, $t1` (texture u) calls a stub at 0x157364 that subtracts k (code at 0x157328, in the unused routine 0x157304) |
| 0x1589A4–0x1589C4, 0x158A48–0x158A70 | glyph-array centring pre-passes: width from the helper |

Code caves: 0x2A4CCC (1,264 bytes, an SDK matrix routine) and 0x1740F8 (the
first 96 bytes of an unused function). Nothing calls or points to either, no
branch enters them, and the table region holds no relocated word.

**New relocation.** The table pointer needs a relocation, otherwise it would
not follow the load address. `vwf_build.py` appends one entry
(r_offset 0x39944 in segment 1, R_MIPS_32, value relative to segment 0) to the
end of `.rel.data.0001`. It grows that section and the 0x700000A0 program
header by 8 bytes and shifts `.comment`, `.shstrtab` and the section header
table. PPSSPP reads relocations through the section headers, the PSP kernel
through the program header, so both are updated.

### Unused paths left alone

The second string-width routine 0x1573DC, the glyph-array width 0x157C90, the
converter 0x158D0C and the char→glyph routine 0x157304 have no callers. The
small HUD fonts (en, es, em) were already proportional and are untouched.

## Glyphs: 4x supersampling

`tools/vwf_font.py` draws each character at 4x (a 56 px cell) from
**Noto Sans JP, weight 600** (`C:\Windows\Fonts\NotoSansJP-VF.ttf`, SIL Open
Font License 1.1):

- Size: capital H is 40 px at 4x, i.e. 10 px. Caps sit on rows 1–10, matching
  the game's full-width Latin, and descenders reach row 13.
- Placement (from 0.7.7): advance = the font's own advance rounded to whole
  pixels. Every glyph's pen sits 1 px into its cell (room for the overhang of
  `j`), plus half its rounding error, so the error is shared by both sides of
  the letter. Before 0.7.7 each glyph took the sub-pixel phase that looked
  sharpest and a left margin that depended on its own ink, which moved letters
  by up to 1 px against each other ("Shi n", loose "u n o").
- At 14 px the glyph is box-filtered 4×4 and quantised to the game's 4 alpha
  levels (with a ×1.15 boost so 1 px strokes stay solid); a quarter pixel either
  way is allowed when it gives sharper stems. The 4x glyph uses the exact
  position. Space = 4 px. The 0x7F
  slot holds an ellipsis (…), 14 px wide.
- Widths: lower case 4–13 px (`i` and `l` 4, most 8–9, `m` 13), capitals
  5–13 px (`I` 5, most 8–10, `W` 13), digits 8 px. The old fixed pitch was
  about 10 px.

**Release note.** OFL 1.1 asks that the copyright notice and licence travel
with the font software. Credit "Noto Sans JP © Google, SIL Open Font License
1.1" in the release notes and include the licence text.

## Limits

- Only ASCII 0x20–0x7F is proportional. Double-byte characters (kana, kanji,
  full-width Latin) keep their 14 px cell.
- ASCII `$ < > @ ^` used to map to β, Ⅰ, Ⅱ, ㌔, ν, and `` ` `` and `{|}~` to a
  space. They are now ordinary ASCII glyphs. No game string uses them
  (checked as above). Two of them are aliases: `|` is drawn as a comma and
  `` ` `` as a double quote (`ALIASES` in `tools/vwf_font.py`), because the
  menu CSVs cannot hold those characters (`docs/build.md`). For Greek letters or Roman numerals, write the
  double-byte Shift-JIS character.
- `{` starts the game's colour codes (`{c…}`) where the caller enables them,
  so avoid a literal `{` in text.
- Text drawn into textures (titles, buttons, loading screens) is not affected.
- "4x" means the glyphs are drawn at 4x and downsampled to native 14 px. The
  game still renders text at 480×272; PPSSPP's 4x rendering scales the result.

## Testing in PPSSPP

`tools/ppsspp_ctl.py` drives PPSSPP's WebSocket debugger: button presses and
screenshots. Use a portable copy (the PPSSPP folder without `installed.txt`,
so it uses `memstick/` next to the exe) with these lines in
`memstick/PSP/SYSTEM/ppsspp.ini` under `[General]`:

```
RemoteDebuggerOnStartup = True
RemoteDebuggerLocal = True
RemoteISOPort = 45678
```

The Direct3D 11 backend cannot hand screenshots to the debugger. The script
then captures the PPSSPP window with `PrintWindow`, which works even when the
window is covered.

```bash
python tools/ppsspp_ctl.py press circle
```

```bash
python tools/ppsspp_ctl.py shot shot.png
```

## HD text (v0.6.0)

At 2x or 4x rendering in PPSSPP, the English text is drawn from **4x glyphs**. No texture pack is needed: the patched game samples a high-resolution glyph page itself.

The game draws each glyph as a sprite. The sprite's screen size comes from the text size, and its texture coordinates come from the font's cell size. A 56 px cell drawn into the same 14 px box therefore shows its detail as soon as PPSSPP renders above 1x. At 1x, and on a real PSP, the result is native-pixel text.

**Font.** The English glyphs are now drawn from **GenEi LateGo v2** (源暎ラテゴ, okoneya.jp, SIL Open Font License 1.1; Latin based on Linux Biolinum). It is kept in `work/fonts/GenEiLateGo_v2.ttc`, with the licence text in `work/fonts/GenEiLatin_LICENSE.txt`. `tools/vwf_build.py --ttf <file> [--ttf-index N]` picks another font, and `--no-hd` builds without the 4x page. GenEi is narrower than Noto Sans JP, so every measured box still fits (`tools/check_widths.py`).

**4x page.** It is appended to `gpsp3_font14.fnt` at offset 0x53740, which grows the file from 341,824 to 456,512 bytes. It is 448 px wide, 512 rows, 4 bpp, with 8 cells of 56 px per row. Like the main atlas, it holds two glyph layers: local glyph L sits in cell L >> 1, layer L & 1. Each 4x glyph uses the same pen position and cell origin as its 14 px version (see the placement rule above), at the exact sub-pixel position.

**Patch.** Code in `vwf_build.py`:

| Where | Change |
| --- | --- |
| 0x15787C | the glyph lookup's first two words become `b 0x15744C` / `nop` |
| 0x15744C | dispatcher, 43 words, in the unused string-width routine 0x1573DC. Its run of 68 words carries no relocation. |
| 30 loads in the sprite emitters 0x157A44, 0x157F10, 0x15802C, 0x15E6xx | `lw rX, 8(desc)` / `lw rY, 0xC(desc)` become `lh rX, 0x18(desc)` / `lh rY, 0x1A(desc)` |

How the dispatcher works:

- It always writes the font's own cell size to descriptor +0x18/+0x1A (halfwords). The text code never reads +0x18.
- For an English glyph of the 14 px font (cell 14, glyph 1210–1305), it writes 56 instead. It then sets the descriptor's base (+0x3C) to the 4x page and its cells per row (+0x10) to 8, runs the original lookup body (0x157884) with the page-local glyph number, and restores both fields.
- The original body then binds the page (TBP, TBW and TSIZE are unchanged, because the page is also 448 wide and bound as 512×512), picks the CLUT layer, and returns column and row.
- The printer still reads +0x08 (14) for the advance, so the layout does not change.

**Checked in PPSSPP 1.20.4** (OpenGL, 4x and 1x): the boot notice, the main menu help bar and the menus. At 4x, also a new campaign into the first mission (narration, mission list, briefing, flight HUD, pause menu). At 1x the GE scales the 4x glyph down into the 14 px cell. This is also what a real PSP would do, and it reads cleanly. Screenshots are in `work/ui/screens_0.6.0/` (local).

**Limit.** Glyphs still sit on whole native pixels, because sprite coordinates are 16-bit integers. At 4x, a 1-native-pixel rounding step in the game's advance (for example at size 12) shows as a 4 px gap. Moving to float vertices with fractional advances would remove this. That change is not made.

**Offscreen text.** The flight HUD's pilot name is drawn into an offscreen 224x16 buffer (PPSSPP logs "Matching from framebuffer ... +224x16"), which is then used as a texture. It stays 1x at any render scale.

Real hardware has not been tried. The extra 112 KB of font data is loaded into the same buffer as the font. PPSSPP loads it without problems.
