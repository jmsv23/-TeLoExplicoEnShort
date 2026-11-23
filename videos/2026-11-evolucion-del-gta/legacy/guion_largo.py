"""Guion del video largo: "GTA 6 vs TODOS los GTA". Fuente de verdad para la voz y el montaje.

Beats: ("vo", "texto") narración · ("clip", "nombre") escena CON SONIDO de assets/video/cortes/<nombre>.mp4.
Los números van escritos como se dicen. Fuentes en ../largo/guion.md.
"""

SECCIONES = [
    dict(id="hook", titulo="Hook", beats=[
        ("vo", "En mil novecientos noventa y siete, Grand Theft Auto era un cochecito pixelado visto desde arriba, "
               "atropellando peatones del tamaño de una hormiga."),
        ("vo", "Hace dos días salió GTA seis. La crítica le dio un noventa y nueve, la calificación más alta de la historia. "
               "Y en un solo día ganó más dinero que las dos últimas películas de Avatar juntas."),
        ("vo", "Pero aquí viene lo raro: los jugadores le están dando un cinco. "
               "Y hay cosas que hacía San Andreas hace más de veinte años que GTA cinco te quitó."),
        ("vo", "Así que hoy vamos a ver veintinueve años de GTA, juego por juego y mecánica por mecánica. "
               "Qué mejoró, qué empeoró, y al final tú decides: ¿evolución, o retroceso?"),
    ]),
    dict(id="origen", titulo="El origen", beats=[
        ("vo", "Empecemos por algo que casi nadie sabe. GTA no iba a ser GTA."),
        ("vo", "En los noventa, un estudio pequeño de Escocia llamado DMA Design trabajaba en un juego llamado Race and Chase. "
               "Carreras y persecuciones. Y la idea era que tú también pudieras jugar como policía."),
        ("vo", "Pero durante las pruebas apareció un error: la inteligencia de los policías salió demasiado agresiva. "
               "En vez de seguirte, te embestían y trataban de sacarte del camino a la fuerza."),
        ("vo", "Lo lógico era arreglarlo. Pero el equipo se dio cuenta de que huir de esos policías locos era lo más divertido del juego. "
               "Así que lo dejaron, quitaron el modo policía, y el criminal pasó a ser el protagonista."),
        ("vo", "Y otro dato: Liberty City, Vice City y San Andreas ya existían en ese primer juego. "
               "Las tres ciudades que conoces nacieron en mil novecientos noventa y siete, en pixeles."),
        ("vo", "El juego se vendió con escándalo a propósito. Los políticos británicos lo atacaron, los periódicos lo llamaron peligroso, "
               "y cada titular era publicidad gratis."),
        ("vo", "Dos años después llegó GTA dos, con pandillas que te respetaban o te odiaban según para quién trabajaras. "
               "Pero seguía viéndose desde arriba. El salto de verdad todavía no llegaba."),
    ]),
    dict(id="salto3d", titulo="GTA III", beats=[
        ("vo", "En dos mil uno, GTA tres lo cambió todo. Por primera vez, la ciudad era en tres dimensiones, "
               "y podías caminar, manejar y disparar en cualquier parte de Liberty City."),
        ("vo", "Hoy suena normal. En ese momento era otro planeta. GTA tres prácticamente inventó el mundo abierto moderno, "
               "y medio mundo de los videojuegos lo copió durante la siguiente década."),
        ("vo", "El protagonista, Claude, no dice una sola palabra en todo el juego. Ni una."),
        ("vo", "Y el juego casi sale distinto. Iba a salir semanas después del ataque a las Torres Gemelas, "
               "y Rockstar lo retrasó para cambiar cosas: hasta las patrullas, que eran azul con blanco como las de Nueva York, "
               "pasaron a ser blanco y negro."),
    ]),
    dict(id="vicecity", titulo="Vice City", beats=[
        ("vo", "Un año después llegó Vice City. Mil novecientos ochenta y seis, neón, camisas hawaianas, "
               "y una radio con éxitos reales de los ochenta. Por primera vez, la música era la mitad del juego."),
        ("vo", "Tommy Vercetti, con la voz del actor Ray Liotta, de Goodfellas, sí hablaba. Y mucho. "
               "Pero tenía un problema muy famoso: no sabía nadar. Si caías al agua, morías."),
        ("vo", "Y ahora viene la comparación que todo mundo está buscando. Vice City en dos mil dos, contra Vice City en dos mil veintiséis."),
        ("vo", "La Vice City original medía menos de diez kilómetros cuadrados. Era todo el juego. "
               "En GTA seis, Vice City es solo una parte de Leonida, un estado completo inspirado en Florida, "
               "con pantanos, islas, carreteras y pueblos."),
        ("vo", "Según Rockstar, el mapa de GTA seis es casi el doble que el de GTA cinco. "
               "Y Vice City, sola, es la ciudad más grande que han construido."),
        ("vo", "Y por cierto: el hotel Ocean View, donde Tommy se quedaba en el juego original, regresó. "
               "Está ahí, en Ocean Beach, esperando a que lo encuentres."),
    ]),
    dict(id="sanandreas", titulo="San Andreas", beats=[
        ("vo", "En dos mil cuatro llegó el juego que para muchos sigue siendo el mejor de todos. San Andreas."),
        ("clip", "cj-here-we-go"),
        ("vo", "Carl Johnson regresa a Los Santos, y en cuanto pisa Grove Street, todo se complica. "
               "Pero lo que hizo legendario a San Andreas no fue la historia. Fue todo lo que podías hacer."),
        ("vo", "Si CJ comía mucha pizza, engordaba. Si iba al gimnasio, ganaba músculo. Si corría, tenía más resistencia. "
               "Y la gente en la calle reaccionaba diferente según cómo te veías."),
        ("vo", "Podías nadar, bucear, tener novias, cortarte el pelo, tatuarte, conquistar territorio de pandillas, "
               "y hasta volar con un jetpack. Y tres ciudades completas: Los Santos, San Fierro y Las Venturas."),
        ("vo", "Y aquí viene lo polémico: el mapa de San Andreas era más grande que el de GTA cuatro, que salió cuatro años después."),
        ("vo", "Hoy, en Metacritic, San Andreas sigue siendo el juego de Rockstar mejor calificado por los jugadores. "
               "Un nueve punto uno. Recuerda ese número, porque al final lo vamos a necesitar."),
    ]),
    dict(id="polemicas", titulo="Las polémicas", beats=[
        ("vo", "Pero San Andreas también trajo el escándalo más grande de la saga. Hot Coffee."),
        ("vo", "Dentro del disco había un minijuego sexual escondido. Rockstar lo había desactivado, pero seguía ahí, "
               "y un fan lo desbloqueó con un mod."),
        ("vo", "Cuando se supo, el juego fue reclasificado como solo para adultos, lo sacaron de las tiendas, "
               "y a Take Two le costó decenas de millones de dólares entre reimpresiones y demandas."),
        ("vo", "Y en medio de todo eso había un abogado obsesionado con destruir GTA: Jack Thompson. "
               "Durante años acusó a la saga de crear criminales, y presentó demanda tras demanda."),
        ("vo", "En dos mil ocho le quitaron la licencia de abogado. ¿Y sabes de dónde era Jack Thompson? De Miami. "
               "Exacto. La ciudad real en la que se inspira Vice City, el lugar donde ocurre GTA seis."),
    ]),
    dict(id="gta4", titulo="GTA IV", beats=[
        ("vo", "En dos mil ocho, Rockstar hizo algo que nadie esperaba: le quitó cosas a GTA."),
        ("vo", "GTA cuatro no tenía gimnasio, ni engordar, ni jetpack. El mapa era más chico que el de San Andreas. "
               "Rockstar quería realismo, y apostó todo a eso."),
        ("vo", "Niko Bellic, un inmigrante de Europa del Este, llega a Liberty City con el sueño americano. "
               "Y su primo Roman no lo deja en paz."),
        ("clip", "roman-bowling"),
        ("vo", "Pero lo que GTA cuatro hizo mejor que todos fue la física. Usaba un motor llamado Euphoria: "
               "los personajes no caían como muñecos, reaccionaban. Se tropezaban, se agarraban de los autos, trataban de no caerse."),
        ("vo", "Y los choques eran brutales. Los autos se abollaban, se doblaban, perdían puertas. "
               "Se sentían pesados, como autos de verdad."),
        ("vo", "Y aquí está la parte que todavía hace enojar a los fans: GTA cinco, cinco años después, tenía choques mucho más suaves. "
               "Los autos casi no se deformaban. En física, GTA cinco fue un paso atrás."),
    ]),
    dict(id="gta5", titulo="GTA V", beats=[
        ("vo", "Pero en todo lo demás, GTA cinco fue un monstruo. Salió en septiembre de dos mil trece, "
               "con tres protagonistas: Michael, Franklin y Trevor. Y podías cambiar entre ellos en cualquier momento."),
        ("vo", "En su primer día ganó ochocientos millones de dólares. En tres días, mil millones. "
               "Ningún producto de entretenimiento de la historia había llegado tan rápido a esa cifra."),
        ("vo", "Y luego no se fue nunca. Salió en PlayStation tres, luego en PlayStation cuatro, luego en PlayStation cinco. "
               "Tres generaciones de consolas con el mismo juego."),
        ("vo", "Hoy lleva más de doscientos quince millones de copias vendidas. Y con GTA Online, siguió generando dinero durante más de una década."),
        ("vo", "El problema es que ese éxito tuvo un costo: mientras GTA Online siguiera imprimiendo dinero, el siguiente GTA podía esperar."),
    ]),
    dict(id="policia", titulo="La policía", beats=[
        ("vo", "Antes de llegar a GTA seis, hay una mecánica que resume perfecto cómo ha evolucionado la saga. La policía."),
        ("vo", "En GTA uno, el nivel de búsqueda eran caritas de policía arriba de la pantalla. Cuatro como máximo."),
        ("vo", "En GTA tres llegaron las seis estrellas. A la sexta, te mandaban al ejército con tanques."),
        ("vo", "En GTA cuatro, aparecía un círculo en el mapa. Si salías del círculo sin que te vieran, escapabas."),
        ("vo", "En GTA cinco, la policía tenía conos de visión. Te escondías en un callejón y esperabas a que las estrellas parpadearan. "
               "Pero había un truco: la policía siempre sabía quién eras."),
        ("vo", "En GTA seis, eso se acabó. Ahora la policía necesita un testigo, una alarma o una cámara para saber que cometiste un crimen. "
               "Y te identifica por tu cara, tu ropa y tu auto."),
        ("vo", "Si te cambias de ropa, pintas el auto o borras el video de seguridad de la tienda, les pierdes la pista. "
               "Ya no hay patrullas en el minimapa, y la sexta estrella regresa."),
        ("vo", "Uno de los jefes de Rockstar lo explicó así: en los GTA anteriores eras casi todopoderoso. "
               "Todos huían de ti aterrados. En GTA seis, el mundo ya no funciona así. La gente se defiende, y te graba con el celular."),
    ]),
    dict(id="espera", titulo="La espera", beats=[
        ("vo", "Ahora, la pregunta que todos se hicieron durante más de una década: ¿por qué tardó tanto?"),
        ("vo", "Mira esto. Entre GTA uno y GTA dos pasaron dos años. Entre GTA tres y Vice City, uno. "
               "Entre San Andreas y GTA cuatro, casi cuatro. Entre GTA cuatro y GTA cinco, cinco."),
        ("vo", "Y entre GTA cinco y GTA seis: trece años."),
        ("vo", "Para que lo dimensiones: pasó menos tiempo entre GTA tres y GTA cinco, con Vice City, San Andreas y GTA cuatro en medio, "
               "que entre GTA cinco y GTA seis."),
        ("vo", "Y la espera tuvo de todo. En dos mil veintidós, un hacker adolescente filtró noventa videos del juego en desarrollo. "
               "Lo hizo desde un cuarto de hotel, con un celular, una tele y un Fire Stick de Amazon."),
        ("vo", "Luego, el primer tráiler se filtró horas antes de su estreno y aun así rompió el récord de YouTube: "
               "noventa millones de vistas en veinticuatro horas."),
        ("clip", "trailer1-lucia"),
        ("vo", "El segundo tráiler fue más lejos: cuatrocientos setenta y cinco millones de vistas en un día, sumando todas las plataformas."),
        ("vo", "Y después vinieron los retrasos. Primero iba a salir en otoño de dos mil veinticinco. Luego en mayo de dos mil veintiséis. "
               "Y al final, el diecinueve de noviembre. Hace dos días."),
    ]),
    dict(id="gta6", titulo="GTA VI", beats=[
        ("vo", "Y valió la pena para Take Two. Entre preventas y el primer día, GTA seis vendió tres mil setecientos noventa millones de dólares."),
        ("vo", "Take Two lo llamó el lanzamiento de entretenimiento más grande de la historia, en cualquier medio. "
               "Ni películas, ni discos, ni ningún otro juego se le acerca."),
        ("vo", "Jason y Lucía son la pareja protagonista. Lucía es la primera mujer protagonista de un GTA desde que la saga pasó a tres dimensiones. "
               "Y la historia principal dura unas ochenta horas."),
        ("vo", "Y lo mejor para los fans de siempre: GTA seis está lleno de referencias a los juegos anteriores."),
        ("vo", "Afuera de la casa de Jason hay un velero idéntico al de Michael, de GTA cinco. "
               "Y su GPS no muestra el mapa de Leonida. Muestra el mapa de Los Santos."),
        ("vo", "En el celular aparecen publicaciones de Race and Chase, el nombre original del primer GTA. "
               "En los pantanos vive el Skunk Ape, el Pie Grande de San Andreas. "
               "Y el actor que le dio voz a Niko Bellic aparece en los créditos como el sicario."),
        ("vo", "Y sí: el gimnasio regresa. Puedes llevar a Jason y a Lucía a entrenar. Lo que GTA cinco te quitó, GTA seis te lo devolvió."),
        ("vo", "Y la física de los choques también regresó. Los autos vuelven a deformarse como en GTA cuatro, "
               "pierden piezas, y ahora hasta tienes que cargarles gasolina."),
    ]),
    dict(id="veredicto", titulo="Veredicto", beats=[
        ("vo", "Entonces, ¿por qué los jugadores le dan un cinco?"),
        ("vo", "En Metacritic, la crítica le dio un noventa y nueve. Empata con Ocarina of Time como el juego mejor calificado de la historia del sitio."),
        ("vo", "Pero la calificación de los usuarios cayó por debajo de cinco. Es la diferencia más grande entre crítica y jugadores en la historia de la página."),
        ("vo", "Una parte es review bombing: miles de calificaciones negativas de gente que ni siquiera tiene el juego, "
               "o que lo ataca por su historia. Pero otra parte son quejas reales."),
        ("vo", "En consolas corre a treinta cuadros por segundo. Tiene errores de lanzamiento. Y la edición de lujo cuesta cien dólares."),
        ("vo", "Y luego está San Andreas, con su nueve punto uno, veintidós años después, todavía como el favorito de los jugadores."),
        ("vo", "Así que este es el resumen de veintinueve años: GTA pasó de pixeles a fotorrealismo. "
               "La policía pasó de caritas en la pantalla a investigar testigos. Las ciudades pasaron a ser un estado completo."),
        ("vo", "Pero en el camino, GTA cinco quitó cosas que San Andreas ya tenía, y GTA cuatro tenía mejor física que su sucesor. "
               "La evolución no siempre fue hacia adelante."),
    ]),
    dict(id="cierre", titulo="Cierre", beats=[
        ("vo", "Ahora te toca a ti. ¿GTA seis es la evolución definitiva, o San Andreas sigue siendo el rey?"),
        ("vo", "Escríbeme en los comentarios cuál es tu GTA favorito y por qué. Yo leo todos."),
        ("vo", "Y si quieres más datos como estos, suscríbete. Nos vemos en Leonida."),
    ]),
]

DIRECCION = ("Narrador de videojuegos para YouTube, energía de amigo que sabe mucho del tema: gancho seco, "
             "ritmo ágil, remates con intención y un poco de humor. Frases claras, sin pausas largas.")
