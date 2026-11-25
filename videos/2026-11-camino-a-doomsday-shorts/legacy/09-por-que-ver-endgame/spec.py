from lib import *

ep = Episode(9, "por-que-ver-endgame", "¿Por qué ver Endgame antes de Doomsday?", 114, cont_in="2.1", cont_pulse="9.1")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def cover_in(svg, x=450, y=640): return f'<div class="c" style="left:{x}px;top:{y}px">{svg}</div>'
LOGO = lambda w, h: '<div class="c" style="position:relative"><img src="' + IMG + 'endgame-logo.png" style="width:%dpx;height:%dpx;object-fit:contain" /></div>' % (w, h)
CLOCK = ('<circle cx="150" cy="150" r="130" fill="#FFF3D6" stroke="#0B0B14" stroke-width="10"/><path d="M150 150 V60 M150 150 L215 190" stroke="#0B0B14" stroke-width="14" stroke-linecap="round"/><circle cx="150" cy="150" r="14" fill="#E8212B" stroke="#0B0B14" stroke-width="6"/>')

# 1 · portada
s = ep.scene("Portada", "S1", bg="ceniza", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 09: Endgame")
s.beat(2, 0.45, "Los **mismos** directores", "¡LOS MISMOS!")
s.beat(3, 1.0, "**directores**", "CAP DIRECTORES")
s.cover("cover", 9, "tinta", cover_in('<div style="background:#FFF3D6;border:8px solid #0B0B14;padding:10px;box-sizing:border-box;width:640px;height:260px">' + '<img src="' + IMG + 'endgame-logo.png" style="width:100%;height:100%;object-fit:contain" /></div>', 450, 640), at="1.1", frm="T")
s.cinta("cinta", "LOS MISMOS DIRECTORES", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=28, seed=2)
s.text("lm", "¡LOS MISMOS!", "ono", "amarillo", y=860, at="1.2", size=190, rot=-7, hold=0.8, misreg=True)
s.cap("cap", "DE ENDGAME", "1.3", width=520)

# 2 · casualidad
s = ep.scene("No es casualidad", "S1", bg="papel", enter="halftone", color="papel")
s.beat(1, 1.9, "hacen **Doomsday**", "Logo")
s.beat(2, 3.0, "es **casualidad**", "¿CASUALIDAD? NO")
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:700px;height:300px;object-fit:contain" /></div>', 90, 430, 900, 420, "papel", rot=-2, at="2.1", frm="T")
s.text("ca", "¿CASUALIDAD?", "ttl", "tinta", y=1050, at="2.2", size=150, rot=-4, how="stamp")
s.obj("fx", "xMark", 540, 1050, 760, 360, ("2.2", .3), how="stamp")
s.text("no", "¡NO!", "ono", "rojo", y=1330, at=("2.2", .4), size=240, rot=-7, hold=1.0, zoom=True)

# 3 · Russo
s = ep.scene("Los Russo", "S2", bg="ciencia", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 3.8, "**Anthony** y Joe", "Silla ANTHONY")
s.beat(2, 4.7, "y **Joe**", "Silla JOE")
s.beat(3, 5.7, "**Infinity** War", "INFINITY WAR")
s.beat(4, 6.7, "y **Endgame**", "Logo Endgame")
s.beat(5, 7.5, "**vuelven**", "Flecha de regreso")
s.img("c1", "a-russo.jpg", 540, 770, 560, 590, "3.1", how="slam", frm="L", pos="top", bob="end")
pass
s.cinta("an", "ANTHONY RUSSO", "amarillo", top=1090, rot=-5, at="3.1")
s.cinta("jo", "JOE RUSSO", "rojo", top=1200, rot=5, at="3.2")
s.panel("iw", '<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:110px;text-align:center;line-height:1">INFINITY<br>WAR</span></div>', 40, 420, 460, 280, "papel", rot=-3, at="3.3", frm="T")
s.panel("eg", LOGO(420, 200), 580, 420, 460, 280, "papel", rot=3, at="3.4", frm="T")
s.text("vu", "¡VUELVEN!", "ono", "amarillo", y=1410, at="3.5", size=150, rot=-6, hold=1.2, misreg=True, zoom=True)

# 4 · tres cosas
s = ep.scene("Tres cosas clave", "S2", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 8.6, "**tres** cosas", "3")
s.beat(2, 10.0, "el **viaje**", "Reloj")
s.beat(3, 11.8, "la muerte de **Tony**", "Reactor apagado")
s.beat(4, 13.5, "el **escudo**", "Escudo")
s.beat(5, 14.6, "de **Sam**", "SAM")
s.text("n3", "3", "kw", "amarillo", y=800, at="4.1", size=700, rot=-5, how="stamp", out="4.2", misreg=True)
V(s, "ck", '<svg viewBox="0 0 300 300" style="width:560px;height:560px;overflow:visible">' + CLOCK + '</svg>', 540, 800, "4.2", how="slam", frm="B", out="4.3")
s.cinta("vi", "VIAJE EN EL TIEMPO", "amarillo", top=1230, rot=-5, at="4.2", out="4.3")
s.img("ar", "a-ironman.jpg", 540, 780, 400, 760, "4.3", how="pop", out="4.4", pos="top")
s.cinta("to", "TONY STARK", "rojo", top=1230, rot=-5, at="4.3", out="4.4")
s.img("sh", "a-samcap.jpg", 540, 780, 480, 690, "4.4", how="slam", frm="R", bob="end", pos="top")
s.cinta("sa", "EL ESCUDO DE SAM", "amarillo", top=1230, rot=-5, at="4.5")

# 5 · el Anciano
s = ep.scene("El Anciano avisa", "S2", bg="multi", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 16.0, "el **Anciano**", "EL ANCIANO")
s.beat(2, 17.0, "**Bruce** Banner", "BRUCE BANNER")
s.beat(3, 18.2, "el **pasado**", "Línea hacia atrás")
s.beat(4, 19.3, "**ramas** nuevas", "Ramas")
s.panel("an", pho("a-ancient.jpg", "50% 15%", "EL ANCIANO", 60), 40, 420, 450, 640, "multi-osc", rot=-3, at="5.1", frm="L")
s.globo("ad", "¡CUIDADO!", 380, 400, 460, 220, "5.1", size=60, rot=3, out="5.3")
s.panel("bb", pho("a-bruce.jpg", "50% 15%", "BRUCE BANNER", 56), 590, 420, 450, 640, "ceniza", rot=3, at="5.2", frm="R")
s.draw("pa2", "M980 1200 H100", "tinta", "5.3", w=60, dur=0.4)
s.draw("pa", "M980 1200 H100", "amarillo", "5.3", w=36, dur=0.4)
s.cinta("pas", "CAMBIAR EL PASADO", "amarillo", top=1280, rot=-4, at="5.3", out="5.4")
V(s, "br", branches(1000, 560), 540, 1230, "5.4", how="slide", frm="L")

# 6 · semilla
s = ep.scene("La semilla", "S2", bg="multi-osc", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 20.7, "la **semilla**", "Semilla")
s.beat(2, 21.7, "del **multiverso**", "Árbol/portal")
s.raw('<div class="c" id="v09-e6-sm" style="left:540px;top:1100px"><div style="width:140px;height:190px;background:#FFD400;border:10px solid #0B0B14;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%"></div></div>', 'COM.dropIn(tl, q("#v09-e6-sm"), %s, { from: -1300 });\nCOM.popOut(tl, q("#v09-e6-sm"), %s);' % (s.t("6.1"), s.t(("6.2", .1))))
s.text("se", "SEMILLA", "ttl", "amarillo", x=360, y=480, at="6.1", size=190, rot=-5, how="stamp", misreg=True)
V(s, "tr", tree(640, 770), 540, 920, "6.2", how="pop", bob="end")
s.flash("6.2")
s.cinta("mv", "EL MULTIVERSO", "amarillo", top=1330, rot=-5, at="6.2")

# 7 · capítulo anterior
s = ep.scene("Capítulo anterior", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 23.2, "el **capítulo** anterior", "Cómic abierto")
s.beat(2, 24.8, "un **final** de temporada", "Claqueta")
s.beat(3, 26.5, "si no lo **viste**", "Ojo tachado")
s.beat(4, 27.7, "a la **mitad**", "Medidor al 50%")
s.obj("cm", "comicOpen", 540, 800, 760, 600, "7.1", how="slam", frm="B", rot=-4, out="7.2")
s.cinta("cp", "CAPÍTULO ANTERIOR", "rojo", top=1230, rot=-5, at="7.1", out="7.2")
s.obj("cl", "clapper", 540, 800, 680, 680, "7.2", how="slam", frm="R", out="7.3")
s.cinta("ft", "FINAL DE TEMPORADA", "amarillo", top=1230, rot=-5, at="7.2", out="7.3")
V(s, "ey", eye(700), 540, 780, "7.3", how="pop", out="7.4")
s.obj("fx", "xMark", 540, 780, 640, 640, ("7.3", .25), how="stamp", out="7.4")
s.cinta("nv", "NO LO VISTE", "rojo", top=1230, rot=-5, at="7.3", out="7.4")
s.raw('<div class="c" id="v09-e7-me" style="left:540px;top:780px"><div style="width:640px;height:140px;background:#FFF3D6;border:10px solid #0B0B14;box-shadow:10px 10px 0 #0B0B14;position:relative"><div style="position:absolute;left:0;top:0;bottom:0;width:50%;background:#E8212B;border-right:10px solid #0B0B14"></div></div></div>', 'COM.panelSlam(tl, q("#v09-e7-me"), %s, { from: "L", rot: 3 });' % s.t("7.4"))
s.text("mi", "50 %", "ttl", "tinta", y=1000, at="7.4", size=280, rot=-4, how="stamp", misreg=True)
s.cinta("em", "LA EMOCIÓN, A LA MITAD", "amarillo", top=1230, rot=-5, at="7.4")

# 8 · cara de Tony
s = ep.scene("La cara de Tony", "S3", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 29.9, "la **cara** de Tony", "Casco de Iron Man")
s.beat(2, 32.0, "convertida en **villano**", "Máscara de Doom")
s.beat(3, 33.2, "necesitas **recordar**", "Nube RECUERDA")
s.beat(4, 34.2, "lo que **costó**", "Reactor y LO QUE COSTÓ")
s.img("ir", "iron-mask.png", 540, 830, 560, 660, "8.1", how="slam", frm="B", pos="center", out="8.2")
s.img("dm", "doom-mask.png", 540, 830, 560, 660, "8.2", how="slam", frm="R", pos="center", out="8.3")
s.flash("8.2")
s.text("vi", "¡VILLANO!", "ono", "amarillo", y=1330, at="8.2", size=220, rot=-6, hold=1.0, misreg=True, zoom=True, out="8.3")
s.globo("re", "RECUERDA", 280, 420, 520, 330, "8.3", kind="nube", size=62, out="8.4")
s.obj("ar", "arcReactor", 540, 820, 500, 500, "8.4", how="pop", bob="end")
s.text("co", "¿LO QUE COSTÓ?", "ttl", "amarillo", y=1260, at="8.4", size=100, rot=-4, how="stamp", misreg=True)

# 9 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 35.6, "**Siguiente**", "Portada N.º 10")
s.beat(2, 36.5, "lo que **pasó**", "Calendario")
s.beat(3, 37.0, "desde **entonces**", "Cinta")
s.cover("cover", 10, "multi-osc", '<div class="c" style="left:450px;top:600px"><div data-com="calendar" style="width:300px;height:320px"></div></div>', at="9.1", frm="R")
s.text("q", "¿QUÉ PASÓ DESDE<br>ENDGAME?", "ttl", "amarillo", x=540, y=1190, at="9.2", size=70, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1290, rot=-8, at="9.3")
