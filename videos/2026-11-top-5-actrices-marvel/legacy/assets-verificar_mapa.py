#!/usr/bin/env python3
"""Hoja de verificación de un mapa de Gemini: una fila por destacado, 1 fps, ±3 s de margen.

Uso: python3 verificar_mapa.py esc-goldeneye-tanque   → _hojas/verif-<video>.jpg
Se revisa a ojo antes de pasar un destacado a cortar.py (Gemini puede fallar un destacado por ~10 s).
"""
import json, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).parent
MARGEN, ANCHO = 3, 200


def main():
    nombre = sys.argv[1]
    mapa = json.loads((AQUI / "_mapas" / f"{nombre}.json").read_text())
    video = AQUI / "video" / f"{nombre}.mp4"
    filas = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, h in enumerate(mapa["destacados"]):
            ini = max(0, int(h["inicio_s"]) - MARGEN)
            n = int(h["fin_s"] + MARGEN) - ini + 1
            etiqueta = f"#{i + 1} {h['titulo']} ({h['inicio']}-{h['fin']})".replace(":", "\\:").replace("'", "")
            fila = Path(tmp) / f"f{i:02d}.jpg"
            vf = (f"fps=1,scale={ANCHO}:-2,drawtext=text='%{{eif\\:{ini}+t\\:d}}s':x=4:y=4:fontsize=16:"
                  f"fontcolor=yellow:box=1:boxcolor=black@0.7,tile={n}x1,pad=iw:ih+26:0:26,"
                  f"drawtext=text='{etiqueta}':x=6:y=4:fontsize=18:fontcolor=white")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(ini), "-t", str(n), "-i", str(video),
                            "-vf", vf, "-frames:v", "1", str(fila)], check=True)
            filas.append(fila)
        out = AQUI / "_hojas" / f"verif-{nombre}.jpg"
        out.parent.mkdir(exist_ok=True)
        ins = sum((["-i", str(f)] for f in filas), [])
        w = max(int(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout) for f in filas)
        pads = "".join(f"[{i}]pad={w}:ih:0:0:black[p{i}];" for i in range(len(filas)))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex",
                        pads + "".join(f"[p{i}]" for i in range(len(filas))) + f"vstack={len(filas)}",
                        str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
