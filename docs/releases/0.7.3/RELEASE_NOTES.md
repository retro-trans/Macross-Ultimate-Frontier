English fan translation of **Macross Ultimate Frontier** for PSP (**NPJH-50050**, v1.02), including English subtitles for the in-mission radio voice.

### Apply

**Recommended:** Use the latest [Retro Trans](https://github.com/retro-trans/retro-trans-tools) app. Click **Refresh catalog**, open **Automatic**, select your original Japanese ISO or the published English v0.7.1 ISO, choose **0.7.3** (or **Latest**), and select a new output filename. The app downloads the matching patch and verifies the result.

**Manual patching:** [DeltaPatcher](https://github.com/marco-calautti/DeltaPatcher) and [xdelta3](https://github.com/jmacd/xdelta) accept the same assets:

| Your source image | Patch |
| --- | --- |
| Original Japanese ISO | `MacrossUltimateFrontier-English-0.7.3.xdelta` |
| Published English v0.7.1 ISO | `MacrossUltimateFrontier-English-0.7.1-to-0.7.3.xdelta` |

```text
xdelta3 -d -s "Macross Ultimate Frontier (Japan).iso" MacrossUltimateFrontier-English-0.7.3.xdelta "Macross Ultimate Frontier English 0.7.3.iso"
```

To upgrade from the published v0.7.1 image:

```text
xdelta3 -d -s "Macross Ultimate Frontier English 0.7.1.iso" MacrossUltimateFrontier-English-0.7.1-to-0.7.3.xdelta "Macross Ultimate Frontier English 0.7.3.iso"
```

Both patches produce the same release image. The upgrade patch requires the exact published v0.7.1 image (SHA-256 `01fdc0b61ea21578593d2fb7c1450c768372bbd02e691aa55ef18554d4e344bc`); use the original disc if yours does not match.

Original Japanese ISO: 1,237,843,968 bytes; SHA-256 `86e942c37f8edaaf9ed1ac4e9292bbcacbef331b7aee6027fb896e015751b205`.

Release output: 1,238,269,952 bytes; SHA-256 `c8d64a7e8d006e88e4532e81d538f7211eafa808de6911c9c0bc746f58dd6a4f`.

The exact source, output and patch hashes are in `BUILD-MANIFEST.json`. `VALIDATION.json` records the patch round trips, and `SHA256SUMS.txt` covers the downloads. Manual patchers require the unpacked ISO.

### What changed since v0.7.1

* **Friendly units shown as enemies:** in missions whose unit placement file has an extra column (89 of 246 files), wingmen and allies had red "EN" tags in the unit list and red marks on the radar, for example Ozma Lee in the first Frontier mission, "Close Encounter". The game uses one translated label as a column name in its unit placement files; it is now left as the game expects, and allies are green again.
* **Title screen:** shows the build version and `github.com / retro-trans` in the bottom right.

Retains all v0.7.1 content: menus and help, narration, briefings and objectives, redrawn textures, radio voice subtitles, and the proportional English font with its 4x glyph page. See the [changelog](https://github.com/retro-trans/Macross-Ultimate-Frontier/blob/main/CHANGELOG.md).

### Release status

**This is an early build. Further proofreading and full in-game playtesting are needed.** File and patch verification shows that the intended data is included and that the patches reproduce the release image. It does not certify emulator or console behavior. In PPSSPP 1.20.4, the title screen and a new campaign into the first Zero mission (radio subtitles, flight HUD) were checked on this image; the ally fix was confirmed in "Close Encounter" on the test build. Most missions have not been played.

Known limitations:

* Only voice clips that the mission script plays are subtitled. Voices played elsewhere (menus, character select samples) are not. The parts of a long subtitle advance at even steps through the clip, not with the phrasing.
* The pilot name in the top-left of the flight HUD is drawn through an offscreen buffer, so it stays 1x at higher render resolutions.
* The 4x font is designed for emulators at 2x resolution or higher. At native 1x resolution the same glyphs are scaled down.
* The image carries a decrypted EBOOT. PPSSPP and custom firmware ISO drivers load it; official firmware without custom firmware does not. Real hardware has not been tried.

**Boot the patched ISO fresh and load a normal save.** Save states keep the old text, fonts and textures in memory.

### How it was translated

This is a **machine translation**, produced with large language models and then reviewed and edited using scene context and a researched glossary. Names and terms follow the [Macross Wiki](https://macross.fandom.com) and avoid Robotech names. The radio voice was transcribed locally with Whisper large-v3 (faster-whisper); uncertain transcripts are marked in the sources. Human proofreading and playtesting are welcome.

### Acknowledgements

* **Project Lead:** pow
* **GenEi LateGo** © okoneya.jp, used for the English glyphs (SIL Open Font License 1.1; the licence is in the repository).
* **PPSSPP**, whose PRX decryption and debugger were used for the EBOOT tools and testing.
* **Whisper** (OpenAI) and **faster-whisper**, used to transcribe the radio voice.

### Source code

Translation text, glossaries and tools are available in the [project repository](https://github.com/retro-trans/Macross-Ultimate-Frontier). GitHub's source archives contain the repository snapshot at the release tag. Use the `.xdelta` assets to patch the game.

### Contribute

Bug reports, proofreading and playtesting are welcome at **[discord.gg/MssepShjmB](https://discord.gg/MssepShjmB)**.

No complete game images are included. Apply the patches to your own disc image.
