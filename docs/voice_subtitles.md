# Voice-clip subtitles

During missions the characters talk over the radio: a portrait (the "cut-in")
opens and a voice clip plays. The game has no text for these lines. Since
v0.7.0 the patched game shows an English subtitle while each clip plays.

Status (v0.7.0, 2026-10-16): working in PPSSPP 1.20.4 (see "Testing"). Not
tried on real hardware.

## Results

| | Clips |
| --- | --- |
| Voice clips | 14,215 (plus 19 sound effects, not subtitled) |
| **With an English subtitle** | **12,489** |
| Silent placeholder clips (no voice in the game) | 1,155 |
| Sound but no words (drums, screams; Whisper or translator) | 439 |
| Repeats of such clips | 89 |
| Era prologue narration (already English text on screen) | 43 |

Translation: 144 slices of 80 rows (`work/translation/en/voice/slices/`),
plus 2,358 repeats (a clip whose transcript repeats an earlier clip of the same
character) that take the first clip's English. Translator flags on the
11,454 slice rows: `whisper_doubt` 1,224 (transcript corrected from context),
`uncertain` 439, `no_subtitle` 223, `unfinished` 73 (lines that trail off; most
still have English), `name_missing` 68, `kept_omission` 25. Every flagged row
has an English note.

## Pipeline

| Step | Tool | Output |
| --- | --- | --- |
| 1. Transcribe every clip | `tools/voice_transcribe.py` (faster-whisper large-v3, CUDA) | `work/source/voice/transcripts.json` (local: Japanese) |
| 2. Retry clips that look like Whisper hallucinations | `tools/voice_transcribe.py --retry` | same file, flag `hallucination` on the ones that stay bad |
| 3. Work file: speaker, series, missions, transcript | `tools/voice_rows.py` | `work/translation/en/voice/voice.json` (local) |
| 4. Translate in 80-row slices | agents, `docs/voice_translation_brief.md`, `tools/voice_slice.py show/check` | `work/translation/en/voice/slices/vslice_NNN.en.json` (committed) |
| 5. Append each line to its clip | `tools/voice_subs_at3.py` | overlay `data/sound/voice/<clip>.at3` |
| 6. EBOOT hooks that read and draw the line | `tools/voice_subs_patch.py` | patched `EBOOT.BIN` |

Steps 5 and 6 run inside `tools/build_iso.py` with `--voice-subs <file>`
(`--voice-placeholder` shows each clip's id instead, to test the hooks).

## The clips

`data/sound/voice/` in `macross.dat` holds 14,234 ATRAC3 clips: 14,215 voice
clips `v<prefix>_<num>.at3` and 19 sound effects. Each voice clip has a 48-byte
lip-sync file `data/sound/vad/<clip>.vad` in the `round_const` fileset bundle:
u32 length in frames at 60 fps, u16 at +6 = 2 (the step), then mouth keys.

`<prefix>` is the face id of the cut-in portrait (`data/menu/face_*/<prefix>_*.gim`).
`work/translation/en/voice/speakers.en.json` names all 79 speakers:

- `o0_of0/of1/of2/om0` and `os_mis`: the selectable operators (Yuu, Claire,
  Pinon, Itsuki) and Misa. They read the same script in their own manner;
  numbers 1000+ are mission lines.
- `p0_om0..2`, `p0_of0..2`: the six selectable custom pilots.
- `p<series>_<name>`: named characters (a Zero, s SDF, i DYRL, z Zentradi,
  p/x Plus, 7 Macross 7, d Protodeviln, g Dynamite 7, f Frontier, y Galaxy and
  Vajra, h Zero's SV-51 pilots, 2 Macross II).

Pilot numbers mean the same situation for every pilot: 000-020 launch,
100-198 combat, 300-371 skills and results, 600-699 story lines for given
missions, 900-905 the era prologue narration (already on screen as English
text, so no subtitle).

The mission scripts (`data/script/*.fes`) do not name clips. They hold
numbers in their string pools (`"124"`) and pick the speaker from the unit
(`PLAYER1`, `FRIGAM`...); the operator chosen in the menu picks `vo0_*`.
`voice_rows.py` lists, for each clip, the missions whose pool holds its
number. It is a hint only: the pools hold other numbers too.

## Whisper

`faster-whisper` 1.2.1, model large-v3, float16 on an RTX 3070 Ti, Japanese,
beam 5, a short hotword prompt with Macross terms (反統合同盟, バルキリー,
可変戦闘機...), no VAD. About 0.3-0.5 s per clip, about 2 hours in all.
The venv is `work/source/whisper_venv` (Python 3.11).

Quality: ordinary speech is good (operators read clearly). Typical errors are
homophones and wrong kanji (半島合同盟 for 反統合同盟, ご縁 for 護衛), which the
translators fix from context; the five operators reading the same script
cross-check each other. Whisper fails on:
- shouts and long held cries (repeated characters, cut to six);
- processed voices (Gepelnitchi), drums (Veffidas never speaks), chanting and
  Vajra cries: it invents "episode 1, episode 2..." lists, "thanks for
  watching", or echoes the hotword prompt.

`--retry` re-runs those without the prompt and with the VAD filter (81
transcripts improved). The 1,392 clips that stay bad are flagged
`hallucination` and get no subtitle. Measured: **1,155 of them are silent
placeholder clips** (peak below -60 dB, many byte-identical, 1.5 or 3 s): the
game ships no voice for Gepelnitchi, Sharon Apple's enemy form (`px_sra`), the
Vajra, the Zentradi soldier, most of Boddole Zer and about a third of Minmay's
clips. The other 237 have sound but no words (Veffidas's drums, sound effects,
held screams). Every row keeps
Whisper's own flags (`logprob`, `nospeech`, `repeat`), and translators add
`whisper_doubt` where they corrected the transcript.

## Where the line is stored

At the end of its own clip, after the RIFF data, in `macross.dat`:

```
... RIFF ATRAC3 clip ... | part 1 NUL [part 2 NUL ...] | u16 len | u16 parts | "SB"
```

`len` counts all parts with their NULs. The RIFF size field is not changed,
so the player never reads the tail. Voice clips sit on 0x8000 boundaries, so
most clips do not even move.

Why not the `.vad` files: they are all in one fileset bundle (`round_const`,
14,436 members) that the game keeps in memory during missions; growing it by
about 500 KB could exhaust memory on a real PSP. The clip tail costs no
memory: the hook reads only the last 0xB8 bytes of one clip.

## EBOOT hooks (`tools/voice_subs_patch.py`)

**Read.** The mission script queues a radio line by loading the clip's `.vad`
into one of two voice slots with the exact-size reader `0x21A00`: `0x1A0A14`
fills slot 0, `0x1A38E4` slot 1. Both calls go to READ_HOOK. It makes the same
call, then builds `data/sound/voice/<clip>.at3`, normalises it (`0x37C60`),
looks it up in the `macross.dat` index (`0x3A9B8`: container, offset, size,
packed) and reads the last 0xB8 bytes (`0x39560`, a read at an offset). With
an `SB` tail it keeps a pointer to the line and its number of parts for that
slot. It also remembers where slot 0 is (from the game's own pointer, so the
.bss shift of `eboot_insert.py` does not matter).

**When.** A queued clip can wait while the other slot plays, so the line
follows the lip-sync, not the load. The game counts a slot's frames (30 fps)
only while its clip plays (`0x1A0AD0`), from 0 to length / step; the counters
are words at slot 0 - 8 and - 4. A slot's line shows while its counter runs
and for 24 frames after. Part i of n shows from i/n of the clip on.

**Draw.** The mission's 2D layer `0x140D38` draws the HUD (`0x170A38`), or only
the cut-in windows while a camera scene runs (`0x19FAD4`), and always ends
with the cut-in step `0x1A024C` (call at `0x140D68`). That call goes to
DRAW_HOOK: it runs `0x1A024C`, then draws the line with the game's text
routine `0x15ABC0` twice, a black shadow 1 px down-right, then white.

| Parameter | Value | Why |
| --- | --- | --- |
| centre | (240, 228) | bottom centre, between the HP bars and the weapons panel |
| alignment | 0 | centred both ways on (x, y), so 1-3 lines stay around y = 228 |
| size | 12 px | VWF font (GenEi), HD glyphs at 2x/4x |
| box | 232 px | x 124-356; the routine shrinks a wider line |
| line step | 13 px | |
| depth (z) | 0xFFFF | nearest. With the game's 0xFF00 the "enemy appeared" banner bars and some HUD panels hid the text |

These are 9 config words at `0x174300`, so a layout can be tried live by
writing them through the PPSSPP debugger.

**Space used.** READ_HOOK: 136 words in an unused GU projection routine
(`0x2A0B70`). DRAW_HOOK: 117 words after the VWF width table in the unused
SDK matrix routine (`0x2A4FD4`). Data: scratch buffers in the unused function
`0x1740F8` after the VWF helper (it holds relocated words, which only matters
for code), and the state words and config in its run without relocations
(`0x1742F0-0x174327`), set to 0 in the EBOOT so nothing shows before the first
clip. Nothing calls or points to these routines. The three replaced words are
`jal` with an R_MIPS_26 relocation, which stays valid for the new target; the
new code carries no relocation (it finds its load address with `bal`).

## Length

At 12 px the box holds about 38 characters per line. A line is wrapped to
232 px with the VWF advances, at most 3 lines per part; a longer line becomes
2-3 parts. The whole line must fit in 178 bytes (`voice_slice.py check`).
Translators aim for about 15-17 characters per second of audio.

## Limits

- Only clips the mission script queues get a subtitle. Clips played another
  way (menus, the era prologue, character select voice samples) do not; the
  prologue already shows English text.
- With the game's "2D Display" option off, whether subtitles still show was
  not checked.
- Two lines spoken at once (both slots playing) show one subtitle, slot 0 first.
- Parts follow the clip at even steps, not the actual phrasing.
- Transcription errors that the translators could not settle are flagged
  `whisper_doubt` / `uncertain` in the slices.
- Not tested on real hardware. The extra file read per queued clip is 0xB8
  bytes from the clip that is about to stream anyway.

## Testing

PPSSPP 1.20.4, a portable copy with the debugger on its own port (45690).
Checked in the v0.7.0 build in the first Zero mission ("Of Sea and Wind"):
the intro camera cut-ins (Luis, Yui), the "enemy appeared" / "allies
sighted" banners (Pinon, Shin), mission start, and radio lines during play
with the HUD (an operator's two-line report, pilot barks). Screenshots:
`work/ui/screens_0.7.0/` (local). Other missions were not played. The tools used: `tools/ppsspp_ctl.py`,
plus memory reads of the hook state (slot pointer, counters, hold) to check
the timing.
