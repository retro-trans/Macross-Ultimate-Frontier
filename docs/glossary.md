# Glossary

Files live in `work/glossary/`:

| File | Contents |
|---|---|
| `characters.json` | 100 characters: playable roster, MUF original characters, supporting cast likely to appear in dialogue |
| `organizations.json` | Militaries, factions, squadrons, bands, fleets |
| `locations.json` | Planets, islands, cities, ships-as-places |
| `mecha.json` | All 100+ units from the game's roster, pack/equipment names, naming conventions |
| `terms.json` | Lore terms, game-system terms, skills, song titles, series titles |

## Spelling policy

1. **Macross Wiki (macross.fandom.com) wins.** We use the article title. Where the wiki contradicts itself (title vs. body vs. infobox `english` field), the entry is marked `needs_check` and `notes` explains the choice.
2. **No Robotech names.** Names such as Rick Hunter, Lisa Hayes, Breetai, Khyron, Zentraedi and Roy Fokker are in `avoid` lists.
3. **Given name first** for Japanese names in English (Alto Saotome, Hikaru Ichijyo). Chinese-order names keep the surname first (Lynn Minmay: "Lynn" is the surname).
4. **Fonts:** macrons and umlauts (Kudō, König) are dropped if the game font can't render them. This gets decided once the font is extracted.

## Fields used by tools

- `en`: the canonical spelling.
- `avoid`: spellings the proofreading script must replace with `en`. Matching is **case-sensitive**: "Edgar Lasalle" is in `avoid`, while "Edgar LaSalle" is the canonical form.
- `gender`: taken from the wiki. `unknown` means use "it" or a neutral construction. Never infer gender from a name.
- `status`: `verified` / `decided` (user confirmed) / `needs_check` / `provisional` / `needs_research`.

## Sources

- Game roster: https://ja.wikipedia.org/wiki/マクロスアルティメットフロンティア (units, cast, original characters, songs)
- Predecessor (original character backgrounds): https://ja.wikipedia.org/wiki/マクロスエースフロンティア
- English names and character facts: https://macross.fandom.com/wiki/Macross_Ultimate_Frontier and the per-character pages linked in each entry

## Decided spellings (confirmed by user, 2026-10-15)

| Item | Spelling | Rejected |
|---|---|---|
| ブリタイ | Vrlitwhai Kridanik | Britai, Breetai |
| カムジン | Quamzin Kravshera | Kamjin, Khyron |
| ミリア | Milia Fallyna Jenius | Milia Farina, Miria |
| ジェフリー | Jeffrey Wilder | Jeffery Wilder |

These entries have `status: "decided"`. Do not reopen them.

## Open decisions (need a human call)

| Item | Wiki says | Common alternative | Current choice |
|---|---|---|---|
| ホイリー | Hoilie / Hollie both used | Hoyly | Hoilie |
| ボドルザー | title "Golg", intro "Gol" | Bodolza | Golg Boddole Zer |
| ビルラー | title "Birler", text "Bilrer" | — | Bilrer |
| 工藤シン | Shin Kudō | Shin Kudo | Shin Kudo (font) |
| ゴルグ・ガンツ・チャーツ | not found | — | needs research |

## Not done yet

- The names are not yet checked against the actual game text. The game data is packed in `PSP_GAME/USRDIR/macross.dat` + `macross.idx` (a `PIDX` archive with hashed names), and `BOOT.BIN` is blank (the EBOOT is encrypted). Extracting the script is the next step. After that, add any names the game uses that are missing here.
- Max text widths per text type have not been measured yet.
