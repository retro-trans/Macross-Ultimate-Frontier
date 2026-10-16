English fan translation of **Macross Ultimate Frontier** for PSP (**NPJH-50050**, v1.02), including English subtitles for the in-mission radio voice.

### Apply

**Recommended:** Use the latest [Retro Trans](https://github.com/retro-trans/retro-trans-tools) app. Click **Refresh catalog**, open **Automatic**, select your original Japanese ISO, choose **0.7.1** (or **Latest**), and select a new output filename. The app downloads the matching patch and verifies the result.

**Manual patching:** [DeltaPatcher](https://github.com/marco-calautti/DeltaPatcher) and [xdelta3](https://github.com/jmacd/xdelta) accept the same asset:

| Your source image | Patch |
| --- | --- |
| Original Japanese ISO | `MacrossUltimateFrontier-English-0.7.1.xdelta` |

```text
xdelta3 -d -s "Macross Ultimate Frontier (Japan).iso" MacrossUltimateFrontier-English-0.7.1.xdelta "Macross Ultimate Frontier English 0.7.1.iso"
```

Original Japanese ISO: 1,237,843,968 bytes; SHA-256 `86e942c37f8edaaf9ed1ac4e9292bbcacbef331b7aee6027fb896e015751b205`.

Release output: 1,238,269,952 bytes; SHA-256 `01fdc0b61ea21578593d2fb7c1450c768372bbd02e691aa55ef18554d4e344bc`.

The exact source, output and patch hashes are in `BUILD-MANIFEST.json`. `VALIDATION.json` records the patch round trip, and `SHA256SUMS.txt` covers the downloads. Manual patchers require the unpacked ISO.

### What's included

This is the first public release.

* **Menus and help:** the main, single-player, network and option menus, help bars, unit, pilot and pack descriptions, the Nyan-Nyan shop with its player titles, and the records screens. 3,525 UI strings.
* **Story text:** prologue and epilogue narration for every era (SDF, DYRL, Zero, Plus, 7, Dynamite 7, Frontier), mission objectives and briefings for 216 missions, and in-mission objectives and tutorial lines.
* **Radio voice subtitles:** the in-mission radio cut-ins have no text in the original game. Each clip was transcribed and translated, and the patched game shows the English line under the cut-in while it plays: in the intro camera, during the "enemy appeared" / "allies sighted" banners and in flight. 12,489 of the 14,215 clips have a subtitle; the rest are silent placeholders, drums or screams without words, or narration already shown as text.
* **Textures:** plain text drawn into images is redrawn in English. The official series logos keep their original Japanese-script designs.
* **Font:** a proportional English font (GenEi LateGo) with its own 4x glyph page. In PPSSPP at 2x–4x rendering, game text is drawn sharp without a texture pack.

See the [changelog](https://github.com/retro-trans/Macross-Ultimate-Frontier/blob/main/CHANGELOG.md).

### Release status

**This is an early build. Further proofreading and full in-game playtesting are needed.** File and patch verification shows that the intended data is included and that the patch reproduces the release image. It does not certify emulator or console behavior. In PPSSPP 1.20.4, the menus, a new campaign through its narration, mission list and briefing, and the first Zero mission (intro, radio subtitles, flight HUD, pause menu) were checked. Most missions have not been played with this build.

Known limitations:

* Only voice clips that the mission script plays are subtitled. Voices played elsewhere (menus, character select samples) are not. The parts of a long subtitle advance at even steps through the clip, not with the phrasing.
* The pilot name in the top-left of the flight HUD is drawn through an offscreen buffer, so it stays 1x at higher render resolutions.
* The 4x font is designed for emulators at 2x resolution or higher. At native 1x resolution the same glyphs are scaled down.
* The image carries a decrypted EBOOT. PPSSPP and custom firmware ISO drivers load it; official firmware without custom firmware does not. Real hardware has not been tried.
* Whether subtitles show with the "2D Display" option off has not been checked.

**Boot the patched ISO fresh and load a normal save.** Save states keep the old text, fonts and textures in memory.

### How it was translated

This is a **machine translation**, produced with large language models and then reviewed and edited using scene context and a researched glossary. Names and terms follow the [Macross Wiki](https://macross.fandom.com) and avoid Robotech names. The radio voice was transcribed locally with Whisper large-v3 (faster-whisper); 1,224 transcripts were corrected from context and 439 lines remain marked uncertain in the sources. Human proofreading and playtesting are welcome.

### Acknowledgements

* **GenEi LateGo** © okoneya.jp, used for the English glyphs (SIL Open Font License 1.1; the licence is in the repository).
* **PPSSPP**, whose PRX decryption and debugger were used for the EBOOT tools and testing.
* **Whisper** (OpenAI) and **faster-whisper**, used to transcribe the radio voice.

### Source code

Translation text, glossaries and tools are available in the [project repository](https://github.com/retro-trans/Macross-Ultimate-Frontier). GitHub's source archives contain the repository snapshot at the release tag. Use the `.xdelta` asset to patch the game.

### Contribute

Bug reports, proofreading and playtesting are welcome at **[discord.gg/MssepShjmB](https://discord.gg/MssepShjmB)**.

No complete game images are included. Apply the patch to your own disc image.
