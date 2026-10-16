# Data formats: Macross Ultimate Frontier (PSP, NPJH-50050, Japan)

How the game's data is stored, and where the translatable text is. Everything
here was worked out from the files in `PSP_GAME/USRDIR`; the EBOOT is encrypted
and `SYSDIR/BOOT.BIN` is zero-filled, so no code was read.

All integers are little-endian. Offsets are from the start of the structure
unless stated.

## Tools

| Tool | What it does |
| --- | --- |
| `tools/muf_archive.py extract <USRDIR> work/source/dat` | Unpacks `macross.dat` and `fileset.dat` into one tree, `work/source/dat/data/...`, and writes the layout to `work/source/dat/_meta/`. |
| `tools/muf_archive.py repack work/source/dat <out> [--base <USRDIR>]` | Rebuilds `macross.idx`, `macross.dat` and `fileset.dat`. With `--base`, members whose content is unchanged are copied from the original instead of being re-compressed. |
| `tools/muf_archive.py verify <a> <b>` | Compares the three files by MD5. |
| `tools/muf_lzss.py` | The member codec (XOR + LZSS). |
| `tools/dump_text.py` | Dumps the text to `work/source/text/*.json`. |
| `tools/glossary_check.py` | Matches the names in the dump against `work/glossary/` and writes `work/glossary/gaps.json`. |
| `tools/gim.py` | Decodes GIM textures to PNG and encodes them back (see "GIM textures" below). |
| `tools/redraw_images.py` | Redraws the Japanese text in textures in English (`docs/image_redraw.md`). |

Round trip, checked on 2026-10-15 (MD5 of all three files identical to the ISO):

- `repack --base`: about 6 s.
- `repack --jobs 10` with no base, so every one of the 27,487 fileset members is
  re-compressed from the extracted files: about 3 minutes.

When a file grows, the repacker moves everything after it and rewrites the
offsets in all three index copies. This was tested by adding 5 KB to
`mission_ext.csv`, then repacking and extracting again.

## USRDIR layout

| File | Size | Content |
| --- | --- | --- |
| `macross.idx` | 690,370 | Master index (PIDX0 v2): directory tree of `macross.dat` + table of filesets in `fileset.dat`. |
| `macross.dat` | 680,689,664 | PIDX0 v1 copy of the tree, then 15,782 raw files. |
| `fileset.dat` | 292,388,288 | PIDX0 v1 copy of the fileset table, then 1,834 FSTS bundles. |
| `data/sound/bgm/*.at3` | | Background music, plain ISO files. |

`macross.dat` holds the voice clips (14,234 `data/sound/voice/*.at3`),
loading-screen pictures, sky and environment models, sound banks and the
`data/extra` files (fonts, `jis2ucs.bin` / `ucs2jis.bin` conversion tables,
logos). Everything else, including all menus, scripts and text, lives only
in `fileset.dat`.

`fileset.dat` groups files by the moment the game loads them
(`GameFlowCampaignCreate`, `round_const`, `mz_320_load`...). A file needed in
several places is stored once per fileset: 65,203 members, 27,487 different
paths. A path always has the same bytes in every fileset, and 1,351 paths are
also in `macross.dat` with the same content. That is why the extracted tree
can merge everything: **edit a file once and the repacker updates every
copy.**

## PIDX0 header (`macross.idx`, and the head of both .dat files)

| Offset | Type | Field |
| --- | --- | --- |
| 0x00 | char[8] | `PIDX0\0\0\0` |
| 0x08 | u32 | version: 2 in `.idx`, 1 in the .dat heads |
| 0x0C | u32 | entry table offset |
| 0x10 | u32 | entry count (15,796; 0 in `fileset.dat`) |
| 0x14 | u32 | root entry count (1; 0 in `fileset.dat`) |
| 0x18 | u32 | fileset table offset |
| 0x1C | u32 | fileset table size (4 = empty) |
| 0x20 | u32 | name table offset |
| 0x24 | u32 | name table size |
| 0x28 | 0x28 × n | container slots: u32 name offset, 20 zero bytes, 16-byte id. `.idx` has two (`macross.dat`, `fileset.dat`); each .dat head has one, carrying the same id as its slot in `.idx`. The ids are not MD5s of the files. They look like build ids, and the repacker leaves them alone. |

**Entry (24 bytes)**: `u32 type, u32 name_offset, u32 a, u32 b, u32 c, u32 d`.
- Directory (type 1): `a` = child count, `b` = index of the first child.
  Entry 0 is the root directory `data`.
- File (type 0): `a` = name offset of its container (0 = `macross.dat`),
  `b` = offset in `macross.dat`, `c` = size, `d` = 0. Files are not compressed.

**Fileset table**: `u32 count`, then `count` u32 pointers (relative to the
table) to 20-byte records: `u32 name_offset, u32 container_name_offset,
u32 offset, u32 size, u32 member_count`. Records are sorted by name.

**Name table**: NUL-terminated ASCII names. Each copy (`.idx`, each .dat head)
has its own name table, so the name offsets differ between copies. Paths are
built by walking the directory tree.

The `.idx`, the `macross.dat` head (0x0–0x9A000) and the `fileset.dat` head
(0x0–0xF000) are three copies of the same layout. The repacker keeps them as
templates in `work/source/dat/_meta/` and patches the offset and size fields.

### Alignment

- `macross.dat`: each file starts on a 0x800 boundary, or a 0x8000 boundary
  for `data/sound/voice/` (streamed clips). The file is padded to the alignment
  of its last file (0x8000).
- `fileset.dat`: each FSTS bundle starts on a 0x800 boundary. There is no
  padding after the last one.
- All padding is zero bytes.

## FSTS bundle (inside `fileset.dat`)

| Offset | Type | Field |
| --- | --- | --- |
| 0x00 | char[4] | `FSTS` |
| 0x04 | u32 | member count |
| 0x08 | u32 | 0x20 (entry table offset) |
| 0x0C | u32 | name table offset (= 0x20 + 16 × count) |
| 0x10 | u32 | name table size |
| 0x14 | 12 bytes | zero |
| 0x20 | 16 × count | `u32 name_offset, u32 data_offset, u32 unpacked_size, u32 packed_size` |
| | | name table: full paths (`data/menu/text/mission_ext.csv`), NUL-terminated, in entry order |

Member data starts on 0x10 boundaries and follows the entry order. The bundle
is padded to 0x10, and the fileset record size includes that padding.

### Member encoding

```
+0  4 bytes  20 33 3B 31  "RAIC" ^ 0x72  -> LZSS-compressed (63,372 members)
             20 33 3B 30  "RAIB" ^ 0x72  -> stored, not compressed (1,831 members)
+4  u32      unpacked size (not XORed)
+8  ...      payload, every byte XORed with 0x72
```

The LZSS is Haruhiko Okumura's `LZSS.C`: 4096-byte ring buffer, maximum match
18, threshold 2, write position starts at 0xFEE, and flag bytes are read LSB
first (1 = literal). A reference is 2 bytes: `offset = b0 | (b1 & 0xF0) << 4`,
`length = (b1 & 0x0F) + 3`. Two details differ from the textbook code:

- The window starts filled with **0x00**, not spaces.
- The lookahead was not cleared between files. Bytes past the end of a very
  short input were non-zero, which changes one 24-byte member
  (`data/menu/setting/a2a_null.a2a`). `muf_lzss.LOOKAHEAD_FILL = 0xFF`
  reproduces it, and any non-zero value would.

With both details, the binary-tree encoder in `tools/muf_lzss.py` re-creates
every compressed member byte for byte. Stored (`RAIB`) members stay stored.
Members that are new or edited are written with the mode they had before.

## File types (extracted tree)

| Extension | Count | What |
| --- | --- | --- |
| `.at3` | 14,241 | ATRAC3 audio (RIFF), almost all voice clips |
| `.vad` | 14,176 | Data paired with the voice clips (not analysed) |
| `.gim` | 10,360 | PSP GIM textures (`MIG.00.1PSP`). Many contain **text drawn as images** (see below) |
| `.gmo` | 1,367 | PSP GMO models (`OMG.00.1PSP`) |
| `.a2a` | 902 | 2D layout/animation (`A2A `), refers to `.gim` by name |
| `.gfp` | 202 | Cockpit portrait packs (`.GFP1.00` header + GIMs) |
| `.fes` | 246 | Mission scripts, `FES 3.04` |
| `.csv` | 307 | Shift-JIS tables: menu text, mission unit lists, AI formations, paths |
| `.fgc` | 89 | `.FGC` collision/geometry |
| `.fnt` | 4 | Fonts: `gpsp3_font14.fnt` (342 KB, main) and three small ones (`_en`, `_em`, `_es`) |
| `.tbl` | 1 | `camera.tbl`, camera parameters (Japanese comments only) |
| `.pbd/.phd/.pef` | 15 | Sound banks |
| `.png`, `.bin` | 8 | Icons, `jis2ucs.bin` / `ucs2jis.bin` |

## Where the text is

All text found in the archives is **Shift-JIS (cp932)**. No UTF-16 text was
found: the scanner's UTF-16 hits were all pixel or float data.

### 1. `data/menu/text/*.csv`: menu and story text (main source)

Shift-JIS, CRLF line ends, no BOM, **no quoting**: a cell can never contain an
ASCII comma or a double quote. `tools/insert_text.py` writes `|` and `` ` ``
instead, and the VWF font draws those slots as `,` and `"` (`docs/build.md`).
A line break inside a cell is the two characters `\n`, which the game
expands. The first row is the header, and the first column is the key. Every
row ends with a comma (an empty last cell).

Briefing stories (`strStory`): each line is copied into an 80-character slot
without a bounds check. A line of 80 characters or more runs into the next
line's slot (seen in game, `docs/text_limits.md`), so a line can hold at most
79 characters. A line wider than the panel is squeezed horizontally to fit.

| File | Rows | Columns | Content |
| --- | --- | --- | --- |
| `mission_ext.csv` | 264 | `eMissionID, strMission, strStory` | Mission objective (shown in mission select) and the briefing story. 216 missions have text. **This is the game's story script.** |
| `ms_ext.csv` | 102 | `id, strDescription` | Unit descriptions. The first line is the unit's display name. |
| `pilot_ext.csv` | 93 | `eId, strDescription` | Pilot profiles, ending with the voice actor `（ＣＶ：…）`. |
| `pack_ext.csv` | 32 | `eId, strDescription` | Equipment pack descriptions, first line = pack name. |
| `nn_ext.csv` | 1,858 | `eId, (text)` | Nyan-Nyan shop / collection names: 0000–0073 pilots (with series headers), 1000–1129 units, 2000–2216 songs, weapons, formations, 3000–3999 gallery captions, 4000s, 5000–5299 player titles and quotes, 6000–6231 figures. |

### 2. `data/script/*.fes`: mission scripts

Binary (`FES 3.04`). The **u16 at 0x12 is the offset of the string pool**,
which runs to the end of the file as NUL-terminated strings. Most strings are
ASCII identifiers: voice-clip ids (`ope00`, `o0_om0`), unit labels
(`PLAYER1`, `ENE010`), events. 232 strings are Japanese: mission objectives
shown during play (`…を撃破せよ`) and tutorial instructions with real newline
bytes. Other header fields are unknown.

Header, as u16 words after the magic (m7_330): `0x3C, 0x1C, 0x13B0, 0x14A0,
0x9D74, 0xA348 (pool), 0x9DDA, 0xA330, 0xA330, 0xA330`. Only the pool offset
is known.

**String references** (worked out 2026-10-15). The script code is a stream of
u16 words. A string is used by the instruction

```
0x0080, k, <u16 offset from the start of the pool>      k = 0, 1 or 2
```

The offset counts from the pool start, not from the start of the file. Each
of the 232 Japanese strings in the 246 files has exactly one such reference
(144 with k = 0, 87 with k = 1, 1 with k = 2). Other words that happen to
equal a string offset follow other opcodes (`0x004A`, jumps or data) and are
not string references.

So the pool can grow at the end: an English string is appended after the last
string and its one reference is repointed (`tools/insert_text.py`). Nothing
else in the file moves. The limit is the pool offset, not the file size: the
largest pool is 0x2C28 bytes, and the tool keeps new offsets below 0x8000 in
case the game reads them signed. The game reads files past 0xFFFF bytes
already (the largest is 0x1066A).

The in-mission radio chatter is voice only (`sound/voice/*.at3`, cut-in
portraits from `.gfp`). No subtitle text was found.

### 3. `data/locate/*.csv`: mission unit lists

The third column `表示名` is the unit's display name (pilot or object). Rows
with `デモ用` / `顔絵用` / `ダミー` are internal. Whether the rest are shown in
game (lock-on labels?) has not been confirmed. 1,070 rows, 205 distinct
names. The other columns are AI and placement data.

### Not covered by the dump

- **EBOOT.BIN**: system messages, menu labels, option and save texts are in
  the executable, not in any CSV. They are dumped separately by
  `tools/dump_eboot.py`; see "EBOOT text" below.
- **Text drawn into GIM images**: menu titles and buttons (`menu/*`), loading
  screens (`menu/load/*.gim`, 1,028 files in `macross.dat`), the briefing and
  gallery screens, cockpit labels (`cockpit/2d_ope_*.gim`, `script/fesrat/*`).
  They are transcribed in `work/translation/en/images/` and redrawn by
  `tools/redraw_images.py`; see "GIM textures" below and `docs/image_redraw.md`.
- `data/formation/*.csv`, `data/path/*.csv`, `tbl/camera.tbl`: internal
  labels and comments only.

## GIM textures (`tools/gim.py`)

All 10,360 `.gim` files are `MIG.00.1PSP` files with one image and one
palette. Layout: a 16-byte file header, then blocks with a 16-byte block
header (`u16 id, u16 unk, u32 block size, u32 next, u32 data offset`).
Block ids: 2 root, 3 picture, 4 image, 5 palette, 0xFF file info (source
file name, author, date, "GimConv 1.42"). Every file has the blocks
2, 3, 4, 5, 0xFF in that order.

The image and palette blocks start with a plane header: `u16 header length,
u16, u16 format, u16 pixel order, u16 width, u16 height, u16 bpp align,
u16 pitch align, u16 height align, ...`, and at +0x1C the offset of the
pixels from the plane header.

| Format | Meaning | In the game |
| --- | --- | --- |
| 0 / 1 / 2 / 3 | RGBA5650 / 5551 / 4444 / 8888 | none |
| 4 | INDEX4 (two pixels per byte, low nibble first) | 6,356 images |
| 5 | INDEX8 | 4,004 images |

Pixel order 1 is the PSP swizzle: the plane is cut into blocks of 16 bytes
by 8 rows, stored block row by block row. 10,339 images are swizzled, 21
are not. A row is padded to a multiple of 16 bytes, and a swizzled plane
to a multiple of 8 rows. Every palette in the game is a 1-row RGBA8888
plane, not swizzled: 16 entries (6,354 files), 256 (4,005) or, once, 21. Alpha is 0–255 (not the PS2
0–128 range).

### Encoding

`gim.encode(original_bytes, rgba_image)` writes the new pixels into a copy of
the original file, so the format, swizzle, palette format, palette size,
padding bytes and the file-info block stay as they were:

- **Indexed textures.** If every colour of the new image is already in the
  palette, the palette is kept and every pixel keeps its old index wherever
  that index still has the right colour (duplicate palette entries stay as
  they were). Otherwise the image is reduced to the palette size with a
  k-means over its distinct colours, weighted by pixel count and seeded with
  the old palette, using an alpha-weighted (premultiplied) colour distance.
- **RGBA textures.** The colours are packed back to the texture's own format
  (5650, 5551, 4444, 8888). Unpacking then packing every 16-bit value gives
  the same value back for all 65,536 values of each format.
- The file size never changes, so the archive offsets of the other members
  do not move.

Round trip, checked on 2026-10-15: `python tools/gim.py roundtrip work/source/dat/data`
decodes and re-encodes all 10,360 textures; all are byte-identical to the
originals.

## Text dump (`work/source/text/`, gitignored)

| File | Entries | Characters |
| --- | --- | --- |
| `menu_text.json` | 2,517 | 54,757 |
| `fes_strings.json` | 232 | 5,799 |
| `locate_names.json` | 1,070 | 7,960 |
| `eboot_strings.json` (`tools/dump_eboot.py`) | 3,575 | 50,825 |

Each entry has a stable `id` (`mission_ext:MA_010:strStory`, `m7_330:2335` =
pool offset in hex, `m7_310:3:FRINKB` = row number and unit label,
`eboot:38F6A0` = file offset in the decrypted EBOOT), the `source` file, its
position, and `jp`.

## EBOOT text (decrypted 2026-10-15)

The EBOOT can be decrypted with the installed PPSSPP: run a portable copy (the
PPSSPP folder copied with `installed.txt` deleted, so it uses `memstick/` next
to the exe) with `DumpFileTypes = 3` under `[General]` in
`memstick/PSP/SYSTEM/ppsspp.ini`, boot the ISO, and PPSSPP writes the
decrypted ELF to `memstick/PSP/SYSTEM/DUMP/NPJH50050_EBOOT.BIN` (5,388,288
bytes, `\x7FELF`). A copy is kept at `work/source/eboot/EBOOT.dec.bin`
(gitignored).

The ELF holds 3,575 Japanese strings (Shift-JIS, NUL-terminated, 4-byte
aligned, all in `.rodata`): menu labels, system and save messages, skill and title
names, unlock messages, gallery captions, song credits, and the **era
prologue/epilogue narration** at 0x38F6A0–0x3927F0 (223 lines, one string
per on-screen line). Between scenes there are ASCII camera labels
(`cam_event_pr_mp_00`...). These are not text. Scene names are assigned by
start offset in `tools/build_dialogue.py`.

No subtitle text for the in-mission voice chatter exists anywhere: not in the
archives (`.vad` files are 48-byte lip-sync data) and not in the EBOOT. The
radio dialogue is voice only.

`work/source/eboot/strings.json` and `strings_clean.json` are an earlier
byte-pattern scan (no references, some float data). They are superseded by
`work/source/text/eboot_strings.json`.

### PRX layout

The decrypted EBOOT is a PRX (ELF type 0xFFA0, MIPS Allegrex). The section
headers and the relocation table are intact, so every address in the module
is known.

| Program header | vaddr | File offset | Size | Contents |
| --- | --- | --- | --- | --- |
| LOAD 0 | 0x000000 | 0x0000A0 | 0x3C14C8 | `.text`, `.rodata` (file = vaddr + 0xA0) |
| LOAD 1 | 0x3C1500 | 0x3C1580 | 0x3EB84 file, 0x1324300 memory | `.data`, then `.sbss`/`.bss` from 0x400090 (file = vaddr + 0x80) |
| 0x700000A0 | | 0x400110 | 0x122790 | relocations, 8 bytes each |

A relocation is `u32 r_offset, u32 r_info`: type = bits 0–7, the segment
`r_offset` is relative to = bits 8–15, the segment the address points into =
bits 16–23. Counts: 30,111 `R_MIPS_32` (pointer words), 30,688 `HI16`, 36,959
`LO16`, 50,964 `R_MIPS_26` (jal). A stored address is relative to the segment
named in bits 16–23: for segment 0 that is the vaddr, for segment 1 it is
`vaddr - 0x3C1500`. The loader adds the load address of that segment (the
game loads at 0x08804000, so segment 1 starts at 0x08BC5500).

`.rodata` is 0x2CC4D0–0x3BE234 (file 0x2CC570). The text sits in
0x38294C–0x3BD890, mixed with ASCII asset paths and number tables.

| File offset | Contents |
| --- | --- |
| 0x3829EC–0x38B912 | song names, mission names and objectives, weapon and unit descriptions (765) |
| 0x38BD0C–0x38D89C | factions, boss and character names, load/save errors, name entry |
| 0x38E6A8–0x3937B8 | skills, then the narration (0x38F6A0–0x3927F0), era menu captions |
| 0x3948A4–0x39739C | pack names, mode and menu help lines (137) |
| 0x398724–0x39E434 | gallery captions (`Ｆ：キャプチャ０３４` ...), wait/comms messages (1,030) |
| 0x3B0B98–0x3B5CDC | battle settings, replay/save messages, ranks, factions |
| 0x3B6308–0x3B9F56 | parameter names, player titles and their unlock conditions, unlock messages (605) |
| 0x3BA614–0x3BD92E | password and shop messages, song credits (161) |
| 0x35D908–0x363808 | the pilot table (vaddr 0x35D868, 152 records of 0xA0 bytes, name at +0) |

### `eboot_strings.json`

`python tools/dump_eboot.py` reads `work/source/eboot/EBOOT.dec.bin`. Each entry
has these fields:

- `id` `eboot:<file offset>`, the same ids the narration rows in
  `dialogue.json` use. `offset` is the file offset, `vaddr` the module address,
  `section` the section.
- `bytes`: Shift-JIS length without the NUL. `capacity`: bytes free in place,
  terminator included. It counts the zero bytes that follow, but stops at the
  next address anything points at. For the pilot table it is the narrowest
  field width in the table (32).
- `jp`: the text, with real newlines. `%s`/`%d` and `{m...}`/`{l...}` are
  format and colour codes. Keep them.
- `refs`: every reference to the string's first byte:
  - `{"kind": "ptr", "vaddr", "offset", "section", "table"}`: a 32-bit pointer
    word. `table` = the run of pointer words it belongs to (`start`, `stride`,
    `index`, `count`). Contiguous words of a struct array count as one run.
  - `{"kind": "code", "insn", "lo", "lo_offset", "hi", "hi_offset"}`: the
    address is built in code by `lui` (`hi`, can be several on different
    paths) + `addiu` (`lo`). `loader_lo` is set when the loader takes the
    `lui` carry from a different LO16 (see below).
- `inline_copy`: code also reads the bytes directly (an inlined fixed-length
  `strcpy` with `lwl`/`lwr`). Six strings: `不明`, `ＮＯ　ＤＡＴＡ` ×2, the
  dash line, the digit table and `×０`. The copy length is in the code, so
  making the string longer has no effect until that code is patched.
- `tails`/`tail_of`: the compiler merged a string into the end of a longer one
  (2 cases: `。` inside the two "mode unlocked" messages). Moving the long
  string must keep a copy of the tail, or repoint it.
- `inner_refs`: addresses referenced inside the string, merged tails of any
  kind. Four strings: an ASCII `"B"` that is the last byte of a final `。`
  (0x81 **0x42**), and empty strings that sit on another string's NUL. These
  strings can move, but their old bytes must stay.
- `in_place`: never moved. This covers the pilot table and the ASCII map at
  0x347E4C (`note` says which).

Totals: 3,277 strings are reached only through pointer words (4,507 words:
3,360 in `.rodata` tables, 1,147 in `.data` structs), 147 strings also through
code (209 `lui`/`addiu` pairs). 266 strings have more than one reference. The
narration shares strings between screens: row 135 (`%s and %s`) is in both the
Plus (file 0x31AB38) and Macross 7 (0x31ABF8) epilogue tables. An edit has to
read right in every place. 151 strings have no reference: the pilot names in
the pilot table (fields of 32–36 bytes, `capacity` says how many). The code
indexes the records, so these names can only be edited in place. The first
record (`工藤　シン`, the default player name) is the table base and has
code references; it is in place only, too.

How the references were found: the HI16 entries are not stored next to their
LO16, so pairing them in list order gives wrong addresses. The tool pairs each
LO16 with the `lui` that sets its base register on every path to it (a
backwards walk over the control-flow graph, with delay slots and likely
branches handled). Check: for all 30,687 HI16s that are used, the LO16 the loader
uses for the carry gives the same carry as the real pairs. 604 LO16s
cannot be paired (values in saved registers across a switch). They are
`lw`/`sw`/`addiu` on struct and `.bss` addresses, and none of them leads to text.

### Relocating EBOOT strings (`tools/eboot_insert.py`)

BASE_RULES wants relocation, not squeezing into the old bytes. `eboot_insert.py`
does this:

```
python tools/eboot_insert.py [--eboot E] [--dump D] [--out O] [--expand N] [--move-all] [--gap-only] [--dry-run] <translations.json>...
python tools/iso_patch.py "<original>.iso" work/output/<name>.iso PSP_GAME/SYSDIR/EBOOT.BIN=<O>
```

Translation files are row lists with `id` (`eboot:...`) and `en`, the same
shape as `dialogue.json`. The output is a decrypted EBOOT, which PPSSPP and
CFW load as it is. For each translated string:

1. In-place strings (`in_place`, `inline_copy`, no references) are written
   over the old bytes and must fit `capacity`. Otherwise the tool stops with
   an error.
2. Every other string moves. Space is taken first from the old slots of
   moved strings, rounded up to 4 bytes, but never a slot with `inner_refs`.
   After that it uses the new gap. Identical texts share one copy.
3. References are patched:
   - Pointer words get the new address, relative to its segment.
   - The `lui`/`addiu` pair gets `(rel + 0x8000) >> 16` and `rel & 0xFFFF`.
   - The relocation entries get the segment of the new address (bits 16–23).
   - Every patched HI16 entry is moved in front of its own LO16. The loader
     takes a HI16's carry from the next LO16 in the list. The carry depends
     on the low half of the segment's load address (0x4000 for segment 0,
     0x5500 for segment 1), so it is only safe when that next LO16 is the
     HI16's own. The order of entries does not matter otherwise.
4. **The gap.** The tool moves `.sbss`/`.bss` (from 0x400090) up by N × 64 KB
   and writes the text there, between `.data` and `.bss`. The space is file
   data at the end of LOAD 1. The shift is a multiple of 64 KB, so no LO16
   changes. Only the HI16s and pointer words that point into `.bss` change:
   11,999 `lui` immediates and 182 words. Each HI16's targets lie on one side
   of 0x400088, and the tool stops if one does not. LOAD 1 `filesz`/`memsz`,
   the relocation header offset and the section headers are updated. By
   default N is the smallest number that fits the text.
5. **Check.** The PSP loader is simulated at 0x08804000 on the input and the
   output. Every paired pointer and `lui`/`addiu` must land on the same object
   as before: the new home of a moved string, `.bss` + the shift, or the same
   address. The moved text is compared byte for byte.

Tests (2026-10-15, PPSSPP 1.20.4):

- No translations: the output is byte-identical to the input.
- `--move-all --gap-only`: all 3,417 movable strings were put into a 128 KB gap
  (106,012 bytes). The game boots and shows the autosave notice, folder
  prompts and main menu help lines from the new addresses.
- Narration (`dialogue.json`) plus three longer English help lines: they were
  shown correctly. A help line can be longer than the old Japanese bytes.
- The same, on top of the VWF EBOOT from `tools/vwf_build.py` (run
  `dump_eboot.py` on that EBOOT first, and pass `--eboot`/`--dump`): the
  proportional font and the relocated English work together.

Space: the old slots hold 100,824 bytes of text. English came out 1.34× the
Shift-JIS bytes in the narration, so a full translation needs about 135 KB:
the old slots plus one or two 64 KB chunks. Memory: the module already ends
at 0x09EE9800, which leaves about 1.1 MB of the 24 MB user memory, and each
chunk takes 64 KB of that. The tests ran fine with 128 KB, but nothing beyond
the main menu was played.

### Rendering ASCII

The table at file 0x347EEC (vaddr 0x347E4C) maps ASCII 0x20–0x7F to
full-width Shift-JIS codes. The text routine at 0x157398 looks up `char * 2`
in it, so English written in ASCII is drawn with full-width glyphs. The map is
not exact: `<` → Ⅰ, `>` → Ⅱ, `@` → ㌔, `^` → ν, and `` ` `` and `{|}~` become
spaces (`{` is also the start of a format code). Without the VWF patch, ASCII
is drawn on a fixed pitch of about 9 px (the Japanese glyphs take about 12 px),
so a help bar takes about 35 characters. A centred line that is too long is
cut off at both ends. `tools/vwf_build.py` makes the 14 px font proportional.
It rewrites this table so that all 96 codes 0x20–0x7F get their own English
glyphs; the special mappings above are gone after that patch (see
`docs/vwf.md`).
In the game font, `⑳` (0x87 0x53) is drawn as ™. The Japanese save messages
use it after メモリースティック. Also not
text: the Shift-JIS list at file 0x3F771C (6,953 characters, 13.9 KB, with no
direct reference). It is probably the font's glyph order.
