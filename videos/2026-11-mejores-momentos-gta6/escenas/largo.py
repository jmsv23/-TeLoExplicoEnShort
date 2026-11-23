"""Dirección visual del largo: TOP 12 momentos de streamers en GTA 6 (estilo "Leonida sunset", heredado de evolucion-del-gta).

S.w("frase") → tiempo absoluto de la frase. S.add(tipo, t, entrada, **params).
Cada puesto: rank (número + streamer + vista previa muda del clip) → clip con sonido y subtítulos → titulo con el remate.
Subtítulos: (inicio, fin, texto) en segundos relativos al inicio del corte (assets/video/cortes/<clip>.mp4).
"""

SUBS = {
    "caseoh-dolores": [(2.5, 3.8, "¿Cómo se llama la serpiente?"), (8.6, 9.8, "Está en todos lados."),
                       (10.8, 13.4, "¡LA SERPIENTE SE LLAMA DOLORES!"), (15.3, 17.4, "Dios mío… juego del año."),
                       (17.6, 20.1, "La serpiente se llama Dolores."), (20.2, 21.9, "Dolores me mató a golpes."),
                       (22.0, 24.0, "No la serpiente… la Dolores de verdad."), (24.2, 25.6, "Dolores, te voy a dar de comer."),
                       (25.7, 29.4, "¡La serpiente se llama Dolores!")],
    "vanoss-gaviota": [(0.9, 2.8, "Ven aquí, no he terminado contigo."), (3.3, 5.1, "¡Vamos, hombre pepinillo!"),
                       (5.1, 8.4, "¿Por qué me haces esto?"), (8.5, 12.8, "¡Vuelve! ¡Mira mi pájaro!"),
                       (12.9, 14.3, "¿Por qué corre así?"), (14.8, 16.6, "No te caigas, está aterrado."),
                       (16.7, 21.5, "Lo persigue un tipo con un animal atropellado."),
                       (21.9, 24.4, "Es lo más «Florida man» que he visto en mi vida.")],
    "peanut-puerta": [(1.7, 4.1, "Qué buen carro, bro."), (4.3, 9.2, "¿Carro equivocado? Bueno… vámonos."),
                      (9.8, 11.9, "¡Oh, no! Adelante…"), (12.0, 13.8, "Rómpete los nudillos en mi cara."),
                      (20.9, 22.6, "¿¡QUÉ ESTÁ PASANDO!?"), (23.5, 25.3, "¡Este tipo está loquísimo!"),
                      (25.8, 27.6, "¡Vete al diablo!"), (30.9, 32.0, "¿Quién era ese tipo?")],
    "lirik-perro": [(1.2, 2.3, "¿¡Qué demonios!?"), (4.8, 5.9, "Sí… ¿qué diablos?"), (7.2, 8.1, "Dios mío."),
                    (10.1, 11.8, "Ok, me estoy volviendo loco."), (12.0, 13.2, "¿ESO ES UN PERRO?"),
                    (13.5, 15.9, "No lo cuestiones."), (15.9, 17.9, "Súbete. Ok, amigo."), (18.7, 20.4, "¿Y ahora qué?")],
    "rubius-bigfoot": [(14.6, 15.8, "¿Pero qué es esta fumada?"), (15.8, 18.6, "¿Dónde nos hemos metido, gente?"),
                       (22.7, 23.7, "¡Por la cara!"), (23.7, 26.5, "Hemos encontrado al Bigfoot de San Andreas.")],
    "willy-coco": [(3.0, 4.4, "¡Ven aquí! ¡Me cago en la leche!"), (6.2, 7.6, "Te tiro un cuchillo arrojadizo…"),
                   (8.0, 9.9, "Tú no me has visto en el clóset."), (10.9, 13.0, "¡MI PIERNA! ¡MI PIERNA!"),
                   (13.8, 16.6, "Vale, lo siento…"), (19.5, 22.6, "¡Que me matas con un cocodrilo!"),
                   (23.0, 25.6, "No, no, no… este es el señor caimán."), (27.9, 29.6, "Intacto."),
                   (30.4, 33.4, "Recupero mi cuchillo… no le puedo hacer nada."), (35.3, 37.6, "Qué locura, tremendo bicho."),
                   (38.8, 41.0, "Me he quedado con uno de vida.")],
    "speed-robo": [(0.9, 2.5, "¡Esto es un asalto!"), (2.6, 3.4, "¡Fiesta!"), (6.5, 9.4, "¡MANOS ARRIBA!"),
                   (9.6, 11.8, "¡Esto es un asalto! ¡Asalto!"), (11.9, 13.2, "¡Dame esto!"),
                   (13.3, 15.4, "¡No quiero lastimar a nadie!"), (15.4, 17.4, "¡Solo dame el dinero! ¡Dame la lana!"),
                   (17.5, 18.3, "¡Rápido!"), (18.4, 20.8, "¡Dame eso! ¡Y que sea todo!")],
    "kai-techo": [(15.6, 18.5, "Bro… ¿por qué está así? Tienes que estar drogado.")],
    "papa-gas": [(1.9, 3.2, "Dios mío, hermano."), (6.2, 9.0, "Tengo que hacerlo, tengo que hacerlo…"),
                 (9.0, 13.5, "TENGO QUE HACERLO, TENGO QUE HACERLO…"), (13.6, 16.0, "¡Oh, no! ¡Dios mío!")],
    "rubius-psico": [(2.8, 8.5, "What the f…"), (10.6, 12.0, "¡LANZAR!"), (17.7, 18.7, "¡Que se sigue viendo el cuerpo!"),
                     (18.7, 22.4, "Me acaban de dar NIVEL PSICÓTICO…"), (24.1, 25.9, "Se me ha llenado todo de sangre."),
                     (25.9, 29.0, "¡Qué barbaridad!")],
    "rubius-salto": [(0.1, 2.3, "Será lo que tenga que ser, chicos."), (4.4, 6.6, "Tres, dos… Dios mío."),
                     (7.6, 8.8, "Dios mío, ¿QUÉ ES ESTE JUEGO?"), (15.6, 16.2, "Uno."), (17.5, 21.4, "Se viene…"),
                     (21.5, 22.4, "¡Ah, vale!"), (22.4, 24.5, "¡HOSTIAS!")],
    "illo-borra": [(0.7, 1.6, "Histórico lo mío."), (2.3, 6.3, "Se me ha ido la olla, se me ha ido la flapa."),
                   (7.2, 8.7, "Lo he hecho por memoria muscular."), (9.9, 12.3, "Por memoria muscular. Qué locura."),
                   (17.0, 17.8, "En vez de cerrar el…"), (18.3, 21.5, "Pero qué loco, ¿no?"),
                   (21.5, 22.7, "82 minutos… no, tardará menos, ¿no?"), (23.5, 24.5, "Esto es loquísimo, ¿eh?"),
                   (25.9, 28.5, "Cable, cable. Sí, pongo cable."), (31.3, 32.5, "Lo que me acaba de pasar es loquísimo."),
                   (32.5, 36.6, "Le di a ELIMINAR creyendo que era cerrar el juego."), (36.7, 37.8, "ACABO DE BORRAR EL JUEGO."),
                   (37.8, 40.4, "Historia absoluta. Locura.")],
}


def puesto(S, num, kick, nombre, sub, clip, desde, frase_nombre, remate, tag=None, entrada="flash"):
    """rank + clip + remate (dict para titulo)."""
    w = S.w
    S.add("rank", S.t0, entrada, num=num, kick=kick, nombre=nombre, sub=sub, video=clip, desde=desde,
          tn=S.t0 + 0.1, tt=w(frase_nombre), ts=w(frase_nombre) + 0.9)
    b = S.clip_beat(clip)
    S.add("clip", b["start"] - 0.3, "corte", clip=clip, tag=tag or f"#{num} · {nombre}", subs=SUBS[clip])
    S.add("titulo", b["end"] + 0.15, "crece", **remate)


def hook(S):
    w = S.w
    S.add("titulo", w("GTA seis salió"), "corte", kick="19 DE NOVIEMBRE DE 2026", l1="LOS STREAMERS", l2="ROMPIERON GTA VI",
          t1=w("los streamers"), t2=w("ya lo rompieron"))
    S.add("foto", w("Uno se agarró"), "latigo", video="willy-coco", desde=8, kb="in", kick="WILLYREX", titulo="VS UN COCODRILO",
          tt=w("cocodrilo"))
    S.add("foto", w("Otro encontró"), "latigo", video="lirik-perro", desde=9, kb="in", kick="LIRIK", titulo="UN PERRO EN MOTO DE AGUA",
          tt=w("un perro"))
    S.add("foto", w("Uno se aventó"), "latigo", video="rubius-salto", desde=12, kb="up", kick="RUBIUS", titulo="DESDE LA ANTENA MÁS ALTA",
          tt=w("la antena"))
    S.add("foto", w("Y uno… borró"), "flash", video="illo-borra", desde=30, kb="in", kick="ILLOJUAN", titulo="¿BORRÓ EL JUEGO?",
          tt=w("borró el juego"), sub="En pleno directo.", ts=w("En pleno directo"))
    S.add("titulo", w("Estos son los doce"), "flash", kick="LOS MEJORES MOMENTOS DE STREAMERS", l1="TOP", l2="12",
          t1=w("Estos son"), t2=w("doce mejores"), sub="quédate hasta el #1", ts=w("Quédate hasta"))


def n12(S):
    puesto(S, 12, "EL JUEGO DEL AÑO, SEGÚN", "CASEOH", "Una serpiente en la cocina… y su nombre.", "caseoh-dolores", 10, "CaseOh",
           dict(kick="#12 · CASEOH", l1="SE LLAMA", l2="DOLORES", t1=S.w("Por una serpiente"), t2=S.w("llamada Dolores")))


def n11(S):
    puesto(S, 11, "EL REY DE GTA V VOLVIÓ", "VANOSS", "Persiguió a un extraño con una gaviota muerta.", "vanoss-gaviota", 2, "VanossGaming",
           dict(kick="#11 · VANOSSGAMING", l1="LO MÁS", l2="FLORIDA MAN", t1=S.w("Lo más Florida"), t2=S.w("en un videojuego")))


def n10(S):
    puesto(S, 10, "ROBO FALLIDO", "THEBURNTPEANUT", "El dueño seguía adentro.", "peanut-puerta", 4, "TheBurntPeanut",
           dict(kick="#10 · THEBURNTPEANUT", l1="LOS PEATONES", l2="YA NO SE DEJAN", t1=S.w("los peatones"), t2=S.w("ya no se dejan")),
           tag="#10 · BURNTPEANUT")


def n9(S):
    puesto(S, 9, "EN MAR ABIERTO", "LIRIK", "Una moto de agua… y no la maneja una persona.", "lirik-perro", 9, "LIRIK",
           dict(kick="#9 · LIRIK", l1="NO LO CUESTIONES", l2="SÚBETE", t1=S.w("No lo cuestiones"), t2=S.w("súbete")))


def n8(S):
    puesto(S, 8, "EASTER EGG", "RUBIUS", "Lo que los fans de San Andreas buscan hace 20 años.", "rubius-bigfoot", 3, "Rubius",
           dict(kick="#8 · RUBIUS", l1="EL BIGFOOT", l2="REGRESÓ", t1=S.w("El Bigfoot"), t2=S.w("de regreso")))


def n7(S):
    puesto(S, 7, "LOS CAIMANES NO SON DECORACIÓN", "WILLYREX", "Se metió al agua sin mirar.", "willy-coco", 8, "Willyrex",
           dict(kick="#7 · WILLYREX", l1="CON 1 DE VIDA", l2="PERO VIVO", t1=S.w("Con un punto"), t2=S.w("Pero vivo")))


def n6(S):
    puesto(S, 6, "PRIMER DÍA, PRIMER ASALTO", "ISHOWSPEED", "Toda la energía de Speed, en un robo.", "speed-robo", 6, "IShowSpeed",
           dict(kick="#6 · ISHOWSPEED", l1="SOLO QUIERE", l2="TODO EL DINERO", t1=S.w("Solo quiere"), t2=S.w("todo el dinero")))


def n5(S):
    puesto(S, 5, "EL CAMINO RÁPIDO", "KAI CENAT", "Tenía que bajar de una azotea.", "kai-techo", 2, "Kai Cenat",
           dict(kick="#5 · KAI CENAT", l1="TÉCNICAMENTE", l2="BAJÓ", t1=S.w("Técnicamente"), t2=S.w("bajó")))


def n4(S):
    puesto(S, 4, "UNA IDEA TERRIBLE", "PAPAPLATTE", "De noche, una gasolinera…", "papa-gas", 4, "Papaplatte",
           dict(kick="#4 · PAPAPLATTE", l1="TENÍA QUE HACERLO", l2="Y LO HIZO", t1=S.w("Tenía que hacerlo"), t2=S.w("Y lo hizo")))


def n3(S):
    puesto(S, 3, "EN LO MÁS ALTO DE LA ANTENA", "RUBIUS", "Con un pasajero al hombro.", "rubius-psico", 3, "Rubius",
           dict(kick="#3 · RUBIUS", l1="EL JUEGO LO DICE", l2="PSICÓTICO", t1=S.w("Y el juego"), t2=S.w("nivel psicótico")))


def n2(S):
    puesto(S, 2, "OTRA VEZ LA ANTENA", "RUBIUS", "Paracaídas, cientos de metros sobre Leonida.", "rubius-salto", 1, "Otra vez Rubius",
           dict(kick="LA FRASE DE LA SEMANA", l1="DIOS MÍO", l2="¿QUÉ ES ESTE JUEGO?", t1=S.w("Dios mío"), t2=S.w("qué es este juego"), fs2=150))


def n1(S):
    puesto(S, 1, "EL BOTÓN EQUIVOCADO", "ILLOJUAN", "Lo abrió en directo… y quiso cerrarlo.", "illo-borra", 30, "IlloJuan",
           dict(kick="#1 · ILLOJUAN", l1="82 MINUTOS", l2="PARA VOLVER", t1=S.w("ochenta y dos minutos"), t2=S.w("volver a descargarlo"),
                sub="y ni siquiera pasó dentro del juego", ts=S.w("ni siquiera")))


def cierre(S):
    w = S.w
    S.add("lista", w("Esos fueron"), "panel", kick="EL TOP 12", items=[
        ("ILLOJUAN", "borró el juego", w("Esos fueron") + 0.3, "1"), ("RUBIUS", "el salto desde la antena", w("Esos fueron") + 0.6, "2"),
        ("RUBIUS", "nivel psicótico", w("Esos fueron") + 0.9, "3"), ("PAPAPLATTE", "la gasolinera", w("Esos fueron") + 1.2, "4")],
        fsi=64, gap=22)
    S.add("titulo", w("Cuál fue tu favorito"), "flash", kick="EN LOS COMENTARIOS", l1="¿CUÁL FUE", l2="TU FAVORITO?",
          t1=w("Cuál fue"), t2=w("tu favorito"), sub="¿y cuál nos faltó?", ts=w("cuál nos faltó"))
    S.add("cta", w("Y si quieres ver"), "panel", video="rubius-salto", desde=12, kick="SIGUIENTE VIDEO", titulo="29 AÑOS DE GTA",
          en_mini="1997 VS 2026", dur="12:08", tt=w("veintinueve años"))
