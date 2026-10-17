# Redrawing the text in textures (v0.4.1, 2026-10-15)

```bash
python tools/redraw_images.py
```

This redraws the Japanese text drawn into game textures (GIM) in English.
It reads the transcriptions in `work/translation/en/images/img_*.json` and the
layout in `work/ui/redraw_layout.json`, and writes:

| Output | What |
| --- | --- |
| `work/output/redraw/overlay/data/...gim` | The re-encoded textures, for `muf_archive.py repack --overlay` (gitignored) |
| `work/ui/redraw_preview/sheet_*.png` | Before/after contact sheets of every texture, after palette reduction (what the game will show) |
| `work/ui/redraw_preview/report.json` | Per text item: the text drawn, font size, horizontal squeeze, whether a short form was used |
| `work/ui/redraw_preview/shared_text.json` | Which textures share text (below) |

It takes about two minutes. `--only <part of a path>` redraws a few textures
into `work/ui/redraw_preview/_only/`; `--no-write` skips the GIM files.
`tools/build_iso.py` runs it as step 4b into the build overlay
(`--no-images` leaves it out).

The contact sheets show the original Japanese textures next to the new ones,
so `work/ui/redraw_preview/*.png` is gitignored (game art and Japanese
script). `report.json`, `shared_text.json` and the layout file have no
Japanese and can be committed.

## Scope

504 rows in `img_menu_a`, `img_menu_b`, `img_script` and `img_art`, in 483
textures (one texture can hold several rows: the button-guide atlas has 15).
`img_logos.json` is never read: the official series logos are kept
(decision 2026-10-15). `img_cockpit` is empty.

| Result | Textures | Rows |
| --- | --- | --- |
| Redrawn and written to the overlay | 479 | 499 |
| Kept as art (not changed) | 4 | 5 |

(The row for the big Nyan-Nyan brush logo is kept, but its texture,
`nyan_shutter.gim`, is written because its other row is redrawn. The two
stamps in `f_008.gim` are lines of a redrawn row.)

The copyright lines on the title screen (`menu/title/title.gim`) and in the
screenshot viewer (`menu/gallery/ssctrl/ss_copyright.gim`) were held out of
0.4.0 because the row notes ask for approval before legal text is changed.
The user approved them on 2026-10-15; they ship from 0.4.1 as
`©… BIGWEST` and `©2007 BIGWEST/MACROSS F PROJECT/MBS`. The layout still
supports `"hold"` (preview only) for any later case like this.

From 0.7.3 the title screen also shows the build version and the group name
in the bottom-right corner ("v0.7.3" over "github.com / retro-trans"), as in
the other retro-trans releases. They are two items on `title.gim` with their
own `text` and erase mode `keep`; `{version}` in an item's text is filled from
`redraw_images.py --version`, which `build_iso.py` passes. A run without it
draws "vdev".

Kept as art, following the row notes and the logo decision:

- `menu/load/f_003.gim` and its gallery thumbnail: the cropped in-scene poster
  in the anime still ("low priority, could be left as is").
- The Nyan-Nyan restaurant logo and seal stamps: `menu/shop/nyan_parts_seal.gim`,
  `menu/shop/shop_attention_base.gim`, the big brush logo in
  `nyan_shutter.gim`, and the two stamps in `menu/load/f_008.gim` (the other
  text in those two textures is redrawn).

Other choices:

- Restricted cards (`limit_*`): the small kanji tag is erased and left blank, as the
  row notes suggest; "LIMIT" is already drawn below.
- No-partner cards (`no_partner_*`): "WAIT" (the note's short form); "STAND BY"
  is already drawn below.
- Tactical analysis counter: the hundred-million and ten-thousand separators are
  erased and the counter word at the end becomes "shots" (row note).
- Control config: "Forward" is spelled out where the note allows it; the
  transform buttons say "Transform (Fighter)" etc., as the notes suggest.
- `mm32.gim` (debug stage banner): the trailing kanji is erased; "TEST" stays.

## How a texture is redrawn

For each texture, every item first **erases** its box, then every item
**draws** its text:

1. Text: the row's `en` (or one line of it, `line`), or the item's `text`,
   then its `fallbacks` (the short forms from the row notes).
2. Fit (`fit()` in the tool): first the font may shrink a little
   (to 86 %) without squeezing, then the text may be squeezed horizontally
   down to 84 %, at any size down to `min_size`. If the full text cannot fit
   that way, the short forms are tried the same way. Only then is the text
   squeezed hard (down to `xscale_min`). Nothing overflows in the current
   layout; three short forms are used (`Wthr` twice, `DEF TGT SEEN`).
3. Render: Noto Sans JP or Noto Serif JP (variable weight, SIL OFL 1.1, the
   same family as the VWF font), drawn at 4x and box-filtered down. Effects
   are layers under the fill: glow (blurred mask), shadow (offset mask),
   outline (dilated mask). The fill can be a vertical gradient (silver and
   metal labels). Italic is a shear.
4. Encode: `gim.encode()` quantizes the result back to the texture's own
   palette size (see `docs/formats.md`, "GIM textures").

### Erase modes

| Mode | Use |
| --- | --- |
| `clear` | Text on a transparent texture (most labels, title cards, HUD alerts) |
| `fill` | Flat plate of one colour (given) |
| `row` | Every row takes the colour of a text-free column (`sample_x`): plates with horizontal bands or scanlines |
| `col` | The same for columns |
| `plate` / `vplate` | Linear interpolation across the box from the pixels left/right (or above/below) of it: gradients (rank ribbons) |
| `copy` | Copy another area of the same texture |
| `inpaint` | Fill from the surrounding pixels (diffusion); with `color`/`tol`/`grow` only the pixels near the text colour are replaced. Used over pictures (stage banners, the anime stills, the tutorial banner) |
| `frost` | Blur and darken the box (available, not used now) |

Several modes can be listed for one item; they run in turn.

### Layout file (`work/ui/redraw_layout.json`)

- `styles`: named presets (font, weight, size, min_size, colour or gradient,
  outline, glow, shadow, italic, caps, tracking, align, line spacing, squeeze limits).
- `rules`: glob patterns for families (`common_*_w.gim`, `2d_ope_*.gim`,
  `*_title.gim`, …). The first matching rule is the base.
- `files`: per-texture entries, merged over the rule. Keys: `style`, `set`
  (style overrides), `items`, `keep` (leave as art), `hold` (preview only),
  `prefer_replace` (a spelled-out form tried first), `style_by_row` (pick a
  colour preset from the row's style words, e.g. red/yellow/green HUD alerts).
- Item keys: `row`, `line`, `text`, `fallbacks`, `box`, `erase`, `erase_box`
  (one box or a list), `share`, `blank`, `no_text`, `keep`, and any style key.
- `thumbnails`: gallery thumbnail → the still it is made from.

Boxes were measured from the textures (bounding boxes of the old glyphs and
the plates around them). Two textures needed in-game corrections:

- The game draws `common_guide_period.gim` / `common_guide_room.gim` only up
  to about x = 64 (the old text width), so the text has to fit there
  ("Switch Era" is squeezed; the short forms are "Era" / "Room").
- `gal_record_list_base.gim` (six dim buttons) has the bright
  `gal_record_list_*.gim` label drawn over the selected button. Both now use
  the same box and size (offset +6, +7/+35/+64/+94/+123/+151), so the bright
  label covers the dim one exactly.

### Loading-screen tip cards (`mac00001`–`mac00008`)

These are typeset as a whole (`tipcard()`): line 0 is the speaker, then the
title (1 or 2 lines), the body, and the sign-off (1 or 2 lines, right-aligned).
Headings (■ ●) and ★ lines start at the margin, "- " lines are bullets, other
body lines are indented continuations; the Ranka card aligns its
"button: action" table on the colon. The font size (8–12) is the largest at
which every line fits the area (x 150–476) with at most 18 % squeeze; spare
height becomes paragraph gaps.

Erasing: bright pixels next to the blue glow inside the text area are
inpainted, then a soft dark, slightly blurred shade is laid under both the old
and the new lines, so no trace of the old glow shows. The English gets the
same white fill and blue glow.

### Gallery thumbnails

The 82×46 `picture_s/*_s.gim` thumbnails are the whole 480×272 still shrunk
(Lanczos; this matches the originals best), so they are regenerated from the
redrawn stills, keeping the old thumbnail's alpha.

## Shared text

`shared_text.json` lists them; in short:

- **_b / _w pairs** (30): the system and music menu buttons exist as a white
  copy and a black copy (cursor on/off). Both copies get the same text, size
  and position.
- **_on / _off pairs**: none among the 504 rows.
- **Normal / `_light`** shop items (8 pairs): same text. The normal
  "Wallpapers" texture is only 24 px wide, so both use "Walls" (`share`).
- **`con_font` / `con_window`** (12 pairs): the same control label, grey on
  transparent and white on a black box.
- **191 mission title cards** (`script/fesrat_m/*_title.gim`): one style
  (white, heavy, 36 px, 1 px dark outline and soft shadow), one rule. Four
  titles appear on two cards each (m7_450/451, mf_340/ms_370, mi_060/mv_028,
  mp_320/mv_012). The English subtitle textures (`*_english.gim`) stay.
- Gallery record buttons: `gal_record_list_base` and the six
  `gal_record_list_*` highlights (above).
- Auto Select / No Sortie / Restricted / Standby cards: four sizes each
  (face_s/m, mecha_s/l).
- HUD alerts: the 80×24 `2d_ope_*` banners and the `2d_rat_*` lines carry
  the same messages in two forms; the game also has wider English twins of
  both, and in game it shows the English twin and our banner together.
- Gallery thumbnails ↔ loading stills (11).

## Palette reduction

All 504 textures are indexed (INDEX4: 16 colours, INDEX8: 256). The new
image is mapped to the old palette when it can be, else reduced with a
k-means seeded with the old palette. Fully transparent pixels always keep an
exact transparent entry: without that rule, a palette entry with alpha 1
filled the empty part of every title card and showed as a faint line at its
edge in game (fixed before the v0.4.0 build).

## Tested in game (PPSSPP 1.20.4, v0.4.0)

Screenshots in `work/ui/screens_0.4.0/` (local):

| Screen | Textures seen |
| --- | --- |
| Main menu, all hangar tabs | Button-guide atlas (OK, Back, Tabs, Menu, Sortie, Viewer, Switch Era) |
| Save data | STA…AWK tiles, Squad tab, Switch Page |
| Hangar: mission | Wthr / Time / Time Limit, GND tag, OK button |
| Hangar: player | GND ONLY tag |
| Hangar: system menu (START) | Era Select, Controller, Settings, Load, Save (black cursor copy), Network, Top Menu |
| Hangar: record | Tactical Analysis panel, record list buttons, legends, totals |
| Hangar: shop | "Press ○ to enter the shop", menu items, Your Nyan-Nyan Pts / pts, Lv / Next Lv |
| Briefing | Sortie button |
| Loading screen | Tip card (Pinon Colette) |
| Mission start | Title card "Of Sea and Wind" |
| In mission | HUD alerts ENEMY INBOUND, ALLIES SIGHTED |
| Pause menu | Resume Mission, Change View, 2D Display, Abort Mission; map info panel |
| Title screen (v0.4.1) | English copyright lines |

Not seen in game yet: the gallery screenshot viewer (its copyright strip included), control config, network rooms,
results screens and the other tip cards; they are checked only in the
preview sheets. Screenshots 00, 03, 07 and 13 were taken on the first 0.4.0
build (before the transparency fix), the rest on the final one.

A faint dotted line under the mission title card is the game's own: the
Japanese disc shows it in the same place, and rows 41–47 of the new
textures are fully transparent.
