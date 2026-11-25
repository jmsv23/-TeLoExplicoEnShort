import json, math
from lib import *

CLIP = json.loads((SERIE / "13-wanda-poscreditos-visionquest" / "clip.json").read_text())
CL_S, CL_D = CLIP["start"], 10.07

ep = Episode(13, "wanda-poscreditos-visionquest", "La Bruja Escarlata está de vuelta... de la mano de Doom", 104, dias=34, cont_in="2.1", cont_pulse="11.1")


def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob:
        ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out:
        ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)


def png(file, w):
    return f'<img src="{IMG}{file}" style="width:{w}px;display:block" />'


def hexburst(w=420, c1="#E8212B", c2="#FFD400"):
    """energía caótica de la Bruja Escarlata: estallido rojo con rayos"""
    rays = ""
    for k in range(16):
        a = k * math.pi / 8
        r0, r1 = 70, 175 if k % 2 == 0 else 130
        x0, y0, x1, y1 = 200 + r0 * math.cos(a), 200 + r0 * math.sin(a), 200 + r1 * math.cos(a + .12), 200 + r1 * math.sin(a + .12)
        rays += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{c1}" stroke-width="16" stroke-linecap="round"/>'
    inner = (rays + f'<circle cx="200" cy="200" r="78" fill="{c1}" {S(9)}/><circle cx="200" cy="200" r="46" fill="{c2}" {S(8)}/>'
             f'<path d="M165 200 C180 160 225 170 235 200 C225 240 180 238 165 200 Z" fill="#FFF3D6" {S(6)}/>')
    return svgbox("0 0 400 400", inner, w, w)


def darkhold(w=380):
    inner = (f'<path d="M50 40 L330 20 L350 300 L70 330 Z" fill="#2A0B3A" {S(10)}/>'
             f'<path d="M70 60 L320 42 L336 290 L88 312 Z" fill="#4B1580" {S(7)}/>'
             f'<circle cx="200" cy="175" r="62" fill="none" stroke="#FFD400" stroke-width="10"/>'
             f'<path d="M200 125 L214 168 L260 168 L222 194 L236 238 L200 212 L164 238 L178 194 L140 168 L186 168 Z" fill="#E8212B" {S(6)}/>')
    return svgbox("0 0 400 360", inner, w, int(w * 360 / 400))


def mountain(w=620):
    inner = (f'<path d="M20 420 L150 200 L205 250 L300 40 L350 120 L420 60 L520 250 L600 420 Z" fill="#6B7280" {S(10)}/>'
             f'<path d="M300 40 L255 175 L300 240 L270 330" fill="none" stroke="#E8212B" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M205 250 L240 330 M420 60 L400 170 L450 230" fill="none" {S(7)}/>'
             f'<rect x="268" y="10" width="64" height="40" fill="#0B0B14"/><path d="M268 10 V-20 M300 10 V-34 M332 10 V-20" {S(14)}/>')
    return svgbox("0 -40 620 480", inner, w, int(w * 480 / 620))


# ---------------------------------------------------------------- 1 portada
s = ep.scene("Portada", "S1", bg="rojo", enter="cut", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 0.0, "(primer frame)", "Portada: Bruja Escarlata vuelve")
s.beat(2, 1.4, "Bruja **Escarlata**", "Burst rojo")
s.raw('<div class="panel" id="v13-e1-cv" style="left:90px;top:330px;width:900px;height:1090px;background:#0E5C32;transform:rotate(-1deg)">'
      '<div class="ttl ttl--amarillo ttl--sm" style="position:absolute;left:0;right:0;top:34px;text-align:center;--rot:-3deg;line-height:1">CAMINO A<br>DOOMSDAY</div>'
      '<div style="position:absolute;left:36px;top:280px;padding:6px 18px;background:#FFF3D6;border:6px solid #0B0B14;font:400 64px Anton;color:#0B0B14;transform:rotate(-4deg);z-index:3">ESPECIAL</div>'
      + Scene.cover_img("a-visionquest.jpg", 520, 520, "center", 450, 640) +
      '<div style="position:absolute;right:30px;top:250px;width:170px;height:170px;border-radius:50%;background:#E8212B;border:8px solid #0B0B14;display:flex;align-items:center;justify-content:center;font:400 40px/1 Anton;color:#FFF3D6;transform:rotate(8deg);text-align:center;z-index:3">SPOILERS</div></div>',
      'COM.panelSlam(tl, q("#v13-e1-cv"), 0.0, { from: "T", rot: 3 });')
s.cinta("cinta", "¡ELLA VUELVE!", "amarillo", top=1230, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("tm", "¡ATENCIÓN!", "ono", "amarillo", y=900, at="1.1", size=210, rot=-7, hold=1.0, misreg=True)
s.zoom("1.2", 1.12)

# ---------------------------------------------------------------- 2 de la mano de Doom
s = ep.scene("De la mano de Doom", "S1", bg="doom-osc", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 4.0, "**Pero** ojo", "Slab verde")
s.beat(2, 5.4, "de la **mano**", "Energía roja + mano")
s.beat(3, 6.5, "mano **de** Doom", "Máscara de Doom")
s.slab("sl", "rojo", "2.1", ("2.1", .5))
s.text("po", "¡PERO OJO!", "ono", "amarillo", y=560, at="2.1", size=190, rot=-6, hold=1.0, misreg=True)
s.panel("sw", pho("a-scarlet.jpg", "50% 10%", "BRUJA ESCARLATA", 40), 40, 480, 480, 640, "rojo", rot=-3, at="2.2", frm="L")
s.text("mn", "DE LA MANO DE", "ttl", "papel", y=1200, at="2.2", size=84, rot=-3, how="stamp")
s.panel("dp", pho("doom-mask.png", "50% 30%", "DOOM", 44), 560, 480, 480, 640, "doom", rot=3, at="2.3", frm="R")
s.text("dd", "DOOM", "ono", "amarillo", y=1380, at="2.3", size=240, rot=-6, hold=1.5, misreg=True, zoom=True)
s.speed("sp", "2.3", n=34, seed=5)

# ---------------------------------------------------------------- 3 VisionQuest
s = ep.scene("VisionQuest", "S2", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 8.0, "Está en la **escena**", "Cinta POSCRÉDITOS")
s.beat(2, 10.0, "de **VisionQuest**", "Póster VisionQuest")
s.cinta("pc", "ESCENA POSCRÉDITOS", "amarillo", top=450, rot=-5, at="3.1", words=["3.1", ("3.1", .6)])
s.img("vq", "a-visionquest.jpg", 540, 920, 760, 760, "3.2", how="slam", frm="B", bob="end", pos="center", rot=-2)
s.cinta("sp", "FINAL DE TEMPORADA", "rojo", top=1370, rot=-4, at="3.2")

# ---------------------------------------------------------------- 4 Wundagore
s = ep.scene("Wundagore", "S2", bg="multi-osc", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 11.0, "**Recuerda**", "Cinta RECUERDA")
s.beat(2, 12.2, "se **enterró**", "Montaña")
s.beat(3, 13.2, "Monte **Wundagore**", "Nombre del monte")
s.beat(4, 14.4, "el **Darkhold**", "Libro maldito")
s.cinta("rc", "RECUERDA", "amarillo", top=450, rot=-5, at="4.1", out="4.2")
V(s, "mt", mountain(820), 540, 740, "4.2", how="slam", frm="B")
s.text("wg", "MONTE WUNDAGORE", "ttl", "amarillo", y=1140, at="4.3", size=96, rot=-3, how="stamp", misreg=True)
V(s, "dh", darkhold(300), 300, 1330, "4.4", how="slam", frm="B", bob="end", rot=-6)
s.text("dk", "DARKHOLD", "ono", "rojo", x=730, y=1330, at="4.4", size=120, rot=-8, hold=1.2)

# ---------------------------------------------------------------- 5 muerta
s = ep.scene("Dada por muerta", "S2", bg="ceniza", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 15.2, "**Todos** la dimos", "Lápida")
s.beat(2, 16.2, "por **muerta**", "Sello MUERTA")
s.beat(3, 17.2, "Hasta **ahora**", "Tachado")
s.text("td", "TODOS LA DIMOS", "ttl", "papel", y=560, at="5.1", size=100, rot=-3, how="stamp")
s.panel("wm", pho("a-wanda-max.jpg", "72% 30%"), 190, 680, 700, 520, "ceniza", rot=-2, at="5.1", frm="B")
s.text("mu", "MUERTA", "ttl", "rojo", y=940, at="5.2", size=270, rot=-5, how="stamp", misreg=True, zoom=True)
s.obj("fb", "forbidden", 540, 940, 640, 640, ("5.3", .1), how="stamp")
s.text("ha", "¡HASTA AHORA!", "ono", "amarillo", y=1380, at="5.3", size=170, rot=-6, hold=1.2, misreg=True)
s.speed("sp", "5.3", n=36, seed=7)

# ---------------------------------------------------------------- 6 el clip
s = ep.scene("Poscréditos", "S3", bg="tinta", enter="cut", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 17.7, "**Mira**", "¡MIRA! + clip")
s.slab("sl", "rojo", "6.1", ("6.1", .35))
s.text("mi", "¡MIRA!", "ono", "amarillo", y=900, at="6.1", size=330, rot=-6, hold=0.8, misreg=True, zoom=True, out=("6.1", .9))
s.cinta("pc", "POSCRÉDITOS · VISIONQUEST", "amarillo", top=420, rot=-4, at=("6.1", .9))
s.raw('<div class="panel" id="v13-e6-vp" style="left:20px;top:560px;width:1040px;height:730px;background:#0B0B14;transform:rotate(0deg);overflow:hidden">'
      '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><span class="ttl ttl--amarillo" style="font-size:90px">POSCRÉDITOS</span></div>'
      f'<video id="v13-clip" class="clip" src="assets/video/camino-a-doomsday/13-poscreditos.mp4" playsinline data-has-audio="true" data-start="{CL_S}" data-duration="{CL_D}" data-track-index="5" data-volume="1" '
      'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:58% 50%"></video></div>',
      'COM.panelSlam(tl, q("#v13-e6-vp"), ' + s.t(("6.1", .9)) + ', { from: "B", rot: 1 });\n'
      f'COM.popOut(tl, q("#v13-e6-vp"), {CL_S + CL_D + 0.1});')
s.cap("cp", "TAL CUAL SE VIO EN PANTALLA", ("6.1", 1.4), left=50, top=1340, width=620)
s.code(f'COM.flashBlanco(tl, stage, {CL_S + CL_D + 0.1});')

# ---------------------------------------------------------------- 7 Despierta
s = ep.scene("Despierta", "S4", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 28.0, "**Despierta**", "Frame de Wanda")
s.beat(2, 30.0, "poder será **mío**", "Tu poder será mío")
s.panel("wf", pho("a-wanda.jpg", "64% 40%", None), 40, 440, 1000, 900, "doom", rot=-1, at="7.1", frm="T")
s.text("de", "«DESPIERTA»", "ono", "amarillo", y=1120, at="7.1", size=170, rot=-6, hold=1.8, misreg=True, zoom=True)
s.cinta("sc", "DOOM LE HABLA A WANDA", "doom", top=1450, rot=-4, at="7.1")
s.slab("sl", "doom", "7.2", ("7.2", .5))
s.text("pm", "TU PODER<br>SERÁ MÍO", "ttl", "amarillo", y=830, at="7.2", size=190, rot=-4, how="stamp", misreg=True, zoom=True)
s.speed("sp", "7.2", n=40, seed=3)

# ---------------------------------------------------------------- 8 rescate vs reclutamiento
s = ep.scene("Reclutamiento", "S4", bg="tinta", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 32.5, "no suena a **rescate**", "RESCATE tachado")
s.beat(2, 34.5, "suena a **reclutamiento**", "RECLUTAMIENTO")
s.text("r1", "¿RESCATE?", "ttl", "papel", y=620, at="8.1", size=150, rot=-3, how="stamp")
s.obj("fb", "forbidden", 540, 620, 560, 560, ("8.1", .3), how="stamp")
s.slab("sl", "doom", "8.2", ("8.2", .4))
s.text("r2", "RECLUTAMIENTO", "ttl", "amarillo", y=1000, at="8.2", size=125, rot=-4, how="stamp", misreg=True, zoom=True)
V(s, "dm", png("doom-mask.png", 400), 540, 1330, "8.2", how="slam", frm="B", bob="end")

# ---------------------------------------------------------------- 9 quién la revivió
s = ep.scene("¿Quién la revivió?", "S4", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 37.0, "**Nadie** sabe", "Cinta NADIE SABE")
s.beat(2, 38.4, "si Doom la **revivió**", "Doom")
s.beat(3, 40.0, "ella sobrevivió **sola**", "Energía roja")
s.cinta("ns", "NADIE SABE", "amarillo", top=460, rot=-5, at="9.1")
s.text("q1", "¿DOOM?", "ono", "amarillo", x=300, y=820, at="9.2", size=150, rot=-6, hold=1.8, misreg=True)
s.panel("dm", pho("doom-mask.png", "50% 30%"), 40, 880, 440, 560, "doom", rot=-3, at="9.2", frm="L")
s.text("q2", "¿SOLA?", "ono", "rojo", x=790, y=820, at="9.3", size=150, rot=6, hold=1.5, misreg=True)
s.panel("sc2", pho("a-scarlet.jpg", "50% 10%"), 600, 880, 440, 560, "rojo", rot=3, at="9.3", frm="R")

# ---------------------------------------------------------------- 10 Olsen
s = ep.scene("Olsen sin confirmar", "S4", bg="papel", enter="pageflip", color="papel")
s.beat(1, 42.0, "**Marvel** no ha confirmado", "Cinta SIN CONFIRMAR")
s.beat(2, 43.8, "Elizabeth **Olsen**", "Nombre")
s.beat(3, 45.5, "Pero **ahora** no hay duda", "Sin duda")
s.cinta("sn", "ANTES: SIN CONFIRMAR", "rojo", top=470, rot=-5, at="10.1")
s.panel("ol", pho("a-olsen-crop.jpg", "50% 25%", "ELIZABETH OLSEN", 40), 50, 560, 460, 600, "papel", rot=-3, at="10.2", frm="L")
s.panel("sw3", pho("a-scarlet.jpg", "50% 10%", "WANDA", 44), 570, 560, 460, 600, "rojo", rot=3, at="10.2", frm="R")
s.text("ap", "¡AHORA NO<br>HAY DUDA!", "ono", "heroe", y=1330, at="10.3", size=130, rot=-5, hold=1.8, misreg=True, zoom=True)

# ---------------------------------------------------------------- 11 estreno
s = ep.scene("Estreno", "S5", bg="tinta", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 46.5, "Doomsday **llega**", "Logo")
s.beat(2, 47.7, "el **dieciocho**", "18 DIC")
s.panel("lg", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:760px;height:300px;object-fit:contain" /></div>', 90, 460, 900, 340, "papel", rot=-2, at="11.1", frm="T")
s.text("fe", "18 DIC", "ttl", "amarillo", y=1050, at="11.2", size=260, rot=-4, how="stamp", misreg=True)
s.text("an", "2026", "ttl", "papel", y=1290, at="11.2", size=170, rot=3, how="stamp")
s.zoom("11.2", 1.1)

# ---------------------------------------------------------------- 12 pregunta
s = ep.scene("Pregunta", "S5", bg="doom-osc", enter="cover", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 49.0, "Y ahora **dime**", "¿?")
s.beat(2, 50.0, "**aliada** de Doom", "ALIADA")
s.beat(3, 51.2, "o su **prisionera**", "PRISIONERA")
s.cinta("di", "TÚ QUÉ CREES", "amarillo", top=450, rot=-5, at="12.1")
s.text("al", "¿ALIADA?", "ono", "heroe", y=640, at="12.2", size=190, rot=-5, hold=1.3, misreg=True, out="12.3")
s.panel("cw", pho("a-wanda-max.jpg", "72% 30%"), 140, 760, 800, 560, "doom", rot=-2, at="12.2", frm="B")
s.draw("ch1", "M120 800 C300 900 480 760 960 1260", "tinta", "12.3", w=46, dur=0.5)
s.draw("ch2", "M120 800 C300 900 480 760 960 1260", "ceniza", "12.3", w=26, dur=0.5)
s.draw("ch3", "M960 800 C780 900 600 760 120 1260", "tinta", ("12.3", .1), w=46, dur=0.5)
s.draw("ch4", "M960 800 C780 900 600 760 120 1260", "ceniza", ("12.3", .1), w=26, dur=0.5)
s.text("pr", "¿PRISIONERA?", "ono", "rojo", y=1420, at="12.3", size=150, rot=-4, hold=2.5, misreg=True, zoom=True)
