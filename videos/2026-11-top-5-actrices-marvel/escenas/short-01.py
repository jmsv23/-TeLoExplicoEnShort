"""Dirección visual del Short (1080×1920). Estilo "Portada". Solo imágenes; un cambio cada ≤1.5–3 s."""


def short(S):
    w = S.w
    # GANCHO (feed de Shorts): Scarlett a pantalla completa desde el cuadro 0, cortes rápidos con flash
    S.add("foto", w("La mujer más sexy"), "corte", img="scarlett-ironman2-pose", pos="50% 30%", kb="in",
          kick="TOP 5 · MCU", tk=0.0, l1="¿LA MÁS SEXY DEL MCU?", t1=0.15, fs1=104)
    S.add("foto", w("según Esquire"), "flash", img="scarlett-cannes-alfombra", pos="38% 40%", kb="in")
    S.add("impresa", w("Dos veces"), "flash", img="scarlett-esquire-2013", pos="50% 20%", vertical=True,
          kick="ESQUIRE · 2006 · 2013", tk=w("Dos veces"),
          dato=("", "2", "", "veces “la mujer más sexy del mundo”", w("Dos veces")), fsd=170)
    S.add("foto", w("Pero es la número uno"), "flash", img="scarlett-oscar-2025-cuerpo", pos="50% 20%", kb="up",
          kick="¿PERO ES LA Nº 1?", tk=w("Pero es"), l1="TOP 5 DEL MCU", t1=w("de Marvel"), fs1=110)
    S.add("contactos", w("Las cinco actrices"), "corte", imgs=[("zoe-oscar-alfombra", "50% 10%"), ("portman-cannes", "50% 10%"),
          ("zendaya-metgala-2024", "50% 10%"), ("olsen-critics-vino", "50% 10%")],
          ts=[w("Las cinco"), w("Las cinco") + 0.25, w("actrices"), w("más guapas")],
          kick="TOP 5 · MARVEL", tk=w("Las cinco"), titulo="LAS MÁS GUAPAS", tt=w("más guapas"), fst=96)
    # Nº5
    S.add("portada", w("Número cinco"), "pagina", n="5", tnum=w("cinco"), img="zoe-oscar-perfil", pos="45% 20%",
          nombre="ZOE", apellido="SALDAÑA", rol="Gamora", tn=w("Zoe Saldaña"), trol=w("Se pintaba"))
    S.add("foto", w("Se pintaba de verde"), "latigo", img="zoe-gamora-retrato", pos="40% 25%", kb="in",
          kick="CADA DÍA DE RODAJE", tk=w("cada día"), l1="PINTADA DE VERDE", t1=w("de verde"))
    S.add("dato", w("y hoy es"), "latigo", img="zoe-oscar-escenario", pos="55% 35%", kick="RÉCORD 2026", pre="Nº ", num="1",
          cuenta=False, label="la actriz más taquillera de la historia", tn=w("la actriz más"), tl=w("de la historia"), fs=200)
    # Nº4
    S.add("portada", w("Número cuatro"), "pagina", n="4", tnum=w("cuatro"), img="portman-cannes", pos="50% 10%",
          nombre="NATALIE", apellido="PORTMAN", rol="Jane Foster", tn=w("Natalie Portman"), trol=w("Ganó un"))
    S.add("foto", w("Ganó un Óscar"), "latigo", img="portman-oscar-2011", pos="50% 20%", kb="in", kick="ÓSCAR 2011",
          l1="UN ÓSCAR", t1=w("Ganó un Óscar") + 0.2)
    S.add("foto", w("y se graduó"), "latigo", img="portman-harvard-2015", pos="40% 30%", kb="r", kick="PSICOLOGÍA",
          l1="HARVARD", t1=w("de Harvard"))
    # Nº3
    S.add("portada", w("Número tres"), "pagina", n="3", tnum=w("tres"), img="zendaya-metgala-flores", pos="80% 25%",
          nombre="", apellido="ZENDAYA", rol="MJ · Spider-Man", tn=w("Zendaya"), trol=w("MJ en Spider-Man"))
    S.add("foto", w("ícono de la moda"), "latigo", img="zendaya-metgala-2024", pos="50% 12%", kb="up", kick="MET GALA",
          l1="ÍCONO DE LA MODA", t1=w("ícono de la moda") + 0.15, fs1=88)
    S.add("foto", w("y ya es la esposa"), "latigo", img="zendaya-holland-premiere", pos="62% 20%", kb="in",
          kick="CON TOM HOLLAND", tk=w("la esposa"), l1="SPIDER-MAN, EN LA VIDA REAL", t1=w("en la vida real"), fs1=74)
    # Nº2
    S.add("portada", w("Número dos"), "pagina", n="2", tnum=w("dos"), img="olsen-corona-retrato", pos="55% 20%",
          nombre="ELIZABETH", apellido="OLSEN", rol="La Bruja Escarlata", tn=w("Elizabeth Olsen"), trol=w("la Bruja Escarlata"))
    S.add("foto", w("Y Doctor Doom"), "latigo", img="visionquest-wanda-revive", pos="45% 40%", kb="in",
          kick="VISIONQUEST · FINAL", tk=w("Doctor Doom"), l1="DOOM LA REVIVE", t1=w("acaba de revivirla"), fs1=92)
    S.add("foto", w("para Doomsday"), "corte", img="doomsday-poster-teaser", pos="50% 30%", kb="in",
          kick="18 DE DICIEMBRE", l1="DOOMSDAY", t1=w("para Doomsday") + 0.2, fs1=110)
    # Nº1
    S.add("titulo", w("Y número uno"), "crece", kick="Y LA NÚMERO UNO…", tk=w("Y número uno"))
    S.add("portada", w("Scarlett Johansson"), "corte", n="1", tnum=w("Scarlett Johansson"), img="scarlett-natasha-retrato",
          pos="50% 25%", nombre="SCARLETT", apellido="JOHANSSON", fsn=104, rol="Black Widow", tn=w("Scarlett Johansson") + 0.2,
          trol=w("Black Widow"))
    S.add("foto", w("Y sí"), "flash", img="scarlett-ironman2-pose", pos="50% 30%", kb="in",
          kick="LA RESPUESTA", tk=w("Y sí"), l1="LA MÁS SEXY, DOS VECES", t1=w("dos veces", after=w("Y sí")), fs1=92)
    # CTA
    t = w("Quién falta")
    S.add("galeria", t, "pagina", kick="¿QUIÉN FALTA?", tk=t,
          items=[("pugh-yelena", "PUGH", t + 0.1, "50% 25%"), ("steinfeld-kate-vertical", "STEINFELD", t + 0.3),
                 ("larson-carol", "LARSON", t + 0.5, "50% 20%"), ("kirby-sue", "KIRBY", t + 0.7, "55% 30%")],
          titulo="EN LOS COMENTARIOS", fst=88, tt=w("Escríbelo"))
    S.add("titulo", w("El top completo"), "crece", kick="VIDEO COMPLETO EN EL CANAL", l1="EL TOP", l2="COMPLETO",
          t1=w("El top completo"), t2=w("completo"), sub="Con las que casi entran.", ts=w("las que casi entran"), fs2=150)
