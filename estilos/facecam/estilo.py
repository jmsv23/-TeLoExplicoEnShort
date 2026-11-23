"""Estilo «Facecam Leonida» — plugin del motor (contrato: estilos/CONTRATO.md).

Extraído de mejores-momentos-de-gta6/_prod/build.py (content-creator/explicando). El motor inyecta antes de usarlo:
W, H, V (vertical), AS (assets), esc, wspan, norm, HF, A_IMG, A_CUT, PIEZA, SFX, ESTILO_DIR, VIDEO.
"""
import html, json, re, subprocess, sys  # noqa: F401
from pathlib import Path  # noqa: F401

CSS = """
@font-face{font-family:Price;src:url(assets/fonts/Pricedown.otf)}
@font-face{font-family:Jost;src:url(assets/fonts/Jost.ttf);font-weight:100 900}
@font-face{font-family:Anton;src:url(assets/fonts/Anton.ttf)}
@font-face{font-family:Pix;src:url(assets/fonts/PressStart2P-Regular.ttf)}
@font-face{font-family:Script;src:url(assets/fonts/Pacifico-Regular.ttf)}
#root{position:absolute;inset:0;overflow:hidden;background:#1a0b2e;color:#fff;font-family:Jost,sans-serif;
  --noche:#1a0b2e;--morado:#4a1a6b;--magenta:#d4246e;--rosa:#ff4fa3;--naranja:#ff8a3d;--sol:#ffc65c;--cian:#3de0ff;--tinta:#0b0612}
.shot{position:absolute;inset:0;overflow:hidden;opacity:0}
.fill{position:absolute;inset:0}
.sky{background:linear-gradient(180deg,#140826 0%,#2e0f4a 34%,#6b1b62 62%,#c23a5e 82%,#ff8a4c 100%)}
.sun{position:absolute;left:50%;width:__SUN__px;height:__SUN__px;margin-left:-__SUNH__px;bottom:-__SUNB__px;border-radius:50%;
  background:linear-gradient(180deg,#ffd36b 0%,#ff8a3d 45%,#ff3f7f 100%);opacity:.55;filter:blur(2px);
  -webkit-mask:repeating-linear-gradient(180deg,#000 0 26px,transparent 26px 34px)}
.grid{position:absolute;left:-20%;right:-20%;bottom:0;height:34%;opacity:.22;transform:perspective(500px) rotateX(62deg);transform-origin:bottom;
  background-image:linear-gradient(#ff4fa3 2px,transparent 2px),linear-gradient(90deg,#ff4fa3 2px,transparent 2px);background-size:90px 90px}
.light-sweep{position:absolute;top:-20%;bottom:-20%;width:40%;left:-50%;transform:skewX(-14deg);
  background:linear-gradient(90deg,rgba(255,180,220,0),rgba(255,180,220,.14),rgba(255,180,220,0))}
.price{font-family:Price,Anton,sans-serif;font-weight:400;line-height:.86;letter-spacing:.01em;color:#fff;
  -webkit-text-stroke:__STK__px #0b0612;paint-order:stroke fill;text-shadow:0 8px 0 #0b0612,0 14px 40px rgba(0,0,0,.45)}
.grad{background:linear-gradient(180deg,#ffe08a 0%,#ff8a3d 48%,#ff3f8f 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
  -webkit-text-stroke:0;text-shadow:none;filter:drop-shadow(0 6px 0 #0b0612) drop-shadow(0 0 2px #0b0612)}
.kick{font-family:Anton,sans-serif;font-size:__KS__px;letter-spacing:.14em;text-transform:uppercase;color:var(--rosa)}
.tag{font-family:Jost,sans-serif;font-weight:600;font-size:28px;letter-spacing:.2em;text-transform:uppercase;color:#ffd9ec}
.sub{font-family:Jost,sans-serif;font-weight:600;line-height:1.18;color:#fff}
.px{font-family:Pix,monospace;line-height:1.3}
.script{font-family:Script,cursive;color:var(--rosa);text-shadow:0 0 18px rgba(255,79,163,.7)}
.w{display:inline-block}
.media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.kb{position:absolute;inset:-3%}
.panel{position:absolute;background:#0b0612;padding:12px;box-shadow:0 0 0 5px #fff,0 0 0 13px #0b0612,0 30px 70px rgba(0,0,0,.55)}
.panel .win{position:relative;width:100%;height:100%;overflow:hidden;background:#222}
.card{background:rgba(11,6,18,.88);box-shadow:0 0 0 4px var(--rosa),0 22px 60px rgba(0,0,0,.5)}
.bar{height:8px;background:linear-gradient(90deg,var(--rosa),var(--naranja))}
.flash{position:absolute;inset:0;background:#ffe9f4;opacity:0;z-index:50;pointer-events:none}
.shade-b{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,8,38,0) 45%,rgba(20,8,38,.85) 100%)}
.tint{position:absolute;inset:0;background:linear-gradient(180deg,rgba(80,20,120,.0),rgba(255,80,140,.10));mix-blend-mode:screen}
.cliptag{position:absolute;left:80px;bottom:80px;z-index:6;padding:14px 24px}
.subt{position:absolute;z-index:8;opacity:0;text-align:center}
.subt span{display:inline-block;background:rgba(11,6,18,.9);box-shadow:0 0 0 4px var(--rosa);padding:10px 26px;font-family:Jost,sans-serif;font-weight:700;font-size:__SUBF__px;line-height:1.15;color:#fff}
.star{display:inline-block;width:__STAR__px;height:__STAR__px;margin:0 8px;background:#0b0612;
  clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}
.star i{position:absolute;inset:6px;background:#fff;clip-path:inherit;opacity:.18}
"""


CSS = (CSS.replace("__SUN__", str(int(W * .62))).replace("__SUNH__", str(int(W * .31))).replace("__SUNB__", str(int(W * .36)))
       .replace("__STK__", "10" if not V else "9").replace("__STAR__", "120" if not V else "110").replace("__KS__", "34" if not V else "44").replace("__SUBF__", "50" if not V else "54"))


JS_HELPERS_T = """
const tl = gsap.timeline({ paused: true });
const E = { inn: "expo.out", cam: "power2.inOut", out: "power3.in" };
function words(sel, at, gap) { tl.fromTo(sel, {opacity:0, y:18}, {opacity:1, y:0, duration:0.25, stagger:gap||0.07, ease:"back.out(2)"}, at); }
function blurIn(sel, at, d) { tl.fromTo(sel, {opacity:0, filter:"blur(10px)"}, {opacity:1, filter:"blur(0px)", duration:d||0.35, ease:"power4.out"}, at); }
function slam(sel, at) { tl.fromTo(sel, {opacity:0, scale:1.6, rotation:-4}, {opacity:1, scale:1, rotation:0, duration:0.45, ease:"back.out(2.2)"}, at); }
function maskUp(sel, at) { tl.fromTo(sel, {opacity:0, clipPath:"inset(100% 0 -20% 0)", y:50}, {opacity:1, clipPath:"inset(0% 0 -20% 0)", y:0, duration:0.6, ease:"expo.out"}, at); }
function track(sel, at) { tl.fromTo(sel, {opacity:0, x:-30}, {opacity:1, x:0, duration:0.55, ease:"expo.out"}, at); }
function rise(sel, at, d) { tl.fromTo(sel, {opacity:0, y:26}, {opacity:1, y:0, duration:d||0.5, ease:"expo.out"}, at); }
function count(sel, to, at, d) { tl.fromTo(sel, {textContent:0}, {textContent:to, duration:d||0.9, snap:{textContent:1}, ease:"power2.out"}, at); }
function grow(sel, at, origin) { tl.fromTo(sel, {scaleX:0, transformOrigin:origin||"left center"}, {scaleX:1, duration:0.7, ease:"expo.out"}, at); }
function kb(sel, at, d, dir) {
  const m = {in:[1.0,1.08,0,0], out:[1.08,1.0,0,0], l:[1.07,1.07,34,-34], r:[1.07,1.07,-34,34], up:[1.05,1.1,0,0]}[dir||"in"];
  tl.fromTo(sel, {scale:m[0], x:m[2]}, {scale:m[1], x:m[3], duration:d, ease:"power1.inOut"}, at);
}
function sweep(sel, at, d) { tl.fromTo(sel, {x:0}, {x:__SW__, duration:d, ease:"power1.inOut"}, at); }
function flash(sel, at) { tl.fromTo(sel, {opacity:0}, {opacity:0.9, duration:0.05, ease:"none"}, at); tl.to(sel, {opacity:0, duration:0.35, ease:"power2.out"}, at + 0.05); }
function panelIn(sel, at, rot) { tl.fromTo(sel, {opacity:0, scale:.7, rotation:(rot||0)*4}, {opacity:1, scale:1, rotation:rot||0, duration:0.6, ease:"back.out(1.6)"}, at); }
function starOn(sel, at) { tl.fromTo(sel, {background:"#0b0612", scale:1.5}, {background:"#ffffff", scale:1, duration:0.3, ease:"back.out(3)"}, at); }
"""


JS_HELPERS = JS_HELPERS_T.replace("__SW__", str(int(W * 1.75)))


def sky_bg(pid, L, sh, grid=True):
    d = sh["end"] - sh["t"]
    h = f'<div class="fill sky"></div><div class="sun"></div>' + ('<div class="grid"></div>' if grid else "")
    h += f'<div id="{pid}-sw" class="light-sweep"></div>'
    return h, f'sweep("#{pid}-sw",{L(sh["t"]):.2f},{max(d, 2.5):.2f});'


def media_html(pid, p, d, L, sh, pos="50% 30%"):
    if p.get("video"):
        return (f'<video id="{pid}-v" class="clip media" data-start="{L(sh["t"]):.3f}" data-duration="{d + 0.6:.3f}" '
                f'{f"data-media-start=\"{p[chr(100)+"esde"]:.2f}\" " if p.get("desde") else ""}src="{AS.vid(p["video"])}" muted playsinline style="object-position:{p.get("pos", "50% 50%")}"></video>')
    return f'<img class="media" src="{AS.img(p["img"])}" style="object-position:{p.get("pos", pos)}">'


def text_block(pid, p, sh, L, js, align="left", fst=None):
    """kick + titulo (Pricedown) + sub + dato. Devuelve html y agrega js."""
    h = ""
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div><div id="{pid}-r" class="bar" style="width:140px;margin:18px {"auto" if align == "center" else "0"} 24px"></div>'
        js.append(f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.25)):.2f});grow("#{pid}-r",{L(p.get("tk", sh["t"] + 0.25)) + 0.15:.2f});')
    if p.get("dato"):
        pre, num, suf, etq, tdat = p["dato"]
        fs = p.get("fsd", 230 if not V else 210)
        h += (f'<div id="{pid}-dn" class="price grad" style="font-size:{fs}px">{esc(pre)}<span id="{pid}-dc">{esc(num)}</span>'
              f'<span style="font-size:{int(fs * .45)}px">{esc(suf)}</span></div>'
              f'<div id="{pid}-dl" class="sub" style="font-size:{p.get("fsl", 40)}px;margin-top:14px">{esc(etq)}</div>')
        js.append(f'slam("#{pid}-dn",{L(tdat):.2f});blurIn("#{pid}-dl",{L(tdat) + 0.35:.2f});')
        if str(num).isdigit() and p.get("cuenta", True):
            js.append(f'count("#{pid}-dc",{num},{L(tdat):.2f},0.9);')
    if p.get("titulo"):
        cls = "px" if p.get("pixel") else "price"
        fs = p.get("fst", fst or (110 if not V else 116))
        fs = min(fs, int(((W - 160) if V else 1100) / (0.68 * max(len(x) for x in p["titulo"].split()))))
        if p.get("pixel"):
            fs = int(fs * .5)
        h += f'<div id="{pid}-t" class="{cls}" style="font-size:{fs}px;margin-top:{16 if p.get("dato") else 0}px">{esc(p["titulo"])}</div>'
        js.append(f'maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.45)):.2f});')
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="sub" style="font-size:{p.get("fss", 46 if not V else 52)}px;margin-top:22px">{wspan(p["sub"])}</div>'
        js.append(f'words("#{pid}-s .w",{L(p.get("ts", sh["t"] + 0.9)):.2f},0.05);')
    return h


def subs_html(pid, subs, t0, js, box):
    """Subtítulos (t_ini, t_fin, texto) relativos al inicio del clip; tarjeta oscura que tapa los subtítulos quemados de origen."""
    h = ""
    for k, (a, b, txt) in enumerate(subs):
        h += (f'<div id="{pid}-sb{k}" class="subt" style="{box}"><span>{esc(txt)}</span></div>')
        js.append(f'tl.fromTo("#{pid}-sb{k}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{t0 + a:.2f});'
                  f'tl.to("#{pid}-sb{k}",{{opacity:0,duration:0.1}},{t0 + b:.2f});')
    return h


def r_clip(pid, sh, L):
    """Momento con sonido original. 16:9: sale de un panel girado y llena la pantalla. 9:16: panel 4:3 sobre el cielo.
    p: clip, pos, tag (#N · STREAMER, fijo todo el clip), subs=[(ini, fin, texto)], titulo (9:16, arriba)."""
    p = sh["p"]
    src = AS.vid(p["clip"])
    d = sh["clip_end"] - sh["clip_start"]
    t = L(sh["clip_start"])
    bg, js0 = sky_bg(pid, L, sh)
    js = [js0]
    vid = (f'<video id="{pid}-v" class="clip media" data-start="{t:.3f}" data-duration="{d:.3f}" src="{src}" muted playsinline '
           f'style="object-position:{p.get("pos", "50% 50%")}"></video>')
    if not V:
        h = bg + (f'<div id="{pid}-pr" style="position:absolute;inset:0;background:#0b0612">'
                  f'<div id="{pid}-kb" style="position:absolute;inset:0;overflow:hidden">{vid}</div>'
                  f'<div id="{pid}-mb" style="position:absolute;inset:0;border:22px solid #0b0612;box-shadow:inset 0 0 0 6px #fff"></div></div>')
        js.append(f'tl.fromTo("#{pid}-pr",{{scale:.55,rotation:-4}},{{scale:1,rotation:0,duration:0.7,ease:"expo.inOut"}},{t - 0.25:.2f});'
                  f'tl.to("#{pid}-mb",{{opacity:0,duration:0.3}},{t + 0.35:.2f});'
                  f'tl.fromTo("#{pid}-kb",{{scale:1.0}},{{scale:1.04,duration:{d:.2f},ease:"none"}},{t:.2f});')
        sbox = "left:50%;bottom:34px;transform:translateX(-50%);max-width:1500px;"
        if p.get("tag"):
            h += f'<div id="{pid}-tag" class="cliptag card" style="left:44px;top:40px;bottom:auto"><span class="kick">{esc(p["tag"])}</span></div>'
            js.append(f'rise("#{pid}-tag",{t + 0.5:.2f});')
    elif p.get("cam"):
        # Short con facecam: cara ampliada arriba (recorte de la misma fuente) + gameplay completo abajo
        cx, cy, cw0, ch0 = p["cam"]
        cw = 660
        ch = int(cw * ch0 / cw0)
        sc = cw / cw0
        cy0 = 290
        gw, gh = 1040, 585
        gy = cy0 + ch + 70
        h = bg + (f'<div id="{pid}-cp" class="panel" style="left:{(W - cw) // 2}px;top:{cy0}px;width:{cw}px;height:{ch}px;padding:10px;transform:rotate(-1.5deg)">'
                  f'<div class="win"><video id="{pid}-vc" class="clip" data-start="{t:.3f}" data-duration="{d:.3f}" src="{src}" muted playsinline '
                  f'style="position:absolute;max-width:none;width:{1920 * sc:.0f}px;height:{1080 * sc:.0f}px;left:{-cx * sc:.0f}px;top:{-cy * sc:.0f}px"></video></div></div>'
                  f'<div id="{pid}-pr" class="panel" style="left:{(W - gw) // 2}px;top:{gy}px;width:{gw}px;height:{gh}px;padding:10px">'
                  f'<div class="win"><div id="{pid}-kb" style="position:absolute;inset:0">{vid}</div></div></div>')
        js.append(f'panelIn("#{pid}-cp",{t - 0.3:.2f},-1.5);panelIn("#{pid}-pr",{t - 0.15:.2f},0);'
                  f'tl.fromTo("#{pid}-kb",{{scale:1.0}},{{scale:1.04,duration:{d:.2f},ease:"none"}},{t:.2f});')
        sbox = f"left:50%;top:{gy + gh + 40}px;transform:translateX(-50%);width:{W - 100}px;"
        py = cy0
    else:
        pw, ph, py = 1040, 780, 470
        h = bg + (f'<div id="{pid}-pr" class="panel" style="left:{(W - pw) // 2}px;top:{py}px;width:{pw}px;height:{ph}px;padding:10px">'
                  f'<div class="win"><div id="{pid}-kb" style="position:absolute;inset:0">{vid}</div></div></div>')
        js.append(f'panelIn("#{pid}-pr",{t - 0.3:.2f},0);'
                  f'tl.fromTo("#{pid}-kb",{{scale:1.0}},{{scale:1.05,duration:{d:.2f},ease:"none"}},{t:.2f});')
        sbox = f"left:50%;top:{py + ph + 50}px;transform:translateX(-50%);width:{W - 100}px;"
    if V:
        if p.get("tag"):
            h += (f'<div id="{pid}-tag" class="card" style="position:absolute;left:50%;transform:translateX(-50%);top:{py - 100}px;padding:12px 26px;white-space:nowrap">'
                  f'<span class="kick">{esc(p["tag"])}</span></div>')
            js.append(f'rise("#{pid}-tag",{t + 0.2:.2f});')
        if p.get("titulo"):
            h += (f'<div id="{pid}-tt" class="price grad" style="position:absolute;left:50px;right:50px;top:{55 if p.get("cam") else 150}px;text-align:center;'
                  f'font-size:{p.get("fst", 120)}px">{esc(p["titulo"])}</div>')
            js.append(f'slam("#{pid}-tt",{t:.2f});')
    h += subs_html(pid, p.get("subs", []), t, js, sbox)
    return h, "".join(js)


def r_rank(pid, sh, L):
    """Puesto del top: número gigante (#12), streamer, título del momento; vista previa muda del clip en panel."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, j0 = sky_bg(pid, L, sh)
    js = [j0]
    h = bg
    if not V:
        pw, ph, px, py = 980, 551, W - 980 - 110, 250
        box = f"left:100px;width:{px - 160}px;top:50%;transform:translateY(-50%);"
        fsn = 330
    else:
        pw, ph, px, py = 980, 551, (W - 980) // 2, 1080
        box = f"left:60px;width:{W - 120}px;top:230px;text-align:center;"
        fsn = 300
    h += (f'<div id="{pid}-pr" class="panel" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(2.5deg)">'
          f'<div class="win"><div id="{pid}-kb" class="kb"><video id="{pid}-v" class="clip media" data-start="{t:.3f}" data-duration="{d + 0.6:.3f}" '
          f'{f"data-media-start=\"{p[chr(100)+"esde"]:.2f}\" " if p.get("desde") else ""}src="{AS.vid(p["video"])}" muted playsinline style="object-position:{p.get("pos", "50% 50%")}"></video></div></div></div>')
    js.append(f'panelIn("#{pid}-pr",{t + 0.35:.2f},2.5);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");')
    tn = L(p.get("tn", sh["t"] + 0.1))
    h += (f'<div style="position:absolute;{box}">'
          f'<div id="{pid}-n" class="price grad" style="font-size:{fsn}px;line-height:.9">{esc(p.get("pref", "#"))}{esc(p["num"])}</div>'
          f'<div id="{pid}-k" class="kick" style="margin-top:18px">{esc(p.get("kick", ""))}</div>'
          f'<div id="{pid}-t" class="price" style="font-size:{p.get("fst", 120 if not V else 116)}px;margin-top:14px">{esc(p["nombre"])}</div>'
          f'<div id="{pid}-s" class="sub" style="font-size:{46 if not V else 50}px;margin-top:22px">{wspan(p["sub"])}</div></div>')
    js.append(f'slam("#{pid}-n",{tn:.2f});track("#{pid}-k",{tn + 0.35:.2f});maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.6)):.2f});'
              f'words("#{pid}-s .w",{L(p.get("ts", sh["t"] + 1.2)):.2f},0.05);')
    return h, "".join(js)


def r_foto(pid, sh, L):
    """Imagen o b-roll a pantalla completa con Ken Burns; texto en tarjeta abajo."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = f'<div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div><div class="tint"></div>'
    js = [f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");']
    if p.get("kick") or p.get("titulo") or p.get("sub") or p.get("dato"):
        h += '<div class="shade-b"></div>'
        x0, yb = (90, 90) if not V else (60, 470)
        mw = p.get("mw", 1250 if not V else W - 120)
        h += f'<div id="{pid}-c" style="position:absolute;left:{x0}px;bottom:{yb}px;max-width:{mw}px">'
        h += text_block(pid, p, sh, L, js, fst=p.get("fst", 104 if not V else 104))
        h += "</div>"
    return h, "".join(js)


def r_panel(pid, sh, L):
    """Media dentro de un panel tipo carátula (borde negro + filo blanco, giro) sobre el cielo; texto al lado."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, j0 = sky_bg(pid, L, sh)
    js = [j0]
    lado = p.get("lado", "der")
    vert = p.get("vertical", False)
    if not V:
        pw, ph = (600, 800) if vert else (960, 600)
        px = W - pw - 130 if lado == "der" else 130
        py = (H - ph) // 2 - 10
        tx = 110 if lado == "der" else px + pw + 100
        tw = (px - 90 - tx) if lado == "der" else (W - tx - 90)
        style = f"left:{tx}px;width:{tw}px;top:50%;transform:translateY(-50%);"
    else:
        pw, ph = (760, 1000) if vert else (940, 620)
        px, py = (W - pw) // 2, 260
        style = f"left:70px;width:{W - 140}px;top:{py + ph + 90}px;"
    rot = p.get("rot", 2.5 if lado == "der" else -2.5)
    h = bg + (f'<div id="{pid}-pr" class="panel" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate({rot}deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
    js.append(f'panelIn("#{pid}-pr",{t + 0.05:.2f},{rot});kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");')
    if p.get("pie"):
        h += f'<div id="{pid}-pie" class="tag" style="position:absolute;left:{px}px;top:{py + ph + 34}px;width:{pw}px;text-align:center">{esc(p["pie"])}</div>'
        js.append(f'blurIn("#{pid}-pie",{t + 0.7:.2f});')
    h += f'<div style="position:absolute;{style}">' + text_block(pid, p, sh, L, js, fst=p.get("fst", 100 if not V else 108)) + "</div>"
    return h, "".join(js)


def r_dato(pid, sh, L):
    """Cifra gigante (Pricedown, degradado de atardecer) que cuenta + etiqueta. Media opcional en panel."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = sky_bg(pid, L, sh)
    h = bg
    con = bool(p.get("img") or p.get("video"))
    if con:
        if not V:
            pw, ph, px, py = 640, 760, W - 640 - 140, (H - 760) // 2
        else:
            pw, ph, px, py = 760, 820, (W - 760) // 2, 220
        h += (f'<div id="{pid}-pr" class="panel" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(2.5deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
        js += f'panelIn("#{pid}-pr",{t + 0.05:.2f},2.5);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
    if not V:
        box = (f"left:110px;width:{(W - 640 - 140 - 200) if con else W - 220}px;top:50%;transform:translateY(-50%);"
               + ("" if con else "text-align:center;"))
    else:
        box = f"left:60px;width:{W - 120}px;top:{1120 if con else 560}px;text-align:center;"
    pre, num, suf = p.get("pre", ""), p["num"], p.get("suf", "")
    fs = p.get("fs", 300 if not V else 250)
    boxw = ((W - 640 - 140 - 200) if con else W - 220) if not V else W - 120
    nch = len(pre) + len(str(num)) + len(suf) * 0.42
    fs = min(fs, int(boxw / (0.66 * nch)))
    tn = L(p.get("tn", sh["t"] + 0.3))
    h += (f'<div style="position:absolute;{box}"><div id="{pid}-k" class="kick">{esc(p.get("kick", ""))}</div>'
          f'<div id="{pid}-n" class="price grad" style="font-size:{fs}px;margin-top:20px;white-space:nowrap">{esc(pre)}<span id="{pid}-c">{esc(num)}</span>'
          f'<span style="font-size:{int(fs * .42)}px">{esc(suf)}</span></div>'
          f'<div id="{pid}-l" class="sub" style="font-size:{p.get("fsl", 46 if not V else 50)}px;margin-top:26px">{esc(p.get("label", ""))}</div></div>')
    js += (f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.15)):.2f});slam("#{pid}-n",{tn:.2f});'
           f'blurIn("#{pid}-l",{L(p.get("tl", sh["t"] + 0.9)):.2f});')
    if p.get("cuenta", True) and str(num).isdigit():
        js += f'count("#{pid}-c",{num},{tn:.2f},{p.get("dc", 1.0)});'
    return h, js


def r_titulo(pid, sh, L):
    """Título de capítulo: kick, l1, l2 gigante en Pricedown con degradado, sub. pixel=True para la era 2D."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh)
    pad = "0 120px" if not V else "0 70px"
    h = bg + f'<div class="fill" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{pad}">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick" style="font-size:{40 if not V else 40}px">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.1)):.2f});'
    if p.get("l1"):
        h += f'<div id="{pid}-l1" class="price" style="font-size:{p.get("fs1", 96 if not V else 90)}px;margin-top:26px">{wspan(p["l1"])}</div>'
        js += f'words("#{pid}-l1 .w",{L(p.get("t1", sh["t"] + 0.25)):.2f},0.09);'
    if p.get("l2"):
        cls = "px" if p.get("pixel") else "price grad"
        fs = p.get("fs2", 250 if not V else 190)
        fs = min(fs, int((W - 160) / (0.68 * max(len(x) for x in p["l2"].split()))))
        if p.get("pixel"):
            fs = int(fs * .42)
        h += f'<div id="{pid}-l2" class="{cls}" style="font-size:{fs}px;margin-top:14px">{esc(p["l2"])}</div>'
        js += f'slam("#{pid}-l2",{L(p.get("t2", sh["t"] + 0.5)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="script" style="font-size:{p.get("fss", 70 if not V else 66)}px;margin-top:34px">{esc(p["sub"])}</div>'
        js += f'blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 1.0)):.2f});'
    h += "</div>"
    return h, js


def r_lista(pid, sh, L):
    """Lista: número en Pricedown + texto, cada renglón cuando la voz lo dice. items=[(titulo, sub, t)]."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh)
    x, y = (200, 150) if not V else (70, 360)
    h = bg + f'<div style="position:absolute;left:{x}px;top:{y}px;right:{x}px">'
    h += f'<div id="{pid}-k" class="kick">{esc(p.get("kick", ""))}</div><div id="{pid}-r" class="bar" style="width:140px;margin:18px 0 36px"></div>'
    js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});grow("#{pid}-r",{L(sh["t"] + 0.3):.2f});'
    for j, it in enumerate(p["items"]):
        titulo, sub, tt = it[:3]
        num = it[3] if len(it) > 3 else str(j + 1)
        h += (f'<div id="{pid}-i{j}" style="display:flex;gap:40px;align-items:center;margin-top:{0 if j == 0 else p.get("gap", 34)}px">'
              f'<div class="price grad" style="font-size:{p.get("fsn", 130 if not V else 120)}px;min-width:{p.get("wn", 130)}px;text-align:center">{esc(num)}</div>'
              f'<div><div class="price" style="font-size:{p.get("fsi", 70 if not V else 66)}px">{esc(titulo)}</div>'
              f'<div class="sub" style="font-size:{40 if not V else 40}px;margin-top:8px;color:#ffd9ec">{esc(sub)}</div></div></div>')
        js += f'tl.fromTo("#{pid}-i{j}",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:0.5,ease:"back.out(1.6)"}},{L(tt):.2f});'
    h += "</div>"
    return h, js


def r_galeria(pid, sh, L):
    """Carátulas en paneles que caen una a una con su año. items=[(img, etiqueta, t, pos)]."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh)
    items = p["items"]
    n = len(items)
    h = bg
    cols = p.get("cols", n if not V else 2)
    rows = (n + cols - 1) // cols
    if not V:
        pw = p.get("pw", min(380, int((W - 200 - (cols - 1) * 40) / cols)))
        ph = int(pw * 1.36)
        gap = (W - 200 - cols * pw) / max(1, cols - 1)
        y0 = (H - rows * (ph + 90)) // 2 + 30
    else:
        pw = p.get("pw", 420)
        ph = int(pw * 1.3)
        gap = W - 140 - 2 * pw
        y0 = p.get("y0", 300)
    for j, it in enumerate(items):
        img, nombre, tt = it[0], it[1], it[2]
        pos = it[3] if len(it) > 3 else "50% 30%"
        rot = [-3, 2, -1.5, 2.5, -2, 1.5, -2.5, 2][j % 8]
        c, r = j % cols, j // cols
        x = (100 if not V else 70) + c * (pw + gap)
        yy = y0 + r * (ph + 100) + (20 if j % 2 and not V else 0)
        hi = p.get("destaca") == j
        h += (f'<div id="{pid}-p{j}" class="panel" style="left:{x:.0f}px;top:{yy}px;width:{pw}px;height:{ph}px;transform:rotate({rot}deg);'
              f'{"box-shadow:0 0 0 5px #fff,0 0 0 13px #ff4fa3,0 30px 70px rgba(0,0,0,.55);" if hi else ""}">'
              f'<div class="win"><img class="media" src="{AS.img(img)}" style="object-position:{pos}"></div>'
              f'<div class="price" style="position:absolute;left:0;right:0;bottom:-74px;text-align:center;font-size:{56 if not V else 56}px">{esc(nombre)}</div></div>')
        js += f'panelIn("#{pid}-p{j}",{L(tt):.2f},{rot});'
    if p.get("kick"):
        ky = 60 if not V else 140
        h += f'<div id="{pid}-k" class="kick" style="position:absolute;left:0;right:0;top:{ky}px;text-align:center;font-size:40px">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.1)):.2f});'
    return h, js


def r_comparar(pid, sh, L):
    """Pantalla dividida: dos medias con etiqueta (izq/der o arriba/abajo). a=dict(img|video, etq, t), b=..."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    h, js = "", ""
    for k, lado in (("a", 0), ("b", 1)):
        q = p[k]
        tk = L(min(q.get("t", sh["t"]), sh["t"] + 0.15)) if lado == 0 else L(min(q.get("t", sh["t"] + 0.6), sh["t"] + 1.8))
        if not V:
            box = f"left:{lado * W // 2}px;top:0;width:{W // 2}px;height:{H}px"
            clip0 = "inset(0 100% 0 0)" if lado == 0 else "inset(0 0 0 100%)"
        else:
            box = f"left:0;top:{lado * H // 2}px;width:{W}px;height:{H // 2}px"
            clip0 = "inset(0 0 100% 0)" if lado == 0 else "inset(100% 0 0 0)"
        sub = dict(q)
        h += (f'<div id="{pid}-{k}" style="position:absolute;{box};overflow:hidden"><div id="{pid}-{k}kb" class="kb">'
              f'{media_html(pid + k, sub, d, L, sh)}</div><div class="shade-b"></div>'
              f'<div id="{pid}-{k}t" class="price grad" style="position:absolute;left:0;right:0;bottom:{60 if not V else 40}px;text-align:center;font-size:{q.get("fs", 150 if not V else 130)}px">{esc(q["etq"])}</div></div>')
        js += (f'tl.fromTo("#{pid}-{k}",{{clipPath:"{clip0}"}},{{clipPath:"inset(0 0 0 0)",duration:0.7,ease:"expo.inOut"}},{tk:.2f});'
               f'kb("#{pid}-{k}kb",{tk:.2f},{d + 0.6:.2f},"{q.get("kb", "in")}");slam("#{pid}-{k}t",{tk + 0.4:.2f});')
    if not V:
        h += f'<div id="{pid}-div" style="position:absolute;left:{W // 2 - 6}px;top:0;width:12px;height:{H}px;background:#0b0612;box-shadow:0 0 0 3px #fff"></div>'
        js += f'tl.fromTo("#{pid}-div",{{scaleY:0}},{{scaleY:1,duration:0.6,ease:"expo.out"}},{t + 0.3:.2f});'
    else:
        h += f'<div id="{pid}-div" style="position:absolute;top:{H // 2 - 6}px;left:0;height:12px;width:{W}px;background:#0b0612;box-shadow:0 0 0 3px #fff"></div>'
        js += f'tl.fromTo("#{pid}-div",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"expo.out"}},{t + 0.3:.2f});'
    if p.get("vs", True):
        vsx = "left:50%;margin-left:-120px" if not V else "right:40px"
        h += (f'<div id="{pid}-vs" class="price" style="position:absolute;{vsx};top:50%;width:240px;margin-top:-110px;'
              f'text-align:center;font-size:{180 if not V else 160}px;color:#ff4fa3">VS</div>')
        js += f'slam("#{pid}-vs",{L(p.get("tvs", sh["t"] + 0.9)):.2f});'
    if p.get("kick"):
        h += (f'<div id="{pid}-k" class="card" style="position:absolute;left:50%;transform:translateX(-50%);top:{50 if not V else 120}px;padding:14px 30px;white-space:nowrap">'
              f'<span class="kick">{esc(p["kick"])}</span></div>')
        js += f'rise("#{pid}-k",{L(p.get("tk", sh["t"] + 0.2)):.2f});'
    return h, js


def r_versus(pid, sh, L):
    """Dos cifras enfrentadas (p.ej. crítica 99 vs usuarios 5). a=(num, etiqueta, t, color) b=..."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh)
    h = bg
    for k, lado in (("a", 0), ("b", 1)):
        num, etq, tt = p[k][:3]
        mal = len(p[k]) > 3 and p[k][3] == "mal"
        if not V:
            box = f"left:{110 + lado * (W // 2)}px;width:{W // 2 - 220}px;top:50%;transform:translateY(-46%);text-align:center"
        else:
            box = f"left:60px;width:{W - 120}px;top:{300 + lado * 760}px;text-align:center"
        fs = p.get("fs", 420 if not V else 380)
        color = "" if not mal else "background:linear-gradient(180deg,#ffffff,#9a8cff);-webkit-background-clip:text;background-clip:text;"
        h += (f'<div style="position:absolute;{box}"><div id="{pid}-{k}n" class="price grad" style="font-size:{fs}px;{color}">{esc(num)}</div>'
              f'<div id="{pid}-{k}l" class="kick" style="font-size:{50 if not V else 50}px;margin-top:20px;color:{"#3de0ff" if mal else "#ff4fa3"}">{esc(etq)}</div></div>')
        js += f'slam("#{pid}-{k}n",{L(tt):.2f});track("#{pid}-{k}l",{L(tt) + 0.3:.2f});'
    h += (f'<div id="{pid}-vs" class="price" style="position:absolute;left:50%;top:50%;width:300px;margin-left:-150px;margin-top:{-100 if not V else -120}px;'
          f'text-align:center;font-size:{150 if not V else 140}px">VS</div>')
    js += f'blurIn("#{pid}-vs",{L(p["b"][2]) - 0.3:.2f});'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick" style="position:absolute;left:0;right:0;top:{80 if not V else 150}px;text-align:center;font-size:44px">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});'
    return h, js


def r_linea(pid, sh, L):
    """Barras de años entre entregas; crecen en proporción. items=[(etiqueta, años, t)]; la última, destacada."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh, grid=False)
    items = p["items"]
    mx = max(x[1] for x in items)
    if not V:
        x0, y0, lw, bw, rh = 140, 210, 560, W - 140 - 560 - 260, (H - 300) / len(items)
    else:
        x0, y0, lw, bw, rh = 60, 380, 420, W - 60 - 420 - 190, (H - 700) / len(items)
    h = bg
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick" style="position:absolute;left:{x0}px;top:{y0 - 110}px;font-size:40px">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});'
    for j, (etq, anios, tt) in enumerate(items):
        last = j == len(items) - 1
        y = y0 + j * rh
        wbar = max(30, bw * anios / mx)
        col = "linear-gradient(90deg,#ff3f8f,#ff8a3d,#ffc65c)" if last else "linear-gradient(90deg,#7a3fd0,#ff4fa3)"
        h += (f'<div id="{pid}-e{j}" class="sub" style="position:absolute;left:{x0}px;top:{y:.0f}px;width:{lw - 30}px;height:{rh * .8:.0f}px;display:flex;align-items:center;justify-content:flex-end;'
              f'font-size:{36 if not V else 30}px;text-align:right">{esc(etq)}</div>'
              f'<div id="{pid}-b{j}" style="position:absolute;left:{x0 + lw}px;top:{y + rh * .12:.0f}px;width:{wbar:.0f}px;height:{rh * .56:.0f}px;background:{col};'
              f'box-shadow:0 0 0 4px #0b0612{",0 0 30px rgba(255,120,80,.8)" if last else ""}"></div>'
              f'<div id="{pid}-n{j}" class="price" style="position:absolute;left:{x0 + lw + wbar + 24:.0f}px;top:{y - rh * .05:.0f}px;font-size:{rh * (1.0 if last else .78):.0f}px">'
              f'{anios}<span style="font-size:.45em"> {"AÑO" if anios == 1 else "AÑOS"}</span></div>')
        js += (f'rise("#{pid}-e{j}",{L(tt):.2f},0.35);grow("#{pid}-b{j}",{L(tt):.2f});'
               f'tl.fromTo("#{pid}-n{j}",{{opacity:0}},{{opacity:1,duration:0.3}},{L(tt) + 0.45:.2f});')
    return h, js


def r_estrellas(pid, sh, L):
    """Nivel de búsqueda: fila de estrellas que se encienden. n=total, on=[(k, t)], texto abajo."""
    p = sh["p"]
    bg, js = sky_bg(pid, L, sh)
    h = bg
    if p.get("img") or p.get("video"):
        d = sh["end"] - sh["t"]
        h = f'<div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div><div class="fill" style="background:rgba(20,8,38,.55)"></div>'
        js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"in");'
    n = p.get("n", 6)
    top = 300 if not V else 640
    h += f'<div style="position:absolute;left:0;right:0;top:{top}px;text-align:center">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick" style="font-size:44px;margin-bottom:40px">{esc(p["kick"])}</div>'
        js += f'track("#{pid}-k",{L(sh["t"] + 0.1):.2f});'
    h += '<div style="white-space:nowrap">'
    for k in range(n):
        h += f'<span id="{pid}-st{k}" class="star"></span>'
    h += "</div>"
    if p.get("titulo"):
        h += f'<div id="{pid}-t" class="price" style="font-size:{p.get("fst", 110 if not V else 100)}px;margin-top:60px;padding:0 60px">{esc(p["titulo"])}</div>'
        js += f'maskUp("#{pid}-t",{L(p.get("tt", sh["t"] + 0.5)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="sub" style="font-size:{46 if not V else 48}px;margin-top:24px;padding:0 80px">{wspan(p["sub"])}</div>'
        js += f'words("#{pid}-s .w",{L(p.get("ts", sh["t"] + 0.9)):.2f},0.05);'
    h += "</div>"
    js += f'tl.fromTo("#{pid} .star",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,stagger:0.05}},{L(sh["t"] + 0.1):.2f});'
    for k, tt in p.get("on", []):
        js += f'starOn("#{pid}-st{k}",{L(tt):.2f});'
    return h, js


def r_cita(pid, sh, L):
    """Cita en tarjeta, con comillas rosas; media opcional en panel."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = sky_bg(pid, L, sh)
    h = bg
    if p.get("img") or p.get("video"):
        pw, ph = (560, 720) if not V else (680, 820)
        px, py = (W - pw - 140, (H - ph) // 2) if not V else ((W - pw) // 2, 200)
        h += (f'<div id="{pid}-pr" class="panel" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(-2.5deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div></div></div>')
        js += f'panelIn("#{pid}-pr",{t + 0.05:.2f},-2.5);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
        box = "left:120px;width:1000px;top:50%;transform:translateY(-50%);" if not V else f"left:70px;width:{W - 140}px;top:1110px;"
    else:
        box = "left:200px;right:200px;top:50%;transform:translateY(-50%);text-align:center;" if not V else f"left:70px;width:{W - 140}px;top:560px;"
    fs = p.get("fs", 70 if not V else 66)
    h += (f'<div style="position:absolute;{box}"><div class="price" style="color:#ff4fa3;font-size:240px;line-height:.6;height:100px">“</div>'
          f'<div id="{pid}-q" class="sub" style="font-size:{fs}px;line-height:1.15;font-weight:700">{wspan(p["texto"])}</div>'
          f'<div id="{pid}-r" class="bar" style="width:140px;margin:40px {"auto" if "center" in box else "0"} 22px"></div>'
          f'<div id="{pid}-a" class="kick">{esc(p["autor"])}</div></div>')
    js += (f'words("#{pid}-q .w",{L(p.get("tq", sh["t"] + 0.2)):.2f},{p.get("gap", 0.08)});'
           f'grow("#{pid}-r",{L(p.get("ta", sh["t"] + 1.0)):.2f});track("#{pid}-a",{L(p.get("ta", sh["t"] + 1.0)) + 0.15:.2f});')
    return h, js


def r_cta(pid, sh, L):
    """Final de Short: miniatura del largo en panel + 'VIDEO COMPLETO EN EL CANAL' + flecha."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    t = L(sh["t"])
    bg, js = sky_bg(pid, L, sh)
    pw, ph = (900, 506) if V else (900, 506)
    px, py = ((W - pw) // 2, 560) if V else ((W - pw) // 2, 250)
    h = bg + (f'<div id="{pid}-pr" class="panel" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;transform:rotate(-2deg)">'
              f'<div class="win"><div id="{pid}-kb" class="kb">{media_html(pid, p, d, L, sh)}</div>'
              f'<div class="price grad" style="position:absolute;left:30px;bottom:24px;font-size:96px">{esc(p.get("en_mini", "1997 VS 2026"))}</div>'
              f'<div style="position:absolute;right:24px;bottom:24px;background:rgba(0,0,0,.8);color:#fff;font:600 30px Jost;padding:4px 12px">{esc(p.get("dur", "13:00"))}</div></div></div>')
    js += f'panelIn("#{pid}-pr",{t + 0.05:.2f},-2);kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
    ty = py + ph + (110 if V else 70)
    h += (f'<div style="position:absolute;left:60px;right:60px;top:{ty}px;text-align:center">'
          f'<div id="{pid}-k" class="kick" style="font-size:44px">{esc(p.get("kick", "VIDEO COMPLETO"))}</div>'
          f'<div id="{pid}-t" class="price" style="font-size:{120 if V else 110}px;margin-top:20px">{esc(p.get("titulo", "EN MI CANAL"))}</div>'
          f'<div id="{pid}-ar" class="price grad" style="font-size:150px;margin-top:10px">▼</div></div>')
    js += (f'track("#{pid}-k",{L(p.get("tk", sh["t"] + 0.2)):.2f});slam("#{pid}-t",{L(p.get("tt", sh["t"] + 0.5)):.2f});'
           f'tl.fromTo("#{pid}-ar",{{y:-20,opacity:0}},{{y:20,opacity:1,duration:0.5,repeat:{int(max(1, d / 0.5))},yoyo:true,ease:"sine.inOut"}},{L(sh["t"] + 0.9):.2f});')
    return h, js


TRANS = {"corte": 0.0, "fundido": 0.45, "panel": 0.6, "flash": 0.0, "crece": 0.55, "iris": 0.65, "latigo": 0.4}


def trans_js(pid, prev, kind, t):
    d = TRANS[kind]
    s = f'#{pid}'
    js = f'tl.set("{s}",{{opacity:1}},{t:.3f});'
    if kind == "fundido":
        js = f'tl.fromTo("{s}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power1.inOut"}},{t:.3f});'
    elif kind == "panel":
        js += (f'tl.fromTo("{s}",{{clipPath:"polygon(120% 0%,120% 0%,120% 100%,100% 100%)"}},'
               f'{{clipPath:"polygon(0% 0%,120% 0%,120% 100%,-20% 100%)",duration:{d},ease:"power3.inOut"}},{t:.3f});')
        if prev:
            js += f'tl.fromTo("#{prev}",{{x:0}},{{x:{-W * 0.1:.0f},duration:{d},ease:"power3.inOut",immediateRender:false}},{t:.3f});'
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


SFX_ENTRADA = {"panel": ("whoosh", -16), "latigo": ("whoosh", -14), "crece": ("whoosh", -17), "iris": ("whoosh", -16)}


def sfx_de(sh, primero):
    p, ev = sh["p"], []
    if not primero and sh["entrada"] in SFX_ENTRADA and sh["tipo"] != "clip":
        ev.append((sh["t"], *SFX_ENTRADA[sh["entrada"]]))
    if sh["tipo"] == "dato":
        ev.append((p.get("tn", sh["t"] + 0.3), "golpe", -12))
    if sh["tipo"] in ("panel", "foto") and p.get("dato"):
        ev.append((p["dato"][4], "golpe", -14))
    if sh["tipo"] == "versus":
        ev += [(p["a"][2], "golpe", -12), (p["b"][2], "golpe", -12)]
    if sh["tipo"] == "titulo" and p.get("t2"):
        ev.append((p["t2"], "golpe", -15))
    if sh["tipo"] == "estrellas":
        ev += [(tt, "lapiz", -16) for _, tt in p.get("on", [])]
    if sh["tipo"] == "rank":
        ev.append((p.get("tn", sh["t"] + 0.1), "golpe", -12))
    if sh["tipo"] == "clip":
        ev.append((sh["clip_start"] - 0.25, "whoosh", -18))
    return ev



# ------------------------------------------------------------------ tratamiento de assets e index
BN_DEFAULT = False


def IMG_VF(bn):
    return "scale='min(2400,iw)':-2,eq=contrast=1.04:saturation=1.08"


def VID_VF(bn):
    return None


INDEX_BG = "#1a0b2e"
GRANO_CSS = 'position:absolute;inset:0;z-index:900;pointer-events:none;opacity:.05;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'240\' height=\'240\'><filter id=\'n\'><feTurbulence baseFrequency=\'.8\' numOctaves=\'2\' seed=\'11\'/></filter><rect width=\'100%\' height=\'100%\' filter=\'url(%23n)\'/></svg>")'

def post_shot(pid, sh, L, i):
    """Entrada «flash»: destello blanco + golpe."""
    if sh["entrada"] != "flash":
        return "", ""
    SFX.append((sh["t"], "golpe", -16))
    return f'<div id="{pid}-tfl" class="flash"></div>', f'flash("#{pid}-tfl",{L(sh["t"]):.2f});'

# ------------------------------------------------------------------ mezcla (ganancia por efecto y adelanto del pico)
SFX_GAIN = {"whoosh": -22, "golpe": -15, "obturador": -12, "papel": -16, "lapiz": -20}
PICO_ANTES = {"whoosh": -0.18}
