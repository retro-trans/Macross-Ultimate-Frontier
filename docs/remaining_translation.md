# Remaining-text translation (v0.3.0, 2026-10-15)

After the dialogue pass (`docs/dialogue_translation.md`, 1,187 rows), every other piece of Japanese in the game was translated. This page lists what was covered and where it is, and the small set of things that are deliberately not translated.

## Coverage

| Source | What | Count | Work file (local, has Japanese) | Committed copy (no Japanese) |
| --- | --- | --- | --- | --- |
| EBOOT strings | Menus, system/save/replay messages, help lines, skills, titles, unlock messages, gallery labels, song credits, unit/weapon names, pilot table | 3,184 distinct | `work/translation/en/ui.json` | `ui.en.json` |
| `data/menu/text/*.csv` | Unit descriptions (`ms_ext`), pilot profiles (`pilot_ext`), pack descriptions (`pack_ext`), the rest of `nn_ext` | 250 distinct | same | same |
| `data/locate/*.csv` | Mission unit display names | 91 distinct | same | same |
| | **ui.json total** | **3,525 distinct strings, 5,848 occurrences**, 100% translated | | |
| `data/locate/*.csv` | Internal labels (demo, portrait and dummy entries) | 51 distinct, 216 rows | `internal_labels.json` | `internal_labels.en.json` |
| Textures (GIM) | Text drawn into images: menu labels, buttons, panels, shop, results, mission title cards, HUD alerts, tip cards, copyright | 504 textures | `images/img_*.json` | `images.en.json` |
| Textures (GIM) | Japanese-script series logos and tags (the Macross Plus katakana tag on 101 stills plus 101 thumbnails, the era and mission logos, the title-screen reading): **kept as they are** | 223 textures (reference only) | `images/img_logos.json` | `images.en.json` |
| `data/tbl/camera.tbl` | Developer comments (never shown) | 50 lines | `camera_tbl.json` | `camera_tbl.en.json` |

The dialogue corpus (narration, briefings, FES lines, shop titles) is covered in `docs/dialogue_translation.md`.

## Process

1. **Text.** `tools/build_ui.py` builds the corpus: one row per distinct Japanese string, with every occurrence listed. Prefills:
   - 316 rows reuse the dialogue translation (`tm`);
   - 1,013 formulaic gallery labels are filled by rule (`tools/prefill_rules.py`).
   12 translator agents covered 15 slices. Each examined every row of its slice, and every slice passes `tools/ui_slice.py check` with 0 errors. The check covers placeholders, line breaks, Shift-JIS encodability, in-place byte limits and avoid-list names.
2. **Consistency and proofreading.** Four meaning proofreaders covered all 3,525 rows except the rule-filled gallery labels, which were verified separately. They made 41 fixes (A 24, B 4, C 9, D 4), plus 4 harmonisation fixes: the composer Atsutaka Kawauchi, Vector Productions, "(Giant)", and Seikan Hikou without the macron.
3. **Images.** `tools/gim.py` decodes all GIM textures; 4,726 in the menu, cockpit and script folders were checked. Five agents viewed every contact sheet in scope and opened candidate textures at full size: art 129 sheets, menu A 29, menu B 27, script 24, cockpit 18. Every texture with Japanese was transcribed and translated, with its size, kind and drawing style recorded for the redraw. `tools/images_export.py` checks that every source file exists and that no English contains Japanese.
4. **Insertion dry runs pass.**
   - `insert_text.py`: all CSV cells, including the unit lists and internal labels.
   - `eboot_insert.py`: 3,509 of 3,575 EBOOT strings translated (dialogue plus UI), and the loader-simulation check is ok.
   The remaining 66 EBOOT strings contain no Japanese words.

## Deliberately not translated

- **140 strings with no Japanese words:** full-width digits and symbols such as `０１２３４５６７８９`, `ＮＯ　ＤＡＴＡ` and `－－－－`, and the renderer's ASCII glyph map (`eboot:347EEC`). The two `。` tail strings belong to their parent string, which is translated.
- **Series logos (decided 2026-10-15: keep):** the official Japanese-script logos and series tags stay as they are and are not redrawn. That covers the era and mission logos, the Macross Plus katakana tag on 101 stills and 101 thumbnails, and the title-screen reading. Their English titles stay in `img_logos.json` for reference only, flagged `keep_original`. Only the plain-text images (504 textures) are redrawn.
- **3D model textures** (`data/arms`, `data/ms`, `data/weapon`, `data/map`, `data/effect`; about 5,600 textures): this is surface art. All 4 effect sheets and samples of the weapon and map sheets were viewed, and no Japanese was found. They were not checked one by one.
- **Byte-pattern hits** in `.gfp`, `.png`, `.fgc` and `.bin`: binary data (images, collision, conversion tables), not text. The cockpit agent confirmed the `.gfp` portrait packs have no text.

## Open points

- **Widths are unmeasured for most of this text.** Some agents measured with the VWF font (slices 12 and 14). Pilot profiles and long weapon names will need refitting; see `tools/check_widths.py`, `work/ui/width_report.md` and `docs/text_limits.md`.
- **Image redraw is not done.** `images.en.json` records each texture's size, style and any short-form fallbacks; GIM re-encoding has not been written yet.
- **Uncertain renderings:** flagged rows carry their reason in `notes`. The main ones:
  - Name readings: Kannara, Ortek, Molly, Kariba and Oigul (glossary entries marked `needs_check`).
  - Credit names: "Son Rui" and "Yuna Katsuki" in the Burning Fire credit.
  - "Gojappe".
  - A few HUD short forms.
- **Name rule:** where the game writes ミハエル, profiles and labels use "Michael"; unit-name suffixes use the nickname "Michel" (as mecha.json requires).
