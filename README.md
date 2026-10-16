# Macross Ultimate Frontier — English patch

Fan translation of the PSP game *Macross Ultimate Frontier* (NPJH-50050, v1.02) into English. The patch is
distributed as an xdelta file that you apply to your own disc image. This repository contains translation text,
glossaries, layout metadata and tools; disc images, extracted game data and Japanese working files are excluded.

## Applying the patch

Use [Retro Trans](https://github.com/retro-trans/retro-trans-tools/releases/latest) for automatic patching:

1. Open **Automatic**, click **Refresh catalog**, and browse to your original Japanese ISO.
2. Select the **Macross Ultimate Frontier** English patch.
3. Leave **Target** on **Latest**, choose a new output filename, and apply the patch. Retro Trans downloads the
   matching patch and verifies the resulting image.

See the [release notes](https://github.com/retro-trans/Macross-Ultimate-Frontier/releases) for changes, known
limitations and supported upgrade paths.

For manual patching:

1. Dump your own Japanese UMD to an ISO. Full patches apply to the original image:
   - `Macross Ultimate Frontier (Japan).iso`, 1,237,843,968 bytes
   - SHA-256 `86e942c37f8edaaf9ed1ac4e9292bbcacbef331b7aee6027fb896e015751b205`
2. Download `MacrossUltimateFrontier-English-<version>.xdelta` from
   [Releases](https://github.com/retro-trans/Macross-Ultimate-Frontier/releases/latest).
3. Apply it with xdelta3 (or any VCDIFF tool such as Delta Patcher):

   ```bash
   xdelta3 -d -s "Macross Ultimate Frontier (Japan).iso" MacrossUltimateFrontier-English-<version>.xdelta "Macross Ultimate Frontier English <version>.iso"
   ```

4. Compare the output SHA-256 with the release notes or `BUILD-MANIFEST.json`, then play it in PPSSPP. Boot it
   fresh and load a normal save: save states made with the Japanese image or an older patch keep the old text in
   memory.

The patched image carries a decrypted EBOOT. PPSSPP and custom firmware ISO drivers load it; official firmware
without custom firmware does not.

## What is translated

- Menus, help text, unit, pilot and pack descriptions, the shop and records screens
- Era prologue and epilogue narration, mission briefings and in-mission objectives
- Text drawn into textures (the official series logos are kept)
- **English subtitles for the in-mission radio voice**, which has no text in the original game
- A proportional English font (GenEi LateGo) with a built-in 4x glyph page, so text stays sharp when PPSSPP
  renders at 2x–4x without a texture pack

## Repository layout

- `docs/` — format notes, build guide, translation briefs and the release guide
- `tools/` — dump, insert, font, subtitle, build and check tools
- `work/glossary/` — researched names and terms every translation must follow
- `work/translation/en/` — the English text (`*.en.json`): dialogue, UI, images, internal labels, voice subtitles,
  with their 80-row slices and reviews
- `work/ui/` — text box limits and width reports; screenshots stay local
- `work/fonts/` — the GenEi LateGo font and its licence

## Build it

Put your original ISO in the project root as `Macross Ultimate Frontier (Japan).iso` and extract its data as
described in [the format notes](docs/formats.md). Then:

```text
python tools/build_iso.py <version> --voice-subs work/translation/en/voice/voice_subs.en.json --tr ...
python tools/relayout_iso.py "Macross Ultimate Frontier (Japan).iso" "work/output/Macross Ultimate Frontier (EN <built>).iso" "work/output/Macross Ultimate Frontier (EN <version>).iso" --write
```

The full command lines for each version are in the [changelog](CHANGELOG.md). [The build guide](docs/build.md)
explains each step, and [the release guide](docs/RETRO_TRANS_RELEASES.md) covers packaging. The Japanese working
files (`work/translation/**/*.json` without `.en`) are generated locally from your own disc and are never
committed; `tools/strip_jp.py` writes the English-only copies.

## Credits

| Role | Contributors |
| --- | --- |
| Project Lead | binhlt0402 |

GenEi LateGo © okoneya.jp, SIL Open Font License 1.1 (`work/fonts/GenEiLatin_LICENSE.txt`).

## License

Translation text and tools: [MIT](LICENSE). The font keeps its own licence (SIL OFL 1.1). The game and its assets
belong to Namco Bandai Games / Artdink and the respective Macross rights holders. Bring your own disc image; this
license does not cover the game or its assets.
