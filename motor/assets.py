"""Assets de un video desde assets/manifest.json (fuente de verdad; los archivos se ignoran en git).

manifest.json
  imagenes:      [{id, archivo: "img/<id>.<ext>", url, pagina, fuente, pin}]
  fuentes_video: [{id, url}]                         → assets/video/<id>.mp4 (yt-dlp)
  cortes:        [{id, fuente, inicio, fin, tipo: voz|voz-alt|broll, zoom?, bloque?, nota?}] → assets/video/cortes/<id>.mp4
pin=true marca lo que no se puede volver a bajar (sin URL directa o fuente que puede desaparecer): ./tl assets respaldar.
"""
import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

from .proyecto import CONFIG, ROOT, die

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
RESPALDO = Path(CONFIG.get("respaldo_assets", "~/Documentos/youtube/_respaldo-assets")).expanduser()


def manifest(v):
    f = v.dir / "assets/manifest.json"
    if not f.exists():
        return {"imagenes": [], "fuentes_video": [], "cortes": []}
    return json.loads(f.read_text())


def guardar(v, m):
    f = v.dir / "assets/manifest.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n")


def bajar(url, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": url})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if len(data) < 2000:
        raise ValueError(f"respuesta muy chica ({len(data)} B)")
    out.write_bytes(data)


def medir(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        w, h = r.stdout.strip().split("\n")[0].split(",")[:2]
        return int(w), int(h)
    except ValueError:
        return 0, 0


def agregar_img(v, iid, url, pagina=None, fuente=None, pin=False):
    """Baja una imagen elegida (de la búsqueda con bx/images-search) y la registra en el manifiesto."""
    m = manifest(v)
    ext = Path(url.split("?")[0]).suffix.lower()
    ext = ext if ext in (".jpg", ".jpeg", ".png", ".webp", ".avif") else ".jpg"
    out = v.a_img / f"{iid}{ext}"
    bajar(url, out)
    if out.suffix in (".webp", ".avif", ".png"):  # el motor trabaja en jpg
        jpg = out.with_suffix(".jpg")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(out), "-q:v", "2", str(jpg)], check=True)
        out.unlink()
        out = jpg
    w, h = medir(out)
    m["imagenes"] = [i for i in m["imagenes"] if i["id"] != iid] + [
        {"id": iid, "archivo": f"img/{out.name}", "url": url, "pagina": pagina, "fuente": fuente, "pin": pin, "tam": f"{w}x{h}"}]
    guardar(v, m)
    print(f"✓ {iid}: {w}×{h}" + ("  ⚠ menos de 1000 px de ancho" if w < 1000 else ""))


def fetch(v, solo_img=False):
    m = manifest(v)
    ok = fallo = 0
    for i in m["imagenes"]:
        out = v.dir / "assets" / i["archivo"]
        if out.exists():
            continue
        if not i.get("url"):
            r = RESPALDO / v.slug / i["archivo"]
            if r.exists():
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(r, out)
                ok += 1
            else:
                print(f"  ✗ {i['id']}: sin URL ni respaldo")
                fallo += 1
            continue
        try:
            bajar(i["url"], out)
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {i['id']}: {e}")
            fallo += 1
    if not solo_img:
        necesarias = {c["fuente"] for c in m["cortes"] if not (v.a_cut / f"{c['id']}.mp4").exists()}
        for fv in m["fuentes_video"]:
            out = v.a_vid / f"{fv['id']}.mp4"
            if fv["id"] not in necesarias or out.exists():
                continue
            r = subprocess.run(["yt-dlp", "-q", "--no-playlist", "-f", "bv*[height<=1080]+ba/b[height<=1080]",
                                "--merge-output-format", "mp4", "-o", str(out), fv["url"]], capture_output=True, text=True)
            if r.returncode:
                print(f"  ✗ video {fv['id']}: {r.stderr.strip()[-200:]}")
                fallo += 1
            else:
                ok += 1
    print(f"✓ fetch: {ok} bajados · {fallo} fallaron")


def cortar_uno(v, c):
    src = v.a_vid / f"{c['fuente']}.mp4"
    if not src.exists():
        die(f"falta la fuente {src.relative_to(ROOT)} (./tl assets fetch {v.slug})")
    out = v.a_cut / f"{c['id']}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()  # por si es un hardlink: no pisar el original
    zoom = c.get("zoom", 1.0) or 1.0
    vf = []
    if zoom < -1:  # recorte centrado
        z = -zoom
        vf.append(f"crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})/2")
    if zoom > 1:  # centrado en x, pegado arriba: saca subtítulos quemados abajo
        vf.append(f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})/2:0")
    vf += ["scale=1920:1080:force_original_aspect_ratio=increase", "crop=1920:1080", "fps=30", "setsar=1"]
    voz = c.get("tipo", "voz").startswith("voz")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{c['inicio']}", "-to", f"{c['fin']}", "-i", str(src),
           "-vf", ",".join(vf), "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p"]
    cmd += (["-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"] if voz
            else ["-c:a", "aac", "-b:a", "160k", "-ar", "48000"])
    subprocess.run(cmd + [str(out)], check=True)
    print(f"  ✓ {c['id']} ({c['fin'] - c['inicio']:.1f} s, {c.get('tipo', 'voz')})")


def cortar(v, ids=None, force=False):
    for c in manifest(v)["cortes"]:
        if ids and c["id"] not in ids:
            continue
        if (v.a_cut / f"{c['id']}.mp4").exists() and not force and not ids:
            continue
        cortar_uno(v, c)


def verificar(v):
    m = manifest(v)
    problemas = []
    for i in m["imagenes"]:
        p = v.dir / "assets" / i["archivo"]
        if not p.exists():
            problemas.append(f"falta imagen {i['id']}")
            continue
        w, h = medir(p)
        if w < 1000:
            problemas.append(f"imagen chica {i['id']} ({w}×{h})")
    for c in m["cortes"]:
        if not (v.a_cut / f"{c['id']}.mp4").exists():
            problemas.append(f"falta corte {c['id']}")
    sin_url = [i["id"] for i in m["imagenes"] if not i.get("url")]
    print(f"{len(m['imagenes'])} imágenes · {len(m['fuentes_video'])} fuentes de video · {len(m['cortes'])} cortes · "
          f"{len(sin_url)} sin URL (pin)")
    for p in problemas:
        print("  ⚠", p)
    return problemas


def respaldar(v):
    """Copia fuera de git lo marcado pin=true (y las imágenes sin URL) a CONFIG.respaldo_assets/<video>/."""
    m = manifest(v)
    n = 0
    for i in m["imagenes"]:
        if not (i.get("pin") or not i.get("url")):
            continue
        p = v.dir / "assets" / i["archivo"]
        if p.exists():
            d = RESPALDO / v.slug / i["archivo"]
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, d)
            n += 1
    for c in m["cortes"]:
        if c.get("pin") and (v.a_cut / f"{c['id']}.mp4").exists():
            d = RESPALDO / v.slug / "video/cortes" / f"{c['id']}.mp4"
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(v.a_cut / f"{c['id']}.mp4", d)
            n += 1
    print(f"✓ respaldo: {n} archivos en {RESPALDO / v.slug}")


def hoja_fuente(v, fuente, cada=1.0):
    """Hoja de contacto a 1 fps de una fuente de video para elegir tiempos de corte (assets/_hojas/, ignorado)."""
    from .render import hoja
    src = v.a_vid / f"{fuente}.mp4"
    if not src.exists():
        die(f"falta {src.relative_to(ROOT)}")
    return hoja(src, v.dir / "assets/_hojas" / f"{fuente}.jpg", cada=cada, ancho=240, cols=12)
