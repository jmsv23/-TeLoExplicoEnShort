"""Motor del estilo «comic» (Camino a Doomsday): 16:9 y 9:16.

Portado de content-creator/explicando/_motion/compositions/camino-a-doomsday/_lf/lib_h.py (generador de LF01-LF04).

Una spec por sección (escenas/<pieza>/<sec>.py) con una función build(S) que recibe un `Sec`:
    s = S.scene(S.w("Kang"), bg="doom", enter="ink")     # escena que empieza cuando se dice "Kang"
    s.text("t", "KANG", at=S.w("Kang"), ...)              # tiempos = palabras reales de la narración
Los tiempos salen de build/timeline-<pieza>.json (./tl voz): S.w("frase") busca la frase en orden dentro de la sección
y devuelve su inicio absoluto; S.we("frase") su fin. S.clip(i) = i-ésimo clip con audio de la sección.
Los assets que faltan van con S.ph(...) / Scene.ph(...): se ven como PLACEHOLDER hasta que exista el archivo
assets/img/lf/ph/<clave>.(jpg|png|webp). Se reemplazan soltando el archivo y reconstruyendo.

Cada PARTE del video (varias secciones) es una composición propia (renders más cortos y estables).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lib as L  # noqa: E402  (helpers SVG de la serie: portal, globe, tree, branches, shield…)

# ---- configuración: la fija configurar() antes de construir (antes venía de lfcfg.py + LFID)
MOTION = HERE          # carpeta base de las rutas de assets (= carpeta del video)
IMG = "assets/img/"
PHDIR = MOTION / IMG / "lf/ph"
LF = MOTION / "assets"  # material extra del video (p. ej. assets/mapa/ de las viñetas de cómic de LF03)
CID = "comic"          # prefijo de los ids de composición (antes camino-a-doomsday-<LFID>)
HEX = L.HEX
BG = L.BG
INK = "#0B0B14"
PARTS = []
DIAS = None
PLACA_RE, PLACA_TXT, TOTAL_DATOS = r"^$", "", 0
SECS = "secs"
W, H = 1920, 1080
VERT = False


def _escena_por_modulo(sid):
    import importlib
    mod = importlib.import_module(f"{SECS}.{sid}")
    importlib.reload(mod)
    return mod.build


ESCENA = _escena_por_modulo  # sid → función build(S) de la sección


def configurar(motion, tl, parts, secs="secs", size=(1920, 1080), dias=None, placa=(r"^$", "", 0), cid="comic",
               img="assets/img/", escena=None):
    """Fija la configuración del módulo (lo llama estilos/comic/estilo.py para cada pieza)."""
    global MOTION, IMG, PHDIR, TL, PARTS, SECS, W, H, VERT, DIAS, PLACA_RE, PLACA_TXT, TOTAL_DATOS, CID, ESCENA, LF
    MOTION, IMG, TL, PARTS, SECS, CID = Path(motion), img, tl, parts, secs, cid
    LF = MOTION / "assets"
    ESCENA = escena or _escena_por_modulo
    PHDIR = MOTION / IMG / "lf/ph"
    W, H = size
    VERT = H > W
    DIAS = dias
    PLACA_RE, PLACA_TXT, TOTAL_DATOS = placa
    L.MOTION, L.IMG = MOTION, IMG
    PH_USED.clear()
    _SVGN[0] = 0


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)


TL = None


def timeline():
    return TL


def f3(x):
    return f"{x:.3f}"


# ---------------------------------------------------------------- piezas de HTML reutilizables
def pho(file, pos="50% 25%", label=None, size=46, lc="#FFD400", sub=None, trama=0.3):
    h = f'<img src="{IMG}{file}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};display:block" />'
    h += f'<div class="pat-benday" style="position:absolute;inset:0;opacity:{trama}"></div>'
    if label:
        sb = f'<span style="display:block;font:700 {int(size*0.55)}px/1.1 Comic Neue,cursive;color:#FFF3D6">{sub}</span>' if sub else ""
        h += f'<div style="position:absolute;left:0;right:0;bottom:0;padding:8px 6px 10px;background:#0B0B14;text-align:center;font:400 {size}px/1 Anton;color:{lc}">{label}{sb}</div>'
    return h


PH_USED = {}


def ph(key, titulo, desc="", pos="50% 25%", label=None, size=46, sub=None):
    """asset pendiente: si existe lf/ph/<key>.*, lo usa como foto; si no, tarjeta PLACEHOLDER."""
    PH_USED[key] = (titulo, desc)
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = PHDIR / f"{key}.{ext}"
        if f.exists():
            return pho(f"lf/ph/{key}.{ext}", pos, label, size, sub=sub)
    lab = (f'<div style="position:absolute;left:0;right:0;bottom:0;padding:8px 6px 10px;background:#0B0B14;text-align:center;font:400 {size}px/1 Anton;color:#FFD400">{label}</div>'
           if label else "")
    return f'<div class="ph"><i>{key}</i><b>{titulo}</b><span>{desc}</span></div>{lab}'


_SVGN = [0]


def svgimg(file, w, h, extra=""):
    """.svg → SVG en línea (usa las fuentes de la página e ids únicos); otros formatos → <img>"""
    if not file.endswith(".svg"):
        return f'<img src="{IMG}{file}" style="width:{w}px;height:{h}px;display:block;{extra}" />'
    _SVGN[0] += 1
    pf = f"s{_SVGN[0]}-"
    src = (MOTION / IMG / file).read_text()
    src = re.sub(r'id="([^"]+)"', lambda m: f'id="{pf}{m.group(1)}"', src)
    src = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{pf}{m.group(1)})", src)
    src = re.sub(r'<svg ([^>]*?)width="\d+" height="\d+"', r'<svg \1', src, count=1)
    return src.replace("<svg ", f'<svg style="width:{w}px;height:{h}px;display:block;overflow:visible;{extra}" ', 1)


# ---------------------------------------------------------------- escena
class Scene:
    def __init__(s, sec, n, start, bg="papel", enter="halftone", color="papel", x=None, y=None, pat="pat-benday"):
        x = W // 2 if x is None else x
        y = H // 2 if y is None else y
        s.sec, s.n, s.start = sec, n, start
        s.end = None
        s.bg, s.enter, s.color, s.x, s.y, s.pat = bg, enter, color, x, y, pat
        s.els, s.js = [], []
        s.P = f"lf-{sec.id}-e{n}"

    # tiempos: absolutos → relativos a la parte (los resuelve Part al escribir)
    def T(s, t):
        return f"T({f3(t)})"

    def id(s, name):
        return f"{s.P}-{name}"

    def sfx(s, name, t, gain=0.0):
        s.sec.sfx.append((name, t, gain))

    def raw(s, html, js=""):
        s.els.append(html)
        if js:
            s.js.append(js)
        return s

    def code(s, js):
        s.js.append(js)
        return s

    def out(s, name, at):
        s.js.append(f'COM.popOut(tl, q("#{s.id(name)}"), {s.T(at - 0.05)});')
        return s

    # ---- texto
    def text(s, name, txt, kind="ono", color="amarillo", x=960, y=540, at=None, size=None, rot=-6, hold=0.9,
             out=None, how=None, words=None, misreg=False, zoom=False, sfx=True):
        i = s.id(name)
        st = (f"font-size:{size}px;" if size else "") + "text-align:center;line-height:.95;"
        cls = {"ono": f"ono ono--{color}", "ttl": f"ttl ttl--{color}", "kw": f"kw kw--{color}"}[kind]
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><span class="{cls}" id="{i}" style="--rot:{rot}deg;{st}">{txt}</span></div>')
        how = how or ("ono" if kind == "ono" else "stamp")
        if how == "ono":
            s.js.append(f'COM.onomato(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot}, hold: {hold}{", out: false" if out else ""} }});')
            if sfx:
                s.sfx("bam", at, -3)
        elif how == "words":
            s.js.append(f'COM.wordPop(tl, q("#{i}"), [{", ".join(s.T(w) for w in words)}]);')
        elif how == "pop":
            s.js.append(f'COM.popIn(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot} }});')
            if sfx:
                s.sfx("pop", at, -8)
        else:
            s.js.append(f'COM.stamp(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot} }});')
            if sfx:
                s.sfx("stamp", at, -6)
        if misreg:
            s.js.append(f'COM.misreg(tl, q("#{i}"), {s.T(at + 0.3)});')
        if zoom:
            s.zoom(at + 0.05)
        if out:
            s.out(name, out)
        return s

    # ---- viñeta
    def panel(s, name, inner, l, t, w, h, bg="papel", rot=0, at=None, frm="L", out=None, prot=None, sfx=True, extra=""):
        i = s.id(name)
        col = HEX.get(bg, bg)
        s.els.append(f'<div class="panel" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;background:{col};transform:rotate({rot}deg);{extra}">{inner}</div>')
        if at is not None:
            s.js.append(f'COM.panelSlam(tl, q("#{i}"), {s.T(at)}, {{ from: "{frm}", rot: {prot if prot is not None else 4} }});')
            if sfx:
                s.sfx("slam", at + 0.2, -9)
        if out:
            s.out(name, out)
        return s

    def img(s, name, file, l, t, w, h, at, frm="R", pos="50% 25%", label=None, out=None, rot=0, bob=None, sub=None):
        return s.panel(name, pho(file, pos, label, sub=sub), l, t, w, h, "tinta", rot, at, frm, out)

    def phpanel(s, name, key, titulo, desc, l, t, w, h, at, frm="R", pos="50% 25%", label=None, out=None, rot=0, sub=None):
        return s.panel(name, ph(key, titulo, desc, pos, label, sub=sub), l, t, w, h, "papel", rot, at, frm, out)

    # ---- objeto (svg/html) suelto, centrado en x,y
    def obj(s, name, inner, x, y, at, how="pop", out=None, bob=None, rot=0, frm="B", sfx=True):
        i = s.id(name)
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><div id="{i}" style="position:relative">{inner}</div></div>')
        s._in(i, at, how, rot, frm, sfx)
        if bob:
            s.js.append(f'COM.idleBob(tl, q("#{i}"), {s.T(at + 0.4)}, {s.T(bob)}, {{ amp: 8, cycle: 1.1 }});')
        if out:
            s.out(name, out)
        return s

    def com(s, name, kind, x, y, w, h, at, how="pop", out=None, bob=None, opts=None, rot=0):
        o = f" data-opts='{opts}'" if opts else ""
        return s.obj(name, f'<div data-com="{kind}"{o} style="width:{w}px;height:{h}px"></div>', x, y, at, how, out, bob, rot)

    def svg(s, name, file, x, y, w, h, at, how="pop", out=None, bob=None, rot=0, frm="B"):
        return s.obj(name, svgimg(file, w, h), x, y, at, how, out, bob, rot, frm)

    def _in(s, i, at, how, rot, frm, sfx=True):
        a = s.T(at)
        if how == "pop":
            s.js.append(f'COM.popIn(tl, q("#{i}"), {a}, {{ rot: {rot or 0} }});')
            if sfx:
                s.sfx("pop", at, -10)
        elif how == "drop":
            s.js.append(f'COM.dropIn(tl, q("#{i}"), {a}, {{ from: -1300 }});')
            if sfx:
                s.sfx("slam", at + 0.3, -8)
        elif how == "slide":
            s.js.append(f'COM.slideIn(tl, q("#{i}"), {a}, "{frm}");')
            if sfx:
                s.sfx("whoosh", at, -10)
        elif how == "slam":
            s.js.append(f'COM.panelSlam(tl, q("#{i}"), {a}, {{ from: "{frm}", rot: {rot or 4} }});')
            if sfx:
                s.sfx("slam", at + 0.2, -9)
        elif how == "stamp":
            s.js.append(f'COM.stamp(tl, q("#{i}"), {a}, {{ rot: {rot or 0} }});')
        elif how == "none":
            pass

    # ---- video (clip real, siempre muted: el audio va en la pista maestra)
    def video(s, name, src, media_in, at, dur, l, t, w, h, tag=None, pos="50% 50%", rot=0, frm="R", slam=True, tint=None, out=True, bg="tinta"):
        i = s.id(name)
        trk = s.sec.vtrack()
        ti = f'<div style="position:absolute;inset:0;background:{HEX.get(tint, tint)};mix-blend-mode:color;opacity:.55"></div>' if tint else ""
        tg = f'<div class="vtag">{tag}</div>' if tag else ""
        inner = (f'<video id="{i}-v" class="clip vclip" src="assets/video/{src}" muted playsinline '
                 f'data-start="__REL{f3(at)}__" data-duration="{f3(dur)}" data-media-start="{f3(media_in)}" data-track-index="{trk}" '
                 f'style="object-position:{pos}"></video>{ti}<div class="vtrama pat-benday"></div>{tg}')
        s.panel(name, inner, l, t, w, h, bg, rot, at - 0.3 if slam else None, frm, None)
        if not slam:  # sin entrada animada: invisible hasta su momento (si no, tapa al clip anterior)
            s.js.append(f'tl.fromTo(q("#{i}"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.01 }}, {s.T(max(0, at - 0.02))});')
        if out:
            s.out(name, at + dur + 0.05)
        return s

    # ---- cinta, caja del narrador, globo, sello
    def cinta(s, name, txt, color="rojo", top=820, rot=-5, at=None, out=None, left=-240):
        i = s.id(name)
        s.els.append(f'<div class="cinta cinta--{color}" id="{i}" style="left:{left}px;top:{top}px;--rot:{rot}deg"><span>{txt}</span></div>')
        s.js.append(f'COM.stamp(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot} }});')
        s.sfx("whoosh2", at, -8)
        if out:
            s.out(name, out)
        return s

    def cap(s, name, txt, at, left=60, top=70, width=720, out=None):
        i = s.id(name)
        s.els.append(f'<div class="cap" id="{i}" style="left:{left}px;top:{top}px;width:{width}px">{txt}</div>')
        s.js.append(f'COM.captionDrop(tl, q("#{i}"), {s.T(at)}, {{ text: {json.dumps(txt, ensure_ascii=False)} }});')
        if out:
            s.js.append(f'COM.captionOut(tl, q("#{i}"), {s.T(out - 0.05)});')
        return s

    def globo(s, name, txt, l, t, w, h, at, kind="globo", out=None, size=48, rot=-2):
        i = s.id(name)
        s.els.append(f'<div class="{kind}" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;font-size:{size}px;text-align:center;display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg)">{txt}</div>')
        s.js.append(f'COM.popIn(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot} }});')
        s.sfx("pop", at, -10)
        if out:
            s.out(name, out)
        return s

    def sello(s, name, txt, x, y, at, color="rojo", rot=-8, size=None, out=None):
        i = s.id(name)
        st = f"font-size:{size}px;" if size else ""
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><div class="sello sello--{color}" id="{i}" style="position:relative;{st}">{txt}</div></div>')
        s.js.append(f'COM.sello(tl, q("#{i}"), {s.T(at)}, {{ rot: {rot} }});')
        s.sfx("stamp", at + 0.15, -4)
        if out:
            s.out(name, out)
        return s

    def ficha(s, name, nombre, texto, imgfile_or_ph, x, y, at, estado=None, ecolor="heroe", rot=0, frm="B", phkey=None, phdesc=""):
        i = s.id(name)
        if phkey:
            im = ph(phkey, nombre, phdesc)
        else:
            im = f'<img src="{IMG}{imgfile_or_ph}" /><div class="pat-benday" style="position:absolute;inset:0;opacity:.25"></div>'
        se = f'<div class="sello sello--{ecolor}">{estado}</div>' if estado else ""
        s.els.append(f'<div class="ficha" id="{i}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="f-img">{im}</div>'
                     f'<div class="f-n">{nombre}</div><div class="f-t">{texto}</div>{se}</div>')
        s.js.append(f'COM.panelSlam(tl, q("#{i}"), {s.T(at)}, {{ from: "{frm}", rot: 4 }});')
        s.sfx("slam", at + 0.2, -9)
        if estado:
            s.js.append(f'COM.sello(tl, q("#{i} .sello"), {s.T(at + 0.45)}, {{ rot: -10 }});')
            s.sfx("stamp", at + 0.6, -6)
        return s

    # ---- efectos
    def speed(s, name, at, mode="radial", dirn="R", n=44, seed=3, dur=0.5, color="#FFF3D6", cx=None, cy=None):
        i = s.id(name)
        s.els.append(f'<div class="speed" id="{i}"></div>')
        extra = (f', dir: "{dirn}"' if mode == "parallel" else "") + (f", cx: {cx}, cy: {cy}" if cx is not None else "")
        s.js.append(f'COM.speedLines(tl, q("#{i}"), {s.T(at)}, {{ mode: "{mode}"{extra}, n: {n}, seed: {seed}, dur: {dur}, color: "{color}" }});')
        return s

    def zoom(s, at, amt=1.18):
        s.js.append(f'COM.zoomGolpe(tl, q("#{s.P}"), {s.T(at)}, {{ amt: {amt} }});')
        return s

    def flash(s, at):
        s.js.append(f'COM.flashBlanco(tl, stage, {s.T(at)});')
        return s

    def shake(s, name, at, amp=12, dur=0.4):
        s.js.append(f'COM.shake(tl, q("#{s.id(name)}"), {s.T(at)}, {{ amp: {amp}, dur: {dur} }});')
        return s

    def pulse(s, name, at, to=1.12):
        s.js.append(f'COM.pulse(tl, q("#{s.id(name)}"), {s.T(at)}, {{ to: {to} }});')
        return s

    def bob(s, name, a, b, amp=8):
        s.js.append(f'COM.idleBob(tl, q("#{s.id(name)}"), {s.T(a)}, {s.T(b)}, {{ amp: {amp}, cycle: 1.1 }});')
        return s

    def move(s, name, at, x=0, y=0, rot=0, scale=1, dur=0.5, ease="power2.out"):
        s.js.append(f'tl.to(q("#{s.id(name)}"), {{ x: {x}, y: {y}, rotation: {rot}, scale: {scale}, duration: {dur}, ease: "{ease}" }}, {s.T(at)});')
        return s

    def kenburns(s, name, a, b, scale=1.12, x=0, y=0):
        """movimiento lento continuo (para que nada quede quieto)"""
        s.js.append(f'tl.fromTo(q("#{s.id(name)}"), {{ scale: 1, x: 0, y: 0 }}, {{ scale: {scale}, x: {x}, y: {y}, duration: {f3(max(0.1, b - a))}, ease: "none", immediateRender: false }}, {s.T(a)});')
        return s

    def slab(s, name, color, at, until, pat=True):
        i = s.id(name)
        s.els.append(f'<div id="{i}" class="{"pat-benday-fuerte" if pat else ""}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:{HEX.get(color, color)}"></div>')
        s.js.append(f'tl.fromTo(q("#{i}"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {s.T(at)});')
        s.js.append(f'tl.to(q("#{i}"), {{ opacity: 0, duration: 0.15 }}, {s.T(until)});')
        return s

    def draw(s, name, d, color, at, w=16, dur=0.5):
        i = s.id(name)
        s.els.append(f'<svg style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:visible" viewBox="0 0 {W} {H}"><path id="{i}" d="{d}" fill="none" stroke="{HEX.get(color, color)}" stroke-width="{w}" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>')
        s.js.append(f'COM.drawOn(tl, q("#{i}"), {s.T(at)}, {{ dur: {dur} }});')
        return s

    def first(s):
        """primer instante en que algo de la escena se mueve (para no abrir escenas vacías)"""
        ts = [float(x) for j in s.js for x in re.findall(r"T\(([\d.]+)\)", j)]
        return min(ts) if ts else None

    # ---- salida
    def html(s):
        return (f'          <section class="scene" id="{s.P}">\n'
                f'            <div class="bg {BG[s.bg]} {s.pat}"></div>\n'
                f'            <div class="cam"><div class="rig">\n'
                + "\n".join("              " + e for e in s.els) +
                '\n            </div></div>\n          </section>')

    def script(s):
        e = (f'COM.scene(tl, q("#{s.P}"), {s.T(s.start)}, {s.T(s.end)}, '
             f'{{ enter: "{s.enter}", color: COM.C.{s.color}, x: {s.x}, y: {s.y} }});')
        return e + "\n" + "\n".join(s.js)


# ---------------------------------------------------------------- sección (palabras + escenas)
class Sec:
    def __init__(s, sid, part):
        tl = timeline()
        s.id, s.part = sid, part
        s.t0, s.t1 = tl["sections"][sid]
        s.words = [(norm(w), a, b, w) for w, a, b, bid in tl["words"] if s.t0 - 0.01 <= a < s.t1]
        s.clips = [c for c in tl["clips"] if c["sec"] == sid]
        s.blocks = [b for b in tl["blocks"] if b["sec"] == sid]
        s.cur = 0
        s.scenes, s.sfx, s.music = [], [], []
        s.dato = None

    def vtrack(s):
        s.part.trk += 1
        return s.part.trk

    def _find(s, phrase, start_idx):
        toks = [norm(t) for t in phrase.split() if norm(t)]
        n = [w[0] for w in s.words]
        for i in range(start_idx, len(n) - len(toks) + 1):
            if n[i:i + len(toks)] == toks:
                return i, i + len(toks) - 1
        return None

    def w(s, phrase, off=0.0, again=False):
        """inicio (abs) de la siguiente aparición de `phrase` desde el cursor; avanza el cursor."""
        r = s._find(phrase, s.cur)
        if r is None:
            r = s._find(phrase, 0) if again else None
        if r is None:
            ctx = " ".join(x[3] for x in s.words[s.cur:s.cur + 18])
            raise SystemExit(f"[{s.id}] no encuentro '{phrase}' después del cursor. Siguen: «{ctx}…»")
        s.cur = r[0] + 1
        s._last = r
        return round(s.words[r[0]][1] + off, 3)

    def we(s, phrase=None, off=0.0):
        """fin (abs) de la frase (o de la última encontrada con w si phrase es None)"""
        if phrase is not None:
            s.w(phrase)
        return round(s.words[s._last[1]][2] + off, 3)

    def peek(s, phrase, off=0.0):
        """como w pero sin mover el cursor"""
        cur = s.cur
        t = s.w(phrase, off)
        s.cur = cur
        return t

    def clip(s, i=0):
        return s.clips[i]

    def scene(s, start, **k):
        sc = Scene(s, len(s.scenes) + 1, start, **k)
        if s.scenes:
            s.scenes[-1].end = start
        s.scenes.append(sc)
        return sc

    def close(s, end=None):
        if s.scenes:
            s.scenes[-1].end = end if end is not None else s.t1


class Part:
    def __init__(s, name, secs):
        s.name, s.secids = name, secs
        s.trk = 10
        tl = timeline()
        s.t0 = tl["sections"][secs[0]][0] if secs[0] != PARTS[0][1][0] else 0.0
        s.t1 = tl["sections"][secs[-1]][1]
        s.secs = []

    @property
    def cid(s):
        return f"{CID}-{s.name}"

    def build(s):
        for sid in s.secids:
            S = Sec(sid, s)
            ESCENA(sid)(S)
            S.close(S.t1)
            # la primera escena de la parte arranca en el inicio de la parte
            s.secs.append(S)
        first = s.secs[0].scenes[0]
        first.start = min(first.start, s.t0)
        # la escena final de cada sección se extiende hasta la primera de la siguiente
        allsc = [sc for S in s.secs for sc in S.scenes]
        for sc in allsc[1:]:
            ft = sc.first()
            if ft is not None and ft > sc.start + 0.7:
                sc.start = round(ft - 0.3, 3)
        for a, b in zip(allsc, allsc[1:]):
            a.end = b.start
        allsc[-1].end = s.t1
        return s

    def html(s):
        tl = timeline()
        dur = round(s.t1 - s.t0, 3)
        P = f"lf-{s.name}"
        scenes_html = "\n".join(sc.html() for S in s.secs for sc in S.scenes)
        js_parts = []
        for S in s.secs:
            for sc in S.scenes:
                js_parts.append(f"          // ===== {S.id} · escena {sc.n} =====\n          {{\n{sc.script()}\n          }}")
        # placa de dato y barra de progreso global
        datos = []
        for S in s.secs:
            m = re.match(PLACA_RE, S.id)
            if m:
                datos.append((int(m.group(1)), S.t0, S.t1))
        dato_html = "\n".join(f'          <div class="dato-c" id="{P}-dato{n}">{PLACA_TXT} <b>{n}</b> / {TOTAL_DATOS}</div>' for n, _, _ in datos)
        dato_js = "\n".join(f'          COM.datoCounter(tl, q("#{P}-dato{n}"), T({f3(a + 0.6)}), T({f3(b)}));' for n, a, b in datos)
        total = tl["dur"]
        js = "\n".join(js_parts)
        body_html = scenes_html
        # tiempos relativos a la parte
        rel = lambda m: f3(float(m.group(1)) - s.t0)
        js = re.sub(r"T\(([\d.]+)\)", lambda m: rel(m), js)
        dato_js = re.sub(r"T\(([\d.]+)\)", lambda m: rel(m), dato_js)
        body_html = re.sub(r"__REL([\d.]+)__", lambda m: rel(m), body_html)
        return f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>{s.cid}</title>
  </head>
  <body>
    <template id="{s.cid}">
      <link rel="stylesheet" href="shared/explicando.css" />
      <link rel="stylesheet" href="shared/comic.css" />
{'      <link rel="stylesheet" href="shared/comic-v.css" />' if VERT else '      <link rel="stylesheet" href="shared/comic-h.css" />'}
      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script src="shared/explicando.js"></script>
      <script src="shared/comic-objects.js"></script>
      <script src="shared/comic.js"></script>
{'      <script src="shared/comic-v.js"></script>' if VERT else '      <script src="shared/comic-h.js"></script>'}
      <style>
        #{P}-root {{ position: absolute; inset: 0; }}
        #{P}-root .c {{ position: absolute; width: 0; height: 0; display: flex; align-items: center; justify-content: center; }}
        #{P}-root .c > * {{ flex: none; }}
      </style>
      <div id="{P}-root" data-composition-id="{s.cid}" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
        <div class="exp-stage" id="{P}-stage">
{body_html}
{"" if DIAS is None else f'          <div class="contador" id="{P}-cont">FALTAN {DIAS} DÍAS</div>'}
{dato_html}
          <div class="prog" id="{P}-prog"><i></i></div>
        </div>
      </div>
      <script>
        (function () {{
          const ID = "{s.cid}";
          const root = document.querySelector('[data-composition-id="' + ID + '"]');
          const stage = root.querySelector(".exp-stage");
          const q = EXP.q(root), qa = EXP.qa(root);
          const tl = gsap.timeline({{ paused: true }});
          COM.chrome(tl, stage);
          {"" if DIAS is None else f'COM.counter(tl, q("#{P}-cont"), {"0.6" if s.name == "p1" else "0"}, {DIAS});'}
          {"" if s.name == "p1" or DIAS is None else f'tl.set(q("#{P}-cont"), {{ x: 0, y: 0, rotation: -3, scale: 1 }}, 0.01);'}
          COM.progress(tl, q("#{P}-prog > i"), 0, {dur}, {f3(s.t0 / total)}, {f3(s.t1 / total)});
{dato_js}
{js}
          window.__timelines[ID] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''

    def wrapper(s):
        dur = round(s.t1 - s.t0, 3)
        rel = f"compositions/{s.name}.html"
        return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{s.cid}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="shared/explicando.css" />
  </head>
  <body>
    <div id="root" data-composition-id="r-{s.cid}" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}" data-fps="30">
      <div id="{s.cid}" data-composition-id="{s.cid}" data-composition-src="{rel}"
        data-start="0" data-duration="{dur}" data-track-index="1" data-width="{W}" data-height="{H}"></div>
    </div>
    <script>
      window.__timelines["r-{s.cid}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
