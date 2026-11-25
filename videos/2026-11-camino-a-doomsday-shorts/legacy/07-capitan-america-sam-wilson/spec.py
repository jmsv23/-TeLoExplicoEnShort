from lib import *

ep = Episode(7, "capitan-america-sam-wilson", "¿Quién es el nuevo Capitán América?", 118, cont_in="2.1", cont_pulse="9.2")
def V(s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B"):
    i = s.id(name)
    ins = {"pop": f'COM.popIn(tl, q("#{i}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{i}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{i}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{i}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
    if bob: ins += f'\nCOM.idleBob(tl, q("#{i}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});'
    if out: ins += f'\nCOM.popOut(tl, q("#{i}"), {s.t(out)} - 0.05);'
    s.raw(f'<div class="c" id="{i}" style="left:{x}px;top:{y}px">{svg}</div>', ins)
def cover_in(svg, x=450, y=640): return f'<div class="c" style="left:{x}px;top:{y}px">{svg}</div>'

# 1 · portada
s = ep.scene("Portada", "S1", bg="heroe", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 07: escudo")
s.beat(2, 0.7, "**entregó**", "¡TOMA!")
s.beat(3, 1.4, "el **escudo**", "CAP EL ESCUDO")
s.cover("cover", 7, "#14378F", Scene.cover_img("a-cap.jpg", 400, 500, "top", 450, 640), at="1.1", frm="T")
s.cinta("cinta", "EL ESCUDO CAMBIÓ DE MANOS", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("tm", "¡TOMA!", "ono", "amarillo", y=900, at="1.2", size=250, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "STEVE ROGERS", "1.3", width=520)
s.zoom("1.2", 1.12)

# 2 · el elegido
s = ep.scene("El elegido", "S1", bg="papel", enter="halftone", color="papel")
s.beat(1, 2.8, "el **elegido**", "Silueta con foco")
s.beat(2, 3.6, "**superpoderes**", "Rayo tachado")
s.panel("el", pho("a-sam.jpg", "50% 15%", "EL ELEGIDO", 70), 250, 420, 580, 760, "heroe", rot=-3, at="2.1", frm="B")
s.obj("bo", "bolt", 540, 800, 560, 640, "2.2", how="pop")
s.obj("fx", "forbidden", 540, 800, 620, 620, ("2.2", .25), how="stamp")
s.text("sp", "SIN SUPERPODERES", "ttl", "rojo", y=1330, at="2.2", size=110, rot=-4, how="stamp", misreg=True)

# 3 · Sam Wilson
s = ep.scene("Sam Wilson", "S2", bg="heroe", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 4.4, "**Sam** Wilson", "SAM WILSON")
s.beat(2, 5.6, "el **Halcón**", "Alas rojas")
s.beat(3, 6.6, "**recibió**", "Escudo llega")
s.beat(4, 7.4, "al final de **Endgame**", "Logo de Endgame")
s.panel("sam", pho("a-sam.jpg", "50% 15%", "SAM WILSON", 56), 60, 420, 440, 640, "ceniza", rot=-3, at="3.1", frm="L")
s.img("wg", "a-samcap.jpg", 780, 790, 440, 620, "3.2", how="slam", frm="T", bob="3.4", pos="top")
s.text("hc", "¡HALCÓN!", "ono", "amarillo", y=1180, at="3.2", size=190, rot=-7, hold=1.2, misreg=True)
pass
s.panel("eg", '<div class="c" style="position:relative"><img src="' + IMG + 'endgame-logo.png" style="width:620px;height:260px;object-fit:contain" /></div>', 130, 1230, 820, 300, "papel", rot=2, at="3.4", frm="B")

# 4 · duda
s = ep.scene("La duda", "S2", bg="ceniza", enter="halftone", color="ceniza")
s.beat(1, 8.4, "En la **serie** Falcon", "Claqueta de serie")
s.beat(2, 10.9, "**dudó**", "Nube ¿?")
s.beat(3, 11.9, "si **merecía**", "¿MEREZCO?")
s.obj("cl", "clapper", 540, 760, 640, 640, "4.1", how="slam", frm="B", out="4.2")
s.cinta("fs", "LA SERIE", "tinta", top=1210, rot=-5, at="4.1", out="4.2")
s.panel("sam", pho("a-sam.jpg", "50% 15%"), 100, 450, 420, 560, "heroe", rot=-3, at="4.2", frm="L")
s.globo("nu", "¿MEREZCO<br>EL ESCUDO?", 420, 430, 600, 400, "4.3", kind="nube", size=64, rot=3)
s.text("dd", "¡DUDÓ!", "ono", "amarillo", y=1250, at="4.2", size=230, rot=-7, hold=1.4, misreg=True)

# 5 · nuevo mundo
s = ep.scene("Un nuevo mundo", "S2", bg="heroe", enter="pageflip", color="heroe")
s.beat(1, 13.2, "**Capitán** América", "Título")
s.beat(2, 14.4, "Un **nuevo** mundo", "NUEVO MUNDO")
s.beat(3, 15.9, "ya lo es de **verdad**", "¡CAPITÁN!")
s.img("sh", "a-brave.jpg", 540, 780, 470, 700, "5.1", how="slam", frm="T", bob="5.3", pos="top")
s.cinta("t", "CAPITÁN AMÉRICA", "rojo", top=1180, rot=-5, at="5.1", words=["5.1", ("5.1", .35)])
s.text("nm", "UN NUEVO MUNDO", "ttl", "amarillo", y=1380, at="5.2", size=100, rot=-4, how="stamp")
s.text("vd", "¡DE VERDAD!", "ono", "amarillo", y=560, at="5.3", size=210, rot=-7, hold=1.0, misreg=True, zoom=True)
s.speed("sl", "5.3", n=36, seed=7)

# 6 · sin suero
s = ep.scene("Sin suero", "S2", bg="ciencia", enter="halftone", color="ciencia")
s.beat(1, 16.9, "no tiene **suero**", "Suero tachado")
s.beat(2, 18.5, "alas de **vibranium**", "Alas")
s.beat(3, 20.0, "**entrenamiento**", "Pesa")
s.beat(4, 21.0, "mucho **carácter**", "¡CARÁCTER!")
s.panel("su", '<div class="c" style="position:relative"><span class="ttl ttl--tinta" style="font-size:150px">SUERO</span></div>', 60, 420, 440, 330, "papel", rot=-3, at="6.1", frm="L")
s.obj("f1", "forbidden", 280, 590, 360, 360, ("6.1", .25), how="stamp")
s.img("wg", "a-samcap.jpg", 800, 600, 330, 470, "6.2", how="slam", frm="R", bob="end", pos="top")
s.cap("vb", "VIBRANIUM", "6.2", left=600, top=870, width=420)
V(s, "db", dumbbell(440), 290, 1060, "6.3", how="slam", frm="L", bob="end")
s.cinta("en", "ENTRENAMIENTO", "tinta", top=1250, rot=-5, at="6.3")
s.text("ca", "¡CARÁCTER!", "ono", "amarillo", x=720, y=1100, at="6.4", size=170, rot=-7, hold=1.4, misreg=True, zoom=True)

# 7 · Red Hulk
s = ep.scene("Red Hulk", "S2", bg="tinta", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 22.1, "su **película**", "Pantalla")
s.beat(2, 23.2, "**Red** Hulk", "Gigante rojo")
s.beat(3, 24.4, "el presidente **Ross**", "PRESIDENTE ROSS")
s.beat(4, 25.1, "**transformado**", "Transformación")
s.obj("sc", "cinemaScreen", 540, 780, 780, 580, "7.1", how="slam", frm="B", out="7.2")
s.img("hk", "a-redhulk.jpg", 380, 880, 600, 760, "7.2", how="slam", frm="B", bob="end", pos="top")
s.img("rs", "a-ross.jpg", 840, 960, 340, 500, "7.3", how="slam", frm="R", pos="top")
s.text("rh", "¡RED HULK!", "ono", "amarillo", x=380, y=470, at="7.2", size=170, rot=-7, hold=1.4, misreg=True, zoom=True)
s.cinta("ro", "PRESIDENTE ROSS", "papel", top=1300, rot=-5, at="7.3")
s.flash("7.4")

# 8 · brazalete
s = ep.scene("El brazalete", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 26.6, "como el **brazalete**", "Brazalete de capitán")
s.beat(2, 28.0, "en un **equipo**", "Camisetas")
s.beat(3, 29.0, "el **jugador** cambia", "Camisetas cambian")
s.beat(4, 30.3, "el **símbolo** se queda", "Brazalete se queda")
V(s, "ab", armband(760), 540, 640, "8.1", how="slam", frm="T", rot=-3)
for k, x in enumerate((220, 540, 860)):
    s.raw(f'<div class="c" id="v07-e8-j{k}" style="left:{x}px;top:1100px"><div data-com="jersey" style="width:250px;height:268px"></div></div>', f'COM.popIn(tl, q("#v07-e8-j{k}"), {s.t("8.2")} + {k*0.1}, {{ rot: -6 }});\nCOM.popOut(tl, q("#v07-e8-j{k}"), {s.t("8.3")} + {k*0.12});')
    s.raw(f'<div class="c" id="v07-e8-k{k}" style="left:{x}px;top:1100px"><div data-com="jersey" data-opts=\'{{"color":"doom","letra":"D"}}\' style="width:250px;height:268px"></div></div>', f'COM.popIn(tl, q("#v07-e8-k{k}"), {s.t("8.3")} + {0.3 + k*0.12}, {{ rot: 6 }});')
s.cinta("cj", "EL JUGADOR CAMBIA", "rojo", top=1350, rot=-4, at="8.3", out="8.4")
s.pulse("ab", "8.4", 1.18)
s.text("sq", "¡SE QUEDA!", "ono", "amarillo", y=1480, at="8.4", size=170, rot=-6, hold=1.2, misreg=True)

# 9 · confirmado
s = ep.scene("Confirmado", "S3", bg="heroe", enter="halftone", color="heroe")
s.beat(1, 31.6, "**Anthony** Mackie", "Cinta")
s.beat(2, 32.8, "está **confirmado**", "Palomita CONFIRMADO")
s.beat(3, 33.8, "de **Doomsday**", "Logo")
s.cinta("an", "ANTHONY MACKIE", "amarillo", top=520, rot=-5, at="9.1", words=["9.1", ("9.1", .35)])
V(s, "ck", check(520), 540, 900, "9.2", how="slam", frm="B", bob="end")
s.text("cf", "¡CONFIRMADO!", "ono", "amarillo", y=1330, at="9.2", size=170, rot=-6, hold=1.2, misreg=True, zoom=True)
s.panel("logo", '<div class="c" style="position:relative"><img src="' + IMG + 'doomsday-logo.png" style="width:700px;height:280px;object-fit:contain" /></div>', 90, 1190, 900, 300, "papel", rot=-2, at="9.3", frm="B")

# 10 · presión
s = ep.scene("Zapatos de Steve", "S3", bg="doom-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 34.9, "**Sam** llega", "Sam con escudo")
s.beat(2, 36.2, "la **presión**", "Peso aplasta")
s.beat(3, 37.2, "llenar los **zapatos**", "Botas")
s.beat(4, 38.0, "de **Steve**", "LOS DE STEVE")
s.panel("sam", pho("a-sam.jpg", "50% 15%"), 40, 420, 380, 560, "heroe", rot=-3, at="10.1", frm="L")
V(s, "sh", shield(300), 700, 700, "10.1", how="slide", frm="R", out="10.2")
s.panel("pr", '<div class="c" style="position:relative"><span class="ttl ttl--papel" style="font-size:170px">PRESIÓN</span></div>', 80, 440, 900, 300, "tinta", rot=0, at="10.2", frm="T", prot=2)
s.code('tl.to(q("#v07-e10-sam"), { scaleY: 0.7, transformOrigin: "50% 100%", duration: 0.25, ease: "power2.in" }, ' + s.t("10.2") + ');')
s.shake("pr", ("10.2", .3), 14)
V(s, "b1", boot(380, "#1E5BFF"), 300, 1150, "10.3", how="slam", frm="L")
V(s, "b2", boot(380, "#E8212B"), 780, 1150, ("10.3", .15), how="slam", frm="R", rot=-4)
s.cinta("st", "LOS DE STEVE", "amarillo", top=1320, rot=-5, at="10.4")
s.zoom("10.4", 1.1)

# 11 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 38.9, "**Siguiente**", "Portada N.º 08")
s.beat(2, 39.5, "el **regreso**", "X")
s.beat(3, 40.1, "**X-Men**", "Cinta")
s.cover("cover", 8, "multi-osc", cover_in(xlogo(360), 450, 610), at="11.1", frm="R")
s.text("q", "EL REGRESO DE<br>LOS X-MEN", "ttl", "amarillo", x=540, y=1140, at="11.2", size=74, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1290, rot=-8, at="11.3")
