"""Piezas comunes: Equipos y duelos de Avengers: Doomsday.

im(id)                     archivo (relativo a assets/img) de un id del manifiesto
tag(s, k, at)              sello de veracidad arriba a la izquierda
still(s, name, id, box, at, kb)   imagen con ken burns
frame(src, t)              fotograma de una fuente de video → archivo relativo a assets/img (cacheado)
clipsc(S, i)               escena casi a pantalla completa del i-ésimo clip CON AUDIO de la sección
tv(s, name, src, tin, at, dur, box)  trozo de video sin audio dentro de una viñeta
barra(s, name, label, val, color, l, t, w, at)   barra de poder 1-10
vs(S, t, a, an, b, bn, bg)  pantalla VS partida (abre cada duelo)
"""
import json
import subprocess
from pathlib import Path

VID = Path(__file__).resolve().parents[2]

# S.w acepta el nombre original o su forma TTS: si no encuentra la frase, reintenta con base/pronunciacion.json
import re as _re
import lib_h as _lh
_ROOT = VID.parents[1]
_PR = sorted(json.loads((_ROOT / "base/pronunciacion.json").read_text())["reglas"]
             + json.loads((VID / "video.json").read_text()).get("pronunciacion", []), key=lambda r: -len(r[0]))


# palabra suelta → su forma TTS, sacada de reglas de igual número de palabras («Kate Bishop» → «Kéit Bíshop» da Kate → Kéit)
_PW = {}
for _a, _b in _PR:
    if len(_a.split()) == len(_b.split()):
        for _x, _y in zip(_a.split(), _b.split()):
            _PW.setdefault(_x, _y)


def _tts(p):
    for a, b in _PR:
        p = _re.sub(r"(?<!\w)" + _re.escape(a) + r"(?!\w)", b, p)
    return p


def _tts_w(p):
    return " ".join(_PW.get(x, x) for x in p.split())


if not getattr(_lh.Sec, "_tts_ok", False):
    _w0 = _lh.Sec.w

    def _w(s, phrase, off=0.0, again=False):
        if s._find(phrase, s.cur) is None:
            for alt in (_tts(phrase), _tts_w(phrase), _tts_w(_tts(phrase))):
                if alt != phrase and s._find(alt, s.cur) is not None:
                    phrase = alt
                    break
        return _w0(s, phrase, off, again)
    _lh.Sec.w = _w
    _lh.Sec._tts_ok = True
_M = {x["id"]: x["archivo"][4:] for x in json.loads((VID / "assets/manifest.json").read_text())["imagenes"]}

ESTADO = {"C": ("CONFIRMADO", "heroe"), "T": ("TEORÍA", "multi"), "L": ("LECTURA", "rojo"),
          "K": ("DATO DE CÓMIC", "doom"), "F": ("FILTRACIÓN", "rojo")}
_n = [0]
FULL = (130, 60, 1660, 934)
TR = "lf04-trailer.mp4"          # tráiler final (subtítulos ES quemados abajo)
T1 = "lf-t07-thor-mjolnir.mp4"   # primer tráiler: Thor vs Doom, Stormbreaker detenida


def im(i, alt=None):
    if i in _M:
        return _M[i]
    if alt and alt in _M:
        return _M[alt]
    raise SystemExit(f"imagen '{i}' no está en el manifiesto")


def tag(s, k, at, out=None, x=230, y=90, size=42):
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, x, y, at, color=col, rot=-5, size=size, out=out)
    return s


def frame(src, t):
    name = f"lf/fr/{Path(src).stem}-{t:.2f}.jpg"
    dst = VID / "assets/img" / name
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", str(VID / "assets/video" / src),
                        "-frames:v", "1", "-q:v", "3", str(dst), "-y"], check=True)
    return name


def still(s, name, i, box, at, kb=None, frm="R", label=None, pos="50% 50%", scale=1.12, x=0, y=0, rot=0, alt=None):
    l, t, w, h = box
    s.img(name, im(i, alt), l, t, w, h, at, frm=frm, pos=pos, label=label, rot=rot)
    if kb:
        s.kenburns(name, at + 0.2, kb, scale=scale, x=x, y=y)
    return s


def fstill(s, name, src, t, box, at, kb=None, frm="R", label=None, pos="50% 40%", scale=1.12):
    """fotograma de video como imagen fija (recorta los subtítulos con pos alto)."""
    l, tp, w, h = box
    s.img(name, frame(src, t), l, tp, w, h, at, frm=frm, pos=pos, label=label)
    if kb:
        s.kenburns(name, at + 0.2, kb, scale=scale)
    return s


def tv(s, name, src, tin, at, dur, box=FULL, tag_txt="TRÁILER FINAL", frm="R", slam=False, pos="50% 35%"):
    l, t, w, h = box
    s.video(name, src, tin, at, dur, l, t, w, h, tag=tag_txt, frm=frm, slam=slam, pos=pos)
    return s


def clipsc(S, i, bg="tinta", enter="ink", box=FULL, cap=None, cap_at=0.8, tag_txt="TRÁILER"):
    c = S.clip(i)
    s = S.scene(c["start"] - 0.3, bg=bg, enter=enter)
    l, t, w, h = box
    d = c["end"] - c["start"]
    s.panel(f"fa{i}", f'<img src="assets/img/{frame(c["src"], c["in"] + 0.05)}" style="width:100%;height:100%;object-fit:cover" />', l, t, w, h, "tinta", 0, s.start + 0.02, "B")
    s.panel(f"fz{i}", f'<img src="assets/img/{frame(c["src"], c["in"] + d - 0.08)}" style="width:100%;height:100%;object-fit:cover" />', l, t, w, h, "tinta", 0, None, "B", sfx=False)
    s.js.append(f'tl.fromTo(q("#{s.id(f"fz{i}")}"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.01 }}, {s.T(c["end"] - 0.02)});')
    s.video(f"clip{i}", c["src"], c["in"], c["start"], d, l, t, w, h, tag=tag_txt, frm="B", slam=False, bg="transparent")
    if cap:
        s.cap(f"cap{i}", cap, c["start"] + cap_at, left=60, top=60, width=900)
    return s, c


COL = {"amarillo": "#FFD400", "rojo": "#E8212B", "heroe": "#1E5BFF", "doom": "#1FA85A", "multi": "#8A2BE2",
       "ciencia": "#00C8E8", "ceniza": "#6B7280"}


def barra(s, name, label, val, color, l, t, w, at, h=74, lsize=40):
    """barra de poder: etiqueta + 10 segmentos que se llenan hasta val."""
    i = s.id(name)
    segs = "".join(f'<div style="flex:1;margin:0 3px;background:{COL[color] if k < val else "#FFF3D6"};'
                   f'border:4px solid #0B0B14" class="sg"></div>' for k in range(10))
    s.els.append(
        f'<div class="panel" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;background:#0B0B14;'
        f'display:flex;align-items:center;padding:8px 12px;box-sizing:border-box">'
        f'<div style="font:400 {lsize}px/1 Anton;color:#FFF3D6;width:34%;white-space:nowrap;overflow:hidden">{label}</div>'
        f'<div style="display:flex;flex:1;height:100%">{segs}</div>'
        f'<div style="font:400 {lsize + 6}px/1 Anton;color:{COL[color]};width:70px;text-align:right">{val}</div></div>')
    s.js.append(f'COM.panelSlam(tl, q("#{i}"), {s.T(at)}, {{ from: "L", rot: 0 }});')
    s.js.append(f'tl.from(q("#{i} .sg"), {{ scaleY: 0, transformOrigin: "50% 100%", duration: 0.18, stagger: 0.04, ease: "back.out(2)" }}, {s.T(at + 0.25)});')
    s.sfx("whoosh", at, -10)
    return s


def vs(S, t, a, an, b, bn, n, bg="rojo", posa="50% 25%", posb="50% 25%"):
    """pantalla VS que abre el duelo n: a (izquierda, héroes) vs b (derecha)."""
    s = S.scene(t, bg=bg, enter="pageflip")
    s.speed("sp", t + 0.05, mode="radial")
    s.img("va", im(a), 60, 150, 820, 760, t + 0.05, frm="L", pos=posa, label=an, rot=-3)
    s.img("vb", im(b), 1040, 150, 820, 760, t + 0.35, frm="R", pos=posb, label=bn, rot=3)
    s.text("vs", "VS", "ttl", "amarillo", 960, 520, t + 0.6, size=260, rot=-8, misreg=True)
    s.text("dn", f"DUELO {n} / 7", "kw", "papel", 960, 80, t + 0.1, size=72, rot=-2, sfx=False)
    s.sfx("braam", t + 0.6, -8)
    return s


def fondo(s, name, i, at, until, dim=0.4, src_t=None, scale=1.08, pos="50% 40%"):
    """imagen a pantalla completa, oscurecida, para que la escena no arranque vacía (id del manifiesto o (src, t) de video)."""
    f = frame(*i) if isinstance(i, tuple) else im(i)
    s.panel(name, f'<img src="assets/img/{f}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};filter:brightness({dim}) saturate(.8)" />',
            0, 0, 1920, 1080, "tinta", 0, at, "B", sfx=False, prot=0)
    s.kenburns(name, at + 0.1, until, scale=scale)
    return s
