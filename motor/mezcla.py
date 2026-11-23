"""Mezcla final: video renderizado + master.wav (voz + escenas) + música por cues con ducking + SFX alineados por pico.

Música: video.json → "musica" (archivos en audio-lib/musica/). Plan por defecto:
  largo  tema (apertura) → cama de fondo bajo la narración → tema de cierre cuyo final cae al terminar el video
  short  tema completo, alineado para que su final coincida con el final del Short
Claves (todas opcionales salvo los archivos):
  "musica": {"tema": "x.wav", "fondo": "y.wav",
             "largo": {"fondo_desde": "<id sección>", "fondo_offset": -1.0, "cierre": "cierre", "cierre_offset": -1.0,
                       "tema_entra": "inicio" | "tras_primer_clip", "tema_desde": 0.0,
                       "gain_tema": -12, "gain_fondo": -15, "gain_cierre": -12.5},
             "short": {"tema_desde": "final" | <segundos>, "gain": -11, "fade_in": 0.3, "fade_out": 1.5}}
SFX: build/sfx-<pieza>.json (lo escribe build) · audio-lib/sfx/<efecto>.wav · audio-lib/sfx/picos.json.
"""
import json
import subprocess

import numpy as np

from .proyecto import CONFIG, ROOT, die
from .voz import dur

MUS = ROOT / "audio-lib/musica"
SFXD = ROOT / "audio-lib/sfx"


def fin_util(p, umbral_db=-40):
    """Último instante con sonido del archivo (para que el acorde final caiga al terminar el video)."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(p), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    env = np.sqrt(np.convolve(x ** 2, np.ones(800) / 800, "same"))
    vivos = np.where(20 * np.log10(env + 1e-9) > umbral_db)[0]
    return (vivos[-1] / 8000) if len(vivos) else dur(p)


def cues(v, pieza, total):
    """[(archivo, desde_s_en_archivo, inicio_s_en_video, fin_s_en_video, fade_in, fade_out, gain_db)]"""
    m = v.meta.get("musica") or {}
    if not m.get("tema"):
        return []
    tema = MUS / m["tema"]
    if not tema.exists():
        die(f"falta la música {tema.relative_to(ROOT)} (ver audio-lib/musica/PROMPTS.md para regenerarla)")
    dt = fin_util(tema)
    if v.vertical(pieza):
        c = m.get("short", {})
        desde = c.get("tema_desde", "final")
        desde = max(0.0, dt - total - 0.5) if desde == "final" else float(desde)
        return [(tema, desde, 0.0, total, c.get("fade_in", 0.3), c.get("fade_out", 1.5), c.get("gain", -11))]
    c = m.get("largo", {})
    tl = json.loads((v.build / f"timeline-{pieza}.json").read_text())
    sec = {s["id"]: s for s in tl["sections"]}
    ids = [s["id"] for s in tl["sections"]]
    fd = c.get("fondo_desde", ids[1] if len(ids) > 1 else ids[0])
    t_fondo = sec[fd]["start"] + c.get("fondo_offset", -1.0)
    ci = c.get("cierre", "cierre" if "cierre" in sec else ids[-1])
    t_cierre = sec[ci]["start"] + c.get("cierre_offset", -1.0)
    largo_cierre = total - t_cierre
    t_tema = 0.0
    if c.get("tema_entra") == "tras_primer_clip":
        t_tema = next(b["end"] for b in tl["beats"] if b["type"] == "clip") - 0.2
    out = [(tema, c.get("tema_desde", 0.0), t_tema, t_fondo + 2.5, 0.4 if t_tema == 0 else 0.8, 3.0, c.get("gain_tema", -12))]
    if m.get("fondo"):
        fondo = MUS / m["fondo"]
        if not fondo.exists():
            die(f"falta la música {fondo.relative_to(ROOT)}")
        out.append((fondo, 0.0, t_fondo, t_cierre + 2.0, 3.0, 3.0, c.get("gain_fondo", -15)))
    out.append((tema, max(0.0, dt - largo_cierre), t_cierre, total, 2.0, 1.2, c.get("gain_cierre", -12.5)))
    return out


def mezclar(v, pieza, E, video_mudo, salida):
    master = v.build / "audio" / pieza / "master.wav"
    total = dur(master)
    picos = json.loads((SFXD / "picos.json").read_text())
    sfx_file = v.build / f"sfx-{pieza}.json"
    ev_all = json.loads(sfx_file.read_text()) if sfx_file.exists() else []
    ev = [e for e in ev_all if (SFXD / f"{e[1]}.wav").exists()]
    faltan = sorted({e[1] for e in ev_all} - {e[1] for e in ev})
    if faltan:
        print(f"  ⚠ SFX sin archivo en audio-lib/sfx/: {', '.join(faltan)}")
    gain, pico_antes = getattr(E, "SFX_GAIN", {}), getattr(E, "PICO_ANTES", {})
    cs = cues(v, pieza, total)
    ins = ["-i", str(video_mudo), "-i", str(master)]
    fc = ["[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][key]"]
    mix = ["[vo]"]
    if cs:
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
        mix.append("[mus]")
    else:
        fc[0] = "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[vo]"
    base = 2 + len(cs)
    for i, (t, name, _) in enumerate(ev):
        ins += ["-i", str(SFXD / f"{name}.wav")]
        start = t + pico_antes.get(name, 0.0) - picos.get(name, 0.0)
        ms = int(max(0.0, start) * 1000)
        fc.append(f"[{base + i}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain.get(name, -18)}dB,adelay={ms}|{ms}[s{i}]")
        mix.append(f"[s{i}]")
    ln = CONFIG["loudness"]
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I={ln['I']}:TP={ln['TP']}:LRA={ln['LRA']}[a]")
    if salida.exists():
        salida.unlink()  # entrega/ tiene un hardlink al final: no pisar la versión ya entregada
    cmd = ["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", str(salida)]
    subprocess.run(cmd, check=True)
    print(f"✓ {salida.name} · {len(ev)} SFX · " + (", ".join(f"{f.stem}@{a:.1f}-{b:.1f}" for f, _, a, b, *_ in cs) or "sin música"))
