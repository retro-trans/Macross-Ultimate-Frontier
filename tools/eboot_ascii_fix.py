"""Fix English unit names that the original EBOOT already has in ASCII.

Usage: python tools/eboot_ascii_fix.py <in EBOOT> <out EBOOT> [--fixes <file>]

The EBOOT carries English labels for the units (lock-on labels, unit lists), with
the game's own romanization: VAJURA, GEPPERNITI, OCTOSS... Each is referenced by a
pointer from its unit record, and no game data file matches them, so they can be
rewritten in place. work/translation/en/eboot_ascii.en.json lists the names that
clash with the glossary (rows: id "eboot_ascii:<file offset hex>", old, en).

Each row is written over the old string at its offset. The tool checks the old
bytes first and that the new name (plus its terminating NUL) fits the slot up to
the next string; the rest of the slot is filled with NUL bytes.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXES = os.path.join(ROOT, "work", "translation", "en", "eboot_ascii.en.json")


def apply(data, rows):
    data = bytearray(data)
    for r in rows:
        off = int(r["id"].split(":")[1], 16)
        old, new = r["old"].encode("ascii"), r["en"].encode("ascii")
        if data[off:off + len(old) + 1] != old + b"\0":
            raise ValueError("%s: expected %r" % (r["id"], r["old"]))
        end = off + len(old) + 1
        while end < len(data) and data[end] == 0:
            end += 1
        if len(new) + 1 > end - off:
            raise ValueError("%s: %r does not fit %d bytes" % (r["id"], r["en"], end - off))
        n = max(len(old), len(new)) + 1
        data[off:off + n] = new + bytes(n - len(new))
    return bytes(data)


def main():
    args = sys.argv[1:]
    fixes = FIXES
    if "--fixes" in args:
        i = args.index("--fixes")
        fixes = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    rows = json.load(open(fixes, encoding="utf-8"))["rows"]
    out = apply(open(args[0], "rb").read(), rows)
    open(args[1], "wb").write(out)
    print("%d unit names fixed" % len(rows))


if __name__ == "__main__":
    main()
