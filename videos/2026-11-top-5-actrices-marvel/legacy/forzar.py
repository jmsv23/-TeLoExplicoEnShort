"""Alineación forzada (wav2vec2 de WhisperX) del texto TTS exacto contra cada wav de bloque.

Se corre con el Python de WhisperX:
  ~/.local/share/uv/tools/whisperx/bin/python forzar.py audio/largo
Escribe <bloque>.forced.json con [[palabra, inicio, fin], ...] en el mismo orden que el texto TTS.
"""
import json, sys
from pathlib import Path

import torch
import whisperx

d = Path(sys.argv[1])
dev = "cuda" if torch.cuda.is_available() else "cpu"
model, meta = whisperx.load_align_model(language_code="es", device=dev)
for wav in sorted(d.glob("*.wav")):
    if wav.name.startswith(".") or wav.stem == "master":
        continue
    tts_file = wav.with_suffix(".tts.txt")
    if not tts_file.exists():
        continue
    out = wav.with_suffix(".forced.json")
    if out.exists() and out.stat().st_mtime > wav.stat().st_mtime and out.stat().st_mtime > tts_file.stat().st_mtime:
        continue
    text = tts_file.read_text().strip()
    audio = whisperx.load_audio(str(wav))
    dur = len(audio) / 16000
    res = whisperx.align([{"text": text, "start": 0.0, "end": dur}], model, meta, audio, dev, return_char_alignments=False)
    ws = res["word_segments"]
    toks = text.split()
    words, last = [], 0.0
    # word_segments sigue el orden del texto; las palabras sin tiempo heredan el del vecino
    for i, tok in enumerate(toks):
        w = ws[i] if i < len(ws) else {}
        s, e = w.get("start"), w.get("end")
        if s is None:
            s = last
            e = last + 0.05
        words.append([tok, round(float(s), 3), round(float(e), 3)])
        last = float(e)
    out.write_text(json.dumps({"dur": dur, "words": words}, ensure_ascii=False))
    print(f"✓ {wav.stem} {len(words)} palabras", flush=True)
