from lib import *

ep = Episode(10, "despues-de-endgame", "¿Qué pasó después de Endgame?", 106, cont_in="2.1", cont_pulse="10.3")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def cover_in(svg, x=450, y=640): return f'<div class="c" style="left:{x}px;top:{y}px">{svg}</div>'
def num(s, name, n, at, color="amarillo", y=560, x=540, out=None, size=520):
    s.text(name, str(n), "kw", color, x=x, y=y, at=at, size=size, rot=-5, how="stamp", out=out, misreg=True)
CH = ("heroe", "multi", "papel", "ciencia", "rojo", "ceniza")

# 1 · portada
s = ep.scene("Portada", "S1", bg="heroe", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 10: calendario")
s.beat(2, 1.2, "pasaron **siete** años", "¡7 AÑOS!")
s.beat(3, 2.3, "más de **treinta**", "30+")
s.cover("cover", 10, "tinta", '<div class="c" style="left:450px;top:620px"><div data-com="calendar" data-opts=\'{"mes":"2019","dia":"7","anio":"AÑOS"}\' style="width:340px;height:360px"></div></div>', at="1.1", frm="T")
s.cinta("cinta", "DESDE ENDGAME", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=28, seed=2)
s.text("s7", "¡7 AÑOS!", "ono", "amarillo", y=900, at="1.2", size=220, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "30+ TÍTULOS", "1.3", width=520)

# 2 · lo único
s = ep.scene("Lo único", "S1", bg="papel", enter="halftone", color="papel")
s.beat(1, 3.4, "treinta **títulos**", "Pila de títulos")
s.beat(2, 5.2, "lo **único**", "SOLO 6")
for k in range(15):
    x, y = 70 + (k % 5) * 190, 440 + (k // 5) * 230
    s.panel(f"t{k}", Scene.pobj("faceless", 1, 1) + '<div class="c" style="position:relative"><span style="font:400 40px Anton;color:#0B0B14">TÍTULO</span></div>', x, y, 170, 200, CH[k % 6], rot=(-3, 2, -2, 3, -1)[k % 5], at=None)
s.code('COM.panelSplit(tl, qa("#v10-e2 .panel"), %s, { dirs: ["T", "B", "L", "R"], gap: 0.04 });' % s.t("2.1"))
s.text("n30", "30+", "ttl", "rojo", y=1280, at="2.1", size=330, rot=-5, how="stamp", out="2.2", misreg=True)
s.slab("sl2", "amarillo", "2.2", ("2.2", 1.5), pat=True)
s.text("n6", "SOLO 6", "ono", "rojo", y=820, at="2.2", size=330, rot=-6, hold=1.3, misreg=True, zoom=True)

# 3 · uno
s = ep.scene("Uno: Sam", "S2", bg="heroe", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 6.6, "**Uno**", "1")
s.beat(2, 8.0, "hereda el **escudo**", "Escudo")
num(s, "n", 1, "3.1", y=700, out="3.2", size=560)
s.img("sh", "a-samcap.jpg", 540, 780, 470, 670, "3.2", how="slam", frm="R", bob="end", pos="top")
s.cinta("sam", "SAM WILSON HEREDA EL ESCUDO", "amarillo", top=1230, rot=-5, at="3.2")

# 4 · Loki
s = ep.scene("Dos: Loki", "S2", bg="multi", enter="halftone", color="multi")
s.beat(1, 8.9, "**Dos**", "2")
s.beat(2, 10.4, "**Sylvie**", "Cuchillo")
s.beat(3, 11.5, "**rompe**", "Línea se rompe")
s.beat(4, 12.5, "el **multiverso**", "Portal abre")
num(s, "n", 2, "4.1", y=700, out="4.2", size=560)
s.img("k", "a-sylvie.jpg", 540, 780, 460, 640, "4.2", how="slam", frm="L", out="4.3", pos="top")
s.cinta("sy", "SYLVIE · LOKI", "amarillo", top=1230, rot=-5, at="4.2", out="4.3")
s.draw("l2", "M60 820 H1020", "tinta", "4.3", w=70, dur=0.3)
s.draw("l1", "M60 820 H1020", "amarillo", "4.3", w=44, dur=0.3)
s.obj("sp", "splat", 540, 820, 900, 900, ("4.3", .3), how="pop", out="4.4")
s.text("rp", "¡CRAC!", "ono", "amarillo", y=1130, at=("4.3", .3), size=230, rot=-7, hold=0.9, zoom=True)
V(s, "pt", portal(600), 540, 760, "4.4", how="pop", bob="end")
s.cinta("ls", "LÍNEA SAGRADA ROTA", "rojo", top=1230, rot=-5, at="4.4")

# 5 · Spider-Man y Strange
s = ep.scene("Tres: al cine", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 13.7, "**Tres**", "3")
s.beat(2, 14.7, "**Spider-Man**", "Máscara")
s.beat(3, 15.8, "Doctor **Strange**", "Runas")
s.beat(4, 16.6, "al **cine**", "Pantalla")
num(s, "n", 3, "5.1", y=700, out="5.2", size=560, color="rojo")
s.img("sp", "a-spider3.jpg", 540, 640, 860, 483, "5.2", how="slam", frm="L", bob="end", pos="center")
s.img("ru", "a-strange-poster.jpg", 540, 1090, 760, 427, "5.3", how="slam", frm="R", bob="end", pos="center")
pass
s.text("ci", "¡AL CINE!", "ono", "rojo", y=1400, at="5.4", size=200, rot=-6, hold=1.4, misreg=True, zoom=True)

# 6 · Cuatro Fantásticos
s = ep.scene("Cuatro: los 4", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 17.3, "**Cuatro**", "4")
s.beat(2, 18.4, "**Fantásticos**", "Emblema")
s.beat(3, 19.0, "desde **otra** Tierra", "Globo")
num(s, "n", 4, "6.1", y=700, out="6.2", size=560)
s.obj("fe", "fourEmblem", 540, 760, 560, 560, "6.2", how="slam", frm="B", bob="6.3", out="6.3")
V(s, "gl", globe(560, "#00C8E8"), 540, 780, "6.3", how="slam", frm="B", bob="end", rot=-5)
s.cinta("ot", "OTRA TIERRA", "amarillo", top=1230, rot=-5, at="6.3")

# 7 · Thunderbolts
s = ep.scene("Cinco: New Avengers", "S2", bg="papel", enter="ink", color="tinta")
s.beat(1, 20.4, "**Cinco**", "5")
s.beat(2, 21.4, "**Thunderbolts**", "Rayo")
s.beat(3, 22.0, "**convertido**", "Transformación")
s.beat(4, 22.8, "**Avengers**", "NEW AVENGERS")
num(s, "n", 5, "7.1", y=700, out="7.2", size=560, color="rojo")
s.img("bo", "a-thunder.jpg", 540, 780, 430, 640, "7.2", how="slam", frm="T", out="7.3", pos="top")
s.cinta("tb", "THUNDERBOLTS", "amarillo", top=1230, rot=-5, at="7.2", out="7.4")
s.flash("7.3")
for k, f in enumerate(("a-bucky.jpg", "a-yelena.jpg", "a-redguardian.jpg", "a-ghost.jpg", "a-walker.jpg")):
    s.panel(f"na{k}", pho(f, "50% 15%"), 40 + k * 205, 600, 190, 300, ("rojo", "heroe", "ceniza", "multi", "amarillo")[k], rot=(-3, 2, -2, 3, -2)[k], at=("7.4", k * 0.07), frm="T")
s.cinta("na", "NEW AVENGERS", "rojo", top=1100, rot=5, at="7.4")

# 8 · Deadpool y Wolverine
s = ep.scene("Seis: Deadpool y Wolverine", "S2", bg="rojo", enter="halftone", color="rojo", pat="pat-benday-fuerte")
s.beat(1, 23.5, "**seis**", "6")
s.beat(2, 24.3, "**Deadpool**", "Máscara")
s.beat(3, 25.0, "**Wolverine**", "Garras")
s.beat(4, 25.8, "**cruzan**", "Portal")
num(s, "n", 6, "8.1", color="papel", y=700, out="8.2", size=560)
V(s, "dp", dpmask(420), 290, 820, "8.2", how="slam", frm="L", bob="end")
s.img("cl", "a-wolverine.jpg", 790, 820, 400, 430, "8.3", how="slam", frm="R", bob="end", pos="top")
s.cinta("dw", "DEADPOOL Y WOLVERINE", "tinta", top=1230, rot=-5, at="8.3")
V(s, "pt", portal(360), 540, 1380, "8.4", how="pop", bob="end")
s.text("cr", "¡CRUZAN!", "ono", "amarillo", y=560, at="8.4", size=190, rot=-6, hold=1.2, misreg=True, zoom=True)

# 9 · resúmenes
s = ep.scene("Resúmenes", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 27.0, "los **resúmenes**", "Seis fichas")
s.beat(2, 29.6, "antes del **final**", "Claqueta")
s.beat(3, 31.2, "no ves **todo**", "Tachado")
s.beat(4, 32.2, "**quién** es quién", "Fichas con nombre")
for k, (nm, c) in enumerate((("SAM", "heroe"), ("LOKI", "multi"), ("STRANGE", "ciencia"), ("LOS 4", "heroe"), ("NEW AVENGERS", "rojo"), ("DEADPOOL", "ceniza"))):
    s.panel(f"r{k}", '<div class="c" style="position:relative"><span style="font:400 %dpx Anton;color:#FFF3D6;text-align:center;line-height:1">%s</span></div>' % (44 if len(nm) > 8 else 60, nm.replace(" ", "<br>") if len(nm) > 8 else nm), 40 + (k % 2) * 520, 420 + (k // 2) * 330, 480, 290, c, rot=(-2, 2)[k % 2], at=None)
s.code('COM.panelSplit(tl, qa("#v10-e9 .panel"), %s, { dirs: ["L", "R"], gap: 0.12 });' % s.t("9.1"))
s.cap("cap", "6 RESÚMENES", "9.1", top=1450, width=520, out="9.2")
s.obj("cl", "clapper", 540, 820, 700, 700, "9.2", how="slam", frm="B", out="9.3")
s.cinta("ft", "ANTES DEL FINAL", "amarillo", top=1230, rot=-5, at="9.2", out="9.3")
s.text("td", "NO VES TODO", "ttl", "rojo", y=700, at="9.3", size=170, rot=-5, how="stamp", out="9.4", misreg=True)
s.text("qq", "¿QUIÉN ES QUIÉN?", "ono", "amarillo", y=1380, at="9.4", size=150, rot=-6, hold=1.2, misreg=True)

# 10 · tablero
s = ep.scene("El tablero", "S3", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 33.8, "esas **seis** piezas", "Seis piezas")
s.beat(2, 35.1, "en el **tablero**", "Tablero")
s.beat(3, 36.0, "para **Doomsday**", "Doom en el tablero")
for k in range(6):
    s.panel(f"p{k}", '<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:90px">%d</span></div>' % (k + 1), 60 + k * 160, 460, 140, 160, CH[k], rot=(-3, 2)[k % 2], at=None)
s.code('COM.panelSplit(tl, qa("#v10-e10 .panel"), %s, { dirs: ["T"], gap: 0.07 });' % s.t("10.1"))
V(s, "bd", board(640), 540, 960, "10.2", how="slam", frm="B")
s.obj("dm", "doomMask", 540, 930, 220, 270, "10.3", how="drop")
s.text("dd", "¡DOOMSDAY!", "ono", "amarillo", y=1380, at="10.3", size=190, rot=-6, hold=1.5, misreg=True, zoom=True)

# 11 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 37.2, "**Siguiente**", "Portada N.º 11")
s.beat(2, 38.2, "la **lista**", "Lista")
s.beat(3, 39.0, "para **maratonear**", "Cinta")
s.cover("cover", 11, "multi-osc", cover_in(listicon(330), 450, 600), at="11.1", frm="R")
s.text("q", "LA LISTA<br>DEFINITIVA", "ttl", "amarillo", x=540, y=1190, at="11.2", size=82, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1310, rot=-8, at="11.3")
