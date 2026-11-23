"""Largo: TOP 12 momentos de streamers en GTA 6 (16:9, ~10 min).

Cada puesto: intro del narrador → clip con el sonido original (subtitulado en escenas_largo.py) → remate corto.
Los números van en palabras para el TTS; en pantalla se usan cifras.
"""

SECCIONES = [
    dict(id="hook", titulo="Hook", beats=[
        ("vo", 'GTA seis salió hace dos días, y los streamers más grandes del planeta ya lo rompieron.'),
        ("vo", 'Uno se agarró a golpes con un cocodrilo. Otro encontró a un perro manejando una moto de agua. Uno se aventó desde la antena más alta del mapa.'),
        ("vo", 'Y uno… borró el juego. En pleno directo. Con miles de personas mirando.'),
        ("vo", 'Estos son los doce mejores momentos de los streamers en GTA seis. Quédate hasta el número uno, porque no lo vas a creer.'),
    ]),
    dict(id="n12", titulo="#12 CaseOh", beats=[
        ("vo", 'Número doce. CaseOh entra a la cocina, ve una serpiente en una caja… y el juego le pide que le dé de comer. Lo que lo rompe es el nombre.'),
        ("clip", "caseoh-dolores"),
        ("vo", 'Juego del año, según CaseOh. Por una serpiente llamada Dolores.'),
    ]),
    dict(id="n11", titulo="#11 Vanoss", beats=[
        ("vo", 'Número once. VanossGaming, el rey de los videos de GTA cinco, tardó cero minutos en volver a las andadas. Agarró una gaviota muerta… y empezó a perseguir a un desconocido con ella.'),
        ("clip", "vanoss-gaviota"),
        ("vo", 'Lo más Florida que se ha visto en un videojuego. Y eso que el juego entero es Florida.'),
    ]),
    dict(id="n10", titulo="#10 TheBurntPeanut", beats=[
        ("vo", 'Número diez. TheBurntPeanut ve una camioneta de lujo y decide robarla. Pequeño detalle: el dueño seguía adentro.'),
        ("clip", "peanut-puerta"),
        ("vo", 'En GTA seis los peatones ya no se dejan. Y este venía con ganas.'),
    ]),
    dict(id="n9", titulo="#9 LIRIK", beats=[
        ("vo", 'Número nueve. LIRIK estaba nadando en mar abierto, a la deriva, cuando de la nada aparece una moto de agua. Y quien la maneja… no es una persona.'),
        ("clip", "lirik-perro"),
        ("vo", 'No lo cuestiones, súbete. La mejor regla para sobrevivir en Leonida.'),
    ]),
    dict(id="n8", titulo="#8 Rubius", beats=[
        ("vo", 'Número ocho. Rubius se mete al pantano, entre árboles y lodo, y se topa con algo que los fans de San Andreas llevan veinte años buscando.'),
        ("clip", "rubius-bigfoot"),
        ("vo", 'El Bigfoot de San Andreas, de regreso en GTA seis. Y sí, te deja drogado.'),
    ]),
    dict(id="n7", titulo="#7 Willyrex", beats=[
        ("vo", 'Número siete. Willyrex se mete al agua sin mirar. Error. En Leonida los caimanes no son decoración.'),
        ("clip", "willy-coco"),
        ("vo", 'Con un punto de vida. Pero vivo. El señor caimán, en cambio, sigue intacto.'),
    ]),
    dict(id="n6", titulo="#6 IShowSpeed", beats=[
        ("vo", 'Número seis. IShowSpeed no pierde el tiempo: primer día, primer asalto. Y lo hace con toda la energía de Speed.'),
        ("clip", "speed-robo"),
        ("vo", 'No quiere lastimar a nadie. Solo quiere todo el dinero. Ya.'),
    ]),
    dict(id="n5", titulo="#5 Kai Cenat", beats=[
        ("vo", 'Número cinco. Kai Cenat está en una azotea y quiere bajar. Podría usar la escalera… pero Kai elige el camino rápido.'),
        ("clip", "kai-techo"),
        ("vo", 'Técnicamente bajó. Eso nadie se lo quita.'),
    ]),
    dict(id="n4", titulo="#4 Papaplatte", beats=[
        ("vo", 'Número cuatro. El streamer alemán Papaplatte acaba de sobrevivir a una persecución de milagro. Va manejando de noche, ve una gasolinera… y se le ocurre una idea terrible.'),
        ("clip", "papa-gas"),
        ("vo", 'Tenía que hacerlo. Lo dijo veinte veces. Y lo hizo.'),
    ]),
    dict(id="n3", titulo="#3 Rubius psicótico", beats=[
        ("vo", 'Número tres. Rubius sube a lo más alto de una antena gigante con un pasajero cargado al hombro. Lo que hace allá arriba le da al juego una reacción que no esperaba.'),
        ("clip", "rubius-psico"),
        ("vo", 'Y el juego se lo dejó clarísimo: nivel psicótico.'),
    ]),
    dict(id="n2", titulo="#2 Rubius salto", beats=[
        ("vo", 'Número dos. Otra vez Rubius, otra vez en la antena. Pero ahora con paracaídas, cientos de metros sobre Leonida. Mira la vista antes de saltar.'),
        ("clip", "rubius-salto"),
        ("vo", 'Dios mío, qué es este juego. Probablemente la frase que más se repitió en todo internet esta semana.'),
    ]),
    dict(id="n1", titulo="#1 IlloJuan", beats=[
        ("vo", 'Y el número uno. IlloJuan llevaba años esperando GTA seis, como todos. Lo instala, lo abre en directo… y quiere cerrarlo un momento. Le da a un botón por memoria muscular. El botón equivocado.'),
        ("clip", "illo-borra"),
        ("vo", 'El instalador le marcaba ochenta y dos minutos para volver a descargarlo. El momento más histórico del lanzamiento, y ni siquiera pasó dentro del juego.'),
    ]),
    dict(id="cierre", titulo="Cierre", beats=[
        ("vo", 'Esos fueron los doce mejores momentos de los streamers en GTA seis. ¿Cuál fue tu favorito? ¿Y cuál nos faltó? Déjalo en los comentarios, que esto apenas empieza.'),
        ("vo", 'Y si quieres ver cómo llegamos hasta aquí, tengo un video con veintinueve años de GTA, del primero al seis. Te espero ahí.'),
    ]),
]

DIRECCION = ("Narrador de videojuegos para YouTube: energía alta, tono cómplice y divertido, como contando chismes de los streamers a un amigo. "
             "Remates con intención, pausas cortas antes del giro. Ritmo ágil.")
