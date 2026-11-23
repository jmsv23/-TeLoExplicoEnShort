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
    # (nombre, fuente, inicio, fin, tipo, bloque, zoom, nota). zoom>1 recorta pegado arriba; zoom<-1 recorta centrado.
    ("cj-here-we-go", "sa-intro", 180.6, 185.0, "voz", "sanandreas", 1.0, "Ah shit, here we go again"),
    ("roman-bowling", "iv-roman", 2.9, 5.9, "voz", "gta4", -1.2, "Niko, it's Roman, let's go bowling (centrado: saca Bandicam y subtítulo)"),
    ("trailer1-lucia", "gta6-tr1", 6.6, 11.2, "voz", "espera", -1.33, "Lucia, do you know why you're here? Bad luck, I guess."),
    ("gta1-calle", "gta1-gameplay", 12.0, 18.0, "broll", "hook", 1.0, "GTA 1 manejando desde arriba"),
    ("gta1-policia", "gta1-gameplay", 195.0, 201.0, "broll", "origen", 1.0, "GTA 1 persecución policial"),
    ("gta2-calle", "gta2-gameplay", 84.0, 90.0, "broll", "origen", 1.0, "GTA 2 calles"),
    ("gta2-calle2", "gta2-gameplay", 176.0, 182.0, "broll", "origen", 1.0, "GTA 2 perseguido por patrullas"),
    ("gta3-ciudad", "gta3-intro", 176.0, 182.0, "broll", "salto3d", 1.0, "GTA III furgón en el puente bajo la lluvia"),
    ("gta3-calle", "gta3-intro", 328.0, 334.0, "broll", "salto3d", 1.0, "GTA III manejando por Liberty City"),
    ("gta3-patrulla", "gta3-intro", 262.0, 268.0, "broll", "salto3d", 1.0, "GTA III ataque al convoy policial"),
    ("vc-atardecer", "vc-gameplay", 66.0, 69.5, "broll", "vicecity", 1.0, "Vice City atardecer con palmeras"),
    ("vc-tommy-auto", "vc-gameplay", 180.0, 186.0, "broll", "vicecity", 1.0, "Tommy en auto deportivo rojo"),
    ("sa-llegada", "sa-intro", 28.5, 34.5, "broll", "sanandreas", 1.0, "CJ llega al aeropuerto"),
    ("sa-callejon", "sa-intro", 174.0, 180.0, "broll", "sanandreas", 1.0, "CJ solo en el callejón"),
    ("sa-cuerpo3", "sa-cuerpo", 9.0, 15.0, "broll", "sanandreas", 1.0, "CJ flaco, musculoso y gordo lado a lado"),
    ("sa-gordo", "sa-cuerpo", 40.0, 46.0, "broll", "sanandreas", 1.0, "CJ intenta saltar el muro"),
    ("sa-musculo", "sa-cuerpo", 92.0, 98.0, "broll", "sanandreas", 1.0, "CJ peleando"),
    ("sa-gym", "sa-cuerpo", 64.0, 70.0, "broll", "sanandreas", 1.0, "CJ saltando entre techos"),
    ("iv-calle", "iv-vs-v-fisica", 16.0, 22.0, "broll", "gta4", 1.0, "GTA IV auto en la calle"),
    ("iv-choque", "iv-vs-v-fisica", 88.5, 92.5, "broll", "gta4", 1.0, "GTA IV impacto brutal"),
    ("iv-euphoria-1", "iv-euphoria", 5.0, 10.0, "broll", "gta4", 1.0, "Euphoria: atropello"),
    ("iv-euphoria-2", "iv-euphoria", 134.0, 139.0, "broll", "gta4", 1.0, "Euphoria: golpe de helicóptero"),
    ("iv-vs-v-a", "iv-vs-v-fisica", 15.0, 21.0, "broll", "gta4", 1.0, "choque en GTA IV"),
    ("iv-vs-v-b", "iv-vs-v-fisica", 2.0, 8.0, "broll", "gta4", 1.0, "choque en GTA V"),
    ("v-ls", "v-trailer", 44.0, 49.0, "broll", "gta5", 1.0, "GTA V salto en paracaídas sobre Los Santos"),
    ("v-ls2", "v-trailer", 35.0, 40.0, "broll", "gta5", 1.0, "GTA V persecución bajo lluvia"),
    ("v-cambio", "v-mft", 60.0, 66.0, "broll", "gta5", 1.0, "GTA V atracos y acción"),
    ("v-michael", "v-mft", 20.0, 26.0, "broll", "gta5", 1.0, "GTA V vida de Michael"),
    ("v-policia", "v-mft", 120.0, 126.0, "broll", "policia", 1.0, "Franklin contra la policía"),
    ("vi-atardecer", "gta6-tr1", 2.4, 5.0, "broll", "hook", -1.33, "GTA 6 atardecer en autopista"),
    ("vi-playa", "gta6-tr1", 11.0, 13.6, "broll", "espera", -1.33, "GTA 6 playa desde el aire"),
    ("vi-noche", "gta6-tr1", 20.0, 26.0, "broll", "espera", -1.33, "GTA 6 vida nocturna"),
    ("vi-caiman", "gta6-tr1", 47.5, 50.5, "broll", "s5", -1.33, "caimán en la tienda"),
    ("vi-entrada", "gta6-tr1", 72.0, 77.0, "broll", "gta6", -1.33, "Jason y Lucía entran armados"),
    ("vi-yate", "gta6-tr2", 93.0, 97.0, "broll", "espera", -1.33, "fiesta en yate"),
    ("vi-explosion", "gta6-tr2", 115.0, 120.0, "broll", "gta6", -1.33, "explosión con policía"),
    ("vi-pantano", "gta6-tr2", 137.0, 142.0, "broll", "vicecity", -1.33, "persecución en el pantano"),
    ("vi-aereo", "gta6-tr2", 6.0, 12.0, "broll", "vicecity", -1.33, "Vice City desde el aire"),
    ("vi-aereo2", "gta6-launch", 16.5, 20.0, "broll", "polemicas", -1.33, "Vice City de noche"),
    ("vi-policia-1", "vi-policia", 148.0, 154.0, "broll", "policia", 1.0, "persecución policial GTA 6"),
    ("vi-policia-2", "vi-policia", 117.0, 123.0, "broll", "policia", 1.0, "asalto y persecución bajo un avión"),
    ("vi-barco", "vi-barco", 51.0, 58.0, "broll", "gta6", 1.0, "GPS del velero con el mapa de Los Santos"),
    ("vi-barco2", "vi-barco", 0.5, 6.0, "broll", "s3", 1.0, "el velero de Michael junto a la casa de Jason"),
    ("vi-gym", "vi-gym", 158.0, 164.0, "broll", "gta6", 1.0, "gimnasio en GTA 6"),
    ("vi-choque-1", "vi-choques", 13.0, 18.0, "broll", "gta6", 1.0, "SUV choca contra camión y vuelca"),
    ("vi-choque-2", "vi-choques", 152.0, 158.0, "broll", "gta6", 1.0, "deportivo rojo vuelca"),
    ("vi-gym2", "gta6-tr2", 39.0, 42.5, "broll", "gta6", -1.33, "pesas en la playa"),
    ("vi-patrulla", "gta6-tr2", 45.5, 50.0, "broll", "policia", -1.33, "patrulla detrás de Jason"),
    ("vc-vs-vi-a", "vc-gameplay", 190.0, 196.0, "broll", "vicecity", 1.0, "Vice City 2002 manejando"),
    ("vc-vs-vi-b", "vi-manejo", 88.0, 94.0, "broll", "vicecity", 1.0, "Vice City 2026 manejando"),
    ("vi-moto", "gta6-launch", 48.0, 51.0, "broll", "shorts", -1.33, "salto en moto"),
]


def cortar(nombre, fuente, a, b, tipo, zoom):
    vf = []
    if zoom < -1:
        z = -zoom
        vf.append(f"crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})/2")
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
