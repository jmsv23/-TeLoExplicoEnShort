from lib import *

ep = Episode(8, "x-men-centinelas", "Los X-Men en Doomsday", 126, cont_in="2.1", cont_pulse="10.3")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def cover_in(svg, x=450, y=640): return f'<div class="c" style="left:{x}px;top:{y}px">{svg}</div>'
PX, MG, CY, BE, NC, MY, GA = "PROFESOR X", "MAGNETO", "CÍCLOPE", "BESTIA", "RONDADOR", "MÍSTICA", "GAMBIT"
def ico(k, w=240):
    if k == PX: return eye(w)
    if k == MG: return magnet(int(w * .8))
    if k == CY: return visor(w)
    if k == BE: return '<div class="c" style="position:relative"><div data-com="gearAtom" style="width:%dpx;height:%dpx"></div></div>' % (w, w)
    if k == NC: return smoke(w)
    if k == MY: return Scene.pobj("faceless", int(w * .6), int(w * .75))
    return card(int(w * .7))
BG = {PX: "multi", MG: "rojo", CY: "heroe", BE: "ciencia", NC: "multi-osc", MY: "ceniza", GA: "amarillo"}
TXT = {PX: "papel", MG: "papel", CY: "papel", BE: "tinta", NC: "papel", MY: "papel", GA: "tinta"}
PH = {PX: "a-xavier.jpg", MG: "a-magneto.jpg", CY: "a-ciclope.jpg", BE: "a-bestia.jpg", NC: "a-nightcrawler.jpg", MY: "a-mistica.jpg", GA: "a-gambit.jpg"}
def chip(s, name, k, l, t, w, h, at, frm="B", rot=0, isz=None):
    if k in PH:
        s.panel(name, pho(PH[k], "50% 20%", k, 44 if w < 360 else 62), l, t, w, h, BG[k], rot=rot, at=at, frm=frm)
        return
    s.panel(name, ico(k, isz or int(min(w, h) * 0.7)) + Scene.plabel(k, TXT[k], 44 if w < 260 else 62, 14), l, t, w, h, BG[k], rot=rot, at=at, frm=frm)

# 1 · portada (los cinco)
s = ep.scene("Portada", "S1", bg="heroe", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 08: X")
s.beat(2, 0.2, "**Profesor** X", "PROFESOR X")
s.beat(3, 1.0, "**Magneto**", "MAGNETO")
s.beat(4, 1.6, "**Cíclope**", "CÍCLOPE")
s.beat(5, 2.2, "**Bestia**", "BESTIA")
s.beat(6, 2.7, "**Rondador** Nocturno", "RONDADOR NOCTURNO")
s.cover("cover", 8, "tinta", cover_in(xlogo(280), 450, 520), at="1.1", frm="T")
s.cinta("cinta", "LOS X-MEN ORIGINALES", "amarillo", top=1450, rot=-6, at="1.1")
for k, (nm, at, y) in enumerate(((PX, "1.2", 930), (MG, "1.3", 1000), (CY, "1.4", 1070), (BE, "1.5", 1140), (NC, "1.6", 1210))):
    s.text(f"n{k}", nm, "ttl", "papel", x=540, y=y + 130, at=at, size=62, rot=(-3, 2, -2, 3, -2)[k], how="pop")
s.speed("sl", "1.2", n=26, seed=2)

# 2 · originales
s = ep.scene("Los originales", "S1", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 3.8, "los X-Men **originales**", "Cinco íconos")
s.beat(2, 4.8, "de **Fox**", "FOX")
s.beat(3, 5.7, "**Doomsday**", "Logo")
for k, (nm, x, y) in enumerate(((PX, 40, 420), (MG, 370, 420), (CY, 700, 420), (BE, 205, 800), (NC, 535, 800))):
    chip(s, f"c{k}", nm, x, y, 320, 340, ("2.1", k * 0.09), frm=("T", "T", "T", "B", "B")[k], rot=(-3, 2, -2, 3, -2)[k])
s.cinta("fox", "DE FOX", "amarillo", top=1230, rot=-5, at="2.2")
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:700px;height:280px;object-fit:contain" /></div>', 90, 1260, 900, 280, "papel", rot=-2, at="2.3", frm="B")

# 3 · reunión imposible
s = ep.scene("Reunión imposible", "S2", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 6.5, "una **reunión**", "Grupo")
s.beat(2, 7.6, "parecía **imposible**", "¡IMPOSIBLE!")
for k, x in enumerate((150, 345, 540, 735, 930)):
    s.panel(f"f{k}", pho(("a-xavier.jpg", "a-magneto.jpg", "a-ciclope.jpg", "a-bestia.jpg", "a-nightcrawler.jpg")[k], "50% 20%"), x - 95, 620, 190, 260, "papel", rot=(-3, 2, -2, 3, -2)[k], at=("3.1", k * 0.07), frm="B")
s.cinta("reu", "LA REUNIÓN", "amarillo", top=1000, rot=-5, at="3.1")
s.text("imp", "¡IMPOSIBLE!", "ono", "amarillo", y=1260, at="3.2", size=200, rot=-6, hold=1.4, misreg=True, zoom=True)

# 4 · derechos
s = ep.scene("Los derechos", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 9.3, "los **derechos**", "Contrato")
s.beat(2, 10.6, "de los **mutantes**", "X")
s.beat(3, 11.8, "**Disney** compró", "DISNEY")
s.beat(4, 12.7, "**Fox**", "FOX")
s.beat(5, 13.6, "dos mil **diecinueve**", "2019")
s.obj("ct", "contract", 300, 780, 440, 540, "4.1", how="drop", out="4.2")
s.obj("xl", "contract", 300, 780, 1, 1, "4.1", how="pop") if False else None
V(s, "xx", xlogo(380), 540, 800, "4.2", how="slam", frm="B", out="4.3")
s.panel("di", '<div class="c" style="position:relative"><img src="' + IMG + 'a-disney.jpg" style="width:400px;height:230px;object-fit:contain" /></div>', 40, 520, 460, 260, "papel", rot=-3, at="4.3", frm="L")
s.panel("fx", '<div class="c" style="position:relative"><img src="' + IMG + 'a-fox.jpg" style="width:400px;height:230px;object-fit:contain" /></div>', 580, 520, 460, 260, "papel", rot=3, at="4.4", frm="R")
s.draw("ar", "M560 650 C520 650 520 650 500 650", "rojo", "4.4", w=22, dur=0.3)
s.text("ano", "2019", "ttl", "rojo", y=1150, at="4.5", size=360, rot=-5, how="stamp", misreg=True, zoom=True)
s.cinta("cp", "DISNEY COMPRÓ FOX", "tinta", top=1400, rot=-4, at="4.5")

# 5 · terreno
s = ep.scene("Preparando el terreno", "S2", bg="ceniza", enter="pageflip", color="ceniza")
s.beat(1, 14.4, "fue **preparando**", "PREPARANDO")
s.beat(2, 15.4, "el **terreno**", "EL TERRENO")
s.text("pr", "PREPARANDO", "ttl", "amarillo", y=700, at="5.1", size=170, rot=-5, how="stamp", out="5.2")
s.obj("g", "gearAtom", 540, 1000, 400, 400, "5.1", how="pop", out="5.2")
V(s, "bd", building(700), 540, 780, "5.2", how="drop")
s.text("te", "EL TERRENO", "ttl", "tinta", y=1250, at="5.2", size=170, rot=-4, how="stamp")

# 6 · Xavier en Strange
s = ep.scene("Xavier en Strange", "S2", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 16.8, "ya **apareció**", "Profesor X")
s.beat(2, 18.4, "como **Xavier**", "XAVIER")
s.beat(3, 19.6, "Doctor **Strange**", "Runas")
s.beat(4, 20.9, "de la **locura**", "Portal loco")
chip(s, "px", PX, 90, 420, 420, 520, "6.1", frm="L", rot=-3, isz=330)
s.cinta("xv", "XAVIER", "amarillo", top=1050, rot=-5, at="6.2")
s.panel("ru", pho("a-strange.jpg", "50% 10%", "STRANGE", 60), 570, 420, 420, 520, "multi-osc", rot=3, at="6.3", frm="R")
V(s, "pt", portal(360), 540, 1280, "6.4", how="pop", bob="end")
s.text("lo", "¡LA LOCURA!", "ono", "amarillo", y=1210, at="6.4", size=140, rot=-6, hold=1.2, misreg=True)

# 7 · se suman
s = ep.scene("Se suman", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 21.9, "se **suman**", "SE SUMAN")
s.beat(2, 23.2, "**Ian** McKellen", "Magneto")
s.beat(3, 24.3, "**James** Marsden", "Cíclope")
s.beat(4, 25.4, "**Alan** Cumming", "Rondador")
s.beat(5, 26.3, "**Kelsey** Grammer", "Bestia")
s.beat(6, 27.1, "**Rebecca** Romijn", "Mística")
s.beat(7, 27.8, "**Channing** Tatum", "Gambit")
s.text("sm", "SE SUMAN", "ttl", "amarillo", y=700, at="7.1", size=200, rot=-5, how="stamp", out="7.2", misreg=True)
for k, (nm, at) in enumerate(((MG, "7.2"), (CY, "7.3"), (NC, "7.4"), (BE, "7.5"), (MY, "7.6"), (GA, "7.7"))):
    chip(s, f"c{k}", nm, 40 + (k % 3) * 345, 440 + (k // 3) * 480, 320, 440, at, frm=("L", "T", "R")[k % 3], rot=(-3, 2, -2)[k % 3], isz=230)
s.zoom("7.7", 1.1)

# 8 · otra Tierra
s = ep.scene("De otra Tierra", "S2", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 28.1, "**Todos** vienen", "Los siete")
s.beat(2, 29.1, "de otra **Tierra**", "Otra Tierra")
V(s, "gl", globe(560, "#00C8E8"), 540, 800, "8.2", how="slam", frm="B", bob="end", rot=-5)
s.text("to", "TODOS", "ttl", "amarillo", y=700, at="8.1", size=300, rot=-5, how="stamp", out="8.2", misreg=True)
s.cinta("ot", "DE OTRA TIERRA", "amarillo", top=1260, rot=-5, at="8.2")

# 9 · banda
s = ep.scene("La banda", "S2", bg="papel", enter="halftone", color="papel")
s.beat(1, 30.8, "tu **banda** favorita", "Micrófono")
s.beat(2, 33.5, "**reunida**", "¡REUNIDA!")
s.beat(3, 34.6, "de **gira**", "DE GIRA")
s.beat(4, 35.6, "la banda **nueva**", "Banda nueva")
V(s, "mc", mic(420), 540, 780, "9.1", how="slam", frm="B", bob="9.2", out="9.2")
s.cinta("bf", "TU BANDA FAVORITA", "rojo", top=1250, rot=-5, at="9.1", out="9.2")
for k, x in enumerate((200, 370, 540, 710, 880)):
    s.panel(f"b{k}", pho(("a-xavier.jpg", "a-magneto.jpg", "a-ciclope.jpg", "a-bestia.jpg", "a-nightcrawler.jpg")[k], "50% 20%"), x - 80, 560, 160, 210, "ceniza", rot=(-3, 2, -2, 3, -2)[k], at=("9.2", k * 0.06), frm="B")
s.text("re", "¡REUNIDA!", "ono", "amarillo", y=1000, at="9.2", size=190, rot=-6, hold=1.2, misreg=True)
s.cinta("gi", "DE GIRA", "tinta", top=1250, rot=4, at="9.3")
s.panel("nb", pho("a-cap.jpg", "50% 20%", "BANDA NUEVA", 52), 300, 1060, 480, 340, "heroe", rot=-3, at="9.4", frm="R")

# 10 · comparten pantalla
s = ep.scene("Misma pantalla", "S3", bg="heroe", enter="pageflip", color="heroe")
s.beat(1, 36.8, "**Mutantes**", "X")
s.beat(2, 37.8, "y **Avengers**", "Escudo")
s.beat(3, 38.5, "**pantalla**", "Pantalla")
s.panel("mu", Scene.pobj("faceless", 1, 1) + '<div class="c" style="position:relative"><div style="width:260px;height:260px">' + xlogo(260) + '</div></div>' + Scene.plabel("MUTANTES", "tinta", 70, 22), 40, 420, 470, 640, "amarillo", rot=-3, at="10.1", frm="L")
s.panel("av", pho("a-cap.jpg", "50% 15%", "AVENGERS", 70), 570, 420, 470, 640, "#14378F", rot=3, at="10.2", frm="R")
s.obj("sc", "cinemaScreen", 540, 1240, 760, 540, "10.3", how="slam", frm="B")
s.text("ju", "¡JUNTOS!", "ono", "amarillo", y=800, at="10.3", size=240, rot=-6, hold=1.2, misreg=True, zoom=True)

# 11 · multiverso abierto
s = ep.scene("Multiverso abierto", "S3", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 39.8, "el **multiverso** abierto", "Portal")
s.beat(2, 41.0, "**nadie** sabe", "¿?")
s.beat(3, 41.9, "**cuántos**", "Siluetas")
s.beat(4, 42.5, "pueden **llegar**", "Salen del portal")
V(s, "pt", portal(640), 540, 720, "11.1", how="pop", bob="end")
s.text("q", "¿?", "kw", "amarillo", y=720, at="11.2", size=500, rot=-6, how="stamp", out="11.3")
for k, x in enumerate((230, 410, 670, 850)):
    s.panel(f"s{k}", Scene.pobj("faceless", 110, 140), x - 80, 1150, 160, 220, ("heroe", "rojo", "doom", "ceniza")[k], rot=(-3, 2, -2, 3)[k], at=("11.3", k * 0.1) if k < 2 else ("11.4", (k - 2) * 0.1), frm="T")
s.cinta("cu", "¿CUÁNTOS MÁS?", "amarillo", top=1420, rot=-5, at="11.3")

# 12 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 43.3, "**Siguiente**", "Portada N.º 09")
s.beat(2, 44.1, "hay que **volver**", "Volver")
s.beat(3, 44.9, "ver **Endgame**", "Cinta")
s.cover("cover", 9, "multi-osc", '<div class="c" style="left:450px;top:590px"><img src="' + IMG + 'endgame-logo.png" style="width:640px;height:260px;object-fit:contain;background:#FFF3D6;border:8px solid #0B0B14;box-sizing:border-box;padding:10px" /></div>', at="12.1", frm="R")
s.text("q", "¿POR QUÉ VOLVER<br>A VER ENDGAME?", "ttl", "amarillo", x=540, y=1190, at="12.2", size=70, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1290, rot=-8, at="12.3")
