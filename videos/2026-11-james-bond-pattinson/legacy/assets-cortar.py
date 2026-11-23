#!/usr/bin/env python3
"""Corta las escenas y el b-roll del video largo desde assets/video/ a assets/video/cortes/.

Escenas "voz" (con sonido): 1080p H.264 + AAC, normalizadas a -16 LUFS.
B-roll: igual pero se usan mudas en la composición.
Uso: python3 cortar.py            (todas)
     python3 cortar.py drno-bond  (solo las que contengan ese texto)
"""
import subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent
SRC, OUT = AQUI / "video", AQUI / "video" / "cortes"

# (nombre, archivo fuente, inicio, fin, tipo, bloque del guion, nota)
CORTES = [
    # --- ESCENAS CON SONIDO (primarias, ~40 s en total) ---
    ("connery-bond-james-bond", "esc-drno-bond-james-bond", 84.6, 89.6, "voz", "3 Connery", '"Bond. James Bond." El origen.'),
    ("lazenby-other-fella", "esc-ohmss-other-fellow", 235.8, 239.9, "voz", "4 Lazenby", '"This never happened to the other fella" a cámara.'),
    ("moore-anders", "esc-moore-frases", 20.0, 23.4, "voz", "5 Moore", '"I didn\'t recognize you with the clothes on": su humor.'),
    ("dalton-bond-james-bond", "esc-tld-apertura", 192.4, 195.2, "voz", "6 Dalton", 'Su debut: "Bond, James Bond."'),
    ("brosnan-corbata", "esc-goldeneye-tanque", 84.0, 89.8, "voz", "7 Brosnan (a favor)", "El tanque rompe el muro y Bond se acomoda la corbata (verificado; mapa Gemini v3)."),
    ("brosnan-auto-invisible", "esc-dad-lago-auto-invisible", 38.0, 46.0, "voz", "7 Brosnan (contra)", "El auto invisible aparece."),
    ("craig-shaken", "esc-casino-shaken", 0.4, 3.6, "voz", "8 Craig", '"Shaken or stirred?" "Do I look like I give a damn?"'),
    ("pattinson-vengeance", "esc-batman-vengeance", 56.8, 61.0, "voz", "10 El patrón", '"I\'m vengeance."'),
    ("pattinson-spider-monkey", "esc-twilight-spider-monkey", 481.6, 484.6, "voz", "10 El patrón", '"Hold on tight, spider monkey."'),
    # --- ESCENAS CON SONIDO (alternativas) ---
    ("connery-laser", "esc-goldfinger-laser", 116.6, 122.3, "voz-alt", "3 Connery", '"Do you expect me to talk?" "No, Mr. Bond, I expect you to die."'),
    ("lazenby-all-the-time", "esc-ohmss-boda-final", 286.6, 290.8, "voz-alt", "4 Lazenby", '"We have all the time in the world": el final triste.'),
    ("moore-jaws", "esc-moore-frases", 68.4, 77.2, "voz-alt", "5 Moore", '"His name\'s Jaws. He kills people."'),
    ("brosnan-surf", "esc-dad-surf", 48.0, 58.0, "voz-alt", "7 Brosnan (contra)", "El surf con efectos digitales."),
    # --- B-ROLL MUDO (dentro de la ficha, mientras habla el narrador) ---
    ("moore-cocodrilos", "esc-lald-cocodrilos", 139.0, 145.0, "broll", "5 Moore", "Corre sobre los cocodrilos."),
    ("dalton-ltk", "esc-ltk-escape", 30.0, 36.0, "broll", "6 Dalton", "Acción de Licencia para matar (revisar)."),
    ("brosnan-tanque-muro", "esc-goldeneye-tanque", 59.0, 66.0, "broll", "7 Brosnan", "El tanque atraviesa el muro."),
    ("brosnan-tanque-estatua", "esc-goldeneye-tanque", 228.6, 234.0, "broll", "7 Brosnan", "El tanque con la estatua encima."),
    ("brosnan-botellas", "esc-goldeneye-tanque", 217.6, 221.5, "broll", "7 Brosnan", "El tanque aplasta el camión de Perrier (mapa Gemini v3)."),
    ("craig-grua", "esc-casino-parkour", 213.0, 222.0, "broll", "8 Craig", "El salto entre grúas."),
    ("craig-excavadora", "esc-skyfall-tren", 171.0, 179.0, "broll", "8 Craig / Skyfall", "La excavadora sobre el tren."),
    ("craig-salto-tren", "esc-skyfall-tren", 182.0, 190.0, "broll", "8 Craig / Skyfall", "Salta de la excavadora al vagón."),
]


# Montajes: varios tramos de la misma fuente encadenados en una sola escena con sonido (verificados con los mapas Gemini)
MONTAJES = [
    ("craig-parkour-voz", "esc-casino-parkour", [(68.0, 72.2), (221.4, 226.2), (280.6, 285.2)], "voz", "8 Craig",
     "Parkour: vigas → salto entre grúas → atraviesa la pared."),
    ("craig-skyfall-voz", "esc-skyfall-tren", [(14.0, 17.6), (184.6, 191.4)], "voz", "8 Craig / Skyfall",
     "Salto en moto al tren → salta de la excavadora al vagón y se acomoda los gemelos."),
    ("moore-cocodrilos-voz", "esc-lald-cocodrilos", [(140.0, 145.2)], "voz", "5 Moore", "Corre sobre los cocodrilos."),
]


def montar(nombre, fuente, tramos, tipo):
    """Encadena tramos con un fundido de audio corto en cada unión (corte seco en imagen)."""
    OUT.mkdir(parents=True, exist_ok=True)
    src = str(SRC / f"{fuente}.mp4")
    ins, fc = [], []
    for i, (a, b) in enumerate(tramos):
        ins += ["-ss", f"{a}", "-to", f"{b}", "-i", src]
        fc.append(f"[{i}:v]scale=-2:1080:flags=lanczos,fps=30,setsar=1[v{i}];"
                  f"[{i}:a]afade=t=in:d=0.04,afade=t=out:st={b - a - 0.06:.2f}:d=0.06[a{i}]")
    n = len(tramos)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    out = OUT / f"{nombre}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", str(out)], check=True)
    return out


def cortar(nombre, fuente, ini, fin, tipo):
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{nombre}.mp4"
    af = "loudnorm=I=-16:TP=-1.5:LRA=11" if tipo.startswith("voz") else "anull"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{ini}", "-to", f"{fin}", "-i", str(SRC / f"{fuente}.mp4"),
           "-vf", "scale=-2:1080:flags=lanczos,fps=30", "-af", af,
           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(out)]
    subprocess.run(cmd, check=True)
    return out


if __name__ == "__main__":
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    for n, f, a, b, t, *_ in CORTES:
        if filtro in n:
            cortar(n, f, a, b, t)
            print(f"ok {n} ({b - a:.1f}s, {t})")
    for n, f, tramos, t, *_ in MONTAJES:
        if filtro in n:
            montar(n, f, tramos, t)
            print(f"ok {n} ({sum(b - a for a, b in tramos):.1f}s, montaje {t})")
