English fan translation of **Macross Ultimate Frontier** for PSP (**NPJH-50050**, v1.02), including English subtitles for the in-mission radio voice.

### Apply

**Recommended:** Use the latest [Retro Trans](https://github.com/retro-trans/retro-trans-tools) app. Click **Refresh catalog**, open **Automatic**, select your original Japanese ISO or a published English v0.7.1, v0.7.3, v0.7.5 or v0.7.8 ISO, choose **0.7.9** (or **Latest**), and select a new output filename. The app downloads the matching patch and verifies the result.

**Manual patching:** [DeltaPatcher](https://github.com/marco-calautti/DeltaPatcher) and [xdelta3](https://github.com/jmacd/xdelta) accept the same assets:

| Your source image | Patch |
| --- | --- |
| Original Japanese ISO | `MacrossUltimateFrontier-English-0.7.9.xdelta` |
| Published English v0.7.8 ISO | `MacrossUltimateFrontier-English-0.7.8-to-0.7.9.xdelta` |
| Published English v0.7.5 ISO | `MacrossUltimateFrontier-English-0.7.5-to-0.7.9.xdelta` |
| Published English v0.7.3 ISO | `MacrossUltimateFrontier-English-0.7.3-to-0.7.9.xdelta` |
| Published English v0.7.1 ISO | `MacrossUltimateFrontier-English-0.7.1-to-0.7.9.xdelta` |

```text
xdelta3 -d -s "Macross Ultimate Frontier (Japan).iso" MacrossUltimateFrontier-English-0.7.9.xdelta "Macross Ultimate Frontier English 0.7.9.iso"
```

To upgrade from a published English image:

```text
xdelta3 -d -s "Macross Ultimate Frontier English 0.7.8.iso" MacrossUltimateFrontier-English-0.7.8-to-0.7.9.xdelta "Macross Ultimate Frontier English 0.7.9.iso"
```

All patches produce the same release image. The upgrade patches require the exact published image (v0.7.8 SHA-256 `fa9614697c3821aa4280a1e3bf6773c9a96717f04174067d68774d2ddc89fbd0`, v0.7.5 SHA-256 `e10fc6a208312c46178a7c17e1a4488e6197482966c2c719d78a6d7f8ca8cbb4`, v0.7.3 SHA-256 `c8d64a7e8d006e88e4532e81d538f7211eafa808de6911c9c0bc746f58dd6a4f`, v0.7.1 SHA-256 `01fdc0b61ea21578593d2fb7c1450c768372bbd02e691aa55ef18554d4e344bc`); use the original disc if yours does not match.

Original Japanese ISO: 1,237,843,968 bytes; SHA-256 `86e942c37f8edaaf9ed1ac4e9292bbcacbef331b7aee6027fb896e015751b205`.

Release output: 1,238,269,952 bytes; SHA-256 `e8620443e6c15db580b13afe31f88459386814129b664da41ee60ca91e7e031e`.

The exact source, output and patch hashes are in `BUILD-MANIFEST.json`. `VALIDATION.json` records the patch round trips, and `SHA256SUMS.txt` covers the downloads. Manual patchers require the unpacked ISO.

### What changed since v0.7.8

* **Skill descriptions rewritten** for nearly every Command and Auto Skill, in one consistent style ("Increase attack power of self and allies by 1.5x and gradually restore HP."), each wrapped to fill its box. Once-only skills end with "※ One use only."
* **Skill names:** "Legendary Elixir" is now **Phantom Elixir**, "Quick Recovery" is now **Rapid Recovery**.
* **Prize Mode list** on the save-select screen no longer runs past its panel; five long names were shortened ("Remove Unit Size Limit", "Remove Fixed-Pilot Limit", "Unlock Shop Line Select", "Unlock EX Challenge", "Free Nyan-Nyan Shop").
* **Nyan-Nyan Shop:** prices read "800 pts" (was "800NPt"). The menu labels are all the same size, keep their size when highlighted, and lose the leftover Japanese bullet dots; "BGM" now uses the English font.
* **Record screens:** "Ulti. Clear Rate" no longer runs into its value, and the Overall Record labels line up with their values as in the Japanese.

Retains all v0.7.8 content. See the [changelog](https://github.com/retro-trans/Macross-Ultimate-Frontier/blob/main/CHANGELOG.md).

### Release status

**This is an early build. Further proofreading and full in-game playtesting are needed.** File and patch verification shows that the intended data is included and that the patches reproduce the release image. It does not certify emulator or console behavior. In PPSSPP 1.20.4, a player's save was loaded on this image to the Nyan-Nyan Shop; the skill screens, Record screens and shop menu were checked on the test build. Most missions have not been played.

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
