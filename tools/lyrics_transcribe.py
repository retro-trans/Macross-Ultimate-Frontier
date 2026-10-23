"""Draft private timed lyrics from the user's local game audio with Whisper.

Run in work/source/whisper_venv. The default is a read-only plan; --write
transcribes Japanese and translates to English. Raw results stay in the
gitignored work/source/lyrics directory. Existing populated lyric templates
are never overwritten. Use --export-only to export an already cached run.
All generated lines require review; song recognition and timing are imperfect.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lyrics

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "work/source/lyrics"


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def draft_lines(segments, duration):
    """Fit complete segments into the box, retaining all recognized words."""
    rows = []
    for number, segment in enumerate(segments):
        text = segment["text"].strip()
        if not text or segment["no_speech_prob"] > 0.95:
            continue
        if re.search(r"(.)\1{12,}", text, re.IGNORECASE):
            continue
        if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", text):
            print("Withheld untranslated segment %d; see cached result" % number, flush=True)
            continue
        if re.fullmatch(r"[\W_]*(?:(?:la|na|ah|oh|aa)[\W_]*){8,}", text, re.IGNORECASE):
            continue
        if any(phrase in text.lower() for phrase in
               ["thank you for watching", "thanks for watching", "please subscribe", "subtitles by",
                "translated by", "translation by", "subbed by", "instagram", "twitter", "sound hodori"]):
            continue
        start, end = max(0.0, segment["start"]), min(duration, segment["end"])
        if end <= start:
            continue
        words = text.split()
        if any(lyrics.width(word) > lyrics.BOX_W for word in words):
            print("Withheld unrenderable segment %d; see cached result" % number, flush=True)
            continue
        chunks, chunk = [], []
        for word in words:
            candidate = " ".join(chunk + [word])
            if chunk and len(lyrics.wrap(candidate)) > 2:
                chunks.append(chunk)
                chunk = []
            chunk.append(word)
        if chunk:
            chunks.append(chunk)
        total = sum(len(" ".join(c)) for c in chunks)
        used = 0
        for chunk in chunks:
            chunk_text = " ".join(chunk)
            a = start + (end - start) * used / total
            used += len(chunk_text)
            b = start + (end - start) * used / total
            rows.append({"start_sec": round(a, 3), "end_sec": round(b, 3),
                         "text": chunk_text, "review_required": True,
                         "source_segment": number,
                         "notes": "Whisper translation draft; check words and sung timing."})
    for index, row in enumerate(rows[:-1]):
        row["end_sec"] = min(row["end_sec"], rows[index + 1]["start_sec"])
    return [row for row in rows if row["end_sec"] > row["start_sec"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=Path(lyrics.LYRICS_DIR))
    parser.add_argument("--widths", default=lyrics.WIDTHS)
    parser.add_argument("--only", default="")
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--export-only", action="store_true")
    args = parser.parse_args()
    jobs = []
    for path in sorted(args.dir.glob("bgm*.json")):
        doc = json.loads(path.read_text(encoding="utf-8-sig"))
        sid = path.stem
        if args.only and sid not in args.only.split(","):
            continue
        if doc.get("lines") or doc.get("same_as") or doc.get("review_status", "").startswith("Withheld:"):
            continue
        audio_path = Path(lyrics.BGM_DIR) / (sid + ".at3")
        if not audio_path.is_file():
            raise FileNotFoundError(audio_path)
        print(sid, doc.get("title", ""), "-> local draft", flush=True)
        jobs.append((path, doc, audio_path))
    print("%d unique songs; %s" % (len(jobs), "writing private drafts" if args.write else "plan only; use --write"), flush=True)
    if not args.write:
        return
    lyrics.load_widths(args.widths)
    model = None
    start_time = time.time()
    for index, (path, doc, audio_path) in enumerate(jobs):
        sid = path.stem
        cache_path = CACHE / (sid + ".json")
        source_hash = hashlib.sha256(audio_path.read_bytes()).hexdigest()
        result = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
        if result and (result.get("audio_sha256") != source_hash or result.get("model") != args.model):
            raise ValueError("Cached model/audio differs for " + sid)
        result.update(song_id=sid, audio_sha256=source_hash, model=args.model,
                      source="User-supplied local game audio; machine draft, not verified lyrics.")
        for task in ["transcribe", "translate"]:
            if task in result:
                continue
            if args.export_only:
                raise ValueError("Missing cached " + task + " for " + sid)
            if model is None:
                from voice_transcribe import add_cuda_dlls
                add_cuda_dlls()
                from faster_whisper import WhisperModel
                model = WhisperModel(args.model, device="cuda", compute_type="int8_float16", local_files_only=True)
            from voice_transcribe import decode
            audio = decode(str(audio_path))
            segments, info = model.transcribe(
                audio, language="ja", task=task, beam_size=5,
                vad_filter=False, condition_on_previous_text=False,
                temperature=[0.0, 0.2, 0.4], word_timestamps=False,
                max_new_tokens=224)
            values = []
            for segment in segments:
                values.append({"start": segment.start, "end": segment.end,
                               "text": segment.text.strip(),
                               "avg_logprob": segment.avg_logprob,
                               "no_speech_prob": segment.no_speech_prob,
                               "compression_ratio": segment.compression_ratio})
            result[task] = values
            save_json(cache_path, result)
            print("%s %s: %d segments (%.0fs elapsed)" % (sid, task, len(values), time.time() - start_time), flush=True)
        rows = draft_lines(result["translate"], float(doc["duration_sec"]))
        draft = dict(doc, lines=rows, review_required=True,
                     provenance={"method": "Whisper %s Japanese transcription and English translation" % args.model,
                                 "source_audio_sha256": source_hash,
                                 "raw_result": str(cache_path.relative_to(ROOT)).replace("\\", "/"),
                                 "timing": "Whisper segment estimates; long captions split proportionally"})
        errors, warnings = [], []
        lyrics.check_doc(draft, sid, errors, warnings)
        if errors or warnings:
            raise ValueError("Invalid draft for %s: %s" % (sid, errors + warnings))
        save_json(path, draft)
        print("[%d/%d] %s: %d English captions, review required" % (index + 1, len(jobs), sid, len(rows)), flush=True)


if __name__ == "__main__":
    main()
