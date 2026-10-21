# Width report

Made by `python tools/check_widths.py`. Widths are px at the size the game draws the text type (see `work/ui/text_limits.json`). Inputs: `work/translation/en/camera_tbl.en.json`, `work/translation/en/dialogue.en.json`, `work/translation/en/eboot_ascii.en.json`, `work/translation/en/images.en.json`, `work/translation/en/internal_labels.en.json`, `work/translation/en/ui.en.json`.

## Summary

| Type | Size | Limit px | Max lines | In game | Rows | Lines | Over | Max fill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fes_objective | 10 | 212 | 2 | confirmed | 88 | 91 | 0 | 100% |
| fes_tutorial | 14 | 309 | 3 | confirmed | 144 | 341 | 0 | 100% |
| mission_objective | 10 | 214 | 2 | confirmed | 216 | 389 | 0 | 100% |
| mission_story | 11 | 429 / 415 | 2 | confirmed | 216 | 432 | 0 | 100% |
| narration | 12 | 468 | 1 | confirmed | 223 | 223 | 0 | 100% |
| nn_title | 14 | 252 | 1 | no | 300 | 300 | 0 | 100% |

## Lines over the limit (0)

None.
## Not measured

Ids not found in the source dumps: 3773 (`eboot_ascii:3809DC`, `eboot_ascii:3809F4`, `eboot_ascii:380A10`, `eboot_ascii:380A2C`, `eboot_ascii:380A48`, `eboot_ascii:380A64`, `eboot_ascii:380AA4`, `eboot_ascii:380ABC`, `eboot_ascii:380AD4`, `eboot_ascii:380AEC`, `eboot_ascii:380CC8`, `eboot_ascii:380CDC`, `eboot_ascii:380CF4`, `eboot_ascii:380D0C`, `eboot_ascii:380D24`, `eboot_ascii:380D3C`, `eboot_ascii:380D54`, `eboot_ascii:380D84`, `eboot_ascii:380D9C`, `eboot_ascii:380DB8`).

