#!/usr/bin/env python3
"""Lista única de cortes del largo → video/cortes/ (1080p30). Todos los tiempos se verificaron a 1 fps
(_hojas/verif-*.jpg y verif2-*.jpg). Las escenas con voz van normalizadas a -16 LUFS.

zoom: recorte centrado hacia arriba para sacar subtítulos quemados en la parte baja (1.0 = sin recorte).
Uso: python3 -P cortar.py [nombre ...]
"""
import subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent
SAL = AQUI / "video" / "cortes"

# nombre, fuente, inicio, fin, tipo, bloque, zoom, nota
CORTES = [
    # Nº5 Zoe Saldaña
    ("zoe-idiotas", "esc-gotg-idiotas", 0.0, 3.97, "voz", "5 Zoe", 1.55, "\"I'm gonna die surrounded by the biggest idiots in the galaxy\". 720p con subtítulo quemado: zoom 1.55 lo saca"),
    ("zoe-gamora-rostro", "esc-gotg-rescate", 133.0, 136.5, "broll", "5 Zoe", 1.0, "primer plano de Gamora en la oscuridad"),
    ("zoe-gamora-flotando", "esc-gotg-rescate", 4.0, 7.0, "broll", "5 Zoe", 1.0, "Gamora flotando en el espacio"),
    # Nº4 Natalie Portman
    ("portman-eat-my-hammer", "esc-lovethunder-mighty", 261.0, 266.0, "voz", "4 Portman", 1.0, "\"Eat my hammer!\" y el rayo"),
    ("portman-mighty-grito", "esc-lovethunder-mighty", 254.6, 258.6, "broll", "4 Portman", 1.0, "Jane grita con el martillo y lo lanza"),
    ("portman-transformacion", "esc-lovethunder-mighty", 120.5, 124.5, "broll", "4 Portman", 1.0, "el martillo llega y aparece la Poderosa Thor"),
    ("portman-cachetada-loki", "esc-thor2-cachetada", 2.4, 4.0, "voz-alt", "4 Portman", 1.0, "\"That's for New York\". Fuente meme vertical con texto: solo si se recorta la banda de película"),
    # Nº3 Zendaya
    ("zendaya-call-me-mj", "esc-homecoming-callmemj", 9.0, 12.0, "voz", "3 Zendaya", 1.0, "\"Thank you. My friends call me MJ.\" (desde 12 s hay un meme de The Office: no pasar)"),
    ("zendaya-lame-party", "esc-homecoming-mj", 0.0, 5.9, "voz", "3 Zendaya", 1.15, "\"Can't believe you're at this lame party\" / \"But you're here too\" / \"Am I?\". Subtítulo quemado: zoom"),
    # Nº2 Elizabeth Olsen
    ("olsen-took-everything", "esc-endgame-wanda", 4.5, 10.4, "voz", "2 Olsen", 1.0, "\"You took everything from me\" / \"I don't even know who you are\""),
    ("olsen-levitando", "esc-endgame-wanda", 13.0, 17.5, "broll", "2 Olsen", 1.0, "Wanda se eleva con poder rojo"),
    ("olsen-wakanda-poder", "esc-iw-wanda-wakanda", 6.0, 10.5, "broll", "2 Olsen", 1.0, "Wanda destroza a las bestias en Wakanda"),
    ("olsen-wakanda-okoye", "esc-iw-wanda-wakanda", 16.6, 22.3, "voz-alt", "2 Olsen", 1.0, "Wanda llega; Okoye: \"Why was she up there all this time?\""),
    # Nº1 Scarlett Johansson
    ("scarlett-on-hold", "esc-avengers-interrogatorio", 132.5, 140.5, "voz", "1 Scarlett", 1.22, "\"Let me put you on hold\" y se libera de la silla. Subtítulo quemado: zoom"),
    ("scarlett-interrogatorio-moron", "esc-avengers-interrogatorio", 115.5, 122.6, "voz-alt", "1 Scarlett", 1.22, "\"I'm in the middle of an interrogation. This moron is giving me everything.\" (WhisperX corre ~17 s antes aquí: tiempos por subtítulo)"),
    ("scarlett-pasillo-camina", "esc-ironman2-pasillo", 107.0, 113.0, "broll", "1 Scarlett", 1.0, "Natasha avanza por el pasillo hacia cámara"),
    ("scarlett-pasillo-desliza", "esc-ironman2-pasillo", 43.0, 46.5, "broll", "1 Scarlett", 1.0, "barrida por el piso"),
    ("scarlett-pasillo-pose", "esc-ironman2-pasillo", 24.0, 27.0, "broll", "1 Scarlett", 1.0, "pose de pelea en el pasillo"),
]


def cortar(nombre, fuente, a, b, tipo, zoom):
    vf = []
    if zoom > 1:
        # recorte centrado en x, pegado arriba en y (saca la franja baja con subtítulos)
        vf.append(f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})/2:0")
    vf += ["scale=1920:1080:force_original_aspect_ratio=increase", "crop=1920:1080", "fps=30", "setsar=1"]
    af = ["loudnorm=I=-16:TP=-1.5:LRA=11"] if tipo.startswith("voz") else []
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a}", "-to", f"{b}", "-i", str(AQUI / "video" / f"{fuente}.mp4"),
           "-vf", ",".join(vf), "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p"]
    cmd += (["-af", ",".join(af), "-c:a", "aac", "-b:a", "192k", "-ar", "48000"] if af else ["-c:a", "aac", "-b:a", "160k", "-ar", "48000"])
    cmd.append(str(SAL / f"{nombre}.mp4"))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    SAL.mkdir(parents=True, exist_ok=True)
    pedir = set(sys.argv[1:])
    for n, f, a, b, t, blq, z, nota in CORTES:
        if pedir and n not in pedir:
            continue
        cortar(n, f, a, b, t, z)
        print(f"ok {n} ({b - a:.1f}s, {t})")
