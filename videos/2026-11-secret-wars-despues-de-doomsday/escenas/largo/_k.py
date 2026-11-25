"""Piezas comunes de LF03 (Secret Wars): sello de estado y viñetas del cómic desde el mapa.

vin(s, "n", 220, at=t)            -> mejor viñeta (valor_video) de la pág. 220, encuadrada a su proporción
vin(s, "n", 237, 4, at=t, box=…)  -> viñeta 4 de la pág. 237 dentro de la caja (l, t, w, h)
Las viñetas se copian de <LF03>/mapa/vinetas/ a assets/img/lf/lf03/ al construir.
"""
import json
import shutil
from pathlib import Path

from lib_h import MOTION, LF, IMG

SV = "lf/lf03-"
I = "lf/lf03/"
MAPA = LF / "mapa"
DST = MOTION / IMG / "lf/lf03"

ESTADO = {"K": ("CÓMIC", "doom"), "C": ("CONFIRMADO", "heroe"), "T": ("TEORÍA", "multi")}
_n = [0]


def tag(s, k, at, out=None):
    """sello de estado fijo arriba a la izquierda."""
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, 210, 90, at, color=col, rot=-5, size=40, out=out)
    return s


def _page(p):
    return json.loads((MAPA / "json" / f"page-{p:03d}.json").read_text())


def pick(page, n=None):
    """(archivo relativo a IMG, aspecto w/h) de la viñeta n (o la de mayor valor_video) de la página."""
    d = _page(page)
    vs = [v for v in d["vinetas"] if v.get("recorte")]
    v = next(x for x in vs if x["n"] == n) if n else max(vs, key=lambda x: (x["valor_video"], (x["bbox"][2]-x["bbox"][0])*(x["bbox"][3]-x["bbox"][1])))
    src = MAPA / v["recorte"]
    DST.mkdir(parents=True, exist_ok=True)
    if not (DST / src.name).exists():
        shutil.copy(src, DST / src.name)
    y0, x0, y1, x1 = v["bbox"]
    asp = ((x1 - x0) * d["ancho"]) / max(1, (y1 - y0) * d["alto"])
    return I + src.name, asp


def vin(s, name, page, n=None, at=None, box=(110, 90, 1700, 900), frm="R", rot=0, kb=None, kscale=1.08, out=None, label=None, pos="50% 40%"):
    """viñeta del cómic que cabe en `box` respetando su proporción (sin recortar de más). kb=fin del ken burns."""
    f, asp = pick(page, n)
    l, t, w, h = box
    if w / h > asp:      # caja más ancha que la viñeta → ajusta por alto
        ww, hh = h * asp, h
    else:
        ww, hh = w, w / asp
    ww, hh = max(ww, w * 0.55), max(hh, h * 0.55)   # no dejar viñetas diminutas (recorta un poco si hace falta)
    ww, hh = min(ww, w), min(hh, h)
    ll, tt = l + (w - ww) / 2, t + (h - hh) / 2
    s.img(name, f, int(ll), int(tt), int(ww), int(hh), at, frm=frm, pos=pos, rot=rot, out=out, label=label)
    if kb:
        s.kenburns(name, at + 0.3, kb, scale=kscale)
    return s


def full(s, name, page, n=None, at=None, until=None, pos="50% 40%", scale=1.1, x=0, y=0):
    """viñeta a pantalla completa (cover) con ken burns lento hasta `until`."""
    f, _ = pick(page, n)
    s.panel(name, f'<img src="{IMG}{f}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}" />'
                  f'<div class="pat-benday" style="position:absolute;inset:0;opacity:.15"></div>',
            0, 0, 1920, 1080, "tinta", 0, None)
    s.code(f'tl.fromTo(q("#{s.id(name)}"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.12 }}, {s.T(at)});')
    if until:
        s.kenburns(name, at, until, scale=scale, x=x, y=y)
    return s


_ELEG = None


def elegida(sec, phrase):
    """(pág, n) elegida por mapa/_scripts/elegir_vinetas.py para este beat, o None."""
    global _ELEG
    if _ELEG is None:
        f = Path(__file__).with_name("vinetas-elegidas.json")
        _ELEG = json.loads(f.read_text()) if f.exists() else {}
    e = _ELEG.get(f"{sec}|{phrase}")
    return (e[0], e[1]) if e else None


def beat(S, phrase, page=None, n=None, fullscreen=False, bg="tinta", enter="cut", k="K", txt=None, tc="amarillo",
         ono=None, oc="rojo", sfx=None, off=0.0, box=None, pos="50% 40%", zoom=False, frm="R", kscale=1.08):
    """escena que empieza cuando se dice `phrase`: viñeta (pág., n) + sello de estado + rótulo/onomatopeya opcionales."""
    t = S.w(phrase, off)
    s = S.scene(t, bg=bg, enter=enter)
    if page and n is None and elegida(S.id, phrase):
        page, n = elegida(S.id, phrase)
    if k:
        tag(s, k, t + 0.05)
    if page:
        if fullscreen:
            full(s, "v", page, n, t + 0.02, t + 8, pos=pos, scale=kscale)
        else:
            vin(s, "v", page, n, t + 0.02, box=box or ((110, 70, 1700, 800) if txt else (110, 90, 1700, 900)),
                kb=t + 8, frm=frm, pos=pos, kscale=kscale)
    if txt:
        s.text("tx", txt, "kw", tc, 960, 975, t + 0.35, size=70, rot=-2)
    if ono:
        s.text("on", ono, "ono", oc, 1480, 800, t + 0.3, rot=-6, hold=1.0, zoom=zoom)
    if sfx:
        s.sfx(sfx, t, -4)
    return s


def capcard(S, n, titulo, bg="rojo"):
    """tarjeta de capítulo al inicio de la sección (dura hasta el siguiente beat)."""
    s = S.scene(S.t0, bg=bg, enter="pageflip", color=bg)
    s.text("cn", f"CAPÍTULO {n}", "ttl", "amarillo", 960, 420, S.t0 + 0.05, size=150, rot=-3, misreg=True)
    s.text("ct", titulo, "kw", "papel", 960, 640, S.t0 + 0.3, size=110, rot=-2)
    s.sfx("pageflip", S.t0, -4)
    return s
