"""Measure translated English in pixels with the variable-width font and flag
lines that do not fit their on-screen box.

Usage:
  python tools/check_widths.py limits
      Derive the box limits from the Japanese source and write
      work/ui/text_limits.json. Hand-set fields (size, limit_override,
      confirmed, evidence) of an existing file are kept.
  python tools/check_widths.py [check] [translation.json ...] [--all]
      Measure every English line (default inputs: work/translation/en/*.en.json)
      and write work/ui/width_report.md and work/ui/width_report.json.
      --all also lists lines that fit. --out DIR writes the report there instead.
      Exit code 1 if anything is over.

Widths: ASCII 0x20-0x7E use the VWF advance from work/output/vwf/vwf_widths.json
(tools/vwf_build.py); at font size s the advance is s - round((14-adv)*s/14).
Double-byte characters are s px. The original Japanese is measured the way
the unpatched game drew it: double-byte s px, single-byte s*0.75 px.

The limit of a text type is the widest Japanese line of that type (the game's
own box, as the designers filled it), at the size the game draws it. Sizes
and boxes confirmed in game are marked in text_limits.json. Strings with no
known box (EBOOT labels outside any list) are held to the width of their own
Japanese line, which is a soft limit: the real box may be wider.

Inputs need only id and en, so the git-safe *.en.json copies work. The
Japanese source dumps in work/source/text/ (tools/dump_text.py,
tools/dump_eboot.py) must exist locally.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(ROOT, "work/source/text")
WIDTHS = os.path.join(ROOT, "work/output/vwf/vwf_widths.json")
LIMITS = os.path.join(ROOT, "work/ui/text_limits.json")
REPORT_MD = os.path.join(ROOT, "work/ui/width_report.md")
REPORT_JSON = os.path.join(ROOT, "work/ui/width_report.json")

NARRATION = (0x38F6A0, 0x3927F0)  # EBOOT file offsets, end inclusive of the last string
HELP_TABLE = 0x3480DC             # vaddr of the 167-entry menu help-line table
MISSION_TABLE = (0x2DA000, 0x2E6000, 0xB0)  # vaddr range of the mission records, record size
MISSION_FIELDS = {0x00: "eboot_objective", 0x04: "eboot_objective", 0xAC: "eboot_objective",
                  0x3C: "eboot_bonus", 0x40: "eboot_bonus", 0x44: "eboot_bonus", 0x9C: "eboot_mission_name"}
BS_N = "\\n"                      # CSV line break: backslash + n
CODE = re.compile(r"\{[a-z]([^{}]*)\}")
PH = re.compile(r"%[-0-9.]*[sd]")
MANUAL = ("size", "limit_override", "line_limits", "max_lines_override", "max_chars", "box", "confirmed", "evidence",
          "note")

# Text types: description and the font size the game draws them at (14 unless confirmed).
TYPES = {
    "narration": "EBOOT era prologue/epilogue narration, one string per on-screen line",
    "mission_objective": "mission_ext.csv strMission: mission objective",
    "mission_story": "mission_ext.csv strStory: mission briefing story",
    "fes_objective": "FES string pools (not mt_*): objective shown during a mission",
    "fes_tutorial": "FES string pools (mt_*): tutorial instruction box",
    "ms_name": "ms_ext.csv strDescription line 1: unit display name",
    "ms_desc": "ms_ext.csv strDescription lines 2+: unit description",
    "pilot_desc": "pilot_ext.csv strDescription: pilot profile (ends with the CV credit)",
    "pack_name": "pack_ext.csv strDescription line 1: pack name",
    "pack_desc": "pack_ext.csv strDescription lines 2+: pack description",
    "nn_pilot": "nn_ext.csv 0000-0999: Nyan-Nyan shop pilot names and series headers",
    "nn_unit": "nn_ext.csv 1000-1999: shop unit names",
    "nn_song": "nn_ext.csv 2000-2999: songs, weapons, formations",
    "nn_gallery": "nn_ext.csv 3000-3999: gallery captions",
    "nn_other": "nn_ext.csv 4000-4999: other collection names",
    "nn_title": "nn_ext.csv 5000-5999: player titles and quotes (ID card)",
    "nn_figure": "nn_ext.csv 6000-6999: figure names",
    "eboot_help": "EBOOT menu help bar (table 0x3480DC, 167 lines)",
    "eboot_objective": "EBOOT mission records +0x00/+0x04/+0xAC: stock objectives (orange objective strip)",
    "eboot_bonus": "EBOOT mission records +0x3C/+0x40/+0x44: bonus conditions",
    "eboot_mission_name": "EBOOT mission records +0x9C: mission name (mission list, title card)",
}
# Measured in PPSSPP 1.20.4 on the original disc, 2026-10-15 (screens: work/output/ui_screens/,
# gitignored because they show Japanese script). Boxes are x, y, w, h in native 480x272 px.
CONFIRMED = {
    "eboot_help": {
        "size": 12, "confirmed": True, "box": [95, 236, 290, 16],
        "evidence": "Help bar, centred. Japanese lines of 20 and 23 chars span 240 and 272 px; the VWF "
                    "test line 'Single-player modes: missions from every era, or a full campaign' spans "
                    "377 px, and this tool gives 378 at size 12. The green frame is about 290 px inside; "
                    "the longest Japanese line (312) already runs onto the bar ends, and text far too "
                    "wide scrolls as a marquee.",
    },
    "narration": {
        "size": 12, "confirmed": True, "box": [6, 190, 468, 80],
        "evidence": "Era prologue: up to 5 strings per screen, each centred on its own line. A 33-char "
                    "line spans 393 px (11.9 per char). The limit is the longest Japanese line (468); "
                    "the screen is 480. v0.2.0 test build (prologue Zero, and the Zero epilogue shown "
                    "through the prologue slots): a line wider than 480 px is cut off at both screen "
                    "edges. 'In that hopeless situation, Shin's voice managed to awaken Sara's heart.' "
                    "spans 422.5 px on screen and this tool gives 425.",
    },
    "mission_story": {
        "size": 11, "confirmed": True, "box": [7, 196, 465, 28], "line_limits": [429, 415],
        "evidence": "Campaign mission screen, left-aligned from x=7, 2 lines. A 33-char line spans "
                    "355 px of ink (size 11). Line 2 shares its row with the launch button, which "
                    "starts at x=424, so line 2 is held to 415. Line 1 is held to the longest Japanese "
                    "line (429); the panel itself runs to about x=472. v0.2.0 test build: a line wider "
                    "than the panel is squeezed horizontally to fit, not cut. Each line is copied into "
                    "an 80-character slot with no bounds check: MA_010 line 1 (92 chars) showed its "
                    "first 80 characters followed by all of line 2, so max_chars is 79 (room for the "
                    "terminator).",
        "max_chars": 79,
    },
    "fes_tutorial": {
        "size": 14, "confirmed": True, "box": [84, 22, 309, 48], "limit_override": 309,
        "evidence": "v0.2.0 test build, tutorial MT_010: the 'Information' box at the top, centred, up "
                    "to 3 lines. The frame is x=82..395, about 309 px inside, which matches the longest "
                    "Japanese line (308 at size 14). 'During training, the flight mode is set to Normal "
                    "Flight' spans 372 px on screen and this tool gives 373. Lines that are too wide "
                    "run past the frame on both sides; they are not cut or squeezed.",
    },
    "mission_objective": {
        "size": 10, "confirmed": True, "box": [248, 134, 214, 26], "limit_override": 214,
        "evidence": "Mission select, 'Mission Information' panel, 2 lines from x=248; the text box ends "
                    "at x=464. A 9-char line spans 82 px of ink (size 10). Box 214 px, wider than the "
                    "longest Japanese line (190).",
    },
    "fes_objective": {
        "size": 10, "confirmed": True, "box": [248, 118, 212, 13], "limit_override": 212,
        "evidence": "Objective strip (orange) in the 'Mission Information' panel and in the pause "
                    "screen, one line from x=248 to the frame at x=462. 6 chars span 57.5 px of ink "
                    "(size 10). The EBOOT stock objectives use the same strip. Box 212 px, wider than "
                    "the longest Japanese line (160). Two-line objectives (3 strings) are shown somewhere "
                    "not yet seen.",
    },
}
CONFIRMED["eboot_objective"] = dict(CONFIRMED["fes_objective"], evidence=(
    "Same orange objective strip as fes_objective: the mission tested (MA_010) shows the EBOOT "
    "stock objective there, in the mission list and the pause screen."))
DEFAULT_PLACEHOLDERS = {
    "%s": {"text": "　" * 10, "note": "player or partner name: assumed 10 double-byte chars, the longest "
                                         "default name (the name entry limit is not confirmed)"},
    "%d": {"text": "999", "note": "a number: assumed 3 ASCII digits"},
}


def load_json(path):
    return json.load(open(path, encoding="utf-8"))


ADV = load_json(WIDTHS)["advance"]


def ascii_adv(o, size):
    return size - round((14 - ADV[o - 0x20]) * size / 14)


def char_width(ch, size, original=False):
    """Pixel advance of one character, or None if Shift-JIS cannot encode it."""
    o = ord(ch)
    if 0x20 <= o < 0x7F:
        return size * 0.75 if original else ascii_adv(o, size)
    try:
        b = ch.encode("cp932")
    except UnicodeEncodeError:
        return None
    if len(b) == 1:  # half-width kana: no VWF entry, assume a full cell
        return size * 0.75 if original else size
    return size


def split_lines(s):
    return s.replace(BS_N, "\n").split("\n")


def expand(line, placeholders):
    line = CODE.sub(lambda m: m.group(1), line)
    return PH.sub(lambda m: placeholders.get(m.group(0)[0] + m.group(0)[-1], {}).get("text", ""), line)


def line_width(line, size, placeholders, original=False):
    w, bad = 0, []
    for ch in expand(line, placeholders):
        cw = char_width(ch, size, original)
        if cw is None:
            bad.append(ch)
            cw = size
        w += cw
    return w, bad


# ---------------------------------------------------------------- sources

class Source:
    """Japanese source text by id, with the text type of each id."""

    def __init__(self):
        self.jp = {}
        self.type = {}
        self.eboot = {}
        for r in load_json(os.path.join(TEXT, "menu_text.json")):
            self.add(r["id"], r["jp"], self.menu_type(r))
        for r in load_json(os.path.join(TEXT, "fes_strings.json")):
            self.add(r["id"], r["jp"], "fes_tutorial" if r["id"].startswith("mt_") else "fes_objective")
        eb = load_json(os.path.join(TEXT, "eboot_strings.json"))
        self.groups = self.eboot_groups(eb)
        for r in eb:
            self.eboot[r["id"]] = r
            self.add(r["id"], r["jp"], self.eboot_type(r))

    def add(self, id_, jp, typ):
        self.jp[id_] = jp
        self.type[id_] = typ

    @staticmethod
    def menu_type(r):
        src = r["source"].rsplit("/", 1)[-1]
        if src == "mission_ext.csv":
            return "mission_objective" if r["field"] == "strMission" else "mission_story"
        if src == "nn_ext.csv":
            n = int(r["key"].rsplit("_", 1)[-1]) // 1000
            return ["nn_pilot", "nn_unit", "nn_song", "nn_gallery", "nn_other", "nn_title", "nn_figure"][min(n, 6)]
        return {"ms_ext.csv": "ms", "pilot_ext.csv": "pilot", "pack_ext.csv": "pack"}[src]

    @staticmethod
    def list_runs(r):
        """Pointer-table runs that hold one kind of string: a field across a struct
        array (stride > 4), or a plain pointer list of 4+ entries."""
        out = []
        for ref in r["refs"]:
            t = ref.get("table")
            if MISSION_TABLE[0] <= ref.get("vaddr", -1) < MISSION_TABLE[1]:
                continue  # mission records: typed by field (mission_field)
            if t and (t["stride"] > 4 or t["count"] >= 4):
                out.append(t["start"])
        return out

    def eboot_groups(self, eb):
        groups = defaultdict(list)
        for r in eb:
            for start in self.list_runs(r):
                groups[start].append(r["id"])
        return groups

    @staticmethod
    def mission_field(r):
        for ref in r["refs"]:
            if ref["kind"] == "ptr" and MISSION_TABLE[0] <= ref["vaddr"] < MISSION_TABLE[1]:
                t = MISSION_FIELDS.get((ref["vaddr"] - MISSION_TABLE[0]) % MISSION_TABLE[2])
                if t:
                    return t
        return None

    def eboot_type(self, r):
        if NARRATION[0] <= r["offset"] <= NARRATION[1]:
            return "narration"
        field = self.mission_field(r)
        if field:
            return field
        runs = self.list_runs(r)
        if HELP_TABLE in runs:
            return "eboot_help"
        if runs:
            # several lists: the narrowest box applies; resolved in Limits.for_id
            return "eboot_list:%06X" % runs[0]
        return "eboot_self"

    def line_types(self, id_, n_lines):
        """Text type of each line: ms/pack split name (line 1) and body."""
        t = self.type[id_]
        if t in ("ms", "pack"):
            return [t + "_name"] + [t + "_desc"] * (n_lines - 1)
        if t == "pilot":
            return ["pilot_desc"] * n_lines
        return [t] * n_lines


# ---------------------------------------------------------------- limits

def jp_lines(jp):
    # mission_ext MC_090 has a typo: a full-width yen + n where a break belongs
    return split_lines(jp.replace("￥ｎ", BS_N))


def derive_limits(src, old):
    placeholders = old.get("placeholders") or DEFAULT_PLACEHOLDERS
    stats = {}

    def feed(typ, id_, line, idx_lines):
        w, _ = line_width(line, 14, placeholders, original=True)
        s = stats.setdefault(typ, {"count": 0, "ids": set(), "jp_max_px": 0, "longest_id": None, "jp_max_lines": 0})
        s["ids"].add(id_)
        if w > s["jp_max_px"]:
            s["jp_max_px"], s["longest_id"] = w, id_
        s["jp_max_lines"] = max(s["jp_max_lines"], idx_lines)

    for id_, jp in src.jp.items():
        t = src.type[id_]
        if t == "eboot_self":
            continue
        lines = jp_lines(jp)
        if t.startswith("eboot_list"):  # a string in several lists counts in each
            for start in Source.list_runs(src.eboot[id_]):
                for n, line in enumerate(lines, 1):
                    feed("eboot_list:%06X" % start, id_, line, n)
            continue
        types = src.line_types(id_, len(lines))
        per_type = defaultdict(int)
        for line, lt in zip(lines, types):
            per_type[lt] += 1
            feed(lt, id_, line, per_type[lt])
    types = {}
    old_types = old.get("types", {})
    for typ in sorted(stats, key=lambda t: (t.startswith("eboot_list"), t)):
        s = stats[typ]
        e = {"desc": TYPES.get(typ) or "EBOOT strings of the pointer list at vaddr 0x%s" % typ.split(":")[1],
             "count": len(s["ids"]), "jp_max_px_at_14": s["jp_max_px"], "jp_max_lines": s["jp_max_lines"],
             "longest_id": s["longest_id"], "size": 14, "confirmed": False}
        e.update(CONFIRMED.get(typ, {}))
        for k in MANUAL:
            if k in old_types.get(typ, {}):
                e[k] = old_types[typ][k]
        size = e["size"]
        e["limit_px"] = e.get("limit_override") or round(s["jp_max_px"] * size / 14, 1)
        e["max_lines"] = e.get("max_lines_override") or s["jp_max_lines"]
        types[typ] = e
    return {
        "_meta": {
            "what": "Box width per text type, in px at the size the game draws that type.",
            "made_by": "tools/check_widths.py limits",
            "method": "limit_px = widest original Japanese line of the type (double-byte = size px, "
                      "single-byte = 0.75 * size), unless limit_override is set. size is 14 unless "
                      "confirmed in game. English is measured with the VWF advances at the same size, "
                      "so an unconfirmed size changes the verdict only by rounding.",
            "eboot_self": "EBOOT strings outside any list are held to the width of their own Japanese "
                          "line (soft limit, box unknown).",
            "hand_set_fields": list(MANUAL),
        },
        "placeholders": placeholders,
        "types": types,
    }


class Limits:
    def __init__(self, data, src):
        self.d, self.src = data, src
        self.types = data["types"]
        self.placeholders = data.get("placeholders") or DEFAULT_PLACEHOLDERS

    def for_line(self, id_, lt, n, jp_line):
        """(type label, size, limit px, max lines, soft) for line n (1-based) of type lt."""
        if lt.startswith("eboot_list") or lt == "eboot_self":
            r = self.src.eboot[id_]
            runs = [k for k in ("eboot_list:%06X" % s for s in Source.list_runs(r)) if k in self.types]
            if runs:
                best = min(runs, key=lambda k: self.types[k]["limit_px"])
                t = self.types[best]
                return best, t["size"], t["limit_px"], t["max_lines"], False
            w, _ = line_width(jp_line or "", 14, self.placeholders, original=True)
            return "eboot_self", 14, w, len(split_lines(r["jp"])), True
        t = self.types[lt]
        per_line = t.get("line_limits") or []
        limit = per_line[min(n, len(per_line)) - 1] if per_line else t["limit_px"]
        return lt, t["size"], limit, t["max_lines"], False


# ---------------------------------------------------------------- check

def load_translations(paths):
    rows = {}
    for p in paths:
        d = load_json(p)
        for r in d.get("rows", []) if isinstance(d, dict) else d:
            if r.get("id") and r.get("en"):
                rows[r["id"]] = r["en"]
    return rows


def check(paths, show_all):
    src = Source()
    if not os.path.exists(LIMITS):
        sys.exit("no %s: run 'python tools/check_widths.py limits' first" % os.path.relpath(LIMITS, ROOT))
    lim = Limits(load_json(LIMITS), src)
    rows = load_translations(paths)
    results, unknown = [], []
    summary = defaultdict(lambda: {"rows": set(), "lines": 0, "over": 0, "max_fill": 0.0})
    for id_, en in rows.items():
        if id_ not in src.type:
            unknown.append(id_)
            continue
        jp = jp_lines(src.jp[id_])
        lines = split_lines(en)
        lts = src.line_types(id_, max(len(lines), len(jp)))
        per_type = defaultdict(int)
        for i, line in enumerate(lines):
            lt = lts[i]
            per_type[lt] += 1
            label, size, limit, max_lines, soft = lim.for_line(id_, lt, per_type[lt], jp[i] if i < len(jp) else None)
            w, bad = line_width(line, size, lim.placeholders)
            issues = []
            if w > limit:
                issues.append("width")
            if per_type[lt] > max_lines:
                issues.append("lines")
            max_chars = lim.types.get(label, {}).get("max_chars")
            if max_chars and len(expand(line, lim.placeholders)) > max_chars:
                issues.append("chars")
            if bad:
                issues.append("unencodable")
            s = summary[label]
            s["rows"].add(id_)
            s["lines"] += 1
            s["max_fill"] = max(s["max_fill"], w / limit if limit else 0)
            if issues:
                s["over"] += 1
            if issues or show_all:
                results.append({"id": id_, "line": i + 1, "type": label, "size": size, "width": w,
                                "limit": limit, "over_by": round(w - limit, 1), "max_lines": max_lines,
                                "issues": issues, "soft": soft, "bad_chars": "".join(bad), "en": line})
    results.sort(key=lambda r: (r["type"], -(r["over_by"])))
    over = [r for r in results if r["issues"]]
    write_report(paths, rows, results, over, summary, unknown, lim)
    print("%d rows, %d lines measured; %d lines over their limit (%d soft)" % (
        len(rows), sum(s["lines"] for s in summary.values()), len(over), sum(r["soft"] for r in over)))
    for t, s in sorted(summary.items()):
        print("  %-24s rows %4d  lines %4d  over %3d  max fill %3d%%" % (
            t, len(s["rows"]), s["lines"], s["over"], round(s["max_fill"] * 100)))
    if unknown:
        print("ids not in the source dumps (not measured): %d, e.g. %s" % (len(unknown), unknown[:5]))
    print("wrote", rel(REPORT_MD), "and", rel(REPORT_JSON))
    return 1 if over else 0


def rel(p):
    try:
        return os.path.relpath(p, ROOT).replace("\\", "/")
    except ValueError:  # another drive
        return p


def fmt(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")


def write_report(paths, rows, results, over, summary, unknown, lim):
    json.dump({"inputs": [rel(p) for p in paths], "rows": len(rows), "lines": results,
               "unknown_ids": unknown}, open(REPORT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = ["# Width report", "",
           "Made by `python tools/check_widths.py`. Widths are px at the size the game draws the text "
           "type (see `work/ui/text_limits.json`). Inputs: %s." % ", ".join(
               "`%s`" % rel(p) for p in paths), "",
           "## Summary", "",
           "| Type | Size | Limit px | Max lines | In game | Rows | Lines | Over | Max fill |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for t, s in sorted(summary.items()):
        e = lim.types.get(t, {})
        out.append("| %s | %s | %s | %s | %s | %d | %d | %d | %d%% |" % (
            t, e.get("size", 14), " / ".join(fmt(x) for x in e.get("line_limits") or [e["limit_px"]]) if e
            else "own JP line", e.get("max_lines", "-"), "confirmed" if e.get("confirmed") else "no",
            len(s["rows"]), s["lines"], s["over"], round(s["max_fill"] * 100)))
    out += ["", "## Lines over the limit (%d)" % len(over), ""]
    if not over:
        out.append("None.")
    by_type = defaultdict(list)
    for r in over:
        by_type[r["type"]].append(r)
    for t, rs in by_type.items():
        out += ["### %s (%d)" % (t, len(rs)), "",
                "| Id | Line | Width | Limit | Over | Issue | English |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for r in rs:
            issue = ", ".join(r["issues"]) + (" (soft)" if r["soft"] else "")
            if r["bad_chars"]:
                issue += " `%s`" % r["bad_chars"]
            if "lines" in r["issues"]:
                issue += " (max %d)" % r["max_lines"]
            if "chars" in r["issues"]:
                issue += " (%d chars, max %d)" % (len(r["en"]), lim.types[r["type"]]["max_chars"])
            out.append("| `%s` | %d | %s | %s | %s | %s | %s |" % (
                r["id"], r["line"], fmt(r["width"]), fmt(r["limit"]), fmt(r["over_by"]), issue,
                r["en"].replace("|", "\\|")))
        out.append("")
    if unknown:
        out += ["## Not measured", "", "Ids not found in the source dumps: %d (%s)." % (
            len(unknown), ", ".join("`%s`" % u for u in unknown[:20])), ""]
    open(REPORT_MD, "w", encoding="utf-8").write("\n".join(out) + "\n")


def main(argv):
    global REPORT_MD, REPORT_JSON
    show_all = "--all" in argv
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
        os.makedirs(out, exist_ok=True)
        REPORT_MD, REPORT_JSON = os.path.join(out, "width_report.md"), os.path.join(out, "width_report.json")
    args = [a for a in argv if not a.startswith("--")]
    if args and args[0] == "limits":
        old = load_json(LIMITS) if os.path.exists(LIMITS) else {}
        data = derive_limits(Source(), old)
        os.makedirs(os.path.dirname(LIMITS), exist_ok=True)
        json.dump(data, open(LIMITS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        named = [t for t in data["types"] if not t.startswith("eboot_list")]
        for t in named:
            e = data["types"][t]
            print("  %-18s size %d  limit %9s px  lines %d  (%d strings, longest %s)%s" % (
                t, e["size"], "/".join(fmt(x) for x in e.get("line_limits") or [e["limit_px"]]),
                e["max_lines"], e["count"], e["longest_id"],
                "  confirmed" if e["confirmed"] else ""))
        print("  + %d EBOOT pointer lists" % (len(data["types"]) - len(named)))
        print("wrote", os.path.relpath(LIMITS, ROOT))
        return 0
    if args and args[0] == "check":
        args = args[1:]
    paths = args or sorted(glob.glob(os.path.join(ROOT, "work/translation/en/*.en.json")))
    return check(paths, show_all)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
