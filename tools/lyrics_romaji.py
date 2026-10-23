"""Add draft romaji above private English lyric captions (plan only by default).

Run with work/source/whisper_venv/Scripts/python.exe; requires fugashi,
unidic-lite and pykakasi. --write saves an English-only backup before editing.
Cached ASR words are aligned by their existing segment times. Word placement
inside a segment remains approximate. No lyrics are fetched or stored in code.
"""

import argparse
import copy
import json
from pathlib import Path
import re
import shutil
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lyrics
from lyrics_transcribe import save_json

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
JP_RUN = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]+")
NOISE = ["instagram", "twitter", "hodori", "translated by", "translation by",
         "subtitles", "subbed by", "thank you for watching",
         "\u3054\u8996\u8074", "\u4f5c\u8a5e", "\u4f5c\u66f2", "\u7de8\u66f2"]


def usable_japanese(text):
    return (bool(CJK.search(text)) and not re.search(r"(.)\1{10,}", text)
            and not any(word in text.lower() for word in NOISE))


class Romanizer:
    def __init__(self):
        from fugashi import Tagger
        from pykakasi import kakasi
        self.tagger = Tagger()
        self.kakasi = kakasi()

    def __call__(self, text):
        def convert(match):
            groups = []
            prefix = False
            for token in self.tagger(match.group()):
                reading = token.feature.kana or token.surface
                if token.surface == '\u79c1':
                    reading = '\u30ef\u30bf\u30b7'
                if token.feature.pos1 == '\u52a9\u8a5e':
                    reading = {'\u306f': '\u30ef', '\u3078': '\u30a8', '\u3092': '\u30aa'}.get(token.surface, reading)
                # Convert conjugated forms together: a terminal small tsu
                # needs the next consonant (mat + te -> matte, not matsu te).
                attach = (groups and (prefix or groups[-1].endswith('\u30c3')
                          or token.feature.pos1 in ('\u52a9\u52d5\u8a5e', '\u63a5\u5c3e\u8f9e')
                          or token.surface in ('\u3066', '\u3067')))
                if attach:
                    groups[-1] += reading
                else:
                    groups.append(reading)
                prefix = token.feature.pos1 == '\u63a5\u982d\u8f9e'
            pieces = [''.join(p['hepburn'] for p in self.kakasi.convert(reading)) for reading in groups]
            return ' ' + ' '.join(pieces) + ' '
        result = JP_RUN.sub(convert, text)
        result = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore').decode('ascii')
        return ' '.join(result.split())


def source_task(rows, raw):
    def score(task):
        hits = 0
        for row in rows:
            index = row.get('source_segment', -1)
            if 0 <= index < len(raw[task]):
                seg = raw[task][index]
                hits += (row['start_sec'] >= seg['start'] - 0.05
                         and row['end_sec'] <= seg['end'] + 0.05)
        return hits
    return max(['translate', 'transcribe'], key=score)


def assign_romaji(rows, raw, romanizer):
    task = source_task(rows, raw)
    assigned = [[] for _ in rows]
    references = [set() for _ in rows]
    sources = list(enumerate(raw['transcribe']))
    sources += [('extra:%d' % i, seg) for i, seg in enumerate(raw.get('romaji_additions', []))]
    for index, seg in sorted(sources, key=lambda item: item[1]['start']):
        if not usable_japanese(seg['text']):
            continue
        eligible = [i for i, row in enumerate(rows)
                    if (task != 'transcribe' or row.get('source_segment') == index)
                    and row['end_sec'] > seg['start'] - 0.5
                    and row['start_sec'] < seg['end'] + 0.5]
        if not eligible:
            continue
        words = romanizer(seg['text']).split()
        total = sum(len(word) for word in words)
        used = 0
        for word in words:
            middle = seg['start'] + (seg['end'] - seg['start']) * (used + len(word) / 2) / total
            used += len(word)
            def distance(i):
                row = rows[i]
                return max(row['start_sec'] - middle, middle - row['end_sec'], 0)
            target = min(eligible, key=distance)
            if task == 'transcribe' or distance(target) <= 2.0:
                assigned[target].append(word)
                references[target].add(index)
    # Some translation segments include a Japanese prefix even when the
    # separate transcription failed. Use that prefix only where ASR is absent.
    for index, seg in enumerate(raw['translate']):
        targets = [i for i, row in enumerate(rows)
                   if task == 'translate' and row.get('source_segment') == index]
        if not targets or any(assigned[i] for i in targets):
            continue
        match = re.match(r'^[^A-Za-z]+', seg['text'])
        prefix = match.group().strip() if match else ''
        if not usable_japanese(prefix):
            continue
        parts = split_words(romanizer(prefix).split(), len(targets))
        for target, words in zip(targets, parts):
            assigned[target] = words.split()
            references[target].add('translation-prefix:%d' % index)
    return task, [' '.join(words) for words in assigned], [sorted(refs, key=str) for refs in references]


def split_words(words, count):
    if not words:
        return [''] * count
    if count > len(words):
        return [' '.join(words)] * count
    return [' '.join(words[i * len(words) // count:(i + 1) * len(words) // count])
            for i in range(count)]


def paired_captions(english, romaji):
    en_words, ro_words = english.split(), romaji.split()
    for count in range(1, max(len(en_words), len(ro_words)) + 1):
        pairs = list(zip(split_words(en_words, count), split_words(ro_words, count)))
        texts = ['\n'.join(value for value in [ro, en] if value) for en, ro in pairs]
        if all(len(lyrics.wrap(text)) <= lyrics.MAX_LINES
               and all(lyrics.width(line) <= lyrics.BOX_W for line in lyrics.wrap(text)) for text in texts):
            return pairs
    raise ValueError('Caption contains a word that cannot fit the lyric box')


def convert_doc(doc, raw, romanizer):
    before = doc['lines']
    task, readings, references = assign_romaji(before, raw, romanizer)
    rows = []
    for index, (old, romaji, refs) in enumerate(zip(before, readings, references)):
        english = ' '.join(old['text'].split())
        pairs = paired_captions(english, romaji)
        for part, (en, ro) in enumerate(pairs):
            row = copy.deepcopy(old)
            row.update(start_sec=round(old['start_sec'] + (old['end_sec'] - old['start_sec']) * part / len(pairs), 3),
                       end_sec=round(old['start_sec'] + (old['end_sec'] - old['start_sec']) * (part + 1) / len(pairs), 3),
                       text='\n'.join(value for value in [ro, en] if value),
                       en=en, romaji=ro, original_caption=index,
                       romaji_source=refs, romaji_review_required=bool(ro))
            row['notes'] = old.get('notes', '') + ' Romaji is derived from ASR; word timing and readings need review.'
            if row['end_sec'] <= row['start_sec']:
                raise ValueError('Caption interval is too short to split')
            rows.append(row)
    result = copy.deepcopy(doc)
    result['lines'] = rows
    result['provenance']['romaji'] = {
        'method': 'fugashi / UniDic-lite readings and pykakasi Hepburn; ASCII long vowels',
        'source_task': task,
        'alignment': 'ASR segment times; proportional word placement and caption splitting',
        'display': 'romaji above English, at most three rows',
        'review_required': True}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', type=Path, default=Path(lyrics.LYRICS_DIR))
    parser.add_argument('--source-dir', type=Path, default=ROOT / 'work/source/lyrics')
    parser.add_argument('--backup', type=Path, default=ROOT / 'work/source/lyrics/english_only_v0.7.14')
    parser.add_argument('--supplements', type=Path, default=ROOT / 'work/source/lyrics/romaji_sources.json')
    parser.add_argument('--widths', default=lyrics.WIDTHS)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    lyrics.load_widths(args.widths)
    romanizer = Romanizer()
    supplements = json.loads(args.supplements.read_text(encoding='utf-8')) if args.supplements.exists() else {}
    pending, report = [], []
    for path in sorted(args.dir.glob('bgm*.json')):
        backup = args.backup / path.name
        doc = json.loads((backup if backup.exists() else path).read_text(encoding='utf-8'))
        if not doc.get('lines'):
            continue
        if any('romaji' in row for row in doc['lines']):
            raise ValueError('English-only backup required for ' + path.name)
        raw = json.loads((args.source_dir / path.name).read_text(encoding='utf-8'))
        supplement = supplements.get(path.stem, {})
        for index, replacement in supplement.get('replace', {}).items():
            raw['transcribe'][int(index)].update(replacement)
        raw['romaji_additions'] = supplement.get('add', [])
        new = convert_doc(doc, raw, romanizer)
        errors, warnings = [], []
        lyrics.check_doc(new, path.stem, errors, warnings)
        if errors or warnings:
            raise ValueError((path.stem, errors, warnings))
        stat = {'song_id': path.stem, 'old_captions': len(doc['lines']), 'captions': len(new['lines']),
                'with_romaji': sum(bool(row['romaji']) for row in new['lines']),
                'original_captions_with_romaji': len({row['original_caption'] for row in new['lines'] if row['romaji']})}
        print(json.dumps(stat), flush=True)
        report.append(stat)
        pending.append((path, backup, new))
    print('%d distinct recordings; %s' % (len(pending), 'writing private drafts' if args.write else 'plan only'), flush=True)
    if args.write:
        # Save every original, including duplicate and withheld templates.
        args.backup.mkdir(parents=True, exist_ok=True)
        for path in args.dir.glob('bgm*.json'):
            backup = args.backup / path.name
            if not backup.exists():
                shutil.copy2(path, backup)
        for path, _, new in pending:
            save_json(path, new)
        save_json(args.source_dir / 'romaji_report.json', report)


if __name__ == '__main__':
    main()
