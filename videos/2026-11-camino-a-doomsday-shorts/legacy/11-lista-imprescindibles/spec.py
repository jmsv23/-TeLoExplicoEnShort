from lib import *

ep = Episode(11, "lista-imprescindibles", "Los 8 títulos imprescindibles antes de Doomsday", 115, cont_in="2.1", cont_pulse="14.2")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def cover_in(svg, x=450, y=640): return f'<div class="c" style="left:{x}px;top:{y}px">{svg}</div>'
def num(s, name, n, at, color="amarillo", y=760, x=270, size=520):
    s.text(name, str(n), "kw", color, x=x, y=y, at=at, size=size, rot=-5, how="stamp", misreg=True)
def tag(s, name, txt, at, color="amarillo", top=1230, rot=-5, out=None):
    s.cinta(name, txt, color, top=top, rot=rot, at=at, out=out)
LISTCOVER = cover_in(listicon(330), 450, 600)

# 1 · portada
s = ep.scene("Portada", "S1", bg="multi", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 11: lista")
s.beat(2, 1.3, "un **fin** de semana", "UN FIN DE SEMANA")
s.cover("cover", 11, "multi-osc", LISTCOVER, at="1.1", frm="T")
s.cinta("cinta", "LOS 8 IMPRESCINDIBLES", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=28, seed=2)
s.cap("cap", "UN FIN DE SEMANA", "1.2", width=640)
s.zoom("1.2", 1.1)

# 2 · ocho
s = ep.scene("Ocho títulos", "S1", bg="papel", enter="halftone", color="papel")
s.beat(1, 3.4, "los **ocho** títulos", "8")
s.beat(2, 5.1, "que de verdad **importan**", "IMPORTAN")
s.beat(3, 6.6, "antes de **Doomsday**", "Logo")
s.text("n8", "8", "kw", "rojo", y=760, at="2.1", size=760, rot=-5, how="stamp", out="2.2", misreg=True)
s.slab("ro", "rojo", "2.2", ("2.2", 1.2))
s.text("im", "IMPORTAN", "ono", "amarillo", y=820, at="2.2", size=220, rot=-6, hold=1.3, misreg=True, zoom=True)
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:700px;height:300px;object-fit:contain" /></div>', 90, 1000, 900, 400, "papel", rot=-2, at="2.3", frm="B")

ROW = [  # n, scene name, bg, numcolor, beats[(anchor-phrase, est, desc)]
    (1, "Uno: Endgame", "heroe", "amarillo", 7.8, [("**Uno**", 7.8, "1"), ("**Endgame**", 8.5, "Logo")]),
    (2, "Dos: Loki", "multi", "amarillo", 9.1, [("**Dos**", 9.1, "2"), ("**Loki**", 9.8, "Casco"), ("**temporadas**", 10.6, "T1 + T2")]),
    (3, "Tres: Strange", "papel", "rojo", 12.0, [("**Tres**", 12.0, "3"), ("**Strange**", 13.0, "Runas"), ("**locura**", 14.7, "Portal")]),
    (4, "Cuatro: Spider-Man", "ciencia", "rojo", 15.8, [("**Cuatro**", 15.8, "4"), ("**Spider-Man**", 16.7, "Máscara"), ("**casa**", 18.2, "Sin camino a casa")]),
    (5, "Cinco: Los 4", "heroe", "amarillo", 19.0, [("**Cinco**", 19.0, "5"), ("**Fantásticos**", 20.0, "Emblema"), ("**First**", 21.0, "First Steps")]),
    (6, "Seis: Thunderbolts", "rojo", "papel", 22.0, [("**Seis**", 22.0, "6"), ("**Thunderbolts**", 22.7, "Rayo")]),
    (7, "Siete: Capitán", "multi", "amarillo", 23.6, [("**Siete**", 23.6, "7"), ("**Capitán**", 24.5, "Escudo"), ("**nuevo**", 25.6, "Un nuevo mundo")]),
    (8, "Ocho: Deadpool y Wolverine", "ceniza", "amarillo", 26.6, [("**ocho**", 26.6, "8"), ("**Deadpool**", 27.3, "Máscara"), ("**Wolverine**", 28.2, "Garras")]),
]
for n, nm, bg, nc, t0, bs in ROW:
    s = ep.scene(nm, "S2", bg=bg, enter=("ink" if n % 2 else "pageflip"), color=("tinta" if n % 2 else "papel"), pat="pat-benday-fuerte" if n % 2 else "pat-benday")
    for i, (a, t, d) in enumerate(bs, 1):
        s.beat(i, t, a, d)
    num(s, "n", n, "%d.1" % (2 + n), color=nc)
    k = 2 + n
    a2, a3 = f"{k}.2", f"{k}.3"
    if n == 1:
        s.panel("t", '<div class="c" style="position:relative"><img src="' + IMG + 'endgame-logo.png" style="width:440px;height:200px;object-fit:contain" /></div>', 520, 520, 520, 500, "papel", rot=3, at=a2, frm="R")
        tag(s, "tg", "EL PUNTO DE PARTIDA", a2)
    elif n == 2:
        s.img("h", "a-loki.jpg", 800, 760, 360, 450, a2, how="slam", frm="R", bob="end", pos="top")
        tag(s, "tg", "TEMPORADAS 1 Y 2", a3)
    elif n == 3:
        s.img("r", "a-strange.jpg", 800, 760, 340, 460, a2, how="slam", frm="R", bob="end", pos="top")
        s.text("lo", "¡LA LOCURA!", "ono", "amarillo", x=640, y=1180, at=a3, size=130, rot=-6, hold=1.2)
        tag(s, "tg", "DOCTOR STRANGE", a2, top=1350)
    elif n == 4:
        s.img("s", "a-spider3.jpg", 790, 760, 460, 258, a2, how="slam", frm="R", bob="end", pos="center")
        tag(s, "tg", "SIN CAMINO A CASA", a3)
    elif n == 5:
        s.img("fe", "a-fantastic4.jpg", 790, 760, 460, 345, a2, how="slam", frm="R", bob="end", pos="center")
        tag(s, "tg", "FIRST STEPS", a3)
    elif n == 6:
        s.img("bo", "a-thunder.jpg", 800, 780, 330, 490, a2, how="slam", frm="R", bob="end", pos="top")
        tag(s, "tg", "THUNDERBOLTS", a2)
    elif n == 7:
        s.img("sh", "a-brave.jpg", 800, 760, 330, 490, a2, how="slam", frm="R", bob="end", pos="top")
        tag(s, "tg", "UN NUEVO MUNDO", a3)
    else:
        V(s, "dp", dpmask(320), 740, 760, a2, how="slam", frm="R", bob="end")
        s.img("cl", "a-wolverine.jpg", 900, 1060, 280, 300, a3, how="slam", frm="B", bob="end", pos="top")
        tag(s, "tg", "DEADPOOL Y WOLVERINE", a3)

# 11 · y lo demás
s = ep.scene("¿Y lo demás?", "S2", bg="ceniza", enter="halftone", color="ceniza")
s.beat(1, 29.7, "¿Y lo **demás**?", "¿?")
s.text("q", "¿Y LO<br>DEMÁS?", "ttl", "amarillo", y=820, at="11.1", size=260, rot=-5, how="stamp", misreg=True, zoom=True)
s.obj("x", "xMark", 540, 1250, 260, 260, ("11.1", .5), how="pop") if False else None

# 12 · saltarse
s = ep.scene("Puedes saltarte", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 31.2, "Puedes **saltarte**", "Flecha de salto")
s.beat(2, 32.4, "**Eternals**", "ETERNALS")
s.beat(3, 33.3, "**Black** Widow", "BLACK WIDOW")
s.beat(4, 34.2, "**Hawkeye**", "HAWKEYE")
s.beat(5, 35.0, "el **hilo**", "Hilo sin cortar")
s.text("sa", "SALTA", "ono", "rojo", y=1480, at="12.1", size=140, rot=-6, hold=1.0)
for k, (nm, at) in enumerate((("ETERNALS", "12.2"), ("BLACK WIDOW", "12.3"), ("HAWKEYE", "12.4"))):
    s.panel(f"e{k}", '<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:%dpx;opacity:.55">%s</span></div>' % (110 if len(nm) < 9 else 84, nm), 60, 430 + k * 270, 960, 240, "ceniza", rot=(-1.5, 1.5, -1)[k], at=at, frm=("L", "R", "L")[k])
    s.obj(f"x{k}", "xMark", 540, 550 + k * 270, 960, 200, (at, .22), how="stamp")
s.draw("hl2", "M60 1330 C300 1250 500 1410 1020 1330", "tinta", "12.5", w=34, dur=0.5)
s.draw("hl", "M60 1330 C300 1250 500 1410 1020 1330", "amarillo", "12.5", w=18, dur=0.5)
s.cinta("hi", "SIN PERDER EL HILO", "amarillo", top=1410, rot=-4, at="12.5")

# 13 · alineación
s = ep.scene("Alineación titular", "S3", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 36.3, "una **alineación** titular", "8 jugadores")
s.beat(2, 38.4, "**ocho** jugadores", "TITULARES")
s.beat(3, 40.0, "es **banca**", "BANCA")
for k in range(8):
    s.panel(f"j{k}", Scene.pobj("faceless", 90, 120) + '<div class="c" style="position:relative"><span style="font:400 50px Anton;color:#0B0B14">%d</span></div>' % (k + 1), 55 + (k % 4) * 240, 430 + (k // 4) * 300, 220, 270, ("papel", "amarillo")[k % 2], rot=(-3, 2, -2, 3)[k % 4], at=None)
s.code('COM.panelSplit(tl, qa("#v11-e13 .panel"), %s, { dirs: ["T", "B"], gap: 0.06 });' % s.t("13.1"))
s.text("ti", "8 TITULARES", "ttl", "amarillo", y=1130, at="13.2", size=150, rot=-4, how="stamp", misreg=True)
for k in range(4):
    s.panel(f"b{k}", Scene.pobj("faceless", 70, 90), 140 + k * 200, 1250, 150, 190, "ceniza", rot=(-2, 2)[k % 2], at=("13.3", k * 0.07), frm="B")
s.cinta("bn", "EL RESTO ES BANCA", "rojo", top=1450, rot=-4, at="13.3")

# 14 · estreno
s = ep.scene("El estreno", "S3", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 41.4, "**Ocho** títulos", "8")
s.beat(2, 43.0, "el **dieciocho**", "Calendario")
s.beat(3, 44.4, "nada **importante**", "Palomita")
s.text("n8", "8", "kw", "amarillo", y=800, at="14.1", size=700, rot=-5, how="stamp", misreg=True)
s.code('COM.popOut(tl, q("#v11-e14-n8"), %s - 0.05);' % s.t("14.2"))
s.obj("cal", "calendar", 540, 800, 520, 560, "14.2", how="drop", bob="14.3", out="14.3")
s.text("fe", "18 DE DICIEMBRE", "ttl", "amarillo", y=1250, at="14.2", size=100, rot=-4, how="stamp", out="14.3")
V(s, "ck", check(520), 540, 800, "14.3", how="slam", frm="B", bob="end")
s.cinta("nn", "SIN PERDERTE NADA", "amarillo", top=1230, rot=-5, at="14.3")

# 15 · CTA
s = ep.scene("Cierre", "S4", bg="multi", enter="halftone", color="multi")
s.beat(1, 45.7, "**Guarda** este video", "Disquete")
s.beat(2, 46.7, "tu **maratón**", "Cinta")
s.beat(3, 47.6, "en el **cine**", "Portada final")
V(s, "fl", floppy(520), 540, 800, "15.1", how="slam", frm="B", bob="15.3", out="15.3")
s.text("g", "GUÁRDALO", "ono", "amarillo", y=1250, at="15.1", size=200, rot=-6, hold=1.8, misreg=True, out="15.3")
s.cinta("ma", "TU MARATÓN", "rojo", top=1060, rot=-5, at="15.2", out="15.3")
s.cover("cover", 11, "multi-osc", LISTCOVER, at="15.3", frm="T")
s.cinta("cine", "NOS VEMOS EN EL CINE", "amarillo", top=1190, rot=-8, at="15.3")
