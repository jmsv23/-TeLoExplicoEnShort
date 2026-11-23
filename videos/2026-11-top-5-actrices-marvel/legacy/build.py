#!/usr/bin/env python3
"""Genera el proyecto HyperFrames (estilo "Portada") desde timeline-<pieza>.json + escenas_<pieza>.py.

    python3 build.py largo          # prepara assets + escribe hf-largo/index.html y compositions/*.html
    python3 build.py short

Arquitectura igual que james-bond/_prod/build.py: cada sección es una sub-composición. Los planos se encadenan
con transiciones causadas por algo en pantalla (pase de página, flash de cámara, foto que crece, iris, látigo).
Los elementos aparecen cuando la voz los nombra. Los videos van mudos: su audio ya está en master.wav.
"""
import html, importlib, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROY = HERE.parent
A_IMG, A_CUT = PROY / "assets/img", PROY / "assets/video/cortes"
FONTS = PROY.parent / "_motion/shared/fonts"
sys.path.insert(0, str(HERE))

PIEZA = sys.argv[1] if len(sys.argv) > 1 else "largo"
V = PIEZA == "short"
W, H = (1080, 1920) if V else (1920, 1080)
HF = HERE / f"hf-{PIEZA}"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", s)


def esc(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------ assets
class Assets:
    def __init__(self):
        self.used = {}

    def img(self, name):
        key = f"img/{name}.jpg"
        self.used[key] = ("img", name)
        return "assets/" + key

    def vid(self, name):
        key = f"video/{name}.mp4"
        self.used[key] = ("vid", name)
        return "assets/" + key

    def prepare(self):
        for key, (kind, name) in self.used.items():
            out = HF / "assets" / key
            out.parent.mkdir(parents=True, exist_ok=True)
            if kind == "img":
                src = next(A_IMG.glob(f"{name}.*"), None)
                if src is None:
                    sys.exit(f"falta la imagen {name}")
            else:
                src = A_CUT / f"{name}.mp4"
            if out.exists() and out.stat().st_mtime > src.stat().st_mtime:
                continue
            if kind == "img":
                # color siempre; un toque cálido y +5 % de contraste (ver _estilo.md)
                vf = "scale='min(2400,iw)':-2,eq=contrast=1.05:saturation=1.03,colorbalance=rm=.02:bm=-.02"
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-vf", vf, "-q:v", "3", str(out)], check=True)
            else:
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-an", "-c:v", "copy", str(out)], check=True)
        fd = HF / "assets/fonts"
        fd.mkdir(parents=True, exist_ok=True)
        for f in ("Jost.ttf", "CormorantGaramond.ttf", "CormorantGaramond-Italic.ttf", "Fraunces.ttf"):
            shutil.copy(FONTS / f, fd / f)
        au = HF / "assets/audio"
        au.mkdir(parents=True, exist_ok=True)
        shutil.copy(HERE / "audio" / PIEZA / "master.wav", au / "master.wav")


AS = Assets()


# ------------------------------------------------------------------ sección / anclas
class Seccion:
    def __init__(self, sec, beats):
        self.id, self.t0, self.t1 = sec["id"], sec["start"], sec["end"]
        self.beats = [b for b in beats if b["sec"] == self.id]
        self.words = [(norm(w), s, e) for b in self.beats if b["type"] == "vo" for w, s, e in b["words"]]
        self.shots = []

    def w(self, frase, n=1, after=None, end=False):
        """Tiempo absoluto de la n-ésima aparición de la frase (desde 'after')."""
        from vo import tts_text
        ws = self.words
        after = self.t0 if after is None else after
        for variante in (frase, tts_text(frase)):
            q = [x for x in norm(variante).split() if x]
            k = 0
            for i in range(len(ws) - len(q) + 1):
                if ws[i][1] + 1e-3 < after:
                    continue
                if all(ws[i + j][0] == q[j] for j in range(len(q))):
                    k += 1
                    if k == n:
                        return ws[i + len(q) - 1][2] if end else ws[i][1]
        raise KeyError(f"[{self.id}] no encuentro «{frase}»")

    def clip_beat(self, name):
        for b in self.beats:
            if b["type"] == "clip" and b["clip"] == name:
                return b
        raise KeyError(f"[{self.id}] no hay clip {name}")

    def add(self, tipo, t, entrada="fundido", **p):
        self.shots.append(dict(tipo=tipo, t=max(self.t0, t - 0.12), entrada=entrada, p=p))
        return self


# ------------------------------------------------------------------ CSS común
CSS = """
@font-face{font-family:Jost;src:url(assets/fonts/Jost.ttf);font-weight:100 900}
@font-face{font-family:Corm;src:url(assets/fonts/CormorantGaramond.ttf);font-weight:300 700}
@font-face{font-family:Corm;src:url(assets/fonts/CormorantGaramond-Italic.ttf);font-weight:300 700;font-style:italic}
@font-face{font-family:Fraun;src:url(assets/fonts/Fraunces.ttf);font-weight:100 900}
#root{position:absolute;inset:0;overflow:hidden;background:#f2ebe0;color:#151214;font-family:Jost,sans-serif;
  --papel:#f2ebe0;--papel2:#e6dccb;--tinta:#151214;--rojo:#c8102e;--champan:#b89a6a;--gris:#7a7470;--flash:#fffaf2}
.shot{position:absolute;inset:0;overflow:hidden;opacity:0}
.fill{position:absolute;inset:0}
.paper{background:radial-gradient(ellipse at 30% 20%,#f7f1e7 0%,#f2ebe0 45%,#e9e0d0 100%)}
.light-sweep{position:absolute;top:-20%;bottom:-20%;width:46%;left:-50%;transform:skewX(-14deg);
  background:linear-gradient(90deg,rgba(255,250,242,0),rgba(255,250,242,.55),rgba(255,250,242,0))}
.mast{font-family:Jost,sans-serif;font-weight:500;font-size:28px;letter-spacing:.34em;text-transform:uppercase;color:var(--tinta)}
.kick{font-family:Jost,sans-serif;font-weight:600;font-size:28px;letter-spacing:.26em;text-transform:uppercase;color:var(--rojo)}
.tag{font-family:Jost,sans-serif;font-weight:500;font-size:28px;letter-spacing:.2em;text-transform:uppercase;color:var(--gris)}
.serif{font-family:Fraun,serif;font-variation-settings:"opsz" 144,"SOFT" 0,"WONK" 0;font-weight:800;letter-spacing:-.01em;line-height:.95;padding-top:.16em;margin-top:-.1em}
.num{font-family:Fraun,serif;font-variation-settings:"opsz" 144,"SOFT" 0,"WONK" 0;font-weight:900;color:var(--rojo);line-height:.8}
.ital{font-family:Corm,serif;font-style:italic;font-weight:500}
.light{font-weight:300;letter-spacing:.14em;text-transform:uppercase}
.rule{height:3px;background:var(--rojo)}
.rule-t{height:2px;background:var(--tinta)}
.w{display:inline-block}
.media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.kb{position:absolute;inset:-2%}
.print{position:absolute;background:#fffdf8;padding:18px;box-shadow:0 2px 4px rgba(40,28,18,.18),0 26px 60px rgba(40,28,18,.28)}
.print .win{position:relative;width:100%;height:100%;overflow:hidden;background:#222}
.card{background:rgba(242,235,224,.96);box-shadow:0 18px 50px rgba(20,12,8,.25)}
.flash{position:absolute;inset:0;background:var(--flash);opacity:0;z-index:50;pointer-events:none}
.shade-b{position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,18,20,0) 55%,rgba(21,18,20,.18) 100%)}
.cliptag{position:absolute;left:96px;bottom:84px;z-index:6;padding:14px 22px}
"""

# ------------------------------------------------------------------ helpers JS
JS_HELPERS_T = """
const tl = gsap.timeline({ paused: true });
const E = { inn: "expo.out", cam: "power2.inOut", out: "power3.in" };
function words(sel, at, gap) { tl.fromTo(sel, {opacity:0, filter:"blur(8px)"}, {opacity:1, filter:"blur(0px)", duration:0.22, stagger:gap||0.08, ease:"power4.out"}, at); }
function blurIn(sel, at, d) { tl.fromTo(sel, {opacity:0, filter:"blur(10px)"}, {opacity:1, filter:"blur(0px)", duration:d||0.35, ease:"power4.out"}, at); }
function maskUp(sel, at) { tl.fromTo(sel, {clipPath:"inset(100% 0 0 0)", y:40}, {clipPath:"inset(0% 0 0 0)", y:0, duration:0.75, ease:"expo.out"}, at); }
function track(sel, at) { tl.fromTo(sel, {opacity:0, x:-26, filter:"blur(6px)"}, {opacity:1, x:0, filter:"blur(0px)", duration:0.7, ease:"expo.out"}, at); }
function rise(sel, at, d) { tl.fromTo(sel, {opacity:0, y:22}, {opacity:1, y:0, duration:d||0.55, ease:"expo.out"}, at); }
function count(sel, to, at, d) { tl.fromTo(sel, {textContent:0}, {textContent:to, duration:d||0.9, snap:{textContent:1}, ease:"power2.out"}, at); }
function rule(sel, at, origin) { tl.fromTo(sel, {scaleX:0, transformOrigin:origin||"left center"}, {scaleX:1, duration:0.8, ease:"expo.out"}, at); }
function kb(sel, at, d, dir) {
  const m = {in:[1.0,1.07,0,0], out:[1.07,1.0,0,0], l:[1.06,1.06,30,-30], r:[1.06,1.06,-30,30], up:[1.05,1.09,0,0]}[dir||"in"];
  tl.fromTo(sel, {scale:m[0], x:m[2]}, {scale:m[1], x:m[3], duration:d, ease:"power1.inOut"}, at);
}
function sweep(sel, at, d) { tl.fromTo(sel, {x:0}, {x:__SW__, duration:d, ease:"power1.inOut"}, at); }
function flash(sel, at) { tl.fromTo(sel, {opacity:0}, {opacity:0.92, duration:0.06, ease:"none"}, at); tl.to(sel, {opacity:0, duration:0.4, ease:"power2.out"}, at + 0.06); }
function printIn(sel, at, rot) { tl.fromTo(sel, {opacity:0, y:90, rotation:(rot||0)*3, scale:.96}, {opacity:1, y:0, rotation:rot||0, scale:1, duration:0.85, ease:"expo.out"}, at); }
function circle(sel, at) { tl.fromTo(sel, {strokeDashoffset:1}, {strokeDashoffset:0, duration:0.7, ease:"power2.inOut"}, at); }
"""


JS_HELPERS = JS_HELPERS_T.replace("__SW__", str(int(W * 1.75)))


def wspan(text, cls="w"):
    return " ".join(f'<span class="{cls}">{esc(x)}</span>' for x in text.split())


def paper_bg(pid, L, sh):
    """Papel con una luz que lo cruza despacio: el fondo nunca está quieto."""
    d = sh["end"] - sh["t"]
    return (f'<div class="fill paper"></div><div id="{pid}-sw" class="light-sweep"></div>',
            f'sweep("#{pid}-sw",{L(sh["t"]):.2f},{max(d, 2.5):.2f});')


def media_html(pid, p, d, L, sh, pos="50% 30%"):
    if p.get("video"):
        return (f'<video id="{pid}-v" class="clip media" data-start="{L(sh["t"]):.3f}" data-duration="{d + 0.6:.3f}" '
                f'src="{AS.vid(p["video"])}" muted playsinline></video>')
    return f'<img class="media" src="{AS.img(p["img"])}" style="object-position:{p.get("pos", pos)}">'


# ------------------------------------------------------------------ renderers de planos
def r_clip(pid, sh, L):
    """Escena con sonido: entra como foto impresa que crece hasta llenar la pantalla."""
    p = sh["p"]
    src = AS.vid(p["clip"])
    d = sh["clip_end"] - sh["clip_start"]
    t = L(sh["clip_start"])
    bg, js = paper_bg(pid, L, sh)
    h = bg + (f'<div id="{pid}-pr" style="position:absolute;inset:0;box-shadow:0 30px 80px rgba(40,28,18,.35)">'
              f'<div id="{pid}-kb" style="position:absolute;inset:0;overflow:hidden"><video id="{pid}-v" class="clip media" '
              f'data-start="{t:.3f}" data-duration="{d:.3f}" src="{src}" muted playsinline></video></div>'
              f'<div id="{pid}-mb" style="position:absolute;inset:0;border:30px solid #fffdf8"></div></div>')
    js += (f'tl.fromTo("#{pid}-pr",{{scale:.58,rotation:-2.5}},{{scale:1,rotation:0,duration:0.75,ease:"expo.inOut"}},{t - 0.25:.2f});'
           f'tl.to("#{pid}-mb",{{opacity:0,duration:0.35,ease:"power1.out"}},{t + 0.3:.2f});'
           f'tl.fromTo("#{pid}-kb",{{scale:1.0}},{{scale:1.04,duration:{d:.2f},ease:"none"}},{t:.2f});')
    if p.get("tag"):
        h += f'<div id="{pid}-tag" class="cliptag card"><span class="kick">{esc(p["tag"])}</span></div>'
        js += f'rise("#{pid}-tag",{t + 0.5:.2f});tl.to("#{pid}-tag",{{opacity:0,duration:0.3}},{t + min(d - 0.4, 3.4):.2f});'
    return h, js


def r_portada(pid, sh, L):
    """Portada de la actriz: foto grande a color, número rojo gigante, nombre y cover lines. Flash al revelar."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    tnum = L(p.get("tnum", sh["t"] + 0.1))
    bg, js = paper_bg(pid, L, sh)
    if not V:
        fx, fw = 820, W - 820
        h = bg + (f'<div id="{pid}-foto" style="position:absolute;left:{fx}px;top:0;width:{fw}px;height:{H}px;overflow:hidden">'
                  f'<div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div>')
        js += (f'tl.fromTo("#{pid}-foto",{{clipPath:"inset(0 0 0 100%)"}},{{clipPath:"inset(0 0 0 0%)",duration:0.9,ease:"expo.inOut"}},{t:.2f});'
               f'kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");')
        h += (f'<div style="position:absolute;left:96px;top:70px;width:{fx - 150}px">'
              f'<div id="{pid}-m" class="mast">TOP 5 · MARVEL</div><div id="{pid}-mr" class="rule-t" style="margin-top:16px"></div></div>')
        js += f'track("#{pid}-m",{t + 0.15:.2f});rule("#{pid}-mr",{t + 0.2:.2f});'
        h += (f'<div id="{pid}-nw" style="position:absolute;left:70px;top:150px;display:flex;align-items:flex-start">'
              f'<span class="ital" style="font-size:96px;color:var(--rojo);margin:52px 10px 0 20px">Nº</span>'
              f'<span id="{pid}-n" class="num" style="font-size:520px">{esc(p["n"])}</span></div>')
        js += f'tl.fromTo("#{pid}-nw",{{opacity:0,scale:1.08,transformOrigin:"20% 30%"}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out"}},{tnum + 0.05:.2f});'
        ty = 640
        h += f'<div style="position:absolute;left:96px;top:{ty}px;width:{fx - 140}px">'
        h += f'<div id="{pid}-n1" class="light" style="font-size:52px">{esc(p["nombre"])}</div>'
        h += f'<div id="{pid}-n2" class="serif" style="font-size:{p.get("fsn", 128)}px;margin-top:6px">{esc(p["apellido"])}</div>'
        h += f'<div id="{pid}-rol" class="ital" style="font-size:52px;margin-top:22px;color:var(--tinta)">{esc(p["rol"])}</div></div>'
    else:
        h = bg + (f'<div id="{pid}-foto" style="position:absolute;left:0;top:0;width:{W}px;height:1180px;overflow:hidden">'
                  f'<div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div><div class="shade-b"></div></div>')
        js += (f'tl.fromTo("#{pid}-foto",{{clipPath:"inset(0 0 100% 0)"}},{{clipPath:"inset(0 0 0% 0)",duration:0.8,ease:"expo.inOut"}},{t:.2f});'
               f'kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");')
        h += (f'<div id="{pid}-mw" class="card" style="position:absolute;left:0;right:0;top:150px;padding:18px 70px">'
              f'<div id="{pid}-m" class="mast" style="text-align:center">TOP 5 · MARVEL</div></div>')
        js += f'rise("#{pid}-mw",{t + 0.15:.2f});track("#{pid}-m",{t + 0.2:.2f});'
        h += (f'<div id="{pid}-nw" style="position:absolute;right:150px;top:860px;display:flex;align-items:flex-start;text-shadow:0 10px 40px rgba(0,0,0,.25)">'
              f'<span class="ital" style="font-size:90px;color:var(--rojo);margin:40px 8px 0 0">Nº</span>'
              f'<span id="{pid}-n" class="num" style="font-size:440px">{esc(p["n"])}</span></div>')
        js += f'tl.fromTo("#{pid}-nw",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:0.8,ease:"expo.out"}},{tnum + 0.05:.2f});'
        h += f'<div style="position:absolute;left:80px;top:1260px;right:180px">'
        h += f'<div id="{pid}-n1" class="light" style="font-size:54px">{esc(p["nombre"])}</div>'
        h += f'<div id="{pid}-n2" class="serif" style="font-size:{p.get("fsn", 128)}px;margin-top:6px">{esc(p["apellido"])}</div>'
        h += f'<div id="{pid}-rol" class="ital" style="font-size:58px;margin-top:20px">{esc(p["rol"])}</div></div>'
    tn = L(p.get("tn", sh["t"] + 0.5))
    js += f'blurIn("#{pid}-n1",{tn:.2f},0.3);maskUp("#{pid}-n2",{tn + 0.15:.2f});blurIn("#{pid}-rol",{L(p.get("trol", sh["t"] + 1.2)):.2f});'
    # cover lines
    if p.get("lines"):
        if not V:
            h += f'<div style="position:absolute;left:96px;bottom:80px;width:{820 - 140}px">'
        else:
            h += f'<div style="position:absolute;left:80px;top:1630px;right:180px">'
        for j, (txt, tt) in enumerate(p["lines"]):
            h += (f'<div id="{pid}-cl{j}" style="display:flex;gap:18px;align-items:baseline;margin-top:{0 if j == 0 else 12}px">'
                  f'<span class="kick" style="font-size:28px">—</span><span style="font-size:36px;font-weight:500">{esc(txt)}</span></div>')
            js += f'rise("#{pid}-cl{j}",{L(tt):.2f});'
        h += "</div>"
    h += f'<div id="{pid}-fl" class="flash"></div>'
    js += f'flash("#{pid}-fl",{tnum:.2f});'
    return h, js


def r_foto(pid, sh, L):
    """Foto o b-roll a color a pantalla completa con Ken Burns; texto en tarjeta de papel abajo a la izquierda."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = f'<div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div>'
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");'
    if p.get("kick") or p.get("l1") or p.get("sub"):
        x0, yb = (96, 96) if not V else (70, 520)
        mw = p.get("mw", 1100 if not V else W - 220)
        h += f'<div id="{pid}-c" class="card" style="position:absolute;left:{x0}px;bottom:{yb}px;max-width:{mw}px;padding:30px 40px 34px">'
        if p.get("kick"):
            h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
            js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.3)):.2f});'
        if p.get("l1"):
            h += f'<div id="{pid}-l1" class="serif" style="font-size:{p.get("fs1", 96 if not V else 100)}px;margin-top:14px">{esc(p["l1"])}</div>'
            js += f'maskUp("#{pid}-l1",{L(p.get("t1", sh["t"] + 0.45)):.2f});'
        if p.get("sub"):
            h += f'<div id="{pid}-s" class="ital" style="font-size:{p.get("fss", 52 if not V else 58)}px;margin-top:12px">{esc(p["sub"])}</div>'
            js += f'blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 0.9)):.2f});'
        h += "</div>"
        js += f'tl.fromTo("#{pid}-c",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.6,ease:E.inn}},{L(min(p.get("tk", 1e9), p.get("t1", 1e9), p.get("ts", 1e9), sh["t"] + 0.3 if p.get("kick") and "tk" not in p else 1e9)) - 0.05:.2f});'
    return h, js


def r_impresa(pid, sh, L):
    """Foto o b-roll impreso (marco blanco, sombra, leve giro) sobre papel; texto al otro lado.
    Texto: kick, titulo (serif), sub (itálica), dato=(pre, num, suf, etiqueta, t) que cuenta."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = paper_bg(pid, L, sh)
    lado = p.get("lado", "der")
    vertical_foto = p.get("vertical", False)
    if not V:
        pw, ph = (560, 760) if vertical_foto else (900, 620)
        px = W - pw - 150 if lado == "der" else 150
        py = (H - ph) // 2 - 10
        tx = 120 if lado == "der" else px + pw + 110
        tw = (px - 110 - tx) if lado == "der" else (W - tx - 110)
        ty = None
    else:
        pw, ph = (760, 1000) if vertical_foto else (900, 640)
        px, py = (W - pw) // 2, 300
        tx, tw, ty = 90, W - 270, py + ph + 110
    rot = p.get("rot", 2.0 if lado == "der" else -2.0)
    h = bg + (f'<div id="{pid}-pr" class="print" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate({rot}deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
    js += f'printIn("#{pid}-pr",{t + 0.05:.2f},{rot});kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");'
    js += f'tl.fromTo("#{pid}-pr",{{x:0}},{{x:{-20 if lado == "der" else 20},duration:{d:.2f},ease:"power1.inOut"}},{t:.2f});'
    if p.get("pie"):
        h += f'<div id="{pid}-pie" class="tag" style="position:absolute;left:{px}px;top:{py + ph + 34}px;width:{pw}px;text-align:center">{esc(p["pie"])}</div>'
        js += f'blurIn("#{pid}-pie",{t + 0.7:.2f});'
    style = f"left:{tx}px;width:{tw}px;" + (f"top:{ty}px;" if ty else "top:50%;transform:translateY(-50%);")
    h += f'<div style="position:absolute;{style}">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div><div id="{pid}-r" class="rule" style="width:120px;margin:22px 0 28px"></div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.3)):.2f});rule("#{pid}-r",{L(p.get("tk", sh["t"] + 0.3)) + 0.2:.2f});'
    if p.get("dato"):
        pre, num, suf, etq, tdat = p["dato"]
        fs = p.get("fsd", 200 if not V else 190)
        h += (f'<div id="{pid}-dn" class="num" style="font-size:{fs}px;line-height:.9">{esc(pre)}<span id="{pid}-dc">{esc(num)}</span>'
              f'<span style="font-size:{int(fs * .42)}px">{esc(suf)}</span></div>'
              f'<div id="{pid}-dl" class="light" style="font-size:{p.get("fsl", 40)}px;margin-top:18px;line-height:1.25">{esc(etq)}</div>')
        js += (f'tl.fromTo("#{pid}-dn",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.6,ease:E.inn}},{L(tdat):.2f});'
               f'blurIn("#{pid}-dl",{L(tdat) + 0.4:.2f});')
        if str(num).isdigit() and p.get("cuenta", True):
            js += f'count("#{pid}-dc",{num},{L(tdat):.2f},0.9);'
    if p.get("titulo"):
        h += f'<div id="{pid}-t" class="serif" style="font-size:{p.get("fst", 104 if not V else 110)}px;margin-top:{20 if p.get("dato") else 0}px">{esc(p["titulo"])}</div>'
        js += f'maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.5)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="ital" style="font-size:{p.get("fss", 56 if not V else 62)}px;margin-top:22px;line-height:1.15">{wspan(p["sub"])}</div>'
        js += f'words("#{pid}-s .w",{L(p.get("ts", sh["t"] + 1.0)):.2f},0.06);'
    h += "</div>"
    return h, js


def r_contactos(pid, sh, L):
    """Hoja de contactos: tira de fotos con número de cuadro; un círculo de lápiz rojo elige una."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = paper_bg(pid, L, sh)
    imgs = p["imgs"]
    n = len(imgs)
    if not V:
        cw = p.get("cw", 330)
        ch = int(cw * 1.3)
        gap = 22
        x0 = (W - (n * cw + (n - 1) * gap + 60)) / 2
        y0 = 240
        stripw, striph = n * cw + (n - 1) * gap + 60, ch + 90
    else:
        cw = 440
        ch = int(cw * 1.25)
        gap = 22
        x0, y0 = (W - (2 * cw + gap + 60)) / 2, 330
        stripw, striph = 2 * cw + gap + 60, ((n + 1) // 2) * (ch + 70) + 30
    h = bg + f'<div id="{pid}-strip" style="position:absolute;left:{x0:.0f}px;top:{y0}px;width:{stripw:.0f}px;height:{striph}px;background:#1b1714;box-shadow:0 26px 60px rgba(40,28,18,.3)">'
    for j, img in enumerate(imgs):
        name, pos = img if isinstance(img, tuple) else (img, "50% 25%")
        if not V:
            cx, cy = 30 + j * (cw + gap), 30
        else:
            cx, cy = 30 + (j % 2) * (cw + gap), 30 + (j // 2) * (ch + 70)
        h += (f'<div id="{pid}-c{j}" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;overflow:hidden">'
              f'<img class="media" src="{AS.img(name)}" style="object-position:{pos}"></div>'
              f'<div style="position:absolute;left:{cx}px;top:{cy + ch + 8}px;font-family:Jost;font-size:28px;letter-spacing:.2em;color:#e0a04a">{j + 1:02d}A ▸</div>')
        tj = p["ts"][j] if p.get("ts") else sh["t"] + 0.2 + j * 0.18
        js += f'tl.fromTo("#{pid}-c{j}",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.out"}},{L(tj):.2f});'
    h += "</div>"
    js += f'tl.fromTo("#{pid}-strip",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.6,ease:E.inn}},{t:.2f});'
    js += f'tl.fromTo("#{pid}-strip",{{x:16}},{{x:-16,duration:{d:.2f},ease:"power1.inOut"}},{t:.2f});'
    if p.get("elegida") is not None:
        j = p["elegida"]
        if not V:
            cx, cy = x0 + 30 + j * (cw + gap), y0 + 30
        else:
            cx, cy = x0 + 30 + (j % 2) * (cw + gap), y0 + 30 + (j // 2) * (ch + 70)
        ex, ey = cx - 40, cy - 40
        h += (f'<svg style="position:absolute;left:{ex:.0f}px;top:{ey}px;overflow:visible" width="{cw + 80}" height="{ch + 80}">'
              f'<ellipse id="{pid}-e" cx="{(cw + 80) / 2}" cy="{(ch + 80) / 2}" rx="{(cw + 60) / 2}" ry="{(ch + 60) / 2}" fill="none" '
              f'stroke="#c8102e" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1.04 1" '
              f'transform="rotate(-6 {(cw + 80) / 2} {(ch + 80) / 2})" style="filter:drop-shadow(0 2px 1px rgba(0,0,0,.2))"/></svg>')
        js += f'circle("#{pid}-e",{L(p["tc"]):.2f});'
    ty = y0 + striph + 70
    h += f'<div style="position:absolute;left:{x0:.0f}px;top:{ty:.0f}px;width:{stripw:.0f}px">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.4)):.2f});'
    if p.get("titulo"):
        h += f'<div id="{pid}-t" class="serif" style="font-size:{p.get("fst", 92)}px;margin-top:14px">{esc(p["titulo"])}</div>'
        js += f'maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.6)):.2f});'
    h += "</div>"
    return h, js


def r_dato(pid, sh, L):
    """Cifra roja grande que cuenta + etiqueta, sobre papel. Opcional: foto impresa al lado."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = paper_bg(pid, L, sh)
    h = bg
    tieneimg = bool(p.get("img") or p.get("video"))
    if tieneimg:
        if not V:
            pw, ph, px, py = 620, 760, W - 620 - 140, (H - 760) // 2
        else:
            pw, ph, px, py = 700, 860, (W - 700) // 2, 220
        h += (f'<div id="{pid}-pr" class="print" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(2deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
        js += f'printIn("#{pid}-pr",{t + 0.05:.2f},2);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
    if not V:
        box = (f"left:120px;width:{(W - 620 - 140 - 220) if tieneimg else W - 240}px;top:50%;transform:translateY(-50%);"
               + ("" if tieneimg else "text-align:center;"))
    else:
        box = f"left:90px;width:{W - 220}px;top:{1180 if tieneimg else 560}px;"
    pre, num, suf = p.get("pre", ""), p["num"], p.get("suf", "")
    fs = p.get("fs", 280 if not V else 240)
    tn = L(p.get("tn", sh["t"] + 0.3))
    h += (f'<div style="position:absolute;{box}"><div id="{pid}-k" class="kick">{esc(p.get("kick", ""))}</div>'
          f'<div id="{pid}-n" class="num" style="font-size:{fs}px;margin-top:24px">{esc(pre)}<span id="{pid}-c">{esc(num)}</span>'
          f'<span style="font-size:{int(fs * .4)}px">{esc(suf)}</span></div>'
          f'<div id="{pid}-l" class="light" style="font-size:{p.get("fsl", 44 if not V else 48)}px;margin-top:30px;line-height:1.3">{esc(p.get("label", ""))}</div></div>')
    js += (f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.2)):.2f});'
           f'tl.fromTo("#{pid}-n",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.6,ease:E.inn}},{tn:.2f});'
           f'blurIn("#{pid}-l",{L(p.get("tl", sh["t"] + 0.9)):.2f});')
    if p.get("cuenta", True) and str(num).isdigit():
        js += f'count("#{pid}-c",{num},{tn:.2f},{p.get("dc", 1.0)});'
    return h, js


def r_cita(pid, sh, L):
    """Cita en Cormorant itálica sobre papel, con comillas rojas; foto impresa opcional."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = paper_bg(pid, L, sh)
    h = bg
    if p.get("img") or p.get("video"):
        pw, ph = (520, 680) if not V else (640, 820)
        px, py = (W - pw - 140, (H - ph) // 2) if not V else ((W - pw) // 2, 200)
        h += (f'<div id="{pid}-pr" class="print" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(-2deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
        js += f'printIn("#{pid}-pr",{t + 0.05:.2f},-2);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
        box = "left:130px;width:1040px;top:50%;transform:translateY(-50%);" if not V else f"left:90px;width:{W - 220}px;top:1110px;"
    else:
        box = "left:220px;right:220px;top:50%;transform:translateY(-50%);text-align:center;" if not V else f"left:90px;width:{W - 220}px;top:600px;"
    fs = p.get("fs", 88 if not V else 84)
    h += (f'<div style="position:absolute;{box}"><div class="ital" style="color:var(--rojo);font-size:220px;line-height:.5;height:90px">“</div>'
          f'<div id="{pid}-q" class="ital" style="font-size:{fs}px;line-height:1.12">{wspan(p["texto"])}</div>'
          f'<div id="{pid}-r" class="rule" style="width:140px;margin:44px {"auto" if "center" in box else "0"} 24px"></div>'
          f'<div id="{pid}-a" class="kick">{esc(p["autor"])}</div></div>')
    js += (f'words("#{pid}-q .w",{L(p.get("tq", sh["t"] + 0.2)):.2f},{p.get("gap", 0.1)});'
           f'rule("#{pid}-r",{L(p.get("ta", sh["t"] + 1.0)):.2f});track("#{pid}-a",{L(p.get("ta", sh["t"] + 1.0)) + 0.15:.2f});')
    return h, js


def r_titulo(pid, sh, L):
    """Título de revista sobre papel: kick rojo, l1 ligera, l2 serif grande, regla y subtítulo."""
    p = sh["p"]
    bg, js = paper_bg(pid, L, sh)
    pad = "0 140px" if not V else "0 180px 0 90px"
    h = bg + f'<div class="fill" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{pad}">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.15)):.2f});'
    if p.get("l1"):
        h += f'<div id="{pid}-l1" class="light" style="font-size:{p.get("fs1", 70 if not V else 64)}px;margin-top:30px">{wspan(p["l1"])}</div>'
        js += f'words("#{pid}-l1 .w",{L(p.get("t1", sh["t"] + 0.3)):.2f},0.09);'
    if p.get("l2"):
        h += f'<div id="{pid}-l2" class="serif" style="font-size:{p.get("fs2", 200 if not V else 150)}px;margin-top:10px">{esc(p["l2"])}</div>'
        js += f'maskUp("#{pid}-l2",{L(p.get("t2", sh["t"] + 0.6)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-r" class="rule" style="width:160px;margin:40px 0 30px"></div>'
        h += f'<div id="{pid}-s" class="ital" style="font-size:{p.get("fss", 62)}px">{esc(p["sub"])}</div>'
        js += f'rule("#{pid}-r",{L(p.get("ts", sh["t"] + 1.0)) - 0.1:.2f},"center");blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 1.0)):.2f});'
    h += "</div>"
    return h, js


def r_reglas(pid, sh, L):
    """Lista numerada: número rojo grande + texto, cada regla cuando la voz la dice."""
    p = sh["p"]
    bg, js = paper_bg(pid, L, sh)
    x, y = (230, 190) if not V else (90, 420)
    h = bg + f'<div style="position:absolute;left:{x}px;top:{y}px;right:{x}px">'
    h += f'<div id="{pid}-k" class="kick">{esc(p.get("kick", "LAS REGLAS"))}</div><div id="{pid}-r" class="rule" style="width:120px;margin:20px 0 40px"></div>'
    js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});rule("#{pid}-r",{L(sh["t"] + 0.3):.2f});'
    for j, (titulo, sub, tt) in enumerate(p["items"]):
        h += (f'<div id="{pid}-i{j}" style="display:flex;gap:44px;align-items:center;margin-top:{0 if j == 0 else 44}px">'
              f'<div class="num" style="font-size:{170 if not V else 160}px;width:{120 if not V else 110}px">{j + 1}</div>'
              f'<div><div class="serif" style="font-size:{66 if not V else 64}px">{esc(titulo)}</div>'
              f'<div class="ital" style="font-size:{46 if not V else 46}px;margin-top:8px;color:#4a4246">{esc(sub)}</div></div></div>')
        js += f'tl.fromTo("#{pid}-i{j}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.6,ease:E.inn}},{L(tt):.2f});'
    h += "</div>"
    return h, js


def r_galeria(pid, sh, L):
    """Fotos impresas que caen sobre el papel una a una (con nombre), estilo mesa de edición."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = paper_bg(pid, L, sh)
    items = p["items"]
    n = len(items)
    h = bg
    if not V:
        pw = p.get("pw", 340 if n >= 5 else 380)
        ph = int(pw * 1.3)
        gap = (W - 200 - n * pw) / max(1, n - 1)
        y = (H - ph) // 2 - 40
    else:
        pw = 440
        ph = int(pw * 1.25)
    for j, it in enumerate(items):
        img, nombre, tt = it[0], it[1], it[2]
        pos = it[3] if len(it) > 3 else "50% 25%"
        rot = [-3, 2, -1.5, 2.5, -2][j % 5]
        if not V:
            x, yy = 100 + j * (pw + gap), y + (24 if j % 2 else 0)
        else:
            x, yy = 70 + (j % 2) * (pw + 60), 240 + (j // 2) * (ph + 140)
        hi = p.get("destaca") == j
        h += (f'<div id="{pid}-p{j}" class="print" style="left:{x:.0f}px;top:{yy}px;width:{pw}px;height:{ph}px;transform:rotate({rot}deg);padding:14px 14px 70px;'
              f'{"outline:6px solid var(--rojo);" if hi else ""}">'
              f'<div class="win" style="height:{ph - 84}px"><img class="media" src="{AS.img(img)}" style="object-position:{pos}"></div>'
              f'<div class="serif" style="font-size:{34 if not V else 36}px;text-align:center;margin-top:16px">{esc(nombre)}</div></div>')
        js += f'printIn("#{pid}-p{j}",{L(tt):.2f},{rot});'
    if p.get("kick"):
        ky = 70 if not V else 120
        h += f'<div id="{pid}-k" class="kick" style="position:absolute;left:0;right:0;top:{ky}px;text-align:center">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.1)):.2f});'
    if p.get("titulo"):
        ty = H - 170 if not V else H - 330
        h += f'<div id="{pid}-t" class="serif" style="position:absolute;left:0;right:0;top:{ty}px;text-align:center;font-size:{p.get("fst", 80)}px">{esc(p["titulo"])}</div>'
        js += f'maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.5)):.2f});'
    return h, js


def r_podio(pid, sh, L):
    """Las cinco portadas en fila (5→1); el número 1 más grande con regla roja."""
    p = sh["p"]
    bg, js = paper_bg(pid, L, sh)
    items = p["items"]  # [(img, n, nombre, t, pos)]
    h = bg
    if not V:
        pw = 300
        ph = int(pw * 1.36)
        gap = 46
        x0 = (W - (5 * pw + 4 * gap)) / 2
        base = 760
    for j, it in enumerate(items):
        img, n, nombre, tt = it[:4]
        pos = it[4] if len(it) > 4 else "50% 25%"
        big = n == 1
        if not V:
            w_, h_ = (pw * 1.18, ph * 1.18) if big else (pw, ph)
            x = x0 + j * (pw + gap) - (w_ - pw) / 2
            yy = base - h_
        else:
            w_, h_ = (560, 700) if big else (420, 520)
            col, row = (j % 2, j // 2) if not big else (0, 0)
            x = (W - w_) / 2 if big else 80 + col * (420 + 80)
            yy = 1160 if big else 240 + row * 590
            if big:
                yy = 1080
        h += (f'<div id="{pid}-p{j}" style="position:absolute;left:{x:.0f}px;top:{yy:.0f}px;width:{w_:.0f}px;height:{h_:.0f}px">'
              f'<div class="print" style="inset:0;padding:12px"><div class="win"><img class="media" src="{AS.img(img)}" style="object-position:{pos}"></div></div>'
              f'<div class="num" style="position:absolute;left:-18px;top:-40px;font-size:{150 if big else 110}px;text-shadow:0 6px 20px rgba(255,250,242,.8)">{n}</div>'
              f'<div class="light" style="position:absolute;left:0;right:0;top:{h_ + 26:.0f}px;text-align:center;font-size:{34 if big else 28}px;font-weight:{500 if big else 400}">{esc(nombre)}</div></div>')
        js += f'printIn("#{pid}-p{j}",{L(tt):.2f},0);'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick" style="position:absolute;left:0;right:0;top:{80 if not V else 120}px;text-align:center">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});'
    return h, js


def r_cta(pid, sh, L):
    """Tu top 5: cinco renglones numerados vacíos + llamada a comentar."""
    p = sh["p"]
    bg, js = paper_bg(pid, L, sh)
    x, y = (360, 150) if not V else (110, 380)
    h = bg + f'<div style="position:absolute;left:{x}px;right:{x}px;top:{y}px">'
    h += f'<div id="{pid}-k" class="kick">{esc(p.get("kick", "AHORA TE TOCA"))}</div>'
    h += f'<div id="{pid}-t" class="serif" style="font-size:{130 if not V else 120}px;margin-top:16px">{esc(p.get("titulo", "TU TOP 5"))}</div>'
    js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.3)):.2f});'
    for k in range(5):
        h += (f'<div id="{pid}-l{k}" style="display:flex;align-items:flex-end;gap:30px;margin-top:{34 if k else 50}px">'
              f'<span class="num" style="font-size:72px;width:60px">{k + 1}</span>'
              f'<span id="{pid}-u{k}" style="flex:1;height:3px;background:var(--tinta);margin-bottom:12px"></span></div>')
        js += (f'tl.fromTo("#{pid}-l{k}",{{opacity:0}},{{opacity:1,duration:0.3}},{L(p["tl"]) + k * 0.12:.2f});'
               f'rule("#{pid}-u{k}",{L(p["tl"]) + k * 0.12:.2f});')
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="ital" style="font-size:{60 if not V else 58}px;margin-top:56px">{esc(p["sub"])}</div>'
        js += f'blurIn("#{pid}-s",{L(p["ts"]):.2f});'
    h += "</div>"
    return h, js


RENDER = {k[2:]: v for k, v in globals().items() if k.startswith("r_")}

TRANS = {"corte": 0.0, "fundido": 0.45, "pagina": 0.7, "flash": 0.0, "crece": 0.6, "iris": 0.7, "latigo": 0.42}


def trans_js(pid, prev, kind, t):
    """Entrada del plano pid a tiempo local t (y salida del anterior)."""
    d = TRANS[kind]
    s = f'#{pid}'
    js = f'tl.set("{s}",{{opacity:1}},{t:.3f});'
    if kind == "fundido":
        js = f'tl.fromTo("{s}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power1.inOut"}},{t:.3f});'
    elif kind == "pagina":
        # pase de página: la nueva página entra en diagonal desde la derecha; la anterior se corre y oscurece apenas
        js += (f'tl.fromTo("{s}",{{clipPath:"polygon(118% 0%,118% 0%,118% 100%,100% 100%)"}},'
               f'{{clipPath:"polygon(0% 0%,118% 0%,118% 100%,-18% 100%)",duration:{d},ease:"power3.inOut"}},{t:.3f});')
        if prev:
            js += f'tl.fromTo("#{prev}",{{x:0,filter:"brightness(1)"}},{{x:{-W * 0.08:.0f},filter:"brightness(0.85)",duration:{d},ease:"power3.inOut",immediateRender:false}},{t:.3f});'
    elif kind == "iris":
        js += f'tl.fromTo("{s}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:{d},ease:"power3.inOut"}},{t:.3f});'
    elif kind == "latigo":
        js += f'tl.fromTo("{s}",{{x:{W * 0.6:.0f},filter:"blur(18px)"}},{{x:0,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{t:.3f});'
        if prev:
            js += f'tl.to("#{prev}",{{x:{-W * 0.6:.0f},filter:"blur(18px)",duration:{d * 0.7:.2f},ease:"power3.in"}},{t - 0.05:.3f});'
    elif kind == "crece":
        js += f'tl.fromTo("{s}",{{opacity:0,scale:1.16,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{t:.3f});'
        if prev:
            js += f'tl.to("#{prev}",{{scale:0.94,duration:{d},ease:"power3.in"}},{t:.3f});'
    return js


SFX = []  # (tiempo absoluto, efecto, ganancia dB) para mezcla.py
SFX_ENTRADA = {"pagina": ("papel", -14), "latigo": ("whoosh", -14), "crece": ("whoosh", -17), "iris": ("whoosh", -16)}


def sfx_de(sh, primero):
    p, ev = sh["p"], []
    if not primero and sh["entrada"] in SFX_ENTRADA and sh["tipo"] != "clip":
        ev.append((sh["t"], *SFX_ENTRADA[sh["entrada"]]))
    if sh["tipo"] == "portada":
        ev.append((p.get("tnum", sh["t"] + 0.1), "obturador", -9))
    if sh["tipo"] == "dato" and p.get("tn"):
        ev.append((p["tn"], "golpe", -12))
    if sh["tipo"] == "impresa" and p.get("dato"):
        ev.append((p["dato"][4], "golpe", -14))
    if sh["tipo"] == "contactos" and p.get("tc"):
        ev.append((p["tc"] + 0.55, "lapiz", -14))
    if sh["tipo"] == "clip":
        ev.append((sh["clip_start"] - 0.25, "whoosh", -18))
    return ev


# ------------------------------------------------------------------ composición por sección
def build_section(S):
    shots = sorted(S.shots, key=lambda s: s["t"])
    for i, sh in enumerate(shots):
        nxt = shots[i + 1] if i + 1 < len(shots) else None
        sh["end"] = (nxt["t"] + TRANS[nxt["entrada"]] + 0.05) if nxt else S.t1 + 0.4
        if sh["tipo"] == "clip":
            b = S.clip_beat(sh["p"]["clip"])
            sh["clip_start"], sh["clip_end"] = b["start"], b["end"]
    dur = S.t1 - S.t0 + 0.5
    L = lambda t: max(0.0, t - S.t0)
    body, js = [], [JS_HELPERS]
    for i, sh in enumerate(shots):
        SFX.extend(sfx_de(sh, i == 0))
        pid = f"{S.id}-s{i:02d}"
        inner, j = RENDER[sh["tipo"]](pid, sh, L)
        if sh["entrada"] == "flash" and sh["tipo"] != "portada":
            inner += f'<div id="{pid}-tfl" class="flash"></div>'
            j += f'flash("#{pid}-tfl",{L(sh["t"]):.2f});'
            SFX.append((sh["t"], "obturador", -11))
        vis = ";opacity:1" if i == 0 and sh["entrada"] == "corte" and L(sh["t"]) < 0.05 else ""
        body.append(f'<div id="{pid}" class="shot" style="z-index:{i + 1}{vis}">{inner}</div>')
        prev = f"{S.id}-s{i - 1:02d}" if i else None
        js.append(trans_js(pid, prev, sh["entrada"], L(sh["t"])))
        js.append(j)
        js.append(f'tl.set("#{pid}",{{opacity:0}},{L(sh["end"]):.3f});')
    js.append(f'tl.set({{}},{{}},{dur:.3f});window.__timelines["{S.id}"] = tl;')
    doc = (f'<template>\n<style>{CSS}</style>\n'
           f'<div id="root" data-composition-id="{S.id}" data-width="{W}" data-height="{H}" data-layout-allow-overflow data-layout-allow-overlap>\n'
           + "\n".join(body) +
           f'\n</div>\n<script>\n' + "\n".join(js) + '\n</script>\n</template>\n')
    (HF / "compositions").mkdir(parents=True, exist_ok=True)
    (HF / "compositions" / f"{S.id}.html").write_text(doc)
    return dur


def main():
    tl = json.loads((HERE / f"timeline-{PIEZA}.json").read_text())
    esc_mod = importlib.import_module(f"escenas_{PIEZA}")
    if not (HF / "hyperframes.json").exists():
        subprocess.run(["npx", "hyperframes", "init", HF.name, "--example", "blank", "--non-interactive", "--skip-skills",
                        "--skill", "hyperframes", "--resolution", "portrait" if V else "landscape"], cwd=HERE, check=True)
    hosts = []
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  str(HERE / "audio" / PIEZA / "master.wav")], capture_output=True, text=True).stdout)
    for sec in tl["sections"]:
        S = Seccion(sec, tl["beats"])
        getattr(esc_mod, S.id.replace("-", "_"))(S)
        d = min(build_section(S), total - S.t0)
        hosts.append(f'<div id="{S.id}" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" '
                     f'data-start="{S.t0:.3f}" data-duration="{d:.3f}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="{W}" data-height="{H}" style="z-index:{len(hosts) + 1}"></div>')
        print(f"  {S.id:10s} {S.t0:7.1f}–{S.t1:7.1f}  {len(S.shots):2d} planos")
    index = f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#f2ebe0}}
#main{{position:relative;width:100%;height:100%;background:#f2ebe0}}
#grano{{position:absolute;inset:0;z-index:900;pointer-events:none;opacity:.06;mix-blend-mode:multiply;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence baseFrequency='.8' numOctaves='2' seed='11'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}</style>
</head><body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
<audio id="voz" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0" data-volume="1" src="assets/audio/master.wav"></audio>
{chr(10).join(hosts)}
<div id="grano" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="9" data-layout-ignore></div>
</div>
<script>window.__timelines = window.__timelines || {{}}; const tl = gsap.timeline({{paused:true}}); tl.set({{}},{{}},{total:.3f}); window.__timelines["main"] = tl;</script>
</body></html>
"""
    (HF / "index.html").write_text(index)
    (HERE / f"sfx-{PIEZA}.json").write_text(json.dumps(sorted(SFX), indent=0))
    AS.prepare()
    print(f"✓ {HF.name}: {len(hosts)} secciones · {total:.1f} s · {len(AS.used)} assets")


if __name__ == "__main__":
    main()
