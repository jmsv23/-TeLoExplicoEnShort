# Brief LF04 — Análisis del TRÁILER FINAL de Avengers: Doomsday (oficial)
Investigado 2026-11-23, el mismo día del tráiler. Largo 16:9 + 1 Short 9:16. Canal: **Te lo explico en Short** (nueva línea: cultura pop → cómics/superhéroes, cine, videojuegos; tono explicativo/noticias).

## Fuentes descargadas
| Archivo | Qué es |
|---|---|
| `fuente/trailer.mp4` | «Avengers: Doomsday \| Tráiler Oficial \| Subtitulado», Marvel Latinoamérica Oficial, 23-nov-2026, 3:15, 1080p, audio inglés + subtítulos ES quemados (222 mil vistas al bajarlo) |
| `fuente/tiktok-analisis.mp4` | Análisis de @pacohdez77 (España), 10:00, vertical, 198 mil vistas el primer día |
| `transcripcion/*.{txt,srt,json}` | WhisperX medium (tráiler en `en`, TikTok en `es`) |
| `analisis/trailer.json`, `analisis/tiktok.json` | Gemini 3.5-flash (una pasada por video; script `analisis/_scripts/analizar.py`) |
| `_revision/trailer-{1..4}.png` | Hojas de contacto 1 fps con tiempo (**usar estos tiempos**: los de Gemini se desfasan a partir de 1:00 y llegan a 3:35 en un video de 3:15) |

## Mapa del tráiler (tiempos verificados en las hojas)
| Tiempo | Qué se ve | Subtítulo | Notas |
|---|---|---|---|
| 0:00-0:40 | Casa de Steve y Peggy. Steve con barba; bebé; baúl con el traje de Cap; el hijo crece (escuela, bici, sombrero de vaquero) | «Tomamos la decisión que sabíamos era correcta» · «¿Por qué se siente tan mal mentirle?» · «¿Cómo sabrá quiénes somos si no se lo decimos?» · «Steven Grant Rogers… ¿crees que ese chico no sabe quién eres?» | **El tráiler NO abre en Latveria** (la filtración lo decía) |
| 0:41-0:46 | Los 4 Fantásticos llegan de noche al jardín | Reed: «¿Eres Steve Rogers?» | |
| 0:47-0:52 | Logo Marvel Studios rojo → corona flotando con el reactor de Tony | | Funeral de Endgame |
| 0:53-0:57 | Blanco y negro: maletín con las Gemas, Steve en la plataforma cuántica, Scott Lang | «Años atrás… hicimos lo necesario…» | Flashback de Endgame |
| 0:59-1:03 | Steve y Peggy llegan en una camioneta azul a la casa amarilla | «…para restaurar el mundo» | |
| 1:04-1:20 | Los 4F en la sala con chimenea; entra el hijo adolescente | «Pero no sabíamos que esas decisiones tendrían consecuencias» · «¡Santo cielo!» · «Papá, ¿eras un superhéroe?» · «Éramos seis. Nos llamaban los Vengadores.» | **Momento más emotivo** |
| 1:21-1:22 | Tarjeta **«16 DE DICIEMBRE»** | | ⚠️ ver «Fecha» |
| 1:23-1:26 | Doom en una catedral verde de Latveria; tres figuras con máscaras doradas | «Todos ustedes…» | Aquelarre/brujas |
| 1:27-1:31 | Despegue de la nave 4F; Peggy y el hijo miran; Steve y Reed en la nave; Thor | «…han vivido vidas robadas…» | |
| 1:33 | Nueva York de noche con **otro planeta en el cielo** | | **Incursión** |
| 1:35-1:42 | Thor con rayos azules vs Doom; ruinas con estatua; Thor sale volando | «…pero ahora tienen que devolverlas.» | |
| 1:43-1:46 | Torre de los Vengadores; anillo brillante; Shang-Chi en un edificio | | |
| 1:47-1:52 | Thunderbolts en la torre; **Kate Bishop**; quinjet; Thor; Yelena | Thor: «No sé qué hacen… ni quiénes son la mitad de ustedes» | |
| 1:53-1:57 | **Cíclope vs Sam Wilson** en una sala de madera (parece la Mansión X) | «Dejen de pelearse por tonterías» | Los héroes chocan primero |
| 1:58-2:05 | Nave 4F aterriza; 4F en la nave; **Steve abraza a Bucky** (Sam mira); Thunderbolts | «Ha llegado la hora. Únanse y manténganse juntos.» | |
| 2:06-2:08 | Muro de agua en Wakanda; **Shuri** con Dora Milaje | «Si no logran confiar en ellos…» | |
| 2:09-2:11 | Steve en la nave… **con el Mjolnir en la mano** | «…ojalá confíen en mí» | |
| 2:12-2:16 | Sue con sus poderes; Thor con **rayos dorados** en el bosque; alguien cae de la nave; magia verde | | Rayo dorado = teoría Fuerza Odín |
| 2:17-2:19 | Doom con brazos abiertos frente a su ejército | «Vamos… a empezar.» | |
| 2:20-2:22 | Bestia y **Cíclope** | «**A mí, mis X-Men.**» | La polémica |
| 2:24-2:42 | Batalla: Gámbito, Mystique, Sam, la Antorcha, Shang-Chi, Reed, Thor, Steve con escudo en el suelo… robots con **rayos desde las palmas**; rayo de Cíclope | | |
| 2:43-2:49 | Título AVENGERS: DOOMSDAY | | |
| 2:51-3:01 | Torre: Thor y Steve. «Qué buen discurso diste» «Gracias» «El tuyo estuvo… flojo para lo que es Cap, ¿no crees?» → Steve sostiene el Mjolnir: «No estás molesto por esto, ¿no?» Thor: «Sabes que sí.» | | Chiste final |
| 3:01 | **El castillo de Doom en medio de rascacielos de Nueva York**, con un haz de luz | | Último plano: ¿mundos fusionados = Battleworld? |
| 3:02-3:14 | Infinity Vision · 16 de diciembre · contador 00:24:15:00:00 | | |

## Lo que confirmó el tráiler (CONFIRMADO = se ve)
Steve vive en la línea temporal que creó en Endgame con Peggy y **tiene un hijo adolescente** que no sabía que su padre fue Capitán América · los 4F van a buscarlo · el viaje en el tiempo de Endgame **«tuvo consecuencias»** · Doom acusa a todos de vivir «vidas robadas» · incursión sobre Nueva York · Thunderbolts/Nuevos Vengadores en la torre, Kate Bishop, Shuri, Bucky, Sam · **Steve lleva el Mjolnir** · Cíclope dice «A mí, mis X-Men» · Gámbito, Mystique, Bestia · Doom tiene un ejército robótico.

## Lectura de imagen y teorías (siempre con sello)
- **Teoría (TikTok):** la línea de Steve sería la Tierra-828 (la de los 4F). Débil: los 4F viajan a su casa en nave. Decir «hay quien cree».
- **Teoría:** rayo dorado = Fuerza Odín (en el bosque Thor le rezaba a Odín en un tráiler anterior). En la pelea contra Doom, el rayo es azul.
- **Teoría:** alguna de las brujas sería Wanda (Olsen está confirmada para Doomsday según el usuario; la de la bruja de Latveria es especulación).
- **Teoría (TikTok):** el que sostiene el Mjolnir podría ser Loki (por eso a Thor le molesta). En Endgame Thor celebró «¡lo sabía!» cuando Steve levantó el martillo: la molestia es un chiste/contradicción → debate.
- **Lectura:** el castillo en Nueva York sugiere mundos que se fusionan → Battleworld (enlazar con LF03 Secret Wars).
- **Confirmado (decisión del usuario):** el ejército de Doom son Centinelas del universo de los X-Men (Yahoo: «Doom leads an army of Sentinels»). Narración: los Vengadores pelearán contra Doom en el universo de los X-Men y Doom usará a sus Centinelas contra ellos.
- **Dato de cómic:** James Rogers, hijo de Steve y Natasha en *Next Avengers: Heroes of Tomorrow* (2008, animada). Correcto según la verificación.

## Filtración (LF02) vs tráiler real — marcador
| Lo filtrado | Resultado |
|---|---|
| Abre en Latveria | ❌ abre en la casa de Steve (Latveria sale a la mitad) |
| Reencuentro Steve–Thor extendido | ✅ escena final completa |
| Steve, Thor y Reed contra Doom | 🟡 están los tres; Thor pelea con Doom |
| Nightcrawler y Bestia | ✅ Bestia se ve; Nightcrawler según la prensa (Yahoo) |
| Cíclope dispara | ✅ (no se ve que Doom casi lo mate) |
| Se oye a Yelena | 🟡 aparece, no habla |
| Loki en su trono, aterrado | ❌ no aparece |
| Magneto | ❌ no aparece |
| Wolverine, Deadpool, telarañas | ❌ no aparecen |
| Cae Tierra-10005, la Torre y el Baxter | 🟡 hay incursión sobre NY; la torre sigue en pie |
| Título, fecha y contador | ✅ hay contador real |
| Millones de Doombots | 🟡 hay un ejército, no «millones» volando |
| «Algún día me perdonarán» | ❌ la frase es «vidas robadas… tienen que devolverlas» |
**Total: 4 ✅ · 4 🟡 · 5 ❌.** Gancho: «la filtración acertó menos de la mitad».

## El TikTok de análisis: qué tomamos y qué mejoramos
- Toma: lectura escena por escena, la polémica de «A mí, mis X-Men» (dice que «le robaron el momento del cine»), la contradicción del Mjolnir, el póster que copia al de Iron Man 2008 (no lo verificamos visualmente: no usar sin ver el póster).
- Mejora: hook en 3 s con la tesis (no 2 min de opinión antes del primer dato), sellos CONFIRMADO/TEORÍA, rótulos para cada Tierra, menos queja personal, marcador contra la filtración y un cierre que lleve al siguiente video.
- Su afirmación de que suena el tema de los Vengadores en vez del de X-Men: **no verificada**, no usar.

## Fecha ⚠️
La tarjeta del tráiler **latino** dice **16 de diciembre** y el contador final marca 24 d 15 h. La prensa mexicana (Claro Sports, El Universal) decía 17-dic; EE. UU. 18-dic (Yahoo). **El guion dice «en el tráiler latino aparece el 16 de diciembre» sin afirmar que se adelantó.** Confirmar con Cinépolis/Cinemex antes de publicar.

## Fuentes
- Tráiler oficial: https://youtu.be/DWEectBgE0Y
- TikTok análisis: https://vt.tiktok.com/ZSsLpo6y6/
- Yahoo (Tom Parfitt, 23-nov-2026): https://www.yahoo.com/entertainment/movies/article/avengers-doomsday-final-trailer-gives-first-look-at-hailee-steinfeld-plus-3-other-things-we-spotted-144448737.html
- ScreenCrush: https://screencrush.com/final-avengers-doomsday-trailer/ · Screen Rant: https://screenrant.com/avengers-doomsday-final-trailer-breakdown-new-scenes-ranked-explained/ · GamesRadar (no se pudo leer)
- Fecha MX: https://www.clarosports.com/tendencias/cine-y-tv/avengers-doomsday-revelan-el-trailer-oficial-de-la-esperada-pelicula-de-marvel-y-vuelve-un-querido-personaje/
