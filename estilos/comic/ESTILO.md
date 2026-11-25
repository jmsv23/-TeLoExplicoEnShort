---
nombre: Cómic (Camino a Doomsday)
voz: narrador-comics
ejemplo: 2026-11-analisis-trailer-final-doomsday
---

# Estilo «Cómic»

**Cuándo usarlo:** Marvel y DC, superhéroes, cómics, tráilers y teorías de películas de superhéroes. Es el estilo de la serie *Camino a Doomsday*, la de más éxito del canal. Sirve para largos (16:9) y shorts (9:16).

**Motor propio.** No usa planos `r_<tipo>`: las escenas se escriben con la API de escenas de `lib_h.py`, en `escenas/<pieza>/<sección>.py` con `def build(S)` (helpers comunes en `_k.py`).
- Catálogo: `./tl planos comic`.
- Ejemplos de referencia: `videos/2026-11-analisis-trailer-final-doomsday/escenas/largo/` (16:9) y `…/escenas/short-01/` (9:16).

**Config por pieza** (`video.json → piezas[i]`):
- `"comic": {"partes": [...], "dias": 24, "placa": ["d(\\d+)", "DETALLE", 10]}`:
  - `partes`: grupos de secciones, una composición por parte;
  - `dias`: contador «FALTAN N DÍAS» (null = sin contador);
  - `placa`: «DETALLE N / 10».
- `"partes": true` renderiza el largo parte por parte.
- `"gaps"` y `"clip_lufs"` ajustan las pausas y el volumen de los clips.

**Música:** `video.json → "musica": {"comic": {"<sección>": "hook|misterio|accion|doom|bonus", "_defecto": "misterio"}}`. Las pistas son `audio-lib/musica/comic-*.wav`.

**SFX:** `audio-lib/sfx/comic/`, con variantes `nombre-N.wav` en rotación. Los nombres los emite el motor (bam, pop, stamp, slam, whoosh, whoosh2, braam, ding, ink, pageflip…).

**Recursos del estilo:** `shared/` (comic.css/js, comic-objects.js, kits h/v, explicando.css/js) y `shared/fonts/`. `lib.py` trae los helpers SVG (portal, shield, globe…).

---

## Ficha original (de camino-a-doomsday/_estilo.md)

> Escrita para los Shorts 01-11. Los largos LF01-LF04 y el short LF04s aplican la misma paleta, tipografía y códigos de animación con el motor `lib_h`.


Este es el estilo **propio de esta serie**. No toca ni modifica `_base/estilo-visual.md`, que sigue siendo el estilo del canal para las demás series; aquí solo se define una paleta, tipografía, ilustración y animación distintas para "Camino a Doomsday". Del estilo base se queda igual: formato 1080 × 1920 a 30 fps, zonas seguras, marca "explicando", palabras clave en lugar de subtítulos, máximo 6 palabras en pantalla y textos de 40 px o más.

Del ritmo de `_base/animacion.md` se queda la sincronía con la sílaba tónica, pero **esta serie es más rápida** (ver "Ritmo").

Sensación buscada: **un cómic que se mueve**. Tinta gruesa, puntos de imprenta, viñetas que chocan, onomatopeyas que golpean la pantalla. Colores saturados y planos, nada realista. Quien ve el video tiene que sentir que está pasando las páginas de un número especial, a toda velocidad.

Público: fans de superhéroes y cómics, mayoría hombres. Por eso el tono visual es **de tienda de cómics, no de caricatura infantil**: contrastes duros, sombras de tinta negra, ángulos dramáticos, villano imponente. Lo divertido viene del ritmo y los golpes de texto, no de personajes tiernos.

## Paleta: cada color significa algo (igual en los 11 videos)

| Token | Hex | Significado |
|---|---|---|
| `--tinta` | `#0B0B14` | Contornos, sombras duras, texto sobre color claro |
| `--papel` | `#FFF3D6` | Fondo base claro (papel de cómic) |
| `--heroe` | `#1E5BFF` | **Héroes, el bien, Tierra-616 (el MCU principal)** |
| `--rojo` | `#E8212B` | **Acción, peligro, impacto, "dato que sorprende"**. Fondo de golpe corto |
| `--amarillo` | `#FFD400` | **Narrador** (la caja de texto) y lo que hay que recordar (resaltador) |
| `--doom` | `#1FA85A` | **Doctor Doom, Latveria, el villano**. Nunca significa "bien" en esta serie |
| `--multi` | `#8A2BE2` | **Multiverso, magia, Loki, Línea Sagrada, incursiones** |
| `--ciencia` | `#00C8E8` | **Ciencia y tecnología**: Cuatro Fantásticos, Reed, Tony |
| `--ceniza` | `#6B7280` | Información neutra, metal, fondos de relleno |

**Fondos de escena**: rotan entre `papel`, `heroe`, `multi`, `doom` y `ciencia`, con la regla de color-significado (el fondo `doom` solo cuando habla Doom o su plan; el `multi` cuando es multiverso). El `rojo` de fondo solo en golpes cortos (≤ 1.5 s; ≤ 3 s en el giro). Sobre fondos de color, el texto va en `papel` o `amarillo` con contorno `tinta`.

**Textura** (el sello visual): **trama de puntos Ben-Day** al 15 % en sombras y fondos, y **líneas de velocidad** radiales en los golpes. Grano de impresión al 4 % encima de todo. Los colores se ven "impresos": ligero desfase de color (misregistration) de 3–4 px en los contornos de lo más importante.

## Tipografía

| Uso | Fuente | Peso / tamaño |
|---|---|---|
| Onomatopeyas, palabras clave, remates | **Bangers** | 140–260 px, MAYÚSCULAS, inclinadas −4° a −8° |
| Títulos, nombres propios, números, fechas | **Anton** | 120–240 px, MAYÚSCULAS, tracking 0 |
| Caja de narrador, globos de diálogo, etiquetas | **Comic Neue** | 700, 48–64 px |

- Las palabras clave llevan contorno `tinta` de 8 px y **sombra dura** desplazada (10 px, 10 px, `tinta`). Las onomatopeyas llevan además un contorno exterior `papel` de 6 px (como pegatina).
- Ningún texto por debajo de 48 px.
- Los acentos y la ñ se verifican en cada render (Bangers y Anton los traen, pero revisa "ÑAN", "MÁS", "DOOMSDAY").

## El narrador y las viñetas

No hay mascota. El que habla es **el narrador de cómic**: una **caja amarilla** con borde `tinta` y esquina cortada, que aparece en una esquina de la viñeta y trae solo 3–6 palabras clave. Es el equivalente de la voz de la serie, y de ahí el nombre del audio de referencia (`narrador-de-comics.mp3`).

| Recurso | Aspecto | Uso |
|---|---|---|
| **Portada** | Cada video abre como la **portada de un número**: logo "CAMINO A DOOMSDAY", cuadro "N.º 03 de 11", ilustración del tema, precio en broma ("GRATIS") | HOOK (primer 1 s) y también hace de miniatura |
| **Viñetas** | Cuadros con borde `tinta` de 10 px y canal blanco de 24 px entre ellos. Se rompen, se inclinan y se salen del marco para dar impacto | Estructura de casi todas las escenas |
| **Contador Doomsday** | Placa de cómic arriba a la derecha dentro de la zona de contenido: "FALTAN 36 DÍAS" (se recalcula en cada publicación; el estreno es el 18 de diciembre de 2026) | Todos los videos, fijo, con `PULSE` en el remate |
| **Globos y pensamientos** | Globos redondos para lo que dice un personaje, nube con burbujas para lo que piensa. Máximo 6 palabras | Doom diciendo "inevitable", Cap pensando "¿quién soy?" |
| **Cintas de tema** | Cinta diagonal `rojo` o `multi` con el título del dato ("INCURSIÓN", "SECRET WARS") | Presentar conceptos nuevos |

## Ilustración de personajes

- **Estilo cómic de tinta**: línea gruesa con grosor variable (más gruesa en el lado de la sombra), relleno plano de la paleta, **sombra de tinta negra con trama**. Anatomía heroica, poses de tres cuartos y ángulos bajos para el villano.
- **Siluetas y símbolos antes que caras.** Los actores reales no se dibujan: Doom aparece como **máscara, armadura y capa verde**; Cap como **escudo**; los Cuatro Fantásticos como **el "4" y sus poderes**; los X-Men como **la "X" y sus siluetas**. Esto evita problemas de parecido, mantiene el estilo uniforme y permite hablar de "el actor" sin mostrar su cara.
- **Fotos o stills oficiales** (`assets/`): solo como recorte pequeño, con trama de puntos y marco de viñeta, ≤ 2 s, para mostrar "esto es real". Nunca a pantalla completa.
- **Objetos de las analogías** (balón y portería, control de videojuego, brazalete de capitán, alineación titular, partidas en paralelo) se dibujan en el mismo estilo de tinta y llevan los colores de su significado.
- Sin emojis: todo se dibuja.

## Ritmo: rápido

La serie es de fans que ya saben ver cómics y tráilers, así que **el corte manda**:

- **Cambio visual cada 1.2 s o menos** (la base pide 1.5 s). Un cambio es: viñeta nueva, golpe de texto, zoom, corte a otro ángulo.
- **Nada quieto más de 0.4 s.** Todo respira: balanceo, temblor leve, líneas de velocidad, trama en movimiento.
- Mínimo **un golpe de onomatopeya cada 5 s** (ver catálogo).
- El HOOK es un golpe en el cuadro 3 (como en la base) y se resuelve en 3 s.
- El GIRO lleva **0.5 s de silencio**, luego `FLASH-BLANCO` y `ZOOM-GOLPE`.
- El PAYBACK regresa a la analogía con el mismo dibujo del desarrollo, pero **terminado** (la portería llena, el brazalete puesto).
- El CTA anuncia el siguiente capítulo con una **portada del siguiente número** que entra deslizándose.

## Animación: códigos propios

Se mantienen `STAMP`, `WORD-POP`, `SHAKE`, `ZOOM-THRU`, `COUNT-UP`, `DRAW-ON` y `PULSE` de `_base/animacion.md`. Cambian o se agregan:

| Código | Descripción | Duración |
|---|---|---|
| `PANEL-SLAM` | Una viñeta entra desde fuera de la pantalla con rotación de 3–5°, rebota y se asienta; el canal blanco se rellena | 0.3 s |
| `PANEL-SPLIT` | La pantalla se divide en 2–4 viñetas con diagonales que cortan, cada una entra con su `PANEL-SLAM` | 0.4 s |
| `PANEL-BREAK` | Un personaje u objeto rompe el borde de su viñeta y la sobrepasa | 0.3 s |
| `ONOMATO` | Una onomatopeya (BAM, KRAKOOM, ZAP, ¡BOOM!) crece de 0 a 120 % con rotación y vuelve a 100 %; salpicadura de líneas de velocidad | 0.25 s |
| `SPEED-LINES` | Líneas radiales o paralelas que cruzan la pantalla hacia un punto | 0.4 s o continuo |
| `HALFTONE-WIPE` | La escena nueva entra con una barrida de puntos Ben-Day que crecen | 0.35 s |
| `INK-SPLASH` | Una mancha de tinta negra llena la pantalla para el corte (para Doom) | 0.3 s |
| `ZOOM-GOLPE` | Zoom rápido de 100 % a 125 % con `CAM-PUNCH` en el cuadro del golpe y regreso lento | 0.2 s + 0.5 s |
| `FLASH-BLANCO` | Cuadro completo en `papel` o blanco 4 frames, y regresa con color | 0.13 s |
| `PAGE-FLIP` | Cambio de página tipo cómic (la esquina se dobla y revela la siguiente) | 0.4 s |
| `MISREG` | El contorno de color se desfasa 3–4 px un instante, como impresión barata | 0.15 s |
| `CAPTION-DROP` | La caja del narrador cae a su esquina y escribe sus palabras | 0.3 s |
| `COVER-SLIDE` | La portada del siguiente número entra al CTA desde la derecha | 0.4 s |

**Curvas**: `back.out(1.7)` y `power4.out` para golpes; `elastic` solo para las onomatopeyas. Squash & stretch en lo que cae o choca (los autos de la incursión, el balón).

## Sonido

Vocabulario de SFX propio: `whoosh` (corte de viñeta), `slam` (`PANEL-SLAM`), `bam` (onomatopeya), `zap` (poder), `page-flip` (cambio de página), `ink` (`INK-SPLASH`), `record-scratch` (mito o giro), `heartbeat` (momento de tensión), `ding` (dato confirmado), `stinger` (el golpe de Doom).

**Música**: orquestal-electrónica de tráiler, bajo contundente, 120–135 BPM, a −20 dB bajo la voz. Se corta 0.5 s antes del giro. En el ep 11 (lista) sube un poco la energía para cerrar la serie.

## Anti-patrones de esta serie

- Estética infantil o "sticker pack": aquí hay tinta y sombra dura.
- Caras de actores reales o capturas de película a pantalla completa.
- Fondos degradados, brillos suaves o sombras difusas: todo es plano y entintado.
- Un `doom` verde en algo positivo, o un `heroe` azul en algo del villano.
- Escenas estáticas de más de 0.4 s o diapositivas con listas.
- Texto que transcribe la narración: solo palabras clave y golpes.
- Más de 3 onomatopeyas visibles a la vez: se vuelve ruido.
- Mostrar el contador del estreno con un número viejo: recalcúlalo al publicar.
