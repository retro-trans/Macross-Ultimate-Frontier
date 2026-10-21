"""Move parts of A2A 2D layouts (data/menu/**/*.a2a) for the English screens.

Usage: python tools/a2a_patch.py [--out <overlay>] [--patches work/ui/a2a_patches.json]

Each layout part has a keyframe of 13 words: [part, 1, 0, -1, 0, 0, 0, 100, 100, -1,
x, y, 0] (docs/formats.md). work/ui/a2a_patches.json lists {file, part, old_x, x};
the tool finds the part's keyframe, checks that x is old_x and writes the new x. The
patched layout goes to <overlay>/<file> for muf_archive.py repack --overlay.
"""
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIG = [1, 0, -1, 0, 0, 0, 100, 100, -1]


def keyframe(data, part):
    """Byte offset of the x word of `part`'s keyframe; exactly one must exist."""
    n = len(data) // 4
    v = struct.unpack_from("<%di" % n, data, 0)
    hits = [i for i in range(n - 12) if v[i] == part and list(v[i + 1:i + 10]) == SIG]
    if len(hits) != 1:
        raise ValueError("part %d: %d keyframes found" % (part, len(hits)))
    return 4 * (hits[0] + 10)


def main():
    args = sys.argv[1:]
    out = args[args.index("--out") + 1] if "--out" in args else os.path.join(ROOT, "work", "output", "build", "overlay")
    pfile = args[args.index("--patches") + 1] if "--patches" in args else os.path.join(ROOT, "work", "ui", "a2a_patches.json")
    patches = json.load(open(pfile, encoding="utf-8"))["patches"]
    by_file = {}
    for p in patches:
        by_file.setdefault(p["file"], []).append(p)
    for f, ps in sorted(by_file.items()):
        src = os.path.join(out, f) if os.path.exists(os.path.join(out, f)) else os.path.join(ROOT, "work", "source", "dat", f)
        data = bytearray(open(src, "rb").read())
        if data[:4] != b"A2A ":
            raise ValueError("%s is not an A2A layout" % f)
        for p in ps:
            o = keyframe(data, p["part"])
            x = struct.unpack_from("<i", data, o)[0]
            if x != p["old_x"]:
                raise ValueError("%s part %d: x is %d, expected %d" % (f, p["part"], x, p["old_x"]))
            struct.pack_into("<i", data, o, p["x"])
        dst = os.path.join(out, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(data)
        print("%s: %d parts moved" % (f, len(ps)))


if __name__ == "__main__":
    main()
