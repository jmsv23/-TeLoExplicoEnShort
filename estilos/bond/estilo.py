"""Estilo «Esmoquin» — plugin del motor (contrato: estilos/CONTRATO.md).

Extraído de james-bond/_prod/build.py (content-creator/explicando). El motor inyecta antes de usarlo:
W, H, V (vertical), AS (assets), esc, wspan, norm, HF, A_IMG, A_CUT, PIEZA, SFX, ESTILO_DIR, VIDEO.
"""
import html, json, re, subprocess, sys  # noqa: F401
from pathlib import Path  # noqa: F401

CSS = """
@font-face{font-family:Jost;src:url(assets/fonts/Jost.ttf);font-weight:100 900}
@font-face{font-family:Corm;src:url(assets/fonts/CormorantGaramond.ttf);font-weight:300 700}
@font-face{font-family:Corm;src:url(assets/fonts/CormorantGaramond-Italic.ttf);font-weight:300 700;font-style:italic}
@font-face{font-family:JBMono;src:url(assets/fonts/JetBrainsMono.ttf);font-weight:100 900}
#root{position:absolute;inset:0;overflow:hidden;background:#07070a;color:#ece6da;font-family:Jost,sans-serif;
  --negro:#07070a;--carbon:#111115;--linea:#2a2a31;--oro:#c8a45c;--oro-claro:#ecd59b;--marfil:#ece6da;--gris:#8b8b93;--rojo:#b0443a}
.shot{position:absolute;inset:0;overflow:hidden;opacity:0}
.fill{position:absolute;inset:0}
.world{background:radial-gradient(ellipse at 50% 45%,#18181d 0%,#07070a 70%)}
.haze{position:absolute;width:62%;height:70%;left:18%;top:15%;border-radius:50%;
  background:radial-gradient(closest-side,rgba(200,164,92,.12),rgba(200,164,92,0));filter:blur(30px)}
.ring{position:absolute;left:50%;top:50%;border-radius:50%}
.kick{font-family:JBMono,monospace;font-size:28px;letter-spacing:.42em;color:var(--oro);text-transform:uppercase}
.tag{font-family:JBMono,monospace;font-size:28px;letter-spacing:.24em;color:var(--gris);text-transform:uppercase}
.rule{height:1px;background:linear-gradient(90deg,transparent,var(--oro),transparent)}
.gold{background:linear-gradient(100deg,#9c7a3a 0%,#ecd59b 30%,#9c7a3a 45%,#fff6dc 50%,#9c7a3a 55%,#ecd59b 70%,#9c7a3a 100%);
  background-size:300% 100%;background-position:100% 0;-webkit-background-clip:text;background-clip:text;color:transparent}
.w{display:inline-block}
.light{font-weight:300}
.ital{font-family:Corm,serif;font-style:italic}
.mono{font-family:JBMono,monospace}
.media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.kb{position:absolute;inset:-2%}
.shade-b{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,7,10,.05) 0%,rgba(7,7,10,0) 40%,rgba(7,7,10,.12) 70%,rgba(7,7,10,.2) 100%)}
.shade-l{position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,7,10,.2) 0%,rgba(7,7,10,.12) 40%,rgba(7,7,10,0) 70%)}
.shade-all{position:absolute;inset:0;background:rgba(7,7,10,.2)}
.lb{position:absolute;left:0;right:0;height:64px;background:#000;z-index:5}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 240px 40px rgba(0,0,0,.2);pointer-events:none}
.txt{filter:drop-shadow(0 2px 3px rgba(0,0,0,.5)) drop-shadow(0 4px 20px rgba(0,0,0,.55))}
.txt, .txt *{text-shadow:0 0 3px rgba(0,0,0,.95),0 0 10px rgba(0,0,0,.85),0 0 26px rgba(0,0,0,.6)}
.gold, .gold *, .txt .gold, .txt .gold *{text-shadow:none!important}
.txt .kick{color:var(--oro-claro)}
.frame{position:absolute;border:1px solid rgba(200,164,92,.6)}
.cliptag{position:absolute;left:96px;bottom:104px;font-family:JBMono,monospace;font-size:28px;letter-spacing:.3em;color:var(--oro-claro);
  text-shadow:0 2px 12px #000;z-index:6}
.big{font-weight:600;letter-spacing:.1em;line-height:1}
.card{background:rgba(17,17,21,.2);border:1px solid rgba(236,230,218,.25)}
"""


JS_HELPERS = """
const tl = gsap.timeline({ paused: true });
const E = { inn: "expo.out", cam: "power2.inOut", out: "power3.in" };
function words(sel, at, gap) { tl.fromTo(sel, {opacity:0, filter:"blur(8px)"}, {opacity:1, filter:"blur(0px)", duration:0.22, stagger:gap||0.08, ease:"power4.out"}, at); }
function blurIn(sel, at, d) { tl.fromTo(sel, {opacity:0, filter:"blur(10px)"}, {opacity:1, filter:"blur(0px)", duration:d||0.35, ease:"power4.out"}, at); }
function goldIn(sel, at) {
  tl.fromTo(sel, {clipPath:"inset(0 100% 0 0)", x:-18, filter:"blur(6px)"}, {clipPath:"inset(0 0% 0 0)", x:0, filter:"blur(0px)", duration:0.85, ease:"expo.out"}, at);
  tl.fromTo(sel, {backgroundPosition:"100% 0"}, {backgroundPosition:"0% 0", duration:1.2, ease:"power2.inOut"}, at + 0.6);
}
function rise(sel, at, d) { tl.fromTo(sel, {opacity:0, y:18}, {opacity:1, y:0, duration:d||0.55, ease:"expo.out"}, at); }
function count(sel, to, at, d) { tl.fromTo(sel, {textContent:0}, {textContent:to, duration:d||0.9, snap:{textContent:1}, ease:"power2.out"}, at); }
function rule(sel, at, origin) { tl.fromTo(sel, {scaleX:0, transformOrigin:origin||"center"}, {scaleX:1, duration:0.8, ease:"expo.out"}, at); }
function kb(sel, at, d, dir) {
  const m = {in:[1.0,1.08,0,0], out:[1.08,1.0,0,0], l:[1.06,1.06,30,-30], r:[1.06,1.06,-30,30], up:[1.05,1.09,0,0]}[dir||"in"];
  tl.fromTo(sel, {scale:m[0], x:m[2]}, {scale:m[1], x:m[3], duration:d, ease:"power1.inOut"}, at);
}
function orbit(sel, at, d, deg) { tl.fromTo(sel, {rotation:0}, {rotation:deg, duration:d, ease:"none"}, at); }
function stamp(sel, at) { tl.fromTo(sel, {opacity:0, scale:1.6, filter:"blur(6px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.32, ease:"power4.out"}, at); }
"""


def world_bg(pid, L, sh, rings=True):
    d = sh["end"] - sh["t"]
    rs = ""
    js = f'tl.fromTo("#{pid}-haze",{{x:-120}},{{x:240,duration:{d:.2f},ease:"power1.inOut"}},{L(sh["t"]):.2f});'
    if rings:
        s1, s2, s3 = (0.47, 0.37, 0.62) if not V else (0.85, 0.67, 1.1)
        rs = (f'<div id="{pid}-r1" class="ring" style="width:{W*s1:.0f}px;height:{W*s1:.0f}px;margin:-{W*s1/2:.0f}px 0 0 -{W*s1/2:.0f}px;border:1.5px dashed rgba(200,164,92,.33)"></div>'
              f'<div class="ring" style="width:{W*s2:.0f}px;height:{W*s2:.0f}px;margin:-{W*s2/2:.0f}px 0 0 -{W*s2/2:.0f}px;border:1.5px solid rgba(200,164,92,.5)"></div>'
              f'<div id="{pid}-r3" class="ring" style="width:{W*s3:.0f}px;height:{W*s3:.0f}px;margin:-{W*s3/2:.0f}px 0 0 -{W*s3/2:.0f}px;border:1px solid #1d1d23"></div>')
        js += f'orbit("#{pid}-r1",{L(sh["t"]):.2f},{d:.2f},{d*3.5:.1f});orbit("#{pid}-r3",{L(sh["t"]):.2f},{d:.2f},{-d*2:.1f});'
    return f'<div class="fill world"></div><div id="{pid}-haze" class="haze"></div>{rs}', js


def r_clip(pid, sh, L):
    """Escena con sonido a color, pantalla completa. Entra por iris; leve empuje de cámara."""
    p = sh["p"]
    src = AS.vid(p["clip"])
    d = sh["clip_end"] - sh["clip_start"]
    h = (f'<div id="{pid}-kb" class="kb" style="inset:0"><video id="{pid}-v" class="clip media" data-start="{L(sh["clip_start"]):.3f}" '
         f'data-duration="{d:.3f}" src="{src}" muted playsinline></video></div>'
         f'<div class="lb" style="top:0"></div><div class="lb" style="bottom:0"></div><div class="vig"></div>')
    js = f'tl.fromTo("#{pid}-kb",{{scale:1.0}},{{scale:1.035,duration:{d:.2f},ease:"none"}},{L(sh["clip_start"]):.2f});'
    if p.get("tag"):
        h += f'<div id="{pid}-tag" class="cliptag">{esc(p["tag"])}</div>'
        js += f'blurIn("#{pid}-tag",{L(sh["clip_start"]) + 0.4:.2f});tl.to("#{pid}-tag",{{opacity:0,duration:0.3}},{L(sh["clip_start"]) + min(d - 0.4, 3.2):.2f});'
    return h, js


def r_foto(pid, sh, L):
    """Foto (B/N por defecto) a pantalla completa con Ken Burns; texto opcional abajo a la izquierda."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    if p.get("video"):
        media = (f'<video id="{pid}-v" class="clip media" data-start="{L(sh["t"]):.3f}" data-duration="{d + 0.6:.3f}" '
                 f'src="{AS.vid(p["video"], bn=p.get("bn", True))}" muted playsinline></video>')
    else:
        media = f'<img class="media" src="{AS.img(p["img"], bn=p.get("bn", True))}" style="object-position:{p.get("pos", "50% 30%")}">'
    h = f'<div id="{pid}-kb" class="kb">{media}</div>'
    h += '<div class="shade-b"></div>' if p.get("sombra", "b") == "b" else ('<div class="shade-l"></div>' if p.get("sombra") == "l" else "")
    h += '<div class="vig"></div>'
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"{p.get("kb", "in")}");'
    x0, yb = (96, 150) if not V else (90, 760)
    if p.get("kick") or p.get("l1") or p.get("l2"):
        h += f'<div class="txt" style="position:absolute;left:{x0}px;bottom:{yb}px;right:{x0 if not V else 190}px">'
        if p.get("kick"):
            h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
            js += f'blurIn("#{pid}-k",{L(p.get("tk", sh["t"] + 0.3)):.2f});'
        if p.get("l1"):
            fs = p.get("fs1", 96 if not V else 104)
            h += f'<div id="{pid}-l1" class="light" style="font-size:{fs}px;letter-spacing:.06em;line-height:1.05;margin-top:18px">{wspan(p["l1"])}</div>'
            js += f'words("#{pid}-l1 .w",{L(p.get("t1", sh["t"] + 0.4)):.2f});'
        if p.get("l2"):
            fs = p.get("fs2", 128 if not V else 132)
            h += f'<div id="{pid}-l2" class="gold big" style="font-size:{fs}px;display:inline-block">{esc(p["l2"])}</div>'
            js += f'goldIn("#{pid}-l2",{L(p.get("t2", sh["t"] + 0.6)):.2f});'
        if p.get("sub"):
            h += f'<div id="{pid}-s" class="ital" style="font-size:{56 if not V else 64}px;margin-top:18px">{esc(p["sub"])}</div>'
            js += f'blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 0.9)):.2f});'
        h += "</div>"
    if p.get("sello"):
        h += (f'<div id="{pid}-sello" style="position:absolute;right:{110 if not V else 70}px;top:{180 if not V else 380}px;'
              f'font-family:JBMono,monospace;font-weight:700;font-size:{p.get("fsello", 64)}px;letter-spacing:.12em;color:var(--rojo);'
              f'border:4px solid var(--rojo);padding:10px 26px;transform:rotate(-6deg)">{esc(p["sello"])}</div>')
        js += f'stamp("#{pid}-sello",{L(p.get("tsello", sh["t"] + 0.5)):.2f});'
    return h, js


def r_titulo(pid, sh, L):
    """Mundo de anillos + título cinético. l2 en oro."""
    p = sh["p"]
    bg, js = world_bg(pid, L, sh)
    f1, f2 = (140, 180) if not V else (118, 150)
    h = bg + f'<div class="fill txt" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{"0 80px" if not V else "0 180px 0 90px"}">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
        js += f'blurIn("#{pid}-k",{L(p.get("tk", sh["t"] + 0.15)):.2f});'
    if p.get("l1"):
        h += f'<div id="{pid}-l1" class="light" style="font-size:{p.get("fs1", f1)}px;letter-spacing:.12em;line-height:1.05;margin-top:30px">{wspan(p["l1"])}</div>'
        js += f'words("#{pid}-l1 .w",{L(p.get("t1", sh["t"] + 0.3)):.2f},0.09);'
    if p.get("l2"):
        h += f'<div id="{pid}-l2" class="gold big" style="font-size:{p.get("fs2", f2)}px;letter-spacing:.14em;line-height:1.08">{esc(p["l2"])}</div>'
        js += f'goldIn("#{pid}-l2",{L(p.get("t2", sh["t"] + 0.6)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-r" class="rule" style="width:{min(900, W - 200)}px;margin:38px 0 28px"></div>'
        h += f'<div id="{pid}-s" class="ital" style="font-size:{58 if not V else 66}px">{esc(p["sub"])}</div>'
        js += f'rule("#{pid}-r",{L(p.get("ts", sh["t"] + 1.0)) - 0.1:.2f});blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 1.0)):.2f});'
    h += "</div><div class='vig'></div>"
    return h, js


def r_ficha(pid, sh, L):
    """Expediente del actor: marco con foto/b-roll B/N, nombre, cifras que cuentan, y barra de recepción."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    bg, js = world_bg(pid, L, sh, rings=False)
    fx, fy, fw, fh = 140, 150, 640, 780
    if p.get("video"):
        media = (f'<video id="{pid}-v" class="clip media" data-start="{L(sh["t"]):.3f}" data-duration="{d + 0.6:.3f}" '
                 f'src="{AS.vid(p["video"], bn=True)}" muted playsinline></video>')
    else:
        media = f'<img class="media" src="{AS.img(p["img"])}" style="object-position:{p.get("pos", "50% 25%")}">'
    h = bg + (f'<div id="{pid}-foto" style="position:absolute;left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px;overflow:hidden;background:#111">'
              f'<div id="{pid}-kb" class="kb">{media}</div></div>'
              f'<div id="{pid}-marco" class="frame" style="left:{fx}px;top:{fy}px;width:{fw}px;height:{fh}px"></div>')
    t = L(sh["t"])
    js += (f'tl.fromTo("#{pid}-foto",{{clipPath:"inset(0 0 100% 0)"}},{{clipPath:"inset(0 0 0% 0)",duration:0.8,ease:E.inn}},{t + 0.05:.2f});'
           f'tl.fromTo("#{pid}-marco",{{opacity:0,scale:1.04}},{{opacity:1,scale:1,duration:0.9,ease:E.inn}},{t + 0.2:.2f});'
           f'kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"up");')
    h += f'<div class="txt" style="position:absolute;left:{fx + fw + 110}px;top:{fy}px;width:{W - fx - fw - 250}px">'
    h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
    js += f'blurIn("#{pid}-k",{t + 0.25:.2f});'
    h += f'<div id="{pid}-n1" class="light" style="font-size:112px;letter-spacing:.08em;line-height:1;margin-top:26px">{esc(p["nombre"])}</div>'
    h += f'<div id="{pid}-n2" class="gold big" style="font-size:150px;display:inline-block">{esc(p["apellido"])}</div>'
    js += f'blurIn("#{pid}-n1",{L(p["tn"]):.2f},0.3);goldIn("#{pid}-n2",{L(p["tn"]) + 0.22:.2f});'
    h += f'<div id="{pid}-r" class="rule" style="margin:36px 0"></div>'
    js += f'rule("#{pid}-r",{L(p["tn"]) + 0.5:.2f},"left center");'
    h += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">'
    for j, (lab, val, tv) in enumerate(p["datos"]):
        num = re.match(r"^(\d+)(.*)$", val)
        inner = (f'<span id="{pid}-c{j}">{num.group(1)}</span><span style="font-size:32px;color:var(--gris)">{esc(num.group(2))}</span>'
                 if num and not p.get("sin_cuenta", {}).get(j) else esc(val))
        h += f'<div id="{pid}-d{j}"><div class="tag">{esc(lab)}</div><div class="mono" style="font-size:76px;margin-top:6px">{inner}</div></div>'
        js += f'rise("#{pid}-d{j}",{L(tv):.2f});'
        if num and not p.get("sin_cuenta", {}).get(j):
            js += f'count("#{pid}-c{j}",{num.group(1)},{L(tv):.2f},{0.6 if int(num.group(1)) < 10 else 0.9});'
    h += "</div>"
    if p.get("recepcion") is not None:
        pct, tr = p["recepcion"]
        h += (f'<div id="{pid}-rec" style="margin-top:56px"><div class="tag">Recepción al anuncio</div>'
              f'<div style="height:6px;background:var(--linea);margin-top:16px;position:relative">'
              f'<div id="{pid}-bar" style="position:absolute;left:0;top:0;bottom:0;width:{pct}%;background:{"var(--rojo)" if pct < 50 else "var(--oro)"};transform-origin:left center"></div></div>'
              f'<div style="display:flex;justify-content:space-between;font-family:JBMono,monospace;font-size:28px;color:var(--gris);margin-top:12px"><span>RECHAZO</span><span>OVACIÓN</span></div></div>')
        js += f'rise("#{pid}-rec",{L(tr):.2f});tl.fromTo("#{pid}-bar",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:E.inn}},{L(tr) + 0.2:.2f});'
    h += "</div><div class='vig'></div>"
    js += f'tl.fromTo("#{pid}-inner",{{x:0}},{{x:-36,duration:{d:.2f},ease:"power1.inOut"}},{t:.2f});'
    return f'<div id="{pid}-inner" class="fill">{h}</div>', js


def r_cita(pid, sh, L):
    """Cita en Cormorant itálica sobre foto oscurecida; letterbox."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h, js = "", ""
    if p.get("img"):
        h += f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"])}" style="object-position:{p.get("pos", "50% 30%")}"></div><div class="shade-all"></div>'
        js += f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"out");'
    else:
        bg, j2 = world_bg(pid, L, sh)
        h += bg
        js += j2
    fs = p.get("fs", 96 if not V else 92)
    h += (f'<div class="fill txt" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{"0 200px" if not V else "0 180px 0 90px"}">'
          f'<div class="ital" style="color:var(--oro);font-size:240px;line-height:.5;height:100px">“</div>'
          f'<div id="{pid}-q" class="ital" style="font-size:{fs}px;line-height:1.15">{wspan(p["texto"])}</div>'
          f'<div id="{pid}-r" class="rule" style="width:420px;margin:52px 0 26px"></div>'
          f'<div id="{pid}-a" class="kick" style="letter-spacing:.32em">{esc(p["autor"])}</div></div>'
          '<div class="lb" style="top:0"></div><div class="lb" style="bottom:0"></div><div class="vig"></div>')
    js += (f'words("#{pid}-q .w",{L(p.get("tq", sh["t"] + 0.2)):.2f},{p.get("gap", 0.11)});'
           f'rule("#{pid}-r",{L(p.get("ta", sh["t"] + 1.0)):.2f});blurIn("#{pid}-a",{L(p.get("ta", sh["t"] + 1.0)) + 0.2:.2f});')
    return h, js


def r_dato(pid, sh, L):
    """Cifra grande en oro que cuenta + etiqueta. Opcional: foto de fondo muy oscura."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    if p.get("img"):
        h = f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"])}"></div><div class="shade-all"></div>'
        js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"in");'
    else:
        h, js = world_bg(pid, L, sh)
    pre, num, suf = p.get("pre", ""), p["num"], p.get("suf", "")
    fs = p.get("fs", 300 if not V else 250)
    t = L(p.get("tn", sh["t"] + 0.3))
    h += (f'<div class="fill txt" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{"0 60px" if not V else "0 180px 0 90px"}">'
          f'<div id="{pid}-k" class="kick">{esc(p.get("kick", ""))}</div>'
          f'<div id="{pid}-n" class="gold" style="font-weight:500;font-size:{fs}px;line-height:1;margin-top:20px;letter-spacing:.02em">'
          f'{esc(pre)}<span id="{pid}-c">{num}</span><span style="font-size:{int(fs * .4)}px">{esc(suf)}</span></div>'
          f'<div id="{pid}-l" class="light" style="font-size:{p.get("fsl", 46 if not V else 52)}px;letter-spacing:.28em;margin-top:28px;text-transform:uppercase">{esc(p.get("label", ""))}</div></div><div class="vig"></div>')
    js += (f'blurIn("#{pid}-k",{L(p.get("tk", sh["t"] + 0.25)):.2f});tl.fromTo("#{pid}-n",{{opacity:0,scale:.94}},{{opacity:1,scale:1,duration:0.5,ease:E.inn}},{t:.2f});'
           f'tl.fromTo("#{pid}-n",{{backgroundPosition:"100% 0"}},{{backgroundPosition:"0% 0",duration:1.2,ease:E.cam}},{t + 0.5:.2f});'
           f'blurIn("#{pid}-l",{L(p.get("tl", sh["t"] + 0.9)):.2f});')
    if p.get("cuenta", True) and str(num).isdigit():
        js += f'count("#{pid}-c",{num},{t:.2f},{p.get("dc", 1.0)});'
    return h, js


def r_procon(pid, sh, L):
    """A favor / en contra con foto B/N a la izquierda; cada punto aparece cuando la voz lo dice."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = (f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"])}" style="object-position:{p.get("pos", "30% 30%")}"></div>'
         f'<div class="fill" style="background:linear-gradient(90deg,rgba(7,7,10,0) 0%,rgba(7,7,10,.12) 46%,rgba(7,7,10,.2) 62%)"></div><div class="vig"></div>')
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"l");'
    x = 1000 if not V else 70
    top = 190 if not V else 980
    h += f'<div class="txt" style="position:absolute;left:{x}px;top:{top}px;right:110px">'
    for j, (titulo, color, items) in enumerate(p["bloques"]):
        if titulo is None:
            continue
        sig = "＋" if color == "oro" else "－"
        h += (f'<div id="{pid}-h{j}" class="kick" style="color:var(--{color});margin-top:{0 if j == 0 else 54}px">{sig} {esc(titulo)}</div>')
        js += f'blurIn("#{pid}-h{j}",{L(items[0][1]) - 0.25:.2f});'
        for k, (txt, tt) in enumerate(items):
            h += f'<div id="{pid}-i{j}{k}" style="font-size:{p.get("fs", 48)}px;font-weight:400;line-height:1.3;margin-top:16px">{esc(txt)}</div>'
            js += f'tl.fromTo("#{pid}-i{j}{k}",{{opacity:0,x:-24,filter:"blur(6px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.45,ease:E.inn}},{L(tt):.2f});'
    h += "</div>"
    return h, js


def r_leccion(pid, sh, L):
    p = sh["p"]
    bg, js = world_bg(pid, L, sh)
    h = bg + (f'<div class="fill txt" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 160px">'
              f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
              f'<div id="{pid}-q" class="ital" style="font-size:{p.get("fs", 92 if not V else 86)}px;line-height:1.15;margin-top:34px">{wspan(p["texto"])}</div></div><div class="vig"></div>')
    js += f'stamp("#{pid}-k",{L(sh["t"]) + 0.1:.2f});words("#{pid}-q .w",{L(p.get("tq", sh["t"] + 0.4)):.2f},0.1);'
    return h, js


def r_posters(pid, sh, L):
    """Pósters a color que entran en abanico con paralaje; cada uno con su año."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    bg, js = world_bg(pid, L, sh, rings=False)
    n = len(p["items"])
    pw = p.get("pw", 360 if n > 3 else 420)
    ph = int(pw * 1.48)
    gap = p.get("gap", 60)
    total = n * pw + (n - 1) * gap
    x0 = (W - total) / 2
    y = (H - ph) / 2 - 30
    h = bg + f'<div id="{pid}-row" class="fill">'
    for j, (img, label, tt) in enumerate(p["items"]):
        rot = (j - (n - 1) / 2) * 2.2
        h += (f'<div id="{pid}-p{j}" style="position:absolute;left:{x0 + j * (pw + gap):.0f}px;top:{y:.0f}px;width:{pw}px;height:{ph}px;'
              f'box-shadow:0 30px 60px rgba(0,0,0,.6);background:#111"><img class="media" src="{AS.img(img, bn=False)}"></div>'
              f'<div id="{pid}-y{j}" class="tag" style="position:absolute;left:{x0 + j * (pw + gap):.0f}px;width:{pw}px;top:{y + ph + 26:.0f}px;text-align:center;color:var(--oro)">{esc(label)}</div>')
        js += (f'tl.fromTo("#{pid}-p{j}",{{opacity:0,y:80,rotation:{rot * 3:.1f},filter:"blur(8px)"}},'
               f'{{opacity:1,y:0,rotation:{rot:.1f},filter:"blur(0px)",duration:0.8,ease:E.inn}},{L(tt):.2f});'
               f'blurIn("#{pid}-y{j}",{L(tt) + 0.35:.2f});')
    h += "</div><div class='vig'></div>"
    js += f'tl.fromTo("#{pid}-row",{{x:40,scale:1}},{{x:-40,scale:1.04,duration:{d:.2f},ease:"power1.inOut"}},{L(sh["t"]):.2f});'
    return h, js


def r_comentarios(pid, sh, L):
    """Internet dividido: tarjetas de comentarios a favor (oro) y en contra (rojo) que aparecen escalonadas."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = (f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"])}" style="object-position:50% 25%"></div>'
         f'<div class="shade-all"></div><div class="vig"></div>')
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"in");'
    for j, (txt, lado, tt, x, y) in enumerate(p["items"]):
        col = "var(--oro)" if lado == "+" else "var(--rojo)"
        h += (f'<div id="{pid}-c{j}" class="card txt" style="position:absolute;left:{x}px;top:{y}px;max-width:{p.get("mw", 720)}px;padding:26px 34px;border-left:4px solid {col}">'
              f'<div class="mono" style="font-size:24px;color:{col};letter-spacing:.2em">{"A FAVOR" if lado == "+" else "EN CONTRA"}</div>'
              f'<div style="font-size:{p.get("fs", 44)}px;margin-top:10px;line-height:1.25">{esc(txt)}</div></div>')
        js += f'tl.fromTo("#{pid}-c{j}",{{opacity:0,y:30,scale:.96}},{{opacity:1,y:0,scale:1,duration:0.5,ease:E.inn}},{L(tt):.2f});'
    if p.get("centro"):
        h += f'<div id="{pid}-cen" class="gold big" style="position:absolute;left:0;right:0;top:{H // 2 - 70}px;text-align:center;font-size:{p.get("fsc", 130)}px">{esc(p["centro"])}</div>'
        js += f'goldIn("#{pid}-cen",{L(p["tc"]):.2f});'
    return h, js


def r_seis(pid, sh, L):
    """Seis retratos B/N en fila que se encienden uno a uno, y un séptimo hueco con '?' (luego se vuelve Pattinson)."""
    p = sh["p"]
    n = 7
    pw, ph, gap = (210, 300, 26) if not V else (300, 420, 24)
    cols = 7 if not V else 3
    bg, js = world_bg(pid, L, sh, rings=False)
    h = bg
    imgs = p["imgs"]
    total = cols * pw + (cols - 1) * gap
    for j in range(n):
        if not V:
            x, y = (W - total) / 2 + j * (pw + gap), (H - ph) / 2
        else:
            r, c = divmod(j, 3)
            x, y = (W - total) / 2 + c * (pw + gap), 330 + r * (ph + gap)
            if j == 6:
                x = (W - pw) / 2
        if j < 6:
            h += (f'<div id="{pid}-f{j}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{pw}px;height:{ph}px;overflow:hidden;background:#111">'
                  f'<img class="media" src="{AS.img(imgs[j][0] if isinstance(imgs[j], tuple) else imgs[j])}" style="object-position:{imgs[j][1] if isinstance(imgs[j], tuple) else "50% 25%"}"></div>'
                  f'<div class="frame" style="left:{x:.0f}px;top:{y:.0f}px;width:{pw}px;height:{ph}px;opacity:.4"></div>')
            tt = L(p["t6"]) + j * 0.12
            js += f'tl.fromTo("#{pid}-f{j}",{{opacity:0,y:30,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.55,ease:E.inn}},{tt:.2f});'
        else:
            h += (f'<div id="{pid}-f6" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{pw}px;height:{ph}px;border:2px solid var(--oro);'
                  f'display:flex;align-items:center;justify-content:center"><span class="gold big" style="font-size:150px;background-position:0 0">?</span></div>')
            js += f'tl.fromTo("#{pid}-f6",{{opacity:0,scale:1.3}},{{opacity:1,scale:1,duration:0.6,ease:E.inn}},{L(p["t7"]):.2f});'
    lab_y = (H + ph) / 2 + 40 if not V else 330 + 3 * (ph + gap) + 30
    h += f'<div id="{pid}-lab" class="kick" style="position:absolute;left:0;right:0;top:{lab_y:.0f}px;text-align:center">{esc(p.get("label", "1962 — 2026"))}</div><div class="vig"></div>'
    js += f'blurIn("#{pid}-lab",{L(p["t6"]) + 0.8:.2f});'
    return h, js


def r_versus(pid, sh, L):
    """Pantalla dividida: dos fotos B/N con etiqueta; una línea dorada al centro."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    (ia, la, ta), (ib, lb, tb) = p["a"], p["b"]
    if not V:
        boxes = [(0, 0, W // 2, H), (W // 2, 0, W // 2, H)]
    else:
        boxes = [(0, 0, W, H // 2), (0, H // 2, W, H // 2)]
    h, js = "", ""
    for j, ((img, lab, tt), (x, y, w, hh)) in enumerate(zip([p["a"], p["b"]], boxes)):
        h += (f'<div id="{pid}-b{j}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hh}px;overflow:hidden">'
              f'<div id="{pid}-kb{j}" class="kb"><img class="media" src="{AS.img(img)}" style="object-position:50% 25%"></div>'
              f'<div class="shade-b"></div>'
              f'<div class="txt" style="position:absolute;left:0;right:0;bottom:{90 if not V else 60}px;text-align:center"><div id="{pid}-l{j}" class="big gold" style="display:inline-block;font-size:{p.get("fs", 84)}px">{esc(lab)}</div></div></div>')
        js += (f'tl.fromTo("#{pid}-b{j}",{{clipPath:"{"inset(0 100% 0 0)" if j == 0 else "inset(0 0 0 100%)"}"}},'
               f'{{clipPath:"inset(0 0% 0 0%)",duration:0.8,ease:E.inn}},{L(sh["t"]) + j * 0.15:.2f});'
               f'kb("#{pid}-kb{j}",{L(sh["t"]):.2f},{d + 0.6:.2f},"{"l" if j == 0 else "r"}");goldIn("#{pid}-l{j}",{L(tt):.2f});')
    h += (f'<div id="{pid}-mid" style="position:absolute;{"left:50%;top:0;bottom:0;width:2px;margin-left:-1px" if not V else "top:50%;left:0;right:0;height:2px;margin-top:-1px"};background:var(--oro)"></div>'
          f'<div class="vig"></div>')
    js += f'tl.fromTo("#{pid}-mid",{{opacity:0}},{{opacity:1,duration:0.5}},{L(sh["t"]) + 0.5:.2f});'
    if p.get("centro"):
        h += (f'<div id="{pid}-c" class="ital" style="position:absolute;left:0;right:0;top:{110 if not V else H // 2 - 70}px;text-align:center;font-size:{p.get("fsc", 72)}px;'
              f'text-shadow:0 4px 30px #000">{esc(p["centro"])}</div>')
        js += f'blurIn("#{pid}-c",{L(p["tc"]):.2f});'
    return h, js


def r_podio(pid, sh, L):
    """Tres medidas de éxito: cada tarjeta con foto, medida y ganador."""
    p = sh["p"]
    bg, js = world_bg(pid, L, sh, rings=False)
    n = len(p["items"])
    if not V:
        cw, chh, gap = 500, 700, 50
        x0, y0 = (W - (n * cw + (n - 1) * gap)) / 2, 200
    else:
        cw, chh, gap = 900, 420, 40
        x0, y0 = (W - cw) / 2, 380
    h = bg + f'<div id="{pid}-k" class="kick" style="position:absolute;left:0;right:0;top:{90 if not V else 220}px;text-align:center">{esc(p["kick"])}</div>'
    js += f'blurIn("#{pid}-k",{L(sh["t"]) + 0.2:.2f});'
    for j, (medida, ganador, detalle, img, tt) in enumerate(p["items"]):
        x, y = (x0 + j * (cw + gap), y0) if not V else (x0, y0 + j * (chh + gap))
        ih = int(chh * .55) if not V else chh
        iw = cw if not V else int(cw * .42)
        tx = 0 if not V else iw + 36
        ty = ih + 28 if not V else 50
        h += (f'<div id="{pid}-c{j}" class="card" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{cw}px;height:{chh}px;overflow:hidden">'
              f'<div style="position:absolute;left:0;top:0;width:{iw}px;height:{ih}px;overflow:hidden"><img class="media" src="{AS.img(img)}" style="object-position:50% 25%"></div>'
              f'<div style="position:absolute;left:{tx + 34}px;top:{ty}px;right:30px">'
              f'<div class="tag" style="color:var(--oro)">{esc(medida)}</div>'
              f'<div class="gold big" style="font-size:{72 if not V else 76}px;margin-top:14px;display:inline-block;background-position:0 0">{esc(ganador)}</div>'
              f'<div class="ital" style="font-size:{40 if not V else 44}px;margin-top:12px;color:var(--marfil)">{esc(detalle)}</div></div></div>')
        js += f'tl.fromTo("#{pid}-c{j}",{{opacity:0,y:50,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:E.inn}},{L(tt):.2f});'
    h += "<div class='vig'></div>"
    return h, js


def r_navegador(pid, sh, L):
    """Barra de navegador minimalista con una URL que se escribe (sitios de protesta reales de 2005)."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = (f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"])}" style="object-position:50% 30%"></div>'
         f'<div class="shade-all"></div><div class="vig"></div>')
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"in");'
    bw = 1300 if not V else 960
    y0 = H // 2 - 200 if not V else 760
    for j, (url, tt) in enumerate(p["urls"]):
        y = y0 + j * 150
        h += (f'<div id="{pid}-u{j}" class="card" style="position:absolute;left:{(W - bw) // 2}px;top:{y}px;width:{bw}px;height:110px;display:flex;align-items:center;'
              f'border-radius:56px;padding:0 44px;gap:26px"><span style="width:20px;height:20px;border-radius:50%;background:var(--rojo)"></span>'
              f'<span class="mono" style="font-size:{46 if not V else 40}px;color:var(--marfil);white-space:nowrap;overflow:hidden">'
              f'<span id="{pid}-t{j}" style="display:inline-block;clip-path:inset(0 100% 0 0)">{esc(url)}</span></span></div>')
        js += (f'rise("#{pid}-u{j}",{L(tt):.2f},0.45);'
               f'tl.fromTo("#{pid}-t{j}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.9,ease:"steps(22)"}},{L(tt) + 0.3:.2f});')
    if p.get("titulo"):
        h += f'<div id="{pid}-ti" class="kick" style="position:absolute;left:0;right:0;top:{y0 - 110}px;text-align:center">{esc(p["titulo"])}</div>'
        js += f'blurIn("#{pid}-ti",{L(sh["t"]) + 0.1:.2f});'
    return h, js


def r_escala(pid, sh, L):
    """Cierre: escala del 1 al 10 que se enciende, con la pregunta; foto de Pattinson a color al fondo."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    h = (f'<div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"], bn=False)}" style="object-position:{p.get("pos", "60% 30%")}"></div>'
         f'<div class="shade-all"></div><div class="vig"></div>')
    js = f'kb("#{pid}-kb",{L(sh["t"]):.2f},{d + 0.6:.2f},"in");'
    cy = H // 2 - 160 if not V else 640
    h += f'<div class="fill txt" style="display:flex;flex-direction:column;align-items:center;padding-top:{cy}px;text-align:center">'
    h += f'<div id="{pid}-q" class="ital" style="font-size:{p.get("fs", 84 if not V else 80)}px;line-height:1.1;padding:{"0 80px" if not V else "0 180px 0 90px"}">{wspan(p["pregunta"])}</div>'
    js += f'words("#{pid}-q .w",{L(p.get("tq", sh["t"] + 0.2)):.2f},0.09);'
    sw = 120 if not V else 70
    h += f'<div style="display:flex;gap:{18 if not V else 7}px;margin-top:64px;{"" if not V else "padding:0 100px 0 10px"}">'
    for k in range(1, 11):
        h += (f'<div id="{pid}-n{k}" class="mono" style="width:{sw}px;height:{sw}px;border:1.5px solid var(--oro);display:flex;align-items:center;'
              f'justify-content:center;font-size:{48 if not V else 40}px;color:var(--oro-claro)">{k}</div>')
        js += f'tl.fromTo("#{pid}-n{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:E.inn}},{L(p["tn"]) + k * 0.06:.2f});'
    h += "</div>"
    if p.get("cta"):
        h += f'<div id="{pid}-cta" class="kick" style="margin-top:60px">{esc(p["cta"])}</div>'
        js += f'blurIn("#{pid}-cta",{L(p["tcta"]):.2f});'
    h += "</div>"
    return h, js


def r_poster(pid, sh, L):
    """Póster enmarcado a la derecha (a color) + título a la izquierda, sobre el mundo de anillos."""
    p = sh["p"]
    d = sh["end"] - sh["t"]
    bg, js = world_bg(pid, L, sh, rings=False)
    pw, ph = (560, 830) if not V else (620, 920)
    x, y = (W - pw - 190, (H - ph) // 2) if not V else ((W - pw) // 2, 300)
    t = L(sh["t"])
    h = bg + (f'<div id="{pid}-p" style="position:absolute;left:{x}px;top:{y}px;width:{pw}px;height:{ph}px;overflow:hidden;'
              f'box-shadow:0 40px 90px rgba(0,0,0,.7);background:#111"><div id="{pid}-kb" class="kb"><img class="media" src="{AS.img(p["img"], bn=False)}"></div></div>'
              f'<div class="frame" id="{pid}-f" style="left:{x - 18}px;top:{y - 18}px;width:{pw + 36}px;height:{ph + 36}px"></div>')
    js += (f'tl.fromTo("#{pid}-p",{{opacity:0,y:70,rotation:3,filter:"blur(10px)"}},{{opacity:1,y:0,rotation:0,filter:"blur(0px)",duration:0.9,ease:E.inn}},{t + 0.05:.2f});'
           f'tl.fromTo("#{pid}-f",{{opacity:0,scale:1.06}},{{opacity:1,scale:1,duration:1.0,ease:E.inn}},{t + 0.25:.2f});'
           f'kb("#{pid}-kb",{t:.2f},{d + 0.6:.2f},"in");'
           f'tl.fromTo("#{pid}-p",{{x:0}},{{x:-24,duration:{d:.2f},ease:"power1.inOut"}},{t:.2f});')
    tx, ty = (150, H // 2 - 150) if not V else (70, y + ph + 90)
    h += f'<div class="txt" style="position:absolute;left:{tx}px;top:{ty}px;width:{(x - tx - 80) if not V else W - 140}px">'
    if p.get("kick"):
        h += f'<div id="{pid}-k" class="kick">{esc(p["kick"])}</div>'
        js += f'blurIn("#{pid}-k",{L(p.get("tk", sh["t"] + 0.3)):.2f});'
    if p.get("l2"):
        h += f'<div id="{pid}-l2" class="gold big" style="font-size:{p.get("fs2", 120)}px;margin-top:22px;display:inline-block;line-height:1.05">{esc(p["l2"])}</div>'
        js += f'goldIn("#{pid}-l2",{L(p.get("t2", sh["t"] + 0.5)):.2f});'
    if p.get("sub"):
        h += f'<div id="{pid}-s" class="ital" style="font-size:56px;margin-top:22px">{esc(p["sub"])}</div>'
        js += f'blurIn("#{pid}-s",{L(p.get("ts", sh["t"] + 1.0)):.2f});'
    h += "</div><div class='vig'></div>"
    return h, js


TRANS = {"corte": 0.0, "fundido": 0.45, "iris": 0.7, "barrido": 0.6, "latigo": 0.42, "zoom": 0.6, "negro": 0.5}


def trans_js(pid, prev, kind, t):
    """Entrada del plano pid a tiempo local t (y salida del anterior)."""
    d = TRANS[kind]
    s = f'#{pid}'
    js = f'tl.set("{s}",{{opacity:1}},{t:.3f});'
    if kind == "fundido":
        js = f'tl.fromTo("{s}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power1.inOut"}},{t:.3f});'
    elif kind == "iris":
        js += f'tl.fromTo("{s}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:{d},ease:"power3.inOut"}},{t:.3f});'
    elif kind == "barrido":
        js += f'tl.fromTo("{s}",{{clipPath:"inset(0 0 0 100%)"}},{{clipPath:"inset(0 0 0 0%)",duration:{d},ease:"power3.inOut"}},{t:.3f});'
    elif kind == "latigo":
        js += f'tl.fromTo("{s}",{{x:{W * 0.6:.0f},filter:"blur(18px)"}},{{x:0,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{t:.3f});'
        if prev:
            js += f'tl.to("#{prev}",{{x:{-W * 0.6:.0f},filter:"blur(18px)",duration:{d * 0.7:.2f},ease:"power3.in"}},{t - 0.05:.3f});'
    elif kind == "zoom":
        js += f'tl.fromTo("{s}",{{opacity:0,scale:1.18,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d},ease:"expo.out"}},{t:.3f});'
        if prev:
            js += f'tl.to("#{prev}",{{scale:0.92,duration:{d},ease:"power3.in"}},{t:.3f});'
    elif kind == "negro":
        js = f'tl.fromTo("{s}",{{opacity:0}},{{opacity:1,duration:{d},ease:"power1.out"}},{t + 0.15:.3f});'
        if prev:
            js += f'tl.to("#{prev}",{{opacity:0,duration:0.2,ease:"power1.in"}},{t - 0.05:.3f});'
    return js


SFX_ENTRADA = {"iris": ("whoosh", -14), "zoom": ("whoosh", -16), "barrido": ("whoosh", -16), "latigo": ("whoosh-rapido", -12)}


def sfx_de(sh, primero):
    p, ev = sh["p"], []
    if not primero and sh["entrada"] in SFX_ENTRADA and sh["tipo"] != "clip":
        ev.append((sh["t"], *SFX_ENTRADA[sh["entrada"]]))
    if p.get("tsello"):
        ev.append((p["tsello"], "sello", -8))
    if sh["tipo"] == "dato" and p.get("tn"):
        ev.append((p["tn"], "golpe", -10))
    if sh["tipo"] == "titulo" and p.get("t2"):
        ev.append((p["t2"], "golpe", -13))
    if sh["tipo"] == "navegador":
        ev += [(t + 0.3, "teclas", -16) for _, t in p["urls"]]
    if sh["tipo"] == "ficha":
        ev += [(t, "tick", -18) for _, _, t in p["datos"]]
    if sh["tipo"] == "seis":
        ev.append((p["t7"], "golpe", -12))
    return ev



# ------------------------------------------------------------------ tratamiento de assets e index
BN_DEFAULT = True


def IMG_VF(bn):
    return "scale='min(2400,iw)':-2" + (",format=gray,eq=contrast=1.12:brightness=-0.02" if bn else "")


def VID_VF(bn):
    return "hue=s=0,eq=contrast=1.12:brightness=-0.02" if bn else None


INDEX_BG = "#07070a"
GRANO_CSS = 'position:absolute;inset:0;z-index:900;pointer-events:none;opacity:.07;background-image:url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'240\' height=\'240\'><filter id=\'n\'><feTurbulence baseFrequency=\'.85\' numOctaves=\'2\' seed=\'7\'/></filter><rect width=\'100%\' height=\'100%\' filter=\'url(%23n)\'/></svg>")'

# ------------------------------------------------------------------ mezcla (ganancia por efecto y adelanto del pico)
SFX_GAIN = {"whoosh": -21, "whoosh-rapido": -18, "golpe": -14, "sello": -15, "tick": -24, "teclas": -21}
PICO_ANTES = {"whoosh": -0.18, "whoosh-rapido": -0.12}
