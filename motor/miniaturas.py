"""Miniaturas (largo, 1280×720) y portadas (short, 1080×1920): base + estilo + capa del video.

  base     base/publicacion/MINIATURAS.md (reglas: 3-5 palabras, complementa al título, una cara, contraste)
  estilo   estilos/<slug>/miniatura.css: la «piel» de las clases semánticas de abajo ({FONTS} = carpeta de fuentes)
           estilos/<slug>/miniaturas.py (opcional): layouts propios o que reemplazan a los de aquí
  video    miniaturas.json: [{"id": "miniatura-A", "pieza": "largo", "layout": "hero", "datos": {...}}, ...]
           o {"id": ..., "pieza": ..., "html": "miniaturas/x.html"} con el <body> a mano (usa las mismas clases)

Clases semánticas que define cada skin: .lienzo .hero .fade .kick .l1 .l2 (acento) .sub .sello .fila .fila-q .vs-linea
Imágenes: {"img": "id-del-manifiesto", "pos": "50% 30%", "bn": true}. Salida: entrega/<id>.png
"""
import json
import subprocess
from pathlib import Path

from .build import cargar, esc
from .proyecto import CONFIG, ROOT, die

TAM = {"largo": (1280, 720), "short": (1080, 1920)}


def _img(v, d):
    if not d:
        return ""
    if isinstance(d, str):
        d = {"img": d}
    src = next((p for p in sorted(v.a_img.glob(f"{d['img']}.*"))), None)
    if src is None:
        die(f"miniatura: falta la imagen {d['img']} en assets/img/")
    filt = "filter:grayscale(1) contrast(1.12) brightness(.98);" if d.get("bn") else ""
    return f'src="{src.resolve().as_uri()}" style="object-position:{d.get("pos", "50% 30%")};{filt}{d.get("css", "")}"'


def _fila(v, d):
    fila = d.get("fila") or []
    if not fila:
        return ""
    h = '<div class="fila">' + "".join(f'<div><img {_img(v, x)}></div>' for x in fila)
    if d.get("fila_q"):
        h += f'<div class="fila-q"><span class="l2">{esc(d["fila_q"])}</span></div>'
    return h + "</div>"


def _textos(d):
    h = ""
    if d.get("kick"):
        h += f'<div class="kick">{esc(d["kick"])}</div>'
    if d.get("l1"):
        h += f'<div class="l1" style="{d.get("css1", "")}">{esc(d["l1"])}</div>'
    if d.get("l2"):
        h += f'<div class="l2" style="{d.get("css2", "")}">{esc(d["l2"])}</div>'
    if d.get("sub"):
        h += f'<div class="sub">{esc(d["sub"])}</div>'
    if d.get("sello"):
        h += f'<div class="sello">{esc(d["sello"])}</div>'
    return h


# -------------------------------------------------------------------- layouts genéricos
def hero(v, d, w, h):
    """Foto protagonista a la derecha, texto a la izquierda, fila opcional de caras abajo."""
    return (f'<div class="lienzo"></div><img class="hero" {_img(v, d["img"])}><div class="fade"></div>'
            f'<div class="bloque" style="position:absolute;left:56px;top:{d.get("top", 70)}px;width:{d.get("ancho", 760)}px">{_textos(d)}</div>'
            + _fila(v, d))


def versus(v, d, w, h):
    """Dos fotos lado a lado (a, b) con etiqueta arriba de cada una y la frase grande abajo al centro."""
    a, b = d["a"], d["b"]
    return (f'<div class="lienzo"></div>'
            f'<img class="vs-a" {_img(v, a)}><img class="vs-b" {_img(v, b)}><div class="vs-linea"></div><div class="fade-b"></div>'
            + (f'<div class="vs-et vs-et-a l1">{esc(a["etiqueta"])}</div>' if a.get("etiqueta") else "")
            + (f'<div class="vs-et vs-et-b l2">{esc(b["etiqueta"])}</div>' if b.get("etiqueta") else "")
            + f'<div class="bloque centro" style="position:absolute;left:0;right:0;bottom:{d.get("abajo", 40)}px;text-align:center">'
              f'{_textos({k: d.get(k) for k in ("kick", "l1", "l2", "sub", "sello", "css1", "css2")})}</div>')


def portada(v, d, w, h):
    """Portada de Short 9:16: foto arriba, texto centrado en el tercio bajo (fuera de la zona de botones)."""
    return (f'<div class="lienzo"></div><img class="hero-v" {_img(v, d["img"])}><div class="fade-v"></div>'
            f'<div class="bloque centro" style="position:absolute;left:60px;right:60px;top:{d.get("top", 1110)}px;text-align:center">'
            f'{_textos(d)}</div>' + _fila(v, d))


LAYOUTS = {"hero": hero, "versus": versus, "portada": portada}


def css_estilo(v):
    d = v.estilo_dir()
    f = d / "miniatura.css"
    if not f.exists():
        die(f"el estilo {v.estilo} no tiene miniatura.css")
    return f.read_text().replace("{FONTS}", (d / "fonts").resolve().as_uri())


def render_uno(v, item):
    tipo = v.pieza(item["pieza"])["tipo"]
    w, h = TAM[tipo]
    if item.get("html"):
        body = (v.dir / item["html"]).read_text()
        body = body.replace("{IMG}", v.a_img.resolve().as_uri())
    else:
        extra = v.estilo_dir() / "miniaturas.py"
        L = dict(LAYOUTS)
        if extra.exists():
            mod = cargar(f"mini_{v.estilo}", extra)
            L.update({k: f for k, f in vars(mod).items() if callable(f) and not k.startswith("_")})
        lay = item.get("layout") or ("portada" if tipo == "short" else "hero")
        if lay not in L:
            die(f"miniatura {item['id']}: no hay layout «{lay}» (hay: {', '.join(L)})")
        body = L[lay](v, item.get("datos", {}), w, h)
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}'
           f'html,body{{width:{w}px;height:{h}px;overflow:hidden}}body{{position:relative}}\n{css_estilo(v)}\n'
           f'{item.get("css", "")}</style></head><body class="{tipo}">{body}</body></html>')
    tmp = v.build / "miniaturas" / f"{item['id']}.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(doc)
    out = v.entrega / f"{item['id']}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CONFIG["chrome"], "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={out.resolve()}", "--virtual-time-budget=4000", "--allow-file-access-from-files",
                    tmp.resolve().as_uri()], capture_output=True, check=False)
    if not out.exists():
        die(f"chrome no generó {out.name}")
    print(f"✓ {out.relative_to(ROOT)} ({w}×{h})")
    return out


def render(v, ids=None):
    f = v.dir / "miniaturas.json"
    if not f.exists():
        die(f"{v.slug}: falta miniaturas.json (plantilla en base/publicacion/miniaturas.ejemplo.json)")
    items = json.loads(f.read_text())
    outs = [render_uno(v, it) for it in items if not ids or it["id"] in ids]
    return outs


def hoja_miniaturas(v, outs):
    """Las miniaturas juntas a tamaño de feed (para elegir A/B como las vería alguien en YouTube)."""
    if not outs:
        return None
    sal = v.build / "miniaturas" / "_revision.jpg"
    ins = []
    for o in outs:
        ins += ["-i", str(o)]
    fc = "".join(f"[{i}:v]scale=-2:360[v{i}];" for i in range(len(outs))) + "".join(f"[v{i}]" for i in range(len(outs))) \
        + f"hstack=inputs={len(outs)}" if len(outs) > 1 else "[0:v]scale=-2:360"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-frames:v", "1", str(sal)], check=False)
    return sal if Path(sal).exists() else None
