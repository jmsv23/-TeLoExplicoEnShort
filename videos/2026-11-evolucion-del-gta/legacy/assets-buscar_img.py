#!/usr/bin/env python3
"""Busca imágenes con Brave (bx images), descarga las K más grandes por consulta y arma una hoja de contactos.

Uso (desde content-creator/, para cargar la key sin imprimirla):
  set -a; . ./.env; set +a
  python3 -I explicando/top-5-actrices-marvel-mas-guapas/assets/buscar_img.py [slug ...]

Salida:
  _busqueda/img-<slug>.json   resultados compactos {t, src, page, img, w, h}
  _candidatos/<slug>-N.jpg     descargas (sin tocar)
  _hojas/hoja-<slug>.jpg       hoja de contactos con número, tamaño y dominio
"""
import json, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
BUS, CAND, HOJ = AQUI / "_busqueda", AQUI / "_candidatos", AQUI / "_hojas"
K = 8
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"

CONSULTAS = {
    "cov-gta1": "Grand Theft Auto 1997 PC box art cover",
    "cov-gta2": "Grand Theft Auto 2 1999 box art cover",
    "cov-gta3": "Grand Theft Auto III cover art PS2",
    "cov-vc": "Grand Theft Auto Vice City cover art",
    "cov-sa": "Grand Theft Auto San Andreas cover art",
    "cov-iv": "Grand Theft Auto IV cover art",
    "cov-v": "Grand Theft Auto V cover art",
    "cov-vi": "Grand Theft Auto VI official key art cover",
    "lucia-arte": "GTA 6 Lucia Caminos official artwork Rockstar",
    "jason-lucia": "GTA 6 Jason and Lucia official artwork",
    "mapa-vc2002": "GTA Vice City 2002 full map",
    "mapa-leonida": "GTA 6 Leonida map official",
    "mapa-gtav": "GTA V full map Los Santos Blaine County",
    "mapa-sa": "GTA San Andreas full map",
    "liotta": "Ray Liotta portrait",
    "thompson": "Jack Thompson attorney video games",
    "metacritic-gta6": "GTA 6 Metacritic 99 score user score",
    "tommy": "Tommy Vercetti Vice City artwork",
    "cj": "CJ Carl Johnson San Andreas artwork",
    "niko": "Niko Bellic GTA IV artwork",
    "mft": "GTA V Michael Franklin Trevor artwork",
    "claude-gta3": "Claude GTA III artwork",
    "dma-design": "DMA Design Dundee 1997 team GTA",
    "ocean-view": "GTA 6 Ocean View Hotel Ocean Beach",
    "vc-neon": "GTA 6 Vice City screenshot official neon",
    "gta6-screens": "GTA 6 official screenshot Leonida",
    "taketwo": "Take-Two Interactive logo",
}


def buscar(slug, q):
    out = BUS / f"img-{slug}.json"
    if out.exists():
        return json.loads(out.read_text())
    r = subprocess.run(["bx", "images", q, "--count", "40"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[{slug}] bx falló: {r.stderr[:200]}")
        return []
    data = json.loads(r.stdout)
    res = []
    for x in data.get("results", []):
        p = x.get("properties", {}) or {}
        res.append({"t": x.get("title", "")[:100], "src": x.get("source", ""), "page": x.get("url", ""),
                    "img": p.get("url", ""), "w": p.get("width") or 0, "h": p.get("height") or 0,
                    "thumb": (x.get("thumbnail") or {}).get("src", "")})
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def bajar(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": ""})
        with urllib.request.urlopen(req, timeout=20) as r:
            b = r.read()
        if len(b) < 15000:
            return False
        dest.write_bytes(b)
        with Image.open(dest) as im:
            im.verify()
        return True
    except Exception:
        dest.unlink(missing_ok=True)
        return False


def hoja(slug, items):
    fuente = ImageFont.load_default(size=22)
    celdas = []
    for i, it in items:
        p = CAND / f"{slug}-{i}.jpg"
        try:
            im = Image.open(p).convert("RGB")
        except Exception:
            continue
        w, h = im.size
        im.thumbnail((420, 420))
        c = Image.new("RGB", (440, 480), (24, 24, 24))
        c.paste(im, ((440 - im.width) // 2, 10 + (420 - im.height) // 2))
        ImageDraw.Draw(c).text((10, 440), f"#{i} {w}x{h} {it['src'][:22]}", fill=(255, 220, 120), font=fuente)
        celdas.append(c)
    if not celdas:
        return
    cols = 4
    filas = (len(celdas) + cols - 1) // cols
    H = Image.new("RGB", (cols * 440, filas * 480), (0, 0, 0))
    for n, c in enumerate(celdas):
        H.paste(c, ((n % cols) * 440, (n // cols) * 480))
    H.save(HOJ / f"hoja-{slug}.jpg", quality=80)


def procesar(slug):
    res = buscar(slug, CONSULTAS[slug])
    vistos, elegidos = set(), []
    for i, x in sorted(enumerate(res), key=lambda t: -(t[1]["w"] * t[1]["h"])):
        if not x["img"] or x["img"] in vistos or min(x["w"], x["h"]) < 500:
            continue
        vistos.add(x["img"])
        elegidos.append((i, x))
    ok = []
    for i, x in elegidos:
        if len(ok) >= K:
            break
        if bajar(x["img"], CAND / f"{slug}-{i}.jpg"):
            ok.append((i, x))
    hoja(slug, ok)
    print(f"[{slug}] {len(res)} resultados, {len(ok)} descargadas")


if __name__ == "__main__":
    for d in (BUS, CAND, HOJ):
        d.mkdir(exist_ok=True)
    slugs = sys.argv[1:] or list(CONSULTAS)
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(procesar, slugs))
