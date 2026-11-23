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
    "zoe-gamora": "Zoe Saldana Gamora Guardians of the Galaxy still",
    "zoe-oscar": "Zoe Saldana Oscar 2025 red carpet",
    "zoe-alfombra": "Zoe Saldana premiere red carpet 2025",
    "portman-jane": "Natalie Portman Jane Foster Thor still",
    "portman-mighty": "Natalie Portman Mighty Thor Love and Thunder",
    "portman-oscar": "Natalie Portman Oscar 2011 best actress Black Swan",
    "portman-alfombra": "Natalie Portman red carpet 2025",
    "zendaya-mj": "Zendaya MJ Spider-Man Homecoming still",
    "zendaya-bnd": "Zendaya MJ Spider-Man Brand New Day",
    "zendaya-metgala": "Zendaya Met Gala look",
    "zendaya-holland": "Zendaya Tom Holland red carpet together",
    "olsen-wanda": "Elizabeth Olsen Scarlet Witch crown Multiverse of Madness",
    "olsen-wandavision": "Elizabeth Olsen WandaVision Wanda",
    "olsen-alfombra": "Elizabeth Olsen red carpet premiere",
    "olsen-visionquest": "VisionQuest finale Doctor Doom Scarlet Witch",
    "scarlett-natasha": "Scarlett Johansson Natasha Romanoff Black Widow Avengers still",
    "scarlett-ironman2": "Scarlett Johansson Iron Man 2 Black Widow",
    "scarlett-esquire": "Scarlett Johansson Esquire cover 2013 sexiest woman alive",
    "scarlett-alfombra": "Scarlett Johansson red carpet 2025",
    "scarlett-endgame": "Scarlett Johansson Black Widow Endgame",
    "pugh-yelena": "Florence Pugh Yelena Belova Thunderbolts",
    "steinfeld-kate": "Hailee Steinfeld Kate Bishop Hawkeye",
    "larson-carol": "Brie Larson Captain Marvel Carol Danvers",
    "kirby-sue": "Vanessa Kirby Sue Storm Fantastic Four First Steps",
    "doomsday-poster": "Avengers Doomsday official poster",
    "pugh-retrato": "Florence Pugh Yelena close up Thunderbolts still",
    "olsen-ultron": "Elizabeth Olsen Wanda Age of Ultron still",
    "olsen-hermanas": "Elizabeth Olsen with Mary-Kate and Ashley Olsen",
    "portman-thor2011": "Natalie Portman Jane Foster Thor 2011 still",
    "portman-harvard": "Natalie Portman Harvard commencement speech 2015",
    "scarlett-jurassic": "Scarlett Johansson Jurassic World Rebirth Zora Bennett still",
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
