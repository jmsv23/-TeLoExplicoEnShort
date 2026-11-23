"""Dirección visual del video largo. Una función por sección del guion (mismo id).

S.w("frase") → tiempo absoluto en que la voz dice la frase. S.add(tipo, t, entrada, **params).
Entradas: corte | fundido | iris | barrido | latigo | zoom | negro. Cada una tiene una causa en pantalla.
Regla: algo cambia cada 1.5–3 s (texto que entra, cifra que cuenta, Ken Burns, cambio de plano).
"""


def clip(S, name, tag="", entrada="iris"):
    b = S.clip_beat(name)
    S.add("clip", b["start"], entrada, clip=name, tag=tag)


def frio(S):
    clip(S, "connery-bond-james-bond", "DR. NO · 1962", entrada="corte")
    S.add("seis", S.w("Desde"), "negro", imgs=["connery-drno-esmoquin", "lazenby-ohmss", "moore-silla-007",
          ("dalton-tld-esmoquin", "22% 30%"), "brosnan-retrato", "craig-casino-esmoquin"],
          t6=S.w("seis actores"), t7=S.w("al séptimo"), label="1962 — 2026 · SAGA OFICIAL")
    S.add("foto", S.w("Robert Pattinson"), "iris", img="pattinson-007-primera-imagen", bn=False, sombra="l", kb="in",
          kick="EL SÉPTIMO", l2="PATTINSON", t2=S.w("Robert Pattinson") + 0.3, pos="60% 40%")
    S.add("foto", S.w("El vampiro"), "corte", img="pattinson-crepusculo", kick="CREPÚSCULO · 2008", kb="l", pos="50% 30%")
    S.add("foto", S.w("El Batman"), "corte", img="pattinson-batman", kick="THE BATMAN · 2022", kb="r")
    S.add("foto", S.w("Y ahora"), "zoom", img="pattinson-007-logo", bn=False, sombra="l", kb="in", pos="70% 40%",
          l2="007", fs2=230, t2=S.w("cero cero siete"))
    S.add("comentarios", S.w("internet se partió"), "barrido", img="pattinson-retrato",
          centro="INTERNET, DIVIDIDO", tc=S.w("se partió"), fsc=110,
          items=[("“La mejor elección en veinte años”", "+", S.w("Unos dicen"), 120, 120),
                 ("“Ese no es Bond”", "-", S.w("Otros"), 1100, 140),
                 ("“Ya demostró todo con Batman”", "+", S.w("mejor elección") + 0.6, 160, 720),
                 ("“El peor error de la saga”", "-", S.w("peor error"), 1080, 740)])
    S.add("titulo", S.w("Yo no te voy"), "zoom", kick="SEIS EXPEDIENTES", l1="TENEMOS NUEVO", l2="JAMES BOND",
          t1=S.w("Te voy a mostrar"), t2=S.w("cada uno"), sub="¿Pattinson está a la altura?", ts=S.w("Porque esta película"))
    S.add("foto", S.w("quédate hasta"), "barrido", img="pattinson-retrato", sombra="l", kb="r", pos="70% 30%",
          kick="AL FINAL", l1="¿A QUIÉN SE PARECE", l2="SU CASO?", t1=S.w("a cuál de todos"), t2=S.w("el caso de"))


def noticia(S):
    S.add("foto", S.w("Primero"), "iris", img="pattinson-007-logo", bn=False, sombra="l", kb="in", pos="70% 40%",
          kick="LO QUE SABEMOS", l1="JAMES BOND", l2="VOLVERÁ", t1=S.w("James Bond volverá"), t2=S.w("volverá"))
    S.add("foto", S.w("La película la dirige"), "barrido", img="villeneuve-retrato", sombra="l", kb="l", pos="65% 30%",
          kick="DIRECTOR", l2="VILLENEUVE", t2=S.w("Denis Villeneuve"), sub="El director de Dune", ts=S.w("el director de Dune"))
    S.add("dato", S.w("Todavía no tiene"), "zoom", kick="SIN TÍTULO · SE FILMA EL PRÓXIMO AÑO", num="2028", cuenta=False,
          label="llega a los cines", tn=S.w("llegaría"), tl=S.w("a los cines"))
    S.add("procon", S.w("A favor de Pattinson"), "latigo", img="pattinson-retrato", pos="25% 30%", bloques=[
        ("A FAVOR", "oro", [("De los más respetados de su generación", S.w("respetados")),
                            ("Ya cargó una franquicia: The Batman", S.w("franquicia")),
                            ("40 años: puede quedarse varias películas", S.w("cuarenta años"))]),
        ("EN CONTRA", "rojo", [("“Una elección demasiado obvia”", S.w("demasiado obvia")),
                               ("No tiene la imagen clásica de Bond", S.w("imagen clásica")),
                               ("Amazon controla la saga desde 2025", S.w("Amazon que"))])])
    S.add("escala", S.w("Antes de seguir"), "iris", img="pattinson-007-primera-imagen", pos="60% 35%",
          pregunta="Tu calificación, del 1 al 10", tq=S.w("tu calificación"), tn=S.w("del uno al diez"),
          cta="AL FINAL VEMOS SI CAMBIASTE", tcta=S.w("Al final vemos"))


def connery(S):
    S.add("ficha", S.w("Expediente uno"), "iris", img="connery-drno-esmoquin", kick="EXPEDIENTE 01 / 06",
          nombre="SEAN", apellido="CONNERY", tn=S.w("Sean Connery"),
          datos=[("PELÍCULAS", "6", S.w("Seis películas")), ("ERA", "62–71", S.w("mil novecientos sesenta")),
                 ("DEBUT", "32 años", S.w("treinta y dos"))], sin_cuenta={1: True},
          recepcion=None)
    S.add("poster", S.w("Hoy es el Bond"), "barrido", img="poster-drno", kick="HOY, EL BOND DE REFERENCIA",
          l2="PERO…", t2=S.w("Pero en su momento"), sub="Su creador no lo quería.", ts=S.w("no lo quería"), fs2=120)
    S.add("foto", S.w("Ian Fleming"), "barrido", img="fleming-retrato", sombra="l", kb="r", pos="55% 35%",
          kick="IAN FLEMING", l1="EL CREADOR", l2="NO LO QUERÍA", t1=S.w("Ian Fleming") + 0.4, t2=S.w("lo describió"))
    S.add("cita", S.w("un doble de acción"), "negro", img="connery-goldfinger-db5", texto="Un doble de acción con demasiado músculo.",
          autor="IAN FLEMING, SOBRE CONNERY", tq=S.w("un doble de acción"), ta=S.w("Él imaginaba"))
    S.add("foto", S.w("Connery le respondió"), "latigo", img="connery-goldfinger-db5", sombra="b", kb="l",
          kick="LA RESPUESTA DE CONNERY", sello="SNOB", tsello=S.w("snob"))
    S.add("foto", S.w("Y entonces pasó"), "zoom", img="connery-drno-esmoquin", sombra="l", kb="in", pos="60% 30%",
          kick="EN LAS NOVELAS DE FLEMING", l1="RAÍCES", l2="ESCOCESAS", t1=S.w("raíces escocesas"), t2=S.w("escocesas"),
          sub="Como Connery.", ts=S.w("Como Connery"))
    clip(S, "connery-laser", "GOLDFINGER · 1964")
    S.add("procon", S.w("A favor inventó"), "negro", img="connery-drno-esmoquin", pos="30% 30%", bloques=[
        ("A FAVOR", "oro", [("Inventó la actitud de Bond", S.w("inventó")),
                            ("Humor seco, elegancia, peligro", S.w("El humor seco"))]),
        ("EN CONTRA", "rojo", [("Su trato a las mujeres no envejeció bien", S.w("visto con ojos"))])])
    S.add("leccion", S.w("Primera lección"), "zoom", kick="LECCIÓN 01", texto="Hasta el creador del personaje se equivocó.",
          tq=S.w("hasta el creador"))


def lazenby(S):
    S.add("ficha", S.w("Expediente dos"), "iris", img="lazenby-ohmss", pos="40% 30%", kick="EXPEDIENTE 02 / 06",
          nombre="GEORGE", apellido="LAZENBY", tn=S.w("George Lazenby"),
          datos=[("PELÍCULAS", "1", S.w("Australiano")), ("AÑO", "1969", S.w("modelo de comerciales")),
                 ("DEBUT", "30 años", S.w("treinta años"))], sin_cuenta={1: True},
          recepcion=(22, S.w("desde la primera escena")))
    clip(S, "lazenby-other-fella", "AL SERVICIO SECRETO DE SU MAJESTAD · 1969")
    S.add("cita", S.w("Esto nunca le pasó"), "negro", texto="Esto nunca le pasó al otro tipo.",
          autor="LAZENBY, MIRANDO A CÁMARA · 1969", tq=S.w("Esto nunca le pasó"), ta=S.w("mirando a la cámara"), gap=0.12)
    S.add("foto", S.w("La recepción fue fría"), "barrido", img="lazenby-ohmss-2", sombra="l", kb="r", pos="60% 30%",
          kick="LA CRÍTICA", l1="ACENTO · EXPERIENCIA", l2="NO ERA CONNERY", t1=S.w("su acento"), t2=S.w("que no era Connery"), fs2=110)
    S.add("dato", S.w("Y antes del estreno"), "zoom", img="lazenby-ohmss", num="1", cuenta=False,
          kick="“BOND ESTÁ PASADO DE MODA”", label="una sola película", tn=S.w("Una sola película"), tl=S.w("Una sola película"),
          tk=S.w("Su representante"))
    S.add("foto", S.w("A favor hoy"), "barrido", img="lazenby-ohmss", sombra="l", kb="in", pos="45% 30%",
          kick="＋ A FAVOR", l1="HOY, DE LAS FAVORITAS", sub="Uno de los finales más tristes de la saga.", ts=S.w("finales más tristes"),
          t1=S.w("favoritas"))
    clip(S, "lazenby-all-the-time", "EL FINAL · 1969", entrada="negro")
    S.add("foto", S.w("En contra una actuación"), "fundido", img="lazenby-ohmss-2", sombra="l", kb="out", pos="60% 30%",
          kick="－ EN CONTRA", l1="ACTUACIÓN RÍGIDA", t1=S.w("actuación rígida"), sello="GUARDA ESTE NOMBRE",
          tsello=S.w("Guarda este nombre"), fsello=46)


def moore(S):
    S.add("ficha", S.w("Expediente tres"), "iris", img="moore-silla-007", pos="50% 30%", kick="EXPEDIENTE 03 / 06",
          nombre="ROGER", apellido="MOORE", tn=S.w("Roger Moore"),
          datos=[("PELÍCULAS", "7", S.w("Siete películas")), ("ERA", "73–85", S.w("mil novecientos setenta")),
                 ("DEBUT", "45 años", S.w("cuarenta y cinco"))], sin_cuenta={1: True},
          recepcion=(45, S.w("la edad")))
    S.add("dato", S.w("En su última película"), "zoom", img="moore-traje", num="57", kick="EN SU ÚLTIMA PELÍCULA",
          label="años · el bond más veterano", tn=S.w("cincuenta y siete"), tl=S.w("cincuenta y siete") + 0.5)
    S.add("foto", S.w("Moore no intentó"), "barrido", img="moore-traje", sombra="l", kb="r", pos="60% 30%",
          kick="A SU MANERA", l1="CEJAS · BROMAS", l2="ENCANTO", t1=S.w("cejas levantadas"), t2=S.w("encanto"))
    clip(S, "moore-cocodrilos-voz", "VIVE Y DEJA MORIR · 1973")
    clip(S, "moore-anders", "EL HOMBRE DEL REVÓLVER DE ORO · 1974", entrada="corte")
    S.add("procon", S.w("A favor convirtió"), "negro", img="moore-silla-007", pos="30% 30%", bloques=[
        ("A FAVOR", "oro", [("Bond, un éxito para toda la familia", S.w("convirtió"))]),
        ("EN CONTRA", "rojo", [("Casi comedia: Bond perdió el peligro", S.w("casi comedia"))])])
    S.add("leccion", S.w("Segunda lección"), "zoom", kick="LECCIÓN 02",
          texto="El público aceptó un Bond completamente distinto.", tq=S.w("el público aceptó"))


def dalton(S):
    S.add("ficha", S.w("Expediente cuatro"), "iris", img="dalton-tld-esmoquin", pos="25% 30%", kick="EXPEDIENTE 04 / 06",
          nombre="TIMOTHY", apellido="DALTON", tn=S.w("Timothy Dalton"),
          datos=[("PELÍCULAS", "2", S.w("Dos películas")), ("ERA", "87–89", S.w("en mil novecientos")),
                 ("DEBUT", "41 años", S.w("cuarenta y un"))], sin_cuenta={1: True},
          recepcion=(55, S.w("cuarenta y un") + 1.0))
    clip(S, "dalton-bond-james-bond", "SU NOMBRE ES PELIGRO · 1987")
    S.add("foto", S.w("Dalton leyó"), "barrido", img="dalton-tld-arma", sombra="l", kb="r", pos="60% 35%",
          kick="FIEL A LAS NOVELAS", l1="SERIO · DURO", l2="ATORMENTADO", t1=S.w("serio"), t2=S.w("atormentado"), fs2=112)
    S.add("foto", S.w("Y al público"), "latigo", video="dalton-ltk", kb="in", kick="LICENCIA PARA MATAR · 1989",
          sello="TAQUILLA BAJA EN EE.UU.", tsello=S.w("rindió por debajo"), fsello=42)
    S.add("dato", S.w("problemas legales"), "zoom", num="6", suf=" años", kick="1989 — 1995",
          label="la saga, congelada", tn=S.w("seis años"), tl=S.w("seis años") + 0.4)
    S.add("procon", S.w("A favor hoy muchos"), "negro", img="dalton-tld-arma", pos="30% 35%", bloques=[
        ("A FAVOR", "oro", [("El más parecido al Bond de los libros", S.w("más parecido"))]),
        ("EN CONTRA", "rojo", [("Llegó en el momento equivocado", S.w("momento equivocado"))])])
    S.add("leccion", S.w("Tercera lección"), "zoom", kick="LECCIÓN 03",
          texto="A veces el público tarda años en darte la razón.", tq=S.w("a veces el público"))


def brosnan(S):
    S.add("ficha", S.w("Expediente cinco"), "iris", img="brosnan-retrato", pos="50% 25%", kick="EXPEDIENTE 05 / 06",
          nombre="PIERCE", apellido="BROSNAN", tn=S.w("Pierce Brosnan"),
          datos=[("PELÍCULAS", "4", S.w("Cuatro películas")), ("ERA", "95–02", S.w("mil novecientos noventa")),
                 ("DEBUT", "42 años", S.w("cuarenta y dos"))], sin_cuenta={1: True},
          recepcion=(85, S.w("cuarenta y dos") + 1.0))
    S.add("foto", S.w("Lo curioso"), "barrido", img="brosnan-remington-steele", sombra="l", kb="r", pos="60% 30%",
          kick="REMINGTON STEELE", l1="CASI BOND", l2="EN 1986", t1=S.w("casi diez años"), t2=S.w("antes"),
          sub="Su contrato con la serie se lo impidió.", ts=S.w("se lo impidió"), fs2=110)
    S.add("foto", S.w("Cuando por fin llegó"), "latigo", video="brosnan-tanque-muro", kb="in", kick="GOLDENEYE · 1995",
          l2="EL REGRESO", t2=S.w("GoldenEye revivió"))
    clip(S, "brosnan-corbata", "GOLDENEYE · 1995")
    S.add("foto", S.w("Un tanque por"), "corte", video="brosnan-tanque-estatua", kb="in", kick="EL EQUILIBRIO PERFECTO",
          tk=S.w("el equilibrio perfecto"), l1="ELEGANTE · DIVERTIDO", l2="CREÍBLE", t1=S.w("Elegante"), t2=S.w("creíble"))
    S.add("poster", S.w("En contra Otro día"), "barrido", img="poster-dad",
          kick="－ EN CONTRA · 2002", l2="OTRO DÍA PARA MORIR", t2=S.w("Otro día para morir"), fs2=100)
    clip(S, "brosnan-auto-invisible", "OTRO DÍA PARA MORIR · 2002")
    S.add("foto", S.w("Efectos que hoy"), "negro", video="brosnan-surf", kb="in", kick="－ EN CONTRA",
          l1="EFECTOS QUE DAN PENA", t1=S.w("Efectos"), sello="REINICIO", tsello=S.w("reiniciar todo"))


def craig(S):
    S.add("ficha", S.w("Expediente seis"), "iris", img="craig-casino-esmoquin", pos="45% 25%", kick="EXPEDIENTE 06 / 06",
          nombre="DANIEL", apellido="CRAIG", tn=S.w("Daniel Craig"),
          datos=[("PELÍCULAS", "5", S.w("Cinco películas")), ("ERA", "06–21", S.w("de dos mil seis")),
                 ("DEBUT", "38 años", S.w("treinta y ocho"))], sin_cuenta={1: True},
          recepcion=(12, S.w("treinta y ocho") + 1.0))
    S.add("foto", S.w("Cuando lo anunciaron"), "barrido", img="craig-2005-chaleco", sombra="l", kb="up", pos="50% 25%",
          kick="OCTUBRE 2005 · EL TÁMESIS", l1="CON CHALECO", l2="SALVAVIDAS", t1=S.w("chaleco salvavidas"),
          t2=S.w("salvavidas"), sub="Y la prensa lo destrozó.", ts=S.w("la prensa lo destrozó"))
    S.add("titulo", S.w("Lo llamaron"), "latigo", kick="LA PRENSA BRITÁNICA", l2="JAMES BLONDE", t2=S.w("James Blonde"),
          sub="“Muy bajo.” “Sin cara de Bond.”", ts=S.w("muy bajo"))
    S.add("navegador", S.w("Hasta crearon"), "zoom", img="craig-casino-esmoquin", titulo="2005 · PÁGINAS DE PROTESTA",
          urls=[("danielcraigisnotbond.com", S.w("páginas web")), ("craignotbond.com", S.w("pedir que lo sacaran"))])
    S.add("poster", S.w("Un año después"), "negro", img="poster-casino",
          kick="UN AÑO DESPUÉS · 2006", l2="CASINO ROYALE", t2=S.w("Casino Royale"), fs2=110)
    clip(S, "craig-parkour-voz", "CASINO ROYALE · 2006")
    clip(S, "craig-shaken", "", entrada="corte")
    S.add("poster", S.w("La crítica se rindió"), "latigo", img="poster-skyfall",
          kick="LA CRÍTICA SE RINDIÓ · 2012", l2="SKYFALL", t2=S.w("Skyfall"), fs2=150)
    clip(S, "craig-skyfall-voz", "SKYFALL · 2012")
    S.add("dato", S.w("Más de mil cien"), "zoom", img="craig-skyfall-londres", pre="$", num="1,108", suf=" M", cuenta=False,
          kick="SKYFALL · 2012", label="la más exitosa de la saga", tn=S.w("Más de mil cien"), tl=S.w("La más exitosa"), fs=260)
    S.add("procon", S.w("A favor le dio"), "negro", img="craig-skyfall-londres", pos="30% 30%", bloques=[
        ("A FAVOR", "oro", [("Emociones, heridas y consecuencias", S.w("emociones"))]),
        ("EN CONTRA", "rojo", [("Demasiado serio: se perdió la diversión", S.w("demasiado serio"))])])


def exito(S):
    S.add("titulo", S.w("Entonces"), "iris", kick="LA PREGUNTA", l1="¿QUIÉN FUE", l2="EL MEJOR?",
          t1=S.w("quién fue"), t2=S.w("el mejor"), sub="Depende de cómo lo midas.", ts=S.w("Depende"))
    S.add("podio", S.w("Por taquilla"), "zoom", kick="TRES MEDIDAS · TRES GANADORES", items=[
        ("TAQUILLA", "CRAIG", "Skyfall · $1,108 M", "craig-skyfall-londres", S.w("Por taquilla")),
        ("PELÍCULAS", "MOORE", "Siete películas", "moore-silla-007", S.w("Por número")),
        ("INFLACIÓN · EE.UU.", "CONNERY", "Operación Trueno · 1965", "connery-goldfinger-db5", S.w("si ajustas"))])


def patron(S):
    S.add("versus", S.w("Te acuerdas de Lazenby"), "iris", a=("lazenby-ohmss", "SE RINDIÓ", S.w("Uno se rindió")),
          b=("craig-casino-esmoquin", "AGUANTÓ", S.w("El otro aguantó")),
          centro="Los dos Bond más criticados", tc=S.w("los dos Bond"))
    S.add("dato", S.w("Y Pattinson ya vivió"), "latigo", img="pattinson-crepusculo", num="75", suf=" mil",
          kick="2008 · CREPÚSCULO", label="firmas para sacarlo", tn=S.w("setenta y cinco mil"), tl=S.w("firmaron"),
          tk=S.w("dos veces"))
    clip(S, "pattinson-spider-monkey", "CREPÚSCULO · 2008")
    S.add("foto", S.w("Y en dos mil diecinueve"), "barrido", img="pattinson-batman", kb="in", kick="2019 · THE BATMAN",
          sello="PETICIONES", tsello=S.w("peticiones"))
    clip(S, "pattinson-vengeance", "THE BATMAN · 2022")
    S.add("foto", S.w("Las dos veces"), "negro", img="pattinson-retrato", sombra="l", kb="r", pos="70% 30%",
          kick="LAS DOS VECES", l1="CALLÓ", l2="A MUCHOS", t1=S.w("callando"), t2=S.w("a muchos"))
    S.add("versus", S.w("Entonces será"), "latigo", a=("craig-casino-esmoquin", "¿CRAIG?", S.w("será Craig")),
          b=("lazenby-ohmss", "¿LAZENBY?", S.w("será Lazenby")))
    S.add("foto", S.w("Eso no lo decide"), "zoom", img="pattinson-007-primera-imagen", bn=False, sombra="l", kb="in",
          pos="60% 40%", kick="NO LO DECIDE INTERNET", l2="LO DECIDE LA PELÍCULA", t2=S.w("Lo decide la película"), fs2=92)


def cierre(S):
    S.add("escala", S.w("Te repito"), "iris", img="pattinson-007-logo", pos="70% 40%",
          pregunta="¿Pattinson va a llenar los zapatos de 007?", tq=S.w("Pattinson va"), tn=S.w("del uno al diez"),
          cta="SUSCRÍBETE · ANALIZAREMOS EL PRIMER ADELANTO", tcta=S.w("suscríbete"))
