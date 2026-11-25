---
name: guion
description: Escribe o reescribe guion/<pieza>.md (lo que dice la voz) y escenas/<pieza>.py (la dirección visual en el estilo del video). Úsala para escribir guiones, cambiar el hook o el texto de una pieza, o rehacer las escenas.
---

# Guion y escenas

Lee primero `base/guion/REGLAS.md` (formato, TTS, duraciones) y `base/canal/LINEA-EDITORIAL.md`. El contenido sale de `brief.md` y de `investigacion/fuentes.md`.

## 1. Guion: guion/<pieza>.md

- Tesis en los primeros 3-5 s. Sin saludo.
- 1-2 bucles abiertos que se cierran al final.
- En el largo, formato lista o «N / N» cuando el tema lo permite, con el contador en pantalla. El Short lleva una sola idea.
- Pregunta de debate a mitad del video, la misma que irá al comentario fijado.
- Cada dato con su sello tal cual está en `fuentes.md`. TEORÍA y FILTRACIÓN se dicen como tales («según el insider X…», «la teoría más fuerte es…»).
- Short: sigue la sección «Shorts: pasar el primer filtro» de `REGLAS.md`: una idea, gancho desde el segundo 0, imagen real y un final que regresa al inicio. **Nunca** cierres con «en el video completo, en mi canal»: el largo se enlaza al publicar. Largo: cierra con el siguiente video de la serie o con la pregunta.
- Escenas con sonido (`[clip: id]`): de 4 a 8 s cada una y ≤ 60 s en total por largo. Se presentan antes y se comentan después.
- `direccion` en el frontmatter, ajustada al tono de la pieza.

Mide con `./tl estado <video>`: las palabras deben quedar en el rango de duración de `REGLAS.md`.

Se completa cuando cada pieza del video tiene su guion dentro del rango de palabras y cada dato del guion está en `fuentes.md` con el mismo sello.

## 2. Escenas: escenas/<pieza>.py

Se escriben **después** de tener los assets (skill `assets`), porque usan sus ids.

**Estilos con motor propio** (`comic`): las escenas son `escenas/<pieza>/<sección>.py` con `def build(S)` y la API de escenas del estilo, no `S.add`. Sigue su `ESTILO.md`, `./tl planos comic` y las escenas de su video de referencia (largo y short). El resto del flujo es igual.

1. Mira el catálogo del estilo con `./tl planos <estilo>`. Los parámetros de cada plano están en `estilos/<estilo>/estilo.py` (`r_<tipo>`).
2. Lee las escenas del video de referencia del estilo (`ESTILO.md → ejemplo`). Son el modelo de ritmo y de uso de los planos.
3. Escribe una función por sección del guion. Cada plano entra con `S.w("frase")`, en el momento en que la voz lo dice.
   - Cambia algo cada 1.5-3 s en el largo, y cada 1-1.5 s en el Short. El primer plano del Short entra en el segundo 0 y se mueve.
   - Varía las entradas.
   - Cada sello del guion lleva su sello en pantalla.
   - En formato lista, el contador se ve.
4. `./tl build <video> <pieza>` señala frases que no se encuentran y planos inexistentes. Corrige hasta que construya.

Se completa cuando `./tl build` termina sin error en cada pieza. La revisión visual es de la skill `montaje`.
