"""Guion v2 del video largo — "Tenemos nuevo James Bond". Fuente de verdad para voz y montaje.

Cada sección es una lista de beats:
  ("vo", "texto")          narración (un bloque de Voicebox)
  ("clip", "nombre")       escena CON SONIDO de assets/video/cortes/<nombre>.mp4; el narrador calla
Los datos están verificados en largo/guion.md → Fuentes y verificación.
"""

SECCIONES = [
    dict(id="frio", titulo="Cold open", beats=[
        ("clip", "connery-bond-james-bond"),
        ("vo", "Desde mil novecientos sesenta y dos, solo seis actores han dicho esa frase en la saga oficial. "
               "Y el dieciséis de noviembre, Amazon presentó al séptimo."),
        ("vo", "Robert Pattinson. El vampiro de Crepúsculo. El Batman más oscuro del cine. Y ahora, cero cero siete."),
        ("vo", "Y, como era de esperarse, internet se partió en dos."),
        ("vo", "Unos dicen que es la mejor elección en veinte años. Otros, que es el peor error de la saga. "
               "Yo no te voy a decir quién tiene razón. Te voy a mostrar algo mejor: qué pasó con cada uno de los "
               "seis Bond cuando los anunciaron. Porque esta película ya la vimos."),
        ("vo", "Y quédate hasta el final, porque te voy a decir a cuál de todos se parece más el caso de Pattinson."),
    ]),
    dict(id="noticia", titulo="La noticia", beats=[
        ("vo", "Primero, lo que sabemos. Amazon MGM lo anunció con un video corto que terminaba con una sola frase: "
               "James Bond volverá. La película la dirige Denis Villeneuve, el director de Dune. Todavía no tiene "
               "título. Se filma el próximo año y llegaría a los cines en dos mil veintiocho."),
        ("vo", "A favor de Pattinson: es de los actores más respetados de su generación, ya cargó una franquicia "
               "gigante con The Batman, y tiene cuarenta años, la edad justa para quedarse varias películas."),
        ("vo", "En contra: hay quien dice que es una elección demasiado obvia, que no tiene la imagen clásica de Bond, "
               "y que la decisión la tomó Amazon, que desde dos mil veinticinco controla la saga. Algo que a muchos "
               "fans todavía no les cae bien."),
        ("vo", "Antes de seguir, déjame en los comentarios tu calificación del uno al diez. "
               "Al final vemos si cambiaste de opinión."),
    ]),
    dict(id="connery", titulo="Expediente 01 · Sean Connery", beats=[
        ("vo", "Expediente uno. Sean Connery. Seis películas oficiales, de mil novecientos sesenta y dos a mil "
               "novecientos setenta y uno. Debutó con treinta y dos años."),
        ("vo", "Hoy es el Bond de referencia. Pero en su momento, el mismísimo creador del personaje no lo quería. "
               "Ian Fleming lo describió como un doble de acción con demasiado músculo. Él imaginaba a alguien más refinado."),
        ("vo", "Connery le respondió llamándolo snob. Y entonces pasó algo curioso: Fleming terminó escribiendo en sus "
               "novelas que Bond tenía raíces escocesas. Como Connery."),
        ("clip", "connery-laser"),
        ("vo", "A favor: inventó la actitud de Bond. El humor seco, la elegancia, el peligro. En contra: visto con ojos "
               "de hoy, su Bond trata a las mujeres de una forma que ya no pasaría. "
               "Primera lección: hasta el creador del personaje se equivocó."),
    ]),
    dict(id="lazenby", titulo="Expediente 02 · George Lazenby", beats=[
        ("vo", "Expediente dos. El Bond que casi nadie recuerda. George Lazenby. Australiano, modelo de comerciales y "
               "sin experiencia como actor. Debutó con treinta años, el más joven de todos. Y desde la primera escena, "
               "la película sabía que el público lo estaba comparando."),
        ("clip", "lazenby-other-fella"),
        ("vo", "Esto nunca le pasó al otro tipo. Así, mirando a la cámara. La recepción fue fría: criticaron su acento, "
               "su falta de experiencia y, sobre todo, que no era Connery. Y antes del estreno, él mismo decidió no "
               "seguir. Su representante le aconsejó que Bond ya estaba pasado de moda. Una sola película."),
        ("vo", "A favor: hoy esa película está entre las favoritas de muchos fans, con uno de los finales más tristes "
               "de la saga."),
        ("clip", "lazenby-all-the-time"),
        ("vo", "En contra: una actuación rígida, y nunca tuvo una segunda oportunidad. Guarda este nombre. "
               "Va a volver al final."),
    ]),
    dict(id="moore", titulo="Expediente 03 · Roger Moore", beats=[
        ("vo", "Expediente tres. El récord. Roger Moore. Siete películas oficiales, de mil novecientos setenta y tres a "
               "mil novecientos ochenta y cinco. Más que nadie."),
        ("vo", "Aquí la crítica fue otra: la edad. Debutó con cuarenta y cinco años, el Bond más viejo en arrancar. "
               "En su última película ya tenía cincuenta y siete."),
        ("vo", "Moore no intentó copiar a Connery. Lo hizo a su manera: con cejas levantadas, bromas y muchísimo "
               "encanto. Hasta para escapar de unos cocodrilos."),
        ("clip", "moore-cocodrilos-voz"),
        ("clip", "moore-anders"),
        ("vo", "A favor: convirtió a Bond en un éxito para toda la familia. En contra: algunas de sus películas son "
               "casi comedia y, para muchos, Bond perdió el peligro. Segunda lección: el público aceptó un Bond "
               "completamente distinto al original."),
    ]),
    dict(id="dalton", titulo="Expediente 04 · Timothy Dalton", beats=[
        ("vo", "Expediente cuatro. El que llegó antes de tiempo. Timothy Dalton. Dos películas, en mil novecientos "
               "ochenta y siete y mil novecientos ochenta y nueve. Debutó con cuarenta y un años."),
        ("clip", "dalton-bond-james-bond"),
        ("vo", "Dalton leyó las novelas de Fleming y quiso un Bond serio, duro, casi atormentado. Justo lo contrario de "
               "Moore. Y al público de esa época no le convenció. Licencia para matar rindió por debajo de lo esperado "
               "en Estados Unidos y, después, problemas legales congelaron la saga seis años."),
        ("vo", "A favor: hoy muchos lo consideran el Bond más parecido al de los libros. En contra: llegó en el momento "
               "equivocado. Tercera lección: a veces el público tarda años en darte la razón."),
    ]),
    dict(id="brosnan", titulo="Expediente 05 · Pierce Brosnan", beats=[
        ("vo", "Expediente cinco. El regreso. Pierce Brosnan. Cuatro películas, de mil novecientos noventa y cinco a "
               "dos mil dos. Debutó con cuarenta y dos años."),
        ("vo", "Lo curioso: Brosnan pudo ser Bond casi diez años antes, pero su contrato con la serie Remington Steele "
               "se lo impidió. Cuando por fin llegó, el público lo recibió con los brazos abiertos. GoldenEye revivió "
               "una saga que muchos daban por muerta. Y nos dejó esto."),
        ("clip", "brosnan-corbata"),
        ("vo", "Un tanque por San Petersburgo, y Bond se acomoda la corbata. Eso es Brosnan: el equilibrio perfecto "
               "entre Connery y Moore. Elegante, divertido y creíble."),
        ("vo", "En contra: Otro día para morir. Un coche invisible."),
        ("clip", "brosnan-auto-invisible"),
        ("vo", "Efectos que hoy dan pena, y un final que obligó a reiniciar todo."),
    ]),
    dict(id="craig", titulo="Expediente 06 · Daniel Craig", beats=[
        ("vo", "Expediente seis. Y aquí está el caso que más se parece a hoy. Daniel Craig. Cinco películas, de dos mil "
               "seis a dos mil veintiuno. Debutó con treinta y ocho años."),
        ("vo", "Cuando lo anunciaron en dos mil cinco, fue un desastre. Lo presentaron en una lancha por el Támesis, con "
               "chaleco salvavidas, y la prensa lo destrozó. Lo llamaron James Blonde, por su pelo rubio. Dijeron que "
               "era muy bajo, que no tenía cara de Bond. Hasta crearon páginas web solo para pedir que lo sacaran."),
        ("vo", "Un año después, se estrenó Casino Royale."),
        ("clip", "craig-parkour-voz"),
        ("clip", "craig-shaken"),
        ("vo", "La crítica se rindió. Y luego vino Skyfall."),
        ("clip", "craig-skyfall-voz"),
        ("vo", "Más de mil cien millones de dólares en taquilla. La más exitosa de toda la historia de Bond."),
        ("vo", "A favor: le dio a Bond emociones, heridas y consecuencias. En contra: para algunos se volvió demasiado "
               "serio, y se perdió la diversión."),
    ]),
    dict(id="exito", titulo="¿Quién fue el más exitoso?", beats=[
        ("vo", "Entonces, ¿quién fue el mejor? Depende de cómo lo midas. Por taquilla, gana Craig, con Skyfall. "
               "Por número de películas, gana Moore, con siete. Pero si ajustas por inflación en Estados Unidos, "
               "Operación Trueno, de Connery, sigue arriba. Dime en los comentarios cuál de las tres medidas cuenta para ti."),
    ]),
    dict(id="patron", titulo="El patrón", beats=[
        ("vo", "¿Te acuerdas de Lazenby? Aquí está el contraste. Lazenby y Craig fueron los dos Bond más criticados al "
               "ser anunciados. Uno se rindió antes de tiempo. El otro aguantó, y terminó con la película más "
               "taquillera de la saga."),
        ("vo", "Y Pattinson ya vivió esto dos veces. Según él mismo, en dos mil ocho setenta y cinco mil personas "
               "firmaron para sacarlo de Crepúsculo."),
        ("clip", "pattinson-spider-monkey"),
        ("vo", "Y en dos mil diecinueve hubo peticiones para quitarlo de Batman."),
        ("clip", "pattinson-vengeance"),
        ("vo", "Las dos veces terminó callando a muchos. Entonces, ¿será Craig, o será Lazenby? Eso no lo decide "
               "internet. Lo decide la película."),
    ]),
    dict(id="cierre", titulo="Cierre", beats=[
        ("vo", "Te repito la pregunta: del uno al diez, ¿Pattinson va a llenar los zapatos de cero cero siete? "
               "¿Cambiaste tu calificación? Te leo en los comentarios. Y suscríbete, porque cuando salga el primer "
               "adelanto, lo vamos a analizar aquí."),
    ]),
]

DIRECCION = ("Narrador de cine para YouTube, cercano y con aplomo, elegante como un tráiler de espías: misterioso y seco "
             "en el gancho, cómplice al contar las anécdotas, con humor sutil en las ironías y firme en las lecciones. "
             "Ritmo ágil pero sin prisa; pausas breves antes de los datos que sorprenden.")
