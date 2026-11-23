---
nombre: Portada
voz: narrador-comics
ejemplo: 2026-11-top-5-actrices-marvel
---

# Estilo «Portada»

**Cuándo usarlo:** rankings de personas (actrices, actores, looks, alfombra roja), temas de moda y celebridades. Revista editorial y luminosa: papel claro, rojo de acento, Fraunces.

**Video de referencia:** `videos/2026-11-top-5-actrices-marvel/`. Su render publicado es el preview del estilo.

Planos, entradas y SFX: `./tl planos portada`. Los parámetros de cada plano están en la función `r_<tipo>` de `estilo.py`.
Miniaturas: `miniatura.css` (skin de los layouts `hero`, `versus` y `portada`).

---

## Ficha original (de top-5-actrices-marvel-mas-guapas/_estilo.md)

> Las rutas de esta ficha (_motion/, _estilo/) son de content-creator/explicando. Las fuentes ya están en fonts/.


Revista de moda y alfombra roja. Cada actriz recibe su **portada**: una foto grande a color, el número del ranking enorme y los "cover lines" de una revista.
Se ve **editorial y luminoso**, al revés del Bond (negro y oro) y de Camino a Doomsday (cómic).
- **No es cómic:** nada de semitonos, viñetas ni onomatopeyas.
- **No es noche ni neón.**

Referencia en movimiento: `_estilo/board.html` y `_estilo/motion-test/` (por hacer al pasar a producción).

## Voz

**"narrador comics"** (Voicebox), igual que Bond. Solo la voz: el estilo visual no es de cómic.

## Paleta (tokens)

| Token | Hex | Uso |
|---|---|---|
| `--papel` | `#f2ebe0` | fondo base (papel couché cálido, con grano fino) |
| `--papel-2` | `#e6dccb` | paneles y sombras del papel |
| `--tinta` | `#151214` | texto principal y el "negro de revista" |
| `--rojo` | `#c8102e` | **acento único**: el número del ranking, las reglas y el círculo de lápiz graso |
| `--champan` | `#b89a6a` | etiquetas finas y filetes secundarios |
| `--gris` | `#7a7470` | pies de foto y créditos |
| `--flash` | `#fffaf2` | solo el flash de cámara (nunca blanco puro de fondo) |

El rojo va en **una sola cosa por pantalla**: el número, o la palabra clave, o el círculo. Nunca en las tres a la vez.

## Tipografía (archivos en `_motion/shared/fonts/`)

| Rol | Fuente | Estilo |
|---|---|---|
| Cabecera de revista, nombres | **Fraunces** (opsz alto, peso 800–900) | MAYÚSCULAS con tracking cerrado (-.01em); el contraste alto la acerca a una Didone de revista |
| Número del ranking | **Fraunces** itálica 900 | "Nº" pequeño + cifra gigante (600–900 px en 16:9), en rojo |
| Frases y citas | **Cormorant Garamond** itálica | sentence case, 60–96 px |
| Etiquetas, cover lines y datos | **Jost** | MAYÚSCULAS, peso 500, tracking .18–.3em |
| Cifras (taquilla, años) | **Jost** 600, cifras tabulares | cuentan hacia arriba |

No uses JetBrains Mono: es del Bond. Ningún texto mide menos de **28 px** en 1080p.

## Motivos

- **Portada por actriz** ("Nº 05" … "Nº 01"):
  - foto a color de alfombra roja o de personaje a sangre;
  - cabecera "TOP 5 MARVEL" arriba;
  - número rojo gigante detrás del recorte de la actriz, si la foto lo permite, o al costado;
  - 2 o 3 cover lines (papel, primera aparición, dato).
- **Hoja de contactos:** una tira de 4 o 6 fotos de película con números de cuadro. Un **círculo de lápiz graso rojo** se dibuja (stroke-dashoffset) alrededor de la elegida. Es el motivo para "su look icónico".
- **Flash de cámara:** un destello cálido (`--flash`, 0.12 s, sube y baja) **solo** al revelar cada número del ranking. Es el único "destello" permitido. Va con un SFX de obturador.
- **Pase de página:** transición entre actrices. La portada se dobla por la esquina (efecto 2D con sombra) y deja ver la siguiente.
- **Regla roja fina** bajo los títulos, y **marco blanco con sombra suave** (foto impresa) para las fotos dentro de la página.
- **Grano** de papel al 6 % en todo. Sin viñeta oscura: el fondo es claro.

## Fotos y clips

- **Fotos a color siempre.** Sin blanco y negro: esto es alfombra roja.
  - Corrección suave: un poco de calidez (+3) y contraste +5 %. Nada de filtros de piel ni retoque.
- **Short:** solo imágenes (portadas, alfombra roja, fotos de personaje).
- **Largo:**
  - **Escenas con sonido**, 1 o 2 por actriz, de 4–8 s (≤60 s en total).
    - Entran como **foto impresa que crece hasta llenar la pantalla** y salen con un pase de página.
    - El narrador se calla y la música baja a -18 dB.
  - **B-roll mudo** de 2–3 s dentro del marco blanco mientras habla el narrador.
- Sin clip disponible: la foto con Ken Burns lento (1.00→1.06).
- ⚠ **Derechos:** igual que en Bond. Escenas cortas, con comentario antes y después, y revisión de Content ID en Studio antes de publicar.

## Movimiento: dinámico, no de circo (mismas leyes que Bond)

1. **El mundo nunca se detiene.**
   - El papel tiene una deriva lenta de luz, como una ventana que pasa.
   - La cámara hace un paneo de ±30 px.
   - La foto lleva Ken Burns.
   - El texto, una vez que aterriza, queda quieto.
2. **Algo nuevo cada 1.5–3 s** en el largo, y cada ≤1.5 s en el Short.
3. **La pantalla se arma con la voz:** foto → número → nombre → cover lines → dato.
4. **Las escenas se conectan por un objeto:** pase de página, foto que crece hasta volverse fondo, o el círculo rojo que se abre en iris.
5. **Máximo 2 movimientos protagonistas a la vez.**

**Prohibido:** rebotes, sacudidas, glitch, zoom-punch, emojis, corazones, brillos "sparkle", y el mismo efecto de entrada en todo.

**Curvas:**
- entradas `expo.out` (0.6–0.9 s); salidas `power3.in`, 40–50 % más cortas;
- cámaras `power2.inOut`;
- el número del ranking entra con `expo.out` 0.8 s desde escala 1.08, tras el flash.

**Entradas de texto** (varía entre ellas):
- nombre en Fraunces con barrido de máscara de abajo hacia arriba;
- cover lines palabra por palabra con desenfoque (8→0 px);
- cifras que cuentan hacia arriba;
- citas en Cormorant que aparecen por línea.

## Sonido

- **Música:** pop elegante de pasarela y fashion show (bajo con pulso, sintes cálidos, sin voz), estilo *runway*. Generada con ACE-Step; se proponen 2 o 3 opciones y el usuario elige.
- **SFX discretos:** el obturador en cada flash, un *swish* de papel en el pase de página y un "tick" de lápiz al cerrar el círculo rojo.
