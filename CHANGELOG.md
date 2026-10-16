# Changelog

## [0.7.1] - 2026-10-16 (first public release)

Same game content as 0.7.0, in the original disc layout.

### Added
- `tools/relayout_iso.py`: rebuilds a built ISO in the original file order. `iso_patch.py` appends grown files at the end, which left dead copies of `macross.dat` and `fileset.dat` (2.2 GB image) and made an xdelta patch nearly as large. Files now keep their order and shift by whole 32 KB blocks where a file grew; directory records and the volume size are rewritten, and every file is verified against the built ISO.
- Public repository files: `README.md`, `CONTRIBUTING.md`, `LICENSE` (MIT for text and tools), `docs/RETRO_TRANS_RELEASES.md`, and `.gitignore` rules from the retro-trans template.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.1).iso`: `python tools/relayout_iso.py "Macross Ultimate Frontier (Japan).iso" "work/output/Macross Ultimate Frontier (EN v0.7.0).iso" "work/output/Macross Ultimate Frontier (EN v0.7.1).iso" --write`. 1,238,269,952 bytes (original 1,237,843,968), SHA-256 `01fdc0b61ea21578593d2fb7c1450c768372bbd02e691aa55ef18554d4e344bc`. 100 of 102 files moved by up to 208 sectors; all 102 match 0.7.0.
- Played in PPSSPP 1.20.4 at 4x from a new campaign into the first Zero mission: mission title card, radio subtitles under the cut-in, flight HUD.
- Release assets built with Retro Trans Tools (`docs/RETRO_TRANS_RELEASES.md`); metadata in `docs/releases/0.7.1/`.

## [0.7.0] - 2026-10-16 (test build, not released)

### Added
- **English subtitles for the in-mission radio voice.** The cut-in lines had no text anywhere in the game. Every clip was transcribed with a local Whisper model, translated, and the patched game now shows the English line under the cut-in while the clip plays: in the pre-mission intro camera, during the "enemy appeared" / "allies sighted" banners and during play with the HUD. Details, numbers and limits: `docs/voice_subtitles.md`.
  - **12,489 of the 14,215 voice clips have a subtitle.** The rest have nothing to show: 1,155 are silent placeholder clips (the game has no voice for Gepelnitchi, Sharon Apple's enemy form, the Vajra, the Zentradi soldier, most of Boddole Zer and about a third of Minmay's clips), 439 are drums or screams without words (plus 89 repeats of such clips), and 43 are the era prologue narration, which is already shown as English text.
  - **Transcription:** faster-whisper large-v3 on the GPU, about 2 hours (`tools/voice_transcribe.py`, venv in `work/source/whisper_venv`). A retry pass re-runs clips that look like Whisper hallucinations. The transcripts are local only (`work/source/voice/`, Japanese).
  - **Translation:** 144 slices of 80 rows (`work/translation/en/voice/slices/`), brief `docs/voice_translation_brief.md`, speaker map `work/translation/en/voice/speakers.en.json` (79 speakers). The five operators read one script, so their transcripts were cross-checked. 1,224 rows are flagged `whisper_doubt` (transcript corrected from context) and 439 `uncertain`, each with a note. A name pass (`tools/voice_fix_names.py`) unified AFOS, Elgersoln, Konig Monster, Klan Klang's team, Nene and GERWALK.
  - **Storage:** each line is appended to the end of its own clip in `macross.dat` (after the RIFF data, which is unchanged), so no memory is added. The `.vad` lip-sync files were not used because their fileset bundle stays in memory during missions.
  - **EBOOT hooks** (`tools/voice_subs_patch.py`): the two calls that load a clip's lip-sync file now also read the line from the clip's tail; the end of the mission's 2D layer now draws it. The line follows the game's lip-sync counter, so it shows while that clip plays (two clips can be queued at once), plus 24 frames. Long lines are cut into parts that advance with the clip. Text: VWF font, 12 px, white with a dark shadow, centred at (240, 228) between the HP bars and the weapons panel, sprite depth nearest so banners do not hide it. Code in two unused routines (253 words); no new relocations.
- New tools: `voice_transcribe.py`, `voice_rows.py`, `voice_slice.py` (show / check a slice), `voice_fix_names.py`, `voice_subs_export.py`, `voice_subs_at3.py`, `voice_subs_patch.py`.
- `tools/build_iso.py`: `--voice-subs <file>` (and `--voice-placeholder` to show clip ids), and `--work <dir>` to build in another folder.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.0).iso`, built with `python tools/build_iso.py 0.7.0 --work work/output/build_0.7.0 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.0.log`). Otherwise the same content as 0.6.0 (GenEi, HD text, textures).
- Played in PPSSPP 1.20.4 through the opening of the first Zero mission: intro cut-ins, both banners, mission start and radio lines in flight (`work/ui/screens_0.7.0/`, local).

### Known
- Only clips that the mission script queues are subtitled; voices played elsewhere (menus, character select samples) are not.
- Parts of a long line advance at even steps of the clip, not with the phrasing.
- Not tried on real hardware. Whether subtitles show with the "2D Display" option off was not checked. Only the first Zero mission was played.

## [0.6.0] - 2026-10-16 (test build, not released)

### Added
- **HD text without a texture pack.** At 2x/4x rendering in PPSSPP, English text is drawn from 4x glyphs that the patched game samples itself. A 4x glyph page is appended to the font, a dispatcher in the glyph lookup routes English glyphs to it, and 30 texture-coordinate loads in the four sprite emitters read the per-glyph cell size. At 1x (and on a real PSP) the GPU scales the same 4x glyphs down to the 14 px cell; this reads cleanly in PPSSPP at 1x. `--no-hd` builds the plain 14 px version. Details: `docs/vwf.md` "HD text".
- **New English font: GenEi LateGo v2** (源暎ラテゴ by okoneya.jp, SIL Open Font License 1.1; Latin based on Linux Biolinum). It is in `work/fonts/` with its licence. Release notes must credit it: "GenEi LateGo © okoneya.jp, SIL Open Font License 1.1", with the licence text included.
- `tools/vwf_font.py`: TTC face index, 4x glyph cells (`build_hd_glyph`), the 4x page packer (`hd_page`) and a 4x preview. `tools/vwf_build.py`: `--ttf`, `--ttf-index`, `--no-hd`. The defaults are GenEi and HD on.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.6.0).iso`, built with `python tools/build_iso.py 0.6.0 --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json`. EBOOT: 3,509 strings, loader check ok.
- With the GenEi widths, every measured box still fits, with more room. The soft-limit list shrank from 1,403 to 1,095 lines.
- Checked in PPSSPP 1.20.4 (OpenGL) at 4x and 1x: the boot notice, the menu help bar and the menus. At 4x, also from a new campaign into the first mission: narration, tutorial notices, mission list, briefing, sortie prompt, in-flight HUD, pause menu and info panel.
- Both v0.6.0 and `-nohd` enter the mission and play. An earlier run seemed to reset to the boot logo on mission start. The same reset showed up with the v0.5.1 ISO under the same scripted button route, so it comes from the test route, not from the font or the patch.
  - Fixed during testing: a sixth texture-coordinate load in emitter 0x15E6xx had been missed, which garbled the help bar. Uneven letter spacing at 4x was evened out.

### Known
- Glyphs still sit on whole native pixels, so a few 1-pixel spacing steps show at 4x.
- The pilot name in the top-left of the flight HUD stays 1x at 4x rendering. The game draws it into an offscreen 224x16 buffer and then uses that as a texture, so the 4x glyphs never reach the screen at full size. The faint left serif of GenEi's "n" also makes "Shin" look like "Shi n" there.
- Not tried on real hardware.

## [0.5.1] - 2026-10-15 (test build, not released)

### Fixed
- **Every line now fits its confirmed on-screen box.** `tools/check_widths.py` reports 0 lines over in every type whose box was measured in game, and in the description, title and gallery lists. The refit followed `docs/refit_brief.md`: compress or abbreviate, never drop the end of a sentence. Fixes are in `work/translation/en/review/refit_*.en.json`.
  - **Briefing stories:** all 198 missions that were over now have 2 lines, each within 429/415 px at size 11 and within 79 characters. This fixes the garbled and memory-corrupting briefing text. Checked in game: MA_010, the mission that showed corrupted text in 0.2.0, now shows both lines cleanly.
  - **Narration:** 56 lines refit to the 480 px screen. Words were moved between rows of the same sentence where needed, adding 9 extra rows; row 135 is untouched.
  - **Other screen text:** tutorial box (34 rows), mission-list objectives (40), objective strip (9), help bar (1).
  - **Descriptions:** unit descriptions (57) and pilot profiles (38) fit 434 px. The unit names and voice-actor credits are unchanged.
  - **Lists:** shop titles and their EBOOT copies, bonus conditions, mission names and list labels (167 fixes).
  - **Gallery labels:** the prefixes "SDF Macross" / "Flash Back 2012" / "Dynamite 7" are now "SDF" / "FB2012" / "D7" everywhere (213 labels), so they fit the 168 px list.
  - **Review corrections to refits:** Boddole Zer's profile keeps that he deems humanity Protoculture and sets out to destroy it; row 179 keeps "deemed uncontrollable"; row 1046 has its subject restored ("An amateur? You're good for one.").
- New tool `tools/fit_line.py`: measures a candidate line, or a whole fix file, against its box.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.5.1).iso`, built with `python tools/build_iso.py 0.5.1 --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json`. EBOOT: 3,509 of 3,575 strings, loader check ok. 479 textures.
- Played in PPSSPP 1.20.4 from boot into the first Zero mission (screenshots in `work/ui/screens_0.5.1/`, local). English throughout:
  - the menus, save data, character, operator and flight setup, and era select;
  - the loading tip card and the Zero prologue;
  - the mission list and info panel, the briefing, the "Proceed?" prompt;
  - the mission title card and the HUD banners.
  The name-entry keyboard labels come from the PSP system keyboard, which PPSSPP draws; they are not game text.

### Still open
- 1,403 strings are over only a **soft** limit: their own Japanese width, with the box not measured. They were not cut. Measure their boxes in game first.
- 15 list labels have unmeasured boxes 14–42 px wide: rank abbreviations, weather words, "Simon", "Civilian", "Mayor". They are kept at their shortest sensible form and flagged.
- The flight-type card's small description text looks cramped (texture redraw). Worth a closer look.

## [0.5.0] - 2026-10-15 (test build, not released)

### Build
- **First build with all the translated text inserted**: `work/output/Macross Ultimate Frontier (EN v0.5.0).iso`, made by `python tools/build_iso.py 0.5.0 --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log: `work/output/build_0.5.0.log`).
  - Dialogue: 1,187 rows. UI and system text: 3,525 strings, 5,848 places. EBOOT: 3,509 of 3,575 strings (the rest have no Japanese words); the loader check is ok.
  - Menu CSVs: mission_ext, ms_ext, nn_ext (1,784 cells), pack_ext and pilot_ext. Unit lists: all mission files, including the internal labels. FES: 232 strings in 82 files.
  - 479 redrawn textures from 0.4.1. The official series logos are kept.
- Boot-tested in PPSSPP 1.20.4 (screenshots in `work/ui/screens_0.5.0/`, local):
  - The autosave notice, the soundtrack-folder prompt, the title-screen copyright and the main menu are English (help bar "Modes for single-player play.", button guide "OK / Back").
  - The attract demo runs in game without problems.
  - Campaign play, the hangar, the shop and the gallery were not played through in this test.
- Known: lines that are too long are still not refitted. Briefing lines over 79 characters show corrupted (about 300 lines, `work/ui/width_report.md`), and long pilot profiles and weapon names may overflow their boxes.

## [0.4.1] - 2026-10-15 (test build, not released)

### Changed
- **English copyright lines shipped** (approved by the user): the title screen (`menu/title/title.gim`) and the screenshot viewer (`menu/gallery/ssctrl/ss_copyright.gim`) now read "©… BIGWEST" and "©2007 BIGWEST/MACROSS F PROJECT/MBS"; "©2009 NBGI" was already Latin. They were held out of 0.4.0.
- Now 479 textures and 499 of the 504 rows are redrawn; the 5 others are kept as art.
- Test ISO: `work/output/Macross Ultimate Frontier (EN v0.4.1).iso` (`python tools/build_iso.py 0.4.1`). Checked in PPSSPP: the title screen shows the English lines (`work/ui/screens_0.4.0/14_title_copyright_v0.4.1.png`). The screenshot-viewer strip is checked in the preview sheet only.

## [0.4.0] - 2026-10-15 (test build, not released)

### Build
- **Test ISO with English textures**: `work/output/Macross Ultimate Frontier (EN v0.4.0).iso`, made by `python tools/build_iso.py 0.4.0`. It is the 0.2.0 build (dialogue, VWF font) plus the redrawn textures; the UI text from 0.3.0 is not inserted yet.
  - `build_iso.py` now runs `tools/redraw_images.py` into the build overlay (step 4b). `--no-images` leaves it out.

### Added
- **Text in textures redrawn in English: 477 textures, 496 of the 504 plain-text rows.** How it works, every choice made and what was tested: `docs/image_redraw.md`.
  - Covered: system and pause menus, control config, hangar panels, colour editor, pilot stats, network rooms, results, shop, save data, flight select, gallery records, rank ribbons, placeholder cards, the 191 mission title cards, the in-mission HUD alerts (2d_ope / 2d_rat), the eight loading-screen tip cards, the tutorial banner, two anime stills and their gallery thumbnails.
  - Official logos (`img_logos.json`) are not touched, as decided. Also kept as art, following the row notes: the cropped poster in the f_003 still, and the Nyan-Nyan restaurant logo and seal stamps.
  - **Held for your OK** (preview only, not in the ISO): the copyright lines on the title screen and in the screenshot viewer. Their row notes ask for approval before legal text is changed.
  - The "Restricted" cards' small tag is left blank (LIMIT is already drawn), and the "Standby" cards say WAIT, as the row notes suggest.
  - Before/after contact sheets for every texture: `work/ui/redraw_preview/` (local, game art). `report.json` lists the size, squeeze and short form of every text; `shared_text.json` lists the textures that share text.
- `tools/gim.py`: **GIM encoder.** `encode` writes new pixels into a copy of the original texture, so the format, swizzle, palette layout and size stay the same. Indexed textures keep their palette when they can; otherwise the image is reduced to the palette size with a k-means seeded with the old palette, and transparent pixels keep an exact transparent entry. RGBA5650/5551/4444/8888 are packed back to their own format. `roundtrip` checks it: all 10,360 textures in the game decode and re-encode byte for byte.
- `tools/redraw_images.py`: layout-driven redraw (erase modes, Noto Sans/Serif JP rendering with outline, glow, shadow and gradient, fitting with the short forms from the row notes, tip-card typesetter, thumbnails, contact sheets).
- `work/ui/redraw_layout.json`: where each text goes and how it is drawn (no Japanese).
- `docs/formats.md`: GIM format and encoder section.

### Found in game (PPSSPP 1.20.4)
- English shows in: the button-guide bar, save data, the hangar mission, player, record and shop tabs, the hangar system menu, the briefing Sortie button, the loading tip card, the mission title card, the HUD alerts and the pause menu. Screenshots: `work/ui/screens_0.4.0/`.
- The game draws `common_guide_period/room.gim` only up to the old text width (about 64 px), so "Switch Era" was cut; it is now squeezed into that width.
- The bright record-list label is drawn over the dim button, so both are now drawn in the same place and size.
- The game shows the English twin of a HUD alert (top left) and the redrawn banner together.
- Fixed before the final build: palette reduction gave the empty area of the textures alpha 1, which showed as a faint line under the mission title cards.

## [0.3.0] - 2026-10-15 (translation only, not built)

### Added
- **All remaining Japanese is translated.** Status and coverage: `docs/remaining_translation.md`.
  - **UI and system text:** 3,525 distinct strings (5,848 occurrences). That covers EBOOT menus and messages, help, skills, titles, unlocks, gallery labels, song credits, unit and weapon names and the pilot table; unit, pilot and pack descriptions; the rest of the Nyan-Nyan list; and mission unit names. 100% translated, every slice passes `tools/ui_slice.py check`, and four proofreaders made 41 fixes. Committed copy: `work/translation/en/ui.en.json`; slices: `slices_ui/ui_01..15.en.json`.
  - **Internal unit-list labels:** 51 distinct, 216 rows (`internal_labels.en.json`).
  - **Text in images:** 504 plain-text textures transcribed and translated, with size, kind and style recorded for the redraw (`images.en.json`).
  - **Decision (2026-10-15):** the official Japanese-script series logos and tags (223 textures) are kept as they are and not redrawn. They are catalogued with English titles for reference only (`keep_original`).
  - **`camera.tbl` developer comments:** 50 lines (`camera_tbl.en.json`).
  - Insertion dry runs pass: all CSV cells, and 3,509 of 3,575 EBOOT strings, with the loader check ok. The rest have no Japanese words.
- Tools:
  - `build_ui.py`, `prefill_rules.py`, `ui_slice.py` (show, check, merge, apply, export).
  - `gim.py`: decodes GIM textures to PNG, with contact sheets.
  - `images_export.py`, `build_internal_labels.py`, `build_camera_comments.py`.
- `docs/ui_translation_brief.md`: UI and image translation rules.
- `.gitignore`: decoded textures (`work/ui/gim_png/`).

### Changed (glossary)
- Added:
  - 22 characters, from the unit lists and profiles: Canaria Berstein, Henry Gilliam, Manfred Brando, Physica S. Fulcrum, Suzie Newtlet and Shun Toma (wiki-checked); Irina Hayakawa and other minor pilots (`needs_check`).
  - Organizations: Dancing Skull, Vector Productions, Irina Squad, Critical Path Corporation.
  - Units: Cheyenne II, SDF-2 Megaroad-01, Super Booster, Gavigla.
  - Songs: Triangler, Koi no Uta.
  - UI terms: Tune Points, Song Weapon, wireless play, "Proceed?", Nyan-Nyan Pts.
  - Conventions: "(Standard)" for generic units; "(TV)" / "(Movie)" / "(Giant)".
- 星間飛行 is now "Seikan Hikou": the macron is not in Shift-JIS.

## [0.2.0] - 2026-10-15 (test build, not released)

### Build
- **First English test ISO**: `work/output/Macross Ultimate Frontier (EN v0.2.0).iso`, made by `python tools/build_iso.py 0.2.0` (about 2.5 minutes, reproducible byte for byte). How it is put together: `docs/build.md`.
  - All 1,187 dialogue rows are inserted: 223 narration lines in the EBOOT, 432 briefing cells in `mission_ext.csv`, 300 shop titles in `nn_ext.csv`, 232 objective and tutorial strings in 82 FES scripts. The VWF font is included.
  - Tested in PPSSPP 1.20.4: it boots, and English shows in the mission information panel, the briefing screen, the tutorial instruction box and the "Data of the History" prologue. The epilogue text was checked through `work/output/debug_epilogue_v0.2.0.iso` (the Zero epilogue put into the Zero prologue slots). Not tested on hardware.
  - The disc carries the decrypted EBOOT. PPSSPP loads it, and so should custom firmware; official firmware would need it signed. A plugin approach was not chosen (`docs/build.md`).
  - Screenshots, with the measured boxes drawn on: `work/ui/screens_0.2.0/` (`tools/label_screens.py`, boxes in `screens.json`).
- Known problem: briefing story lines over 79 characters are shown corrupted (see Found in game). 503 lines need rewording; list in `work/ui/width_report.md`.

### Added (insertion)
- `tools/insert_text.py`: writes the CSV cells and FES strings into an overlay tree for `muf_archive.py repack --overlay`. Every row is checked against its Japanese source bytes first.
  - CSV: an ASCII comma becomes `|` and a double quote becomes `` ` ``. The VWF font draws those two slots as `,` and `"` (`ALIASES` in `tools/vwf_font.py`), so the CSVs need that font. `ō` (no Shift-JIS code, one shop title) is written as `ou`.
  - FES: the English is appended to the string pool and its one reference is repointed.
- `tools/build_iso.py`: the whole build in one command.
- `tools/label_screens.py`: draws text boxes onto screenshots.

### Found in game
- **FES string references**: the instruction `0x0080, k, <offset from pool start>`. Each of the 232 Japanese strings has exactly one. Offsets count from the pool, so the pool can grow at the end without moving anything (`docs/formats.md`).
- **Briefing story**: each line is copied into an 80-character slot with no bounds check, so a line may hold 79 characters at most. A longer line runs into the next line (MA_010 showed it). A line wider than the panel is squeezed to fit.
- **Tutorial box** (`fes_tutorial`): size 14, about 309 px inside, up to 3 lines, centred. Too-wide lines run past the frame. Now confirmed in `work/ui/text_limits.json`.
- **Narration**: lines wider than the 480 px screen are cut off at both edges.
- The width checker matches the screen to within 3 px. `check_widths.py` now also checks a per-type `max_chars` (79 for briefing stories).
- Result: 503 of 1,776 lines over (was 485 before the character limit and the tutorial box were known): 323 briefing story lines in 198 missions, 56 narration, 44 shop titles, 40 mission objectives, 39 tutorial lines, 1 FES objective.

### Added
- **All story and dialogue text is translated to English: 1,187 of 1,187 rows.** That covers 223 prologue/epilogue narration lines from the EBOOT, 432 mission objective and briefing rows (`mission_ext.csv`), 232 in-mission objective and tutorial lines (FES scripts) and 300 Nyan-Nyan shop titles and quotes (`nn_ext.csv` 5000–5299). Status, process and open points are in `docs/dialogue_translation.md`.
  - Committed copies (no Japanese): `work/translation/en/dialogue.en.json`, `work/translation/en/slices/slice_01..15.en.json`, and the applied review fixes in `work/translation/en/review/*.en.json`.
- The EBOOT is decrypted with a portable PPSSPP copy (`DumpFileTypes = 3`). It shows that the in-mission radio chatter has no subtitle text anywhere and is voice only. Recorded in `docs/formats.md`, together with the narration location and the pointer tables (one string is shared by two epilogues).
- Tools:
  - `build_dialogue.py`: builds the work file and keeps existing English.
  - `show_slice.py` / `show_rows.py`: viewers.
  - `check_slice.py`: validates ids, line breaks, placeholders, Japanese leaks and avoid-list names.
  - `merge_slices.py`, `apply_fixes.py`: reviewed fixes go into the slice files, with a dry run by default.
  - `fix_names.py`: glossary name pass, dry run by default.
  - `strip_jp.py`: writes the git-safe `*.en.json`.
- **EBOOT text dump with references.** `tools/dump_eboot.py` writes `work/source/text/eboot_strings.json` (gitignored): 3,575 Japanese strings, 50,825 characters. It covers menu labels, system, save and replay messages, help lines, titles and unlock conditions, gallery captions, song credits, narration and pilot names.
  - The strings are found through the PRX relocation table, so every reference is listed: 4,507 pointer words (with their table runs) and 209 `lui`/`addiu` pairs in code.
  - HI16s are paired with their LO16s through the control-flow graph, because list order gives wrong pairs. All 30,687 used HI16s agree with the loader's carry rule.
  - Flags: strings copied inline with a fixed length (6), merged string tails (2), and pilot-table names that have no pointer and can only be edited in place (151).
  - `docs/formats.md` covers the PRX layout, the JSON fields, how to relocate strings (pointer and code patching, the HI16 carry rule, where new memory could come from) and the ASCII → full-width map the text renderer uses. It supersedes the earlier byte-scan files in `work/source/eboot/`.
  - Fixed: values that point into the data segment are stored relative to that segment, and the carry is now checked per segment. The dump output did not change. `capacity` no longer runs past the next referenced address. New flags: `inner_refs` (merged ASCII and empty tails) and `in_place` (the pilot table and the ASCII map).
- **EBOOT insertion: `tools/eboot_insert.py`.** It relocates translated strings. They go first into the freed old slots, then into a new N × 64 KB gap opened between `.data` and `.bss`.
  - It patches pointer words, `lui`/`addiu` pairs and relocation entries, and reorders HI16 entries so the loader's carry is right. In-place strings must fit.
  - It checks every reference by simulating the PSP loader on the input and the output.
  - Tested in PPSSPP 1.20.4. With all 3,417 movable strings in the gap, the game boots to the main menu unchanged. Narration plus longer English help lines are shown correctly, also on top of the VWF EBOOT. No translations gives a byte-identical file.
  - Test ISOs are built with `tools/iso_patch.py`.
- **Variable-width font for English.** `tools/vwf_build.py` patches the EBOOT and rebuilds the 14 px font so ASCII text is proportional (about 4–13 px per letter instead of a fixed ~10 px). Details are in `docs/vwf.md`.
  - Glyphs are drawn at 4x from Noto Sans JP (weight 600, SIL OFL 1.1) by `tools/vwf_font.py`, then downsampled to the game's 14×14 2 bpp cells. The sharpest sub-pixel phase is picked per glyph. They occupy 96 rare-kanji slots that no game string uses.
  - The game's own bearing-table code, until now used only by the HUD fonts, is switched on for the 14 px font. It is used by the printer, the width measurer (centring and right-align) and the line truncator. A small helper does the same for the glyph-array path (lock-on unit labels).
  - The EBOOT is a relocatable PRX, so patches are PC-relative and never touch a relocated word. The table pointer gets one new relocation, appended to the reloc table.
  - Tested in PPSSPP 1.20.4: help bar, menus, title screen, a lock-on label, Japanese text unchanged. Real hardware is not tested.
  - Test disc: `work/output/vwf_test.iso` (font and EBOOT only, no translations).
- `tools/muf_archive.py repack --overlay <tree>`: patched files (such as the font) replace extracted ones without touching `work/source/dat`.
- `tools/ppsspp_ctl.py`: drives PPSSPP's WebSocket debugger (button presses, screenshots) for automated in-game checks.
- `docs/translation_brief.md`: the translator rules for this game.
- **Pixel width check: `tools/check_widths.py`.** It measures every English line with the VWF advances, at the size the game draws that text type. It writes `work/ui/width_report.md` and `.json`, which list each line over its box with its id, width and limit, plus line-count overflows and characters Shift-JIS cannot encode. Details are in `docs/text_limits.md`.
  - `work/ui/text_limits.json` holds the box limits for 21 text types plus 26 EBOOT pointer lists. Each limit is the widest Japanese line of its type. Five boxes were measured in PPSSPP and are marked `confirmed`:
    - help bar: size 12
    - narration: size 12, centred
    - briefing story: size 11, 429/415 px, because the launch button cuts into line 2
    - mission objective panel: size 10, 214 px
    - orange objective strip: size 10, 212 px
  - The EBOOT mission records are typed by field: objectives, bonus conditions and mission name.
  - Result on the 0.2.0 dialogue: 485 of 1,776 lines are over. That is 305 briefing-story lines (up to 1.8 times the box), 56 narration, 44 shop titles, 40 mission objectives, 39 tutorial lines (box not confirmed yet) and 1 FES objective. Row `NNSHOP_ITEM_5283` contains `ō`, which Shift-JIS cannot encode. Nothing was cut; the lines are listed for rewording.

### Changed (glossary)
- ゲペルニッチ is now **Gepelnitchi**. The wiki page "Geperuniti" used before is a vandalised stub.
- バーミリオン小隊 is now **Vermillion Flight** (wiki title).
- 新統合軍 is now **"New U.N. Forces"**, kept apart from 新統合宇宙軍 "New U.N. Spacy". Brief and glossary disagreed; decided in review.
- The game reading ギリアム・アングレート is fixed. Japanese short forms (`ja_aliases`) are added for the main cast.
- Added:
  - Characters: the magazine cameos.
  - Organizations: Latence, 117th Research Fleet, Sagittarius Squadron, Purple Flight, Pink Pecker, Dalmatian High School, Editorial Sentai Dengeki V.
  - Places: Lux, Island 3, Ontario Autonomous Zone, Asuka II, Global, Fulbtzs-Berrentzs, Boddole Zer's mobile fortress.
  - Terms: about 40, including AFOS, Kadun, Operation Iconoclasm and Stargazer, Spiritia Farm Project, the tutorial controls and the stock objectives.
  - Songs: "Love Drifts Away".
- Ranks: army style (Misa "Lieutenant/Captain Hayase", Roy "Major Focker").

## [0.1.0] - 2026-10-15 (not built)

### Added
- Project folder layout: `work/{output,glossary,ui,translation,source}`, `docs`, `tools`, `incoming`.
- Glossary v0.1.0 in `work/glossary/`:
  - `characters.json`: 100 characters, with English name, Japanese name, aliases, spellings to avoid, gender, species, position, affiliation, personality, in-game role and source links.
  - `organizations.json` (34), `locations.json` (15), `mecha.json` (103 units plus packs and conventions), `terms.json` (lore, game system, skills, songs, series titles).
- `docs/glossary.md`: spelling policy, field meanings, sources, open spelling decisions.
- `.gitignore` that keeps the ISO and extracted source data out of git.
- Archive tools (formats in `docs/formats.md`):
  - `tools/muf_archive.py`: extracts `macross.idx` / `macross.dat` / `fileset.dat` into `work/source/dat/` (41,918 files) and repacks them. The repack is byte-identical to the ISO, including a full re-compression of all 27,487 fileset members. Files that grow are relocated, and every index copy is updated.
  - `tools/muf_lzss.py`: the fileset member codec (XOR 0x72 + Okumura LZSS, plus a stored mode). Its encoder reproduces the original compressed data exactly.
- `tools/dump_text.py`: dumps the game text to `work/source/text/` (gitignored). It covers the 5 menu-text CSVs (2,517 cells: mission briefings, unit, pilot and pack descriptions, shop names), 232 Japanese strings from the mission scripts, and 1,070 unit display names.
- `tools/glossary_check.py` and its output `work/glossary/gaps.json`: names the game uses, matched against the glossary. Summary in `docs/glossary_gaps.md`.
- `docs/formats.md`: the PIDX0 index, FSTS bundles, member compression, FES string pools, the CSV rules (no quoting, so no ASCII commas in translations), and where the text is.

### Notes
- The glossary is built from ja.wikipedia (game roster) and the Macross Wiki (English names and character facts). It has not been checked against the game's own text yet, because the `macross.dat` archive is still unextracted.
- 24 characters were marked `needs_check`. See the open-decisions table in `docs/glossary.md`.
- First check against the game text: 52 character names, 22 units and about 16 organization or operation names are missing from the glossary. One spelling differs: the game writes ギリアム・アングレート, the glossary ギリアム・アングリット. See `docs/glossary_gaps.md`.
- Not dumped yet: strings inside the encrypted EBOOT (probably most menu and system text), and text drawn into GIM images.

### Changed
- The user confirmed four spellings, now `status: "decided"`: Vrlitwhai Kridanik, Quamzin Kravshera, Milia Fallyna Jenius and Jeffrey Wilder. 20 characters remain `needs_check`.
