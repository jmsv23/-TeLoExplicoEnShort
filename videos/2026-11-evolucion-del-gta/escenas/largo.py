"""Dirección visual del largo (estilo "Leonida sunset"). Una función por sección del guion (mismo id).

S.w("frase") → tiempo absoluto de la frase. S.add(tipo, t, entrada, **params).
Entradas: corte | fundido | panel | crece | iris | latigo | flash.
B-roll: video="<corte>" (assets/video/cortes, mudo). Imágenes: img="<nombre>" (assets/img).
"""


def clip(S, name, tag="", entrada="corte"):
    b = S.clip_beat(name)
    S.add("clip", b["start"] - 0.3, entrada, clip=name, tag=tag)


def hook(S):
    w = S.w
    S.add("foto", w("En mil novecientos"), "corte", video="gta1-calle", kb="in",
          kick="1997", titulo="UN COCHECITO PIXELADO", tt=w("un cochecito"), pixel=True)
    S.add("foto", w("atropellando peatones"), "latigo", video="gta1-policia", kb="in")
    S.add("titulo", w("Hace dos días"), "flash", kick="19 DE NOVIEMBRE DE 2026", l2="GTA VI", t2=w("salió GTA"))
    S.add("versus", w("La crítica le dio"), "panel", kick="METACRITIC",
          a=("99", "LA CRÍTICA", w("noventa y nueve")), b=("¿?", "LOS JUGADORES", w("la calificación más")))
    S.add("dato", w("Y en un solo día"), "latigo", kick="EN UN SOLO DÍA", pre="$", num="3790", suf=" M", tn=w("ganó más dinero"),
          label="Más que las dos últimas Avatar juntas", tl=w("Avatar"), video="vi-atardecer")
    S.add("versus", w("Pero aquí viene lo raro"), "crece", kick="METACRITIC",
          a=("99", "LA CRÍTICA", w("Pero aquí")), b=("5", "LOS JUGADORES", w("un cinco"), "mal"))
    S.add("comparar", w("Y hay cosas que hacía"), "panel", kick="¿EVOLUCIÓN?",
          a=dict(video="sa-callejon", etq="2004", t=w("San Andreas")), b=dict(video="v-ls", etq="2013", t=w("GTA cinco te quitó")))
    S.add("galeria", w("Así que hoy"), "panel", kick="29 AÑOS DE GTA", items=[
        ("gta1-cover", "1997", w("veintinueve años")), ("gta3-cover", "2001", w("veintinueve años") + .15),
        ("vc-cover", "2002", w("veintinueve años") + .3), ("sa-cover", "2004", w("veintinueve años") + .45),
        ("iv-cover", "2008", w("juego por juego")), ("v-cover", "2013", w("juego por juego") + .15),
        ("vi-cover", "2026", w("mecánica por mecánica"))], destaca=6)
    S.add("titulo", w("Qué mejoró"), "flash", l1="¿EVOLUCIÓN", l2="O RETROCESO?", t1=w("evolución"), t2=w("retroceso"))


def origen(S):
    w = S.w
    S.add("titulo", w("Empecemos"), "panel", kick="CAPÍTULO 1 · EL ORIGEN", l1="GTA NO IBA A SER", l2="GTA", t1=w("GTA no"), t2=w("ser GTA"))
    S.add("panel", w("En los noventa"), "panel", img="rockstar-north", lado="der", kick="DUNDEE, ESCOCIA", tk=w("Escocia"),
          titulo="DMA DESIGN", tt=w("DMA Design"), sub="Hoy se llama Rockstar North.", ts=w("trabajaba en"))
    S.add("titulo", w("Race and Chase"), "flash", kick="EL NOMBRE ORIGINAL", l2="RACE'N'CHASE", t2=w("Race and Chase"),
          sub="…y podías jugar como policía", ts=w("jugar como policía"), pixel=True)
    S.add("foto", w("Pero durante las pruebas"), "latigo", video="gta1-policia", kb="in",
          kick="UN ERROR DE PROGRAMACIÓN", tk=w("un error"), titulo="POLICÍAS LOCOS", tt=w("demasiado agresiva"))
    S.add("foto", w("Lo lógico era"), "panel", video="gta1-calle", kb="l",
          kick="SE QUEDÓ EL ERROR", titulo="EL CRIMINAL ES EL HÉROE", tt=w("el criminal"))
    S.add("lista", w("Y otro dato"), "panel", kick="YA EXISTÍAN EN 1997", items=[
        ("LIBERTY CITY", "Nueva York", w("Liberty City"), "1"), ("VICE CITY", "Miami", w("Vice City"), "2"),
        ("SAN ANDREAS", "California", w("San Andreas"), "3")])
    S.add("panel", w("El juego se vendió"), "crece", img="gta1-cover", lado="izq", vertical=True,
          kick="ESCÁNDALO A PROPÓSITO", tk=w("escándalo"), titulo="PUBLICIDAD GRATIS", tt=w("publicidad gratis"),
          sub="Políticos y periódicos lo atacaron.", ts=w("Los políticos"))
    S.add("foto", w("Dos años después"), "panel", video="gta2-calle", kb="in",
          kick="1999", titulo="GTA 2", tt=w("GTA dos"), sub="Pandillas que te respetan… o te odian.", ts=w("pandillas"))
    S.add("foto", w("Pero seguía viéndose"), "latigo", video="gta2-calle2", kb="out",
          kick="TODAVÍA DESDE ARRIBA", tk=w("desde arriba"))


def salto3d(S):
    w = S.w
    S.add("titulo", w("En dos mil uno"), "flash", kick="CAPÍTULO 2 · 2001", l2="GTA III", t2=w("GTA tres"),
          sub="El salto a 3D", ts=w("tres dimensiones"))
    S.add("foto", w("y podías caminar"), "latigo", video="gta3-ciudad", kb="in", kick="LIBERTY CITY EN 3D", tk=w("Liberty City"))
    S.add("foto", w("Hoy suena normal"), "panel", video="gta3-calle", kb="l",
          kick="EL PRIMER MUNDO ABIERTO MODERNO", tk=w("inventó"), titulo="MEDIO MUNDO LO COPIÓ", tt=w("lo copió"))
    S.add("panel", w("El protagonista, Claude"), "panel", img="claude", lado="der", vertical=True,
          kick="CLAUDE", titulo="0 PALABRAS", tt=w("Ni una"), sub="No habla en todo el juego.", ts=w("no dice"))
    S.add("foto", w("Y el juego casi sale"), "latigo", video="gta3-ciudad", kb="in",
          kick="RETRASADO TRAS EL 11-S", tk=w("Torres Gemelas"))
    S.add("comparar", w("hasta las patrullas"), "panel", kick="LAS PATRULLAS CAMBIARON",
          a=dict(img="gta3-cover", etq="AZUL", t=w("azul con blanco"), fs=120), b=dict(video="gta3-calle", etq="BLANCO Y NEGRO", t=w("blanco y negro"), fs=100))


def vicecity(S):
    w = S.w
    S.add("titulo", w("Un año después"), "flash", kick="CAPÍTULO 3 · 2002", l2="VICE CITY", t2=w("Vice City"), sub="1986, neón y radio", ts=w("neón"))
    S.add("foto", w("y una radio"), "latigo", video="vc-atardecer", kb="in", kick="LA MÚSICA ERA LA MITAD DEL JUEGO", tk=w("la mitad"))
    S.add("panel", w("Tommy Vercetti"), "panel", img="tommy", lado="izq", vertical=True,
          kick="TOMMY VERCETTI", titulo="RAY LIOTTA", tt=w("Ray Liotta"), sub="La voz de Goodfellas.", ts=w("Goodfellas"))
    S.add("foto", w("Pero tenía un problema"), "latigo", video="vc-tommy-auto", kb="in",
          kick="SU GRAN DEBILIDAD", titulo="NO SABÍA NADAR", tt=w("no sabía nadar"))
    S.add("comparar", w("Y ahora viene la comparación"), "flash", kick="LA MISMA CIUDAD, 24 AÑOS DESPUÉS",
          a=dict(video="vc-vs-vi-a", etq="2002", t=w("dos mil dos")), b=dict(video="vc-vs-vi-b", etq="2026", t=w("dos mil veintiséis")))
    S.add("comparar", w("La Vice City original"), "panel", kick="TAMAÑO",
          a=dict(img="mapa-vc2002", etq="< 10 KM²", t=w("menos de diez"), fs=110), b=dict(img="mapa-leonida", etq="LEONIDA", t=w("Leonida"), fs=110), vs=False)
    S.add("foto", w("con pantanos"), "latigo", video="vi-pantano", kb="in", kick="UN ESTADO COMPLETO", tk=w("pantanos"))
    S.add("dato", w("Según Rockstar"), "panel", kick="SEGÚN ROCKSTAR", num="2", suf="×", tn=w("casi el doble"),
          label="el mapa de GTA 5", tl=w("GTA cinco"), img="mapa-leonida")
    S.add("foto", w("Y Vice City, sola"), "latigo", video="vi-aereo", kb="in",
          kick="VICE CITY", titulo="LA CIUDAD MÁS GRANDE DE ROCKSTAR", tt=w("la ciudad más grande"), fst=88)
    S.add("panel", w("Y por cierto"), "crece", img="ocean-view", lado="der",
          kick="REGRESÓ", titulo="HOTEL OCEAN VIEW", tt=w("Ocean View"), sub="En Ocean Beach, como en 2002.", ts=w("Ocean Beach"))


def sanandreas(S):
    w = S.w
    S.add("titulo", w("En dos mil cuatro"), "flash", kick="CAPÍTULO 4 · 2004", l1="EL FAVORITO DE MUCHOS", l2="SAN ANDREAS",
          t1=w("para muchos"), t2=w("San Andreas"))
    clip(S, "cj-here-we-go", "AH SH*T, HERE WE GO AGAIN")
    S.add("foto", w("Carl Johnson regresa"), "panel", video="sa-llegada", kb="in", kick="CARL JOHNSON", tk=w("Carl Johnson"))
    S.add("foto", w("Pero lo que hizo legendario"), "latigo", video="sa-callejon", kb="l",
          titulo="TODO LO QUE PODÍAS HACER", tt=w("todo lo que podías"))
    S.add("comparar", w("Si CJ comía"), "panel", kick="TU CUERPO CAMBIABA",
          a=dict(video="sa-gordo", etq="PIZZA", t=w("engordaba")), b=dict(video="sa-musculo", etq="GYM", t=w("ganaba músculo")))
    S.add("foto", w("Y la gente en la calle"), "latigo", video="sa-gym", kb="in", kick="LA GENTE REACCIONABA", tk=w("reaccionaba"))
    S.add("lista", w("Podías nadar"), "panel", kick="EN SAN ANDREAS PODÍAS", gap=18, fsn=90, fsi=60, items=[
        ("NADAR Y BUCEAR", "Tommy no podía", w("nadar"), "✓"), ("TENER NOVIAS", "y salir con ellas", w("tener novias"), "✓"),
        ("TATUARTE Y CORTARTE EL PELO", "", w("tatuarte"), "✓"), ("CONQUISTAR TERRITORIO", "guerras de pandillas", w("conquistar"), "✓"),
        ("VOLAR CON JETPACK", "", w("jetpack"), "✓")])
    S.add("galeria", w("Y tres ciudades"), "crece", kick="TRES CIUDADES", items=[
        ("mapa-sa", "LOS SANTOS", w("Los Santos"), "80% 80%"), ("mapa-sa", "SAN FIERRO", w("San Fierro"), "10% 40%"),
        ("mapa-sa", "LAS VENTURAS", w("Las Venturas"), "85% 10%")])
    S.add("comparar", w("Y aquí viene lo polémico"), "flash", kick="TAMAÑO DEL MAPA",
          a=dict(img="mapa-sa", etq="SAN ANDREAS", t=w("San Andreas"), fs=110), b=dict(video="iv-calle", etq="GTA IV", t=w("GTA cuatro"), fs=120))
    S.add("dato", w("Hoy, en Metacritic"), "panel", kick="EL MEJOR CALIFICADO POR LOS JUGADORES", pre="", num="9.1", tn=w("nueve punto uno"),
          label="Recuerda este número", tl=w("Recuerda"), img="sa-cover", cuenta=False)


def polemicas(S):
    w = S.w
    S.add("titulo", w("Pero San Andreas también"), "flash", kick="EL ESCÁNDALO MÁS GRANDE", l2="HOT COFFEE", t2=w("Hot Coffee"))
    S.add("panel", w("Dentro del disco"), "panel", img="sa-cover", lado="der", vertical=True,
          kick="ESCONDIDO EN EL DISCO", titulo="UN MINIJUEGO PROHIBIDO", tt=w("minijuego"), sub="Un fan lo desbloqueó con un mod.", ts=w("un fan"))
    S.add("lista", w("Cuando se supo"), "panel", kick="LO QUE PASÓ", items=[
        ("SOLO PARA ADULTOS", "lo reclasificaron", w("solo para adultos"), "1"), ("FUERA DE LAS TIENDAS", "retiro masivo", w("sacaron de las tiendas"), "2"),
        ("DECENAS DE MILLONES", "en reimpresiones y demandas", w("decenas de millones"), "3")])
    S.add("titulo", w("Y en medio de todo"), "panel", kick="EL ENEMIGO DE GTA", l2="JACK THOMPSON", t2=w("Jack Thompson"),
          sub="demanda tras demanda", ts=w("demanda tras"))
    S.add("titulo", w("En dos mil ocho"), "crece", kick="2008", l1="LE QUITARON LA LICENCIA", t1=w("le quitaron"), l2="¿DE DÓNDE ERA?", t2=w("de dónde era"))
    S.add("foto", w("De Miami"), "flash", video="vi-aereo2", kb="in", kick="JACK THOMPSON ERA DE…", titulo="MIAMI", tt=w("De Miami"),
          sub="La ciudad real detrás de Vice City.", ts=w("La ciudad real"))


def gta4(S):
    w = S.w
    S.add("titulo", w("En dos mil ocho"), "flash", kick="CAPÍTULO 5 · 2008", l2="GTA IV", t2=w("le quitó cosas"), sub="Le quitó cosas a GTA", ts=w("le quitó"))
    S.add("lista", w("GTA cuatro no tenía"), "panel", kick="ADIÓS A…", items=[
        ("GIMNASIO", "", w("gimnasio"), "✗"), ("ENGORDAR", "", w("engordar"), "✗"), ("JETPACK", "", w("jetpack"), "✗")])
    S.add("foto", w("Rockstar quería realismo"), "latigo", video="iv-calle", kb="in", kick="APOSTÓ TODO AL", titulo="REALISMO", tt=w("realismo"))
    S.add("panel", w("Niko Bellic"), "panel", img="niko", lado="izq", vertical=True, kick="NIKO BELLIC", titulo="EL SUEÑO AMERICANO", tt=w("sueño americano"),
          sub="Y su primo Roman no lo deja en paz.", ts=w("su primo"))
    clip(S, "roman-bowling", "«LET'S GO BOWLING»")
    S.add("foto", w("Pero lo que GTA cuatro hizo"), "flash", video="iv-euphoria-1", kb="in", kick="MOTOR EUPHORIA", tk=w("Euphoria"),
          titulo="FÍSICA QUE REACCIONA", tt=w("reaccionaban"))
    S.add("foto", w("Se tropezaban"), "latigo", video="iv-euphoria-2", kb="out")
    S.add("foto", w("Y los choques eran brutales"), "panel", video="iv-choque", kb="in", kick="CHOQUES BRUTALES", tk=w("brutales"),
          titulo="SE SENTÍAN PESADOS", tt=w("pesados"))
    S.add("comparar", w("Y aquí está la parte"), "flash", kick="FÍSICA DE CHOQUES",
          a=dict(video="iv-vs-v-a", etq="GTA IV", t=w("Y aquí está")), b=dict(video="iv-vs-v-b", etq="GTA V", t=w("GTA cinco, cinco años")))
    S.add("titulo", w("En física, GTA cinco"), "crece", l1="EN FÍSICA", l2="UN PASO ATRÁS", t1=w("En física"), t2=w("paso atrás"))


def gta5(S):
    w = S.w
    S.add("foto", w("Pero en todo lo demás"), "flash", video="v-ls", kb="in", kick="CAPÍTULO 6 · 2013", titulo="GTA V", tt=w("un monstruo"))
    S.add("panel", w("con tres protagonistas"), "panel", img="mft-arte", lado="der", kick="TRES PROTAGONISTAS", tk=w("tres protagonistas"),
          titulo="MICHAEL · FRANKLIN · TREVOR", tt=w("Michael"), fst=80)
    S.add("foto", w("Y podías cambiar"), "latigo", video="v-cambio", kb="in", kick="CAMBIO DE PERSONAJE", tk=w("cambiar entre"))
    S.add("dato", w("En su primer día"), "flash", kick="PRIMER DÍA", pre="$", num="800", suf=" M", tn=w("ochocientos millones"),
          label="y $1,000 M en solo tres días", tl=w("En tres días"), img="v-cover")
    S.add("titulo", w("Ningún producto"), "panel", kick="RÉCORD GUINNESS", l1="EL MÁS RÁPIDO DE LA HISTORIA", l2="$1,000 M", t1=w("Ningún producto"), t2=w("tan rápido"))
    S.add("lista", w("Y luego no se fue nunca"), "panel", kick="3 GENERACIONES", items=[
        ("PLAYSTATION 3", "2013", w("PlayStation tres"), "3"), ("PLAYSTATION 4", "2014", w("PlayStation cuatro"), "4"),
        ("PLAYSTATION 5", "2022", w("PlayStation cinco"), "5")])
    S.add("dato", w("Hoy lleva más de"), "crece", kick="COPIAS VENDIDAS", pre="+", num="215", suf=" M", tn=w("doscientos quince"),
          label="Y GTA Online, imprimiendo dinero una década", tl=w("GTA Online"), video="v-michael")
    S.add("foto", w("El problema es que"), "latigo", video="v-ls2", kb="out", kick="EL PRECIO DEL ÉXITO", tk=w("un costo"),
          titulo="EL SIGUIENTE GTA PODÍA ESPERAR", tt=w("podía esperar"), fst=84)


def policia(S):
    w = S.w
    S.add("estrellas", w("Antes de llegar"), "flash", n=6, kick="LA POLICÍA", titulo="CÓMO EVOLUCIONÓ", tt=w("ha evolucionado"),
          on=[(k, w("La policía") + k * 0.12) for k in range(6)])
    S.add("foto", w("En GTA uno"), "panel", video="gta1-policia", kb="in", kick="GTA 1 · 1997", titulo="CARITAS DE POLICÍA", tt=w("caritas"),
          sub="Cuatro como máximo.", ts=w("Cuatro"), pixel=True)
    S.add("estrellas", w("En GTA tres llegaron"), "latigo", video="gta3-patrulla", n=6, kick="GTA III · 2001", titulo="LLEGA EL EJÉRCITO", tt=w("ejército"),
          on=[(k, w("seis estrellas") + k * 0.1) for k in range(6)])
    S.add("foto", w("En GTA cuatro, aparecía"), "panel", video="iv-calle", kb="in", kick="GTA IV · 2008", titulo="EL CÍRCULO", tt=w("un círculo"),
          sub="Sal del círculo sin que te vean.", ts=w("Si salías"))
    S.add("foto", w("En GTA cinco, la policía"), "latigo", video="v-policia", kb="in", kick="GTA V · 2013", titulo="CONOS DE VISIÓN", tt=w("conos"))
    S.add("titulo", w("Pero había un truco"), "crece", l1="LA POLICÍA SIEMPRE SABÍA", l2="QUIÉN ERAS", t1=w("la policía siempre"), t2=w("quién eras"))
    S.add("lista", w("En GTA seis, eso se acabó"), "flash", kick="GTA VI · NECESITAN", items=[
        ("UN TESTIGO", "", w("un testigo"), "1"), ("UNA ALARMA", "", w("una alarma"), "2"), ("UNA CÁMARA", "", w("una cámara"), "3")])
    S.add("lista", w("Y te identifica"), "panel", kick="TE RECONOCEN POR", items=[
        ("TU CARA", "", w("tu cara"), "1"), ("TU ROPA", "", w("tu ropa"), "2"), ("TU AUTO", "", w("tu auto"), "3")], fsn=100)
    S.add("foto", w("Si te cambias de ropa"), "latigo", video="vi-policia-1", kb="in", kick="LES PIERDES LA PISTA", tk=w("les pierdes"))
    S.add("estrellas", w("Ya no hay patrullas"), "panel", video="vi-policia-2", n=6, kick="SIN PATRULLAS EN EL MINIMAPA", titulo="LA SEXTA ESTRELLA REGRESA",
          tt=w("la sexta estrella"), on=[(k, w("sexta estrella") + k * 0.12) for k in range(6)])
    S.add("cita", w("Uno de los jefes"), "panel", texto="En los GTA anteriores eras casi todopoderoso. Este mundo ya no funciona así.",
          autor="ROB NELSON · ROCKSTAR NORTH", tq=w("eras casi"), ta=w("La gente se defiende"), img="vi-policia-playa")


def espera(S):
    w = S.w
    S.add("titulo", w("Ahora, la pregunta"), "flash", kick="CAPÍTULO 7 · LA ESPERA", l2="¿POR QUÉ TARDÓ TANTO?", t2=w("por qué tardó"), fs2=170)
    S.add("linea", w("Mira esto"), "panel", kick="AÑOS ENTRE CADA GTA", items=[
        ("GTA → GTA 2", 2, w("Entre GTA uno")), ("GTA III → VICE CITY", 1, w("Entre GTA tres")),
        ("SAN ANDREAS → GTA IV", 4, w("Entre San Andreas")), ("GTA IV → GTA V", 5, w("Entre GTA cuatro y GTA cinco")),
        ("GTA V → GTA VI", 13, w("trece años"))])
    S.add("dato", w("Para que lo dimensiones"), "crece", kick="GTA III → GTA V", num="12", suf=" AÑOS", tn=w("menos tiempo"),
          label="Menos que entre GTA V y GTA VI (13)", tl=w("que entre GTA cinco"))
    S.add("foto", w("Y la espera tuvo"), "panel", video="vi-noche", kb="in", kick="2022 · LA GRAN FILTRACIÓN", tk=w("filtró"),
          titulo="90 VIDEOS FILTRADOS", tt=w("noventa videos"))
    S.add("panel", w("Lo hizo desde"), "latigo", img="vi-pareja", lado="der", kick="DESDE UN HOTEL", titulo="CON UN FIRE STICK", tt=w("Fire Stick"),
          sub="Un celular, una tele y un Fire Stick de Amazon.", ts=w("un celular"))
    S.add("dato", w("Luego, el primer tráiler"), "flash", kick="TRÁILER 1 · 24 HORAS", num="90", suf=" M", tn=w("noventa millones"),
          label="Récord de YouTube, aun filtrado", tl=w("récord"), video="vi-playa")
    clip(S, "trailer1-lucia", "TRÁILER 1 · 2023")
    S.add("dato", w("El segundo tráiler"), "flash", kick="TRÁILER 2 · UN DÍA", num="475", suf=" M", tn=w("cuatrocientos setenta"),
          label="vistas sumando plataformas", tl=w("sumando"), video="vi-yate")
    S.add("lista", w("Y después vinieron"), "panel", kick="LOS RETRASOS", items=[
        ("OTOÑO 2025", "la fecha original", w("otoño"), "✗"), ("26 MAYO 2026", "otra vez no", w("mayo"), "✗"),
        ("19 NOV 2026", "hace dos días", w("diecinueve de noviembre"), "✓")])


def gta6(S):
    w = S.w
    S.add("dato", w("Y valió la pena"), "flash", kick="PREVENTAS + PRIMER DÍA", pre="$", num="3790", suf=" M", tn=w("tres mil setecientos"),
          label="Lanzamiento récord de la historia", tl=w("noventa millones de dólares"), img="vi-keyart")
    S.add("foto", w("Take Two lo llamó"), "latigo", video="vi-explosion", kb="in", kick="TAKE-TWO", titulo="NADA SE LE ACERCA", tt=w("se le acerca"))
    S.add("panel", w("Jason y Lucía"), "panel", img="jl-armas", lado="izq", kick="JASON Y LUCÍA", tk=w("Jason y Lucía"),
          titulo="LA PRIMERA PROTAGONISTA EN 3D", tt=w("la primera mujer"), fst=84, sub="Historia de unas 80 horas.", ts=w("ochenta horas"))
    S.add("titulo", w("Y lo mejor para"), "flash", kick="PARA LOS FANS DE SIEMPRE", l2="EASTER EGGS", t2=w("referencias"))
    S.add("foto", w("Afuera de la casa"), "panel", video="vi-barco", kb="in", kick="EL VELERO DE MICHAEL", tk=w("velero"),
          titulo="SU GPS MARCA LOS SANTOS", tt=w("el mapa de Los Santos"), fst=86)
    S.add("lista", w("En el celular"), "panel", kick="MÁS REFERENCIAS", items=[
        ("RACE'N'CHASE", "el nombre original de GTA", w("Race and Chase"), "1"), ("SKUNK APE", "el Pie Grande de San Andreas", w("Skunk Ape"), "2"),
        ("EL ACTOR DE NIKO", "en créditos como el sicario", w("Niko Bellic"), "3")])
    S.add("foto", w("Y sí: el gimnasio"), "flash", video="vi-gym", kb="in", kick="LO QUE GTA V TE QUITÓ", titulo="REGRESA EL GIMNASIO", tt=w("el gimnasio regresa"))
    S.add("comparar", w("Y la física de los choques"), "panel", kick="REGRESA LA DEFORMACIÓN",
          a=dict(video="iv-choque", etq="GTA IV", t=w("Y la física")), b=dict(video="vi-choque-1", etq="GTA VI", t=w("como en GTA cuatro")))
    S.add("foto", w("pierden piezas"), "latigo", video="vi-choque-2", kb="in", kick="Y AHORA", titulo="HASTA CARGAS GASOLINA", tt=w("gasolina"))


def veredicto(S):
    w = S.w
    S.add("titulo", w("Entonces"), "flash", kick="EL VEREDICTO", l1="¿POR QUÉ LOS JUGADORES", l2="LE DAN UN 5?", t1=w("por qué"), t2=w("un cinco"))
    S.add("panel", w("En Metacritic, la crítica"), "panel", img="metacritic-99", lado="der", kick="LA CRÍTICA", titulo="99 / 100", tt=w("noventa y nueve"),
          sub="Empata con Ocarina of Time.", ts=w("Ocarina"))
    S.add("versus", w("Pero la calificación"), "crece", kick="LA MAYOR DIFERENCIA DE LA HISTORIA",
          a=("99", "CRÍTICA", w("Pero la calificación")), b=("<5", "USUARIOS", w("por debajo de cinco"), "mal"))
    S.add("panel", w("Una parte es review bombing"), "panel", img="metacritic-user", lado="der", pos="0% 100%", kick="REVIEW BOMBING", tk=w("review bombing"),
          titulo="GENTE QUE NI LO TIENE", tt=w("ni siquiera"))
    S.add("lista", w("En consolas corre"), "latigo", kick="LAS QUEJAS REALES", items=[
        ("30 FPS", "en consolas", w("treinta cuadros"), "1"), ("ERRORES", "de lanzamiento", w("errores"), "2"), ("$100", "la edición de lujo", w("cien dólares"), "3")])
    S.add("panel", w("Y luego está San Andreas"), "crece", img="sa-cover", lado="izq", vertical=True, kick="22 AÑOS DESPUÉS",
          dato=("", "9.1", "", "Sigue siendo el favorito de los jugadores", w("nueve punto uno")), cuenta=False)
    S.add("comparar", w("Así que este es el resumen"), "flash", kick="29 AÑOS",
          a=dict(video="gta1-calle", etq="1997", t=w("de pixeles")), b=dict(video="vi-aereo", etq="2026", t=w("a fotorrealismo")))
    S.add("foto", w("La policía pasó"), "latigo", video="vi-policia-1", kb="in", titulo="DE CARITAS A TESTIGOS", tt=w("investigar testigos"))
    S.add("foto", w("Las ciudades pasaron"), "latigo", video="vi-pantano", kb="out", titulo="DE CIUDAD A ESTADO", tt=w("estado completo"))
    S.add("titulo", w("Pero en el camino"), "panel", l1="LA EVOLUCIÓN NO SIEMPRE", l2="FUE HACIA ADELANTE", t1=w("La evolución"), t2=w("hacia adelante"), fs2=170)


def cierre(S):
    w = S.w
    S.add("comparar", w("Ahora te toca"), "flash", kick="TÚ DECIDES",
          a=dict(img="vi-keyart", etq="GTA VI", t=w("GTA seis")), b=dict(img="cj", etq="SAN ANDREAS", t=w("San Andreas"), fs=110))
    S.add("titulo", w("Escríbeme en los comentarios"), "panel", kick="EN LOS COMENTARIOS", l2="¿TU GTA FAVORITO?", t2=w("tu GTA favorito"), fs2=170,
          sub="Yo leo todos", ts=w("Yo leo"))
    S.add("foto", w("Y si quieres más"), "crece", img="jl-atardecer", kb="in", kick="SUSCRÍBETE", tk=w("suscríbete"),
          titulo="NOS VEMOS EN LEONIDA", tt=w("Nos vemos"))
