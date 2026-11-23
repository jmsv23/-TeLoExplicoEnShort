"""Guion del video largo: "Las 5 actrices más guapas de Marvel". Es la fuente de verdad para la voz y el montaje.

Cada sección es una lista de beats:
  ("vo", "texto")      narración (un bloque de Voicebox)
  ("clip", "nombre")   escena CON SONIDO de assets/video/cortes/<nombre>.mp4; el narrador calla
Los datos están verificados en largo/guion.md, secciones "Verificado" y "Fuentes ya verificadas".
"""

SECCIONES = [
    dict(id="hook", titulo="Hook", beats=[
        ("vo", "Marvel tiene a algunas de las mujeres más famosas del planeta. Pero en esta lista solo caben cinco."),
        ("vo", "Y antes de que lo preguntes: sí, ya sabes quién es la número uno. O eso crees. "
               "Porque la historia de cómo llegó a ese papel casi nadie la conoce."),
        ("vo", "En este top hay una actriz que ganó un Óscar después de pintarse de verde, otra que estudió en Harvard "
               "mientras filmaba Star Wars, y otra que acaba de romper un récord de taquilla este verano."),
        ("vo", "Y quédate hasta el final, porque antes de la número uno te enseño a las cuatro que casi entran. "
               "Seguro una es tu favorita."),
    ]),
    dict(id="reglas", titulo="Las reglas", beats=[
        ("vo", "Tres reglas rápidas. Uno: solo actrices del universo cinematográfico de Marvel, el de los Avengers."),
        ("vo", "Dos: no medimos solo la cara. Cuenta la presencia en pantalla, el carisma, y ese look que se te queda grabado."),
        ("vo", "Y tres: es mi top, no el tuyo. Si no estás de acuerdo, el lugar para pelear es en los comentarios. "
               "Al final te pido tu top cinco."),
    ]),
    dict(id="n5", titulo="Nº 5 · Zoe Saldaña", beats=[
        ("vo", "En el número cinco: la mujer más peligrosa de la galaxia. Zoe Saldaña. Gamora, en Guardianes de la galaxia."),
        ("vo", "Para ser Gamora, pasaba horas en la silla de maquillaje cada día de rodaje, cubierta de pintura verde. "
               "Y aun así, su mirada se robaba cada escena."),
        ("clip", "zoe-idiotas"),
        ("vo", "Pero hay algo que la hace única en esta lista. Zoe creció entre Nueva York y República Dominicana, "
               "habla español, y antes de actuar estudió ballet."),
        ("vo", "Y su récord es ridículo: está en las tres películas más taquilleras de la historia. "
               "Avatar, Avengers Endgame, y Avatar: el camino del agua."),
        ("vo", "En enero de este año se convirtió en la actriz más taquillera de todos los tiempos, con más de quince mil "
               "millones de dólares. ¿Y a quién le quitó el trono? Lo vas a ver más adelante."),
        ("vo", "Por si fuera poco, en dos mil veinticinco ganó el Óscar. "
               "Belleza, disciplina, y una carrera que nadie en Hollywood ha igualado. Número cinco."),
    ]),
    dict(id="n4", titulo="Nº 4 · Natalie Portman", beats=[
        ("vo", "En el número cuatro: la científica que terminó levantando el martillo. Natalie Portman. Jane Foster, en Thor."),
        ("vo", "Natalie empezó a actuar a los doce años, en El perfecto asesino. Y mientras filmaba las precuelas de "
               "Star Wars como la reina Amidala, estudiaba psicología en la Universidad de Harvard. Y se graduó."),
        ("vo", "En dos mil once ganó el Óscar por El cisne negro, el mismo año en que se estrenó Thor."),
        ("vo", "Durante años, muchos pensaron que Jane era solo la novia de Thor. Hasta Thor: amor y trueno, "
               "donde se convirtió en la Poderosa Thor. Entrenó durante meses para ese papel."),
        ("clip", "portman-eat-my-hammer"),
        ("vo", "Lo que hace distinta su belleza es ese aire clásico, casi de estrella del cine antiguo. Treinta años en "
               "pantalla, y su cara sigue siendo de las más reconocibles del mundo."),
        ("vo", "Y ojo, porque los rumores dicen que podría volver en Avengers Doomsday. Marvel todavía no lo confirma. "
               "Ahora, si crees que debería estar más arriba, espera a ver a quién puse en el número tres."),
    ]),
    dict(id="n3", titulo="Nº 3 · Zendaya", beats=[
        ("vo", "En el número tres: la más joven de la lista. Zendaya. MJ, en Spider-Man."),
        ("vo", "Llegó a Marvel en Spider-Man: de regreso a casa, con un personaje que casi no sonreía. "
               "Y aun así, se robó la película."),
        ("clip", "zendaya-call-me-mj"),
        ("vo", "Lo de Zendaya va más allá de la belleza: es un ícono de la moda. Cada vez que pisa una alfombra roja, "
               "lo que se pone es noticia al día siguiente."),
        ("vo", "Y como actriz no se queda atrás. Ganó dos premios Emmy por Euphoria, y es la persona más joven en "
               "ganarlo dos veces como mejor actriz de drama."),
        ("vo", "Este verano, Spider-Man: un nuevo día debutó con más de novecientos treinta millones de dólares en todo "
               "el mundo en su primer fin de semana. El segundo mejor estreno de la historia."),
        ("vo", "Y fuera de la pantalla, la historia más bonita de Marvel: en junio, Tom Holland confirmó que ya se "
               "casaron. Peter Parker y MJ, en la vida real. Número tres."),
    ]),
    dict(id="n2", titulo="Nº 2 · Elizabeth Olsen", beats=[
        ("vo", "En el número dos: la mujer más poderosa del universo Marvel. Elizabeth Olsen. "
               "Wanda Maximoff, la Bruja Escarlata."),
        ("vo", "Primer dato curioso: es la hermana menor de las gemelas Olsen, Mary-Kate y Ashley. "
               "Y de niña pensó en cambiarse el apellido, para que nadie la comparara con ellas."),
        ("vo", "Llegó a Marvel en Avengers: era de Ultrón. Y en diez años pasó de ser una chica asustada a la villana "
               "de Doctor Strange en el multiverso de la locura."),
        ("clip", "olsen-took-everything"),
        ("vo", "Con WandaVision demostró que podía cargar una serie entera, y recibió una nominación al Emmy. "
               "Su belleza tiene algo que pocas logran: puede verse dulce en una escena, y aterradora en la siguiente."),
        ("vo", "Y esta es la noticia que tiene a todos hablando. Hace unos días, en el final de VisionQuest, Doctor Doom "
               "aparece frente al cuerpo de Wanda y le dice: Bruja Escarlata, despierta. Tu poder será mío."),
        ("vo", "Ella había dicho que no estaría en Doomsday. Y ahora, todo indica que vuelve. Número dos."),
    ]),
    dict(id="menciones", titulo="Las que casi entran", beats=[
        ("vo", "Antes del número uno, las cuatro que casi entran."),
        ("vo", "Florence Pugh, Yelena Belova. Pasó de ser la hermana de Black Widow a liderar Thunderbolts, "
               "y estará en Doomsday."),
        ("vo", "Hailee Steinfeld, Kate Bishop en Ojo de Halcón. La heredera natural del arco y la flecha."),
        ("vo", "Brie Larson, Capitana Marvel. La primera película encabezada por una superheroína en pasar los mil "
               "millones de dólares."),
        ("vo", "Y Vanessa Kirby, Sue Storm en Los Cuatro Fantásticos: primeros pasos. La nueva mujer invisible, "
               "que de invisible no tiene nada."),
        ("vo", "¿Alguna de ellas debió estar en el top? Ahí está la pelea. Pero ahora sí."),
    ]),
    dict(id="n1", titulo="Nº 1 · Scarlett Johansson", beats=[
        ("vo", "En el número uno. Scarlett Johansson. Natasha Romanoff, la Viuda Negra."),
        ("vo", "Y aquí está la historia que casi nadie conoce: Natasha no era para ella. Scarlett hizo una audición y "
               "la rechazaron. El papel fue para Emily Blunt, que tuvo que dejarlo por otro contrato. "
               "Y Scarlett tuvo una segunda oportunidad. La aprovechó."),
        ("vo", "Debutó en Iron Man dos, con una pelea en un pasillo que todavía se recuerda. Y en Avengers dejó claro "
               "que la más peligrosa del equipo no necesitaba superpoderes."),
        ("clip", "scarlett-on-hold"),
        ("vo", "Después, más de diez años como la única Avenger original. Sin poderes. Solo con su inteligencia."),
        ("vo", "La revista Esquire la nombró dos veces la mujer más sexy del mundo, en dos mil seis y en dos mil trece. "
               "Es la única mujer que lo ha logrado dos veces."),
        ("vo", "Y en dos mil veinticinco, con Jurassic World: Renace, se convirtió en la protagonista más taquillera "
               "de la historia. ¿Te acuerdas de Zoe Saldaña? Fue ella quien le quitó ese trono en enero. "
               "Las dos mujeres más taquilleras del cine salieron de Marvel."),
        ("vo", "Scarlett no está en Doomsday. Ella misma lo dijo: extraña a sus compañeros. Pero no le hace falta. "
               "Para millones, nadie ha estado a su altura. Número uno."),
    ]),
    dict(id="cierre", titulo="Cierre", beats=[
        ("vo", "Ese es mi top. Zoe, Natalie, Zendaya, Elizabeth, y Scarlett en el trono."),
        ("vo", "Ahora te toca a ti. Escribe tu top cinco en los comentarios, y dime quién falta. Leo todos."),
        ("vo", "Y si quieres saber qué va a pasar en Avengers Doomsday, tengo una serie entera sobre el camino a "
               "Doomsday. Te espera en el canal."),
    ]),
]

DIRECCION = ("Narrador de cine para YouTube, cálido y con energía, como un presentador de alfombra roja que cuenta "
             "secretos de Hollywood: entusiasta pero elegante, remates con intención, ritmo ágil sin atropellarse.")
