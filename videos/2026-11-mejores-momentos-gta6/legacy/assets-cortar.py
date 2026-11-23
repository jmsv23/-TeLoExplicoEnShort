#!/usr/bin/env python3
"""Corta los momentos elegidos de videos/ a assets/video/cortes/<nombre>.mp4 (1920x1080, 30 fps, con audio)."""
import subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parent.parent
V = {"01": "01_es_streamers_6wA7C9ooKUc", "02": "02_en_streamers_xrWAL5ZhFiQ", "03": "03_en_launch_uSgJ0C6eViI",
     "04": "04_rubius_ndt7erSfBhw", "05": "05_caseoh_1UYqV49-L5Y"}
CORTES = {  # nombre: (video, inicio, fin)
    "illo-borra": ("01", 80.0, 120.6), "rubius-psico": ("01", 489.5, 519.0), "rubius-salto": ("04", 979.0, 1006.0),
    "papa-gas": ("02", 497.0, 513.5), "kai-techo": ("03", 202.0, 220.5), "speed-robo": ("02", 116.0, 137.0),
    "willy-coco": ("01", 131.5, 172.5), "rubius-bigfoot": ("04", 458.5, 486.0), "lirik-perro": ("02", 235.5, 263.0),
    "peanut-puerta": ("03", 167.5, 199.5), "vanoss-gaviota": ("03", 259.0, 284.0), "caseoh-dolores": ("05", 279.0, 308.5),
    # Shorts
    "illo-borra-s": ("01", 101.0, 120.6), "kai-techo-s": ("03", 206.5, 219.5), "papa-gas-s": ("02", 504.5, 513.5),
    "willy-coco-s": ("01", 140.5, 158.5),
}
out = P / "assets/video/cortes"
for n, (v, a, b) in CORTES.items():
    if len(sys.argv) > 1 and n not in sys.argv[1:]:
        continue
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{a}", "-i", str(P / "videos" / f"{V[v]}.mp4"), "-t", f"{b - a}",
                    "-vf", "scale=1920:1080,fps=30", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out / f"{n}.mp4")], check=True)
    print("✓", n, round(b - a, 1))
