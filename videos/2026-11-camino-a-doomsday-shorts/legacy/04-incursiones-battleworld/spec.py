from lib import *

ep = Episode(4, "incursiones-battleworld", "¿Qué son las incursiones y Battleworld?", 132, cont_in="2.1", cont_pulse="12.2")
two_globes = ('<div class="c" style="left:300px;top:700px"><div id="v04-e1-ga" style="width:360px;height:360px">' + globe(360).replace('class="c" style="position:relative"', 'style="position:relative;display:flex"') + '</div></div>'
              '<div class="c" style="left:600px;top:700px"><div id="v04-e1-gb" style="width:360px;height:360px">' + globe(360, "#00C8E8").replace('class="c" style="position:relative"', 'style="position:relative;display:flex"') + '</div></div>')

# 1 · portada
s = ep.scene("Portada", "S1", bg="multi", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 04: dos Tierras")
s.beat(2, 0.6, "En los **cómics**", "CAP EN LOS CÓMICS")
s.beat(3, 1.5, "dos **Tierras**", "Dos globos chocan")
s.cover("cover", 4, "multi-osc", two_globes, at="1.1", frm="T")
s.cinta("cinta", "DOS TIERRAS CHOCARON", "rojo", top=1190, rot=-8, at="1.1")
s.cap("cap", "EN LOS CÓMICS", "1.2", width=560)
s.speed("sl", "1.3", n=30, seed=2)
s.code('tl.to(q("#v04-e1-ga"), { x: 40, duration: 0.25, ease: "power4.in" }, b("1.3"));\ntl.to(q("#v04-e1-gb"), { x: -40, duration: 0.25, ease: "power4.in" }, b("1.3"));')
s.zoom("1.3", 1.12)

# 2 · choque
s = ep.scene("El choque", "S1", bg="rojo", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 2.6, "**chocaron**", "¡CRASH!")
s.beat(2, 3.6, "multiverso **entero**", "Portales se rompen")
s.beat(3, 4.1, "se **acabó**", "FIN")
s.text("cr", "¡CRASH!", "ono", "amarillo", y=820, at="2.1", size=290, rot=-8, hold=1.0, misreg=True, zoom=True)
s.speed("sl", "2.1", n=40, seed=3, dur=0.6)
s.flash("2.1")
s.raw('<div class="c" id="v04-e2-pt" style="left:540px;top:780px">' + portal(700) + '</div>', 'COM.popIn(tl, q("#v04-e2-pt"), %s, { rot: 0 });\nCOM.popOut(tl, q("#v04-e2-pt"), %s - 0.05);' % (s.t("2.2"), s.t("2.3")))
s.obj("sp", "splat", 540, 800, 1000, 1000, "2.3", how="pop")
s.text("fin", "FIN", "ttl", "papel", y=1300, at="2.3", size=300, rot=-4, misreg=True)

# 3 · cine
s = ep.scene("Al cine", "S1", bg="papel", enter="halftone", color="papel")
s.beat(1, 4.6, "**Marvel**", "Cinta MARVEL")
s.beat(2, 5.7, "esa **historia**", "Cómic abierto")
s.beat(3, 6.8, "para el **cine**", "Pantalla de cine")
s.cinta("mv", "MARVEL PREPARA", "rojo", top=470, rot=-5, at="3.1", words=["3.1", ("3.1", .35)])
s.obj("cm", "comicOpen", 540, 900, 700, 560, "3.2", how="slam", frm="L", rot=-4, out="3.3")
s.obj("sc", "cinemaScreen", 540, 900, 820, 600, "3.3", how="slam", frm="R", bob="end")
s.cinta("cine", "EN CINES", "amarillo", top=1280, rot=-5, at="3.3")

# 4 · incursión
s = ep.scene("Se llama incursión", "S2", bg="multi", enter="pageflip", color="multi")
s.beat(1, 7.9, "Se **llama**", "Nube SE LLAMA")
s.beat(2, 8.5, "**incursión**", "¡INCURSIÓN!")
s.text("ll", "SE LLAMA…", "ttl", "papel", y=820, at="4.1", size=170, rot=-4, out="4.2")
s.slab("sl2", "multi-osc", "4.2", ("4.2", 0.9))
s.text("inc", "INCURSIÓN", "ono", "amarillo", y=820, at="4.2", size=210, rot=-6, hold=1.5, misreg=True, zoom=True)
s.speed("sl", "4.2", n=38, seed=4)

# 5 · dos universos
s = ep.scene("Dos universos", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 9.8, "dos **universos**", "Dos portales se acercan")
s.beat(2, 11.2, "se **superponen**", "Se traslapan")
s.beat(3, 12.6, "**destruirse**", "Uno se agrieta")
s.beat(4, 13.8, "el otro **viva**", "El otro brilla")
s.raw('<div class="c" id="v04-e5-a" style="left:280px;top:820px">' + portal(560) + '</div>', 'COM.slideIn(tl, q("#v04-e5-a"), %s, "L");\ntl.to(q("#v04-e5-a"), { x: 130, duration: 0.5, ease: "power2.inOut" }, %s);' % (s.t("5.1"), s.t("5.2")))
s.raw('<div class="c" id="v04-e5-b" style="left:800px;top:820px">' + portal(560, ("#1FA85A", "#0E5C32", "#FFD400", "#FFF3D6")) + '</div>', 'COM.slideIn(tl, q("#v04-e5-b"), %s, "R");\ntl.to(q("#v04-e5-b"), { x: -130, duration: 0.5, ease: "power2.inOut" }, %s);' % (s.t("5.1"), s.t("5.2")))
s.cap("cap", "INCURSIÓN", "5.2", top=1330, width=480)
s.code('tl.to(q("#v04-e5-a"), { scale: 0, rotation: -40, duration: 0.3, ease: "power3.in" }, %s);' % s.t("5.3"))
s.obj("sp", "splat", 410, 820, 700, 700, "5.3", how="pop", out="5.4")
s.text("de", "¡DESTRUIDO!", "ono", "rojo", y=1230, at="5.3", size=170, rot=-7, hold=1.1, zoom=True)
s.pulse("b", "5.4", 1.18)
s.text("viva", "¡VIVE!", "ono", "amarillo", y=1230, at="5.4", size=210, rot=-6, hold=1.0)

# 6 · mueren los dos
s = ep.scene("Mueren los dos", "S2", bg="rojo", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 15.3, "mueren", "Ambos se rompen")
s.beat(2, 16.0, "los **dos**", "X sobre los dos")
s.raw('<div class="c" id="v04-e6-a" style="left:330px;top:820px">' + portal(480) + '</div>', 'COM.popIn(tl, q("#v04-e6-a"), %s - 0.3, { rot: 0 });\ntl.to(q("#v04-e6-a"), { scale: 0, rotation: -30, duration: 0.25, ease: "power3.in" }, %s);' % (s.t("6.1"), s.t("6.1")))
s.raw('<div class="c" id="v04-e6-b" style="left:750px;top:820px">' + portal(480, ("#1FA85A", "#0E5C32", "#FFD400", "#FFF3D6")) + '</div>', 'COM.popIn(tl, q("#v04-e6-b"), %s - 0.3, { rot: 0 });\ntl.to(q("#v04-e6-b"), { scale: 0, rotation: 30, duration: 0.25, ease: "power3.in" }, %s);' % (s.t("6.1"), s.t("6.1", )))
s.text("mu", "¡MUEREN!", "ono", "amarillo", y=820, at="6.1", size=250, rot=-7, hold=1.2, misreg=True, zoom=True)
s.obj("x", "xMark", 540, 1250, 420, 420, "6.2", how="stamp")
s.cinta("amb", "LOS DOS", "papel", top=1500, rot=-5, at="6.2")

# 7 · borrando mundos
s = ep.scene("Mundos borrados", "S2", bg="tinta", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 17.0, "las **incursiones**", "Fila de mundos")
s.beat(2, 18.1, "**borrando** mundos", "X sobre cada mundo")
s.beat(3, 19.3, "**uno por uno**", "Quedan menos")
cl = ("#1E5BFF", "#8A2BE2", "#00C8E8", "#E8212B", "#1FA85A", "#FFD400")
for k in range(6):
    x, y = 220 + (k % 3) * 320, 620 + (k // 3) * 380
    s.raw(f'<div class="c" id="v04-e7-w{k}" style="left:{x}px;top:{y}px">' + globe(280, cl[k]) + '</div>', f'COM.popIn(tl, q("#v04-e7-w{k}"), {s.t("7.1")} + {k*0.1}, {{ rot: -8 }});\nCOM.popOut(tl, q("#v04-e7-w{k}"), {s.t("7.2")} + {0.2+ k*0.35});')
s.text("bor", "BORRADOS", "ttl", "amarillo", y=1300, at="7.2", size=170, rot=-4, misreg=True)
s.cinta("uno", "UNO POR UNO", "rojo", top=1480, rot=-5, at="7.3")

# 8 · Battleworld
s = ep.scene("Battleworld", "S2", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 21.7, "los **restos**", "Pedazos caen")
s.beat(2, 22.7, "**nació**", "Se arma el planeta")
s.beat(3, 23.4, "**Battleworld**", "Planeta mosaico + cinta")
s.beat(4, 24.5, "**pedazos**", "Cada pedazo brilla")
s.beat(5, 25.1, "**realidades**", "CAP DE REALIDADES")
s.raw('<div class="c" id="v04-e8-m" style="left:540px;top:820px">' + mosaic(760) + '</div>', 'tl.set(qa("#v04-e8-m .pz"), { opacity: 0 }, 0);\ntl.fromTo(qa("#v04-e8-m .pz"), { opacity: 0, y: -900 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.in", stagger: 0.09, immediateRender: false }, %s);\nCOM.idleBob(tl, q("#v04-e8-m"), %s + 0.6, E("8")[1], { amp: 10, cycle: 1.2 });' % (s.t("8.1"), s.t("8.1")))
s.text("nac", "¡NACE!", "ono", "amarillo", x=340, y=470, at="8.2", size=190, rot=-6, hold=0.9)
s.cinta("bw", "BATTLEWORLD", "amarillo", top=1280, rot=-5, at="8.3", words=["8.3"])
s.speed("sl", "8.3", n=34, seed=5)
s.zoom("8.3", 1.12)
s.code('COM.pulse(tl, q("#v04-e8-m"), %s, { to: 1.1 });' % s.t("8.4"))
s.cap("cap", "PEDAZOS DE REALIDADES", "8.5", top=1460, width=780)

# 9 · Dios Doom
s = ep.scene("Dios Doom", "S2", bg="doom", enter="pageflip", color="doom")
s.beat(1, 25.9, "Su **dueño**", "Doom aparece")
s.beat(2, 27.3, "convertido en **Dios**", "¡DIOS DOOM!")
s.img("doom", "drdoom-recorte.png", 540, 860, 760, 760, "9.1", how="slide", frm="B", bob="end")
s.obj("crown", "crown", 360, 430, 520, 370, "9.2", how="drop")
s.text("dios", "¡DIOS DOOM!", "ono", "amarillo", y=1330, at="9.2", size=200, rot=-6, hold=1.4, misreg=True, zoom=True)
s.speed("sl", "9.2", n=36, seed=9)

# 10 · autos
s = ep.scene("Dos autos", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 28.7, "**Imagina**", "Nube IMAGINA")
s.beat(2, 29.8, "dos **autos**", "Dos autos desde los lados")
s.beat(3, 31.2, "de **frente**", "Choque frontal")
s.beat(4, 32.2, "un solo **carril**", "Carretera de un carril")
s.beat(5, 33.6, "**desaparecer**", "Uno se desvanece")
s.globo("im", "IMAGINA", 280, 400, 520, 330, "10.1", kind="nube", size=62, out="10.2")
s.raw('<div style="position:absolute;left:0;top:1010px;width:1080px;height:180px;background:#6B7280;border-top:10px solid #0B0B14;border-bottom:10px solid #0B0B14" id="v04-e10-rd"><div style="position:absolute;left:0;right:0;top:80px;height:14px;background:repeating-linear-gradient(90deg,#FFD400 0 60px,transparent 60px 110px)"></div></div>', 'COM.slideIn(tl, q("#v04-e10-rd"), %s, "B");' % s.t("10.2"))
s.raw('<div class="c" id="v04-e10-a" style="left:200px;top:980px">' + car(440, "#1E5BFF") + '</div>', 'COM.slideIn(tl, q("#v04-e10-a"), %s, "L");\ntl.to(q("#v04-e10-a"), { x: 130, duration: 0.45, ease: "power4.in" }, %s);' % (s.t("10.2"), s.t(("10.3", -0.15))))
s.raw('<div class="c" id="v04-e10-b" style="left:880px;top:980px">' + car(440, "#E8212B", True) + '</div>', 'COM.slideIn(tl, q("#v04-e10-b"), %s, "R");\ntl.to(q("#v04-e10-b"), { x: -130, duration: 0.45, ease: "power4.in" }, %s);' % (s.t("10.2"), s.t(("10.3", -0.15))))
s.text("bam", "¡BAM!", "ono", "amarillo", y=700, at="10.3", size=270, rot=-8, hold=1.0, zoom=True, misreg=True)
s.flash("10.3")
s.cinta("car", "UN SOLO CARRIL", "rojo", top=1300, rot=-4, at="10.4")
s.code('tl.to(q("#v04-e10-b"), { scale: 0, rotation: 30, opacity: 0, duration: 0.3, ease: "power3.in" }, %s);' % s.t("10.5"))
s.text("des", "UNO SOBRA", "ttl", "rojo", y=560, at="10.5", size=130, rot=-4)

# 11 · Doom junta pedazos
s = ep.scene("Doom construye", "S2", bg="doom", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 35.6, "juntó los **pedazos**", "Pedazos vuelan al centro")
s.beat(2, 37.2, "para **construir**", "Se arma el planeta")
s.beat(3, 38.1, "un **mundo**", "¡MUNDO!")
s.raw('<div class="c" id="v04-e11-m" style="left:540px;top:820px">' + mosaic(780) + '</div>', 'tl.set(qa("#v04-e11-m .pz"), { opacity: 0 }, 0);\ntl.fromTo(qa("#v04-e11-m .pz"), { opacity: 0, x: 700, rotation: 90 }, { opacity: 1, x: 0, rotation: 0, duration: 0.35, ease: "back.out(1.4)", stagger: 0.12, immediateRender: false }, %s);\nCOM.idleBob(tl, q("#v04-e11-m"), %s + 0.6, E("11")[1], { amp: 10, cycle: 1.2 });' % (s.t("11.1"), s.t("11.1")))
s.panel("dm", Scene.pobj("doomMask", 180, 230), 800, 380, 200, 250, "doom-osc", rot=4, at="11.2", frm="R")
s.text("mun", "¡UN MUNDO!", "ono", "amarillo", y=1330, at="11.2", size=200, rot=-6, hold=1.0, zoom=True)

# 12 · Doomsday fecha
s = ep.scene("Doomsday", "S3", bg="doom-osc", enter="halftone", color="doom", pat="pat-benday-fuerte")
s.beat(1, 39.0, "**Doomsday**", "Logo")
s.beat(2, 40.1, "este **diciembre**", "Calendario 18 DIC")
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:760px;height:380px;object-fit:contain" /></div>', 90, 430, 900, 520, "papel", rot=-2, at="12.1", frm="T")
s.obj("cal", "calendar", 540, 1250, 400, 420, ("12.1", 0.9), how="drop", bob="end")
s.text("fe", "18 DE DICIEMBRE", "ttl", "amarillo", y=1560, at=("12.1", 1.1), size=96, rot=-4, how="stamp")

# 13 · Secret Wars
s = ep.scene("Secret Wars", "S3", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 41.2, "**Secret** Wars", "SECRET WARS")
s.beat(2, 43.0, "que **cierra**", "CIERRA LA SAGA")
s.beat(3, 44.2, "dos mil **veintisiete**", "2027")
s.text("sw", "SECRET<br>WARS", "ttl", "amarillo", y=720, at="13.1", size=270, rot=-5, misreg=True, zoom=True)
s.speed("sl", "13.1", n=34, seed=4)
s.cinta("cie", "CIERRA LA SAGA", "rojo", top=1180, rot=-5, at="13.2", words=["13.2", ("13.2", .3), ("13.2", .5)])
s.text("a27", "2027", "kw", "papel", y=1450, at="13.3", size=250, rot=-4, how="stamp", misreg=True)

# 14 · un hombre
s = ep.scene("El mismo hombre", "S3", bg="doom", enter="halftone", color="doom")
s.beat(1, 45.7, "todo **gira**", "Mundos orbitan")
s.beat(2, 46.9, "mismo **hombre**", "Doom al centro")
s.img("doom", "doom-mask.png", 540, 800, 520, 620, "14.2", how="slam", frm="B", pos="center")
for k, (x, y, c) in enumerate(((200, 560, "#1E5BFF"), (880, 600, "#8A2BE2"), (240, 1120, "#00C8E8"), (860, 1150, "#E8212B"))):
    s.raw(f'<div class="c" id="v04-e14-w{k}" style="left:{x}px;top:{y}px">' + globe(220, c) + '</div>', f'COM.popIn(tl, q("#v04-e14-w{k}"), {s.t("14.1")} + {k*0.1}, {{ rot: -8 }});\nCOM.idleBob(tl, q("#v04-e14-w{k}"), {s.t("14.1")} + 0.5, E("14")[1], {{ amp: 12, cycle: {0.9 + k*0.1} }});')
s.text("hom", "¡EL MISMO!", "ono", "amarillo", y=1400, at="14.2", size=200, rot=-6, hold=1.0, misreg=True, zoom=True)

# 15 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 47.9, "**Siguiente**", "Portada N.º 05")
s.beat(2, 48.8, "el **guardián**", "Cinta GUARDIÁN")
s.beat(3, 49.9, "**Loki**", "Casco de Loki")
s.cover("cover", 5, "multi-osc", Scene.cover_img('a-loki.jpg', 400, 500, 'top', 450, 640), at="15.1", frm="R")
s.text("q", "¿EL GUARDIÁN<br>DEL MULTIVERSO?", "ttl", "amarillo", x=540, y=1060, at="15.2", size=82, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1230, rot=-8, at="15.3")
