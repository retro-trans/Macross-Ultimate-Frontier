# Building a test ISO (v0.4.1, 2026-10-15)

```bash
python tools/build_iso.py 0.4.1
```

This takes the original disc (`Macross Ultimate Frontier (Japan).iso` in the
project root) and the work file `work/translation/en/dialogue.json`, and writes
`work/output/Macross Ultimate Frontier (EN v0.4.1).iso`. It takes about five
minutes (two of them for the texture redraw). Everything it makes goes to `work/output/` (gitignored).

| Step | Tool | Output |
| --- | --- | --- |
| 1 | `vwf_build.py`: proportional font + EBOOT patches (`docs/vwf.md`) | `work/output/vwf/` |
| 2 | `dump_eboot.py` on that EBOOT: string map with references | `work/output/build/eboot_strings.vwf.json` |
| 3 | `eboot_insert.py`: relocate the narration (`docs/formats.md`) | `work/output/build/EBOOT.BIN` |
| 4 | `insert_text.py`: CSV cells and FES string pools | `work/output/build/overlay/data/...` |
| 4b | `redraw_images.py`: textures with the text redrawn in English (`docs/image_redraw.md`; skip with `--no-images`) | `work/output/build/overlay/data/...gim` |
| 4c | voice subtitles, only with `--voice-subs <file>`: `voice_subs_patch.py` hooks the EBOOT, `voice_subs_at3.py` appends each line to its clip (`docs/voice_subtitles.md`) | `work/output/build/EBOOT.BIN`, `overlay/data/sound/voice/*.at3` |
| 4d | song lyrics, only with `--lyrics <dir>` or `--lyrics-placeholder`: `lyrics_patch.py` hooks the EBOOT, `lyrics.py build` appends each song's lines to its `bgmNN.at3` (`docs/lyrics.md`) | `work/output/build/EBOOT.BIN`, `work/output/build/bgm/*.at3` |
| 5 | `muf_archive.py repack --overlay` (the VWF font is copied into the overlay) | `work/output/build/USRDIR/` |
| 6 | `iso_patch.py`: EBOOT and the three archive files | the ISO |

`--work <dir>` puts the intermediate files in `<dir>` (and `<dir>/vwf`) instead of
`work/output/build` and `work/output/vwf`, so two builds can run side by side.
`--voice-subs work/translation/en/voice/voice_subs.en.json` adds the voice-clip
subtitles (write that file with `python tools/voice_subs_export.py`);
`--voice-placeholder` shows each clip's id instead, to test the hooks.
`--lyrics work/translation/en/lyrics` adds the filled song lyrics (normally private;
the v0.7.15 release has explicit user authorization: `docs/lyrics.md`); `--lyrics-placeholder` shows test lines
("bgm03 line 1 at 0:02") in every song instead.

Other translation files can be added with `--tr <file>` (the rows need `id`,
`en`, and for CSV/FES rows `jp` and `ref` as in `dialogue.json`, because
`insert_text.py` checks the source bytes before it replaces them).

## What goes where

| Text | Rows | How it is inserted |
| --- | --- | --- |
| Narration (EBOOT) | 223 | Moved to the old slots of moved strings and a new 64 KB gap; pointer words, `lui`/`addiu` pairs and relocations are patched. Row 135 (`%s and %s`) keeps one copy that both epilogue tables point to. |
| Briefings (`mission_ext.csv`) | 432 | Cell replaced. The file grows from 44,437 to 53,987 bytes; the repacker moves the members after it. |
| Shop titles and quotes (`nn_ext.csv` 5000–5299) | 300 | Cell replaced (70,184 → 71,472 bytes). |
| In-mission objectives and tutorial lines (FES) | 232 in 82 files | English appended after the pool, the one reference repointed (below). |

### CSV: commas and double quotes

The menu CSVs have no quoting, so a cell cannot hold an ASCII `,` or `"`.
`insert_text.py` writes `|` for a comma and `` ` `` for a double quote, and
`tools/vwf_font.py` (`ALIASES`) draws those two font slots as a comma and a
double quote. No game string uses `|` or `` ` `` (`docs/vwf.md`), so nothing
else changes. **The CSVs and the VWF font must ship together.** EBOOT and
FES text keeps real commas and quotes.

The CSV's two-character `\n` line break is kept as it is. One character has
no Shift-JIS code: `ō` in `NNSHOP_ITEM_5283` ("Seikan Hikō") is written as
`ou`. The tool lists every such replacement.

### FES string pools

A FES script uses a string with the instruction `0x0080, k, <offset>` (three
u16 words, `k` = 0–2), where the offset counts from the start of the string
pool (the u16 at 0x12), not from the start of the file. Each of the 232
Japanese strings has exactly one such reference. `insert_text.py` appends the
English after the last string and repoints that reference; the old Japanese
bytes stay in place, so no other offset in the file moves. Details in
`docs/formats.md`.

### How the patched EBOOT gets onto the disc

The disc carries the **decrypted** EBOOT (a plain PRX ELF) as
`PSP_GAME/SYSDIR/EBOOT.BIN`. `iso_patch.py` appends it to the image (it is
64 KB larger than the original) and updates its directory record.

- PPSSPP loads an unencrypted EBOOT directly. Tested: 1.20.4.
- Custom firmware (PRO, ME, ARK, through their ISO drivers) also loads an
  unencrypted PRX. Not tested on hardware.
- Official firmware without CFW needs a signed EBOOT. If that is ever wanted,
  the patched ELF can be re-signed with a tool such as `sign_np`. This has
  not been tried.
- `SYSDIR/BOOT.BIN` is zero-filled on the original disc and is not used.
- A plugin (patching the encrypted EBOOT in memory at boot) was not chosen:
  it would only work on CFW, cannot run in PPSSPP without extra setup, and
  every EBOOT patch (VWF, relocations) would need to be redone as
  run-time hooks.

`iso_patch.py` appends every file that grows and leaves the old copy as dead
space, so the test ISO is about 290 MB larger than the original (the old
`fileset.dat` is still in it). This does not matter for testing. A release
build can be laid out compactly later.

## Debug build: epilogue text

Epilogues play only after the last mission of an era. To see their text
without that, `work/output/debug_epilogue_v0.2.0.iso` puts the Zero epilogue
(the 13 lines without `%s`) into the 15 Zero prologue slots, which play
right after a new campaign is started. It is made with the same tools; only
the translation file differs. It uses the same narration renderer, so the
widths are the same.

## Release image

A release ISO is the built ISO re-laid out in the original file order with
`tools/relayout_iso.py` (see `docs/RETRO_TRANS_RELEASES.md`). The built test ISO
keeps appended copies and is not a release source.
