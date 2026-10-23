# Retro Trans release packaging

Macross Ultimate Frontier follows the
[Retro Trans release standard](https://github.com/retro-trans/retro-trans-tools/blob/main/docs/RELEASE_STANDARD.md).
Stable identity: game ID `macross-ultimate-frontier`, platform `PSP`, edition `NPJH50050`, language `en`.
Never reuse a version for different bytes; a corrected image is a new `0.x.y`.

For v0.7.15 the user explicitly authorized publishing a patch containing the
draft English lyrics and romaji. This overrides the earlier local-only lyric
rule for that release. The lyric working files and Japanese ASR transcripts
remain gitignored; upload only the patches and standard release metadata.

## Release image

`tools/build_iso.py` appends every file that outgrew its sectors at the end of the image. For `macross.dat` and
`fileset.dat` that leaves a dead 970 MB copy behind (a 2.2 GB test ISO), and the new data sits too far from
the original bytes for xdelta to match. Release images are re-laid out first:

```text
python tools/relayout_iso.py "Macross Ultimate Frontier (Japan).iso" "work/output/Macross Ultimate Frontier (EN <built>).iso" "work/output/Macross Ultimate Frontier (EN <version>).iso"
python tools/relayout_iso.py ... --write
```

The tool keeps the original file order, shifts later files by whole 32 KB blocks where a file grew, rewrites the
directory records and volume size, and verifies every file against the built ISO. The game opens files by path,
so the moved files load as before. Boot the re-laid-out image in PPSSPP before packaging.

## Build and validate

Use Python 3.12+ (the release builder needs it) with Retro Trans Tools checked out under ignored `work/local/`.
Write the private builder configuration under `work/local/` (it holds local paths):

```json
{
  "game_id": "macross-ultimate-frontier",
  "game_name": "Macross Ultimate Frontier",
  "platform": "PSP",
  "version": "<version>",
  "source_commit": "<full commit of this repository at the release tag>",
  "patches": [
    {
      "patch": "MacrossUltimateFrontier-English-<version>.xdelta",
      "edition": "NPJH50050",
      "language": "en",
      "source_version": "original",
      "source_format": "iso",
      "target_format": "iso",
      "source": "<original ISO>",
      "target": "<release ISO>"
    }
  ]
}
```

Add an upgrade row (`source_version` = the previous published version, source = that exact published image)
for every later release. Then build and validate:

```text
python -m retro_trans.release build work/local/release-<version>.json --out work/release/<version>
python -m retro_trans.release validate work/release/<version>
```

The builder encodes each patch, decodes it again and compares the complete target. Only the patches,
`BUILD-MANIFEST.json`, `VALIDATION.json` and `SHA256SUMS.txt` are release assets. Never upload an ISO, extracted
game data or the private configuration. Copy the three metadata files to `docs/releases/<version>/`.

## Publish and confirm discovery

Tag the release commit `v<version>`. Stage a draft release, upload the patches, `VALIDATION.json` and
`SHA256SUMS.txt`, upload `BUILD-MANIFEST.json` last, check the uploaded sizes and hashes, then publish. Notes
follow the sibling releases: Apply, changes, release status, included content, how it was translated,
acknowledgements (GenEi LateGo, SIL OFL 1.1), Source code and Contribute.

After publishing, run **Refresh patch catalog** in Retro Trans Tools Actions with
`repository=retro-trans/Macross-Ultimate-Frontier` (or wait for the hourly run) and confirm the release appears
in the public catalog.

Packaging and catalog checks verify patch application, not in-game behaviour. Keep runtime limitations explicit
in the notes.
