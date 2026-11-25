from lib import *

ep = Episode(12, "doom-no-es-variante-de-tony", "Feige: Doom NO es una variante de Tony Stark", 144, dias=34, cont_in="2.1", cont_pulse="12.2")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def png(file, w): return f'<img src="{IMG}{file}" style="width:{w}px;display:block" />'
def star(w=300):
    pts = " ".join(f"{50+(46 if k%2==0 else 20)*__import__('math').sin(k*3.14159/6):.1f},{50-(46 if k%2==0 else 20)*__import__('math').cos(k*3.14159/6):.1f}" for k in range(12))
    return svgbox("0 0 100 100", f'<polygon points="{pts}" fill="#E8212B" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>', w, w)

# 1 · portada
s = ep.scene("Portada", "S1", bg="doom-osc", enter="cut", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 12: Feige")
s.beat(2, 0.4, "Kevin **Faigui**", "¡FEIGE!")
s.beat(3, 1.7, "acaba de **matar**", "Teoría tachada")
s.cover("cover", 12, "#0E5C32", Scene.cover_img("a-feige.jpg", 400, 500, "top", 450, 640), at="1.1", frm="T", tot=13)
s.cinta("cinta", "FEIGE HABLÓ", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("tm", "¡FEIGE!", "ono", "amarillo", y=900, at="1.2", size=250, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "LA TEORÍA MÁS GRANDE", "1.3", width=560)
s.zoom("1.2", 1.12)
s.pulse("cover", ("1.3", 1.1), 1.06)

# 2 · la teoría
s = ep.scene("La teoría", "S1", bg="ciencia", enter="halftone", color="ciencia")
s.beat(1, 4.1, "La **pregunta**", "¿?")
s.beat(2, 6.4, "Robert **Downey** Junior", "Foto RDJ")
s.beat(3, 8.0, "un **Tony** Stark", "Iron Man")
s.beat(4, 8.7, "**malvado**", "¿MALVADO?")
s.cinta("q", "LA GRAN PREGUNTA", "rojo", top=450, rot=-5, at="2.1", words=["2.1", ("2.1", .3)])
s.panel("rd", pho("rdj-recorte.jpg", "50% 15%", "DOOM", 56), 90, 640, 440, 620, "doom", rot=-3, at="2.2", frm="L")
V(s, "ir", png("ironman-cut.png", 300), 790, 960, "2.3", how="slam", frm="R", bob="end")
s.text("mv", "¿MALVADO?", "ono", "rojo", y=1380, at="2.4", size=190, rot=-7, hold=1.2, misreg=True, zoom=True)

# 3 · la respuesta
s = ep.scene("La respuesta", "S2", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 10.2, "Su **respuesta**", "SU RESPUESTA")
s.beat(2, 11.0, "**no**", "NO gigante")
s.text("sr", "SU RESPUESTA", "ttl", "amarillo", y=700, at="3.1", size=130, rot=-4, how="stamp", out="3.2")
s.slab("sl", "rojo", "3.2", ("3.2", .8))
s.text("no", "¡NO!", "ono", "papel", y=900, at="3.2", size=420, rot=-6, hold=1.6, misreg=True, zoom=True)
s.speed("sp", "3.2", n=40, seed=4)

# 4 · Empire
s = ep.scene("Empire", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 13.0, "la revista **Empire**", "Portada Empire")
s.beat(2, 14.6, "es **no**", "Globo NO")
s.img("em", "a-empire.jpg", 540, 880, 560, 726, "4.1", how="slam", frm="B", bob="end", pos="top", rot=-2)
s.cinta("ci", "REVISTA EMPIRE", "doom", top=1330, rot=-5, at="4.1")
s.globo("gl", "LA RESPUESTA<br>ES NO", 600, 360, 440, 220, "4.2", kind="globo", size=60, rot=3)

# 5 · Victor von Doom
s = ep.scene("Victor von Doom", "S2", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 16.5, "Es **Victor**", "Doom aparece")
s.beat(2, 17.3, "von **Doom**", "VICTOR VON DOOM")
s.flash("5.1")
s.img("dm", "drdoom-recorte.png", 540, 800, 700, 700, "5.1", how="slam", frm="T", bob="end", pos="center")
s.text("vn", "VICTOR VON DOOM", "ttl", "amarillo", y=1370, at="5.2", size=110, rot=-4, how="stamp", misreg=True)
s.zoom("5.1", 1.14)

# 6 · el ejemplo
s = ep.scene("El ejemplo", "S3", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 19.3, "puso un **ejemplo**", "Cinta EJEMPLO")
s.beat(2, 20.4, "¿**Steve** Rogers", "Steve Rogers")
s.beat(3, 21.6, "una **variante**", "Nube ¿VARIANTE?")
s.beat(4, 22.4, "de **Johnny** Storm", "Johnny Storm")
s.cinta("ex", "EL EJEMPLO DE FEIGE", "amarillo", top=450, rot=-5, at="6.1", out="6.2")
s.panel("st", pho("a-cap.jpg", "50% 15%", "STEVE ROGERS", 52), 60, 520, 460, 640, "heroe", rot=-3, at="6.2", frm="L")
s.globo("nu", "¿VARIANTE?", 300, 1210, 620, 340, "6.3", kind="nube", size=56, rot=3)
s.panel("jo", pho("a-johnny-evans.jpg", "50% 20%", "JOHNNY STORM", 52), 560, 520, 460, 640, "rojo", rot=3, at="6.4", frm="R")

# 7 · Chris Evans
s = ep.scene("Chris Evans", "S3", bg="papel", enter="pageflip", color="papel")
s.beat(1, 24.2, "Chris **Evans** interpretó", "Cinta CHRIS EVANS")
s.beat(2, 25.3, "a los **dos**", "Escudo + llama")
s.beat(3, 26.2, "**nadie** los confunde", "Tachado")
s.cinta("ev", "CHRIS EVANS", "tinta", top=470, rot=-5, at="7.1", words=["7.1", ("7.1", .3)])
V(s, "sh", shield(330), 300, 900, "7.2", how="slam", frm="L", bob="end")
V(s, "fl", flame(300), 790, 900, ("7.2", .2), how="slam", frm="R", bob="end")
s.text("y", "+", "ono", "amarillo", x=540, y=900, at="7.2", size=200, rot=-6, hold=1.0)
s.obj("fb", "forbidden", 540, 1190, 480, 480, ("7.3", .1), how="stamp")
s.text("nd", "¡NADIE!", "ono", "amarillo", y=1480, at="7.3", size=170, rot=-6, hold=1.2, misreg=True)

# 8 · 1 · 2 · 0
s = ep.scene("Cuentas", "S3", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 28.2, "Un **actor**", "1 ACTOR")
s.beat(2, 29.1, "dos **personajes**", "2 PERSONAJES")
s.beat(3, 30.3, "cero **parentesco**", "0 PARENTESCO")
s.text("a1", "1 ACTOR", "ttl", "amarillo", y=560, at="8.1", size=180, rot=-3, how="stamp", misreg=True)
s.text("a2", "2 PERSONAJES", "ttl", "papel", y=860, at="8.2", size=150, rot=3, how="stamp", misreg=True)
s.text("a3", "0 PARENTESCO", "ttl", "rojo", y=1160, at="8.3", size=150, rot=-3, how="stamp", misreg=True, zoom=True)
s.speed("sp", "8.3", n=36, seed=8)

# 9 · cómics
s = ep.scene("1961", "S3", bg="doom-osc", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 33.0, "**Además** Doom apareció", "Cinta EN LOS CÓMICS")
s.beat(2, 34.0, "mil **novecientos** sesenta", "1961 + Fantastic Four 5")
s.beat(3, 36.3, "**antes** que", "Tales of Suspense")
s.beat(4, 36.9, "**Iron** Man", "1963")
s.cinta("co", "EN LOS CÓMICS", "amarillo", top=450, rot=-5, at="9.1", out="9.2")
s.panel("ff", '<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px"><span class="ttl ttl--amarillo" style="font-size:78px;text-align:center;line-height:.95">FANTASTIC<br>FOUR</span><img src="' + IMG + 'doom-mask.png" style="width:190px;border:8px solid #0B0B14" /><span class="ttl ttl--papel" style="font-size:64px">N.º 5</span></div>', 60, 500, 460, 640, "doom", rot=-3, at=("9.1", 1.7), frm="L")
s.text("y61", "1961", "ttl", "amarillo", x=290, y=1280, at="9.2", size=190, rot=-4, how="stamp", misreg=True)
s.img("ts", "a-tos39.jpg", 790, 800, 440, 560, "9.3", how="slam", frm="R", pos="50% 100%", rot=3)
s.text("y63", "1963", "ttl", "rojo", x=790, y=1280, at="9.4", size=190, rot=4, how="stamp", misreg=True, zoom=True)

# 10 · giro
s = ep.scene("Ojo", "S4", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 38.0, "**Ojo**", "¡OJO!")
s.beat(2, 40.3, "no **aparecerá**", "Máscara Iron Man + sin confirmar")
s.beat(3, 42.0, "no es **Tony**", "Doom ≠ Tony")
s.slab("sl", "rojo", "10.1", ("10.1", .5))
s.text("oj", "¡OJO!", "ono", "amarillo", y=820, at="10.1", size=380, rot=-7, hold=1.3, misreg=True, zoom=True)
V(s, "im", png("iron-mask.png", 360), 300, 780, ("10.1", 0.9), how="slam", frm="L", bob="end")
s.cap("nc", "FEIGE NO LO DIJO", "10.2", left=470, top=1150, width=540)
s.cinta("tn", "DOOM ≠ TONY", "doom", top=1350, rot=-5, at="10.3")
V(s, "dm", png("doom-mask.png", 300), 790, 780, "10.3", how="slam", frm="R", bob="end")

# 11 · otro personaje, mismo actor
s = ep.scene("Otro personaje", "S4", bg="doom-osc", enter="pageflip", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 43.4, "es **otro** personaje", "Máscara de Doom")
s.beat(2, 44.8, "el mismo **actor**", "Foto RDJ")
V(s, "dm", png("doom-mask.png", 420), 540, 800, "11.1", how="slam", frm="T", bob="end")
s.cinta("op", "OTRO PERSONAJE", "amarillo", top=420, rot=-5, at="11.1")
s.panel("rd", pho("rdj-recorte.jpg", "50% 42%", "EL MISMO ACTOR", 48), 270, 1070, 540, 380, "heroe", rot=2, at="11.2", frm="B", prot=2)
s.pulse("dm", "11.2", 1.1)

# 12 · fecha
s = ep.scene("Estreno", "S4", bg="tinta", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 47.0, "**Avengers** Doomsday llega", "Logo")
s.beat(2, 48.0, "el **dieciocho** de diciembre", "18 DIC")
s.panel("lg", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:760px;height:300px;object-fit:contain" /></div>', 90, 460, 900, 340, "papel", rot=-2, at="12.1", frm="T")
s.text("fe", "18 DIC", "ttl", "amarillo", y=1050, at="12.2", size=260, rot=-4, how="stamp", misreg=True)
s.text("an", "2026", "ttl", "papel", y=1290, at=("12.2", .3), size=170, rot=3, how="stamp")
s.zoom("12.2", 1.1)

# 13 · cierre + suscripción
s = ep.scene("Cierre", "S5", bg="doom-osc", enter="cover", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 50.0, "Esta **revelación**", "Teorías tachadas")
s.beat(2, 51.8, "teorías de los **fans**", "Fans")
s.beat(3, 53.6, "**Suscríbete** al canal", "SUSCRÍBETE")
s.beat(4, 55.2, "para más **curiosidades**", "Cinta")
s.cinta("rv", "REVELACIÓN", "amarillo", top=460, rot=-5, at="13.1", out="13.2")
s.text("tt", "TEORÍAS<br>DE LOS FANS", "ttl", "papel", y=800, at="13.1", size=120, rot=-3, how="stamp")
s.draw("tx", "M 120 960 L 960 640", "rojo", ("13.1", 1.2), w=26, dur=0.3)
s.out("tt", "13.3")
s.code(f'tl.to(q("#{s.id("tx")}"), {{ opacity: 0, duration: 0.05 }}, {s.t("13.3")} - 0.05);')
s.slab("sl", "rojo", "13.3", ("13.3", .4))
s.text("su", "¡SUSCRÍBETE!", "ono", "amarillo", y=900, at="13.3", size=150, rot=-7, hold=1.6, misreg=True, zoom=True)
s.cinta("cu", "MÁS CURIOSIDADES", "papel", top=1250, rot=-5, at="13.4")
s.speed("sp", "13.3", n=36, seed=9)
