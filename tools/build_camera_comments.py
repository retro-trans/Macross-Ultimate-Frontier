"""English for the developer comments in data/tbl/camera.tbl (never shown in game).

Usage: python tools/build_camera_comments.py
Writes work/translation/en/camera_tbl.json (line number, Japanese, English;
gitignored) and camera_tbl.en.json (no Japanese). Comment lines start with ';'.
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = {
 1: '; Values are ignored if there is a space between "=" and the value.',
 2: '; Lines starting with ";" are comments.',
 4: '; Camera behaviour parameters.',
 5: '; Basic tuning is done with the following parameters:',
 6: ';\tEYE_X\t\tOffset of the eye (camera) X coordinate.',
 7: ';\tEYE_Y\t\tOffset of the eye (camera) Y coordinate.',
 8: ';\tEYE_Z\t\tOffset of the eye (camera) Z coordinate.',
 9: ';\tTARGET_X\tOffset of the look-at point X coordinate.',
 10: ';\tTARGET_Y\tOffset of the look-at point Y coordinate.',
 11: ';\tTARGET_Z\tOffset of the look-at point Z coordinate.',
 12: ';\tROLL\t\tRotation offset (degrees).',
 13: ';\tRATE\t\tInterpolation rate.',
 15: '; Fighter mode (not locked on).',
 16: "; The offset is computed from the unit's tilt.",
 17: '; It is computed within the FIGHTER_PITCH_RANGE and FIGHTER_ROLL_RANGE',
 18: '; set in [BEHAVIOR_PARAM].',
 19: '; With FIGHTER_ROLL at 60.0, a tilt of -60 to 60 degrees maps to a rate of -1.0 to 1.0,',
 20: '; and the parameters below are multiplied by that rate to get the offset.',
 21: '; The ROLL value is ignored.',
 35: '; GERWALK mode (not locked on).',
 36: '; Values for turning left.',
 37: '; When turning right, the ROLL value is inverted.',
 48: '; Battroid mode (not locked on).',
 59: '; Fighter mode (locked on).',
 60: '; The offset is computed from the positions of the unit and the target.',
 61: '; It uses the angle of the target as seen from the unit, within the',
 62: '; LOCKON_FIGHTER_PITCH_RANGE and LOCKON_FIGHTER_ROLL_RANGE of [BEHAVIOR_PARAM].',
 63: '; (offset computed in that range)',
 64: '; The ROLL value is ignored.',
 82: '; GERWALK mode (locked on).',
 83: '; Values for turning left.',
 84: '; When turning right, EYE_X, TARGET_X and ROLL are inverted.',
 95: '; Battroid mode (locked on, short range).',
 96: '; Used when the distance to the target is LOCKON_BATTROID_SHORT or less.',
 107: '; Battroid mode (locked on, mid range).',
 118: '; Battroid mode (locked on, long range).',
 119: '; Used when the distance to the target is LOCKON_BATTROID_LONG or more.',
 130: '; While shooting down missiles.',
 141: '; During an SP attack.',
 154: '; Individual parameters.',
 155: ';\tBOOST_EYE_OFFSET_Z\t\t\tEye Z offset while boosting.',
 156: ';\tCHARGE_BOOST_EYE_OFFSET_Z\tEye Z offset during a Charge Boost.',
 157: ';\tBREAK_EYE_OFFSET_Z\t\t\tEye Z offset while braking.',
 158: ";\tFIGHTER_ROLL_RATE\t\t\tRate of camera Z rotation relative to the unit's tilt in Fighter mode.",
 159: ';\tFIGHTER_PITCH\t\t\t\tNose pitch range in Fighter mode (degrees).',
 160: ';\tFIGHTER_ROLL\t\t\t\tBank range in Fighter mode (degrees).',
 161: ';\tLOCKON_FIGHTER_PITCH\t\tNose pitch range in Fighter mode, locked on (degrees).',
 162: ';\tLOCKON_FIGHTER_ROLL\t\t\tBank range in Fighter mode, locked on (degrees).',
 163: ';\tLOCKON_BATTROID_SHORT\t\tSwitch distance for Battroid mode (locked on, short range).',
 164: ';\tLOCKON_BATTROID_LONG\t\tSwitch distance for Battroid mode (locked on, long range).',
}
JPW = re.compile(r"[぀-ヿ㐀-鿿]")
lines = open(os.path.join(ROOT, "work/source/dat/data/tbl/camera.tbl"), "rb").read().decode("cp932").splitlines()
rows, missing = [], []
for i, l in enumerate(lines, 1):
    if JPW.search(l):
        if i not in EN:
            missing.append(i)
        rows.append({"line": i, "jp": l, "en": EN.get(i, "")})
print("japanese lines %d, translated %d, missing %s" % (len(rows), sum(1 for r in rows if r["en"]), missing))
out = os.path.join(ROOT, "work/translation/en/camera_tbl.json")
json.dump({"file": "data/tbl/camera.tbl", "rows": rows}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"file": "data/tbl/camera.tbl", "rows": [{"line": r["line"], "en": r["en"]} for r in rows]},
          open(out[:-5] + ".en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
