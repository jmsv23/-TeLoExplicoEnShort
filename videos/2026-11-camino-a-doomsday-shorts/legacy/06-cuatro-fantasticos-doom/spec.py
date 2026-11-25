from lib import *

ep = Episode(6, "cuatro-fantasticos-doom", "Los Cuatro Fantásticos y Doom", 137, cont_in="2.1", cont_pulse="10.1")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
FOUR = Scene.cover_img("a-logo4.jpg", 420, 430, "center", 450, 640)

# 1 · portada
s = ep.scene("Portada", "S1", bg="heroe", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 06: emblema 4")
s.beat(2, 0.4, "Los **Cuatro**", "¡LOS 4!")
s.beat(3, 1.9, "en **First** Steps", "CAP FIRST STEPS")
s.cover("cover", 6, "#14378F", FOUR, at="1.1", frm="T")
s.cinta("cinta", "NO SON DE NUESTRO UNIVERSO", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("l4", "¡LOS 4!", "ono", "amarillo", y=900, at="1.2", size=260, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "FIRST STEPS", "1.3", width=520)
s.zoom("1.2", 1.12)

# 2 · otro universo
s = ep.scene("No son de aquí", "S1", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 3.5, "de **nuestro** universo", "Tierra-616 con X")
s.beat(2, 4.2, "universo", "Otra Tierra retro")
s.beat(3, 5.0, "**cambia** todo", "¡CAMBIA TODO!")
V(s, "g1", globe(520), 300, 820, "2.1", how="slam", frm="L", out="2.3")
s.obj("fx", "forbidden", 300, 820, 460, 460, ("2.1", .3), how="stamp", out="2.3")
s.cinta("n616", "NUESTRO UNIVERSO", "amarillo", top=1230, rot=-5, at="2.1", out="2.3")
V(s, "g2", globe(520, "#00C8E8"), 780, 1000, "2.2", how="slam", frm="R", bob="end", rot=-4)
s.cinta("otra", "OTRA TIERRA", "rojo", top=1400, rot=5, at="2.2")
s.text("cam", "¡CAMBIA<br>TODO!", "ono", "amarillo", x=400, y=620, at="2.3", size=220, rot=-7, hold=1.4, misreg=True, zoom=True)

# 3 · reparto
s = ep.scene("La familia", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 7.3, "es **Reed** Richards", "Reed: estira")
s.beat(2, 8.9, "es **Sue**", "Sue: campo de fuerza")
s.beat(3, 10.3, "es **Johnny**", "Johnny: fuego")
s.beat(4, 11.4, "**Grimm**", "Ben: roca")
for k, (nm, act, f, pos, x, y, at, frm) in enumerate((("REED", "PEDRO PASCAL", "a-pedro.jpg", "50% 15%", 40, 400, "3.1", "L"), ("SUE", "VANESSA KIRBY", "a-vanessa.jpg", "50% 15%", 550, 400, "3.2", "R"), ("JOHNNY", "JOSEPH QUINN", "a-joseph.jpg", "50% 15%", 40, 930, "3.3", "L"), ("BEN", "EBON MOSS-BACHRACH", "a-ebon.jpg", "50% 25%", 550, 930, "3.4", "R"))):
    s.panel(f"p{k}", pho(f, pos, nm, 64, sub=act), x, y, 490, 500, "papel", rot=(-2, 2, 2, -2)[k], at=at, frm=frm)
s.code('COM.shake(tl, q("#v06-e3-p3"), %s, { amp: 10, dur: 0.4 });' % s.t("3.4"))

# 4 · primera familia
s = ep.scene("Tierra retrofuturista", "S2", bg="ciencia", enter="pageflip", color="ciencia")
s.beat(1, 13.0, "primera **familia**", "Emblema 4 + LA PRIMERA FAMILIA")
s.beat(2, 14.3, "una **Tierra**", "Globo retro")
s.beat(3, 15.6, "años **sesenta**", "AÑOS 60")
s.img("fe", "a-fantastic4.jpg", 540, 800, 920, 690, "4.1", how="slam", frm="B", bob="4.2", pos="center")
s.cinta("fam", "LA PRIMERA FAMILIA", "rojo", top=1250, rot=-5, at="4.1", out="4.2")
V(s, "gl", globe(600, "#FFD400"), 540, 820, "4.2", how="pop", bob="end", rot=-8)
s.cinta("retro", "TIERRA RETROFUTURISTA", "tinta", top=1250, rot=5, at="4.2")
s.text("s60", "AÑOS 60", "ttl", "tinta", x=360, y=520, at="4.3", size=200, rot=-5, how="stamp", misreg=True, zoom=True)
s.code('tl.set(q("#v06-e4-s60"), { webkitTextStroke: "0px" }, 0);') if False else None

# 5 · compañeros
s = ep.scene("Compañeros", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 16.9, "En los **cómics**", "Cómic abierto")
s.beat(2, 18.0, "**compañero** de universidad", "Edificio y dos estudiantes")
s.beat(3, 19.4, "von **Doom**", "Victor von Doom")
s.obj("cm", "comicOpen", 540, 780, 700, 560, "5.1", how="slam", frm="B", rot=-4, out="5.2")
s.cap("cap", "EN LOS CÓMICS", "5.1", top=1260, width=520, out="5.2")
V(s, "bd", building(700), 540, 620, "5.2", how="slide", frm="T")
s.panel("r", pho("a-reed.jpg", "50% 10%", "REED", 48), 120, 960, 330, 390, "heroe", rot=-3, at="5.2", frm="L")
s.panel("v", pho("drdoom-recorte.png", "50% 10%", "VICTOR", 48), 630, 960, 330, 390, "doom", rot=3, at=("5.2", .15), frm="R")
s.cinta("vvd", "VICTOR VON DOOM", "doom", top=1440, rot=-5, at="5.3")

# 6 · advierte
s = ep.scene("La advertencia", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 20.8, "le **advirtió**", "Reed con globo")
s.beat(2, 21.7, "**fallaría**", "Experimento con grieta")
s.panel("r", pho("a-reed.jpg", "50% 10%", "REED", 70), 80, 440, 450, 700, "papel", rot=-3, at="6.1", frm="L")
s.globo("cu", "¡CUIDADO!", 480, 450, 520, 260, "6.1", size=78, rot=3)
s.obj("g", "gearAtom", 790, 1000, 420, 420, "6.2", how="pop")
s.obj("x", "xMark", 790, 1000, 480, 480, ("6.2", .25), how="stamp")
s.text("fa", "¡VA A FALLAR!", "kw", "amarillo", y=1330, at="6.2", size=140, rot=-4, how="stamp", misreg=True)

# 7 · explotó
s = ep.scene("Doom no escuchó", "S2", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 22.9, "no **escuchó**", "Doom: ¡NO!")
s.beat(2, 23.9, "todo **explotó**", "¡KRAKOOM!")
s.beat(3, 25.0, "lo **culpa**", "Flecha a los 4")
s.img("mask", "doom-mask.png", 400, 880, 600, 720, "7.1", how="slide", frm="T", pos="center", bob="end")
s.text("no", "¡NO!", "ono", "amarillo", x=760, y=500, at="7.1", size=240, rot=-7, hold=1.2)
s.slab("ro", "rojo", "7.2", ("7.2", 0.8))
s.obj("sp", "splat", 540, 820, 1000, 1000, "7.2", how="pop", out="7.3")
s.text("kr", "¡KRAKOOM!", "ono", "amarillo", y=820, at="7.2", size=230, rot=-7, hold=0.9, misreg=True, zoom=True, out="7.3")
s.img("fe", "a-logo4.jpg", 840, 1050, 330, 330, "7.3", how="slam", frm="R", pos="center")
s.draw("fl", "M650 1050 C700 990 720 990 760 1020", "amarillo", "7.3", w=18, dur=0.3)
s.text("cu", "¡CULPA!", "ono", "rojo", x=760, y=700, at="7.3", size=190, rot=-8, hold=1.2)

# 8 · analogía
s = ep.scene("El alumno brillante", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 27.0, "el **alumno** más brillante", "Examen de Doom: 9")
s.beat(2, 29.0, "siempre le **ganaba**", "Examen de Reed: 10")
s.beat(3, 30.3, "con **armaduras**", "Armadura")
s.beat(4, 31.4, "y **rayos** cósmicos", "Rayo cósmico")
s.panel("ed", '<div class="c" style="position:relative;flex-direction:column"><span style="font:400 58px Anton;color:#0B0B14">EXAMEN</span><span class="ttl ttl--doom" style="font-size:280px;line-height:1">9</span></div>', 40, 420, 480, 620, "papel", rot=-3, at="8.1", frm="L")
s.panel("er", '<div class="c" style="position:relative;flex-direction:column"><span style="font:400 58px Anton;color:#0B0B14">EXAMEN</span><span class="ttl ttl--rojo" style="font-size:280px;line-height:1">10</span></div>', 560, 420, 480, 620, "papel", rot=3, at="8.2", frm="R")
s.cinta("ga", "SIEMPRE GANABA REED", "heroe", top=1090, rot=-5, at="8.2")
s.obj("ar", "doomMask", 250, 1400, 240, 300, "8.3", how="pop", bob="end")
s.obj("bo", "bolt", 830, 1400, 240, 300, "8.4", how="pop", bob="end")
s.text("ac", "ARMADURAS<br>+ RAYOS", "ttl", "tinta", x=540, y=1400, at="8.4", size=62, rot=-3, how="pop")

# 9 · película termina
s = ep.scene("Doom en escena", "S2", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 32.4, "la **película** termina", "Pantalla de cine")
s.beat(2, 33.3, "**termina** con Doom", "Pantalla se oscurece")
s.beat(3, 34.2, "**apareciendo**", "Doom aparece")
s.obj("sc", "cinemaScreen", 540, 820, 860, 640, "9.1", how="slam", frm="B")
s.code('tl.fromTo(q("#v06-e9-sc"), { opacity: 1 }, { opacity: 1, duration: 0.01, immediateRender: false }, %s);' % s.t("9.2"))
s.img("mask", "doom-mask.png", 540, 820, 520, 620, "9.3", how="slam", frm="B", pos="center")
s.text("do", "¡DOOM!", "ono", "amarillo", y=1330, at="9.3", size=230, rot=-6, hold=1.2, misreg=True, zoom=True)
s.cap("cap", "ESCENA FINAL", "9.2", top=1450, width=520)

# 10 · Doomsday
s = ep.scene("No solo héroes", "S3", bg="multi", enter="halftone", color="multi")
s.beat(1, 35.7, "**Doomsday**", "Logo")
s.beat(2, 36.8, "no es **solo** héroes", "Siluetas héroes")
s.beat(3, 37.9, "un **villano**", "Villano solo")
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:700px;height:300px;object-fit:contain" /></div>', 90, 400, 900, 400, "papel", rot=-2, at="10.1", frm="T")
for k, x in enumerate((220, 540, 860)):
    s.panel(f"h{k}", pho(("a-cap.jpg", "a-thor.jpg", "a-tom.jpg")[k], "50% 15%"), x - 110, 1040, 220, 280, "heroe", rot=(-3, 2, -2)[k], at=("10.2", k * 0.1), frm="B")
s.cinta("sol", "NO SOLO HÉROES", "amarillo", top=1380, rot=-5, at="10.2")
s.text("vi", "¿UN VILLANO?", "kw", "rojo", y=900, at="10.3", size=170, rot=-5, how="stamp", misreg=True)

# 11 · Reed vs hombre
s = ep.scene("Reed contra Doom", "S3", bg="papel", enter="ink", color="tinta")
s.beat(1, 38.8, "Es **Reed** contra", "Reed")
s.beat(2, 39.8, "**contra**", "VS")
s.beat(3, 40.6, "el **hombre**", "Doom")
s.beat(4, 41.3, "que lo **odia**", "¡ODIO!")
s.beat(5, 42.0, "la **universidad**", "Edificio")
s.panel("r", pho("a-reed.jpg", "50% 10%", "REED", 70), 40, 420, 450, 760, "heroe", rot=-3, at="11.1", frm="L")
s.panel("d", pho("drdoom-recorte.png", "50% 10%", "DOOM", 70), 590, 420, 450, 760, "doom", rot=3, at="11.3", frm="R")
s.text("vs", "VS", "ono", "amarillo", y=800, at="11.2", size=300, rot=-6, hold=9, misreg=True)
s.text("od", "¡ODIA!", "ono", "rojo", x=380, y=1330, at="11.4", size=240, rot=-7, hold=1.0, zoom=True)
V(s, "bd", building(330), 840, 1330, "11.5", how="pop")

# 12 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 42.7, "**Siguiente**", "Portada N.º 07")
s.beat(2, 44.1, "el **escudo**", "Escudo")
s.beat(3, 44.9, "**Capitán** América", "Cinta")
s.cover("cover", 7, "multi-osc", Scene.cover_img('a-sam.jpg', 400, 500, 'top', 450, 640), at="12.1", frm="R")
s.text("q", "¿QUIÉN CARGA<br>EL ESCUDO?", "ttl", "amarillo", x=540, y=1130, at="12.2", size=80, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1290, rot=-8, at="12.3")
