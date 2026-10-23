# Song lyrics in missions

The patched game can show a song's lyrics at the top of the screen while the
song plays in a mission. Lyric working files are excluded from the repository.
Public patches normally omit their text; the user explicitly authorized the
v0.7.15 release to include the English lyrics and romaji. Fill the templates yourself, or draft them
from locally supplied audio at your request using the workflow below.

Status (v0.7.12, 2026-10-23): the mechanism works in PPSSPP 1.20.4 with
placeholder lines (see "Testing"). No real lyrics are included. Not tried on
real hardware.

Local continuation (v0.7.14, 2026-10-23): at the user's request, Whisper drafts
now fill the ignored templates for 29 tracks, with 304 English captions.
`bgm79`, `bgm80`, and `bgm81` remain empty because no reliable words were
recognized. The local ISO and its lyric tails pass file checks; the draft
words and timing still need review in game. See CHANGELOG and the handoff.

Local continuation (v0.7.15): romaji is displayed above English wherever a
Japanese source reading is available. The 29 tracks now contain 306 display
captions, 239 with romaji across 27 tracks. All 304 English captions from
v0.7.14 are preserved; two were split to keep the combined display within
three rows. English-only refrains stay in English. Source readings and timing
remain drafts; the three previously withheld tracks are still empty.

## Filling in the lyrics

1. Make the empty templates (once; existing files are never overwritten):

   ```bash
   python tools/lyrics.py templates
   ```

   This writes one file per song to `work/translation/en/lyrics/<song_id>.json`
   (32 songs, see the table below). `--all` also makes templates for the
   instrumental tracks.

2. Open a song's file and fill in `lines`, one entry per lyric line, in play
   order:

   ```json
   {
     "song_id": "bgm03",
     "title": "Do You Remember Love? (Vocal)",
     "file": "PSP_GAME/USRDIR/data/sound/bgm/bgm03.at3",
     "duration_sec": 108.7,
     "loop_start_sec": 1.73,
     "loop_end_sec": 108.75,
     "lines": [
       {"start_sec": 12.0, "end_sec": 16.5, "text": "first line of the song"},
       {"start_sec": "0:17.2", "text": "second line\nwith a second row"}
     ]
   }
   ```

   - `start_sec` / `end_sec`: seconds from the start of the file, as a number
     (`12.5`) or a string (`"1:02.5"`). Leave `end_sec` out and the line lasts
     until the next one starts (at most 6 s).
   - `text`: plain ASCII is safest (the English VWF font). `\n` starts a second
     row. A line is wrapped to the 290 px box automatically; at most 3 rows.
     Curly quotes, dashes and `…` are converted; `{` is not allowed (it starts
     a colour code in the game's text routine).
   - Only `lines` is read; the other fields are there to help you.
   - The game's file is a short "game size" edit (about 0:30 to 2:00), not the
     full single. Time the lines against this file: play it in any player that
     reads ATRAC3 (foobar2000 with the vgmstream plugin, or VLC), or watch the
     placeholder build (below), which shows the time on screen.
   - Files with `"same_as": "bgm01"` are the very same recording as that song
     (the game has 8 such pairs among the songs). Leave their `lines` empty and
     they show that song's lines.
   - The song loops: after `loop_end_sec` it continues from `loop_start_sec`,
     and so do the lyrics.

3. Check the files:

   ```bash
   python tools/lyrics.py check
   ```

   It reports bad times, overlapping lines, and lines too wide for the box.

4. Build a local ISO with them:

   ```bash
   python tools/build_iso.py 0.7.12-lyrics --lyrics work/translation/en/lyrics --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json
   ```

**Keep lyric working files outside git.** `work/translation/*/lyrics/` remains
in `.gitignore`. Adding `--lyrics` puts that text into the resulting patch.
The user explicitly authorized this for the v0.7.15 release on 2026-10-23;
earlier local-only notes describe the policy before that request. Future
releases need explicit authorization to include lyric text. Builds without
`--lyrics` show nothing for songs.

### Drafting from locally supplied audio

At the user's request, the local song audio can be transcribed and translated
with the installed faster-whisper environment. This does not fetch lyrics from
the web. Keep the resulting text and audio private, in the ignored directories.

```text
work/source/whisper_venv/Scripts/python.exe tools/lyrics_transcribe.py --widths work/output/build_0.7.13/vwf/vwf_widths.json
work/source/whisper_venv/Scripts/python.exe tools/lyrics_transcribe.py --widths work/output/build_0.7.13/vwf/vwf_widths.json --write
```

The first command previews the songs to process. The second uses the cached
large-v3 model on the GPU, saves Japanese transcription and English translation
segments to `work/source/lyrics/bgmNN.json`, and fills empty lyric templates
with English captions. Populated templates are preserved. Exact duplicate
recordings continue to inherit through `same_as`.

Every exported caption is marked `review_required`: Whisper can mishear
singing, omit words, or invent text over instrumental passages. Obvious credit
hallucinations, untranslated segments and repeated vocalizations are filtered. Segment times are
estimates; a long caption is split proportionally to fit two rows. Review the
words and timing against the audio before treating the draft as finished.

### Adding romaji

`tools/lyrics_romaji.py` derives ASCII Hepburn romaji from the saved Japanese
ASR segments, using fugashi/UniDic-lite readings and pykakasi. Long vowels use
ASCII spellings such as `ou` and `uu`. Romaji appears above the English at the
existing font size; long captions are split within their original interval
so the combined display never exceeds the three-row, 290 px box.

Dependencies in `work/source/whisper_venv`: `fugashi==1.5.2`,
`unidic-lite==1.0.8`, `pykakasi==2.3.0`. Preview before writing:

```text
work/source/whisper_venv/Scripts/python.exe tools/lyrics_romaji.py --widths work/output/build_0.7.14/vwf/vwf_widths.json
work/source/whisper_venv/Scripts/python.exe tools/lyrics_romaji.py --widths work/output/build_0.7.14/vwf/vwf_widths.json --write
```

The tool backs up all English-only templates in the ignored directory
`work/source/lyrics/english_only_v0.7.14/`. Reruns use that backup, preventing
romaji from being added twice. Local reading corrections and short-crop ASR
retries are recorded in `work/source/lyrics/romaji_sources.json` and
`romaji_retry_results.json`; the converter loads the corrections when present.
Summary: `work/source/lyrics/romaji_report.json`.

Generated rows retain separate `en` and `romaji` fields for review, plus the
combined `text` that the game actually displays. If editing a generated row
directly, update `text` too. Romaji has the same transcription uncertainties
as the source; word placement inside each ASR segment is approximate.

To try the display without lyrics, `--lyrics-placeholder` gives every BGM
file test lines every 6 s: "bgm03 line 1 at 0:02", "bgm03 line 2 at 0:08", ...

## The songs

The game names its music in a table of 93 entries in the EBOOT (`0x377D00`,
16 bytes each: name, track number, flags, sound-test order, volume, credits).
Entry N is `PSP_GAME/USRDIR/data/sound/bgm/bgmNN.at3`, a plain file on the
disc (not in `macross.dat`): ATRAC3, stereo, 44.1 kHz, about 66 kbps, with a
loop (`smpl` chunk). 86 of the 93 files exist; 54, 55, 75 and 90-92 are
unused names.

A track counts as a song when its credits name a singer or a lyricist, plus
the three game-original song skills (Sara, Ishtar, Myung), whose credits name
nobody (vocals not checked). That gives 32 songs (`python tools/lyrics.py
list`; `--all` lists all 86 tracks):

| Song id | Title | Plays as | Length | Loop | Same recording as |
| --- | --- | --- | --- | --- | --- |
| bgm01 | Fire Valkyrie (Song Weapon 2) | song weapon / SPA of a unit | 1:00.00 | 0:07.61-1:00.08 |  |
| bgm02 | Mylene Valkyrie (Song Weapon 2) | song weapon / SPA of a unit | 0:55.11 | 0:00.05-0:55.16 |  |
| bgm03 | Do You Remember Love? (Vocal) | mission BGM | 1:48.70 | 0:01.73-1:48.75 |  |
| bgm05 | Mylene Valkyrie (Song Weapon 1) | song weapon / SPA of a unit | 1:05.26 | 0:03.38-1:05.10 |  |
| bgm06 | Sharon (Skill: Sharon's Temptation) | song skill | 1:32.57 | 0:01.85-1:32.64 |  |
| bgm10 | My Boyfriend is a Pilot (Vocal) | mission BGM | 0:59.00 | 0:00.06-0:59.06 |  |
| bgm12 | INFORMATION HIGH (Vocal) | mission BGM | 1:32.57 | 0:01.85-1:32.64 | bgm06 |
| bgm16 | Totsugeki Love Heart (Vocal) | mission BGM | 1:00.00 | 0:03.23-0:59.57 |  |
| bgm18 | HOLY LONELY LIGHT (Basara) | mission BGM | 1:00.00 | 0:07.61-1:00.08 | bgm01 |
| bgm19 | HOLY LONELY LIGHT (Mylene) | mission BGM | 0:55.11 | 0:00.05-0:55.16 | bgm02 |
| bgm21 | MY FRIENDS (Vocal) | mission BGM | 1:05.26 | 0:03.38-1:05.10 | bgm05 |
| bgm24 | Ranka (Skill: Kira☆) | song skill | 1:14.92 | 0:01.71-1:14.99 |  |
| bgm25 | TRY AGAIN (Vocal) | mission BGM | 1:37.16 | 0:00.08-1:37.24 |  |
| bgm27 | Lion (Vocal) | mission BGM | 1:27.76 | 0:14.95-1:27.81 |  |
| bgm30 | Sheryl (Skill: Galactic Fairy 1) | song skill | 1:24.36 | 0:00.06-1:24.42 |  |
| bgm31 | Sagittarius ☆ 9 PM Don't be late (Vocal) | mission BGM | 1:42.19 | 0:17.90-1:42.25 |  |
| bgm35 | Sheryl (Skill: Galactic Fairy 3) | song skill | 1:23.32 | 0:07.74-1:23.40 |  |
| bgm44 | Minmay (Skill: Do You Remember Love?) | song skill | 1:47.04 | 0:00.09-1:47.13 |  |
| bgm51 | Fire Valkyrie (Song SPA) | song weapon / SPA of a unit | 1:37.16 | 0:00.08-1:37.24 |  |
| bgm56 | Fire Valkyrie (Song Weapon 1) | song weapon / SPA of a unit | 1:00.00 | 0:03.23-0:59.57 | bgm16 |
| bgm57 | Sheryl (Skill: Galactic Fairy 2) | song skill | 0:58.92 | 0:02.45-0:58.97 |  |
| bgm61 | Seikan Hikou (Vocal) | mission BGM | 1:53.57 | 0:18.26-1:53.63 |  |
| bgm62 | Northern Cross (Vocal) | mission BGM | 1:36.85 | 0:20.98-1:36.91 |  |
| bgm65 | DYNAMITE EXPLOSION (Vocal) | mission BGM | 1:00.42 | 0:00.09-1:00.50 |  |
| bgm67 | Infinity #7 (Vocal) | mission BGM | 0:58.92 | 0:02.45-0:58.97 | bgm57 |
| bgm69 | VF-19P (Song Weapon 1) | song weapon / SPA of a unit | 1:00.42 | 0:00.09-1:00.50 | bgm65 |
| bgm79 | Sara (Skill: Song of Destruction) | song skill | 1:46.44 | 0:51.67-1:46.52 |  |
| bgm80 | Ishtar (Skill: Emulator) | song skill | 0:31.15 | 0:02.30-0:31.20 |  |
| bgm81 | Myung (Skill: VOICES) | song skill | 1:20.79 | 0:00.05-1:20.84 |  |
| bgm82 | Fold Speaker (Song Weapon 1) | song weapon / SPA of a unit | 1:14.92 | 0:01.71-1:14.99 | bgm24 |
| bgm83 | Fold Speaker (Song Weapon 2) | song weapon / SPA of a unit | 1:12.76 | 0:00.05-1:12.81 |  |
| bgm89 | Burning Fire (Vocal) | mission BGM | 1:36.99 | 0:00.06-1:37.05 |  |

"Plays as" comes from the table's own names: "(Vocal)" tracks are mission
music (chosen in the hangar's BGM list, or Random), "Skill:" tracks play when
that singer's skill is used, "Song Weapon" / "Song SPA" tracks when a unit
fires its song weapon. The mission scripts (`data/script/*.fes`) all carry the
same block of singer skill names (`minmay`, `minmay2`, `basara`, `sheryl`,
`sheryl2`, `ranka`, `ranka2`, `sharon`, `minmay_last_shooting`, ...); they do
not name files. The instrumental tracks (the game's own music, the
instrumental versions, jingles) are listed by `--all`.

The game also plays custom music from the memory stick
(`ms0:/MUSIC/MUF/BGMnn/`); those files get no lyrics.

## How it works

### Where the lines are stored

At the end of the song's own file, after the RIFF data:

```
... ATRAC3 RIFF file ... | zero pad to 4 | blob | u32 blob_len | "LYR1"
blob = u32 loop_start, u32 loop_end, u32 count,
       count x (u32 start, u32 end, u32 text offset from the blob start),
       the texts (Shift-JIS, NUL-terminated, "\n" between rows), zero pad to 4
```

Times are in samples (44,100 a second). The RIFF sizes are not changed, so the
ATRAC decoder never reads the tail. The files grow by a few hundred bytes to a
few KB; `iso_patch.py` moves a grown file to the end of the image, and
`relayout_iso.py` keeps the original order for release images.

### How a song plays

The sound code has three channels, each with one ATRAC stream object (0x6C
bytes, class at `0x3C0F90`): channel 0 plays the BGM, 1 the voice clips, 2 a
third stream. A BGM file is loaded **whole** into the stream's data buffer
(stream `+0x34`, its size at `+0x30`; checked in PPSSPP: 905,948 bytes for
`bgm78.at3`, the file's size), so the lyrics tail arrives with the song: no
extra read and no extra memory beyond the tail itself.

Each stream runs in its own sound thread. Starting it calls the method
`0x26C8DC`, which hands the buffer to `sceAtracSetDataAndGetID` (call at
`0x26C8F0`); the thread then decodes with `sceAtracDecodeData` (call at
`0x26CA88`, about 2,048 samples at a time, a little ahead of the speaker) and
loops the song with `sceAtracSetLoopNum(-1)`.

### EBOOT hooks (`tools/lyrics_patch.py`)

| Hook | Site | What it does |
| --- | --- | --- |
| SET_HOOK | `0x26C8F0` (`jal sceAtracSetDataAndGetID`) | makes the call, then records the stream for its channel (`+8`), sets the channel's sample counter to 0 and gives it a start number |
| DEC_HOOK | `0x26CA88` (`jal sceAtracDecodeData`) | makes the call, then adds the samples decoded to the channel's counter |
| DRAW_HOOK | `0x140D68` (end of the mission 2D layer) | runs the previous target (the voice subtitles' hook, or `0x1A024C`), then draws the current line |

The counter follows the music: it stops when the sound is paused and does not
move for a song that is loaded but silent. DRAW_HOOK picks the channel that
decoded within the last 20 frames, has a `LYR1` tail, and was started last
(so a song skill wins over the mission BGM). The song time is the counter
minus a lag of 2,048 samples (the decoder's lead), folded back into the loop
after the loop end. The line whose `[start, end)` holds that time is drawn
with the game's text routine `0x15ABC0`, a black shadow 1 px down-right, then
the text.

| Parameter | Value | Why |
| --- | --- | --- |
| position | x 240, top at y 4, lines going down (alignment 3) | the top band between the partner/team panels (left, up to x 91) and the mission timer (right, from x 392); the voice subtitles use the bottom centre (y 208-248) |
| size | 12 px, VWF font | as the voice subtitles |
| box | 290 px (x 95-385) | wider lines are wrapped by `lyrics.py`; the game shrinks anything still wider |
| line step | 13 px | three rows end at y 43, still left of the radar (x 408 on) |
| colour | pale yellow `0xFFA0F0FF` (ABGR) | tells lyrics from speech |
| depth | 0xFFFF | nearest, like the voice subtitles |
| lag | 2,048 samples | the decoder runs that far ahead |

These are 11 config words at `0x2A2654`, so a layout or the lag can be tried
live through the PPSSPP debugger.

**Space used.** 208 words of code at `0x2A1A5C` and 32 state/config words at
`0x2A2600`, in a run of unused VFPU vector helpers (`0x2A1A5C-0x2A26DC`,
800 words, no relocations; no call, jump or pointer reaches them). The three
replaced words are `jal` with an R_MIPS_26 relocation, which stays valid for
the new target; the new code carries no relocation (it finds its load address
with `bal`). The state words are 0 in the EBOOT.

## Testing

PPSSPP 1.20.4, a portable copy with the debugger on its own port, build
`work/output/Macross Ultimate Frontier (EN v0.7.12).iso` (placeholder lines in
all 86 BGM files, plus the normal voice subtitles). Screenshots:
`work/ui/screens_0.7.12_lyrics/` (local).

- The grown files load and play: the BGM stream's buffer size was the new file
  size (bgm71 519,056, bgm66 855,812, bgm18 487,060 bytes) with `LYR1` at its
  end, at the title screen, in Free Play Versus and in Co-op.
- The channel 0 counter runs at real time (about 5.0 s of music per 5 s).
- Attract-mode demo battle: "bgm78 line 1 at 0:02" at the top, the voice
  subtitle at the bottom.
- Free Play Versus, bgm66 (Random): "line 2 at 0:08" at 10.3 s, "line 3 at
  0:14" at 15.3 s. After the loop end (105.6 s) the time folds back: at
  113.9 s it showed "line 3 at 0:14" (113.9 - 105.6 + 5.6 = 13.9 s, then
  14.0).
- Co-op "Of Sea and Wind" with HOLY LONELY LIGHT chosen (bgm18): lines follow
  the song with the campaign HUD, also with 2D Display OFF (the HUD goes,
  the lyrics stay). Screenshots taken between two reads of the counter: the
  gaps between lines (18.5-20.0 s, 24.5-26.0 s) showed nothing, the lines in
  between showed the right line.
- The pause menu hides the lyrics; the music, and so the counter, keep going
  there, so the lines are still in step after Resume.
- Two-row lines (texts rewritten in RAM): centred, the second row 13 px lower.
- The patch also assembles on an EBOOT without voice subtitles (it then calls
  `0x1A024C` itself) and refuses to patch an EBOOT twice.

Not checked: whether the lines match the singing by ear (no real lyrics were
used; the timing is the decoder's sample count, a few hundredths of a second
ahead of the speaker minus the lag); song skills and song weapons (the test
save has no singer unlocked: they use the same stream code, but which channel
they play on was not seen); real hardware.

## Limits

- Lyrics show only in missions (the hook is in the mission's 2D layer), not
  in menus or the sound test.
- Two songs at once: the one started last is shown.
- Banners such as "ALLIED ARMY EXISTS" at the start of a mission cover the
  top-left of the band for a moment; the lyrics are drawn on top of them.
- Timing is by decoded samples, not checked against the singing by ear.
  Shift a song by changing its times, or all songs with the lag word.
  Real hardware not tried.
- Custom memory-stick music gets no lyrics.
