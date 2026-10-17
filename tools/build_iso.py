"""Build a translated test ISO from the original disc (docs/build.md).

Usage:
  python tools/build_iso.py <version> [--iso "<original>.iso"] [--tr <translation.json> ...] [--no-images] [--no-hd] [--ttf <font>]
                            [--voice-subs <subs.json> ...] [--voice-placeholder] [--work <dir>]
  e.g. python tools/build_iso.py 0.4.0

Steps (each one is a tool that can also be run on its own):
  1. tools/vwf_build.py       VWF font + patched EBOOT        -> work/output/vwf/
  2. tools/dump_eboot.py      string map of that EBOOT        -> work/output/build/eboot_strings.vwf.json
  3. tools/eboot_insert.py    relocate the English EBOOT text -> work/output/build/EBOOT.BIN
  4. tools/insert_text.py     CSV cells and FES string pools  -> work/output/build/overlay/
     (the VWF font is copied into the same overlay)
  4b. tools/redraw_images.py  English redrawn textures (GIM)  -> work/output/build/overlay/
     (skip with --no-images; layout in work/ui/redraw_layout.json, docs/image_redraw.md)
  4c. tools/voice_subs_patch.py + voice_subs_at3.py: voice-clip subtitles (only with
     --voice-subs or --voice-placeholder; docs/voice_subtitles.md)
  5. tools/muf_archive.py     repack with the overlay         -> work/output/build/USRDIR/
  6. tools/iso_patch.py       new EBOOT and archives          -> work/output/Macross Ultimate Frontier (EN v<version>).iso

--work <dir> puts the intermediate files in <dir> (and <dir>/vwf) instead of
work/output/build and work/output/vwf, so two builds can run side by side.

The EBOOT on the disc is the decrypted PRX (plain ELF). PPSSPP and custom
firmware load it as it is; see docs/build.md.
"""

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def run(*args):
    print(">", " ".join(args), flush=True)
    subprocess.run([PY] + list(args), cwd=ROOT, check=True)


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        sys.exit(__doc__)
    version = args.pop(0)
    iso = "Macross Ultimate Frontier (Japan).iso"
    tr = []
    images = True
    vwf_args = []
    voice_subs, voice_placeholder, work = [], False, None
    while args:
        a = args.pop(0)
        if a == "--iso":
            iso = args.pop(0)
        elif a == "--tr":
            tr.append(args.pop(0))
        elif a == "--no-images":
            images = False
        elif a == "--no-hd":
            vwf_args.append("--no-hd")
        elif a == "--ttf":
            vwf_args += ["--ttf", args.pop(0)]
        elif a == "--voice-subs":
            voice_subs.append(args.pop(0))
        elif a == "--voice-placeholder":
            voice_placeholder = True
        elif a == "--work":
            work = args.pop(0)
        else:
            sys.exit("unknown argument " + a)
    tr = tr or [os.path.join("work", "translation", "en", "dialogue.json")]

    b = work or os.path.join("work", "output", "build")
    vwf = os.path.join(work, "vwf") if work else os.path.join("work", "output", "vwf")
    if work:
        vwf_args += ["--out", vwf]
    vwf_eboot = os.path.join(vwf, "PSP_GAME", "SYSDIR", "EBOOT.BIN")
    dump = os.path.join(b, "eboot_strings.vwf.json")
    eboot = os.path.join(b, "EBOOT.BIN")
    overlay = os.path.join(b, "overlay")
    usrdir = os.path.join(b, "USRDIR")
    out_iso = os.path.join("work", "output", "Macross Ultimate Frontier (EN v%s).iso" % version)

    if os.path.isdir(os.path.join(ROOT, overlay)):
        shutil.rmtree(os.path.join(ROOT, overlay))
    run("tools/vwf_build.py", *vwf_args)
    run("tools/dump_eboot.py", vwf_eboot, dump)
    run("tools/eboot_insert.py", "--eboot", vwf_eboot, "--dump", dump, "--out", eboot, *tr)
    if voice_subs or voice_placeholder:
        run("tools/voice_subs_patch.py", eboot, eboot)
    run("tools/insert_text.py", "--out", overlay, *tr)
    font = os.path.join("data", "extra", "gpsp3_font14.fnt")
    os.makedirs(os.path.join(ROOT, overlay, "data", "extra"), exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, vwf, font), os.path.join(ROOT, overlay, font))
    if images:
        run("tools/redraw_images.py", "--out", overlay, "--preview", os.path.join(b, "redraw"), "--no-sheets",
            "--version", version)
    if voice_subs or voice_placeholder:
        run("tools/voice_subs_at3.py", "--out", overlay, "--widths", os.path.join(vwf, "vwf_widths.json"),
            *(["--placeholder"] if voice_placeholder else voice_subs))
    run("tools/muf_archive.py", "repack", os.path.join("work", "source", "dat"), usrdir,
        "--base", os.path.join("work", "source", "iso", "PSP_GAME", "USRDIR"), "--overlay", overlay)
    run("tools/iso_patch.py", iso, out_iso,
        "PSP_GAME/SYSDIR/EBOOT.BIN=" + eboot,
        *["PSP_GAME/USRDIR/%s=%s" % (f, os.path.join(usrdir, f)) for f in ("fileset.dat", "macross.dat", "macross.idx")])
    print("built", out_iso)


if __name__ == "__main__":
    main()
