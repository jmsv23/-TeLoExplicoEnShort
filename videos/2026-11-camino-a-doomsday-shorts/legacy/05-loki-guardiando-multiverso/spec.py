from lib import *

ep = Episode(5, "loki-guardiando-multiverso", "¿Qué hizo Loki y por qué es clave para Doomsday?", 128, cont_in="2.1", cont_pulse="9.2")
V = lambda s, name, svg, x, y, at, how="pop", bob=None, out=None, rot=0, frm="B": (
    s.raw(f'<div class="c" id="{s.id(name)}" style="left:{x}px;top:{y}px">{svg}</div>',
          {"pop": f'COM.popIn(tl, q("#{s.id(name)}"), {s.t(at)}, {{ rot: {rot} }});', "slam": f'COM.panelSlam(tl, q("#{s.id(name)}"), {s.t(at)}, {{ from: "{frm}", rot: {rot or 4} }});',
           "slide": f'COM.slideIn(tl, q("#{s.id(name)}"), {s.t(at)}, "{frm}");', "drop": f'COM.dropIn(tl, q("#{s.id(name)}"), {s.t(at)}, {{ from: {-(y+500)} }});'}[how]
          + (f'\nCOM.idleBob(tl, q("#{s.id(name)}"), {s.t(at)} + 0.4, {s.t(bob)}, {{ amp: 9, cycle: 1.0 }});' if bob else "")
          + (f'\nCOM.popOut(tl, q("#{s.id(name)}"), {s.t(out)} - 0.05);' if out else "")))

# 1 · portada
s = ep.scene("Portada", "S1", bg="multi", enter="cut")
s.beat(1, 0.0, "(primer frame)", "Portada N.º 05: casco de Loki")
s.beat(2, 0.6, "**terminó** su serie", "¡LOKI!")
s.beat(3, 1.4, "su **serie**", "CAP")
s.cover("cover", 5, "multi-osc", Scene.cover_img('a-loki.jpg', 400, 500, 'top', 450, 640), at="1.1", frm="T")
s.cinta("cinta", "LOKI SOSTIENE TODO", "amarillo", top=1190, rot=-8, at="1.1")
s.speed("sl", "1.2", n=30, seed=2)
s.text("lk", "¡LOKI!", "ono", "amarillo", y=880, at="1.2", size=260, rot=-7, hold=0.9, misreg=True)
s.cap("cap", "FINAL DE SU SERIE", "1.3", width=620)
s.zoom("1.2", 1.12)

# 2 · trono
s = ep.scene("El trono", "S1", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 2.6, "en un **trono**", "Trono con Loki")
s.beat(2, 3.5, "**sosteniendo**", "Portal sobre sus manos")
s.beat(3, 4.2, "con sus **manos**", "Pulso")
V(s, "th", throne(780), 540, 900, "2.1", how="slam", frm="B", bob="end")
s.img("hm", "a-loki.jpg", 540, 740, 260, 330, "2.1", how="drop", pos="top")
V(s, "pt", portal(420), 360, 440, "2.2", how="pop")
s.pulse("pt", "2.3", 1.2)
s.cinta("sost", "SOSTIENE EL MULTIVERSO", "amarillo", top=1300, rot=-5, at="2.2")

# 3 · ramas ardiendo
s = ep.scene("Ramas ardiendo", "S2", bg="rojo", enter="halftone", color="rojo", pat="pat-benday-fuerte")
s.beat(1, 5.1, "la **segunda** temporada", "TEMPORADA 2")
s.beat(2, 6.4, "las **ramas**", "Ramas de colores")
s.beat(3, 7.8, "se están **quemando**", "Llamas")
s.beat(4, 8.8, "sin **control**", "¡SIN CONTROL!")
s.cinta("t2", "LOKI · TEMPORADA 2", "tinta", top=470, rot=-5, at="3.1", out="3.2")
V(s, "br", branches(1000, 560), 540, 830, "3.2", how="slide", frm="L")
s.code('tl.set(qa("#v05-e3-br .br"), {}, 0);')
for k, (x, y, w) in enumerate(((250, 760, 260), (540, 700, 330), (820, 780, 280), (400, 1000, 240), (700, 1030, 260))):
    V(s, f"f{k}", flame(w), x, y, ("3.3", k * 0.09), how="pop", bob="end")
s.text("sc", "SIN CONTROL", "ttl", "amarillo", y=1330, at="3.4", size=170, rot=-5, misreg=True, zoom=True)
s.speed("sl", "3.3", n=34, seed=6)

# 4 · falla
s = ep.scene("Intenta y falla", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 9.9, "**intenta** arreglarlo", "Casco + engranaje")
s.beat(2, 11.0, "una y **otra** vez", "Flecha circular")
s.beat(3, 12.0, "y **falla**", "X roja")
s.img("hm", "a-loki.jpg", 340, 860, 380, 480, "4.1", how="slam", frm="L", out="4.3", pos="top")
s.obj("g", "gearAtom", 780, 860, 380, 380, "4.1", how="pop", out="4.3")
s.spin("g", "4.1", 160, 3)
s.cinta("int", "INTENTA ARREGLARLO", "amarillo", top=1230, rot=-5, at="4.1", out="4.3")
V(s, "cy", cycle(520), 540, 840, "4.2", how="pop", out="4.3", rot=-20)
s.code('tl.fromTo(q("#v05-e4-cy"), { rotation: 0 }, { rotation: 360, duration: 1.6, ease: "none", immediateRender: false }, %s);' % s.t("4.2"))
s.obj("x", "xMark", 540, 850, 640, 640, "4.3", how="stamp")
s.text("fa", "¡FALLA!", "ono", "rojo", y=1300, at="4.3", size=260, rot=-7, hold=1.2, misreg=True, zoom=True)

# 5 · toma el trono
s = ep.scene("Toma el trono", "S2", bg="multi", enter="halftone", color="multi")
s.beat(1, 13.6, "lo único que **queda**", "Solo queda una opción")
s.beat(2, 14.9, "toma el **trono**", "Trono entra")
s.beat(3, 16.0, "He Who **Remains**", "Kang se va, Loki entra")
s.text("q", "LO ÚNICO<br>QUE QUEDA", "ttl", "papel", y=820, at="5.1", size=170, rot=-4, out="5.2")
V(s, "th", throne(780), 540, 900, "5.2", how="slam", frm="B", bob="end")
s.img("kg", "a-kang.jpg", 540, 800, 340, 430, "5.2", how="pop", out="5.3", pos="center")
s.img("hm", "a-loki.jpg", 540, 800, 340, 430, "5.3", how="drop", pos="top")
s.cinta("hwr", "HE WHO REMAINS", "amarillo", top=1300, rot=-5, at="5.3", words=["5.3", ("5.3", .3), ("5.3", .5)])
s.flash("5.3")

# 6 · Yggdrasil
s = ep.scene("Yggdrasil", "S2", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 17.6, "Con su **magia**", "Runas")
s.beat(2, 18.8, "todas las **ramas**", "Ramas confluyen")
s.beat(3, 20.2, "un solo **árbol**", "Árbol crece")
s.beat(4, 21.4, "**Yggdrasil**", "Cinta YGGDRASIL")
s.beat(5, 22.4, "**mitología**", "NÓRDICA")
s.beat(6, 23.4, "mantiene **vivas**", "Hojas brillan")
s.obj("ru", "runes", 540, 760, 560, 560, "6.1", how="pop", out="6.2")
s.pulse("ru", ("6.1", .3), 1.15)
V(s, "br", branches(1000, 560), 540, 830, "6.2", how="slide", frm="R", out="6.3")
V(s, "tr", tree(820, 980), 540, 820, "6.3", how="pop")
s.code('tl.fromTo(qa("#v05-e6-tr .lf"), { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.08, transformOrigin: "50% 50%", immediateRender: false }, ' + s.t("6.3") + ');')
s.cinta("yg", "YGGDRASIL", "amarillo", top=1330, rot=-5, at="6.4")
s.cap("cap", "MITOLOGÍA NÓRDICA", "6.5", top=1470, width=700)
s.pulse("tr", "6.6", 1.08)
s.flash("6.6")

# 7 · dios de las historias
s = ep.scene("Dios de las historias", "S2", bg="amarillo" if False else "multi", enter="halftone", color="multi")
s.beat(1, 24.4, "es el **dios**", "Loki con aura")
s.beat(2, 25.5, "de las **historias**", "Cómic abierto")
s.speed("sl", "7.1", n=40, seed=3, dur=0.8)
s.img("hm", "a-loki.jpg", 540, 780, 520, 660, "7.1", how="slam", frm="B", bob="end", pos="top")
s.text("dios", "¡DIOS!", "ono", "amarillo", x=300, y=420, at="7.1", size=240, rot=-7, hold=1.1, misreg=True, zoom=True)
s.obj("cm", "comicOpen", 540, 1220, 560, 450, "7.2", how="slam", frm="B", rot=4)
s.cinta("hist", "DIOS DE LAS HISTORIAS", "amarillo", top=1450, rot=-5, at="7.2")

# 8 · portero
s = ep.scene("El portero", "S2", bg="papel", enter="pageflip", color="papel")
s.beat(1, 26.8, "**Piénsalo** como", "Nube PIÉNSALO")
s.beat(2, 27.8, "un **portero**", "Portería + Loki")
s.beat(3, 29.0, "todo el **multiverso**", "Portales detrás")
s.beat(4, 30.3, "**nadie** más", "Cancha vacía")
s.beat(5, 31.0, "en la **cancha**", "Cinta SOLO ÉL")
s.globo("nube", "PIÉNSALO ASÍ", 120, 420, 560, 340, "8.1", kind="nube", size=56, out="8.2")
s.obj("goal", "goal", 540, 840, 860, 640, "8.2", how="slam", frm="B")
s.img("hm", "a-loki.jpg", 540, 990, 250, 320, "8.2", how="drop", bob="end", pos="top")
V(s, "p1", portal(230), 400, 780, "8.3", how="pop")
V(s, "p2", portal(230), 540, 720, ("8.3", .15), how="pop")
V(s, "p3", portal(230), 680, 780, ("8.3", .3), how="pop")
s.text("nad", "¿NADIE?", "ono", "rojo", y=1320, at="8.4", size=230, rot=-6, hold=1.0)
s.cinta("sl", "SOLO ÉL", "amarillo", top=1450, rot=-5, at="8.5")
s.zoom("8.5", 1.1)

# 9 · última defensa
s = ep.scene("La última defensa", "S3", bg="multi-osc", enter="ink", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 32.8, "el más **sarcástico**", "Globo ¿EN SERIO?")
s.beat(2, 34.7, "la **última** defensa", "Escudo ÚLTIMA DEFENSA")
s.beat(3, 36.0, "cada **realidad**", "Portales detrás")
s.img("hm", "a-loki.jpg", 540, 900, 460, 580, "9.1", how="slam", frm="B", bob="end", pos="top")
s.globo("gl", "¿EN SERIO?", 60, 400, 470, 230, "9.1", size=64, out="9.2")
s.text("ul", "ÚLTIMA<br>DEFENSA", "ttl", "amarillo", x=380, y=560, at="9.2", size=190, rot=-5, misreg=True, zoom=True)
for k, x in enumerate((220, 540, 860)):
    V(s, f"p{k}", portal(260), x, 1300, ("9.3", k * 0.12), how="pop", bob="end")

# 10 · romper
s = ep.scene("Si alguien quiere romper", "S3", bg="tinta", enter="halftone", color="tinta", pat="pat-benday-fuerte")
s.beat(1, 37.4, "quiere **romper**", "Portal se agrieta")
s.beat(2, 38.4, "ya **sabe**", "Ojo")
s.beat(3, 39.2, "dónde **buscar**", "Cinta")
V(s, "pt", portal(640), 540, 780, "10.1", how="pop", out="10.2")
s.obj("sp", "splat", 540, 780, 900, 900, ("10.1", .6), how="pop", out="10.2")
s.text("rom", "¡CRAC!", "ono", "amarillo", y=780, at=("10.1", .6), size=250, rot=-8, hold=0.8, zoom=True)
V(s, "ey", eye(780), 540, 760, "10.2", how="pop")
s.cinta("bus", "SABE DÓNDE BUSCAR", "rojo", top=1200, rot=-5, at="10.3")

# 11 · CTA
s = ep.scene("Siguiente número", "S4", bg="multi", enter="cover", color="papel")
s.beat(1, 39.9, "**Siguiente**", "Portada N.º 06")
s.beat(2, 40.6, "los **Cuatro**", "Emblema 4")
s.beat(3, 41.0, "**Fantásticos**", "Cinta")
s.cover("cover", 6, "multi-osc", Scene.cover_img('a-logo4.jpg', 380, 390, 'center', 450, 640), at="11.1", frm="R")
s.text("q", "LOS CUATRO<br>FANTÁSTICOS", "ttl", "amarillo", x=540, y=1130, at="11.2", size=80, rot=-4, how="stamp")
s.cinta("cinta", "SIGUE LA SERIE", "amarillo", top=1290, rot=-8, at="11.3")
