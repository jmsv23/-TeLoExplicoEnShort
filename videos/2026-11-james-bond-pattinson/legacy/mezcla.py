#!/usr/bin/env python3
"""Mezcla final: video renderizado + master.wav (voz + escenas) + música por cues con ducking + SFX alineados por pico.

    python3 mezcla.py largo        → render/largo-final.mp4
    python3 mezcla.py short        → render/short-final.mp4

Música (audio/musica/): tema-principal.wav (apertura y cierre) y tema-fondo.wav (cama bajo la narración).
Los cues se derivan del timeline: el tema arranca al terminar la escena de apertura y vuelve en el cierre
de modo que su acorde final cae al terminar el video. Ducking por sidechain contra master (voz + escenas).
SFX: sfx-<pieza>.json (build.py) · audio/sfx/picos.json → el pico de cada efecto cae en el tiempo del evento.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.argv[1] if len(sys.argv) > 1 else "largo"
VID = HERE / "render" / f"{P}-video.mp4"
MASTER = HERE / "audio" / P / "master.wav"
MUS = HERE / "audio/musica"
SFXD = HERE / "audio/sfx"
import os
OUT = Path(os.environ["MEZCLA_OUT"]) if os.environ.get("MEZCLA_OUT") else HERE / "render" / f"{P}-final.mp4"
TEMA = Path(os.environ["MEZCLA_TEMA"]) if os.environ.get("MEZCLA_TEMA") else None  # prueba de otro tema principal

# ganancia por efecto (todos normalizados a -3 dBFS de pico) y adelanto del pico respecto al evento
GAIN = {"whoosh": -21, "whoosh-rapido": -18, "golpe": -14, "sello": -15, "tick": -24, "teclas": -21}
PICO_ANTES = {"whoosh": -0.18, "whoosh-rapido": -0.12}  # el pico del whoosh cae ~0.15 s dentro de la transición


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


# El tema elegido (opción B, moderna) crece de suave a clímax: se entra a mitad de la subida
TEMA_DESDE_APERTURA = 70.0
TEMA_DESDE_SHORT = 60.0


def fin_util(p, umbral_db=-40):
    """Último instante con música por encima del umbral (descarta el silencio final del archivo)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(p), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    env = np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "same"))
    vivos = np.where(20 * np.log10(env + 1e-9) > umbral_db)[0]
    return (vivos[-1] / 8000) if len(vivos) else dur(p)


def cues():
    """[(archivo, desde_s_en_archivo, inicio_s_en_video, fin_s_en_video, fade_in, fade_out, gain_db)]"""
    total = dur(MASTER)
    tema, fondo = TEMA or (MUS / "tema-principal.wav"), MUS / "tema-fondo.wav"
    dt = fin_util(tema)
    if P == "short":
        return [(tema, TEMA_DESDE_SHORT, 0.0, total, 0.6, 2.5, -12)]
    tl = json.loads((HERE / f"timeline-{P}.json").read_text())
    sec = {s["id"]: s for s in tl["sections"]}
    apertura_fin = next(b["end"] for b in tl["beats"] if b["type"] == "clip")          # tras "Bond. James Bond."
    t_fondo = sec["noticia"]["start"] - 1.5
    t_cierre = sec["cierre"]["start"] - 1.0
    largo_cierre = total - t_cierre
    return [
        (tema, TEMA_DESDE_APERTURA, apertura_fin - 0.2, t_fondo + 2.5, 0.8, 3.0, -12),                  # apertura → título
        (fondo, 0.0, t_fondo, t_cierre + 2.0, 3.0, 3.0, -14),                           # cama de narración
        (tema, max(0.0, dt - largo_cierre), t_cierre, total, 2.0, 1.2, -14.5),            # cierre: acaba con el acorde final
    ]


def main():
    total = dur(MASTER)
    picos = json.loads((SFXD / "picos.json").read_text())
    ev = [e for e in json.loads((HERE / f"sfx-{P}.json").read_text()) if (SFXD / f"{e[1]}.wav").exists()]
    cs = cues()
    ins = ["-i", str(VID), "-i", str(MASTER)]
    fc = ["[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][key]"]
    mlab = []
    for j, (f, desde, a, b, fi, fo, g) in enumerate(cs):
        ins += ["-i", str(f)]
        k = 2 + j
        d = b - a
        ms = int(a * 1000)
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim={desde:.3f}:{desde + d:.3f},asetpts=PTS-STARTPTS,"
                  f"volume={g}dB,afade=t=in:d={fi},afade=t=out:st={max(0, d - fo):.3f}:d={fo},adelay={ms}|{ms}[m{j}]")
        mlab.append(f"[m{j}]")
    fc.append("".join(mlab) + f"amix=inputs={len(mlab)}:normalize=0:duration=longest,atrim=0:{total:.3f}[mus0]")
    fc.append("[mus0][key]sidechaincompress=threshold=0.05:ratio=4:attack=40:release=500:makeup=1[mus]")
    mix = ["[vo]", "[mus]"]
    base = 2 + len(cs)
    for i, (t, name, _) in enumerate(ev):
        ins += ["-i", str(SFXD / f"{name}.wav")]
        start = t + PICO_ANTES.get(name, 0.0) - picos.get(name, 0.0)
        ms = int(max(0.0, start) * 1000)
        fc.append(f"[{base + i}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={GAIN.get(name, -18)}dB,adelay={ms}|{ms}[s{i}]")
        mix.append(f"[s{i}]")
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"✓ {OUT} · {len(ev)} SFX · cues: " + ", ".join(f"{Path(f).stem}@{a:.1f}-{b:.1f}" for f, _, a, b, *_ in cs))


if __name__ == "__main__":
    main()
