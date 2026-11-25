from lib import *

ep = Episode(3, "que-es-el-multiverso", "¿Qué es el multiverso de Marvel?", 134, cont_in="2.1", cont_pulse="11.2")

# 1 · portada
s = ep.scene("Portada", "S1", bg="multi", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 03: portales, cinta TODO EMPEZÓ CON UNA PUÑALADA")
s.beat(2, 0.7, "el **caos**", "¡CAOS!")
s.beat(3, 1.4, "del **multiverso**", "CAP MULTIVERSO")
s.cover("cover", 3, "multi-osc", portal(500).replace('class="c" style="position:relative"', 'class="c" style="left:450px;top:640px"'), at="1.1", frm="T")
s.cinta("cinta", "TODO EMPEZÓ CON UNA PUÑALADA", "rojo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("caos", "¡CAOS!", "ono", "amarillo", y=900, at="1.2", size=250, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "EL MULTIVERSO", "1.3", width=560)
s.zoom("1.2", 1.12)

# 2 · puñalada
s = ep.scene("La puñalada", "S1", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 3.6, "una sola **puñalada**", "Cuchillo ¡ZAS!")
s.beat(2, 5.2, "primera **temporada**", "Claqueta LOKI T1")
s.beat(3, 6.5, "de **Loki**", "Casco de Loki")
s.obj("k", "knife", 540, 760, 1, 1, "2.1", how="pop") if False else None
s.raw('<div class="c" id="v03-e2-k" style="left:540px;top:800px">' + knife(760) + '</div>', 'COM.slideIn(tl, q("#v03-e2-k"), %s, "L");\nCOM.popOut(tl, q("#v03-e2-k"), %s - 0.05);' % (s.t("2.1"), s.t("2.2")))
s.speed("sl", "2.1", n=36, seed=5)
s.text("zas", "¡ZAS!", "ono", "rojo", y=1250, at="2.1", size=280, rot=-8, hold=1.2, misreg=True, zoom=True)
s.flash("2.1")
s.img("clap", "a-lokilogo.jpg", 540, 820, 900, 500, "2.2", how="slam", frm="B", out="2.3", pos="center")
s.text("t1", "LOKI · T1", "ttl", "amarillo", y=1260, at="2.2", size=130, rot=-4, out="2.3")
s.img("h", "a-loki.jpg", 540, 820, 620, 800, "2.3", how="slam", frm="T", pos="top", bob="end")
s.cinta("loki", "LOKI", "multi", top=1250, rot=-6, at="2.3")

# 3 · línea sagrada
s = ep.scene("Línea Sagrada", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 7.6, "Antes, el **tiempo**", "Nube ANTES + reloj")
s.beat(2, 9.0, "una sola **línea**", "Línea recta se dibuja")
s.beat(3, 10.3, "la Línea **Sagrada**", "Rótulo LÍNEA SAGRADA")
s.beat(4, 11.5, "la **TVA**", "Placa TVA")
s.globo("antes", "ANTES", 280, 400, 520, 330, "3.1", kind="nube", size=64, out="3.2")
s.raw('<div class="c" id="v03-e3-rl" style="left:540px;top:960px">' + svgbox("0 0 300 300", '<circle cx="150" cy="150" r="130" fill="#FFF3D6" stroke="#0B0B14" stroke-width="10"/><path d="M150 150 V60 M150 150 L215 190" stroke="#0B0B14" stroke-width="14" stroke-linecap="round"/><circle cx="150" cy="150" r="14" fill="#E8212B" stroke="#0B0B14" stroke-width="6"/>', 420, 420) + '</div>', 'COM.popIn(tl, q("#v03-e3-rl"), %s, { rot: -8 });\nCOM.popOut(tl, q("#v03-e3-rl"), %s - 0.05);' % (s.t("3.1"), s.t("3.2")))
s.draw("linea2", "M60 960 H1020", "tinta", "3.2", w=70, dur=0.45)
s.draw("linea", "M60 960 H1020", "amarillo", "3.2", w=44, dur=0.45)
s.cinta("sag", "LÍNEA SAGRADA", "multi", top=700, rot=-5, at="3.3", words=["3.3", ("3.3", .35)])
s.panel("tva", '<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:230px">TVA</span></div>', 250, 1130, 580, 270, "amarillo", rot=-3, at="3.4", frm="B")
s.shake("tva", ("3.4", .3), 10)

# 4 · He Who Remains
s = ep.scene("El guardián", "S2", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 12.9, "Su **guardián**", "Silueta de Kang en trono")
s.beat(2, 14.0, "He Who **Remains**", "Cinta HE WHO REMAINS")
s.beat(3, 15.0, "una **variante**", "Dos siluetas iguales")
s.beat(4, 15.8, "de **Kang**", "Etiqueta KANG")
s.img("kang", "a-kang.jpg", 540, 820, 520, 650, "4.1", how="slam", frm="B", pos="center", bob="4.3")
s.cinta("hwr", "HE WHO REMAINS", "amarillo", top=1260, rot=-5, at="4.2", words=["4.2", ("4.2", .3), ("4.2", .55)])
s.img("kang2", "a-kang.jpg", 190, 830, 340, 430, "4.3", how="slam", frm="L", out="4.4", pos="center")
s.img("kang3", "a-kang.jpg", 890, 830, 340, 430, "4.3", how="slam", frm="R", out="4.4", pos="center")
s.text("var", "VARIANTE", "ttl", "papel", x=330, y=450, at="4.3", size=130, rot=-4)
s.text("kk", "¡KANG!", "ono", "amarillo", y=1020, at="4.4", size=240, rot=-7, hold=1.0, misreg=True, zoom=True)

# 5 · Sylvie
s = ep.scene("Sylvie lo mata", "S2", bg="rojo", enter="halftone", color="rojo", pat="pat-benday-fuerte")
s.beat(1, 16.5, "Cuando **Sylvie**", "Silueta de Sylvie con cinta")
s.beat(2, 17.7, "lo **mata**", "Cuchillo ¡ZAS!")
s.beat(3, 18.9, "la línea **explota**", "Línea se rompe")
s.beat(4, 19.9, "se **ramifican**", "Ramas de colores")
s.beat(5, 20.8, "sin **control**", "¡SIN CONTROL!")
s.panel("syl", pho("a-sylvie.jpg", "50% 15%", "SYLVIE", 90), 250, 430, 580, 780, "doom", rot=-3, at="5.1", frm="L", out="5.2")
s.raw('<div class="c" id="v03-e5-k" style="left:540px;top:800px">' + knife(800) + '</div>', 'COM.slideIn(tl, q("#v03-e5-k"), %s, "R");\nCOM.popOut(tl, q("#v03-e5-k"), %s - 0.05);' % (s.t("5.2"), s.t("5.3")))
s.speed("sl", "5.2", n=38, seed=6)
s.text("mata", "¡ZAS!", "ono", "amarillo", y=1260, at="5.2", size=260, rot=-8, hold=1.0, zoom=True)
s.obj("sp", "splat", 540, 900, 1000, 1000, "5.3", how="pop", out="5.4")
s.text("exp", "¡KRAKOOM!", "ono", "papel", y=820, at="5.3", size=230, rot=-6, hold=1.0, out=None)
s.flash("5.3")
s.raw('<div class="c" id="v03-e5-br" style="left:540px;top:830px">' + branches(1000, 560) + '</div>', 'COM.drawOn(tl, qa("#v03-e5-br .br"), %s, { dur: 0.6 });' % s.t("5.4"))
s.text("ctrl", "SIN CONTROL", "ttl", "amarillo", y=1300, at="5.5", size=170, rot=-5, misreg=True, zoom=True)

# 6 · de ahí salió todo
s = ep.scene("De ahí salió todo", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 21.5, "salió **todo**", "Cinta DE AHÍ SALIÓ TODO")
s.beat(2, 23.0, "los **Spider-Man**", "Tres máscaras")
s.beat(3, 25.0, "a **casa**", "Rótulo SIN CAMINO A CASA")
s.beat(4, 26.3, "la **locura**", "Portal + runas")
s.beat(5, 27.3, "Doctor **Strange**", "Rótulo DOCTOR STRANGE")
s.cinta("todo", "DE AHÍ SALIÓ TODO", "rojo", top=520, rot=-5, at="6.1", out="6.2")
for k, (x, f, r) in enumerate(((190, "a-tobey.jpg", -6), (540, "a-andrew.jpg", 0), (890, "a-tom.jpg", 6))):
    s.img(f"sp{k}", f, x, 840, 320, 450, ("6.2", k * 0.12), how="pop", out="6.4", pos="50% 10%", rot=r)
s.cinta("snc", "SIN CAMINO A CASA", "amarillo", top=1250, rot=-5, at="6.3", out="6.4")
s.panel("loc", pho("a-strange.jpg", "50% 10%", "LA LOCURA", 90), 150, 430, 780, 800, "multi", rot=2, at="6.4", frm="R")
s.flash("6.4")
s.cinta("ds", "DOCTOR STRANGE", "amarillo", top=1300, rot=-5, at="6.5")

# 7 · videojuego
s = ep.scene("Un solo guardado", "S2", bg="ciencia", enter="halftone", color="ciencia")
s.beat(1, 28.2, "**Imagina**", "Nube IMAGINA")
s.beat(2, 29.1, "un **videojuego**", "Control de videojuego")
s.beat(3, 30.4, "un solo **guardado**", "Disquete 1 SOLO GUARDADO")
s.globo("im", "IMAGINA", 280, 420, 520, 330, "7.1", kind="nube", size=64, out="7.2")
s.raw('<div class="c" id="v03-e7-gp" style="left:540px;top:900px">' + gamepad(900) + '</div>', 'COM.panelSlam(tl, q("#v03-e7-gp"), %s, { from: "L", rot: 5 });\nCOM.idleBob(tl, q("#v03-e7-gp"), %s + 0.4, %s, { amp: 9, cycle: 1.0 });\nCOM.popOut(tl, q("#v03-e7-gp"), %s - 0.05);' % (s.t("7.2"), s.t("7.2"), s.t("7.3"), s.t("7.3")))
s.raw('<div class="c" id="v03-e7-fl" style="left:540px;top:820px">' + floppy(560) + '</div>', 'COM.dropIn(tl, q("#v03-e7-fl"), %s, { from: -1400 });' % s.t("7.3"))
s.text("uno", "1", "kw", "amarillo", x=540, y=820, at="7.3", size=300, rot=-5, how="stamp")
s.cinta("solo", "UN SOLO GUARDADO", "rojo", top=1200, rot=-5, at="7.3")

# 8 · mil partidas
s = ep.scene("Mil partidas", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 32.3, "hay **mil** partidas", "Cuadrícula de 12 partidas")
s.beat(2, 33.8, "en **paralelo**", "Líneas paralelas")
s.beat(3, 35.0, "**nadie** sabe", "Signos de interrogación")
s.beat(4, 35.9, "la **original**", "¿CUÁL ES LA ORIGINAL?")
cols = ("#1E5BFF", "#8A2BE2", "#00C8E8", "#E8212B", "#1FA85A", "#FFD400")
for k in range(12):
    x, y = 60 + (k % 3) * 330, 420 + (k // 3) * 250
    s.panel(f"g{k}", f'<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:70px">PARTIDA {k+1}</span></div>', x, y, 300, 220, cols[k % 6], rot=(-2, 1, 2, -1)[k % 4], at=None)
s.code('COM.panelSplit(tl, qa("#v03-e8 .panel"), %s, { dirs: ["L", "R", "T", "B"], gap: 0.05 });' % s.t("8.1"))
s.speed("par", "8.2", mode="parallel", dirn="R", n=26, seed=8, dur=0.8, color="#0B0B14")
s.text("nadie", "¿?", "kw", "rojo", x=540, y=860, at="8.3", size=520, rot=-6, how="stamp", out="8.4")
s.cinta("orig", "¿CUÁL ES LA ORIGINAL?", "amarillo", top=1560, rot=-4, at="8.4")
s.zoom("8.4", 1.1)

# 9 · 616
s = ep.scene("Tierra-616", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 36.8, "Nuestra **Tierra**", "Globo terráqueo azul")
s.beat(2, 38.2, "la **seiscientos** dieciséis", "616")
s.raw('<div class="c" id="v03-e9-gl" style="left:540px;top:780px">' + globe(640) + '</div>', 'COM.slideIn(tl, q("#v03-e9-gl"), %s, "B");\nCOM.idleBob(tl, q("#v03-e9-gl"), %s + 0.4, E("9")[1], { amp: 9, cycle: 1.0 });' % (s.t("9.1"), s.t("9.1")))
s.cinta("prin", "TIERRA PRINCIPAL", "amarillo", top=1200, rot=-5, at="9.1")
s.text("n616", "616", "ttl", "amarillo", y=820, at="9.2", size=520, rot=-5, how="stamp", misreg=True, zoom=True)
s.speed("sl", "9.2", n=30, seed=7)

# 10 · cualquiera puede venir
s = ep.scene("Cualquiera puede venir", "S3", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 39.9, "hoy **cualquier** héroe", "Portal con silueta azul")
s.beat(2, 41.2, "o **villano**", "Portal con silueta verde")
s.beat(3, 42.5, "otra **realidad**", "Rótulo OTRA REALIDAD")
s.raw('<div class="c" id="v03-e10-p1" style="left:300px;top:840px">' + portal(540) + '</div>', 'COM.popIn(tl, q("#v03-e10-p1"), %s, { rot: -10 });\nCOM.idleBob(tl, q("#v03-e10-p1"), %s + 0.4, E("10")[1], { amp: 9, cycle: 1.0 });' % (s.t("10.1"), s.t("10.1")))
s.panel("h", pho("a-cap.jpg", "50% 15%"), 230, 770, 140, 190, "heroe", rot=0, at="10.1", frm="T", slam=True)
s.raw('<div class="c" id="v03-e10-p2" style="left:790px;top:1180px">' + portal(540, ("#1FA85A", "#0E5C32", "#FFD400", "#FFF3D6")) + '</div>', 'COM.popIn(tl, q("#v03-e10-p2"), %s, { rot: 10 });\nCOM.idleBob(tl, q("#v03-e10-p2"), %s + 0.4, E("10")[1], { amp: 9, cycle: 1.0 });' % (s.t("10.2"), s.t("10.2")))
s.panel("v", pho("drdoom-recorte.png", "50% 10%"), 725, 1100, 130, 170, "doom", rot=0, at="10.2", frm="B")
s.text("or", "OTRA<br>REALIDAD", "ttl", "amarillo", x=540, y=1000, at="10.3", size=150, rot=-5, misreg=True, zoom=True)

# 11 · alguien tiene que cuidar
s = ep.scene("Alguien cuida", "S3", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 43.7, "alguien tiene que **cuidar**", "Ojo vigilante")
s.beat(2, 45.3, "esas **partidas**", "Partidas bajo el ojo")
s.raw('<div class="c" id="v03-e11-ey" style="left:540px;top:620px">' + eye(760) + '</div>', 'COM.popIn(tl, q("#v03-e11-ey"), %s, { rot: 0 });\nCOM.idleBob(tl, q("#v03-e11-ey"), %s + 0.4, E("11")[1], { amp: 9, cycle: 1.0 });' % (s.t("11.1"), s.t("11.1")))
s.text("q", "¿QUIÉN?", "ono", "amarillo", y=1000, at="11.1", size=250, rot=-6, hold=1.5)
for k in range(6):
    x, y = 60 + (k % 3) * 330, 1130 + (k // 3) * 170
    s.panel(f"g{k}", f'<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:52px">PARTIDA</span></div>', x, y, 300, 140, cols[k % 6], rot=(-2, 1, 2)[k % 3], at=None)
s.code('COM.panelSplit(tl, qa("#v03-e11 .panel"), %s, { dirs: ["B", "L", "R"], gap: 0.06 });' % s.t("11.2"))

# 12 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 46.5, "**Siguiente**", "Portada N.º 04 entra")
s.beat(2, 47.3, "dos **universos**", "Dos portales")
s.beat(3, 47.9, "**chocan**", "¡CHOQUE!")
two = ('<div class="c" style="left:340px;top:700px"><svg viewBox="0 0 200 200" style="width:260px;height:260px"><circle cx="100" cy="100" r="90" fill="#1E5BFF" stroke="#0B0B14" stroke-width="9"/></svg></div>'
       '<div class="c" style="left:560px;top:700px"><svg viewBox="0 0 200 200" style="width:260px;height:260px"><circle cx="100" cy="100" r="90" fill="#E8212B" stroke="#0B0B14" stroke-width="9"/></svg></div>')
s.cover("cover", 4, "multi-osc", two, at="12.1", frm="R")
s.text("q", "¿QUÉ PASA SI<br>CHOCAN?", "ttl", "amarillo", x=540, y=1010, at="12.2", size=100, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1200, rot=-8, at="12.3")
s.text("boom", "¡CRASH!", "ono", "rojo", y=720, at="12.3", size=200, rot=-8, hold=0.8, zoom=True)
