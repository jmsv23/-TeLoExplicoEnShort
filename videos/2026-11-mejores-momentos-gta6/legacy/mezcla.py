#!/usr/bin/env python3
"""Mezcla final: video renderizado + master.wav (voz + escenas) + música por cues con ducking + SFX alineados por pico.

    python3 mezcla.py largo        → render/largo-final.mp4
    python3 mezcla.py short        → render/short-final.mp4

Música (audio/musica/). PROVISIONAL hasta que el usuario elija: tema = opcion-A-runway.wav, cama = A-fondo.wav.
Para probar otra: MEZCLA_TEMA=audio/musica/opcion-B-glam.wav MEZCLA_OUT=render/short-B.mp4 python3 mezcla.py short
  - Short: el tema completo bajo la voz.
  - Largo: el tema en el hook y las reglas, la cama bajo los cinco puestos, y el tema vuelve en el cierre de modo que
    su acorde final cae al terminar el video.
Ducking por sidechain contra master (voz + escenas). SFX: sfx-<pieza>.json (build.py) + audio/sfx/picos.json.
"""
import json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = sys.argv[1] if len(sys.argv) > 1 else "largo"
VID = HERE / "render" / f"{P}-video.mp4"
MASTER = HERE / "audio" / P / "master.wav"
MUS = HERE / "audio/musica"
SFXD = HERE / "audio/sfx"
OUT = Path(os.environ["MEZCLA_OUT"]) if os.environ.get("MEZCLA_OUT") else HERE / "render" / f"{P}-final.mp4"
TEMA = Path(os.environ["MEZCLA_TEMA"]) if os.environ.get("MEZCLA_TEMA") else MUS / "opcion-A-synthwave.wav"
FONDO = Path(os.environ["MEZCLA_FONDO"]) if os.environ.get("MEZCLA_FONDO") else MUS / "fondo-loop.wav"

GAIN = {"whoosh": -22, "golpe": -15, "obturador": -12, "papel": -16, "lapiz": -20}
PICO_ANTES = {"whoosh": -0.18}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def fin_util(p, umbral_db=-40):
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
    dt = fin_util(TEMA)
    if P != "largo":
        desde = max(0.0, dt - total - 0.5)  # que el final del tema coincida con el final del Short
        return [(TEMA, desde, 0.0, total, 0.3, 1.5, -11)]
    tl = json.loads((HERE / f"timeline-{P}.json").read_text())
    sec = {s["id"]: s for s in tl["sections"]}
    t_fondo = sec["n12"]["start"] - 0.5
    t_cierre = sec["cierre"]["start"] - 1.0
    largo_cierre = total - t_cierre
    return [
        (TEMA, 0.0, 0.0, t_fondo + 2.5, 0.4, 3.0, -12),
        (FONDO, 0.0, t_fondo, t_cierre + 2.0, 3.0, 3.0, -17),
        (TEMA, max(0.0, dt - largo_cierre), t_cierre, total, 2.0, 1.2, -12.5),
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
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[pre]")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # loudnorm en dos pasadas (lineal): ganancia constante, sin bombeo entre voz y escenas
    medir = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *ins, "-filter_complex",
                            ";".join(fc) + ";[pre]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]", "-map", "[a]", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    m = json.loads(medir[medir.rindex("{"):medir.rindex("}") + 1])
    fc.append(f"[pre]loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}[a]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", str(OUT)]
    subprocess.run(cmd, check=True)
    print(f"✓ {OUT} · {len(ev)} SFX · cues: " + ", ".join(f"{Path(f).stem}@{a:.1f}-{b:.1f}" for f, _, a, b, *_ in cs))


if __name__ == "__main__":
    main()
