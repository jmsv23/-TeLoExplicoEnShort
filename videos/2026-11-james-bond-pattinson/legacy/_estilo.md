# Estilo "Esmoquin": James Bond (Short + largo)

Elegante, negro y oro, de ritmo pausado. **No es cómic**: nada de semitonos, viñetas,
onomatopeyas ni cortes frenéticos. El estilo cómic queda solo para Marvel.

Frames de referencia: `_estilo/board.html` (`#f1`…`#f5`) → `_estilo/f*.png`, `sheet-h.jpg`, `sheet-v.jpg`.

## Voz

**"narrador comics"** (Voicebox). Solo la voz: el estilo visual no es de cómic.

## Paleta (tokens)

| Token | Hex | Uso |
|---|---|---|
| `--negro` | `#07070a` | fondo base (con viñeta radial a `#16161b`) |
| `--carbon` | `#111115` | paneles |
| `--linea` | `#2a2a31` | anillos y barras inactivas |
| `--oro` | `#c8a45c` | acentos, etiquetas, reglas |
| `--oro-claro` | `#ecd59b` | brillo del dorado metálico |
| `--marfil` | `#ece6da` | texto principal (nunca blanco puro) |
| `--gris` | `#8b8b93` | etiquetas secundarias |
| `--rojo` | `#a33a32` | solo "contra" y "rechazo" |

El oro metálico (degradado en el texto) es **solo para la palabra clave** de cada escena: un
nombre, una cifra o "JAMES BOND". Todo lo demás va en marfil.

## Tipografía

El logo 007 no es una fuente: es un diseño propio (Joe Caroff, 1962) y marca registrada. No se usa ni se imita.

| Rol | Fuente | Estilo |
|---|---|---|
| Títulos, nombres | **Jost** (geométrica tipo Futura) | MAYÚSCULAS; peso 300 + 600 combinados; tracking amplio .08–.16em |
| Citas, preguntas | **Cormorant Garamond** itálica | sentence case, 58–96 px |
| Datos, etiquetas, cifras | **JetBrains Mono** | etiquetas con tracking .3–.5em; cifras tabulares |

Archivos en `_motion/shared/fonts/` (Jost.ttf, CormorantGaramond*.ttf, JetBrainsMono.ttf).

## Motivos

- **Anillos finos** concéntricos (oro al 55 % + línea): aluden a la mira sin copiar el *gun barrel*.
- **Regla dorada** horizontal que se desvanece en los extremos: separa título y subtítulo.
- **Letterbox** (barras negras de 64 px) en hook y citas: el momento "de cine".
- **Grano** fino al 10 % y **viñeta** en todos los frames.
- **Ficha "Expediente NN / 06"** por actor: foto o clip en blanco y negro con marco dorado;
  películas · era · edad al debutar; ＋ pro en oro y － contra en rojo; barra de "recepción al anuncio".

## Fotos y clips

- **Short:** solo imágenes (fotos y pósters), sin clips.
- **Largo:** dos usos de video.
  - **Escenas con sonido**, una o dos por Bond, de 4–8 s: la frase o el momento icónico ("Bond, James Bond", "This never happened to the other fellow", el auto invisible, "Do I look like I give a damn").
    - La voz del narrador se calla durante la escena y la música baja a -18 dB.
    - La escena entra a pantalla completa por iris desde el anillo y sale con un fundido a negro de 0.3 s.
  - **B-roll mudo** de 2–3 s dentro del marco de la ficha mientras habla el narrador.
- Las fotos dentro de la ficha van en **blanco y negro** con contraste +10 %. Las **escenas con sonido van a color**: son "la película" y contrastan con el expediente.
- Sin clip disponible, se usa la foto con Ken Burns lento (escala 1.00→1.06).
- Pattinson aparece a color en el cierre: "el nuevo".
- ⚠ **Derechos:** las escenas con audio original pueden recibir reclamos de Content ID (los ingresos van al dueño o el video se bloquea en algunos países).
  - Mantén cada escena corta (≤8 s), con comentario antes y después, y no más de ~60 s de escenas en total.
  - Revisa los reclamos en YouTube Studio antes de publicar en público.

## Movimiento: dinámico, no de circo

Referencia en movimiento: `_estilo/motion-test.mp4` (13 s, proyecto en `_estilo/motion-test/`).

### Que no parezca slides

1. **El mundo nunca se detiene.** Al fondo, los anillos giran a 2–4°/s, la bruma dorada deriva y la cámara hace un paneo lateral de ±30 px por escena.
   El fondo vive; el texto, en cambio, una vez que aterriza, queda **quieto**.
2. **Algo nuevo cada 1.5–3 s.** Un elemento que entra, un dato que cuenta o un barrido de luz.
   Nunca hay más de ~3 s de pantalla sin un cambio, aunque la escena dure 6 s.
3. **La pantalla se arma con la voz.** Cada dato aparece cuando el narrador lo nombra, no todo de golpe.
   La ficha del actor se construye por partes: foto → nombre → cifras → ＋ → － → barra.
4. **Las escenas se conectan por un objeto.** Nunca hay un corte seco de fondo a fondo.
   - El anillo se abre en iris hacia la siguiente escena.
   - La ficha sale en látigo y la siguiente entra a la misma velocidad.
   - La foto se agranda hasta volverse fondo.
5. **La foto o el clip se mueve dentro del marco** (Ken Burns 1.00→1.07 con deriva), el título no.

### Que no sea circo

- **Máximo 2 movimientos protagonistas a la vez**, más el fondo.
- **Prohibido:**
  - rebotes, sacudidas, giros de texto y zoom-punch;
  - glitch, destellos de color y emojis;
  - el mismo efecto de entrada en todo;
  - títulos que "respiran" o flotan.
- **Curvas:** las entradas usan `expo.out` (0.6–0.9 s) y las salidas `power3.in`, 40–50 % más cortas. Las cámaras usan `power2.inOut`.
- **Varía las entradas dentro del mismo video:**
  - palabra por palabra con desenfoque (8→0 px, 0.2 s, 0.08–0.09 s entre palabras);
  - barrido dorado de izquierda a derecha con el tracking cerrándose (.34em→.16em);
  - letra por letra solo en etiquetas mono;
  - cifras que cuentan hacia arriba (0.8 s).
- **Oro:** un barrido de luz cruza la palabra dorada **una vez** (1.2 s) al aparecer. Nunca en bucle.

### Ritmo

- **Largo:** una escena de 3–6 s, con 2–3 cambios internos.
- **Short:** cortes cada ≤1.5 s. Corta rápido, pero cada elemento sigue entrando suave.
- Antes de cada revelación (una cifra o "¿y qué pasó?") se sostiene 0.3–0.7 s y luego entra el dato.

### Legibilidad

Ningún texto mide menos de **28 px** en 1080p, porque la mayoría lo ve en el teléfono.
Las etiquetas mono van a 28 px con tracking .24–.42em.

## Sonido

- Cama musical de espionaje **genérica** (ACE-Step): cuerdas graves, guitarra *twang*, metales sordos. **Nunca** el tema de Bond.
- SFX discretos: un *whoosh* suave en el iris, un *tick* en los datos y un golpe grave en las revelaciones.
