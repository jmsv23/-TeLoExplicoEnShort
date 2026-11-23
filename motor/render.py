"""Render con HyperFrames (entero o por partes), hoja de contacto a 1 fps y ensamblado del final.

Los largos se pueden renderizar por partes (piezas[].partes en video.json = secciones por parte): cada parte
es su propio proyecto hf-<pieza>-p<a>, se renderiza aparte y se une sin recodificar.
"""
import json
import math
import os
import subprocess
from pathlib import Path

from . import build as B
from .mezcla import mezclar
from .proyecto import CONFIG, ROOT, die
from .voz import dur


def npx_render(hf, out, workers=None, draft=False):
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["npx", "--yes", f"hyperframes@{CONFIG['hyperframes']}", "render", "-o", str(out), "--skill", "hyperframes",
           "--workers", str(workers or CONFIG["workers"])]
    if draft:
        cmd += ["--quality", "draft"]
    r = subprocess.run(cmd, cwd=hf, capture_output=True, text=True)
    if r.returncode or not out.exists():
        die(f"render falló en {hf.name}:\n{(r.stdout + r.stderr)[-2500:]}")
    print(f"  ✓ {out.name} ({dur(out):.1f} s)")


def lint(hf):
    r = subprocess.run(["npx", "--yes", f"hyperframes@{CONFIG['hyperframes']}", "lint"], cwd=hf, capture_output=True, text=True)
    txt = (r.stdout + r.stderr).strip()
    return r.returncode == 0, txt[-1500:]


def render(v, pieza, workers=None, draft=False):
    """build + render (+ partes) + mezcla → build/render/<pieza>-final.mp4"""
    rd = v.build / "render"
    mudo = rd / f"{pieza}-video{'.draft' if draft else ''}.mp4"
    k = v.pieza(pieza).get("partes")
    hf, nsec = B.build(v, pieza)
    if k and nsec > k:
        trozos = []
        for a in range(0, nsec, k):
            hfp, _ = B.build(v, pieza, (a, min(a + k, nsec)))
            out = rd / f"{pieza}-p{a}.mp4"
            npx_render(hfp, out, workers, draft)
            trozos.append(out)
        lst = rd / f".{pieza}-partes.txt"
        lst.write_text("".join(f"file '{p.resolve()}'\n" for p in trozos))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(mudo)],
                       check=True)
    else:
        npx_render(hf, mudo, workers, draft)
    E = B.cargar_estilo(v, pieza, hf)
    final = rd / f"{pieza}-final{'.draft' if draft else ''}.mp4"
    mezclar(v, pieza, E, mudo, final)
    return final


def hoja(video, salida, cada=1.0, ancho=320, cols=10):
    """Hoja de contacto: 1 frame cada `cada` s (por defecto 1 fps, el máximo que usamos para revisar)."""
    d = dur(video)
    n = max(1, int(d / cada))
    filas = math.ceil(n / cols)
    salida.parent.mkdir(parents=True, exist_ok=True)
    vf = (f"fps=1/{cada},scale={ancho}:-2,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{filas}")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-vf", vf, "-frames:v", "1", "-q:v", "4", str(salida)],
                   check=True)
    print(f"✓ hoja {salida.relative_to(ROOT)} ({n} frames)")
    return salida


def loudness(video):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    j = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    try:
        x = json.loads(j)
        return float(x["input_i"]), float(x["input_tp"])
    except (ValueError, KeyError):
        return None, None


# HyperFrames no corre desde un ~/.cache escribible por el grupo: caché privada (700) definida en config.json
_cache = Path(CONFIG.get("hyperframes_cache", "~/.local/share/hyperframes-cache")).expanduser()
_cache.mkdir(parents=True, exist_ok=True)
_cache.chmod(0o700)
os.environ.setdefault("HYPERFRAMES_CACHE_DIR", str(_cache))
