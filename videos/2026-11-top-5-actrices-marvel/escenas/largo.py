"""Dirección visual del video largo (estilo "Portada"). Una función por sección del guion (mismo id).

S.w("frase") → tiempo absoluto en que la voz dice la frase. S.add(tipo, t, entrada, **params).
Entradas: corte | fundido | pagina | crece | iris | latigo. El flash de cámara va dentro de cada "portada".
Regla: algo cambia cada 1.5–3 s (texto que entra, cifra que cuenta, Ken Burns, cambio de plano).
"""


def clip(S, name, tag="", entrada="corte"):
    b = S.clip_beat(name)
    S.add("clip", b["start"] - 0.3, entrada, clip=name, tag=tag)


def hook(S):
    w = S.w
    S.add("contactos", w("Marvel tiene"), "fundido", imgs=[("zoe-oscar-perfil", "45% 20%"), ("portman-cannes", "50% 12%"),
          ("zendaya-metgala-flores", "75% 25%"), ("olsen-corona-retrato", "50% 20%"), ("scarlett-natasha-retrato", "50% 25%")],
          cw=300, kick="TOP 5 · MARVEL", tk=w("las mujeres más famosas"), titulo="SOLO CABEN CINCO", tt=w("solo caben cinco"))
    S.add("titulo", w("Y antes de que"), "pagina", kick="LA NÚMERO UNO", l1="¿YA SABES", l2="QUIÉN ES?", t1=w("ya sabes"),
          t2=w("quién es"), sub="O eso crees.", ts=w("O eso crees"))
    S.add("impresa", w("Porque la historia"), "crece", img="scarlett-natasha-retrato", pos="50% 25%", lado="der",
          kick="LA HISTORIA DETRÁS", titulo="CASI NADIE LA CONOCE", tt=w("casi nadie"))
    S.add("foto", w("una actriz que ganó"), "pagina", img="zoe-gamora-retrato", pos="50% 25%", kb="r",
          kick="UNA GANÓ UN ÓSCAR…", l1="…DESPUÉS DE PINTARSE DE VERDE", t1=w("pintarse de verde"), fs1=72)
    S.add("foto", w("otra que estudió"), "latigo", img="portman-harvard-2015", pos="50% 30%", kb="l",
          kick="OTRA ESTUDIÓ EN HARVARD…", l1="…MIENTRAS FILMABA STAR WARS", t1=w("mientras filmaba"), fs1=72)
    S.add("foto", w("y otra que acaba"), "latigo", img="zendaya-holland-bnd", pos="50% 20%", kb="in",
          kick="Y OTRA ROMPIÓ UN RÉCORD", l1="ESTE VERANO", t1=w("este verano"), fs1=80)
    S.add("galeria", w("Y quédate hasta"), "pagina", kick="ANTES DE LA NÚMERO UNO", tk=w("antes de la número"),
          items=[("pugh-yelena", "¿?", w("las cuatro"), "50% 25%"), ("steinfeld-kate-vertical", "¿?", w("las cuatro") + 0.2),
                 ("larson-carol", "¿?", w("las cuatro") + 0.4, "50% 20%"), ("kirby-sue", "¿?", w("las cuatro") + 0.6, "55% 30%")],
          titulo="LAS QUE CASI ENTRAN", tt=w("casi entran"))


def reglas(S):
    w = S.w
    S.add("reglas", w("Tres reglas"), "pagina", kick="TRES REGLAS RÁPIDAS", items=[
        ("SOLO EL MCU", "El universo de los Avengers.", w("Uno")),
        ("NO SOLO LA CARA", "Presencia, carisma y un look que se queda grabado.", w("Dos")),
        ("ES MI TOP", "¿No estás de acuerdo? A los comentarios.", w("Y tres"))])
    S.add("titulo", w("Al final te pido"), "crece", kick="AL FINAL", l2="TU TOP 5", t2=w("tu top cinco"), fs2=220)


def n5(S):
    w = S.w
    S.add("portada", w("En el número cinco"), "pagina", n="5", tnum=w("cinco"), img="zoe-oscar-perfil", pos="45% 20%",
          nombre="ZOE", apellido="SALDAÑA", rol="Gamora · Guardianes de la galaxia", tn=w("Zoe Saldaña"), trol=w("Gamora"),
          lines=[("La más peligrosa de la galaxia", w("la mujer más peligrosa"))])
    S.add("contactos", w("Para ser Gamora"), "pagina", imgs=[("zoe-gamora-prueba-maquillaje", "50% 20%"), ("zoe-gamora-set-croma", "52% 30%"),
          ("zoe-gamora-retrato", "50% 25%"), ("zoe-gamora-polaroid", "45% 25%")], elegida=2, tc=w("su mirada"),
          kick="HORAS DE MAQUILLAJE, CADA DÍA", tk=w("horas"), titulo="CUBIERTA DE PINTURA VERDE", tt=w("pintura verde"))
    clip(S, "zoe-idiotas", "GUARDIANES DE LA GALAXIA · 2014")
    S.add("impresa", w("Pero hay algo"), "pagina", img="zoe-critics-rojo", pos="50% 15%", vertical=True, lado="izq",
          kick="NUEVA YORK · REP. DOMINICANA", tk=w("Nueva York"), titulo="HABLA ESPAÑOL", tt=w("habla español"),
          sub="Y antes de actuar, estudió ballet.", ts=w("estudió ballet"))
    S.add("impresa", w("Y su récord"), "crece", video="zoe-gamora-flotando", lado="der", kick="SU RÉCORD",
          dato=("", "3", "", "de las películas más taquilleras de la historia", w("las tres películas")),
          sub="Avatar · Avengers: Endgame · Avatar: el camino del agua", ts=w("Avatar"), fss=44)
    S.add("dato", w("En enero de este año"), "pagina", img="zoe-oscar-alfombra", pos="50% 15%", kick="ENERO 2026",
          pre="$", num="15", suf=" MIL M", label="la actriz más taquillera de la historia", tn=w("quince mil"),
          tl=w("actriz más taquillera"))
    S.add("foto", w("Y a quién le quitó"), "latigo", video="zoe-gamora-rostro", kb="in",
          kick="LO VAS A VER MÁS ADELANTE", tk=w("Lo vas a ver"), l1="¿A QUIÉN LE QUITÓ EL TRONO?", t1=w("quién le quitó"), fs1=70)
    S.add("foto", w("Por si fuera poco"), "pagina", img="zoe-oscar-escenario", pos="50% 35%", kb="in",
          kick="OSCAR 2025", l1="GANÓ EL ÓSCAR", t1=w("ganó el Óscar"))
    S.add("foto", w("Belleza disciplina"), "crece", img="zoe-oscar-perfil", pos="45% 20%", kb="l",
          kick="NÚMERO CINCO", tk=w("Número cinco"), l1="ZOE SALDAÑA", t1=w("Belleza"),
          sub="Belleza, disciplina y una carrera sin igual.", ts=w("disciplina"))


def n4(S):
    w = S.w
    S.add("portada", w("En el número cuatro"), "pagina", n="4", tnum=w("cuatro"), img="portman-cannes", pos="50% 12%",
          nombre="NATALIE", apellido="PORTMAN", rol="Jane Foster · Thor", tn=w("Natalie Portman"), trol=w("Jane Foster"),
          lines=[("La científica que levantó el martillo", w("la científica"))])
    S.add("dato", w("Natalie empezó"), "pagina", kick="EL PERFECTO ASESINO · 1994", num="12", suf=" AÑOS",
          label="su primer papel en el cine", tn=w("doce años"), tl=w("El perfecto asesino"), img="portman-jane-2011", pos="50% 30%")
    S.add("impresa", w("Y mientras filmaba"), "latigo", img="portman-harvard-2015", pos="50% 30%", lado="der",
          kick="REINA AMIDALA + UNIVERSIDAD", tk=w("la reina Amidala"), titulo="PSICOLOGÍA EN HARVARD", tt=w("psicología"),
          sub="Y se graduó.", ts=w("Y se graduó"))
    S.add("contactos", w("En dos mil once"), "pagina", imgs=[("portman-cisne-negro", "50% 30%"), ("portman-oscar-2011", "50% 20%"),
          ("portman-jane-2011", "50% 30%"), ("portman-jane-thor", "60% 30%")], elegida=1, tc=w("ganó el Óscar"),
          kick="2011", titulo="ÓSCAR Y THOR, EL MISMO AÑO", tt=w("el mismo año"))
    S.add("impresa", w("Durante años"), "pagina", img="portman-jane-thor", pos="60% 30%", lado="izq",
          kick="DURANTE AÑOS", titulo="“SOLO LA NOVIA DE THOR”", tt=w("la novia de Thor"), fst=84)
    S.add("foto", w("Hasta Thor"), "crece", img="portman-mighty-trono", pos="50% 30%", kb="in",
          kick="THOR: AMOR Y TRUENO · 2022", l1="LA PODEROSA THOR", t1=w("la Poderosa Thor"),
          sub="Entrenó durante meses.", ts=w("Entrenó"))
    clip(S, "portman-eat-my-hammer", "THOR: AMOR Y TRUENO · 2022")
    S.add("foto", w("Lo que hace distinta"), "pagina", img="portman-cannes", pos="50% 14%", kb="up",
          kick="SU SELLO", tk=w("su belleza"), sub="Un aire clásico, de estrella del cine antiguo.", ts=w("aire clásico"))
    S.add("impresa", w("Treinta años"), "latigo", img="portman-comiccon-martillo", pos="60% 30%", lado="der",
          kick="UNA CARA INOLVIDABLE", dato=("", "30", "", "años en pantalla", w("Treinta años")),
          sub="Y sigue siendo de las más reconocibles del mundo.", ts=w("sigue siendo"))
    S.add("impresa", w("Y ojo"), "pagina", img="doomsday-poster-oficial", pos="50% 20%", vertical=True, lado="der",
          kick="RUMOR · SIN CONFIRMAR", tk=w("los rumores"), titulo="¿VUELVE EN DOOMSDAY?", tt=w("podría volver"),
          sub="Marvel todavía no lo confirma.", ts=w("Marvel todavía"))
    S.add("foto", w("Ahora si crees"), "latigo", video="portman-mighty-grito", kb="in",
          kick="¿DEBERÍA ESTAR MÁS ARRIBA?", tk=w("más arriba"), l1="ESPERA AL Nº 3", t1=w("a quién puse"))


def n3(S):
    w = S.w
    S.add("portada", w("En el número tres"), "pagina", n="3", tnum=w("tres"), img="zendaya-metgala-flores", pos="78% 22%",
          nombre="", apellido="ZENDAYA", rol="MJ · Spider-Man", tn=w("Zendaya"), trol=w("MJ en Spider-Man"),
          lines=[("La más joven de la lista", w("la más joven"))])
    S.add("impresa", w("Llegó a Marvel"), "pagina", img="zendaya-mj-homecoming", pos="50% 30%", lado="der",
          kick="DE REGRESO A CASA · 2017", tk=w("de regreso a casa"), titulo="CASI NO SONREÍA", tt=w("casi no sonreía"),
          sub="Y aun así, se robó la película.", ts=w("se robó"))
    clip(S, "zendaya-call-me-mj", "SPIDER-MAN: DE REGRESO A CASA · 2017")
    S.add("contactos", w("Lo de Zendaya"), "pagina", imgs=[("zendaya-metgala-2024", "50% 15%"), ("zendaya-metgala-azul", "50% 12%"),
          ("zendaya-metgala-flores", "78% 22%"), ("zendaya-holland-premiere", "70% 15%")], elegida=0, tc=w("alfombra roja"),
          kick="ÍCONO DE LA MODA", tk=w("un ícono"), titulo="NOTICIA AL DÍA SIGUIENTE", tt=w("es noticia"))
    S.add("dato", w("Y como actriz"), "pagina", img="zendaya-mj-nwh", pos="50% 30%", kick="EUPHORIA", num="2",
          suf=" EMMY", cuenta=False, label="la más joven en ganarlo dos veces como mejor actriz de drama",
          tn=w("dos premios"), tl=w("la persona más joven"), fsl=38)
    S.add("dato", w("Este verano"), "latigo", img="zendaya-mj-bnd", pos="50% 30%", kick="SPIDER-MAN: UN NUEVO DÍA · 2026",
          pre="$", num="932", suf=" M", label="de estreno mundial · el segundo mejor de la historia",
          tn=w("novecientos treinta"), tl=w("El segundo mejor"), fsl=38)
    S.add("foto", w("Y fuera de la pantalla"), "pagina", img="zendaya-holland-bnd", pos="50% 20%", kb="in",
          kick="JUNIO 2026 · TOM HOLLAND LO CONFIRMÓ", tk=w("Tom Holland"), l1="PETER Y MJ, EN LA VIDA REAL",
          t1=w("Peter Parker"), fs1=76, sub="Número tres.", ts=w("Número tres"))


def n2(S):
    w = S.w
    S.add("portada", w("En el número dos"), "pagina", n="2", tnum=w("dos"), img="olsen-corona-retrato", pos="50% 20%",
          nombre="ELIZABETH", apellido="OLSEN", rol="Wanda · la Bruja Escarlata", tn=w("Elizabeth Olsen"),
          trol=w("Wanda Maximoff"), lines=[("La más poderosa del universo Marvel", w("la mujer más poderosa"))])
    S.add("impresa", w("Primer dato curioso"), "pagina", img="olsen-con-hermanas", pos="50% 25%", lado="der",
          kick="LA HERMANA MENOR", tk=w("la hermana menor"), titulo="LAS GEMELAS OLSEN", tt=w("las gemelas"),
          sub="De niña pensó en cambiarse el apellido.", ts=w("pensó en cambiarse"))
    S.add("contactos", w("Llegó a Marvel"), "pagina", imgs=[("olsen-wanda-ultron", "50% 25%"), ("olsen-wandavision-traje", "45% 25%"),
          ("olsen-bruja-darkhold", "50% 30%"), ("olsen-bruja-corona", "50% 25%")], elegida=3, tc=w("la villana"),
          kick="2015 → 2022", tk=w("era de Ultrón"), titulo="DE CHICA ASUSTADA A VILLANA", tt=w("chica asustada"))
    clip(S, "olsen-took-everything", "AVENGERS: ENDGAME · 2019")
    S.add("impresa", w("Con WandaVision"), "pagina", img="olsen-wandavision-cocina", pos="50% 30%", lado="izq",
          kick="WANDAVISION · 2021", titulo="NOMINADA AL EMMY", tt=w("nominación al Emmy"))
    S.add("foto", w("Su belleza tiene algo"), "crece", video="olsen-wakanda-poder", kb="in",
          kick="SU SELLO", tk=w("pocas logran"), sub="Dulce en una escena. Aterradora en la siguiente.", ts=w("puede verse dulce"))
    S.add("foto", w("Y esta es la noticia"), "pagina", img="visionquest-wanda-revive", pos="50% 40%", kb="in",
          kick="VISIONQUEST · FINAL · 10 NOV", tk=w("el final de VisionQuest"), l1="DOOM LA REVIVE", t1=w("Doctor Doom"))
    S.add("cita", w("Bruja Escarlata despierta"), "crece", img="doom-doomsday", pos="50% 30%",
          texto="Bruja Escarlata, despierta. Tu poder será mío.", autor="DOCTOR DOOM · VISIONQUEST",
          tq=w("Bruja Escarlata despierta"), ta=w("será mío"))
    S.add("impresa", w("Ella había dicho"), "pagina", img="doomsday-poster-teaser", pos="50% 30%", vertical=True, lado="der",
          kick="AVENGERS: DOOMSDAY · 18 DIC", tk=w("no estaría"), titulo="TODO INDICA QUE VUELVE", tt=w("todo indica"),
          sub="Número dos.", ts=w("Número dos"))


def menciones(S):
    w = S.w
    S.add("titulo", w("Antes del número uno"), "pagina", kick="ANTES DEL Nº 1", l2="LAS QUE CASI ENTRAN",
          t2=w("las cuatro"), fs2=150)
    S.add("foto", w("Florence Pugh"), "crece", img="pugh-yelena", pos="50% 25%", kb="in", kick="YELENA · THUNDERBOLTS*",
          tk=w("Yelena Belova"), l1="FLORENCE PUGH", t1=w("Florence Pugh") + 0.2, sub="Estará en Doomsday.", ts=w("estará en Doomsday"))
    S.add("foto", w("Hailee Steinfeld"), "latigo", img="steinfeld-kate-arco", pos="50% 30%", kb="l", kick="KATE BISHOP · OJO DE HALCÓN",
          tk=w("Kate Bishop"), l1="HAILEE STEINFELD", t1=w("Hailee Steinfeld") + 0.2, sub="La heredera del arco y la flecha.",
          ts=w("La heredera"))
    S.add("foto", w("Brie Larson"), "latigo", img="larson-carol", pos="50% 25%", kb="r", kick="CAPITANA MARVEL",
          tk=w("Capitana Marvel"), l1="BRIE LARSON", t1=w("Brie Larson") + 0.2,
          sub="La primera superheroína en pasar los $1,000 M.", ts=w("La primera película"))
    S.add("foto", w("Y Vanessa Kirby"), "latigo", img="kirby-sue", pos="55% 30%", kb="in", kick="SUE STORM · 4 FANTÁSTICOS",
          tk=w("Sue Storm"), l1="VANESSA KIRBY", t1=w("Vanessa Kirby") + 0.2, sub="De invisible no tiene nada.",
          ts=w("de invisible no"))
    t = w("Alguna de ellas")
    S.add("galeria", t, "pagina", kick="¿DEBIÓ ENTRAR ALGUNA?", tk=t + 0.1,
          items=[("pugh-yelena", "PUGH", t + 0.1, "50% 25%"), ("steinfeld-kate-vertical", "STEINFELD", t + 0.3),
                 ("larson-carol", "LARSON", t + 0.5, "50% 20%"), ("kirby-sue", "KIRBY", t + 0.7, "55% 30%")],
          titulo="PERO AHORA SÍ…", tt=w("Pero ahora sí"))


def n1(S):
    w = S.w
    S.add("portada", w("En el número uno"), "pagina", n="1", tnum=w("uno"), img="scarlett-oscar-2025", pos="50% 18%",
          nombre="SCARLETT", apellido="JOHANSSON", fsn=104, rol="Natasha Romanoff · Black Widow", tn=w("Scarlett Johansson"),
          trol=w("Natasha Romanoff"), lines=[("La Viuda Negra", w("la Viuda Negra"))])
    S.add("impresa", w("Y aquí está la historia"), "pagina", img="scarlett-natasha-retrato", pos="50% 25%", lado="der",
          kick="LA HISTORIA QUE CASI NADIE CONOCE", tk=w("casi nadie"), titulo="NO ERA PARA ELLA", tt=w("no era para ella"),
          sub="Hizo la audición… y la rechazaron.", ts=w("la rechazaron"))
    S.add("titulo", w("El papel fue para"), "crece", kick="EL PAPEL FUE PARA", l2="EMILY BLUNT", t2=w("Emily Blunt"),
          sub="Tuvo que dejarlo por otro contrato.", ts=w("tuvo que dejarlo"))
    S.add("foto", w("Y Scarlett tuvo"), "pagina", img="scarlett-ironman2-pose-h", pos="50% 30%", kb="in",
          kick="SEGUNDA OPORTUNIDAD", tk=w("segunda oportunidad"), l1="LA APROVECHÓ", t1=w("La aprovechó"))
    S.add("foto", w("Debutó en Iron Man"), "latigo", video="scarlett-pasillo-camina", kb="in",
          kick="IRON MAN 2 · 2010", tk=w("Iron Man"), l1="LA PELEA DEL PASILLO", t1=w("una pelea"))
    S.add("foto", w("Y en Avengers"), "latigo", img="scarlett-natasha-avengers", pos="50% 20%", kb="up",
          kick="THE AVENGERS · 2012", tk=w("Y en Avengers"), l1="SIN SUPERPODERES", t1=w("no necesitaba"))
    clip(S, "scarlett-on-hold", "THE AVENGERS · 2012")
    S.add("contactos", w("Después más de diez"), "pagina", imgs=[("scarlett-ironman2-pose", "50% 20%"), ("scarlett-natasha-ultron", "50% 25%"),
          ("scarlett-endgame-vormir", "40% 30%"), ("scarlett-blackwidow-2021", "50% 25%")], elegida=3, tc=w("su inteligencia"),
          kick="2010 — 2021", tk=w("diez años"), titulo="LA ÚNICA AVENGER ORIGINAL", tt=w("la única Avenger"))
    S.add("impresa", w("La revista Esquire"), "pagina", img="scarlett-esquire-2013", pos="50% 20%", vertical=True, lado="der",
          kick="ESQUIRE · 2006 · 2013", tk=w("La revista Esquire"),
          dato=("", "2", "", "veces “la mujer más sexy del mundo”", w("dos veces")),
          sub="La única mujer que lo ha logrado.", ts=w("Es la única"))
    S.add("dato", w("Y en dos mil veinticinco"), "pagina", img="scarlett-jurassic-rebirth", pos="50% 30%",
          kick="JURASSIC WORLD: RENACE · 2025", pre="Nº ", num="1", cuenta=False,
          label="la protagonista más taquillera de la historia", tn=w("la protagonista"), tl=w("más taquillera"))
    t = w("Te acuerdas")
    S.add("galeria", t, "latigo", pw=440, kick="LAS DOS MÁS TAQUILLERAS DEL CINE", tk=t,
          items=[("zoe-oscar-perfil", "ZOE SALDAÑA", w("Zoe Saldaña"), "45% 20%"),
                 ("scarlett-natasha-retrato", "SCARLETT JOHANSSON", w("Las dos mujeres"), "50% 25%")],
          titulo="SALIERON DE MARVEL", tt=w("salieron de Marvel"))
    S.add("foto", w("Scarlett no está"), "pagina", img="scarlett-blackwidow-2021", pos="50% 30%", kb="in",
          kick="NO ESTÁ EN DOOMSDAY", tk=w("no está en Doomsday"), sub="“Extraño a mis compañeros.”", ts=w("extraña"))
    S.add("foto", w("Pero no le hace falta"), "crece", img="scarlett-cannes-alfombra", pos="35% 40%", kb="in",
          kick="PARA MILLONES", tk=w("Para millones"), l1="NÚMERO UNO", t1=w("Número uno"),
          sub="Nadie ha estado a su altura.", ts=w("nadie ha estado"))


def cierre(S):
    w = S.w
    S.add("podio", w("Ese es mi top"), "pagina", kick="MI TOP 5", items=[
        ("zoe-oscar-perfil", 5, "ZOE", w("Zoe"), "45% 20%"), ("portman-cannes", 4, "NATALIE", w("Natalie"), "50% 12%"),
        ("zendaya-metgala-flores", 3, "ZENDAYA", w("Zendaya"), "78% 22%"), ("olsen-corona-retrato", 2, "ELIZABETH", w("Elizabeth"), "50% 20%"),
        ("scarlett-oscar-2025", 1, "SCARLETT", w("Scarlett"), "50% 18%")])
    S.add("cta", w("Ahora te toca"), "pagina", tl=w("Escribe tu top"), tt=w("Escribe tu top"),
          sub="¿Quién falta? Te leo en los comentarios.", ts=w("quién falta"))
    S.add("impresa", w("Y si quieres saber"), "crece", img="doomsday-poster-oficial", pos="50% 20%", vertical=True, lado="der",
          kick="SERIE EN EL CANAL", tk=w("una serie entera"), titulo="CAMINO A DOOMSDAY", tt=w("el camino"),
          sub="Te espera en el canal.", ts=w("Te espera"))
