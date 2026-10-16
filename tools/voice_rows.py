"""Build the voice-clip translation work file (docs/voice_subtitles.md).

Usage:
  python tools/voice_rows.py            build / refresh work/translation/en/voice/voice.json
  python tools/voice_rows.py --stats    print counts only

Inputs:
  work/source/voice/transcripts.json        Whisper output (tools/voice_transcribe.py), Japanese
  work/translation/en/voice/speakers.en.json  who speaks each prefix
  data/script/*.fes                         which missions use which clip numbers
  work/translation/en/dialogue.json         mission objectives and briefings (English, for context)

Output (gitignored, holds Japanese): work/translation/en/voice/voice.json
  rows: row, id, prefix, num, speaker, series, jp, dur, whisper (Whisper's
  flags), missions (mission scripts whose string pool holds the clip number:
  a hint only, the pools also hold other numbers), skip (why a clip gets no
  subtitle), en, flags, notes.
Existing English, flags and notes are kept when the file is rebuilt, and
the slice files work/translation/en/voice/slices/vslice_NNN.en.json win over
them (merge order: work file, then slices).

Also writes work/translation/en/voice/missions.en.json: for each mission id,
its English objective and briefing, for translators' context.

Row order (80 rows per slice):
  1. operators by clip number, the five operators of one number together
     (they read the same script, so the five transcripts check each other);
  2. the six custom pilots, by number;
  3. the named characters, by series then speaker then number;
  4. after the slices: a named character's clips with nothing to translate
     (silent placeholders, drums, narration) and repeats, whose transcript is
     the same as an earlier clip of the same character (same_as). Repeats are
     not translated again; voice_subs_export.py gives them the first clip's
     English.
"""

import glob
import json
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VDIR = os.path.join(ROOT, "work", "translation", "en", "voice")
WORK = os.path.join(VDIR, "voice.json")
SLICES = os.path.join(VDIR, "slices")
TRANSCRIPTS = os.path.join(ROOT, "work", "source", "voice", "transcripts.json")
SCRIPTS = os.path.join(ROOT, "work", "source", "dat", "data", "script")
SLICE_ROWS = 80

OPERATORS = ["o0_of0", "o0_of1", "o0_of2", "o0_om0", "o0_om1", "os_mis"]
CUSTOM = ["p0_om0", "p0_om1", "p0_om2", "p0_of0", "p0_of1", "p0_of2"]
SERIES_ORDER = ["Macross Zero", "SDF Macross", "Macross: Do You Remember Love?", "Macross Plus",
                "Macross 7", "Macross Dynamite 7", "Macross Frontier", "Macross II"]
MAX_MISSIONS = 6   # a clip number used by more missions than this is a stock line


def fes_numbers():
    """clip number -> sorted list of mission ids whose script pool has that number."""
    use = {}
    for f in sorted(glob.glob(os.path.join(SCRIPTS, "*.fes"))):
        d = open(f, "rb").read()
        pool = struct.unpack_from("<H", d, 0x12)[0]
        mid = os.path.basename(f)[:-4].upper()
        for s in set(d[pool:].split(b"\0")):
            if re.fullmatch(rb"\d{3,4}", s):
                use.setdefault(int(s), set()).add(mid)
    return {n: sorted(m) for n, m in use.items()}


def mission_context():
    d = json.load(open(os.path.join(ROOT, "work", "translation", "en", "dialogue.json"), encoding="utf-8"))
    out = {}
    for r in d["rows"]:
        if r["cat"] == "briefing":
            field = r["id"].rsplit(":", 1)[1]
            out.setdefault(r["scene"], {})["objective" if field == "strMission" else "briefing"] = \
                r.get("en", "").replace("\\n", " ")
    return out


def skip_reason(cid, num, t):
    if not cid.startswith("v"):
        return "sound effect"
    if cid.startswith("vp") and 900 <= num < 1000:
        return "era prologue narration: already on screen as English text"
    if "silent" in t.get("flags", []):
        return "no speech: silent placeholder clip"
    if "hallucination" in t.get("flags", []):
        return "no speech Whisper could read (shout, drums, effect)"
    return ""


def build():
    trans = json.load(open(TRANSCRIPTS, encoding="utf-8"))
    speakers = json.load(open(os.path.join(VDIR, "speakers.en.json"), encoding="utf-8"))["speakers"]
    uses = fes_numbers()
    old = {}
    if os.path.exists(WORK):
        old = {r["id"]: r for r in json.load(open(WORK, encoding="utf-8"))["rows"]}
    for p in sorted(glob.glob(os.path.join(SLICES, "vslice_*.en.json"))):
        for r in json.load(open(p, encoding="utf-8"))["rows"]:
            old.setdefault(r["id"], {}).update({k: r[k] for k in ("en", "flags", "notes") if k in r})

    clips = {}
    for cid in trans:
        m = re.fullmatch(r"v(\w+?)_(\d+)", cid)
        if m and m.group(1) in speakers:
            clips[cid] = (m.group(1), int(m.group(2)))

    def key(cid):
        prefix, num = clips[cid]
        if prefix in OPERATORS:
            return (0, num, OPERATORS.index(prefix))
        if prefix in CUSTOM:
            return (1, num, CUSTOM.index(prefix))
        sp = speakers[prefix]
        series = SERIES_ORDER.index(sp["series"]) if sp["series"] in SERIES_ORDER else 99
        return (2, series, sp["name"], prefix, num)

    # within one named character, a clip whose transcript repeats an earlier clip's
    # (Max's three variants, Klan's two sizes...) is not translated again: it goes after
    # all slices and takes the first clip's English (`same_as`)
    order, first, dups = sorted(clips, key=key), {}, {}
    for cid in order:
        prefix = clips[cid][0]
        if prefix in OPERATORS or prefix in CUSTOM:
            continue
        k = (speakers[prefix]["name"], trans[cid]["jp"])
        if trans[cid]["jp"] and k in first:
            dups[cid] = first[k]
        else:
            first.setdefault(k, cid)
    # named characters' clips with nothing to translate also go after the slices
    def group2_skip(c):
        prefix, num = clips[c]
        return prefix not in OPERATORS and prefix not in CUSTOM and skip_reason(c, num, trans[c])
    tail = [c for c in order if c in dups or group2_skip(c)]
    order = [c for c in order if c not in tail] + tail

    rows = []
    for i, cid in enumerate(order, 1):
        prefix, num = clips[cid]
        t, sp = trans[cid], speakers[prefix]
        o = old.get(cid, {})
        missions = uses.get(num, [])
        rows.append({
            "row": i, "id": cid, "prefix": prefix, "num": num,
            "speaker": sp["name"], "series": sp["series"],
            "jp": t["jp"], "dur": t["dur"], "whisper": t["flags"],
            "missions": missions if len(missions) <= MAX_MISSIONS else ["(stock line, %d missions)" % len(missions)],
            "skip": skip_reason(cid, num, t) or ("same line as " + dups[cid] if cid in dups else ""),
            "same_as": dups.get(cid, ""),
            "en": o.get("en", ""), "flags": o.get("flags", []), "notes": o.get("notes", ""),
        })
    to_slice = sum(1 for r in rows if not r["same_as"] and not (r["skip"] and r["prefix"] not in OPERATORS + CUSTOM))
    meta = {"about": "Voice-clip subtitles (docs/voice_subtitles.md). Rows hold Japanese: not for git; "
                     "the slices are the committed copy.",
            "slice_rows": SLICE_ROWS, "slices": -(-to_slice // SLICE_ROWS), "after_slices": len(rows) - to_slice}
    return {"_meta": meta, "rows": rows}


def main():
    d = build()
    rows = d["rows"]
    print("%d rows, %d slices, %d repeats and no-speech rows after them; %d to translate, %d skipped, %d translated"
          % (len(rows), d["_meta"]["slices"], d["_meta"]["after_slices"], sum(1 for r in rows if not r["skip"]),
             sum(1 for r in rows if r["skip"]), sum(1 for r in rows if r["en"])))
    if "--stats" in sys.argv:
        return
    json.dump(d, open(WORK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(mission_context(), open(os.path.join(VDIR, "missions.en.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("wrote", WORK)


if __name__ == "__main__":
    main()
