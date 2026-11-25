"""Generador de episodios de Camino a Doomsday (02-11).
Una spec de episodio (eps/epNN.py) define escenas y beats; este módulo escribe
  - <ep>/motion-script.md   (beats con ancla en **negritas** para `tiempos`)
  - _motion/compositions/camino-a-doomsday/NN-slug.html   (composición HyperFrames)
Uso: python3 _gen/build.py NN [--script]   (--script = solo motion-script.md)
Tiempos: nunca segundos absolutos; todo es b("escena.beat", offset). 'end' = fin de la escena."""
import re
from pathlib import Path

# Portado de content-creator/explicando/_motion/compositions/camino-a-doomsday/_gen/lib.py.
# Las rutas las fija lib_h.configurar() (MOTION = carpeta del video, IMG = "assets/img/").
GEN = Path(__file__).resolve().parent
COMP = GEN
MOTION = GEN
SERIE = GEN
IMG = "assets/img/"

BG = {"papel": "bg-com-papel", "heroe": "bg-com-heroe", "multi": "bg-com-multi", "doom": "bg-com-doom",
      "ciencia": "bg-com-ciencia", "rojo": "bg-com-rojo", "ceniza": "bg-com-ceniza", "tinta": "bg-com-tinta", "doom-osc": "bg-com-doom-osc", "multi-osc": "bg-com-multi-osc"}
HEX = {"tinta": "#0B0B14", "papel": "#FFF3D6", "heroe": "#1E5BFF", "rojo": "#E8212B", "amarillo": "#FFD400",
       "doom": "#1FA85A", "multi": "#8A2BE2", "ciencia": "#00C8E8", "ceniza": "#6B7280",
       "doom-osc": "#0E5C32", "multi-osc": "#4B1580"}


def bt(x, ep_scene=None):
    """'3.2' | ('3.2', .15) | 'end' → código JS"""
    if x == "end":
        return f'E("{ep_scene}")[1]'
    if isinstance(x, tuple):
        return f'b("{x[0]}", {x[1]})'
    return f'b("{x}")'


class Scene:
    def __init__(s, ep, n, nombre, seg, bg="papel", enter="halftone", color="papel", x=540, y=820, pat="pat-benday"):
        s.ep, s.n, s.nombre, s.seg = ep, n, nombre, seg
        s.bg, s.enter, s.color, s.x, s.y, s.pat = bg, enter, color, x, y, pat
        s.beats, s.els, s.js = [], [], []
        s.P = f"v{ep.num}-e{n}"
        s.lastbeat = None

    # ---- beats
    def beat(s, i, t_est, voz, nota=""):
        s.beats.append((f"{s.n}.{i}", t_est, voz, nota))
        s.lastbeat = f"{s.n}.{i}"
        return s

    def t(s, x):
        return bt(x, s.n)

    def id(s, name):
        return f"{s.P}-{name}"

    # ---- piezas base
    def raw(s, html, js=""):
        s.els.append(html)
        if js:
            s.js.append(js)
        return s

    def code(s, js):
        s.js.append(js)
        return s

    def _out(s, sel, out, fn="popOut"):
        if out:
            s.js.append(f'COM.{fn}(tl, q("{sel}"), {s.t(out) if not isinstance(out, tuple) or True else ""} - 0.05);'
                        .replace(f"{s.t(out)} - 0.05", f"{s.t(out)} - 0.05"))

    def out(s, name, at):
        s.js.append(f'COM.popOut(tl, q("#{s.id(name)}"), {s.t(at)} - 0.05);')
        return s

    def hide(s, name):
        s.js.append(f'tl.set(q("#{s.id(name)}"), {{ opacity: 0 }}, 0);')
        return s

    # ---- texto: ono (Bangers), ttl (Anton), kw
    def text(s, name, txt, kind="ono", color="amarillo", x=540, y=820, at=None, size=None, rot=-6, hold=0.9,
             out=None, how=None, words=None, misreg=False, zoom=False):
        i = s.id(name)
        st = f"font-size:{size}px;" if size else ""
        st += "text-align:center;line-height:.95;"
        cls = {"ono": f"ono ono--{color}", "ttl": f"ttl ttl--{color}", "kw": f"kw kw--{color}"}[kind]
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><span class="{cls}" id="{i}" style="--rot:{rot}deg;{st}">{txt}</span></div>')
        how = how or ("ono" if kind == "ono" else "stamp")
        if how == "ono":
            s.js.append(f'COM.onomato(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot}, hold: {hold}{", out: false" if out else ""} }});')
        elif how == "words":
            ts = ", ".join(s.t(w) for w in words)
            s.js.append(f'COM.wordPop(tl, q("#{i}"), [{ts}]);')
        elif how == "pop":
            s.js.append(f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});')
        else:
            s.js.append(f'COM.stamp(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});')
        if misreg:
            s.js.append(f'COM.misreg(tl, q("#{i}"), {s.t(at)} + 0.3);')
        if zoom:
            s.js.append(f'COM.zoomGolpe(tl, q("#{s.P}"), {s.t(at)} + 0.05);')
        if out:
            s.out(name, out)
        return s

    # ---- viñeta con contenido
    def panel(s, name, inner, l, t, w, h, bg="papel", rot=0, at=None, frm="L", out=None, prot=None, slam=True):
        i = s.id(name)
        col = HEX.get(bg, bg)
        s.els.append(f'<div class="panel" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;background:{col};transform:rotate({rot}deg)">{inner}</div>')
        if at is not None:
            s.js.append(f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {prot if prot is not None else 4} }});')
        if out:
            s.out(name, out)
        return s

    @staticmethod
    def pobj(name, w, h, opts=None, extra=""):
        o = f" data-opts='{opts}'" if opts else ""
        return f'<div class="c" style="position:relative"><div data-com="{name}"{o} style="width:{w}px;height:{h}px;{extra}"></div></div>'

    @staticmethod
    def plabel(txt, color="tinta", size=64, bottom=30):
        return f'<div style="position:absolute;left:0;right:0;bottom:{bottom}px;text-align:center;font:400 {size}px/1 Anton;color:{HEX.get(color, color)}">{txt}</div>'

    @staticmethod
    def pimg(file, w, h, pos="top"):
        return (f'<div class="c" style="position:relative"><div style="width:{w}px;height:{h}px;position:relative"><img src="{IMG}{file}" '
                f'style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block;border:10px solid #0B0B14;box-shadow:10px 10px 0 #0B0B14;box-sizing:border-box" />'
                f'<div class="pat-benday" style="position:absolute;inset:0;opacity:.6"></div></div></div>')

    # ---- objeto suelto
    def obj(s, name, com, x, y, w, h, at, how="pop", out=None, opts=None, bob=None, rot=None, frm="B"):
        i = s.id(name)
        o = f" data-opts='{opts}'" if opts else ""
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><div id="{i}" data-com="{com}"{o} style="width:{w}px;height:{h}px"></div></div>')
        s._in(i, at, how, rot, frm, y)
        if bob:
            s.js.append(f'COM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});')
        if out:
            s.out(name, out)
        return s

    def img(s, name, file, x, y, w, h, at, how="slam", out=None, pos="top", rot=0, frm="R", bob=None):
        i = s.id(name)
        s.els.append(f'<div class="c" style="left:{x}px;top:{y}px"><div id="{i}" style="width:{w}px;height:{h}px;position:relative;transform:rotate({rot}deg)">'
                     f'<img src="{IMG}{file}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block;border:10px solid #0B0B14;box-shadow:10px 10px 0 #0B0B14;box-sizing:border-box" />'
                     f'<div class="pat-benday" style="position:absolute;inset:0;opacity:.6"></div></div></div>')
        s._in(i, at, how, None, frm, y)
        if bob:
            s.js.append(f'COM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});')
        if out:
            s.out(name, out)
        return s

    def _in(s, i, at, how, rot, frm, y=800):
        a = s.t(at)
        if how == "pop":
            s.js.append(f'COM.popIn(tl, q("#{i}"), {a}, {{ rot: {rot or 0} }});')
        elif how == "drop":
            s.js.append(f'COM.dropIn(tl, q("#{i}"), {a}, {{ from: {-(y + 500)} }});')
        elif how == "slide":
            s.js.append(f'COM.slideIn(tl, q("#{i}"), {a}, "{frm}");')
        elif how == "slam":
            s.js.append(f'COM.panelSlam(tl, q("#{i}"), {a}, {{ from: "{frm}", rot: {rot or 4} }});')
        elif how == "stamp":
            s.js.append(f'COM.stamp(tl, q("#{i}"), {a}, {{ rot: {rot or 0} }});')

    # ---- cinta, caja narrador, globo, nube
    def cinta(s, name, txt, color="rojo", top=1200, rot=-6, at=None, out=None, left=-160, words=None):
        i = s.id(name)
        s.els.append(f'<div class="cinta cinta--{color}" id="{i}" style="left:{left}px;top:{top}px;--rot:{rot}deg"><span>{txt}</span></div>')
        if words:
            s.js.append(f'COM.wordPop(tl, q("#{i} span"), [{", ".join(s.t(w) for w in words)}]);')
        s.js.append(f'COM.stamp(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});')
        if out:
            s.out(name, out)
        return s

    def cap(s, name, txt, at, left=50, top=1330, width=560, out=None):
        i = s.id(name)
        s.els.append(f'<div class="cap" id="{i}" style="left:{left}px;top:{top}px;width:{width}px">{txt}</div>')
        s.js.append(f'COM.captionDrop(tl, q("#{i}"), {s.t(at)}, {{ text: {txt!r} }});'.replace("'", '"'))
        if out:
            s.js.append(f'COM.captionOut(tl, q("#{i}"), {s.t(out)} - 0.05);')
        return s

    def globo(s, name, txt, l, t, w, h, at, kind="globo", out=None, size=58, rot=-2):
        i = s.id(name)
        s.els.append(f'<div class="{kind}" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;font-size:{size}px;text-align:center;display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg)">{txt}</div>')
        s.js.append(f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});')
        if out:
            s.out(name, out)
        return s


    # ---- portada de cómic (HOOK y CTA)
    def cover(s, name, num, bg, inner, at=None, frm="T", out=None, rot=-1, tot=11):
        i = s.id(name)
        s.els.append(
            f'<div class="panel" id="{i}" style="left:90px;top:330px;width:900px;height:1090px;background:{HEX.get(bg, bg)};transform:rotate({rot}deg)">'
            '<div class="ttl ttl--amarillo ttl--sm" style="position:absolute;left:0;right:0;top:34px;text-align:center;--rot:-3deg;line-height:1">CAMINO A<br>DOOMSDAY</div>'
            f'<div style="position:absolute;left:36px;top:280px;padding:6px 18px;background:#FFF3D6;border:6px solid #0B0B14;font:400 64px Anton;color:#0B0B14;transform:rotate(-4deg)">N.º {num:02d} DE {tot}</div>'
            f'{inner}'
            '<div style="position:absolute;right:30px;top:250px;width:170px;height:170px;border-radius:50%;background:#E8212B;border:8px solid #0B0B14;display:flex;align-items:center;justify-content:center;font:400 52px Anton;color:#FFF3D6;transform:rotate(8deg)">GRATIS</div></div>')
        if at is not None:
            s.js.append(f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: 3 }});')
        if out:
            s.out(name, out)
        return s

    @staticmethod
    def cover_img(file, w=400, h=470, pos="center", x=450, y=600):
        return (f'<div class="c" style="left:{x}px;top:{y}px"><div style="width:{w}px;height:{h}px;position:relative"><img src="{IMG}{file}" '
                f'style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block;border:10px solid #0B0B14;box-shadow:10px 10px 0 #0B0B14;box-sizing:border-box" />'
                '<div class="pat-benday" style="position:absolute;inset:0;opacity:.6"></div></div></div>')

    # ---- efectos
    def speed(s, name, at, mode="radial", dirn="U", n=30, seed=3, dur=0.5, color="#FFF3D6"):
        i = s.id(name)
        s.els.append(f'<div class="speed" id="{i}"></div>')
        d = f', dir: "{dirn}"' if mode == "parallel" else ""
        s.js.append(f'COM.speedLines(tl, q("#{i}"), {s.t(at)}, {{ mode: "{mode}"{d}, n: {n}, seed: {seed}, dur: {dur}, color: "{color}" }});')
        return s

    def zoom(s, at, amt=1.2):
        s.js.append(f'COM.zoomGolpe(tl, q("#{s.P}"), {s.t(at)}, {{ amt: {amt} }});')
        return s

    def flash(s, at):
        s.js.append(f'COM.flashBlanco(tl, stage, {s.t(at)});')
        return s

    def shake(s, name, at, amp=12, dur=0.4):
        s.js.append(f'COM.shake(tl, q("#{s.id(name)}"), {s.t(at)}, {{ amp: {amp}, dur: {dur} }});')
        return s

    def pulse(s, name, at, to=1.12):
        s.js.append(f'COM.pulse(tl, q("#{s.id(name)}"), {s.t(at)}, {{ to: {to} }});')
        return s

    def spin(s, name, at, deg=140, dur=3):
        s.js.append(f'tl.fromTo(q("#{s.id(name)}"), {{ rotation: 0 }}, {{ rotation: {deg}, duration: {dur}, ease: "none" }}, {s.t(at)});')
        return s

    def move(s, name, at, x=0, y=0, rot=0, scale=1, dur=0.5, ease="power2.out"):
        s.js.append(f'tl.to(q("#{s.id(name)}"), {{ x: {x}, y: {y}, rotation: {rot}, scale: {scale}, duration: {dur}, ease: "{ease}" }}, {s.t(at)});')
        return s

    def slab(s, name, color, at, until, pat=True):
        """golpe de color a pantalla completa (≤ 1.5 s)"""
        i = s.id(name)
        s.els.append(f'<div id="{i}" class="{"pat-benday-fuerte" if pat else ""}" style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:{HEX.get(color, color)}"></div>')
        s.js.append(f'tl.fromTo(q("#{i}"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {s.t(at)});')
        s.js.append(f'tl.to(q("#{i}"), {{ opacity: 0, duration: 0.15 }}, {s.t(until)});')
        return s

    def draw(s, name, d, color, at, w=16, dur=0.4, dash=None):
        """trazo SVG en coordenadas de pantalla (1080x1920) que se dibuja"""
        i = s.id(name)
        da = f'stroke-dasharray="{dash}"' if dash else 'stroke-dasharray="1" stroke-dashoffset="1"'
        s.els.append(f'<svg style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible" viewBox="0 0 1080 1920"><path id="{i}" d="{d}" fill="none" stroke="{HEX.get(color, color)}" stroke-width="{w}" stroke-linecap="round" pathLength="1" {da}/></svg>')
        s.js.append(f'COM.drawOn(tl, q("#{i}"), {s.t(at)}, {{ dur: {dur} }});')
        return s

    # ---- salida
    def html(s):
        return (f'          <section class="scene" id="{s.P}">\n'
                f'            <div class="bg {BG[s.bg]} {s.pat}"></div>\n'
                f'            <div class="cam"><div class="rig">\n'
                + "\n".join("              " + e for e in s.els) +
                '\n            </div></div>\n          </section>')

    def script(s):
        enter = (f'COM.scene(tl, q("#{s.P}"), E("{s.n}")[0], E("{s.n}")[1], '
                 f'{{ enter: "{s.enter}", color: COM.C.{s.color}, x: {s.x}, y: {s.y} }});')
        return enter + "\n" + "\n".join(s.js)


class Episode:
    def __init__(s, num, slug, titulo, palabras, dias=36, cont_in="2.1", cont_pulse=None):
        s.num, s.slug, s.titulo, s.palabras = f"{num:02d}", slug, titulo, palabras
        s.dias, s.cont_in, s.cont_pulse = dias, cont_in, cont_pulse
        s.scenes = []

    def scene(s, *a, **k):
        sc = Scene(s, len(s.scenes) + 1, *a, **k)
        s.scenes.append(sc)
        return sc

    # motion-script.md mínimo para `tiempos`
    def motion_script(s):
        out = [f"# Motion script · {s.num} · {s.titulo}\n",
               f"- **Guion**: `guion-tts.md` ({s.palabras} palabras, voz \"narrador comics\")",
               "- **Estilo**: `../_estilo.md` (cómic que se mueve, sin Moni). Generado desde `_motion/compositions/camino-a-doomsday/_gen/eps/ep" + s.num + ".py` (fuente de verdad: edita ahí y corre `_gen/build.py`).",
               f"- **Contador**: `FALTAN {s.dias} DÍAS` (recalcular al publicar).\n", "---\n"]
        for sc in s.scenes:
            out.append(f"## Escena {sc.n} · {sc.nombre} · {sc.seg} · \n")
            out.append("| # | t (s) | Voz (disparador) | Visual |\n|---|---|---|---|")
            for bid, t, voz, nota in sc.beats:
                out.append(f'| {bid} | {t} | "{voz}" | {nota} |')
            out.append("")
        return "\n".join(out)

    def composition(s, dur):
        P = f"v{s.num}"
        cid = f"camino-a-doomsday-{s.num}-{s.slug}"
        html = "\n".join(sc.html() for sc in s.scenes)
        js = "\n".join(f"          // ===== escena {sc.n} =====\n          {{\n{sc.script()}\n          }}" for sc in s.scenes)
        cp = (f'COM.counterPulse(tl, q("#{P}-cont"), b("{s.cont_pulse}"));' if s.cont_pulse else "")
        return f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>{s.num}-{s.slug}</title>
  </head>
  <body>
    <template id="{cid}">
      <link rel="stylesheet" href="shared/explicando.css" />
      <link rel="stylesheet" href="shared/comic.css" />
      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script src="shared/explicando.js"></script>
      <script src="shared/comic-objects.js"></script>
      <script src="shared/comic.js"></script>
      <script src="assets/timings/camino-a-doomsday/{s.num}-{s.slug}.js"></script>
      <style>
        #{P}-root {{ position: absolute; inset: 0; }}
        #{P}-root .c {{ position: absolute; width: 0; height: 0; display: flex; align-items: center; justify-content: center; }}
        #{P}-root .c > * {{ flex: none; }}
      </style>

      <div id="{P}-root" data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-exp="dur" data-width="1080" data-height="1920">
        <div class="exp-stage" id="{P}-stage">
{html}
          <div class="contador" id="{P}-cont">FALTAN {s.dias} DÍAS</div>
        </div>
        <audio id="{P}-vo" src="assets/audio/camino-a-doomsday/{s.num}-{s.slug}.wav" data-start="0" data-duration="{dur}" data-exp="dur" data-track-index="9"></audio>
      </div>

      <script>
        (function () {{
          const ID = "{cid}";
          const T = EXP.T(ID);
          const b = (id, off) => EXP.beat(T, id, off);
          const E = (n) => T.e[n];
          const root = document.querySelector('[data-composition-id="' + ID + '"]');
          const stage = root.querySelector(".exp-stage");
          const q = EXP.q(root), qa = EXP.qa(root);
          const tl = gsap.timeline({{ paused: true }});
          const ch = COM.chrome(tl, stage, T);
          COM.counter(tl, q("#{P}-cont"), b("{s.cont_in}", 0.15), {s.dias});
          {cp}
{js}
          window.__timelines[ID] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''


# ---- dibujos SVG sueltos (coordenadas propias, se meten con Scene.pobj-like via svgbox)
INK = "#0B0B14"


def svgbox(vb, inner, w, h, extra=""):
    return (f'<div class="c" style="position:relative"><svg viewBox="{vb}" style="width:{w}px;height:{h}px;overflow:visible;{extra}">{inner}</svg></div>')


def S(w=8):
    return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def portal(w=520, colors=("#8A2BE2", "#00C8E8", "#FFD400", "#FFF3D6")):
    """portales concéntricos (multiverso)"""
    r = [200, 150, 100, 52]
    inner = "".join(f'<circle cx="200" cy="200" r="{rr}" fill="{c}" {S(8)}/>' for rr, c in zip(r, colors))
    return svgbox("0 0 400 400", inner, w, w)


def building(w=520, label="UNI"):
    """edificio con frontón y columnas (universidad)"""
    cols = "".join(f'<rect x="{50+k*60}" y="120" width="34" height="140" fill="#FFF3D6" {S(7)}/>' for k in range(5))
    inner = (f'<polygon points="20,120 190,20 360,120" fill="#FFD400" {S(8)}/>'
             f'<rect x="20" y="120" width="340" height="24" fill="#6B7280" {S(8)}/>{cols}'
             f'<rect x="10" y="260" width="360" height="30" fill="#6B7280" {S(8)}/>'
             f'<circle cx="190" cy="76" r="22" fill="#E8212B" {S(7)}/>')
    return svgbox("0 0 380 300", inner, w, int(w * 300 / 380))


_AM, _RO, _PA, _HE, _MU, _CI, _DO, _CE = "#FFD400", "#E8212B", "#FFF3D6", "#1E5BFF", "#8A2BE2", "#00C8E8", "#1FA85A", "#6B7280"


def knife(w=300):
    inner = (f'<path d="M40 40 L300 250 L270 290 L20 90 Z" fill="{_PA}" {S(8)}/>'
             f'<path d="M270 290 L330 230 L360 260 L300 330 Z" fill="{_RO}" {S(8)}/>'
             f'<path d="M300 250 L330 230" {S(8)}/>')
    return svgbox("0 0 380 350", inner, w, int(w * 350 / 380))


def loki_helmet(w=360):
    inner = (f'<path d="M110 120 C60 100 40 40 70 10 C60 60 100 80 130 90 Z" fill="{_AM}" {S(8)}/>'
             f'<path d="M290 120 C340 100 360 40 330 10 C340 60 300 80 270 90 Z" fill="{_AM}" {S(8)}/>'
             f'<path d="M100 130 C100 60 300 60 300 130 L290 250 C270 300 130 300 110 250 Z" fill="{_DO}" {S(8)}/>'
             f'<path d="M120 130 C150 100 250 100 280 130 L270 190 L200 160 L130 190 Z" fill="{_AM}" {S(8)}/>'
             f'<path d="M200 160 L200 280" {S(8)}/>')
    return svgbox("0 0 400 320", inner, w, int(w * 320 / 400))


def gamepad(w=420):
    inner = (f'<path d="M80 100 C30 100 10 230 40 260 C70 290 110 240 150 220 L270 220 C310 240 350 290 380 260 C410 230 390 100 340 100 Z" fill="{_HE}" {S(9)}/>'
             f'<rect x="75" y="150" width="70" height="22" fill="{_PA}" {S(6)}/><rect x="99" y="126" width="22" height="70" fill="{_PA}" {S(6)}/>'
             f'<circle cx="300" cy="150" r="20" fill="{_RO}" {S(6)}/><circle cx="345" cy="175" r="20" fill="{_AM}" {S(6)}/>')
    return svgbox("0 0 420 300", inner, w, int(w * 300 / 420))


def floppy(w=300):
    inner = (f'<rect x="20" y="20" width="260" height="260" rx="14" fill="{_CI}" {S(9)}/>'
             f'<rect x="70" y="20" width="150" height="90" fill="{_PA}" {S(7)}/><rect x="170" y="35" width="30" height="60" fill="{INK}"/>'
             f'<rect x="60" y="160" width="180" height="120" fill="{_PA}" {S(7)}/>'
             f'<path d="M90 195 H210 M90 225 H210" {S(6)}/>')
    return svgbox("0 0 300 300", inner, w, w)


def spidey(w=300):
    ln = "".join(f'<path d="{d}" {S(5)} fill="none"/>' for d in ("M150 20 V280", "M20 150 H280", "M45 45 L255 255", "M255 45 L45 255"))
    ring = "".join(f'<circle cx="150" cy="150" r="{r}" fill="none" {S(5)}/>' for r in (50, 95))
    inner = (f'<ellipse cx="150" cy="150" rx="125" ry="140" fill="{_RO}" {S(9)}/>{ln}{ring}'
             f'<path d="M60 130 C90 90 130 140 140 160 C110 175 70 165 60 130 Z" fill="{_PA}" {S(7)}/>'
             f'<path d="M240 130 C210 90 170 140 160 160 C190 175 230 165 240 130 Z" fill="{_PA}" {S(7)}/>')
    return svgbox("0 0 300 300", inner, w, w)


def globe(w=380, color=_HE):
    inner = (f'<circle cx="200" cy="200" r="170" fill="{color}" {S(10)}/>'
             f'<path d="M110 130 C150 90 200 120 190 160 C180 200 130 190 110 130 Z M230 220 C280 200 310 240 270 290 C230 300 210 260 230 220 Z" fill="{_DO}" {S(7)}/>'
             f'<ellipse cx="200" cy="200" rx="170" ry="60" fill="none" {S(5)}/><path d="M200 30 V370" {S(5)}/>')
    return svgbox("0 0 400 400", inner, w, w)


def branches(w=900, h=500):
    """línea que se ramifica (multi colores); paths con clase .br para drawOn"""
    cols = [_MU, _CI, _AM, _RO, _DO, _PA]
    ds = ["M20 250 H300", "M300 250 C400 250 420 120 600 100 H880", "M300 250 C420 250 460 190 620 190 H880",
          "M300 250 H880", "M300 250 C420 250 460 320 620 330 H880", "M300 250 C400 250 420 380 600 400 H880"]
    inner = "".join(f'<path class="br" d="{d}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>'
                    f'<path class="br" d="{d}" fill="none" stroke="{c}" stroke-width="16" stroke-linecap="round"/>' for d, c in zip(ds, cols))
    return svgbox("0 0 900 500", inner, w, h)


def eye(w=360):
    inner = (f'<path d="M20 100 C80 10 220 10 280 100 C220 190 80 190 20 100 Z" fill="{_PA}" {S(9)}/>'
             f'<circle cx="150" cy="100" r="48" fill="{_MU}" {S(8)}/><circle cx="150" cy="100" r="18" fill="{INK}"/>')
    return svgbox("0 0 300 200", inner, w, int(w * 200 / 300))


def car(w=420, color="#E8212B", flip=False):
    fl = ' transform="translate(400 0) scale(-1 1)"' if flip else ""
    inner = (f'<g{fl}><path d="M20 150 L40 100 C60 80 90 80 110 80 L200 80 C240 80 270 110 300 130 L380 140 C395 145 395 170 380 175 L30 175 C15 175 15 160 20 150 Z" fill="{color}" {S(9)}/>'
             f'<path d="M120 90 L195 90 C225 90 245 110 265 128 L120 128 Z" fill="{_CI}" {S(7)}/>'
             f'<circle cx="100" cy="178" r="30" fill="{INK}"/><circle cx="100" cy="178" r="12" fill="{_PA}"/>'
             f'<circle cx="310" cy="178" r="30" fill="{INK}"/><circle cx="310" cy="178" r="12" fill="{_PA}"/></g>')
    return svgbox("0 0 400 220", inner, w, int(w * 220 / 400))


def mosaic(w=620):
    """planeta-mosaico (Battleworld): círculo de 9 pedazos de colores; cada pedazo .pz"""
    import math
    cols = [_HE, _MU, _CI, _RO, _DO, _AM, _PA, _CE, _MU]
    out = ""
    for k in range(9):
        a0, a1 = 2 * math.pi * k / 9, 2 * math.pi * (k + 1) / 9
        x0, y0, x1, y1 = 200 + 170 * math.cos(a0), 200 + 170 * math.sin(a0), 200 + 170 * math.cos(a1), 200 + 170 * math.sin(a1)
        out += f'<path class="pz" d="M200 200 L{x0:.1f} {y0:.1f} A170 170 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{cols[k]}" {S(8)}/>'
    return svgbox("0 0 400 400", out, w, w)


def throne(w=420):
    inner = (f'<path d="M70 380 V120 C70 20 330 20 330 120 V380 Z" fill="{_AM}" {S(9)}/>'
             f'<path d="M105 360 V130 C105 60 295 60 295 130 V360 Z" fill="{_MU}" {S(7)}/>'
             f'<rect x="40" y="290" width="320" height="50" rx="10" fill="{_AM}" {S(9)}/>'
             f'<rect x="40" y="200" width="46" height="100" rx="10" fill="{_AM}" {S(9)}/><rect x="314" y="200" width="46" height="100" rx="10" fill="{_AM}" {S(9)}/>'
             f'<circle cx="200" cy="60" r="16" fill="{_RO}" {S(6)}/>')
    return svgbox("0 0 400 400", inner, w, w)


def flame(w=200, c1=_RO, c2=_AM):
    inner = (f'<path d="M100 10 C130 70 190 100 170 170 C155 220 45 220 30 170 C10 110 70 80 100 10 Z" fill="{c1}" {S(8)}/>'
             f'<path d="M100 90 C115 120 145 135 135 170 C125 200 75 200 65 170 C58 140 90 125 100 90 Z" fill="{c2}" {S(6)}/>')
    return svgbox("0 0 200 230", inner, w, int(w * 230 / 200))


def tree(w=760, h=900):
    cols = [_MU, _CI, _AM, _RO, _DO, _PA]
    br = ["M400 760 C400 600 400 520 400 420", "M400 520 C330 470 250 440 150 330", "M400 520 C470 470 550 440 650 330",
          "M400 440 C360 360 330 280 300 120", "M400 440 C440 360 470 280 500 120", "M400 420 C400 330 400 230 400 60"]
    inner = f'<path class="tr" d="M400 860 C395 800 405 780 400 760" fill="none" stroke="{INK}" stroke-width="64" stroke-linecap="round"/><path class="tr" d="M400 860 C395 800 405 780 400 760" fill="none" stroke="#8B5A2B" stroke-width="44" stroke-linecap="round"/>'
    for d, c in zip(br, cols):
        inner += f'<path class="tr" d="{d}" fill="none" stroke="{INK}" stroke-width="46" stroke-linecap="round"/><path class="tr" d="{d}" fill="none" stroke="{c}" stroke-width="26" stroke-linecap="round"/>'
    for x, y, c in ((150, 330, _CI), (650, 330, _RO), (300, 120, _AM), (500, 120, _DO), (400, 60, _PA)):
        inner += f'<circle class="lf" cx="{x}" cy="{y}" r="46" fill="{c}" {S(8)}/>'
    return svgbox("0 0 800 900", inner, w, h)


def cycle(w=400):
    inner = (f'<path d="M60 150 A100 100 0 1 1 150 250" fill="none" {S(36)}/><path d="M60 150 A100 100 0 1 1 150 250" fill="none" stroke="{_AM}" stroke-width="20" stroke-linecap="round"/>'
             f'<polygon points="20,140 100,140 60,210" fill="{_AM}" {S(8)}/>')
    return svgbox("0 0 300 300", inner, w, w)


def shield(w=420):
    inner = (f'<circle cx="200" cy="200" r="180" fill="{_RO}" {S(9)}/><circle cx="200" cy="200" r="135" fill="{_PA}" {S(7)}/>'
             f'<circle cx="200" cy="200" r="95" fill="{_RO}" {S(7)}/><circle cx="200" cy="200" r="58" fill="{_HE}" {S(7)}/>'
             f'<polygon points="200,150 213,188 252,188 220,211 232,250 200,226 168,250 180,211 148,188 187,188" fill="{_PA}" {S(5)}/>')
    return svgbox("0 0 400 400", inner, w, w)


def power(kind, w=300):
    if kind == "stretch":
        inner = f'<path d="M20 150 C60 40 100 260 140 150 C180 40 220 260 260 150 L330 150" fill="none" {S(34)}/><path d="M20 150 C60 40 100 260 140 150 C180 40 220 260 260 150 L330 150" fill="none" stroke="{_CI}" stroke-width="18" stroke-linecap="round"/><circle cx="330" cy="150" r="26" fill="{_PA}" {S(8)}/>'
    elif kind == "force":
        inner = f'<circle cx="150" cy="150" r="125" fill="{_CI}" fill-opacity=".35" {S(9)}/><circle cx="150" cy="150" r="85" fill="none" stroke="{INK}" stroke-width="9" stroke-dasharray="22 16"/><circle cx="150" cy="150" r="35" fill="{_PA}" {S(8)}/>'
    elif kind == "rock":
        inner = f'<path d="M40 230 L30 130 L90 50 L190 40 L260 100 L275 210 L210 265 L90 265 Z" fill="{_CE}" {S(10)}/><path d="M90 50 L110 130 L190 40 M110 130 L130 215 L210 265 M110 130 L30 130" fill="none" {S(7)}/>'
    else:
        return flame(int(w * .8))
    return svgbox("0 0 340 300", inner, w, int(w * 300 / 340))


def wings(w=520, color=_RO):
    wing = (f'<path d="M200 150 C150 60 70 40 10 60 C40 80 50 110 30 135 C60 135 80 150 70 175 C100 170 120 185 115 205 C150 195 180 190 200 200 Z" fill="{color}" {S(9)}/>'
            f'<path d="M50 90 L190 170 M40 125 L185 185" fill="none" {S(5)}/>')
    inner = wing + f'<g transform="translate(400 0) scale(-1 1)">{wing}</g><circle cx="200" cy="190" r="22" fill="{_PA}" {S(8)}/>'
    return svgbox("0 0 400 240", inner, w, int(w * 240 / 400))


def dumbbell(w=420):
    inner = (f'<rect x="90" y="120" width="220" height="40" fill="{_CE}" {S(9)}/>'
             f'<rect x="40" y="60" width="50" height="160" rx="10" fill="{_RO}" {S(9)}/><rect x="310" y="60" width="50" height="160" rx="10" fill="{_RO}" {S(9)}/>'
             f'<rect x="10" y="90" width="30" height="100" rx="8" fill="{_CE}" {S(8)}/><rect x="360" y="90" width="30" height="100" rx="8" fill="{_CE}" {S(8)}/>')
    return svgbox("0 0 400 280", inner, w, int(w * 280 / 400))


def hulk(w=520, color=_RO):
    inner = (f'<path d="M110 160 C90 40 310 40 290 160 C285 210 115 210 110 160 Z" fill="{color}" {S(10)}/>'
             f'<path d="M60 260 C20 330 10 420 60 470 L340 470 C390 420 380 330 340 260 C320 215 280 205 200 205 C120 205 80 215 60 260 Z" fill="{color}" {S(10)}/>'
             f'<circle cx="40" cy="420" r="55" fill="{color}" {S(10)}/><circle cx="360" cy="420" r="55" fill="{color}" {S(10)}/>'
             f'<path d="M135 120 L190 150 M265 120 L210 150" {S(12)}/><path d="M150 180 L250 180" {S(8)}/>')
    return svgbox("0 0 400 480", inner, w, int(w * 480 / 400))


def armband(w=640):
    inner = (f'<rect x="20" y="30" width="360" height="160" rx="12" fill="{_AM}" {S(10)}/>'
             f'<rect x="20" y="30" width="360" height="30" fill="{_RO}" {S(8)}/><rect x="20" y="160" width="360" height="30" fill="{_RO}" {S(8)}/>'
             f'<text x="200" y="150" text-anchor="middle" font-family="Anton" font-size="120" fill="{INK}">C</text>')
    return svgbox("0 0 400 220", inner, w, int(w * 220 / 400))


def check(w=300, color=_HE):
    inner = f'<circle cx="150" cy="150" r="130" fill="{color}" {S(10)}/><path d="M85 155 L135 205 L220 100" fill="none" stroke="{_PA}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
    return svgbox("0 0 300 300", inner, w, w)


def boot(w=420, color=_RO):
    inner = (f'<path d="M80 20 H190 V150 C190 180 260 180 310 205 C350 225 350 270 310 270 H50 C20 270 20 245 30 230 L80 150 Z" fill="{color}" {S(10)}/>'
             f'<rect x="20" y="255" width="330" height="26" rx="8" fill="{_PA}" {S(8)}/><path d="M110 60 H170 M110 95 H170" {S(7)}/>')
    return svgbox("0 0 370 300", inner, w, int(w * 300 / 370))


def xlogo(w=420):
    inner = (f'<path d="M60 40 L340 360 M340 40 L60 360" stroke="{INK}" stroke-width="110" stroke-linecap="round"/>'
             f'<path d="M60 40 L340 360 M340 40 L60 360" stroke="{_AM}" stroke-width="80" stroke-linecap="round"/>')
    return svgbox("0 0 400 400", inner, w, w)


def magnet(w=300):
    inner = (f'<path d="M60 40 V190 C60 300 240 300 240 190 V40" fill="none" {S(70)}/><path d="M60 40 V190 C60 300 240 300 240 190 V40" fill="none" stroke="{_RO}" stroke-width="46"/>'
             f'<rect x="25" y="20" width="70" height="60" fill="{_PA}" {S(8)}/><rect x="205" y="20" width="70" height="60" fill="{_PA}" {S(8)}/>')
    return svgbox("0 0 300 320", inner, w, int(w * 320 / 300))


def visor(w=300):
    inner = (f'<ellipse cx="150" cy="130" rx="85" ry="105" fill="{_PA}" {S(9)}/><rect x="60" y="100" width="180" height="34" rx="10" fill="{_RO}" {S(8)}/>'
             f'<path d="M240 117 H300" stroke="{_RO}" stroke-width="22" stroke-linecap="round"/><path d="M60 235 C90 310 210 310 240 235 Z" fill="{_HE}" {S(9)}/>')
    return svgbox("0 0 320 300", inner, w, int(w * 300 / 320))


def smoke(w=300, txt="BAMF"):
    inner = (f'<circle cx="110" cy="170" r="80" fill="{_MU}" {S(9)}/><circle cx="190" cy="140" r="90" fill="{_MU}" {S(9)}/><circle cx="170" cy="210" r="75" fill="{_HE}" {S(9)}/>'
             f'<text x="150" y="190" text-anchor="middle" font-family="Bangers" font-size="62" fill="{_AM}" stroke="{INK}" stroke-width="6" paint-order="stroke">{txt}</text>')
    return svgbox("0 0 300 300", inner, w, w)


def card(w=260):
    inner = (f'<rect x="40" y="20" width="200" height="280" rx="18" fill="{_PA}" {S(9)}/>'
             f'<text x="70" y="85" font-family="Anton" font-size="64" fill="{_RO}">A</text>'
             f'<path d="M140 120 C100 170 90 200 125 210 C135 212 140 205 140 205 C140 205 145 212 155 210 C190 200 180 170 140 120 Z" fill="{_RO}" {S(6)}/>')
    return svgbox("0 0 280 320", inner, w, int(w * 320 / 280))


def mic(w=260):
    inner = (f'<rect x="90" y="20" width="120" height="190" rx="60" fill="{_CE}" {S(9)}/><path d="M90 90 H210 M90 130 H210" {S(6)}/>'
             f'<path d="M60 130 C60 260 240 260 240 130" fill="none" {S(12)}/><path d="M150 245 V300 M100 305 H200" {S(12)}/>')
    return svgbox("0 0 300 330", inner, w, int(w * 330 / 300))


def dpmask(w=300):
    inner = (f'<ellipse cx="150" cy="160" rx="110" ry="135" fill="{_RO}" {S(10)}/>'
             f'<path d="M60 130 C85 90 120 110 125 160 C100 195 65 180 60 130 Z" fill="{INK}"/><path d="M240 130 C215 90 180 110 175 160 C200 195 235 180 240 130 Z" fill="{INK}"/>'
             f'<ellipse cx="97" cy="140" rx="17" ry="11" fill="{_PA}" transform="rotate(-20 97 140)"/><ellipse cx="203" cy="140" rx="17" ry="11" fill="{_PA}" transform="rotate(20 203 140)"/>')
    return svgbox("0 0 300 320", inner, w, int(w * 320 / 300))


def claws(w=300):
    inner = "".join(f'<path d="M{40+k*80} 30 L{110+k*80} 270" stroke="{INK}" stroke-width="56" stroke-linecap="round"/><path d="M{40+k*80} 30 L{110+k*80} 270" stroke="{_AM}" stroke-width="34" stroke-linecap="round"/>' for k in range(3))
    return svgbox("0 0 340 300", inner, w, int(w * 300 / 340))


def board(w=520):
    sq = "".join(f'<rect x="{i*100}" y="{j*100}" width="100" height="100" fill="{_PA if (i+j)%2 else _CE}"/>' for i in range(4) for j in range(4))
    inner = sq + f'<rect x="0" y="0" width="400" height="400" fill="none" {S(10)}/>'
    return svgbox("-5 -5 410 410", inner, w, w)


def listicon(w=300):
    rows = "".join(f'<rect x="60" y="{70+k*80}" width="36" height="36" fill="{_PA}" {S(7)}/><path d="M66 {88+k*80} L77 {100+k*80} L95 {74+k*80}" fill="none" stroke="{_HE}" stroke-width="9" stroke-linecap="round"/><path d="M120 {88+k*80} H240" {S(10)}/>' for k in range(3))
    inner = f'<rect x="30" y="20" width="240" height="300" rx="14" fill="{_AM}" {S(10)}/>' + rows
    return svgbox("0 0 300 340", inner, w, int(w * 340 / 300))


def pho(file, pos="50% 20%", label=None, size=54, lc="#FFD400", sub=None):
    """foto que llena la viñeta (object-fit cover) con trama y, opcional, banda de tinta abajo con el nombre"""
    h = f'<img src="{IMG}{file}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};display:block" />'
    h += '<div class="pat-benday" style="position:absolute;inset:0;opacity:.3"></div>'
    if label:
        sb = f'<span style="display:block;font:700 {int(size*0.5)}px/1.1 Comic Neue,cursive;color:#FFF3D6;letter-spacing:1px">{sub}</span>' if sub else ""
        h += (f'<div style="position:absolute;left:0;right:0;bottom:0;padding:10px 6px 12px;background:#0B0B14;text-align:center;font:400 {size}px/1 Anton;color:{lc}">{label}{sb}</div>')
    return h
