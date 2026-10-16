# Width report

Made by `python tools/check_widths.py`. Widths are px at the size the game draws the text type (see `work/ui/text_limits.json`). Inputs: `work/translation/en/dialogue.en.json`, `work/translation/en/ui_insert.json`, `work/translation/en/internal_labels.en.json`.

## Summary

| Type | Size | Limit px | Max lines | In game | Rows | Lines | Over | Max fill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eboot_bonus | 14 | 140 | 1 | no | 47 | 47 | 1 | 103% |
| eboot_help | 12 | 312 | 1 | confirmed | 137 | 137 | 0 | 87% |
| eboot_list:30BBD8 | 14 | 350 | 3 | no | 4 | 11 | 0 | 83% |
| eboot_list:31B74C | 14 | 364 | 1 | no | 17 | 17 | 0 | 88% |
| eboot_list:34F250 | 14 | 70 | 1 | no | 3 | 3 | 0 | 94% |
| eboot_list:34F2EC | 14 | 42 | 1 | no | 8 | 8 | 0 | 93% |
| eboot_list:34F320 | 14 | 84 | 1 | no | 10 | 10 | 0 | 87% |
| eboot_list:34F354 | 14 | 112 | 1 | no | 12 | 12 | 0 | 62% |
| eboot_list:35D624 | 14 | 42 | 1 | no | 18 | 18 | 6 | 181% |
| eboot_list:366F50 | 14 | 112 | 2 | no | 2 | 3 | 0 | 86% |
| eboot_list:36707C | 14 | 385 | 3 | no | 12 | 26 | 0 | 83% |
| eboot_list:378010 | 14 | 224 | 1 | no | 3 | 3 | 0 | 69% |
| eboot_list:378060 | 14 | 224 | 1 | no | 3 | 3 | 0 | 84% |
| eboot_list:3ED08C | 14 | 112 | 1 | no | 11 | 11 | 0 | 93% |
| eboot_list:3ED12C | 14 | 210 | 2 | no | 1 | 2 | 0 | 69% |
| eboot_list:3ED720 | 14 | 154 | 1 | no | 5 | 5 | 0 | 68% |
| eboot_list:3ED748 | 14 | 112 | 1 | no | 4 | 4 | 0 | 89% |
| eboot_list:3ED96C | 14 | 182 | 2 | no | 6 | 11 | 0 | 91% |
| eboot_list:3ED9B8 | 14 | 434 | 3 | no | 5 | 15 | 0 | 91% |
| eboot_list:3ED9F8 | 14 | 14 | 1 | no | 5 | 5 | 5 | 329% |
| eboot_list:3F6BAC | 14 | 42 | 1 | no | 3 | 3 | 0 | 95% |
| eboot_list:3FB6D8 | 14 | 168 | 1 | no | 1024 | 1024 | 0 | 89% |
| eboot_list:3FEF20 | 14 | 266 | 2 | no | 5 | 6 | 0 | 80% |
| eboot_list:3FF300 | 14 | 252 | 1 | no | 31 | 31 | 0 | 88% |
| eboot_list:3FF3B0 | 14 | 420 | 2 | no | 22 | 29 | 0 | 81% |
| eboot_list:3FF4C4 | 14 | 196 | 2 | no | 5 | 7 | 0 | 77% |
| eboot_list:3FF5D8 | 14 | 364 | 2 | no | 2 | 4 | 0 | 87% |
| eboot_mission_name | 14 | 266 | 1 | no | 200 | 200 | 0 | 91% |
| eboot_objective | 10 | 212 | 1 | confirmed | 65 | 65 | 0 | 96% |
| eboot_self | 14 | own JP line | - | no | 1616 | 2338 | 1095 | 396% |
| fes_objective | 10 | 212 | 2 | confirmed | 88 | 91 | 0 | 95% |
| fes_tutorial | 14 | 309 | 3 | confirmed | 144 | 341 | 0 | 90% |
| mission_objective | 10 | 214 | 2 | confirmed | 216 | 389 | 0 | 95% |
| mission_story | 11 | 429 / 415 | 2 | confirmed | 216 | 432 | 0 | 90% |
| ms_desc | 14 | 434 | 2 | no | 102 | 204 | 0 | 92% |
| ms_name | 14 | 364 | 1 | no | 102 | 102 | 0 | 78% |
| narration | 12 | 468 | 1 | confirmed | 223 | 223 | 0 | 95% |
| nn_figure | 14 | 252 | 1 | no | 202 | 202 | 0 | 83% |
| nn_gallery | 14 | 168 | 1 | no | 1000 | 1000 | 0 | 89% |
| nn_other | 14 | 112 | 1 | no | 23 | 23 | 0 | 91% |
| nn_pilot | 14 | 252 | 1 | no | 74 | 74 | 0 | 87% |
| nn_song | 14 | 329 | 1 | no | 87 | 87 | 0 | 80% |
| nn_title | 14 | 252 | 1 | no | 300 | 300 | 0 | 92% |
| nn_unit | 14 | 196 | 1 | no | 98 | 98 | 0 | 81% |
| pack_desc | 14 | 322 | 1 | no | 32 | 32 | 0 | 90% |
| pack_name | 14 | 280 | 1 | no | 32 | 32 | 0 | 73% |
| pilot_desc | 14 | 434 | 3 | no | 93 | 251 | 0 | 92% |

## Lines over the limit (1107)

### eboot_bonus (1)

| Id | Line | Width | Limit | Over | Issue | English |
| --- | --- | --- | --- | --- | --- | --- |
| `eboot:382C68` | 1 | 144 | 140 | 4 | width | Repel Bird Human Fast |

### eboot_list:35D624 (6)

| Id | Line | Width | Limit | Over | Issue | English |
| --- | --- | --- | --- | --- | --- | --- |
| `eboot:3B498C` | 1 | 76 | 42 | 34 | width | Ldg. Airman |
| `eboot:3B4984` | 1 | 69 | 42 | 27 | width | Div. Cmdr. |
| `eboot:3B48DC` | 1 | 56 | 42 | 14 | width | Sgt. Maj. |
| `eboot:3B497C` | 1 | 48 | 42 | 6 | width | Civilian |
| `eboot:3B4958` | 1 | 47 | 42 | 5 | width | Lt. Col. |
| `eboot:3B490C` | 1 | 44 | 42 | 2 | width | 2nd Lt. |

### eboot_list:3ED9F8 (5)

| Id | Line | Width | Limit | Over | Issue | English |
| --- | --- | --- | --- | --- | --- | --- |
| `eboot:393BFC` | 1 | 46 | 14 | 32 | width | Cloudy |
| `eboot:393C0C` | 1 | 35 | 14 | 21 | width | Snow |
| `eboot:393BF8` | 1 | 33 | 14 | 19 | width | Clear |
| `eboot:393C00` | 1 | 28 | 14 | 14 | width | Rain |
| `eboot:393C04` | 1 | 23 | 14 | 9 | width | Fog |

### eboot_self (1095)

| Id | Line | Width | Limit | Over | Issue | English |
| --- | --- | --- | --- | --- | --- | --- |
| `eboot:387ED8` | 1 | 305 | 154 | 151 | width (soft) | Small-Caliber Anti-Personnel Laser Machine Gun |
| `eboot:387CD0` | 1 | 301 | 154 | 147 | width (soft) | Medium-Caliber Charged Particle Beam Cannon |
| `eboot:3878BC` | 1 | 220 | 84 | 136 | width (soft) | Anti-Air/Anti-Ground Machine Gun |
| `eboot:38740C` | 1 | 289 | 154 | 135 | width (soft) | Liquid-Cooled Charged Particle Beam Cannon |
| `eboot:387DAC` | 2 | 342 | 210 | 132 | width (soft) | Anti-air machine gun mounted on the back of the head |
| `eboot:387ADC` | 1 | 213 | 84 | 129 | width (soft) | Heavy Quantum Reaction Cannon |
| `eboot:38584C` | 1 | 280 | 154 | 126 | width (soft) | Single-Barrel Charged Particle Beam Cannon |
| `eboot:387A24` | 1 | 278 | 154 | 124 | width (soft) | Twin Guided Anti-Ship Heavy Beam Cannon |
| `eboot:387CA4` | 2 | 303 | 182 | 121 | width (soft) | Warps with power beyond human understanding |
| `eboot:3B1544` | 1 | 373 | 252 | 121 | width (soft) | A match cannot be played with everyone on the same team. |
| `eboot:3BBA48` | 2 | 288 | 168 | 120 | width (soft) | Series: The Super Dimension Fortress Macross |
| `eboot:3BBAA8` | 2 | 288 | 168 | 120 | width (soft) | Series: The Super Dimension Fortress Macross |
| `eboot:3BBB14` | 2 | 288 | 168 | 120 | width (soft) | Series: The Super Dimension Fortress Macross |
| `eboot:3BBB7C` | 2 | 288 | 168 | 120 | width (soft) | Series: The Super Dimension Fortress Macross |
| `eboot:3BBBF0` | 2 | 288 | 168 | 120 | width (soft) | Series: The Super Dimension Fortress Macross |
| `eboot:387E60` | 1 | 273 | 154 | 119 | width (soft) | Long-Range Charged Particle Beam Cannon |
| `eboot:387ADC` | 2 | 271 | 154 | 117 | width (soft) | Fires the Heavy Quantum Reaction Cannon |
| `eboot:387ED8` | 2 | 312 | 196 | 116 | width (soft) | Anti-personnel machine gun mounted on the head |
| `eboot:388A68` | 2 | 214 | 98 | 116 | width (soft) | Rams into the target with its body |
| `eboot:3887A8` | 2 | 265 | 154 | 111 | width (soft) | A shockwave released from its entire body |
| `eboot:3878BC` | 2 | 320 | 210 | 110 | width (soft) | Machine guns mounted on the chest and both arms |
| `eboot:387DAC` | 1 | 262 | 154 | 108 | width (soft) | Small-Caliber Anti-Air Laser Machine Gun |
| `eboot:3B6DF8` | 1 | 178 | 70 | 108 | width (soft) | Super Dimension Restaurant |
| `eboot:38A1B0` | 1 | 275 | 168 | 107 | width (soft) | Unmanned fighter with artificial intelligence |
| `eboot:38E848` | 1 | 219 | 112 | 107 | width (soft) | Become invincible for a short time. |
| `eboot:3B143C` | 1 | 287 | 182 | 105 | width (soft) | Due to the "Unit" rule setting, the current unit |
| `eboot:3878E8` | 1 | 272 | 168 | 104 | width (soft) | Triple Anti-Ground/Anti-Ship Heavy Missile |
| `eboot:38ACD4` | 1 | 314 | 210 | 104 | width (soft) | Variable attacker that can also operate underwater |
| `eboot:38B634` | 1 | 300 | 196 | 104 | width (soft) | Mainstay mobile weapon of the Mardook forces |
| `eboot:38B69C` | 1 | 300 | 196 | 104 | width (soft) | Mainstay mobile weapon of the Mardook forces |
| `eboot:3B31B4` | 1 | 295 | 192.5 | 102.5 | width (soft) | Resume the operation from where you left off? |
| `eboot:384FE8` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:3852D4` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:385588` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:3858DC` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:3863E8` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:386BDC` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:386DDC` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:386EBC` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:387030` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:387440` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:387804` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:387D14` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:3880E0` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:388BDC` | 2 | 354 | 252 | 102 | width (soft) | Missiles that can be fired in succession at a single enemy |
| `eboot:38E6F0` | 1 | 242 | 140 | 102 | width (soft) | Defense is doubled, and you no longer |
| `eboot:38EC60` | 2 | 338 | 238 | 100 | width (soft) | Zentradi-piloted units drop; other units grow stronger. |
| `eboot:38939C` | 2 | 323 | 224 | 99 | width (soft) | Being amphibious, it can be deployed in many roles |
| `eboot:38A01C` | 2 | 280 | 182 | 98 | width (soft) | The living core unit of Boddole Zer's flagship |
| `eboot:385C24` | 1 | 195 | 98 | 97 | width (soft) | Medium-Caliber Beam Cannon |
| `eboot:3879DC` | 2 | 223 | 126 | 97 | width (soft) | Klan fires you up with a rallying cry |
| `eboot:38B43C` | 2 | 307 | 210 | 97 | width (soft) | Carries a powerful large beam cannon on its back |
| `eboot:38AF60` | 2 | 236 | 140 | 96 | width (soft) | Luca's unit, an electronic warfare type |
| `eboot:38B0F8` | 2 | 236 | 140 | 96 | width (soft) | Luca's unit, an electronic warfare type |
| `eboot:3880E0` | 1 | 305 | 210 | 95 | width (soft) | Close-Range Small High-Mobility Missile (Rapid) |
| `eboot:388480` | 2 | 305 | 210 | 95 | width (soft) | Tentacles that can attack several enemies at once |
| `eboot:3B7534` | 1 | 137 | 42 | 95 | width (soft) | Overthrowing the Top |
| `eboot:3BCDFC` | 1 | 235 | 140 | 95 | width (soft) | Mission Continues (Macross Frontier) |
| `eboot:38991C` | 1 | 388 | 294 | 94 | width (soft) | Super Dimension Fortress rebuilt from a giant space battleship |
| `eboot:389BAC` | 1 | 388 | 294 | 94 | width (soft) | Super Dimension Fortress rebuilt from a giant space battleship |
| `eboot:3B8C74` | 1 | 206 | 112 | 94 | width (soft) | Go In and Get Smashed to Pieces |
| `eboot:3B9130` | 1 | 206 | 112 | 94 | width (soft) | Basara's Self-Proclaimed Disciple |
| `eboot:385B64` | 2 | 261 | 168 | 93 | width (soft) | Performs a melee attack with the bayonet |
| `eboot:388300` | 2 | 261 | 168 | 93 | width (soft) | Calls in underlings of the Quamzin family |
| `eboot:389260` | 1 | 315 | 224 | 91 | width (soft) | Variable fighter developed by the Anti-U.N. Forces |
| `eboot:3892B8` | 1 | 315 | 224 | 91 | width (soft) | Variable fighter developed by the Anti-U.N. Forces |
| `eboot:389330` | 1 | 315 | 224 | 91 | width (soft) | Variable fighter developed by the Anti-U.N. Forces |
| `eboot:3B6DEC` | 1 | 161 | 70 | 91 | width (soft) | Super Dimension Fortress |
| `eboot:3863A4` | 1 | 216 | 126 | 90 | width (soft) | MDE Particle Anti-Gravity Cannon |
| `eboot:38654C` | 2 | 314 | 224 | 90 | width (soft) | A large missile with tremendous destructive power |
| `eboot:3870BC` | 2 | 299 | 210 | 89 | width (soft) | High-speed autocannons mounted on both arms |
| `eboot:387138` | 2 | 299 | 210 | 89 | width (soft) | High-speed autocannons mounted on both arms |
| `eboot:387638` | 1 | 285 | 196 | 89 | width (soft) | OT Hypervelocity Electromagnetic Railcannon |
| `eboot:3870BC` | 1 | 381 | 294 | 87 | width (soft) | 78mm Liquid-Cooled High-Speed Autocannon (Machine Gun) |
| `eboot:3891F4` | 1 | 157 | 70 | 87 | width (soft) | Reaction Weapon Launch |
| `eboot:38E97C` | 2 | 297 | 210 | 87 | width (soft) | openings, and makes you invincible for a while. |
| `eboot:3BCFB8` | 4 | 325 | 238 | 87 | width (soft) | Lyrics: Toshiyuki Furuya  Music: Yoshiki Fukuyama |
| `eboot:3BD16C` | 4 | 325 | 238 | 87 | width (soft) | Lyrics: Toshiyuki Furuya  Music: Yoshiki Fukuyama |
| `eboot:387AA4` | 1 | 170 | 84 | 86 | width (soft) | Anti-Ship Reaction Weapon |
| `eboot:389050` | 2 | 296 | 210 | 86 | width (soft) | Upgraded attack and electronic warfare abilities |
| `eboot:3893F0` | 2 | 365 | 280 | 85 | width (soft) | Said to make the song of destruction roar across the world |
| `eboot:38BE3C` | 1 | 420 | 336 | 84 | width (soft) | Vajra homeworld guardian, the Super Dimension Cinderella. Kira☆ |
| `eboot:38784C` | 1 | 195 | 112 | 83 | width (soft) | Charged Particle Beam Cannon |
| `eboot:388824` | 2 | 321 | 238 | 83 | width (soft) | Fires Spiritia absorption beams from its entire body |
| `eboot:38A8DC` | 2 | 335 | 252 | 83 | width (soft) | Chlore's unit, with yellow as the pilot's personal color |
| `eboot:3928D0` | 2 | 223 | 140 | 83 | width (soft) | will be returned to the initial limits. |
| `eboot:3B6BDC` | 1 | 111 | 28 | 83 | width (soft) | Hardened Warrior |
| `eboot:3B7470` | 1 | 152 | 70 | 82 | width (soft) | Spare Me Your Opinions |
| `eboot:386FFC` | 1 | 221 | 140 | 81 | width (soft) | 57mm Multipurpose Rapid-Fire Gun |
| `eboot:389FB8` | 2 | 303 | 224 | 79 | width (soft) | A warrior who can down a Valkyrie bare-handed |
| `eboot:3857C0` | 2 | 274 | 196 | 78 | width (soft) | Missiles with tremendous destructive power |
| `eboot:386D58` | 2 | 274 | 196 | 78 | width (soft) | Missiles with tremendous destructive power |
| `eboot:38730C` | 2 | 274 | 196 | 78 | width (soft) | Missiles with tremendous destructive power |
| `eboot:387D64` | 1 | 274 | 196 | 78 | width (soft) | Close-Combat Large Multi-Warhead Missile |
| `eboot:3B7B08` | 1 | 204 | 126 | 78 | width (soft) | Guess I've lost too much blood... |
| `eboot:386F6C` | 1 | 273 | 196 | 77 | width (soft) | Triple-Mount Anti-Ground Missile Launcher |
| `eboot:385410` | 2 | 286 | 210 | 76 | width (soft) | A grenade with tremendous destructive power |
| `eboot:385524` | 2 | 412 | 336 | 76 | width (soft) | Missiles that fly straight at the enemy and cause a blast on impact |
| `eboot:38862C` | 2 | 258 | 182 | 76 | width (soft) | Autocannons mounted on both shoulders |
| `eboot:3B728C` | 1 | 118 | 42 | 76 | width (soft) | Half-Hatched Punk |
| `eboot:3B8B18` | 1 | 160 | 84 | 76 | width (soft) | Long-Range Support Type |
| `eboot:3B8CEC` | 1 | 118 | 42 | 76 | width (soft) | Booze and Women |
| `eboot:387604` | 1 | 243 | 168 | 75 | width (soft) | Guided Focused Beam Cannon System |
| `eboot:3884B4` | 1 | 201 | 126 | 75 | width (soft) | Omnidirectional Tentacle Attack |
| `eboot:389260` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38967C` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:389D88` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38A218` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38AD34` | 1 | 285 | 210 | 75 | width (soft) | A man obsessed with the white Galaxy Whale |
| `eboot:38AE10` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38AE74` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38B150` | 2 | 229 | 154 | 75 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:3B121C` | 2 | 159 | 84 | 75 | width (soft) | Waiting for other players. |
| `eboot:3859F8` | 1 | 242 | 168 | 74 | width (soft) | Long-Barrel High-Penetration Gun Pod |
| `eboot:386020` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:386060` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:3860AC` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:386114` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:38615C` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:3862B8` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:3862F4` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:38633C` | 2 | 256 | 182 | 74 | width (soft) | Sings a red-hot song that shakes the soul |
| `eboot:3884B4` | 2 | 242 | 168 | 74 | width (soft) | Tentacles that attack in every direction |
| `eboot:3884F0` | 2 | 241 | 168 | 73 | width (soft) | Performs a melee attack with tentacles |
| `eboot:38AFC4` | 2 | 269 | 196 | 73 | width (soft) | Alto's unit, tuned for high-mobility combat |
| `eboot:3B13D8` | 1 | 227 | 154 | 73 | width (soft) | The player and support cannot sortie |
| `eboot:3B5404` | 1 | 129 | 56 | 73 | width (soft) | Multipurpose Carrier |
| `eboot:3855D8` | 1 | 114 | 42 | 72 | width (soft) | Reaction Weapons |
| `eboot:387FD8` | 1 | 268 | 196 | 72 | width (soft) | Medium-Caliber Rapid-Fire Impact Cannon |
| `eboot:3886AC` | 2 | 268 | 196 | 72 | width (soft) | Beam cannons mounted on both shoulders |
| `eboot:38F310` | 2 | 226 | 154 | 72 | width (soft) | to 100% at the start of each mission. |
| `eboot:3B93BC` | 1 | 142 | 70 | 72 | width (soft) | Black-Rimmed Glasses |
| `eboot:385FE0` | 2 | 337 | 266 | 71 | width (soft) | Fires in speaker pods to make the target hear the song |
| `eboot:387708` | 2 | 253 | 182 | 71 | width (soft) | Fires harpoons made for catching whales |
| `eboot:38A01C` | 1 | 267 | 196 | 71 | width (soft) | Supreme commander of the Zentradi fleets |
| `eboot:38E6A8` | 1 | 127 | 56 | 71 | width (soft) | Standard Equipment |
| `eboot:395BC4` | 1 | 169 | 98 | 71 | width (soft) | Communication Sync Error |
| `eboot:38A804` | 1 | 336 | 266 | 70 | width (soft) | Variable attacker converted from a U.N. Forces design |
| `eboot:3B4AAC` | 1 | 196 | 126 | 70 | width (soft) | Nyan-Nyan Chinese Restaurant |
| `eboot:3B6C54` | 1 | 112 | 42 | 70 | width (soft) | First-Gen Diehard |
| `eboot:3B7144` | 1 | 126 | 56 | 70 | width (soft) | Vanguard of Beauty |
| `eboot:38ECBC` | 1 | 125 | 56 | 69 | width (soft) | Song of Destruction |
| `eboot:386370` | 2 | 307 | 238 | 69 | width (soft) | Main weapon developed for use against the Vajra |
| `eboot:3863A4` | 2 | 307 | 238 | 69 | width (soft) | Main weapon developed for use against the Vajra |
| `eboot:387500` | 1 | 293 | 224 | 69 | width (soft) | Liquid-Cooled 40cm Liquid-Propellant Cannon |
| `eboot:387F90` | 1 | 293 | 224 | 69 | width (soft) | Large-Caliber Mid-Range Fluid Plasma Cannon |
| `eboot:3B6B54` | 1 | 125 | 56 | 69 | width (soft) | Previous Game Title |
| `eboot:3B75F4` | 1 | 153 | 84 | 69 | width (soft) | You're not getting away! |
| `eboot:3B8AEC` | 1 | 167 | 98 | 69 | width (soft) | Close Range? Bring It On!! |
| `eboot:385D1C` | 1 | 194 | 126 | 68 | width (soft) | Semi-Fixed Laser Machine Gun |
| `eboot:386FFC` | 2 | 264 | 196 | 68 | width (soft) | Rapid-fire gun mounted on the upper head |
| `eboot:38A86C` | 1 | 334 | 266 | 68 | width (soft) | Variable bomber converted from a U.N. Forces design |
| `eboot:38E974` | 1 | 96 | 28 | 68 | width (soft) | Encouragement |
| `eboot:3B7048` | 1 | 124 | 56 | 68 | width (soft) | Kamikaze Daredevil |
| `eboot:385AF8` | 2 | 459 | 392 | 67 | width (soft) | Fires the shoulder-mounted twin beam cannon and the head laser cannon |
| `eboot:385DB4` | 2 | 361 | 294 | 67 | width (soft) | Standard main weapon of variable fighters (two equipped) |
| `eboot:385E64` | 2 | 361 | 294 | 67 | width (soft) | Standard main weapon of variable fighters (two equipped) |
| `eboot:3869D4` | 2 | 277 | 210 | 67 | width (soft) | Laser cannon mounted on the right shoulder |
| `eboot:3889F8` | 2 | 291 | 224 | 67 | width (soft) | A powerful laser fired from the top of the head |
| `eboot:3887E8` | 2 | 290 | 224 | 66 | width (soft) | A beam that absorbs a large amount of Spiritia |
| `eboot:38A0E8` | 2 | 304 | 238 | 66 | width (soft) | High-performing, but twitchy and hard to handle |
| `eboot:38A650` | 2 | 360 | 294 | 66 | width (soft) | Ray and Veffidas's unit, with green as their personal color |
| `eboot:3B58F4` | 1 | 108 | 42 | 66 | width (soft) | Reaction Weapon |
| `eboot:385EF4` | 1 | 163 | 98 | 65 | width (soft) | Semi-Fixed Beam Cannon |
| `eboot:38A278` | 1 | 289 | 224 | 65 | width (soft) | Variable fighter developed for special missions |
| `eboot:38A2D8` | 1 | 289 | 224 | 65 | width (soft) | Variable fighter developed for special missions |
| `eboot:38A34C` | 1 | 289 | 224 | 65 | width (soft) | Variable fighter developed for special missions |
| `eboot:38AAA0` | 1 | 289 | 224 | 65 | width (soft) | Variable fighter developed for special missions |
| `eboot:38EB50` | 1 | 275 | 210 | 65 | width (soft) | Freezes enemies for an instant, and you and |
| `eboot:3B8E34` | 1 | 177 | 112 | 65 | width (soft) | Macross 7 Fleet Commander |
| `eboot:38E83C` | 1 | 120 | 56 | 64 | width (soft) | Emergency Evasion |
| `eboot:3B88D0` | 1 | 120 | 56 | 64 | width (soft) | Cool and Collected |
| `eboot:363628` | 1 | 119 | 56 | 63 | width (soft) | Iron Wall Defender |
| `eboot:385BE8` | 1 | 175 | 112 | 63 | width (soft) | Small-Caliber Laser Cannon |
| `eboot:386584` | 1 | 175 | 112 | 63 | width (soft) | Small-Caliber Laser Cannon |
| `eboot:386CCC` | 2 | 217 | 154 | 63 | width (soft) | Machine gun mounted at the waist |
| `eboot:388124` | 1 | 343 | 280 | 63 | width (soft) | Close-Range Small High-Mobility Missile (Rapid/Blast) |
| `eboot:3B137C` | 1 | 273 | 210 | 63 | width (soft) | You will return to the mission select screen. |
| `eboot:3B5658` | 1 | 119 | 56 | 63 | width (soft) | Heavy Attack Craft |
| `eboot:3B5910` | 1 | 133 | 70 | 63 | width (soft) | Poachers' Mothership |
| `eboot:3B6E30` | 1 | 175 | 112 | 63 | width (soft) | Super Dimension Cinderella |
| `eboot:3B8628` | 1 | 231 | 168 | 63 | width (soft) | Heh, you came. Annihilation Beauty. |
| `eboot:38A93C` | 2 | 286 | 224 | 62 | width (soft) | A dim-witted monster with powerful weapons |
| `eboot:38F1B0` | 1 | 258 | 196 | 62 | width (soft) | Affinity changes at twice the normal rate. |
| `eboot:3B717C` | 1 | 118 | 56 | 62 | width (soft) | One Shot, One Kill |
| `eboot:386914` | 1 | 173 | 112 | 61 | width (soft) | Anti-Air Laser Machine Gun |
| `eboot:3871BC` | 1 | 173 | 112 | 61 | width (soft) | Anti-Air Laser Machine Gun |
| `eboot:38F1DC` | 1 | 131 | 70 | 61 | width (soft) | Signal to Strike Back |
| `eboot:3B2978` | 1 | 117 | 56 | 61 | width (soft) | Add-on Equipment |
| `eboot:3B884C` | 1 | 103 | 42 | 61 | width (soft) | Assistant Master |
| `eboot:3BC1AC` | 4 | 299 | 238 | 61 | width (soft) | Lyrics: Takashi Matsumoto  Music: Yoko Kanno |
| `eboot:3BCE24` | 4 | 299 | 238 | 61 | width (soft) | Lyrics: Takashi Matsumoto  Music: Yoko Kanno |
| `eboot:3BD53C` | 4 | 299 | 238 | 61 | width (soft) | Lyrics: Takashi Matsumoto  Music: Yoko Kanno |
| `eboot:3853BC` | 2 | 326 | 266 | 60 | width (soft) | Missiles that burst and split into several after launch |
| `eboot:385CE0` | 2 | 326 | 266 | 60 | width (soft) | Missiles that burst and split into several after launch |
| `eboot:389618` | 2 | 256 | 196 | 60 | width (soft) | A trainer, but also capable of real combat |
| `eboot:38B634` | 2 | 214 | 154 | 60 | width (soft) | Specializes in close-quarters melee |
| `eboot:3B2E08` | 4 | 158 | 98 | 60 | width (soft) | "%s"? |
| `eboot:3B2E7C` | 2 | 158 | 98 | 60 | width (soft) | "%s"? |
| `eboot:3BD25C` | 1 | 214 | 154 | 60 | width (soft) | Mission Continues (Macross Zero) |
| `eboot:3BD7F8` | 3 | 172 | 112 | 60 | width (soft) | Music: Nobuhiko Kashihara |
| `eboot:38D630` | 1 | 213 | 154 | 59 | width (soft) | The partner and support cannot be |
| `eboot:3B2E08` | 2 | 311 | 252 | 59 | width (soft) | It will be removed automatically when you sortie. |
| `eboot:38862C` | 1 | 198 | 140 | 58 | width (soft) | Twin Swivel Heavy Autocannon |
| `eboot:3886AC` | 1 | 142 | 84 | 58 | width (soft) | Anti-Air Beam Cannon |
| `eboot:38892C` | 1 | 268 | 210 | 58 | width (soft) | Medium-Caliber Rapid-Fire Impact Cannon |
| `eboot:3898AC` | 1 | 254 | 196 | 58 | width (soft) | High-performance commander's Valkyrie |
| `eboot:389A8C` | 1 | 254 | 196 | 58 | width (soft) | High-performance commander's Valkyrie |
| `eboot:389AEC` | 1 | 254 | 196 | 58 | width (soft) | High-performance commander's Valkyrie |
| `eboot:38B6FC` | 1 | 254 | 196 | 58 | width (soft) | High-performance commander's Valkyrie |
| `eboot:3BCAA8` | 1 | 212 | 154 | 58 | width (soft) | Mission Continues (SDF Macross) |
| `eboot:38967C` | 1 | 323 | 266 | 57 | width (soft) | Standard mass-produced Valkyrie of the VF-1 series |
| `eboot:3896DC` | 1 | 323 | 266 | 57 | width (soft) | Standard mass-produced Valkyrie of the VF-1 series |
| `eboot:389A18` | 1 | 323 | 266 | 57 | width (soft) | Standard mass-produced Valkyrie of the VF-1 series |
| `eboot:389C6C` | 2 | 267 | 210 | 57 | width (soft) | High-performance unit that excels in melee |
| `eboot:3B6BE4` | 1 | 113 | 56 | 57 | width (soft) | Swift as Lightning |
| `eboot:3B6C28` | 1 | 85 | 28 | 57 | width (soft) | God of Battle |
| `eboot:3B7498` | 1 | 85 | 28 | 57 | width (soft) | The Great Me |
| `eboot:3B7510` | 1 | 85 | 28 | 57 | width (soft) | Lethal Charm |
| `eboot:3B8C88` | 1 | 183 | 126 | 57 | width (soft) | To the Endth of the Galaxy☆ |
| `eboot:388FA8` | 1 | 182 | 126 | 56 | width (soft) | The U.N. Forces' main fighter |
| `eboot:38939C` | 1 | 350 | 294 | 56 | width (soft) | Amphibious Destroid developed by the Anti-U.N. Forces |
| `eboot:38A728` | 2 | 280 | 224 | 56 | width (soft) | Flown mainly by Varauta Army rank and file |
| `eboot:3B5A48` | 1 | 182 | 126 | 56 | width (soft) | Vajra Sub-Queen Mothership |
| `eboot:3B8828` | 1 | 112 | 56 | 56 | width (soft) | Headlong Charger |
| `eboot:3B8A10` | 1 | 112 | 56 | 56 | width (soft) | Records Strategist |
| `eboot:3BBE90` | 3 | 164 | 108.5 | 55.5 | width (soft) | Music: Atsutaka Kawauchi |
| `eboot:3BD6F8` | 3 | 164 | 108.5 | 55.5 | width (soft) | Music: Atsutaka Kawauchi |
| `eboot:3868A8` | 2 | 335 | 280 | 55 | width (soft) | Fires a heavy particle reaction beam from the gun pod |
| `eboot:38773C` | 1 | 97 | 42 | 55 | width (soft) | Harpoon Throw |
| `eboot:38844C` | 2 | 237 | 182 | 55 | width (soft) | Extends tentacles to attack the enemy |
| `eboot:38EB10` | 1 | 251 | 196 | 55 | width (soft) | Deals heavy damage to nearby enemies. |
| `eboot:3B1314` | 1 | 237 | 182 | 55 | width (soft) | You were disconnected from the host. |
| `eboot:3B8C60` | 1 | 167 | 112 | 55 | width (soft) | Nyan-Nyan Shop Exclusive |
| `eboot:3BD32C` | 1 | 125 | 70 | 55 | width (soft) | The Power to Reject |
| `eboot:3BD338` | 1 | 125 | 70 | 55 | width (soft) | The Power to Reject |
| `eboot:384F88` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:3859A4` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:385BA0` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:385C6C` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:385CA8` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:385E0C` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:38662C` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:386664` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:386B6C` | 2 | 264 | 210 | 54 | width (soft) | Standard main weapon of variable fighters |
| `eboot:387804` | 1 | 278 | 224 | 54 | width (soft) | Close-Range Anti-Air Quad Missile Launcher |
| `eboot:38836C` | 2 | 390 | 336 | 54 | width (soft) | Can send Zentradi soldiers charging at several enemies at once |
| `eboot:389CD0` | 2 | 250 | 196 | 54 | width (soft) | Excellent firepower, agility and mobility |
| `eboot:389D24` | 2 | 250 | 196 | 54 | width (soft) | Excellent firepower, agility and mobility |
| `eboot:389EC4` | 1 | 194 | 140 | 54 | width (soft) | A soldier of the Zentradi forces |
| `eboot:389EF8` | 1 | 110 | 56 | 54 | width (soft) | All-Forces Charge |
| `eboot:3BC1AC` | 3 | 236 | 182 | 54 | width (soft) | Vocals: Ranka Lee=Megumi Nakajima |
| `eboot:3BCE24` | 3 | 236 | 182 | 54 | width (soft) | Vocals: Ranka Lee=Megumi Nakajima |
| `eboot:3BD53C` | 3 | 236 | 182 | 54 | width (soft) | Vocals: Ranka Lee=Megumi Nakajima |
| `eboot:3861BC` | 2 | 347 | 294 | 53 | width (soft) | Fires in speaker pods to make the target hear the drums |
| `eboot:38D5EC` | 1 | 207 | 154 | 53 | width (soft) | The player and support cannot be |
| `eboot:3B7294` | 1 | 109 | 56 | 53 | width (soft) | Valued Customer |
| `eboot:3B902C` | 1 | 151 | 98 | 53 | width (soft) | "Nyan-Nyan" Poster Girl |
| `eboot:385324` | 2 | 150 | 98 | 52 | width (soft) | Performs a melee attack |
| `eboot:386768` | 1 | 304 | 252 | 52 | width (soft) | 57mm Anti-Ship/Anti-Air Rapid-Fire Beam Turret |
| `eboot:3894B4` | 2 | 220 | 168 | 52 | width (soft) | Heavily armored and highly mobile |
| `eboot:3B5708` | 1 | 122 | 70 | 52 | width (soft) | Vrlitwhai's Flagship |
| `eboot:3B888C` | 1 | 94 | 42 | 52 | width (soft) | Finesse Fighter |
| `eboot:3850D0` | 2 | 261 | 210 | 51 | width (soft) | Missiles that cause a huge blast on impact |
| `eboot:385934` | 2 | 261 | 210 | 51 | width (soft) | Missiles that cause a huge blast on impact |
| `eboot:3867D4` | 2 | 289 | 238 | 51 | width (soft) | Performs a melee attack with the assault knife |
| `eboot:386BA0` | 2 | 261 | 210 | 51 | width (soft) | Missiles that cause a huge blast on impact |
| `eboot:387138` | 1 | 331 | 280 | 51 | width (soft) | 78mm Liquid-Cooled High-Speed Autocannon (Laser) |
| `eboot:387354` | 1 | 317 | 266 | 51 | width (soft) | Short-Range High-Mobility Homing Missile (Multi) |
| `eboot:387D64` | 2 | 261 | 210 | 51 | width (soft) | Missiles that cause a huge blast on impact |
| `eboot:387E98` | 1 | 191 | 140 | 51 | width (soft) | Close-Combat Homing Missile |
| `eboot:3B9348` | 1 | 107 | 56 | 51 | width (soft) | Bit of an Airhead |
| `eboot:3BCDE4` | 1 | 191 | 140 | 51 | width (soft) | Mission Continues (Macross 7) |
| `eboot:38A0E8` | 1 | 246 | 196 | 50 | width (soft) | Prototype variable fighter for the VF-19 |
| `eboot:38A13C` | 1 | 246 | 196 | 50 | width (soft) | Prototype variable fighter for the VF-22 |
| `eboot:3B6ECC` | 1 | 78 | 28 | 50 | width (soft) | King of Fists |
| `eboot:3B7E34` | 1 | 218 | 168 | 50 | width (soft) | Perish! Scatter to the galaxy's end!! |
| `eboot:3BC2B4` | 3 | 162 | 112 | 50 | width (soft) | Music: Yoshiki Fukuyama |
| `eboot:3BD788` | 3 | 162 | 112 | 50 | width (soft) | Music: Yoshiki Fukuyama |
| `eboot:388588` | 2 | 231 | 182 | 49 | width (soft) | A flash grenade that blinds the target |
| `eboot:388678` | 2 | 245 | 196 | 49 | width (soft) | Beam cannons mounted on both hands |
| `eboot:389750` | 1 | 301 | 252 | 49 | width (soft) | Valkyrie with upgraded weapons over the VF-1A |
| `eboot:3897BC` | 1 | 301 | 252 | 49 | width (soft) | Valkyrie with upgraded weapons over the VF-1A |
| `eboot:389830` | 1 | 301 | 252 | 49 | width (soft) | Valkyrie with upgraded weapons over the VF-1A |
| `eboot:38F160` | 1 | 189 | 140 | 49 | width (soft) | Units that normally cannot fly |
| `eboot:3B7DB0` | 1 | 147 | 98 | 49 | width (soft) | It's in your hands now!! |
| `eboot:385ABC` | 2 | 314 | 266 | 48 | width (soft) | A single anti-air laser cannon mounted in the head |
| `eboot:386BDC` | 1 | 216 | 168 | 48 | width (soft) | Medium Anti-Ship Missiles (Rapid) |
| `eboot:387B70` | 2 | 370 | 322 | 48 | width (soft) | Can send Ghosts on suicide runs at several enemies at once |
| `eboot:3B4C28` | 1 | 104 | 56 | 48 | width (soft) | New U.N. Forces |
| `eboot:3B6DC4` | 1 | 76 | 28 | 48 | width (soft) | Fierce Deity |
| `eboot:3B6DCC` | 1 | 76 | 28 | 48 | width (soft) | Demon God |
| `eboot:3B72D8` | 1 | 104 | 56 | 48 | width (soft) | Storm of Thanks |
| `eboot:3B87BC` | 1 | 118 | 70 | 48 | width (soft) | Can't Stand Losing |
| `eboot:3B8804` | 1 | 104 | 56 | 48 | width (soft) | Luck Is Skill Too |
| `eboot:385230` | 2 | 299 | 252 | 47 | width (soft) | A single laser machine gun mounted in the head |
| `eboot:386A70` | 2 | 299 | 252 | 47 | width (soft) | A single laser machine gun mounted in the head |
| `eboot:3871BC` | 2 | 229 | 182 | 47 | width (soft) | Machine gun mounted atop the head |
| `eboot:388030` | 1 | 89 | 42 | 47 | width (soft) | Hand Grenade |
| `eboot:388588` | 1 | 89 | 42 | 47 | width (soft) | Flash Grenade |
| `eboot:388F00` | 1 | 117 | 70 | 47 | width (soft) | Hyper Speed Move |
| `eboot:3890AC` | 2 | 229 | 182 | 47 | width (soft) | Flown mainly by rank-and-file pilots |
| `eboot:38B3EC` | 2 | 299 | 252 | 47 | width (soft) | Agile, with a beam cannon on the tip of its head |
| `eboot:38EA00` | 1 | 89 | 42 | 47 | width (soft) | Bombing King |
| `eboot:3B6C0C` | 1 | 103 | 56 | 47 | width (soft) | Battle-Hardened |
| `eboot:3B7008` | 1 | 131 | 84 | 47 | width (soft) | Militant Commander |
| `eboot:3B7100` | 1 | 103 | 56 | 47 | width (soft) | Beautiful Mayor |
| `eboot:3B9058` | 1 | 89 | 42 | 47 | width (soft) | Shao Pai Long |
| `eboot:3B92B0` | 1 | 89 | 42 | 47 | width (soft) | Song Priestess |
| `eboot:3B92CC` | 1 | 103 | 56 | 47 | width (soft) | Wholesome Boy |
| `eboot:38777C` | 1 | 172 | 126 | 46 | width (soft) | Burning Passion for Whales |
| `eboot:389A18` | 2 | 270 | 224 | 46 | width (soft) | Hikaru's unit, with red as his personal color |
| `eboot:389A8C` | 2 | 270 | 224 | 46 | width (soft) | Hikaru's unit, with red as his personal color |
| `eboot:38AB0C` | 1 | 312 | 266 | 46 | width (soft) | Variable fighter developed from an improved VF-1 |
| `eboot:38AB70` | 1 | 312 | 266 | 46 | width (soft) | Variable fighter developed from an improved VF-1 |
| `eboot:38EF0C` | 1 | 144 | 98 | 46 | width (soft) | Missile Disposal Squad |
| `eboot:3987DC` | 1 | 200 | 154 | 46 | width (soft) | The connection was interrupted. |
| `eboot:3B75D0` | 1 | 88 | 42 | 46 | width (soft) | Soothing Soul |
| `eboot:3B836C` | 1 | 214 | 168 | 46 | width (soft) | What was that mountain called...? |
| `eboot:3B83C8` | 1 | 214 | 168 | 46 | width (soft) | I'll make the universe ring with it!! |
| `eboot:3B8684` | 1 | 214 | 168 | 46 | width (soft) | How dare mere lower lifeforms...!! |
| `eboot:3B8A40` | 1 | 116 | 70 | 46 | width (soft) | All Units Obtained |
| `eboot:3BAF68` | 2 | 158 | 112 | 46 | width (soft) | "%s"? |
| `eboot:3BD878` | 4 | 326 | 280 | 46 | width (soft) | Arrangement: Son Rui, Yuna Katsuki, Keisuke Iizuka |
| `eboot:3B8F8C` | 1 | 115 | 70 | 45 | width (soft) | Guide of the Wind |
| `eboot:389218` | 1 | 213 | 168 | 45 | width (soft) | The Anti-U.N. Forces' main fighter |
| `eboot:389510` | 1 | 241 | 196 | 45 | width (soft) | Close-in air defense Destroid for space |
| `eboot:38E878` | 1 | 255 | 210 | 45 | width (soft) | The Boost Gauge is no longer consumed. |
| `eboot:38EA34` | 1 | 101 | 56 | 45 | width (soft) | Legendary Elixir |
| `eboot:38EC04` | 1 | 269 | 224 | 45 | width (soft) | Attack power of you and your allies triples, |
| `eboot:3B6BB4` | 1 | 87 | 42 | 45 | width (soft) | The Real Deal |
| `eboot:3B6C18` | 1 | 87 | 42 | 45 | width (soft) | King of Melee |
| `eboot:3B7E0C` | 1 | 157 | 112 | 45 | width (soft) | You're in my way. Move! |
| `eboot:387070` | 2 | 268 | 224 | 44 | width (soft) | Beam machine gun mounted atop the head |
| `eboot:389F0C` | 1 | 128 | 84 | 44 | width (soft) | All-Forces Full Salvo |
| `eboot:38A1B0` | 2 | 296 | 252 | 44 | width (soft) | Being unmanned, it can fight at extreme speeds |
| `eboot:38F090` | 1 | 86 | 42 | 44 | width (soft) | Drill Sergeant |
| `eboot:3B734C` | 1 | 72 | 28 | 44 | width (soft) | Self-Taught |
| `eboot:3B7958` | 1 | 212 | 168 | 44 | width (soft) | Why did you come to this planet? |
| `eboot:3BD7DC` | 1 | 212 | 168 | 44 | width (soft) | Quiet, Like 200 Million Years Ago |
| `eboot:3BD7F8` | 1 | 212 | 168 | 44 | width (soft) | Quiet, Like 200 Million Years Ago |
| `eboot:386730` | 2 | 253 | 210 | 43 | width (soft) | Beam machine gun mounted in the head |
| `eboot:38873C` | 2 | 253 | 210 | 43 | width (soft) | A powerful beam fired from a pentagram |
| `eboot:3887A8` | 1 | 71 | 28 | 43 | width (soft) | Pulse Wave |
| `eboot:389300` | 1 | 127 | 84 | 43 | width (soft) | Fuel-Air Bomb Drop |
| `eboot:3B8B28` | 1 | 141 | 98 | 43 | width (soft) | Shooting Attack Usage |
| `eboot:3BCDC8` | 1 | 211 | 168 | 43 | width (soft) | Mission Continues (Macross Plus) |
| `eboot:38740C` | 2 | 238 | 196 | 42 | width (soft) | Beam cannons mounted on both arms |
| `eboot:38773C` | 2 | 294 | 252 | 42 | width (soft) | Can throw harpoons at several enemies at once |
| `eboot:38784C` | 2 | 238 | 196 | 42 | width (soft) | Beam cannons mounted on both arms |
| `eboot:389490` | 1 | 126 | 84 | 42 | width (soft) | Spinning Super Shot |
| `eboot:3895A0` | 1 | 126 | 84 | 42 | width (soft) | Super Flamethrower |
| `eboot:389A60` | 1 | 126 | 84 | 42 | width (soft) | Squadron Full Salvo |
| `eboot:389C14` | 2 | 210 | 168 | 42 | width (soft) | Simple in design and easy to field |
| `eboot:38A054` | 1 | 98 | 56 | 42 | width (soft) | Tentacle Frenzy |
| `eboot:38B4F8` | 2 | 280 | 238 | 42 | width (soft) | Brera's unit, with purple as his personal color |
| `eboot:38F304` | 1 | 98 | 56 | 42 | width (soft) | Quick Recovery |
| `eboot:38F4D8` | 1 | 140 | 98 | 42 | width (soft) | Chinese Diner Regular |
| `eboot:3B7984` | 1 | 196 | 154 | 42 | width (soft) | No one else gets the white one! |
| `eboot:3BAFB4` | 4 | 154 | 112 | 42 | width (soft) | "%s". |
| `eboot:3BB038` | 2 | 154 | 112 | 42 | width (soft) | "%s". |
| `eboot:388870` | 2 | 237 | 196 | 41 | width (soft) | A black hole that swallows everything |
| `eboot:3892B8` | 2 | 293 | 252 | 41 | width (soft) | Nora's unit, with magenta as her personal color |
| `eboot:389EC4` | 2 | 251 | 210 | 41 | width (soft) | A giant five times the height of a human |
| `eboot:38EAB4` | 1 | 223 | 182 | 41 | width (soft) | Attack power of you and your allies |
| `eboot:38ED48` | 1 | 279 | 238 | 41 | width (soft) | Reverses the up/down and left/right controls |
| `eboot:38F0F0` | 1 | 69 | 28 | 41 | width (soft) | Awakening |
| `eboot:38F2D0` | 1 | 181 | 140 | 41 | width (soft) | SP Gauge consumption drops |
| `eboot:3B6BF0` | 1 | 69 | 28 | 41 | width (soft) | Crack Pilot |
| `eboot:3B70DC` | 1 | 111 | 70 | 41 | width (soft) | Strongest Captain |
| `eboot:3B72A0` | 1 | 125 | 84 | 41 | width (soft) | Owned at start with |
| `eboot:3B8E14` | 1 | 111 | 70 | 41 | width (soft) | Street Performer? |
| `eboot:3BBE04` | 1 | 181 | 140 | 41 | width (soft) | Totsugeki Love Heart (Vocal) |
| `eboot:385AF8` | 1 | 275 | 234.5 | 40.5 | width (soft) | AA Pulse Laser Cannon/Twin Beam Cannon |
| `eboot:389124` | 2 | 320 | 280 | 40 | width (soft) | Roy Focker's unit, marked with his skull trademark |
| `eboot:38F3B0` | 1 | 250 | 210 | 40 | width (soft) | Nyan-Nyan Points earned drop to 0, but |
| `eboot:392AE0` | 1 | 194 | 154 | 40 | width (soft) | The partner and support cannot |
| `eboot:3B1280` | 2 | 264 | 224 | 40 | width (soft) | Start wireless play with this many players. |
| `eboot:3B14E4` | 1 | 194 | 154 | 40 | width (soft) | The selected pilot cannot sortie |
| `eboot:3B5C84` | 1 | 82 | 42 | 40 | width (soft) | Not Acquired |
| `eboot:3B9E30` | 2 | 432 | 392 | 40 | width (soft) | press the analog stick left/right to switch between each era's factions. |
| `eboot:363448` | 1 | 109 | 70 | 39 | width (soft) | Expert Marksman |
| `eboot:3B9000` | 1 | 109 | 70 | 39 | width (soft) | Love Drifts Away |
| `eboot:386200` | 2 | 249 | 210 | 39 | width (soft) | Plays red-hot drums that shake the soul |
| `eboot:3883DC` | 2 | 333 | 294 | 39 | width (soft) | Can send soldiers charging at several enemies at once |
| `eboot:388FF4` | 2 | 291 | 252 | 39 | width (soft) | Used as anti-air weaponry on the carrier Asuka |
| `eboot:3890F0` | 1 | 165 | 126 | 39 | width (soft) | Melee Combo (Transform) |
| `eboot:3891AC` | 2 | 305 | 266 | 39 | width (soft) | Has four cannons that can load reaction weapons |
| `eboot:38EDA8` | 2 | 291 | 252 | 39 | width (soft) | *Hold the L button when activating for no SPA |
| `eboot:38EE70` | 1 | 81 | 42 | 39 | width (soft) | Clairvoyance |
| `eboot:38EEC8` | 1 | 81 | 42 | 39 | width (soft) | Medic Squad |
| `eboot:3B7278` | 1 | 95 | 56 | 39 | width (soft) | Owned at Start |
| `eboot:3BAE78` | 1 | 207 | 168 | 39 | width (soft) | Start without carrying over data? |
| `eboot:385038` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:385080` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:385880` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:386448` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:386F6C` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:387354` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:3878E8` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:387E98` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:388678` | 1 | 178 | 140 | 38 | width (soft) | Built-In Pulse Beam Cannon |
| `eboot:3889B0` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:388BAC` | 2 | 234 | 196 | 38 | width (soft) | Attacks with the claws on both hands |
| `eboot:388C18` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:388D18` | 2 | 318 | 280 | 38 | width (soft) | Missiles that can lock onto several enemies at once |
| `eboot:3893F0` | 1 | 206 | 168 | 38 | width (soft) | A god of legend on Mayan Island |
| `eboot:3BBDB8` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC1AC` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC3A4` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC3DC` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC5EC` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC650` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BC6E4` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BCE24` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BCE94` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BD37C` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:3BD53C` | 2 | 150 | 112 | 38 | width (soft) | Series: Macross Frontier |
| `eboot:386114` | 1 | 177 | 140 | 37 | width (soft) | Song (Totsugeki Love Heart) |
| `eboot:3885F0` | 2 | 177 | 140 | 37 | width (soft) | Attacks with a flamethrower |
| `eboot:3888F4` | 1 | 177 | 140 | 37 | width (soft) | Large-Caliber Beam Cannon |
| `eboot:38D5A8` | 1 | 205 | 168 | 37 | width (soft) | The player and partner cannot be |
| `eboot:38E800` | 2 | 177 | 140 | 37 | width (soft) | negates solid-ammo attacks. |
| `eboot:361328` | 1 | 92 | 56 | 36 | width (soft) | Rookie Soldier |
| `eboot:385230` | 1 | 120 | 84 | 36 | width (soft) | Laser Machine Gun |
| `eboot:385264` | 1 | 120 | 84 | 36 | width (soft) | Laser Machine Gun |
| `eboot:3855F8` | 1 | 120 | 84 | 36 | width (soft) | Laser Machine Gun |
| `eboot:385ABC` | 1 | 176 | 140 | 36 | width (soft) | Anti-Air Pulse Laser Cannon |
| `eboot:386A70` | 1 | 176 | 140 | 36 | width (soft) | Anti-Air Pulse Laser Cannon |
| `eboot:386AAC` | 1 | 176 | 140 | 36 | width (soft) | Anti-Air Pulse Laser Cannon |
| `eboot:386D1C` | 1 | 92 | 56 | 36 | width (soft) | Fuel-Air Bomb |
| `eboot:387F90` | 2 | 288 | 252 | 36 | width (soft) | Plasma cannon mounted on the right shoulder |
| `eboot:38836C` | 1 | 92 | 56 | 36 | width (soft) | Soldier Charge |
| `eboot:3883DC` | 1 | 92 | 56 | 36 | width (soft) | Soldier Charge |
| `eboot:388548` | 1 | 162 | 126 | 36 | width (soft) | Spiritia Absorption Device |
| `eboot:38F03C` | 2 | 260 | 224 | 36 | width (soft) | you are invincible for a while. *Once only |
| `eboot:38F3A4` | 1 | 92 | 56 | 36 | width (soft) | Tuning Fanatic |
| `eboot:3B6BBC` | 1 | 78 | 42 | 36 | width (soft) | Full-Fledged |
| `eboot:3B6D60` | 1 | 92 | 56 | 36 | width (soft) | Up-and-Comer |
| `eboot:3B6E54` | 1 | 78 | 42 | 36 | width (soft) | Fan Favorite |
| `eboot:3B6F04` | 1 | 120 | 84 | 36 | width (soft) | GERWALK Diehard |
| `eboot:3B7448` | 1 | 106 | 70 | 36 | width (soft) | No Holding Back |
| `eboot:3B77C4` | 1 | 204 | 168 | 36 | width (soft) | Where's the Bird Human's head? |
| `eboot:3B8D74` | 1 | 106 | 70 | 36 | width (soft) | Strongest Groom |
| `eboot:35DCC8` | 1 | 88 | 52.5 | 35.5 | width (soft) | Hikaru Ichijyo |
| `eboot:3B6F30` | 1 | 88 | 52.5 | 35.5 | width (soft) | Hikaru Ichijyo |
| `eboot:38730C` | 1 | 315 | 280 | 35 | width (soft) | Short-Range High-Mobility Homing Missile (Blast) |
| `eboot:387604` | 2 | 203 | 168 | 35 | width (soft) | Fires beams from its entire body |
| `eboot:38787C` | 2 | 161 | 126 | 35 | width (soft) | Calls in Cheyenne II units |
| `eboot:387A24` | 2 | 203 | 168 | 35 | width (soft) | Fires beams from its entire body |
| `eboot:3898AC` | 2 | 343 | 308 | 35 | width (soft) | The Skull Leader's unit, marked with a skull trademark |
| `eboot:38B1B4` | 2 | 287 | 252 | 35 | width (soft) | Klan's unit, with crimson as her personal color |
| `eboot:38E6C0` | 1 | 231 | 196 | 35 | width (soft) | Fully restores ammo for all weapons. |
| `eboot:38E9CC` | 1 | 245 | 210 | 35 | width (soft) | Attack power, speed and boost capacity |
| `eboot:38F460` | 1 | 189 | 154 | 35 | width (soft) | Halves the effects of all songs. |
| `eboot:38F534` | 2 | 175 | 140 | 35 | width (soft) | already charged to 3 blocks. |
| `eboot:3B1858` | 1 | 231 | 196 | 35 | width (soft) | The screenshots you took will not be |
| `eboot:3B6CD0` | 1 | 91 | 56 | 35 | width (soft) | Star Performer |
| `eboot:3BBE1C` | 1 | 133 | 98 | 35 | width (soft) | Totsugeki Love Heart |
| `eboot:3BBE80` | 1 | 133 | 98 | 35 | width (soft) | Totsugeki Love Heart |
| `eboot:3BBE90` | 1 | 133 | 98 | 35 | width (soft) | Totsugeki Love Heart |
| `eboot:3BD038` | 1 | 63 | 28 | 35 | width (soft) | Encounter |
| `eboot:3BD040` | 1 | 63 | 28 | 35 | width (soft) | Encounter |
| `eboot:386AF0` | 2 | 244 | 210 | 34 | width (soft) | Captures the target with a balloon shot |
| `eboot:3873A4` | 1 | 356 | 322 | 34 | width (soft) | Short-Range High-Mobility Homing Missile (Rapid/Blast) |
| `eboot:3888F4` | 2 | 272 | 238 | 34 | width (soft) | Beam cannon mounted on the left shoulder |
| `eboot:388B08` | 2 | 328 | 294 | 34 | width (soft) | Rapid-fire missiles that create a huge blast on impact |
| `eboot:388E40` | 2 | 328 | 294 | 34 | width (soft) | Rapid-fire missiles that create a huge blast on impact |
| `eboot:38AC50` | 2 | 286 | 252 | 34 | width (soft) | Gamlin's unit, with black as his personal color |
| `eboot:38F24C` | 1 | 202 | 168 | 34 | width (soft) | Boost Gauge consumption drops |
| `eboot:392AA4` | 1 | 188 | 154 | 34 | width (soft) | The player and support cannot |
| `eboot:3B9E30` | 1 | 314 | 280 | 34 | width (soft) | When selecting units and characters in the Hangar, |
| `eboot:3BCE14` | 1 | 132 | 98 | 34 | width (soft) | Seikan Hikou (Vocal) |
| `eboot:3855F8` | 2 | 285 | 252 | 33 | width (soft) | Four laser machine guns mounted in the head |
| `eboot:388030` | 2 | 145 | 112 | 33 | width (soft) | Throws a hand grenade |
| `eboot:392BB4` | 1 | 257 | 224 | 33 | width (soft) | Switch eras with Left/Right on the D-pad |
| `eboot:3B0B98` | 1 | 61 | 28 | 33 | width (soft) | Unknown |
| `eboot:3B5038` | 1 | 61 | 28 | 33 | width (soft) | Unknown |
| `eboot:3B73C8` | 1 | 89 | 56 | 33 | width (soft) | Proud Camper |
| `eboot:3B82E4` | 1 | 229 | 196 | 33 | width (soft) | Me... the one hailed as Ace of Aces... |
| `eboot:3B89EC` | 2 | 117 | 84 | 33 | width (soft) | All Skills Obtained |
| `eboot:3B8C9C` | 1 | 117 | 84 | 33 | width (soft) | Professor Piro-Piro |
| `eboot:3BD420` | 1 | 201 | 168 | 33 | width (soft) | Sara (Skill: Song of Destruction) |
| `eboot:3BD43C` | 1 | 201 | 168 | 33 | width (soft) | Sara (Skill: Song of Destruction) |
| `eboot:38851C` | 2 | 158 | 126 | 32 | width (soft) | Standard main armament |
| `eboot:38E93C` | 1 | 298 | 266 | 32 | width (soft) | Receive covering fire from the Macross Cannon. |
| `eboot:38ECFC` | 1 | 200 | 168 | 32 | width (soft) | Sivil appears in front of you and |
| `eboot:3B4F70` | 1 | 200 | 168 | 32 | width (soft) | Sheryl Nome (Military Uniform) |
| `eboot:3B6BD4` | 1 | 60 | 28 | 32 | width (soft) | Instructor |
| `eboot:3B92F0` | 1 | 102 | 70 | 32 | width (soft) | Reliable Big Bro |
| `eboot:3B9718` | 1 | 172 | 140 | 32 | width (soft) | Training Completion Bonus |
| `eboot:385264` | 2 | 283 | 252 | 31 | width (soft) | Two laser machine guns mounted in the head |
| `eboot:385450` | 2 | 241 | 210 | 31 | width (soft) | Standard main weapon of the Valkyrie |
| `eboot:3854A0` | 2 | 241 | 210 | 31 | width (soft) | Standard main weapon of the Valkyrie |
| `eboot:3854CC` | 2 | 241 | 210 | 31 | width (soft) | Standard main weapon of the Valkyrie |
| `eboot:386914` | 2 | 283 | 252 | 31 | width (soft) | Two laser machine guns mounted in the head |
| `eboot:386AAC` | 2 | 283 | 252 | 31 | width (soft) | Two laser machine guns mounted in the head |
| `eboot:386E3C` | 1 | 213 | 182 | 31 | width (soft) | Large 6-Barrel AA Gatling Cannon |
| `eboot:3895C4` | 1 | 213 | 182 | 31 | width (soft) | Ultra-long-range artillery Destroid |
| `eboot:389F8C` | 1 | 101 | 70 | 31 | width (soft) | Super Full Salvo |
| `eboot:38BE3C` | 2 | 227 | 196 | 31 | width (soft) | She controls the Vajra with her song |
| `eboot:3B7304` | 1 | 59 | 28 | 31 | width (soft) | Nameless |
| `eboot:35DF48` | 1 | 97 | 66.5 | 30.5 | width (soft) | Hayao Kakizaki |
| `eboot:35DFE8` | 1 | 97 | 66.5 | 30.5 | width (soft) | Hayao Kakizaki |
| `eboot:387708` | 1 | 114 | 84 | 30 | width (soft) | Harpoon Launcher |
| `eboot:389330` | 2 | 282 | 252 | 30 | width (soft) | Ivanov's unit, with black as his personal color |
| `eboot:38AAA0` | 2 | 310 | 280 | 30 | width (soft) | The unit Liza stole to escape the black marketeers |
| `eboot:3B49CC` | 1 | 72 | 42 | 30 | width (soft) | U.N. Forces |
| `eboot:38ED38` | 1 | 128 | 98 | 30 | width (soft) | Sharon's Temptation |
| `eboot:3B5618` | 1 | 100 | 70 | 30 | width (soft) | Air Combat Pod |
| `eboot:3B7638` | 1 | 114 | 84 | 30 | width (soft) | Versus Matches: 3 |
| `eboot:3B7A44` | 1 | 184 | 154 | 30 | width (soft) | I'll borrow your luck for now. |
| `eboot:3BC2F8` | 3 | 233 | 203 | 30 | width (soft) |         & Ranka Lee=Megumi Nakajima |
| `eboot:3BC928` | 1 | 114 | 84 | 30 | width (soft) | Roar of the Giants |
| `eboot:3BC938` | 1 | 114 | 84 | 30 | width (soft) | Roar of the Giants |
| `eboot:3BCD14` | 3 | 233 | 203 | 30 | width (soft) |         & Ranka Lee=Megumi Nakajima |
| `eboot:3BD074` | 3 | 233 | 203 | 30 | width (soft) |         & Ranka Lee=Megumi Nakajima |
| `eboot:3BD5DC` | 3 | 233 | 203 | 30 | width (soft) |         & Ranka Lee=Megumi Nakajima |
| `eboot:38E6E8` | 1 | 57 | 28 | 29 | width (soft) | Iron Wall |
| `eboot:38EAFC` | 1 | 99 | 70 | 29 | width (soft) | The Last Supper |
| `eboot:3B11CC` | 1 | 155 | 126 | 29 | width (soft) | The operation will begin. |
| `eboot:3B1520` | 1 | 267 | 238 | 29 | width (soft) | Not enough players have joined the match. |
| `eboot:3B7558` | 1 | 85 | 56 | 29 | width (soft) | Late Bloomer |
| `eboot:3B75A8` | 1 | 85 | 56 | 29 | width (soft) | Punching Bag |
| `eboot:3B7660` | 1 | 113 | 84 | 29 | width (soft) | Versus Matches: 5 |
| `eboot:3BC230` | 4 | 379 | 350 | 29 | width (soft) | Lyrics: K.Inojo, Kyoko Fukuyama  Music: Yoshiki Fukuyama |
| `eboot:3BCB30` | 4 | 379 | 350 | 29 | width (soft) | Lyrics: K.Inojo, Kyoko Fukuyama  Music: Yoshiki Fukuyama |
| `eboot:3BBB7C` | 4 | 263 | 234.5 | 28.5 | width (soft) | Lyrics: Akane Asa  Music: Kentaro Haneda |
| `eboot:38AA20` | 2 | 308 | 280 | 28 | width (soft) | Armed with a harpoon gun pod for whale hunting |
| `eboot:38AD24` | 1 | 70 | 42 | 28 | width (soft) | Diving Suit |
| `eboot:38B028` | 2 | 266 | 238 | 28 | width (soft) | Ozma's unit, an upgraded commander type |
| `eboot:38E930` | 1 | 84 | 56 | 28 | width (soft) | Covering Fire |
| `eboot:3B49E4` | 1 | 84 | 56 | 28 | width (soft) | Mayan Island |
| `eboot:3B66A4` | 1 | 350 | 322 | 28 | width (soft) | The color settings will be reset to default. Are you sure? |
| `eboot:3B6D7C` | 1 | 84 | 56 | 28 | width (soft) | Head Honcho |
| `eboot:3B741C` | 1 | 112 | 84 | 28 | width (soft) | Master of Evasion |
| `eboot:3B7604` | 1 | 112 | 84 | 28 | width (soft) | Versus Matches: 1 |
| `eboot:3B7690` | 1 | 112 | 84 | 28 | width (soft) | Versus Matches: 7 |
| `eboot:3B76A0` | 1 | 168 | 140 | 28 | width (soft) | Can you keep up with me? |
| `eboot:3B8198` | 1 | 210 | 182 | 28 | width (soft) | *pant pant*... Ah... how beautiful. |
| `eboot:3B9184` | 1 | 84 | 56 | 28 | width (soft) | Seikan Hikou |
| `eboot:3BCE24` | 1 | 84 | 56 | 28 | width (soft) | Seikan Hikou |
| `eboot:3BB89C` | 3 | 136 | 108.5 | 27.5 | width (soft) | Music: Kazuhiko Kato |
| `eboot:387070` | 1 | 209 | 182 | 27 | width (soft) | 12.7mm Twin Beam Machine Gun |
| `eboot:389178` | 1 | 139 | 112 | 27 | width (soft) | Full Salvo (Transform) |
| `eboot:38AA20` | 1 | 251 | 224 | 27 | width (soft) | A variable trainer built for flight training |
| `eboot:3B6DBC` | 1 | 55 | 28 | 27 | width (soft) | Overlord |
| `eboot:3B6E7C` | 1 | 55 | 28 | 27 | width (soft) | Tactician |
| `eboot:3B6FE0` | 1 | 97 | 70 | 27 | width (soft) | Strongest Bride |
| `eboot:3B8314` | 1 | 181 | 154 | 27 | width (soft) | We will now cover your ship. |
| `eboot:3BB7F0` | 1 | 209 | 182 | 27 | width (soft) | Do You Remember Love? (Vocal) |
| `eboot:385D60` | 2 | 334 | 308 | 26 | width (soft) | Performs a melee attack with a pinpoint barrier punch |
| `eboot:387284` | 2 | 278 | 252 | 26 | width (soft) | Attacks with the Gun Cluster's flamethrower |
| `eboot:388A8C` | 2 | 222 | 196 | 26 | width (soft) | Captures the target with sticky glue |
| `eboot:389434` | 1 | 68 | 42 | 26 | width (soft) | Super Shot |
| `eboot:389B44` | 1 | 264 | 238 | 26 | width (soft) | Variable fighter that fixed the VF-1's flaws |
| `eboot:389C6C` | 1 | 306 | 280 | 26 | width (soft) | Battle pod developed from collected combat data |
| `eboot:3B6BAC` | 1 | 54 | 28 | 26 | width (soft) | Virtuoso |
| `eboot:3B6F24` | 1 | 96 | 70 | 26 | width (soft) | Skull Squadron |
| `eboot:3BBB60` | 1 | 194 | 168 | 26 | width (soft) | My Boyfriend is a Pilot (Vocal) |
| `eboot:385B64` | 1 | 53 | 28 | 25 | width (soft) | Bayonet |
| `eboot:3871E8` | 2 | 291 | 266 | 25 | width (soft) | Rockets fired in rapid succession at one enemy |
| `eboot:38A788` | 2 | 291 | 266 | 25 | width (soft) | Gigile's unit, with stronger weapons and thrust |
| `eboot:38B484` | 2 | 305 | 280 | 25 | width (soft) | Only for cyborg soldiers with mechanized bodies |
| `eboot:3B6B74` | 1 | 67 | 42 | 25 | width (soft) | In Training |
| `eboot:3B6DA4` | 1 | 81 | 56 | 25 | width (soft) | Army of One |
| `eboot:3B6F98` | 1 | 53 | 28 | 25 | width (soft) | Kakizaki |
| `eboot:3B7160` | 1 | 81 | 56 | 25 | width (soft) | Kabuki Actor |
| `eboot:3B7720` | 1 | 137 | 112 | 25 | width (soft) | That damn fledgling... |
| `eboot:3B788C` | 1 | 221 | 196 | 25 | width (soft) | Still playing the noble knight, huh? |
| `eboot:3B8AD4` | 2 | 81 | 56 | 25 | width (soft) | Listed Above |
| `eboot:3B8AFC` | 1 | 123 | 98 | 25 | width (soft) | Melee Attack Usage |
| `eboot:3B91E4` | 1 | 123 | 98 | 25 | width (soft) | Ranka (Hypnotized) |
| `eboot:3BD204` | 1 | 291 | 266 | 25 | width (soft) | Mission Continues (Do You Remember Love?) |
| `eboot:3BB80C` | 4 | 273 | 248.5 | 24.5 | width (soft) | Lyrics: Kazumi Yasui  Music: Kazuhiko Kato |
| `eboot:3BC9D4` | 4 | 273 | 248.5 | 24.5 | width (soft) | Lyrics: Kazumi Yasui  Music: Kazuhiko Kato |
| `eboot:3865D0` | 2 | 262 | 238 | 24 | width (soft) | Launches a wave attack with three Ghosts |
| `eboot:386958` | 2 | 206 | 182 | 24 | width (soft) | Launches a wave attack with bits |
| `eboot:387CD0` | 2 | 234 | 210 | 24 | width (soft) | Beam cannon mounted atop the head |
| `eboot:387E60` | 2 | 234 | 210 | 24 | width (soft) | Beam cannon mounted atop the head |
| `eboot:389830` | 2 | 262 | 238 | 24 | width (soft) | Milia's unit, with red as her personal color |
| `eboot:389BAC` | 2 | 304 | 280 | 24 | width (soft) | ARMD-01 and ARMD-02 are attached as its arms |
| `eboot:389DEC` | 2 | 262 | 238 | 24 | width (soft) | Milia's unit, with red as her personal color |
| `eboot:38A34C` | 2 | 262 | 238 | 24 | width (soft) | Milia's unit, with red as her personal color |
| `eboot:38A4F0` | 2 | 262 | 238 | 24 | width (soft) | Milia's unit, with red as her personal color |
| `eboot:38A560` | 2 | 318 | 294 | 24 | width (soft) | Basara's unit, with blazing red as his personal color |
| `eboot:38B390` | 2 | 192 | 168 | 24 | width (soft) | The latest Battle-class Macross |
| `eboot:38B568` | 2 | 192 | 168 | 24 | width (soft) | The latest Battle-class Macross |
| `eboot:38B8B0` | 2 | 262 | 238 | 24 | width (soft) | Milia's unit, with red as her personal color |
| `eboot:38ECFC` | 2 | 192 | 168 | 24 | width (soft) | puts up a barrier for a set time. |
| `eboot:38EED0` | 1 | 192 | 168 | 24 | width (soft) | When you rescue your partner, |
| `eboot:38EF1C` | 2 | 122 | 98 | 24 | width (soft) | 1.5x as many times. |
| `eboot:38F458` | 1 | 52 | 28 | 24 | width (soft) | Earplugs |
| `eboot:3B58CC` | 1 | 136 | 112 | 24 | width (soft) | Galaxy Whale (White) |
| `eboot:3B6B7C` | 1 | 66 | 42 | 24 | width (soft) | Greenhorn |
| `eboot:3B6D9C` | 1 | 52 | 28 | 24 | width (soft) | Emperor |
| `eboot:3B775C` | 1 | 122 | 98 | 24 | width (soft) | Versus Matches: 30 |
| `eboot:3B77B4` | 1 | 122 | 98 | 24 | width (soft) | Versus Matches: 40 |
| `eboot:3B784C` | 1 | 122 | 98 | 24 | width (soft) | Versus Matches: 60 |
| `eboot:3B7948` | 1 | 122 | 98 | 24 | width (soft) | Versus Matches: 90 |
| `eboot:386E3C` | 2 | 247 | 224 | 23 | width (soft) | Gatling cannons mounted on both arms |
| `eboot:38777C` | 2 | 303 | 280 | 23 | width (soft) | A burning passion for whales raises attack power |
| `eboot:389F40` | 2 | 303 | 280 | 23 | width (soft) | Steering it the way Quamzin orders is hard work |
| `eboot:38E7AC` | 1 | 205 | 182 | 23 | width (soft) | Guarding an enemy melee attack |
| `eboot:38EF70` | 1 | 261 | 238 | 23 | width (soft) | Damage to battleships and bases doubles. |
| `eboot:38EFAC` | 1 | 191 | 168 | 23 | width (soft) | Makes combos easier to chain. |
| `eboot:38F36C` | 1 | 191 | 168 | 23 | width (soft) | Boosts unit performance while |
| `eboot:3B12FC` | 1 | 177 | 154 | 23 | width (soft) | The connection was refused. |
| `eboot:3B6BA4` | 1 | 65 | 42 | 23 | width (soft) | Supernova |
| `eboot:3B72E4` | 1 | 65 | 42 | 23 | width (soft) | Apprentice |
| `eboot:3B7710` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 20 |
| `eboot:3B778C` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 35 |
| `eboot:3B77E0` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 45 |
| `eboot:3B77FC` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 50 |
| `eboot:3B787C` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 65 |
| `eboot:3B78F4` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 80 |
| `eboot:3B7974` | 1 | 121 | 98 | 23 | width (soft) | Versus Matches: 95 |
| `eboot:3B8398` | 1 | 219 | 196 | 23 | width (soft) | I'll make it ring to the galaxy's end! |
| `eboot:3B88F4` | 1 | 79 | 56 | 23 | width (soft) | Full Mastery |
| `eboot:3B8CD4` | 1 | 65 | 42 | 23 | width (soft) | Lone Wolf |
| `eboot:3B8FA8` | 1 | 121 | 98 | 23 | width (soft) | Kadun of the Curse |
| `eboot:3855D8` | 2 | 190 | 168 | 22 | width (soft) | Attacks with reaction weapons |
| `eboot:386CCC` | 1 | 134 | 112 | 22 | width (soft) | 12.7mm Machine Gun |
| `eboot:3871E8` | 1 | 302 | 280 | 22 | width (soft) | 12-Round Close-Range Homing Rocket Launcher |
| `eboot:387440` | 1 | 302 | 280 | 22 | width (soft) | 12-Round Close-Range Homing Rocket Launcher |
| `eboot:387AA4` | 2 | 190 | 168 | 22 | width (soft) | Attacks with reaction weapons |
| `eboot:389454` | 1 | 176 | 154 | 22 | width (soft) | Anti-air interceptor Destroid |
| `eboot:389808` | 1 | 78 | 56 | 22 | width (soft) | Hyper Speed |
| `eboot:38A9BC` | 2 | 274 | 252 | 22 | width (soft) | The largest and mightiest of the Protodeviln |
| `eboot:38B094` | 2 | 246 | 224 | 22 | width (soft) | Michel's unit, a long-range support type |
| `eboot:38B3EC` | 1 | 148 | 126 | 22 | width (soft) | Vajra, an alien life form |
| `eboot:38B43C` | 1 | 148 | 126 | 22 | width (soft) | Vajra, an alien life form |
| `eboot:3B6EF4` | 1 | 106 | 84 | 22 | width (soft) | Battroid Diehard |
| `eboot:3B76B8` | 1 | 120 | 98 | 22 | width (soft) | Versus Matches: 10 |
| `eboot:3B7734` | 1 | 120 | 98 | 22 | width (soft) | Versus Matches: 25 |
| `eboot:3B782C` | 1 | 120 | 98 | 22 | width (soft) | Versus Matches: 55 |
| `eboot:3B78AC` | 1 | 120 | 98 | 22 | width (soft) | Versus Matches: 70 |
| `eboot:3B7918` | 1 | 120 | 98 | 22 | width (soft) | Versus Matches: 85 |
| `eboot:3B87E0` | 1 | 78 | 56 | 22 | width (soft) | Sitting Duck |
| `eboot:3BC900` | 1 | 92 | 70 | 22 | width (soft) | Bowels of War |
| `eboot:3BC90C` | 1 | 92 | 70 | 22 | width (soft) | Bowels of War |
| `eboot:3BD22C` | 1 | 106 | 84 | 22 | width (soft) | Nyan-Nyan Shop |
| `eboot:3BD23C` | 1 | 106 | 84 | 22 | width (soft) | Nyan-Nyan Shop |
| `eboot:3BD6F8` | 1 | 344 | 322 | 22 | width (soft) | Totsugeki Love Heart (Storm Valkyrie: Song Weapon 1) |
| `eboot:38EC40` | 1 | 161 | 140 | 21 | width (soft) | Do You Remember Love? |
| `eboot:3B9080` | 1 | 161 | 140 | 21 | width (soft) | Do You Remember Love? |
| `eboot:3BB884` | 1 | 161 | 140 | 21 | width (soft) | Do You Remember Love? |
| `eboot:38584C` | 2 | 217 | 196 | 21 | width (soft) | Beam cannon mounted on the arm |
| `eboot:385C24` | 2 | 217 | 196 | 21 | width (soft) | Beam cannon mounted on the arm |
| `eboot:3887E8` | 1 | 203 | 182 | 21 | width (soft) | Spiritia Absorption Beam (Large) |
| `eboot:388824` | 1 | 203 | 182 | 21 | width (soft) | Spiritia Absorption Beam (Multi) |
| `eboot:388C58` | 2 | 147 | 126 | 21 | width (soft) | Calls in Gigamesh units |
| `eboot:388D50` | 1 | 119 | 98 | 21 | width (soft) | 30mm Autocannon |
| `eboot:388F00` | 2 | 231 | 210 | 21 | width (soft) | Moves faster than the eye can follow |
| `eboot:3899A0` | 2 | 287 | 266 | 21 | width (soft) | Equipped with a FAST Pack made for the VT-1 |
| `eboot:392B6C` | 1 | 189 | 168 | 21 | width (soft) | Force-purged when add-on HP |
| `eboot:3B76EC` | 1 | 119 | 98 | 21 | width (soft) | Versus Matches: 15 |
| `eboot:3B78C8` | 1 | 119 | 98 | 21 | width (soft) | Versus Matches: 75 |
| `eboot:3BB80C` | 1 | 161 | 140 | 21 | width (soft) | Do You Remember Love? |
| `eboot:3BB89C` | 1 | 161 | 140 | 21 | width (soft) | Do You Remember Love? |
| `eboot:386200` | 1 | 188 | 168 | 20 | width (soft) | Drums (Totsugeki Love Heart) |
| `eboot:38654C` | 1 | 160 | 140 | 20 | width (soft) | Large Anti-Carrier Missile |
| `eboot:386730` | 1 | 174 | 154 | 20 | width (soft) | 12.7mm Beam Machine Gun |
| `eboot:3869D4` | 1 | 132 | 112 | 20 | width (soft) | Rotary Laser Cannon |
| `eboot:387118` | 1 | 104 | 84 | 20 | width (soft) | Missile Jamming |
| `eboot:387238` | 2 | 272 | 252 | 20 | width (soft) | Attacks with the Gun Cluster's laser cannon |
| `eboot:387684` | 1 | 258 | 238 | 20 | width (soft) | Large Homing Anti-Ship Missile Launcher |
| `eboot:387D14` | 1 | 230 | 210 | 20 | width (soft) | Close-Combat Small Homing Missile |
| `eboot:389728` | 1 | 76 | 56 | 20 | width (soft) | Triple Clone |
| `eboot:38B150` | 1 | 286 | 266 | 20 | width (soft) | Battle suit upgraded from the Queadluun-Rau |
| `eboot:38B1B4` | 1 | 286 | 266 | 20 | width (soft) | Battle suit upgraded from the Queadluun-Rau |
| `eboot:38B6FC` | 2 | 286 | 266 | 20 | width (soft) | Barnrose's unit, with red as her personal color |
| `eboot:38EDA8` | 1 | 286 | 266 | 20 | width (soft) | Stops everything but you and triggers an SPA. |
| `eboot:3B57C8` | 1 | 76 | 56 | 20 | width (soft) | Gigile's Ship |
| `eboot:3B5BB8` | 1 | 132 | 112 | 20 | width (soft) | Micronization Device |
| `eboot:3B78D8` | 1 | 188 | 168 | 20 | width (soft) | Heh, sorry. It was an accident. |
| `eboot:3B900C` | 1 | 174 | 154 | 20 | width (soft) | Minmay (Love Drifts Away) |
| `eboot:3BBB7C` | 1 | 146 | 126 | 20 | width (soft) | My Boyfriend is a Pilot |
| `eboot:3BBBDC` | 1 | 146 | 126 | 20 | width (soft) | My Boyfriend is a Pilot |
| `eboot:3BBBF0` | 1 | 146 | 126 | 20 | width (soft) | My Boyfriend is a Pilot |
| `eboot:386274` | 2 | 271 | 252 | 19 | width (soft) | Gun pod that fires whale-catching harpoons |
| `eboot:387118` | 2 | 145 | 126 | 19 | width (soft) | Jams incoming missiles |
| `eboot:3885AC` | 2 | 243 | 224 | 19 | width (soft) | Laser guns mounted on both shoulders |
| `eboot:38AFC4` | 1 | 285 | 266 | 19 | width (soft) | Latest-model variable fighter issued to S.M.S. |
| `eboot:38B028` | 1 | 285 | 266 | 19 | width (soft) | Latest-model variable fighter issued to S.M.S. |
| `eboot:38B094` | 1 | 285 | 266 | 19 | width (soft) | Latest-model variable fighter issued to S.M.S. |
| `eboot:38B0F8` | 1 | 285 | 266 | 19 | width (soft) | Latest-model variable fighter issued to S.M.S. |
| `eboot:38B218` | 2 | 257 | 238 | 19 | width (soft) | A maiden who fights clad in a Super Pack |
| `eboot:3B4A18` | 1 | 103 | 84 | 19 | width (soft) | Anti-U.N. Forces |
| `eboot:38F294` | 1 | 243 | 224 | 19 | width (soft) | Your attacks ignore all types of barrier. |
| `eboot:3B6E84` | 1 | 75 | 56 | 19 | width (soft) | True Master |
| `eboot:3B7FAC` | 1 | 215 | 196 | 19 | width (soft) | Oh my, you don't want me along? |
| `eboot:3B8798` | 1 | 89 | 70 | 19 | width (soft) | Weak Finisher |
| `eboot:3B88AC` | 1 | 75 | 56 | 19 | width (soft) | One-Hit Kill |
| `eboot:3B8F40` | 1 | 75 | 56 | 19 | width (soft) | White Larva |
| `eboot:3B940C` | 1 | 117 | 98 | 19 | width (soft) | Admired Big Sister |
| `eboot:3BB80C` | 3 | 117 | 98 | 19 | width (soft) | Vocals: Mari Iijima |
| `eboot:3BBA48` | 3 | 145 | 126 | 19 | width (soft) | Music: Kentaro Haneda |
| `eboot:3BBAA8` | 3 | 145 | 126 | 19 | width (soft) | Music: Kentaro Haneda |
| `eboot:3BBB14` | 3 | 145 | 126 | 19 | width (soft) | Music: Kentaro Haneda |
| `eboot:3BBB7C` | 3 | 117 | 98 | 19 | width (soft) | Vocals: Mari Iijima |
| `eboot:3BBBF0` | 3 | 145 | 126 | 19 | width (soft) | Music: Kentaro Haneda |
| `eboot:3BC9D4` | 3 | 117 | 98 | 19 | width (soft) | Vocals: Mari Iijima |
| `eboot:386274` | 1 | 172 | 154 | 18 | width (soft) | Harpoon Launcher Gun Pod |
| `eboot:388778` | 2 | 172 | 154 | 18 | width (soft) | A beam fired from the head |
| `eboot:3888A4` | 1 | 116 | 98 | 18 | width (soft) | Spiritia Absorption |
| `eboot:389378` | 1 | 116 | 98 | 18 | width (soft) | Melee + Full Salvo |
| `eboot:38965C` | 1 | 88 | 70 | 18 | width (soft) | Melee Combo |
| `eboot:38991C` | 2 | 340 | 322 | 18 | width (soft) | The Daedalus and Prometheus are attached as its arms |
| `eboot:38A804` | 2 | 298 | 280 | 18 | width (soft) | Developed as the Varauta Army's new mainstay |
| `eboot:392A68` | 1 | 186 | 168 | 18 | width (soft) | The player and partner cannot |
| `eboot:3B7228` | 1 | 116 | 98 | 18 | width (soft) | Handsome Cyborg |
| `eboot:3B7328` | 1 | 60 | 42 | 18 | width (soft) | Old Hand |
| `eboot:3B7E78` | 1 | 130 | 112 | 18 | width (soft) | Versus Matches: 300 |
| `eboot:3B8710` | 1 | 130 | 112 | 18 | width (soft) | Ah... it's connected... |
| `eboot:3B8FB8` | 1 | 116 | 98 | 18 | width (soft) | Sara (Bird Human) |
| `eboot:3858DC` | 1 | 353 | 336 | 17 | width (soft) | Semi-Conformal Medium-Range Guided Missiles (Rapid) |
| `eboot:386BA0` | 1 | 213 | 196 | 17 | width (soft) | Medium Anti-Ship Missiles (Blast) |
| `eboot:386D58` | 1 | 213 | 196 | 17 | width (soft) | Medium Anti-Ship Missiles (Blast) |
| `eboot:386F2C` | 1 | 199 | 182 | 17 | width (soft) | 40cm Liquid-Propellant Cannon |
| `eboot:387594` | 1 | 87 | 70 | 17 | width (soft) | Power Charge |
| `eboot:387B70` | 1 | 101 | 84 | 17 | width (soft) | Ghost Kamikaze |
| `eboot:3885F0` | 1 | 87 | 70 | 17 | width (soft) | Flamethrower |
| `eboot:38BD38` | 1 | 73 | 56 | 17 | width (soft) | Unavailable |
| `eboot:392B1C` | 3 | 171 | 154 | 17 | width (soft) | when add-on HP drops to 0 |
| `eboot:3B719C` | 1 | 87 | 70 | 17 | width (soft) | Young Master |
| `eboot:3B74BC` | 1 | 87 | 70 | 17 | width (soft) | Chicken Punk |
| `eboot:3B7C94` | 1 | 129 | 112 | 17 | width (soft) | Versus Matches: 200 |
| `eboot:3B7D2C` | 1 | 129 | 112 | 17 | width (soft) | Versus Matches: 230 |
| `eboot:3B7D64` | 1 | 129 | 112 | 17 | width (soft) | Versus Matches: 240 |
| `eboot:3B7DC0` | 1 | 129 | 112 | 17 | width (soft) | Versus Matches: 260 |
| `eboot:3B7E50` | 1 | 129 | 112 | 17 | width (soft) | Versus Matches: 290 |
| `eboot:3B8FD0` | 1 | 143 | 126 | 17 | width (soft) | The First Miss Macross |
| `eboot:386C70` | 1 | 254 | 238 | 16 | width (soft) | Medium Anti-Ship Missiles (Rapid/Blast) |
| `eboot:387C28` | 2 | 198 | 182 | 16 | width (soft) | Fires lasers from its entire body |
| `eboot:388E04` | 1 | 86 | 70 | 16 | width (soft) | Laser Cannon |
| `eboot:38EF60` | 1 | 100 | 84 | 16 | width (soft) | Sabotage Squad |
| `eboot:38F1E8` | 1 | 268 | 252 | 16 | width (soft) | When your HP drops to 30% or less, the SP |
| `eboot:3B5558` | 1 | 128 | 112 | 16 | width (soft) | ARMD Space Carrier |
| `eboot:3B5728` | 1 | 72 | 56 | 16 | width (soft) | Milia's Ship |
| `eboot:3B58A8` | 1 | 86 | 70 | 16 | width (soft) | Galaxy Whale |
| `eboot:3B6B84` | 1 | 44 | 28 | 16 | width (soft) | Recruit |
| `eboot:3B799C` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 100 |
| `eboot:3B7AB8` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 130 |
| `eboot:3B7B1C` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 140 |
| `eboot:3B7BB8` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 160 |
| `eboot:3B7C5C` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 190 |
| `eboot:3B7CF4` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 220 |
| `eboot:3B7D9C` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 250 |
| `eboot:3B7E20` | 1 | 128 | 112 | 16 | width (soft) | Versus Matches: 280 |
| `eboot:3B8558` | 1 | 198 | 182 | 16 | width (soft) | Papa is not cheating on anyone. |
| `eboot:3B8BA0` | 1 | 100 | 84 | 16 | width (soft) | GERWALK Love |
| `eboot:3BC118` | 3 | 128 | 112 | 16 | width (soft) | Music: Miki Kawano |
| `eboot:392934` | 1 | 71 | 56 | 15 | width (soft) | Auto Select |
| `eboot:3B1370` | 1 | 71 | 56 | 15 | width (soft) | Auto Select |
| `eboot:385118` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:3851D4` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:385710` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:385EA0` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:3864F4` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:386C70` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:3873A4` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:388054` | 2 | 183 | 168 | 15 | width (soft) | Calls in Nousjadeul-Ger units |
| `eboot:388124` | 2 | 295 | 280 | 15 | width (soft) | Rapid fire. Missiles that cause a blast on impact |
| `eboot:38A9BC` | 1 | 309 | 294 | 15 | width (soft) | Varauta Army commander and Protodeviln leader |
| `eboot:38B69C` | 2 | 253 | 238 | 15 | width (soft) | Feff's unit, with red as his personal color |
| `eboot:38EAA0` | 1 | 85 | 70 | 15 | width (soft) | Galactic Fairy |
| `eboot:3B6E10` | 1 | 85 | 70 | 15 | width (soft) | Galactic Fairy |
| `eboot:3B4DD4` | 1 | 71 | 56 | 15 | width (soft) | Planet Zola |
| `eboot:3B59E0` | 1 | 85 | 70 | 15 | width (soft) | Vajra Cocoon |
| `eboot:3B6F68` | 1 | 43 | 28 | 15 | width (soft) | Genius |
| `eboot:3B785C` | 1 | 225 | 210 | 15 | width (soft) | I don't wanna hear your weird song. |
| `eboot:3B79CC` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 105 |
| `eboot:3B7A5C` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 120 |
| `eboot:3B7AF4` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 135 |
| `eboot:3B7B54` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 145 |
| `eboot:3B7B88` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 150 |
| `eboot:3B7C28` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 180 |
| `eboot:3B7CCC` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 210 |
| `eboot:3B7DF8` | 1 | 127 | 112 | 15 | width (soft) | Versus Matches: 270 |
| `eboot:35A480` | 2 | 224 | 210 | 14 | width (soft) | Do not remove the Memory Stick⑳ |
| `eboot:35A4D0` | 2 | 224 | 210 | 14 | width (soft) | Do not remove the Memory Stick⑳ |
| `eboot:35A538` | 2 | 224 | 210 | 14 | width (soft) | Do not remove the Memory Stick⑳ |
| `eboot:35F488` | 1 | 42 | 28 | 14 | width (soft) | Kinryu |
| `eboot:387E20` | 1 | 182 | 168 | 14 | width (soft) | Large-Caliber Impact Cannon |
| `eboot:389878` | 1 | 112 | 98 | 14 | width (soft) | Double Full Salvo |
| `eboot:38EA48` | 2 | 266 | 252 | 14 | width (soft) | you, and revives any that were shot down. |
| `eboot:395B74` | 2 | 238 | 224 | 14 | width (soft) | Press the × button to abort the battle |
| `eboot:3B1144` | 1 | 42 | 28 | 14 | width (soft) | Versus |
| `eboot:3B4AC0` | 1 | 210 | 196 | 14 | width (soft) | Lynn Minmay (Love Drifts Away) |
| `eboot:3B6B4C` | 1 | 56 | 42 | 14 | width (soft) | Beginner |
| `eboot:3B6F14` | 1 | 98 | 84 | 14 | width (soft) | Fighter Diehard |
| `eboot:3B76FC` | 1 | 126 | 112 | 14 | width (soft) | Heh, the boy again? |
| `eboot:3B79FC` | 1 | 126 | 112 | 14 | width (soft) | Versus Matches: 110 |
| `eboot:3B7A80` | 1 | 126 | 112 | 14 | width (soft) | Versus Matches: 125 |
| `eboot:3B7BF0` | 1 | 126 | 112 | 14 | width (soft) | Versus Matches: 170 |
| `eboot:3613C8` | 1 | 139 | 126 | 13 | width (soft) | Grunt: Shot 0 Melee 0 |
| `eboot:3633A8` | 1 | 97 | 84 | 13 | width (soft) | Veteran Soldier |
| `eboot:387638` | 2 | 265 | 252 | 13 | width (soft) | Laser cannons mounted on both shoulders |
| `eboot:387C58` | 1 | 167 | 154 | 13 | width (soft) | Scatter Laser Machine Gun |
| `eboot:388984` | 1 | 83 | 70 | 13 | width (soft) | Machine Gun |
| `eboot:388A68` | 1 | 69 | 56 | 13 | width (soft) | Body Slam |
| `eboot:38AD34` | 2 | 307 | 294 | 13 | width (soft) | Diving-suited, he fights whales with one harpoon |
| `eboot:38B764` | 2 | 279 | 266 | 13 | width (soft) | Twitchy custom for the Ravens special forces |
| `eboot:38B844` | 1 | 307 | 294 | 13 | width (soft) | Variable fighter issued to the Dancing Skull team |
| `eboot:38B8B0` | 1 | 307 | 294 | 13 | width (soft) | Variable fighter issued to the Dancing Skull team |
| `eboot:38E8F0` | 2 | 167 | 154 | 13 | width (soft) | melee attack power triples. |
| `eboot:38F0F8` | 2 | 265 | 252 | 13 | width (soft) | awaken, invincible for a while. *Once only |
| `eboot:3B6F44` | 1 | 97 | 84 | 13 | width (soft) | Pineapple Salad |
| `eboot:3B7370` | 1 | 125 | 112 | 13 | width (soft) | Completionist KING |
| `eboot:3B7A30` | 1 | 125 | 112 | 13 | width (soft) | Versus Matches: 115 |
| `eboot:3B931C` | 1 | 69 | 56 | 13 | width (soft) | Tough Guy |
| `eboot:3BAF20` | 1 | 195 | 182 | 13 | width (soft) | Not enough Nyan-Nyan Points. |
| `eboot:35E088` | 1 | 79 | 66.5 | 12.5 | width (soft) | Misa Hayase |
| `eboot:3B7258` | 1 | 79 | 66.5 | 12.5 | width (soft) | Misa Hayase |
| `eboot:385A44` | 2 | 334 | 322 | 12 | width (soft) | Multi-lock. Missiles that cause a huge blast on impact |
| `eboot:386AF0` | 1 | 82 | 70 | 12 | width (soft) | Balloon Shot |
| `eboot:38844C` | 1 | 96 | 84 | 12 | width (soft) | Tentacle Attack |
| `eboot:388E9C` | 2 | 334 | 322 | 12 | width (soft) | Multi-lock. Missiles that cause a huge blast on impact |
| `eboot:389454` | 2 | 250 | 238 | 12 | width (soft) | Used as the Macross's anti-air weaponry |
| `eboot:3B5424` | 1 | 110 | 98 | 12 | width (soft) | Missile Destroyer |
| `eboot:3B6E04` | 1 | 82 | 70 | 12 | width (soft) | Galactic Diva |
| `eboot:3B7928` | 1 | 222 | 210 | 12 | width (soft) | A toast to our reunion after 7 years! |
| `eboot:3B8170` | 1 | 166 | 154 | 12 | width (soft) | Was I a genius all along...? |
| `eboot:3B8738` | 1 | 152 | 140 | 12 | width (soft) | Those goddamn bugs...!! |
| `eboot:3B8958` | 2 | 96 | 84 | 12 | width (soft) | Over 1,000,000 |
| `eboot:3B8C00` | 1 | 152 | 140 | 12 | width (soft) | Nyan-Nyan Shop Owner |
| `eboot:3634E8` | 1 | 81 | 70 | 11 | width (soft) | Melee Expert |
| `eboot:3857C0` | 1 | 263 | 252 | 11 | width (soft) | Ultra-High-Mobility Micro Missiles (Blast) |
| `eboot:38F02C` | 1 | 95 | 84 | 11 | width (soft) | Pineapple Cake |
| `eboot:3B71B8` | 1 | 95 | 84 | 11 | width (soft) | Pineapple Cake |
| `eboot:3B6D18` | 1 | 95 | 84 | 11 | width (soft) | To the Endth☆ |
| `eboot:3B886C` | 1 | 53 | 42 | 11 | width (soft) | Gambler |
| `eboot:3B8FE4` | 1 | 123 | 112 | 11 | width (soft) | Minmay (Swimsuit) |
| `eboot:360888` | 1 | 91 | 80.5 | 10.5 | width (soft) | Hibiki Kanzaki |
| `eboot:385324` | 1 | 38 | 28 | 10 | width (soft) | Melee |
| `eboot:385710` | 1 | 304 | 294 | 10 | width (soft) | Ultra-High-Mobility Micro Missiles (Rapid/Blast) |
| `eboot:386D1C` | 2 | 178 | 168 | 10 | width (soft) | Attacks with a fuel-air bomb |
| `eboot:388098` | 1 | 276 | 266 | 10 | width (soft) | High-Speed Rotary 3-Barrel Laser Pulse Gun |
| `eboot:3884F0` | 1 | 38 | 28 | 10 | width (soft) | Melee |
| `eboot:3896DC` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:3897BC` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:389AEC` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:389E5C` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:38A47C` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:38B844` | 2 | 262 | 252 | 10 | width (soft) | Max's unit, with blue as his personal color |
| `eboot:38EC04` | 2 | 136 | 126 | 10 | width (soft) | but defense is halved. |
| `eboot:3B114C` | 1 | 38 | 28 | 10 | width (soft) | Co-op |
| `eboot:3B5534` | 1 | 94 | 84 | 10 | width (soft) | Liaison Shuttle |
| `eboot:3B5638` | 1 | 80 | 70 | 10 | width (soft) | Quel-Quallie |
| `eboot:3B57A8` | 1 | 80 | 70 | 10 | width (soft) | Varauta Ship |
| `eboot:3B6C5C` | 1 | 108 | 98 | 10 | width (soft) | Destroid Diehard |
| `eboot:3B726C` | 1 | 66 | 56 | 10 | width (soft) | Greenhorn |
| `eboot:3B8948` | 1 | 94 | 84 | 10 | width (soft) | Missile Heaven |
| `eboot:3B90E8` | 1 | 122 | 112 | 10 | width (soft) | School Festival Idol |
| `eboot:3BAF04` | 1 | 178 | 168 | 10 | width (soft) | Leave the Nyan-Nyan Shop? |
| `eboot:3BC040` | 3 | 122 | 112 | 10 | width (soft) | Music: Hideki Sudo |
| `eboot:38633C` | 1 | 51 | 42 | 9 | width (soft) | Song SP |
| `eboot:3872EC` | 2 | 135 | 126 | 9 | width (soft) | Calls in Phalanx units |
| `eboot:388480` | 1 | 135 | 126 | 9 | width (soft) | Multi-Tentacle Attack |
| `eboot:388D18` | 1 | 107 | 98 | 9 | width (soft) | Air-to-Air Missile |
| `eboot:38B304` | 1 | 275 | 266 | 9 | width (soft) | Variable attack space carrier, S.M.S. flagship |
| `eboot:38B304` | 2 | 303 | 294 | 9 | width (soft) | Only 400 m class, yet it bears the Macross name |
| `eboot:38BD0C` | 1 | 107 | 98 | 9 | width (soft) | Vajra Sub-Queen |
| `eboot:3B5A70` | 1 | 107 | 98 | 9 | width (soft) | Vajra Sub-Queen |
| `eboot:38EFD4` | 1 | 37 | 28 | 9 | width (soft) | Cheer |
| `eboot:392B1C` | 2 | 191 | 182 | 9 | width (soft) | and performance are kept even |
| `eboot:3B1820` | 1 | 177 | 168 | 9 | width (soft) | The mission will be aborted. |
| `eboot:3B4EFC` | 1 | 149 | 140 | 9 | width (soft) | Ranka Lee (Hypnotized) |
| `eboot:3B783C` | 1 | 107 | 98 | 9 | width (soft) | Thrilling, isn't it? |
| `eboot:3B7F10` | 1 | 93 | 84 | 9 | width (soft) | Versus Wins: 3 |
| `eboot:3B85F4` | 1 | 219 | 210 | 9 | width (soft) | I'll wreck you! Suppression Beauty! |
| `eboot:3B8AFC` | 2 | 79 | 70 | 9 | width (soft) | 65% or More |
| `eboot:3B8B28` | 2 | 79 | 70 | 9 | width (soft) | 65% or More |
| `eboot:3B8B58` | 2 | 79 | 70 | 9 | width (soft) | 65% or More |
| `eboot:3B8D50` | 1 | 51 | 42 | 9 | width (soft) | Faceless |
| `eboot:3B8E94` | 1 | 121 | 112 | 9 | width (soft) | Wandering Vocalist |
| `eboot:3B9250` | 1 | 121 | 112 | 9 | width (soft) | Sagittarius ☆ 9 PM |
| `eboot:35E8A8` | 1 | 78 | 70 | 8 | width (soft) | Boddole Zer |
| `eboot:385BE8` | 2 | 218 | 210 | 8 | width (soft) | Laser cannon mounted in the chest |
| `eboot:386F00` | 2 | 120 | 112 | 8 | width (soft) | Calls in Cheyennes |
| `eboot:389D88` | 1 | 274 | 266 | 8 | width (soft) | Battle suit developed by the Zentradi forces |
| `eboot:389DEC` | 1 | 274 | 266 | 8 | width (soft) | Battle suit developed by the Zentradi forces |
| `eboot:389E5C` | 1 | 274 | 266 | 8 | width (soft) | Battle suit developed by the Zentradi forces |
| `eboot:38A3A8` | 1 | 246 | 238 | 8 | width (soft) | Variable fighter evolved from the VF-11 |
| `eboot:38A3A8` | 2 | 260 | 252 | 8 | width (soft) | Flown mainly by Emerald Force members |
| `eboot:38A408` | 1 | 246 | 238 | 8 | width (soft) | Variable fighter evolved from the VF-11 |
| `eboot:38A8DC` | 1 | 274 | 266 | 8 | width (soft) | Battle suit developed by the Zentradi forces |
| `eboot:38ABDC` | 1 | 246 | 238 | 8 | width (soft) | Variable fighter evolved from the VF-11 |
| `eboot:38B764` | 1 | 246 | 238 | 8 | width (soft) | Variable fighter evolved from the VF-11 |
| `eboot:38F480` | 1 | 36 | 28 | 8 | width (soft) | Taunt |
| `eboot:3B5768` | 1 | 50 | 42 | 8 | width (soft) | Bomber |
| `eboot:3B72A0` | 2 | 120 | 112 | 8 | width (soft) | save data carryover |
| `eboot:3B7ED8` | 1 | 92 | 84 | 8 | width (soft) | Versus Wins: 2 |
| `eboot:3B7F44` | 1 | 92 | 84 | 8 | width (soft) | Versus Wins: 5 |
| `eboot:3B8B80` | 2 | 120 | 112 | 8 | width (soft) | Usage 65% or More |
| `eboot:3B8BB0` | 1 | 106 | 98 | 8 | width (soft) | GERWALK Mode |
| `eboot:3B8BB0` | 2 | 120 | 112 | 8 | width (soft) | Usage 65% or More |
| `eboot:3B8BE0` | 2 | 120 | 112 | 8 | width (soft) | Usage 65% or More |
| `eboot:3B8D34` | 1 | 36 | 28 | 8 | width (soft) | Daisy |
| `eboot:3B9760` | 2 | 162 | 154 | 8 | width (soft) | Units from the cleared era |
| `eboot:387998` | 1 | 119 | 112 | 7 | width (soft) | Feelings for Michel |
| `eboot:38EBB4` | 2 | 133 | 126 | 7 | width (soft) | gradually recover HP. |
| `eboot:3B5ABC` | 1 | 77 | 70 | 7 | width (soft) | Giant Ranka |
| `eboot:3B7EA4` | 1 | 91 | 84 | 7 | width (soft) | Versus Wins: 1 |
| `eboot:3B7F74` | 1 | 91 | 84 | 7 | width (soft) | Versus Wins: 7 |
| `eboot:3B8A5C` | 2 | 91 | 84 | 7 | width (soft) | All S or Higher |
| `eboot:3B91E4` | 2 | 161 | 154 | 7 | width (soft) | Clear Enemy "Koi no Uta" |
| `eboot:3BC9D4` | 1 | 371 | 364 | 7 | width (soft) | Do You Remember Love? (Skill: Do You Remember Love?) |
| `eboot:388FD4` | 1 | 62 | 56 | 6 | width (soft) | Full Salvo |
| `eboot:3891AC` | 1 | 216 | 210 | 6 | width (soft) | Prototype Destroid of the Monster |
| `eboot:38E740` | 2 | 272 | 266 | 6 | width (soft) | ○ button: On/Off  □ button: Change color |
| `eboot:3937A0` | 1 | 174 | 168 | 6 | width (soft) | Clear the wallpaper setting? |
| `eboot:395B74` | 1 | 146 | 140 | 6 | width (soft) | Waiting for connection. |
| `eboot:3B1114` | 1 | 76 | 70 | 6 | width (soft) | Force Battle |
| `eboot:3B5B70` | 1 | 62 | 56 | 6 | width (soft) | Container |
| `eboot:3B6BC4` | 1 | 90 | 84 | 6 | width (soft) | Galactic Guide |
| `eboot:3B6FA8` | 1 | 62 | 56 | 6 | width (soft) | Ally Killer |
| `eboot:3B71F8` | 1 | 90 | 84 | 6 | width (soft) | Clumsy Genes |
| `eboot:3B7F54` | 1 | 202 | 196 | 6 | width (soft) | The Vajra sing with their bellies! |
| `eboot:3B81C4` | 1 | 160 | 154 | 6 | width (soft) | I-I'm still alive, somehow. |
| `eboot:3B8A1C` | 1 | 118 | 112 | 6 | width (soft) | All Pilots Obtained |
| `eboot:3B9398` | 1 | 62 | 56 | 6 | width (soft) | Peppy Kid |
| `eboot:3BB258` | 1 | 146 | 140 | 6 | width (soft) | Waiting for connection. |
| `eboot:38A984` | 1 | 131 | 126 | 5 | width (soft) | Super Pentacle Beam |
| `eboot:38AEE0` | 2 | 299 | 294 | 5 | width (soft) | Flown by Alto as leader of Sagittarius Squadron |
| `eboot:38B28C` | 1 | 285 | 280 | 5 | width (soft) | Variable bomber developed from the Monster |
| `eboot:38E97C` | 1 | 229 | 224 | 5 | width (soft) | Reloads all weapons, shortens attack |
| `eboot:38F528` | 1 | 61 | 56 | 5 | width (soft) | Full Spirit |
| `eboot:3B4A8C` | 1 | 159 | 154 | 5 | width (soft) | Lynn Minmay (Swimsuit) |
| `eboot:3B6FEC` | 1 | 117 | 112 | 5 | width (soft) | Milia (U.N. Forces) |
| `eboot:3B79B0` | 1 | 173 | 168 | 5 | width (soft) | That one wants to fight me. |
| `eboot:3B8F64` | 1 | 89 | 84 | 5 | width (soft) | Red Rampager |
| `eboot:3BD274` | 1 | 257 | 252 | 5 | width (soft) | Mission Continues (Macross Dynamite 7) |
| `eboot:387180` | 2 | 144 | 140 | 4 | width (soft) | Calls in Defender units |
| `eboot:388A8C` | 1 | 60 | 56 | 4 | width (soft) | Glue Trap |
| `eboot:3895C4` | 2 | 256 | 252 | 4 | width (soft) | Poor mobility, but tremendous firepower |
| `eboot:389750` | 2 | 256 | 252 | 4 | width (soft) | Hikaru's unit, the hero mecha of Macross |
| `eboot:38ED48` | 2 | 130 | 126 | 4 | width (soft) | of every enemy unit. |
| `eboot:3B5784` | 1 | 88 | 84 | 4 | width (soft) | Laser Satellite |
| `eboot:3B57E8` | 1 | 186 | 182 | 4 | width (soft) | Varauta Fleet Flagship Carrier |
| `eboot:3B6DB0` | 1 | 60 | 56 | 4 | width (soft) | Unrivaled |
| `eboot:3B8A30` | 1 | 102 | 98 | 4 | width (soft) | Mecha Collector |
| `eboot:3B8B44` | 1 | 130 | 126 | 4 | width (soft) | Vocalist Declaration! |
| `eboot:3BAEF8` | 1 | 18 | 14 | 4 | width (soft) | NP |
| `eboot:3BC2F8` | 1 | 186 | 182 | 4 | width (soft) | Lion  Series: Macross Frontier |
| `eboot:388258` | 2 | 213 | 210 | 3 | width (soft) | Captures the target with a net gun |
| `eboot:38F36C` | 2 | 129 | 126 | 3 | width (soft) | you pilot a Destroid. |
| `eboot:392924` | 1 | 87 | 84 | 3 | width (soft) | Revert Tuning |
| `eboot:3B49F0` | 1 | 157 | 154 | 3 | width (soft) | Sara Nome (Bird Human) |
| `eboot:3B5050` | 1 | 101 | 98 | 3 | width (soft) | Mardook Forces |
| `eboot:3B6F30` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6F54` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6F70` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6F98` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6FB4` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6FD0` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B6FEC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7018` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B702C` | 1 | 59 | 56 | 3 | width (soft) | Hellraiser |
| `eboot:3B7038` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7054` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7078` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B709C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B70C8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B70E8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B710C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7134` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7150` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B716C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7188` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B71A8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B71C8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B71E8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7208` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7238` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B7258` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B812C` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 34 |
| `eboot:3B8188` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 40 |
| `eboot:3B81B4` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 43 |
| `eboot:3B81DC` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 46 |
| `eboot:3B8208` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 49 |
| `eboot:3B82B4` | 1 | 199 | 196 | 3 | width (soft) | As a warrior, learn some shame. |
| `eboot:3B8304` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 64 |
| `eboot:3B84EC` | 1 | 101 | 98 | 3 | width (soft) | Versus Wins: 94 |
| `eboot:3B8CDC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8CF4` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8D24` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8D3C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8D58` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8D80` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8DAC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8DE0` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8E04` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8E20` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8E48` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8E7C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8EA8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8ED8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8F04` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8F2C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8F4C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8F74` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8F98` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8FB8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B8FE4` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B900C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B903C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9060` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9098` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B90C8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B90FC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9120` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9144` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9168` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9190` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B91BC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9230` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9264` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9290` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B92B8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B92D8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B92FC` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9328` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9354` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9378` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B93A4` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B93C8` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B93F4` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B941C` | 2 | 59 | 56 | 3 | width (soft) | Unlocked |
| `eboot:3B9760` | 1 | 101 | 98 | 3 | width (soft) | Era Clear Bonus |
| `eboot:3BB74C` | 1 | 213 | 210 | 3 | width (soft) | Mylene Valkyrie (Song Weapon 2) |
| `eboot:3BC42C` | 4 | 122 | 119 | 3 | width (soft) | Music: Yoko Kanno |
| `eboot:3BCE7C` | 1 | 143 | 140 | 3 | width (soft) | Northern Cross (Vocal) |
| `eboot:35EDA8` | 1 | 83 | 80.5 | 2.5 | width (soft) | Basara Nekki |
| `eboot:35F7A8` | 1 | 83 | 80.5 | 2.5 | width (soft) | Basara Nekki |
| `eboot:35F848` | 1 | 83 | 80.5 | 2.5 | width (soft) | Basara Nekki |
| `eboot:360C48` | 1 | 114 | 112 | 2 | width (soft) | Miyuki Shirakawa |
| `eboot:361148` | 1 | 114 | 112 | 2 | width (soft) | Miyuki Shirakawa |
| `eboot:3B50E0` | 1 | 114 | 112 | 2 | width (soft) | Miyuki Shirakawa |
| `eboot:385638` | 1 | 254 | 252 | 2 | width (soft) | Quad Laser Cannon/Twin Beam Cannon |
| `eboot:385880` | 1 | 352 | 350 | 2 | width (soft) | Semi-Conformal Medium-Range Guided Missiles (Multi) |
| `eboot:388778` | 1 | 72 | 70 | 2 | width (soft) | Head Beam |
| `eboot:38E868` | 1 | 86 | 84 | 2 | width (soft) | Infinite Boost |
| `eboot:38EED0` | 2 | 170 | 168 | 2 | width (soft) | their HP is restored to 50%. |
| `eboot:392B6C` | 3 | 142 | 140 | 2 | width (soft) | powerful shooting SPA |
| `eboot:3B7018` | 1 | 58 | 56 | 2 | width (soft) | Vrlitwhai |
| `eboot:3B8B58` | 1 | 72 | 70 | 2 | width (soft) | Song Usage |
| `eboot:3B8B70` | 1 | 86 | 84 | 2 | width (soft) | Battroid Love |
| `eboot:3B90FC` | 1 | 44 | 42 | 2 | width (soft) | Myung |
| `eboot:3B9354` | 1 | 114 | 112 | 2 | width (soft) | Miyuki Shirakawa |
| `eboot:3BB8F0` | 1 | 212 | 210 | 2 | width (soft) | Mylene Valkyrie (Song Weapon 1) |
| `eboot:35E9E8` | 1 | 113 | 112 | 1 | width (soft) | Isamu Alva Dyson |
| `eboot:386C1C` | 1 | 253 | 252 | 1 | width (soft) | Medium Anti-Ship Missiles (Multi/Blast) |
| `eboot:3877C8` | 2 | 225 | 224 | 1 | width (soft) | Gatling guns mounted on both arms |
| `eboot:389124` | 1 | 281 | 280 | 1 | width (soft) | Commander's VF-1 prototype variable fighter |
| `eboot:389560` | 2 | 281 | 280 | 1 | width (soft) | Front-mounted weapons excel at focused fire |
| `eboot:389B44` | 2 | 253 | 252 | 1 | width (soft) | Hikaru flew it as a VF-4 squadron leader |
| `eboot:38A278` | 2 | 267 | 266 | 1 | width (soft) | Flown mainly by Diamond Force members |
| `eboot:38A6B8` | 2 | 281 | 280 | 1 | width (soft) | Its powerful trump card: the Macross Cannon |
| `eboot:38E800` | 1 | 183 | 182 | 1 | width (soft) | Reflects beam-type shots and |
| `eboot:3B2AC4` | 2 | 169 | 168 | 1 | width (soft) | wireless play will now end. |
| `eboot:3B6B8C` | 1 | 57 | 56 | 1 | width (soft) | Fledgling |
| `eboot:3B71A8` | 1 | 29 | 28 | 1 | width (soft) | Luca |
| `eboot:3B7F9C` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 10 |
| `eboot:3B7FCC` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 13 |
| `eboot:3B7FFC` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 16 |
| `eboot:3B8034` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 19 |
| `eboot:3B8068` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 22 |
| `eboot:3B8094` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 25 |
| `eboot:3B80CC` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 28 |
| `eboot:3B80FC` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 31 |
| `eboot:3B8160` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 37 |
| `eboot:3B8240` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 52 |
| `eboot:3B826C` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 55 |
| `eboot:3B82A4` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 58 |
| `eboot:3B82D4` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 61 |
| `eboot:3B832C` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 67 |
| `eboot:3B833C` | 1 | 211 | 210 | 1 | width (soft) | Show me this thing called 'kiiss'... |
| `eboot:3B835C` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 70 |
| `eboot:3B8388` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 73 |
| `eboot:3B83B8` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 76 |
| `eboot:3B83E4` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 79 |
| `eboot:3B841C` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 82 |
| `eboot:3B8454` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 85 |
| `eboot:3B8464` | 1 | 211 | 210 | 1 | width (soft) | Special live show time! Let's start! |
| `eboot:3B8484` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 88 |
| `eboot:3B84B8` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 91 |
| `eboot:3B8518` | 1 | 99 | 98 | 1 | width (soft) | Versus Wins: 97 |
| `eboot:3B86B4` | 1 | 183 | 182 | 1 | width (soft) | Heh, such futile struggling...!! |
| `eboot:3B9370` | 1 | 43 | 42 | 1 | width (soft) | Big Sis |
| `eboot:3B9718` | 2 | 99 | 98 | 1 | width (soft) | All units receive |
| `eboot:3BB074` | 1 | 169 | 168 | 1 | width (soft) | You already own this item. |
| `eboot:3BCD14` | 4 | 260 | 259 | 1 | width (soft) | Lyrics: Yuho Iwasato  Music: Yoko Kanno |
| `eboot:3BD074` | 4 | 260 | 259 | 1 | width (soft) | Lyrics: Yuho Iwasato  Music: Yoko Kanno |

## Not measured

Ids not found in the source dumps: 1067 (`locate:ma_030:3:FRIROY`, `locate:ma_040:22:ENEROY`, `locate:ma_060:3:FRIROY`, `locate:ma_090:3:FRIROY`, `locate:ma_095:3:FRIROY`, `locate:mc_010:5:ENEROY`, `locate:me_100:4:ENES00`, `locate:me_100:9:ENES10`, `locate:me_130:10:ENES00`, `locate:me_160:24:ENES10`, `locate:mh_010:5:ENEROY`, `locate:mh_020:11:ENEROY`, `locate:mi_010:4:FRIROY`, `locate:mi_010:8:DEMOROY`, `locate:mi_015:7:DEMOROY`, `locate:mi_030:34:FRIROY`, `locate:mi_030:35:DEMOROY`, `locate:ms_310:3:FRIROY`, `locate:ms_315:3:FRIROY`, `locate:ms_320:6:FRIROY`).

