"""Transcribe the voice clips (data/sound/voice/*.at3) with a local Whisper model.

Runs in the faster-whisper venv (work/source/whisper_venv, Python 3.11, CUDA):

  work/source/whisper_venv/Scripts/python tools/voice_transcribe.py [--limit N] [--only PREFIX]

Each clip is decoded with ffmpeg (ATRAC3) to 16 kHz mono and transcribed in
Japanese. Results go to work/source/voice/transcripts.json (gitignored: it holds
Japanese), keyed by clip id (file name without .at3). The run resumes: clips
already in the file are skipped.

Per clip it stores the text, the duration, and Whisper's confidence figures
(avg_logprob, no_speech_prob, compression_ratio). `uncertain` is set when any
of them crosses the thresholds below, or the text is empty / a known
hallucination.

Hotwords (series names, mecha terms) are read from work/source/voice/hotwords.txt
when it exists, one per line.

--retry re-runs the clips whose text looks like a Whisper hallucination
(`suspicious()`: stock video-caption phrases, "episode N" lists, repeats, far
too many characters for the clip length) without the hotword prompt and with
the VAD filter on, and keeps the new text when it is not suspicious. Clips that
stay suspicious are flagged "hallucination" (usually no speech: shouts,
chanting, processed voices).
"""

import argparse
import json
import os
import subprocess
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "work", "source", "dat", "data", "sound", "voice")
OUT_DIR = os.path.join(ROOT, "work", "source", "voice")
OUT = os.path.join(OUT_DIR, "transcripts.json")
HOTWORDS = os.path.join(OUT_DIR, "hotwords.txt")

# Confidence thresholds for the `uncertain` flag
LOGPROB_MIN = -0.8
NOSPEECH_MAX = 0.6
COMPRESSION_MAX = 2.4


def add_cuda_dlls():
    """Put the pip-installed cuBLAS / cuDNN DLLs on the search path (Windows)."""
    import importlib.util
    spec = importlib.util.find_spec("nvidia")
    if not spec or not spec.submodule_search_locations:
        return
    for base in spec.submodule_search_locations:
        for sub in os.listdir(base):
            b = os.path.join(base, sub, "bin")
            if os.path.isdir(b):
                os.add_dll_directory(b)
                os.environ["PATH"] = b + os.pathsep + os.environ["PATH"]


def collapse_runs(text, keep=6):
    """Shorten a run of one repeated character (a held shout) to `keep` chars."""
    out, n, changed = [], 0, False
    for i, ch in enumerate(text):
        n = n + 1 if i and ch == text[i - 1] else 1
        if n <= keep:
            out.append(ch)
        else:
            changed = True
    return "".join(out), changed


HALLUCINATIONS = ["\u3054\u8996\u8074\u3042\u308a\u304c\u3068\u3046\u3054\u3056\u3044\u307e\u3057\u305f", "\u3054\u6e05\u8074", "\u30c1\u30e3\u30f3\u30cd\u30eb\u767b\u9332", "\u5b57\u5e55", "\u6700\u5f8c\u307e\u3067\u3054\u8996\u8074"]
HOTWORD_LEAK = 3   # this many bare hotwords as words = the prompt leaking into a clip without speech


HOT_LIST = [l.strip() for l in open(HOTWORDS, encoding="utf-8")] if os.path.exists(HOTWORDS) else []


def suspicious(text, dur):
    import re
    if not text:
        return True
    if any(h in text for h in HALLUCINATIONS):
        return True
    if re.search(r"\u7b2c\d+[\u8a71\u7ae0]", text):
        return True
    if len(text) > 4 and len(text) / max(dur, 0.3) > 16:
        return True
    if HOT_LIST and sum(1 for w in text.split() if w in HOT_LIST) >= HOTWORD_LEAK:
        return True
    words = text.split()
    if len(words) >= 4 and len(set(words)) <= len(words) // 3:
        return True
    return False


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "fatal", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        stdout=subprocess.PIPE, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--compute", default="float16")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="", help="only clips whose id starts with this")
    ap.add_argument("--beam", type=int, default=5)
    ap.add_argument("--retry", action="store_true", help="re-run suspicious clips without the prompt")
    args = ap.parse_args()

    add_cuda_dlls()
    from faster_whisper import WhisperModel

    os.makedirs(OUT_DIR, exist_ok=True)
    data = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    hot = None
    if os.path.exists(HOTWORDS):
        hot = " ".join(l.strip() for l in open(HOTWORDS, encoding="utf-8") if l.strip())

    clips = sorted(f[:-4] for f in os.listdir(VOICE) if f.lower().endswith(".at3"))
    if args.retry:
        todo = [c for c in clips if c in data and c.startswith(args.only)
                and (suspicious(data[c]["jp"], data[c]["dur"]) or "repeat" in data[c]["flags"])]
        hot = None
    else:
        todo = [c for c in clips if c not in data and c.startswith(args.only)]
    if args.limit:
        todo = todo[:args.limit]
    print("%d clips, %d done, %d to do" % (len(clips), len(data), len(todo)), flush=True)

    model = WhisperModel(args.model, device="cuda", compute_type=args.compute)
    t0 = time.time()
    for i, cid in enumerate(todo):
        audio = decode(os.path.join(VOICE, cid + ".at3"))
        dur = len(audio) / 16000.0
        segs, info = model.transcribe(
            audio, language="ja", beam_size=args.beam, vad_filter=args.retry,
            condition_on_previous_text=False, hotwords=hot, temperature=[0.0, 0.2, 0.4],
            max_new_tokens=min(300, int(dur * 20) + 12))
        segs = list(segs)
        text = "".join(s.text for s in segs).strip()
        text, collapsed = collapse_runs(text)
        lp = min((s.avg_logprob for s in segs), default=-9.0)
        ns = max((s.no_speech_prob for s in segs), default=1.0)
        cr = max((s.compression_ratio for s in segs), default=0.0)
        flags = []
        if not text:
            flags.append("empty")
        if lp < LOGPROB_MIN:
            flags.append("logprob")
        if ns > NOSPEECH_MAX:
            flags.append("nospeech")
        if cr > COMPRESSION_MAX or collapsed:
            flags.append("repeat")
        if args.retry:
            old = data[cid]
            if suspicious(text, dur):
                flags = sorted(set(old["flags"]) | {"hallucination"})
                text, lp, ns, cr = old["jp"], old["logprob"], old["nospeech"], old["compression"]
            else:
                flags.append("retried")
        data[cid] = {"jp": text, "dur": round(dur, 2), "logprob": round(lp, 3),
                     "nospeech": round(ns, 3), "compression": round(cr, 2),
                     "uncertain": bool(set(flags) - {"retried"}), "flags": flags}
        if args.limit and args.limit <= 50:
            sys.stdout.buffer.write(("%s %.1fs %s %s\n" % (cid, dur, text, flags)).encode("utf-8"))
            sys.stdout.flush()
        if (i + 1) % 200 == 0:
            json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
            el = time.time() - t0
            print("%d/%d  %.0fs  eta %.0f min" % (i + 1, len(todo), el, el / (i + 1) * (len(todo) - i - 1) / 60), flush=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("done in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
