"""Dirección visual de los 6 Shorts (9:16). Una función por Short (s1..s6). Mismas reglas que escenas_largo.py.
Todos cierran con el plano "cta" que manda al video largo.
"""

DUR_LARGO = "12:08"


def cta(S, frase, titulo="EN MI CANAL"):
    w = S.w
    S.add("cta", w(frase), "flash", img="vi-keyart", kick="VIDEO COMPLETO", titulo=titulo, en_mini="1997 VS 2026", dur=DUR_LARGO,
          tt=w(frase) + 0.6)


def s1(S):
    w = S.w
    S.add("dato", w("GTA seis ganó"), "corte", kick="GTA VI · EN UN DÍA", pre="$", num="3790", suf=" M", tn=w("ganó en un día"),
          label="= las dos últimas Avatar juntas", tl=w("Avatar"), video="vi-entrada")
    S.add("foto", w("Entre preventas"), "latigo", video="vi-explosion", kb="in", kick="PREVENTAS + PRIMER DÍA",
          dato=("$", "3790", " M", "millones de dólares", w("tres mil setecientos")))
    S.add("titulo", w("Take Two lo llamó"), "flash", kick="TAKE-TWO", l1="EL LANZAMIENTO MÁS GRANDE", l2="DE LA HISTORIA", t1=w("el lanzamiento"),
          t2=w("de la historia"), sub="películas, discos, juegos", ts=w("películas"))
    S.add("comparar", w("Para que lo compares"), "panel", kick="PRIMER DÍA",
          a=dict(video="v-ls", etq="$800 M", t=w("ochocientos millones"), fs=120), b=dict(video="vi-yate", etq="$3790 M", t=w("Para que lo compares") + 0.3, fs=120))
    S.add("titulo", w("Y el dato más loco"), "crece", kick="EL DATO MÁS LOCO", l1="GTA III → GTA V", l2="12 AÑOS", t1=w("entre GTA tres"), t2=w("GTA cinco, que"))
    S.add("dato", w("Trece años de espera"), "flash", kick="GTA V → GTA VI", num="13", suf=" AÑOS", tn=w("Trece años"), label="de espera", tl=w("de espera"))
    S.add("comparar", w("Pero el dinero"), "panel", kick="¿EVOLUCIÓN O RETROCESO?",
          a=dict(video="sa-cuerpo3", etq="SAN ANDREAS", t=w("San Andreas"), fs=100), b=dict(video="iv-vs-v-b", etq="GTA V", t=w("un paso atrás"), fs=120))
    cta(S, "Te lo cuento", "29 AÑOS DE GTA")


def s2(S):
    w = S.w
    S.add("versus", w("La crítica le dio"), "corte", kick="GTA VI EN METACRITIC",
          a=("99", "LA CRÍTICA", w("noventa y nueve")), b=("5", "LOS JUGADORES", w("un cinco"), "mal"))
    S.add("panel", w("Noventa y nueve en Metacritic"), "panel", img="metacritic-99", kick="METASCORE", titulo="99 / 100", tt=w("Noventa y nueve"),
          sub="Empata con Ocarina of Time.", ts=w("Ocarina"))
    S.add("panel", w("Pero la calificación"), "latigo", img="metacritic-user", pos="0% 100%", kick="USER SCORE", titulo="MENOS DE 5", tt=w("por debajo de cinco"),
          sub="La mayor diferencia de la historia del sitio.", ts=w("La diferencia"))
    S.add("foto", w("Una parte es review bombing"), "panel", video="vi-noche", kb="in", kick="REVIEW BOMBING", titulo="NI TIENEN EL JUEGO", tt=w("ni siquiera"))
    S.add("lista", w("Pero también hay quejas"), "panel", kick="LAS QUEJAS REALES", items=[
        ("30 FPS", "en consola", w("treinta cuadros"), "1"), ("ERRORES", "de lanzamiento", w("tiene errores"), "2"),
        ("$100", "edición de lujo", w("cien dólares"), "3")])
    S.add("titulo", w("Y sabes cuál sigue"), "flash", kick="EL FAVORITO DE LOS JUGADORES", l1="UNO DE HACE", l2="22 AÑOS", t1=w("Uno de hace"), t2=w("veintidós años"))
    cta(S, "Cuál es", "LA RESPUESTA EN MI CANAL")
    S.add("titulo", w("Y tú, cuánto le das"), "crece", kick="EN LOS COMENTARIOS", l2="¿CUÁNTO LE DAS?", t2=w("cuánto le das"), fs2=150)


def s3(S):
    w = S.w
    S.add("foto", w("El barco de Michael"), "corte", video="vi-barco2", kb="in", kick="EASTER EGG EN GTA VI", titulo="EL BARCO DE MICHAEL", tt=w("El barco"))
    S.add("foto", w("Y su GPS"), "latigo", video="vi-barco", kb="in", kick="SU GPS MARCA", titulo="LOS SANTOS", tt=w("Los Santos"))
    S.add("panel", w("Está estacionado"), "panel", img="mft-arte", kick="EL MISMO VELERO DE GTA V", tk=w("mismo velero"),
          titulo="NO MUESTRA LEONIDA", tt=w("no muestra Leonida"))
    S.add("titulo", w("En el celular"), "flash", kick="EN EL CELULAR", l2="RACE'N'CHASE", t2=w("Race and Chase"), sub="el nombre original de GTA", ts=w("el nombre"), pixel=True)
    S.add("foto", w("En los pantanos"), "latigo", video="vi-pantano", kb="in", kick="EN LOS PANTANOS", titulo="SKUNK APE", tt=w("Skunk Ape"),
          sub="El Pie Grande de San Andreas.", ts=w("el Pie Grande"))
    S.add("panel", w("Y el actor"), "panel", img="niko", vertical=True, kick="EN LOS CRÉDITOS", titulo="EL ACTOR DE NIKO", tt=w("Niko Bellic"),
          sub="Rockstar no ha dicho si es él.", ts=w("Rockstar no"))
    S.add("foto", w("Y en lo más alto"), "latigo", video="vi-aereo", kb="up", kick="EN LO MÁS ALTO DE UNA TORRE", titulo="UN HUEVO DE PASCUA LITERAL", tt=w("Literal"), fst=96)
    S.add("comparar", w("Pero el easter egg"), "flash", kick="VICE CITY",
          a=dict(video="vc-vs-vi-a", etq="2002", t=w("Pero el easter egg") + 0.3), b=dict(video="vc-vs-vi-b", etq="2026", t=w("te va a volar")))
    cta(S, "Lo comparo todo", "1997 VS 2026")


def s4(S):
    w = S.w
    S.add("estrellas", w("En GTA seis"), "corte", video="vi-policia-1", n=6, kick="GTA VI", titulo="LA POLICÍA YA NO SABE DÓNDE ESTÁS", tt=w("ya no sabe"),
          on=[(k, w("la policía") + k * 0.1) for k in range(6)], fst=88)
    S.add("foto", w("Durante veinticinco años"), "latigo", video="gta1-policia", kb="in", kick="25 AÑOS", titulo="SIEMPRE SABÍAN QUIÉN ERAS", tt=w("exactamente"), fst=90)
    S.add("lista", w("En GTA tres llegaron"), "panel", kick="CÓMO CAMBIÓ", items=[
        ("GTA III", "seis estrellas", w("En GTA tres"), "★"), ("GTA IV", "el círculo en el mapa", w("En GTA cuatro"), "◯"),
        ("GTA V", "conos de visión", w("En GTA cinco"), "▲")])
    S.add("lista", w("En GTA seis, la policía necesita"), "flash", kick="GTA VI · NECESITAN", items=[
        ("UN TESTIGO", "", w("un testigo"), "1"), ("UNA ALARMA", "", w("una alarma"), "2"), ("UNA CÁMARA", "", w("una cámara"), "3")])
    S.add("titulo", w("Y te busca"), "crece", kick="TE BUSCAN POR", l1="TU CARA · TU ROPA", l2="TU AUTO", t1=w("tu cara"), t2=w("tu auto"))
    S.add("foto", w("Te cambias de ropa"), "latigo", video="vi-policia-2", kb="in", kick="¿TE CAMBIAS? ¿PINTAS EL AUTO?", titulo="LES PIERDES LA PISTA", tt=w("Les pierdes"))
    S.add("estrellas", w("Ya no hay patrullas"), "panel", video="vi-patrulla", n=6, kick="SIN PATRULLAS EN EL MINIMAPA", titulo="REGRESA LA 6ª ESTRELLA", tt=w("sexta estrella"),
          on=[(k, w("sexta estrella") + k * 0.1) for k in range(6)])
    S.add("foto", w("Y no solo la policía"), "latigo", video="vi-noche", kb="in", kick="LA GENTE YA NO HUYE", titulo="TE GRABA CON EL CELULAR", tt=w("te graba"), fst=90)
    S.add("titulo", w("Pero el origen"), "flash", kick="EL ORIGEN", l1="NACIÓ DE UN", l2="ERROR", t1=w("nació de"), t2=w("un error"), sub="y sin él, GTA no existiría", ts=w("sin ese error"))
    cta(S, "La historia completa", "LA HISTORIA EN MI CANAL")


def s5(S):
    w = S.w
    S.add("comparar", w("Vice City en dos mil dos"), "corte", kick="LA MISMA CIUDAD",
          a=dict(video="vc-vs-vi-a", etq="2002", t=w("Vice City en")), b=dict(video="vc-vs-vi-b", etq="2026", t=w("dos mil veintiséis")))
    S.add("panel", w("La original medía"), "panel", img="mapa-vc2002", kick="VICE CITY 2002", titulo="MENOS DE 10 KM²", tt=w("menos de diez"),
          sub="Y era todo el juego.", ts=w("Y era todo"))
    S.add("foto", w("Tommy Vercetti no sabía"), "latigo", video="vc-tommy-auto", kb="in", kick="TOMMY VERCETTI", titulo="NO SABÍA NADAR", tt=w("no sabía nadar"))
    S.add("panel", w("En GTA seis, Vice City"), "panel", img="mapa-leonida", kick="GTA VI", titulo="LEONIDA", tt=w("Leonida"),
          sub="Un estado completo inspirado en Florida.", ts=w("un estado"))
    S.add("dato", w("Según Rockstar"), "flash", kick="SEGÚN ROCKSTAR", num="2", suf="×", tn=w("casi el doble"), label="el mapa de GTA V", tl=w("GTA cinco"), video="vi-aereo")
    S.add("foto", w("Y Vice City es"), "latigo", video="vi-playa", kb="in", titulo="LA CIUDAD MÁS GRANDE DE ROCKSTAR", tt=w("la ciudad más grande"), fst=92)
    S.add("panel", w("Y el hotel Ocean View"), "panel", img="ocean-view", kick="REGRESÓ", titulo="HOTEL OCEAN VIEW", tt=w("Ocean View"),
          sub="Mismo lugar, 24 años después.", ts=w("Mismo lugar"))
    S.add("foto", w("Y Leonida no es solo"), "latigo", video="vi-caiman", kb="in", kick="LEONIDA TIENE", titulo="CAIMANES", tt=w("caimanes"))
    S.add("comparar", w("Pero hay un GTA"), "flash", kick="¿CUÁL ERA MÁS GRANDE?",
          a=dict(img="sa-cover", etq="¿?", t=w("Pero hay un GTA") + 0.2), b=dict(img="iv-cover", etq="¿?", t=w("cuatro años después")))
    cta(S, "Te lo enseño", "LA RESPUESTA EN MI CANAL")


def s6(S):
    w = S.w
    S.add("comparar", w("GTA cinco empeoró"), "corte", kick="FÍSICA DE CHOQUES",
          a=dict(video="iv-vs-v-b", etq="GTA V", t=w("GTA cinco empeoró")), b=dict(video="vi-choque-1", etq="GTA VI", t=w("GTA seis los arregló")))
    S.add("foto", w("En GTA cuatro, los autos"), "latigo", video="iv-choque", kb="in", kick="GTA IV · 2008", titulo="SE ABOLLABAN Y DOBLABAN", tt=w("se abollaban"), fst=90)
    S.add("foto", w("Y los personajes"), "latigo", video="iv-euphoria-1", kb="in", kick="MOTOR EUPHORIA", titulo="NO CAÍAN COMO MUÑECOS", tt=w("no caían"), fst=90)
    S.add("foto", w("se agarraban"), "latigo", video="iv-euphoria-2", kb="out")
    S.add("comparar", w("Un choque a toda velocidad"), "panel", kick="EL MISMO CHOQUE",
          a=dict(video="iv-vs-v-a", etq="GTA IV", t=w("Un choque")), b=dict(video="iv-vs-v-b", etq="GTA V", t=w("En GTA cinco, salías")))
    S.add("titulo", w("Cinco años después"), "flash", kick="GTA V · 2013", l1="EN FÍSICA", l2="UN PASO ATRÁS", t1=w("suavizó"), t2=w("un paso atrás"))
    S.add("foto", w("GTA seis regresó"), "latigo", video="vi-choque-2", kb="in", kick="GTA VI · 2026", titulo="REGRESA LA DEFORMACIÓN", tt=w("se deforman"), fst=92)
    S.add("foto", w("y ahora hasta"), "latigo", video="vi-policia-2", kb="in", titulo="Y CARGAS GASOLINA", tt=w("gasolina"))
    S.add("comparar", w("Pero la física no es"), "flash", kick="22 AÑOS DESPUÉS",
          a=dict(video="sa-cuerpo3", etq="2004", t=w("San Andreas")), b=dict(video="vi-gym", etq="2026", t=w("veintidós años")))
    cta(S, "Cuáles son", "EN EL VIDEO COMPLETO")
