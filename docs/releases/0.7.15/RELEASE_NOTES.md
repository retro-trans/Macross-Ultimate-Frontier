English fan translation of **Macross Ultimate Frontier** for PSP (**NPJH-50050**, v1.02), including radio voice subtitles and draft English song lyrics with romaji.

### Apply

**Recommended:** Use [Retro Trans](https://github.com/retro-trans/retro-trans-tools). Refresh the catalog, open **Automatic**, select your original Japanese ISO or a published English v0.7.1, v0.7.3, v0.7.5, v0.7.8 or v0.7.9 ISO, choose **0.7.15** or **Latest**, and select a new output filename. The app downloads the matching patch and verifies the result.

**Manual patching:** [DeltaPatcher](https://github.com/marco-calautti/DeltaPatcher) and [xdelta3](https://github.com/jmacd/xdelta) accept the same assets:

| Your source image | Patch |
| --- | --- |
| Original Japanese ISO | `MacrossUltimateFrontier-English-0.7.15.xdelta` |
| Published English v0.7.9 ISO | `MacrossUltimateFrontier-English-0.7.9-to-0.7.15.xdelta` |
| Published English v0.7.8 ISO | `MacrossUltimateFrontier-English-0.7.8-to-0.7.15.xdelta` |
| Published English v0.7.5 ISO | `MacrossUltimateFrontier-English-0.7.5-to-0.7.15.xdelta` |
| Published English v0.7.3 ISO | `MacrossUltimateFrontier-English-0.7.3-to-0.7.15.xdelta` |
| Published English v0.7.1 ISO | `MacrossUltimateFrontier-English-0.7.1-to-0.7.15.xdelta` |

```text
xdelta3 -d -s "Macross Ultimate Frontier (Japan).iso" MacrossUltimateFrontier-English-0.7.15.xdelta "Macross Ultimate Frontier English 0.7.15.iso"
```

Upgrade patches require the exact published source ISO. Local test images need the full patch applied to the original disc. All six patches produce the same compact release image; exact source hashes are recorded in `BUILD-MANIFEST.json`.

Original Japanese ISO: 1,237,843,968 bytes; SHA-256 `86e942c37f8edaaf9ed1ac4e9292bbcacbef331b7aee6027fb896e015751b205`.

Release output: 1,238,335,488 bytes; SHA-256 `ad326ede78bf0e2a94dd88a4c3fc41325892134c666bb152cbb163fe0c4cffdf`.

`VALIDATION.json` records complete patch decode/hash round trips. `SHA256SUMS.txt` covers every patch and both metadata files. Manual patchers require an unpacked ISO.

### What changed since v0.7.9

* **Song captions during missions:** draft English lyrics appear at the top of the screen, with **romaji above English** where a Japanese transcription is available. There are 306 display captions across 29 tracks; 239 captions have romaji across 27 tracks. Long captions fit within three rows. Voice subtitles remain at the bottom.
* **Zentradi voice subtitles:** Boddole Zer and Milia now have subtitles for their Zentradi-language clips, plus a previously missing Quamzin line. Reused clips receive the same text. Voice coverage is now **12,506 of 14,215 clips**. The Zentradi interpretations remain uncertain and were derived from word-list meanings.
* **UI wording:** sentences spell out **Nyan-Nyan Points**, while labels and amounts use **pts**. **Evening** is now **Dusk**, and **Full Spirit** is now **High Spirit**. Several skill descriptions have corrected multiplier wording and line breaks.

Retains the menus, profiles, briefings, objectives, narration, image-text redraws, proportional font and voice subtitles from earlier releases. Details are in the [changelog](https://github.com/retro-trans/Macross-Ultimate-Frontier/blob/main/CHANGELOG.md).

### Release status

**This is an early machine-translated build. The song lyrics, romaji readings and timing are drafts.** Full human proofreading and in-game playtesting are still needed.

All 102 files in the compact image match the test build. All 306 caption records match their intended text and timing data, and every original song audio prefix is unchanged. Each of the six patches was decoded and checked against the complete release image. These checks verify the files and patch application; they do not certify gameplay behavior.

The release image was freshly launched in an isolated PPSSPP 1.20.4 setup and recognized as NPJH50050 v1.02. **This release's lyric display has not been visually playtested, and its timing has not been checked by ear.** The caption mechanism was tested with placeholder text in an earlier build. Real hardware has not been tested.

Known limitations:

* Whisper can mishear singing or omit passages. Some lyric lines are absent, and romaji inherits transcription and dictionary-reading errors. Timing inside ASR segments is approximate.
* Sara (`bgm79`), Ishtar (`bgm80`) and Myung (`bgm81`) have no lyric captions because no reliable words were recovered. English-only refrains and passages without usable Japanese ASR remain English-only.
* Lyrics appear in missions. Custom memory-stick music has no lyric captions; when supported songs overlap, the most recently started one is selected.
* Radio subtitles cover voice clips played through the mission script. Menu and character-selection samples are outside that hook. Parts of a long radio subtitle advance at even intervals through its clip.
* The pilot name in the top-left flight HUD remains 1x at higher render resolutions. The built-in 4x font is designed for emulator rendering at 2x or higher and is scaled down at native 1x.
* The image carries a decrypted EBOOT. PPSSPP and custom firmware ISO drivers load it; official firmware without custom firmware does not.

**Boot the patched ISO fresh and load a normal save.** Save states retain old text, fonts and textures in memory.

### How it was translated

The translation was produced with large language models, then reviewed and edited using scene context and a researched glossary. Names and terms follow the [Macross Wiki](https://macross.fandom.com) and avoid Robotech names. Radio voice and song audio were transcribed locally with Whisper large-v3 through faster-whisper. English lyric drafts received corrections for obvious recognition errors; romaji uses fugashi, UniDic-lite and pykakasi. Human proofreading and playtesting are welcome.

### Acknowledgements

* **Project Lead:** pow.
* **GenEi LateGo** © okoneya.jp, used for the English glyphs under the SIL Open Font License 1.1; its licence is in the repository.
* **PPSSPP**, whose PRX decryption and debugger were used for the tools and testing.
* **Whisper**, **faster-whisper**, **fugashi**, **UniDic-lite** and **pykakasi**, used for the transcription and reading drafts.

### Source code

Tools, glossaries and English script data are in the [project repository](https://github.com/retro-trans/Macross-Ultimate-Frontier). Source commit: `86e8834e1d4094536a17f20d9aab2aea29f585c2`. GitHub's source archives contain the repository snapshot at the release tag. Lyric working files and Japanese ASR transcripts stay outside git; the released patches include the English lyric and romaji text as explicitly requested by the project lead.

### Contribute

Bug reports, proofreading and playtesting are welcome at **[discord.gg/MssepShjmB](https://discord.gg/MssepShjmB)**.

No complete game images are included. Apply the patches to your own disc image.
