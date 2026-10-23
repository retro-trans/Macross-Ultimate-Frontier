# Changelog

## [0.7.15] - 2026-10-23 (public release, includes lyric drafts)

### Added
- Romaji above the existing English song lyrics, using the saved local Japanese ASR transcripts. ASCII Hepburn readings use fugashi/UniDic-lite and pykakasi, with particle readings and conjugated verb endings handled together. Short audio crops were retried for gaps; local reading corrections stay in ignored `work/source/lyrics/`.
- `tools/lyrics_romaji.py`: previews changes by default; `--write` saves the English-only templates before adding romaji. Reruns use that backup. Combined captions retain separate `en` and `romaji` review fields and fit the existing 290 px, three-row lyric box.
- Romaji appears in 239 display captions across 27 tracks. All 304 English captions from v0.7.14 are preserved; splitting two long captions gives 306 display captions across the same 29 tracks. English refrains and passages without a usable Japanese transcription remain English-only. The three previously withheld tracks remain empty. Readings and word timing are still drafts and need in-game review.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.15).iso`, built with `python tools/build_iso.py 0.7.15 --work work/output/build_0.7.15 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json --lyrics work/translation/en/lyrics` (log `work/output/build_0.7.15.log`). The user subsequently requested a release and explicitly confirmed including lyrics and romaji, overriding the earlier local-only rule for this version.
- Verified all 102 ISO files against the 33 replacement outputs and unchanged original files. All 306 caption records match their text and timing inputs; original song audio bytes are unchanged. Width/timing checks report no errors or warnings, and texture redraw has no overflow or missing layouts. English preservation was checked against the v0.7.14 backup. Not tested in game.
- Size: 2,223,337,472 bytes; SHA-256 `78b92d6109f103c8223de7e418e68ad4e1b30c58695c7a64e014950355cd494b`. Verification and frozen lyric inputs: `work/output/build_0.7.15/verification.json` and `lyric_inputs/`.
- Compact release image: `work/output/Macross Ultimate Frontier (EN v0.7.15 release).iso`, 1,238,335,488 bytes, SHA-256 `ad326ede78bf0e2a94dd88a4c3fc41325892134c666bb152cbb163fe0c4cffdf`. Re-laid out with `tools/relayout_iso.py`; all 102 files match the test build.
- Retro Trans release assets: full patch (4,525,410 bytes) and upgrades from the published 0.7.9 (45,712), 0.7.8 (98,032), 0.7.5 (431,330), 0.7.3 (433,494) and 0.7.1 (422,443). All six complete decode/hash round trips and the standard manifest/checksum validation pass. Source/tag commit: `86e8834e1d4094536a17f20d9aab2aea29f585c2`; metadata and notes: `docs/releases/0.7.15/`.
- Freshly launched the compact image in isolated PPSSPP 1.20.4; the debugger recognizes NPJH50050 v1.02 and a running game. Framebuffer readback was unavailable, so this session does not establish visual or gameplay verification. Lyric words and sung timing still need review.

## [0.7.14] - 2026-10-23 (private lyric draft build, not released)

### Added
- At the user's request, transcribed the locally supplied game songs with Whisper large-v3 and drafted English lyric captions. The private templates now provide 304 timed captions across 29 tracks (21 distinct recordings plus eight exact duplicates). No web lyric text was fetched.
- `tools/lyrics_transcribe.py`: read-only plan by default; `--write` uses the existing local faster-whisper environment and cached model, saves Japanese transcription and English translation segments in ignored `work/source/lyrics/`, and fills empty lyric templates. Existing populated templates are preserved. Obvious credit hallucinations, repeated vocalizations and untranslated segments are withheld.
- Corrected or withheld obvious ASR errors in the local drafts. Every caption remains marked `review_required`; transcription, translation and sung timing have not been checked by ear. Some passages are missing. Sara (`bgm79`), Ishtar (`bgm80`) and Myung (`bgm81`) have no captions because ASR did not recover reliable words. Private review details: `work/source/lyrics/review_report.json` and `review_drafts.py`.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.14).iso`, built with `python tools/build_iso.py 0.7.14 --work work/output/build_0.7.14 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json --lyrics work/translation/en/lyrics` (log `work/output/build_0.7.14.log`). Includes the 12,506 voice subtitles and actual draft captions instead of placeholder labels. Keep this ISO and its lyric text local; no public release or patch was created.
- Verified all 102 ISO files against the 33 replacement outputs and the unchanged original files. All 29 song tails contain the expected 304 captions and timing records; each original audio file is byte-identical before its appended tail. Texture redraw: 481 textures, no overflow or missing layouts. Not tested in game.
- Size: 2,219,476,992 bytes; SHA-256 `3cb7286a85e1ba43c432d0bcd2a0a0129c175dcc43bf817ee902070a6624c942`. Verification details: `work/output/build_0.7.14/verification.json`.

## [0.7.13] - 2026-10-23 (local test build, not released)

### Changed
- Local rebuild of the current English translation and 12,506 voice subtitles without the v0.7.12 placeholder lyric captions. No song lyrics are included.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.13).iso`, built with `python tools/build_iso.py 0.7.13 --work work/output/build_0.7.13 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.13.log`).
- Verified all 102 ISO files against the four build outputs and the unchanged original files; volume size and file extents also pass. Texture redraw: 481 textures, no overflow or missing layouts. Not tested in game.
- Size: 2,216,732,672 bytes; SHA-256 `e5d69477cd6500a88211d406dbf1168cfa2f671ff74b9e820b183865b366b164`. Verification details: `work/output/build_0.7.13/verification.json`.

## [0.7.12] - 2026-10-23 (test build, placeholder lyrics, not released)

### Added
- **Song lyrics in missions** (system only; `docs/lyrics.md`). While a song plays in a mission, the current lyric line is shown at the top of the screen (pale yellow, VWF font, 12 px, between the partner/team panels and the timer), clear of the voice subtitles at the bottom. The lyric text is not included: song lyrics are copyrighted, so the user fills in the templates, which stay local.
  - `tools/lyrics.py`: `list` (the 32 vocal tracks of the 86 BGM files, from the EBOOT's BGM table, with length and loop), `templates` (one `work/translation/en/lyrics/bgmNN.json` per song: title, file, length, loop, empty `lines` of `start_sec` / `end_sec` / `text`; 8 songs are the same recording as another and say `same_as`), `check`, `build` (appends the lines to the song's own `bgmNN.at3`).
  - `tools/lyrics_patch.py`: EBOOT hooks at the ATRAC stream start (0x26C8F0) and decode (0x26CA88) count the samples played per sound channel; a draw hook at the end of the mission 2D layer (0x140D68, chained after the voice subtitles) shows the line for the song time, folded back into the song's loop. 208 words of code in unused VFPU helpers (0x2A1A5C).
  - The game loads a BGM file whole into its stream buffer, so the lyrics arrive with the song: no extra read, no extra memory beyond the tail.
  - `tools/build_iso.py --lyrics <dir>` (your filled files) or `--lyrics-placeholder` (test lines "bgm03 line 1 at 0:02" every 6 s in every BGM file).
  - `work/translation/*/lyrics/` is gitignored. Never build a public release with `--lyrics`: the patch would carry the lyric text.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.12).iso`, built with `python tools/build_iso.py 0.7.12 --work work/output/build_0.7.12 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json --lyrics-placeholder` (log `work/output/build_0.7.12.log`). Same content as 0.7.11 plus placeholder lyrics in every BGM file: a test of the mechanism, not for players.
- Checked in PPSSPP 1.20.4: placeholder lines appear and change on time in the attract demo, Free Play Versus (bgm66, also after the loop end) and Co-op "Of Sea and Wind" (bgm18, also with 2D Display OFF); the voice subtitles still show. Song skills, real hardware and timing by ear were not checked (`docs/lyrics.md`, Testing).

## [0.7.11] - 2026-10-23 (test build, not released)

### Added
- **Subtitles for the Zentradi-language voice clips** (player report: Golg Boddole Zer had none in a Do You Remember Love?-era mission). These clips are in the film's invented Zentradi language, so Whisper wrote phonetic nonsense and they were flagged `no_subtitle`. They are now read with the film's published Zentradi word list (Japanese Wikipedia "Zentradi" language section and a fan word list; each row's `notes` give the words used). All are flagged `uncertain`: the meaning comes from the word list, not from the film's own subtitle.
  - Golg Boddole Zer: "Perish now, Micronians!" (vpz_bd2_106, *holt de-zants maikuraan*), "The enemy... is Protoculture!" (vpz_bd2_160, *deburan protoculture*), "Hear this! The enemy shall perish! All Zentradi forces, attack!" (vpz_bd2_600; its ending *arma zentran holt gadoras* is his attack order in the film). The game reuses these clips in nine more slots (107, 108, 161, 162, 187-189, 602, 609), which get the same lines.
  - Milia (both sizes): "Enemy!" (vps_mil_012, vps_mil_604, vpz_mil_012, vpz_mil_604, *deburan*).
  - Quamzin: vpz_qmj_310 is Japanese, not Zentradi; read as *chi ga tagiru na! omae to no sentou wa yo*: "Fighting with you gets my blood boiling!" (second half guessed).
- Voice subtitles: 12,506 of 14,215 clips (was 12,489).

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.11).iso`, built with `python tools/build_iso.py 0.7.11 --work work/output/build_0.7.11 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.11.log`). Same content as 0.7.10 plus the subtitles above. Not yet checked in game.

## [0.7.10] - 2026-10-22 (test build, not released)

### Changed
- **Nyan-Nyan Points wording** (user decision, recorded in `work/glossary/terms.json`): sentences spell out "Nyan-Nyan Points"; labels and amounts use lowercase "pts".
  - The eight shop help lines now read "Spend Nyan-Nyan Points to get ..." (u1202-u1209, was "Nyan-Nyan Pts").
  - The shop's balance label is "Your Nyan-Nyan pts" (`nyan_base_00.gim`, was "Pts"). Prices already read "800 pts".
- Mission information: time of day "Evening" is now **"Dusk"** (u0867).
- "Full Spirit" is now **"High Spirit"** (u0989; glossary updated).
- Skill descriptions brought in line with the later wording (player feedback):
  - Melee Genes: "Increase melee attack power to 3x, but can / no longer guard." (u0917).
  - Ace and Bombing King: "by 1.5x" is now "to 1.5x", and Ace starts "Increase" like the others (u0922, u0924). Galactic Fairy gets the same "to 1.5x" (u0928).
  - Clairvoyance: "Increase lock-on range to 2x and multi-lock / speed to 1.5x." (u0946).
  - Medic Squad: line break moved so "50% of their HP" stays together (u0948).

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.10).iso`, built with `python tools/build_iso.py 0.7.10 --work work/output/build_0.7.10 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.10.log`).
- Checked in PPSSPP 1.20.4 with the reported save: the shop shows "Your Nyan-Nyan pts", "800 pts" and "Spend Nyan-Nyan Points to get "Units"."

## [0.7.9] - 2026-10-21 (public release)

### Changed
- "Legendary Elixir" is now **"Phantom Elixir"** (u0925; recorded in `work/glossary/terms.json`, skills).
- Kira☆: "Momentarily freezes enemies, and self and / nearby allies gradually restore HP." (u0932; was "Freezes enemies for an instant, and you and / nearby allies gradually recover HP.").
- Skill descriptions reworded from player feedback (2026-10-21), "you" now "self" where the skill affects the user:
  - VOICES: "Self and nearby allies gradually recover HP." (u0933).
  - Emulator: "Increase self and allies' attack power to 3x, but / decrease defense to 0.5x." (u0935).
  - Do You Remember Love?: "Decrease parameters of Zentradi-type weapons / and Zentradi-piloted units; strengthen others." (u0936; the suggested "...while strengthening other weapons" needed three lines, the box holds two).
  - Spiritia Barrier: "Sivil appears in front of you and deploys a / barrier for a set time." (u0938).
  - Max World Second: "Stops movement of all but self and uses SPA. / *Hold L Button on activation to not use SPA." (u0942; shortened from the suggestion to fit 283 px per line).
  - Rolling Plus: "In Fighter mode, increase roll speed and allow / up to 4 consecutive rolls." (u0944).
  - Clairvoyance: "Lock-on range doubles, and increase multi-lock / speed to 1.5x." (u0946).
  - Medic Squad: "When rescuing your partner, they recover 50% / of their HP." (u0948).
  - Missile Disposal Squad: "Increase limit of Anti-Missile Action to 1.5x." (u0950).
  - Sabotage Squad: "Increase damage to battleships and bases to 2x." (u0952).
  - Cheer: "Restores HP to 50% when HP drops to 30% or / below. ※ One use only." (u0956).
  - Pineapple Cake: "Restores HP and grants temporary invincibility / when HP reaches 0%. ※ One use only." (u0958). The once-only notes now use the reference mark ※ as the Japanese does (Shift-JIS 0x81A6, drawn with the game's own glyph) instead of "*".
  - Drill Sergeant: "Increase experience points gained for each of / partner's parameters to 2x on mission clear." (u0960; "when clearing a mission" shortened to fit two lines).
  - Awakening: "Become temporarily invincible and awaken / at 30% HP or below. ※ One use only." (u0962; shortened to fit two lines).
  - Triangler: "Affinity changes at 2x the normal rate." (u0966).
  - Signal to Strike Back: "Recover 6 SP Gauge blocks when HP drops to / 30% or below. ※ One use only." (u0968).
  - Boost Maniac and Thrifty: "Decrease Boost / SP Gauge consumption to 75% / of normal." (u0970, u0974).
  - "Quick Recovery" is now **"Rapid Recovery"** (u0975, recorded in the glossary): "Restore HP to 100% at the start of each mission / during consecutive missions." (u0976).
  - Destroyer: "Increase unit performance when piloting / a Destroid." (u0978).
  - Tuning Fanatic: "Decrease earned Nyan-Nyan Points to 0, but / increase earned Tune Points to 2x." (u0980).
  - Outcast: "Decreases Affinity with each selected character / when a mission is cleared." (u0982; Affinity keeps its glossary capital).
  - Earplugs: "Decrease effect of all songs to 0.50x." (u0984).
  - Taunt: "Increase enemy attack power to 2x, but increase / EXP of player's parameters to 2x." (u0986).
  - Full Spirit: "Fill 3 SP Gauge blocks at start of mission." (u0990, now one line).
  - Iron Wall: "Increase defense to 2x and no longer stagger / when hit." (u0903).
  - Reflection: "Reflect beam-type shots and negate / solid-ammo attacks." (u0909).
  - Emergency Evasion: "Become invincible temporarily." (u0911).
  - Rally: "Reload all weapons, shorten attack openings, / and become invincible temporarily." (u0921).
  - Galactic Fairy: the line now breaks after "by" (u0928).
- **Prize Mode list on the save-select screen** ran past its panel (player screenshot of 0.7.8: "Remove Boarding Size Limit", "Remove Fixed-Pilot Unit Limit"). The panel draws the names at 0.85 scale and holds about 155 px in `check_widths.py` units (measured: "Remove Tune Lower Limit", 152, ends 4 px from the frame). Five of the twelve names were longer and are shortened; the Nyan-Nyan Shop list uses the same strings:
  - "Remove Unit Size Limit" (u2463, was "Remove Boarding Size Limit"), "Remove Fixed-Pilot Limit" (u2464, was "Remove Fixed-Pilot Unit Limit").
  - "Unlock Shop Line Select" (u2468, was "Unlock Nyan-Nyan Shop Line Select"), "Unlock EX Challenge" (u2469, was "Unlock EX Challenge Mode"), "Free Nyan-Nyan Shop" (u2471, was "Nyan-Nyan Shop: Everything Free").
- **Nyan-Nyan Shop price unit** read "6400NPt": the game draws the unit as three strings at fixed x after the price (the "Nyan" kanji at +0x93, "p" at +0x9C, "t" at +0xA0, size 10; code at 0x25C02C-0x25C0A4), and the English "NP" ran under the "p". The kanji string (u3025) is now "pts" (fits its 4-byte slot) and the "p" and "t" strings are emptied in place (`work/translation/en/eboot_ascii.en.json`). The number was right-aligned against +0x92, touching the unit; it now ends at +0x8F (`addiu v0, s5, 0x92` -> `0x8f` at 0x25BED4), so prices read "800 pts". The word patch is in the new `work/ui/eboot_word_patches.json` (old word checked), applied by `tools/eboot_ascii_fix.py` in build step 3b. Checked in game.
- **Nyan-Nyan Shop menu**: labels were all different sizes and changed size when highlighted. The normal-state textures are only as wide as their Japanese text (Units, Walls 24 px, Titles 25, Icons 37, Movies 38, BGM 28), and each label had been fitted to its own width, with the highlighted (47 px) versions drawn larger. Now every label, normal and highlighted, is drawn at size 10 and only squeezed sideways to its normal texture width (at most 0.82x). The leftover Japanese bullet dot before each label is erased, which gives 5 px more room. "BGM" kept the original Japanese texture and is now redrawn in the same font. Checked in game.
- **Record > Campaign Record**: "Ultimate Clear Rate" ran into the value box beside it; now **"Ulti. Clear Rate"**.
- **Record > Overall Record**: the middle labels did not line up with their values. In the Japanese texture both middle labels end at x=145, where the values end; "Times Shot Down" was left-aligned from x=89. It is now right-aligned to the same edge as "Item Completion Rate" (box narrowed so it keeps a gap after "Total Sorties"). Checked in game.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.9).iso`, built with `python tools/build_iso.py 0.7.9 --work work/output/build_0.7.9 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.9.log`).
- Release image `work/output/Macross Ultimate Frontier (EN v0.7.9 release).iso` (`tools/relayout_iso.py`, all 102 files match the build): 1,238,269,952 bytes, SHA-256 `e8620443e6c15db580b13afe31f88459386814129b664da41ee60ca91e7e031e`. Booted in PPSSPP 1.20.4: title stamp v0.7.9, the reported save loads, shop prices read "800 pts".
- Release assets: full patch (4,515,354 bytes) and upgrades from the published 0.7.8 (77,707 bytes), 0.7.5 (410,596), 0.7.3 (412,214) and 0.7.1 (402,578); source commit `19b63ce`, metadata in `docs/releases/0.7.9/`.

## [0.7.8] - 2026-10-21 (public release)

### Changed
- **All mission briefings** given the same military-briefing pass: 180 of the 432 briefing rows (`mission_ext.csv` strStory and strMission, 118 distinct texts) now say "Commencing..." for the source's "the operation now begins", "Annihilate" for its order to annihilate (was a mix with "Wipe out"), "Suppress" for "suppression", and drop contractions and casual phrasing ("we'll", "can't let them", "Get out of it", "hit the Macross all-out"). Character-voiced briefings (Basara, Sharon, Grace, the tutorials, the Chronicle profiles, the parody missions) are unchanged. Every changed row passes `fit_line.py` (at most 79 characters per strStory line).
- **Skill names and descriptions** (Player > Support > Command Skill), from player screenshots of 0.7.7:
  - "Missile Read" is now **"Missile Reading"**, description "Slow down the speed of enemy missiles." (u0914, u0915).
  - "Encouragement" is now **"Rally"** (u0920).
  - Shock Guard: "Always parry when guarding an enemy's melee attack." (u0907; was "Guarding an enemy melee attack always parries it.").
  - Flight Carnival: "○ Button: On/Off  □ Button: Change Color" (u0905).
  - Ace: "Increases attack power, speed, and boost capacity by 1.5x." (u0922; was "Attack power, speed and boost capacity increase 1.5x.").
  - Bombing King: "Increase all weapons' ammo capacity by 1.5x." (u0924; was "All weapons carry 1.5x ammo.").
  - Legendary Elixir: "Restore HP to self and nearby allies, and revive any shot-down allies." (u0926).
  - Galactic Fairy: "Increase attack power of self and allies by 1.5x and gradually restore HP." (u0928).
  - Both names are recorded in `work/glossary/terms.json` (skills).
- **Skill descriptions rewrapped to the box.** Line 1 broke well before the right edge ("You can no longer guard, but / melee attack power triples."). The box is 189 px wide and draws the text at 2/3 size, which is 283 px in `check_widths.py` units (measured from the 0.7.7 screenshots: the Encouragement line 2 at 283 px ends 1 px from the frame). 39 descriptions (u0903-u0990) now fill line 1 up to 283 px, with no one-word last line; two now fit on one line (u0933, u0974). u0936 (Do You Remember Love?) ran past the box on line 2 and is reworded: "Zentradi weapons and Zentradi-piloted units / weaken in all stats; others grow stronger."

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.8).iso`, built with `python tools/build_iso.py 0.7.8 --work work/output/build_0.7.8 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.8.log`).
- Checked in PPSSPP 1.20.4 with the reported save (Player > Support): Shock Guard and Circus Flight wrap as listed; the widest rewrapped line (283 px, u0974) fits with about 16 px to spare, tested by writing it over a description in RAM since the other skills are locked in that save.
- Release image `work/output/Macross Ultimate Frontier (EN v0.7.8 release).iso` (`tools/relayout_iso.py`, all 102 files match the build): 1,238,269,952 bytes, SHA-256 `fa9614697c3821aa4280a1e3bf6773c9a96717f04174067d68774d2ddc89fbd0`. Booted in PPSSPP 1.20.4: title stamp v0.7.8, the reported save loads to the mission list and the MA_010 briefing.
- Release assets: full patch (4,516,457 bytes) and upgrades from the published 0.7.5 (391,117 bytes), 0.7.3 (392,863 bytes) and 0.7.1 (407,363 bytes); source commit `03560b3`, metadata in `docs/releases/0.7.8/`.

## [0.7.7] - 2026-10-21 (test build, not released)

### Changed
- Unit stat "Shooting Def." is now **"Ranged Def."** (u2450, Hangar and Partner unit stats), pairing with "Melee Def.". The pilot stat "Shooting" is a different term and is unchanged.
- Pilot stat "Stamina" is now **"Endurance"**, abbreviated **END** (was STA): the Hangar pilot status panel and the stat headers on the card spec, results, character and save-select screens (5 textures; rows in `work/translation/en/images/`, three hardcoded labels in `work/ui/redraw_layout.json`).
- Both decisions are recorded in `work/glossary/terms.json` (game_system).
- **Briefing for "Of Sea and Wind"** (MA_010, MA_015), reworded to read like a military briefing: "Commencing the operation to annihilate the "Anti-U.N. Forces," / enemy of the U.N. Forces. Eliminate the Anti-U.N. TYPE-29 fighter formation." (was "...wipe out the U.N.'s foe: ..."). The line break moved so both lines stay under the 79-character slot.
- **Help bar "Tabs"** no longer touches the L/R icons: the word starts 3 px into its atlas slot (`common_guide_message.gim`).
- **Sortie button on the briefing screen** (`brief_decision_icon.gim`): the erase sampled a column inside the old Japanese glyph and left a grey band behind "Sortie", squeezed to 8 px. It is now erased with the button's own background and drawn at 9 px from 2 px further left.
- **Total Missiles Fired** read "78 6394" for 786,394: the 12 digit slots were grouped by four around the Japanese unit marks (oku, man), which the English texture leaves out. The slots are now grouped by three from the right with a small gap ("786 394"), via the new layout step `tools/a2a_patch.py` (positions in `work/ui/a2a_patches.json`, format in `docs/formats.md`). Real commas would need a code hook, since the digit texture has no comma. Checked in game: "15 589 shots".
- "Micro Missiles" is now **"Micro-Missiles"** in all 15 weapon names and descriptions (several already used the hyphen).
- "Item Collection Rate" is now **"Item Completion Rate"** on the overall-record panel (`gal_r_c_all_rate_base.gim`).
- **Full-width Latin now uses the English font.** Unit names and labels the game already had in full-width Latin (ＶＦ－２７, ＴＹＰＥ－１４, ＨＰ, Ｓ．Ｍ．Ｓ, ＦＩＲＥ ＢＯＭＢＥＲ, shop song titles) were drawn with the fixed-width Japanese glyphs ("V F - 2 7"). `tools/fullwidth.py` (build step 3c) rewrites them as ASCII: 54 EBOOT strings in place (1 byte per character, so they always fit) and 73 cells of `menu/text/nn_ext.csv` through `insert_text.py`. Digit tables and dash placeholders stay; α and × keep their glyphs (SV-51α). The names occur in no other game file, so nothing looks them up; the unit placement CSVs are not touched.
- Pack descriptions overflowing their box (reported from a player screenshot of 0.7.5: u1004 "Force-purged when add-on HP" touched the right border at 226 px): with the new spacing the widest lines of u1004 and u1003 are 196 and 194 px, so the text is unchanged. `work/output/vwf/vwf_widths.json` (read by `check_widths.py`) had stayed at the 0.6.0 widths because builds now write to `build_*/vwf`; it is refreshed from 0.7.7.
- **Even letter spacing, exact sub-pixel text.** Gaps between letters varied by up to about a pixel (loose "Turni ng", tight "Melee", "Shi n"). Three causes, three fixes:
  - Font build (`tools/vwf_font.py`): each glyph took the sub-pixel position that looked sharpest and a left margin that depended on its own ink. Every glyph's pen now sits 1 px into its cell.
  - Advances: the bearing table holds whole pixels at 14 px (i 3.75 -> 4, e 6.25 -> 6) and the printer rounded each letter again at smaller sizes. A byte table at 0x158D54 now holds each glyph's (integer - true advance) in 1/64 px; the printer's two advance blocks call a routine at 0x157560 that uses the exact advance, rounds once for the whole-pixel pen and carries the remainder to the next letter.
  - Drawing: the remainder (-0.5..0.5 px, font descriptor +0x28) is passed to the sprite emitter 0x157F10, which moves the glyph's texture u by that fraction of the cell, so each glyph is drawn at its exact position (1/56 px steps on the 4x page). The shadowed-text emitter 0x15E644 (help bars, record screens), which draws each glyph up to six times, gets the same shift in all six passes (without it, the help line read "overal l records ac ross").
  - Measured in game at 4x on the 10 px stat labels: "Turning" gaps 3,5,4,5,6,3 (the font's own design 4,6,4,6,6,4; 0.7.6 had 6,6,7,6,9,4), "Melee" 3,3,4,3 (design 3,4,4,2). Text is a little narrower than before; every measured box still fits. Code: `tools/vwf_build.py` (`adv_code`, `emit_code`, `frac_patches`), details in `docs/vwf.md`.
- Includes the 0.7.6 clear-rate panel fix.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.7).iso`, built with `python tools/build_iso.py 0.7.7 --work work/output/build_0.7.7 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.7.log`).
- Checked in PPSSPP 1.20.4 with the reported save: "Ranged Def." on the Player and Partner unit stats, "END" in the save-select stat headers.
- Spacing checked in PPSSPP at 4x: Partner unit stats ("VF-0D", "HP" now in the English font), help lines, mission list and info panel, Record screens ("Item Completion Rate").
- The first 0.7.7 rebuild stopped at the last step (the ISO was open in PPSSPP); `iso_patch.py` was rerun alone.

## [0.7.6] - 2026-10-21 (test build, not released)

### Fixed
- **Record screen, clear-rate panel** (`menu/gallery/gal_r_com_clear_rate_base.gim`):
  - Four labels sat next to the wrong values. The English lines run row by row (Campaign | S Rank, Extra Enemy | Ultimate, Chronicle | EX), but the layout placed them column by column, so "S Rank Rate", "Extra Enemy Clear Rate", "Ultimate Clear Rate" and "Chronicle Completion" were each beside another rate's percentage. The items now follow the original positions.
  - The labels were slanted, grey and of mixed sizes; the Japanese is upright, bold white and uniform. Now upright white, weight 800, all 9 px ("Extra Enemy Clear Rate" squeezed to 80% instead of shortened).
  - The green arrows before each value box were erased; the erase boxes now stop before them.
  - All in `work/ui/redraw_layout.json`; the translation is unchanged.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.6).iso`, built with `python tools/build_iso.py 0.7.6 --work work/output/build_0.7.6 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.6.log`).
- Checked in PPSSPP 1.20.4 with the reported save: Record > Campaign Record shows the labels upright, in the Japanese order, each beside its own value, with the arrows.
- Added `docs/mission_titles.md`: all 247 mission records in the EBOOT mission table (id, title, objective), grouped by id prefix.

## [0.7.5] - 2026-10-18 (public release)

### Fixed
- **Game hangs when a save is loaded (or a mode is unlocked).** Reported by a player whose save would not open; their save is in `incoming/NPJH50050000` (local). The original Japanese game loads it and then shows the prize notice "Chronicle Mode has been unlocked"; 0.7.3 (the public release) hung at that point, writing past the end of memory (PPSSPP log: "Bad memory access ... 0ad40000" onward).
  - Cause: four prize notices are copied with an inlined fixed-length copy whose end address is a separate constant (start + 32 or start + 96, from a code pair or the constant pool at 0x37FA78): "Chronicle Mode / Enemy Mode / Extra Mode has been unlocked." and the Hangar era-faction tip. `eboot_insert.py` moved the English to new addresses and repointed the start but not the end, so the copy loop never reached its end. `dump_eboot.py` had read the end constants as merged "tails" of the strings.
  - `tools/dump_eboot.py`: a string with any reference into its middle is now `inline_copy` with its original length as the limit, so `eboot_insert.py` writes it in place (or stops the build if the English is too long). Only these four strings are affected. The same cause applies to every earlier build that translated these strings, including the public 0.7.1.
  - u3005 (Hangar tip) shortened to fit 97 bytes: "In the Hangar, push the analog stick left/right / to switch era factions for units and characters." The three mode notices already fit.
- Includes the 0.7.4 unit-name fix (VAJRA etc.).

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.5).iso`, built with `python tools/build_iso.py 0.7.5 --work work/output/build_0.7.5 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.5.log`).
- Release image `work/output/Macross Ultimate Frontier (EN v0.7.5 release).iso` (`tools/relayout_iso.py`, all 102 files match the build): 1,238,269,952 bytes, SHA-256 `e10fc6a208312c46178a7c17e1a4488e6197482966c2c719d78a6d7f8ca8cbb4`. The reported save loads on it to the mission list.
- Release assets: full patch (4,509,112 bytes) and upgrades from the published 0.7.3 (30,042 bytes) and 0.7.1 (46,726 bytes); metadata in `docs/releases/0.7.5/`.
- Checked in PPSSPP 1.20.4 with the reported save: 0.7.3 hangs after "Load the data?" (99 bad memory accesses logged); 0.7.5 shows "Chronicle Mode has been unlocked.", two "New mission added" notices and reaches the mission list, with no bad accesses. The Japanese game behaves the same as 0.7.5 (`work/ui/screens_save/`, local).

## [0.7.4] - 2026-10-18 (test build, not released)

### Fixed
- **Vajra spelled "VAJURA" on lock-on labels and unit lists.** These names are not Japanese text: the original EBOOT already carries English unit labels with the game's own romanization, referenced from the unit records, so the translation had never touched them. 33 labels that clash with the glossary are now rewritten in place: VAJURA / BAJURA -> VAJRA (ship, carrier, cocoon, larva, queen, small and large drones), VAJURA SEMI-QUEEN -> VAJRA SUB-QUEEN, GEPPERNITI -> GEPELNITCHI, OCTOSS -> OCTOS, BARAUTA -> VARAUTA (ships and carriers). CALL_VAJURA is an internal identifier and stays.
  - `work/translation/en/eboot_ascii.en.json`: the rows (file offset, old, new, glossary note).
  - `tools/eboot_ascii_fix.py`: checks the old bytes and that the new name fits its slot (GEPELNITCHI fills its 12 bytes exactly), NUL-fills the rest. No game data file contains these names, and each is referenced only by its unit record, so nothing matches on them. `tools/build_iso.py` runs it after `eboot_insert.py`.
  - Other names in the table were left as the game has them where the glossary has no entry (for example GOLG GANTS CHARTS, QUEL QUALLIE, QDL-RAU).

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.4).iso`, built with `python tools/build_iso.py 0.7.4 --work work/output/build_0.7.4 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.4.log`).
- Checked in PPSSPP 1.20.4 at 4x: new campaign, Frontier era, "Close Encounter" (MF_310): the lock-on labels read VAJRA(S). Radio subtitles show for Ozma and the operator.

## [0.7.3] - 2026-10-17 (public release)

### Added
- **Title screen shows the build version and the group name** in the bottom-right corner, as in the other retro-trans releases: "v0.7.3" over "github.com / retro-trans", white with a dark outline, drawn into `data/menu/title/title.gim` next to the English copyright lines.
  - `work/ui/redraw_layout.json`: two items on `title.gim` with their own `text`, right-aligned in boxes (356, 246, 120×11) and (316, 258, 160×11), erase mode `keep`.
  - `tools/redraw_images.py`: an item's `text` may contain `{version}`, filled from the new `--version` option (default `dev`); `tools/build_iso.py` passes its build version.
- Includes the 0.7.2 fix (friendly units shown as enemies).

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.3).iso`, built with `python tools/build_iso.py 0.7.3 --work work/output/build_0.7.3 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.3.log`).
- Release image `work/output/Macross Ultimate Frontier (EN v0.7.3 release).iso`: `python tools/relayout_iso.py "Macross Ultimate Frontier (Japan).iso" "work/output/Macross Ultimate Frontier (EN v0.7.3).iso" "work/output/Macross Ultimate Frontier (EN v0.7.3 release).iso" --write`. 1,238,269,952 bytes, SHA-256 `c8d64a7e8d006e88e4532e81d538f7211eafa808de6911c9c0bc746f58dd6a4f`; all 102 files match the build. The appended-layout test ISO is not a release source.
- Release assets (Retro Trans Tools): full patch from the original disc (4,510,329 bytes) and an upgrade from the published 0.7.1 image (30,783 bytes); metadata in `docs/releases/0.7.3/`.
- Checked in PPSSPP 1.20.4 at 4x: the title screen shows "v0.7.3" and "github.com / retro-trans" (test build and release image); the release image runs from a new campaign into the first Zero mission (mission list, radio subtitle under the cut-in, flight HUD). The 0.7.2 fix was checked in "Close Encounter" on 0.7.2.

## [0.7.2] - 2026-10-17 (test build, not released)

### Fixed
- **Friendly units shown as enemies in some missions** (every build with the EBOOT text, 0.5.0-0.7.1): in missions whose unit placement file has the extra column (89 of the 246 files), wingmen and allies had red "EN" tags in the unit list and red marks on the radar; for example Ozma Lee in the first Frontier mission, "Close Encounter" (MF_310). Cause: the EBOOT string 追加装備 ("Add-on Equipment", eboot:3B2978, row u2297) is not only a label but a column name of the unit placement files `data/locate/*.csv`. The game compares header cell 4 with it (code at 0x1C1B20 and 0x1C3564) to tell the files with that extra column from the others; translated, those files were read with the wrong layout, so every later column (side, team, AI...) was off by one. The string now stays Japanese; it is never shown in game. Same bug as in the Macross Triangle Frontier translation (its 0.1.19).
  - `tools/dump_eboot.py`: `NOT_TEXT` entry for vaddr 0x3B28D8; NOT_TEXT strings now carry `not_text`.
  - `tools/build_ui.py`: such strings stay as a row with status `not_text` (row ids do not shift) and no English; `tools/ui_slice.py` skips them in `check`, `merge` and `export`, so `ui_insert.json` no longer writes it.
  - Checked: no other translated EBOOT string is a CSV header in the game data; the only whole-cell matches are unit display names in `locate/*.csv` (translated there too) and the `COMMENT` column of `path/*.csv`.
  - Missed by the 0.7.1 playtest because the first Zero mission (MZ_310) uses a file without the extra column.

### Build
- `work/output/Macross Ultimate Frontier (EN v0.7.2).iso`, built with `python tools/build_iso.py 0.7.2 --work work/output/build_0.7.2 --voice-subs work/translation/en/voice/voice_subs.en.json --tr work/translation/en/dialogue.json --tr work/translation/en/ui_insert.json --tr work/translation/en/internal_labels.json` (log `work/output/build_0.7.2.log`). EBOOT: 3,508 of 3,575 strings, loader check ok. 2,216,732,672 bytes (appended layout, not yet re-laid out with `tools/relayout_iso.py`), SHA-256 `123677EA69379F87C0D1A7841FD62BF21197FD48A308683C88FD7613A73BDB18`.
- Checked in PPSSPP 1.20.4 in "Close Encounter" (MF_310) against the Japanese game and 0.7.1: Ozma Lee now has the green "FR" tag and allies are green on the radar, as in the original; 0.7.1 showed a red "EN" tag (`work/ui/screens_0.7.2/`, local). Only that mission was played.

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
