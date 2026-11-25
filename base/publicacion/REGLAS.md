# Publicación: títulos, descripción, tags y miniaturas

Esta es la base del canal. Cada video llena `entrega/PUBLICACION.md` a partir de `PUBLICACION.template.md`. Si el video necesita algo distinto (otro tono de título, un CTA especial, otra playlist), lo escribe en `publicacion.override.md` en la raíz del video. Lo que diga el override gana sobre estas reglas.

## Datos antes de escribir

1. **Búsquedas reales:** autocompletado de YouTube con la skill `youtube-trends`. Anota en PUBLICACION.md la fecha y las frases que usaste.
2. **Datos del canal:** con la skill `channel-insights`, revisa qué títulos y miniaturas retuvieron mejor y qué búsquedas traen vistas.
3. **Ventana:** el estreno o la noticia que hace urgente el video, y la fecha límite para publicarlo.

## Títulos

- Lleva la búsqueda principal al inicio, en el orden en que la gente la teclea.
- Usa una palabra en MAYÚSCULAS como gancho (NUEVO, MÁS, TODOS). No más de una.
- Hay dos patrones que funcionan en el canal:
  - **afirmación + giro:** «El NUEVO James Bond es Robert Pattinson… y ya odiaron a todos los 007»;
  - **pregunta + promesa:** «¿Robert Pattinson será el MEJOR James Bond? Así recibieron a los otros 6».
- 60-70 caracteres como máximo.
- Si es un rumor, el título lo dice («filtración», «teoría», «¿será…?»). Nunca lo afirma.
- **Largo:** 2 títulos para la prueba A/B (YouTube Studio → «Probar y comparar») más 1 de respaldo.
- **Short:** el título con 1 emoji y `#shorts`.

## Descripción del largo

1. Dos líneas de gancho con las búsquedas principales escritas de forma natural.
2. 👇 La pregunta de debate (la misma del video) y «Te leo en los comentarios».
3. Capítulos con los tiempos reales del render. Salen de `build/timeline-largo.json`: el inicio de cada sección y su título del guion.
4. Datos y fuentes: cada dato clave con su fuente y fecha. Si hay fragmentos de películas o juegos, agrega: «Fragmentos usados con fines de comentario y análisis».
5. Exactamente 3 hashtags.

## Tags

De 15 a 25, sacados del autocompletado: búsqueda principal, variantes, nombres propios y títulos relacionados. Sin repetir el título palabra por palabra.

## Comentario fijado

La pregunta de debate en otra versión, con una opción polémica («¿será Craig… o será Lazenby?»).

## Short

- **Portada:** `portada-short-NN.png`. Se sube como miniatura; en móvil se elige el fotograma más parecido.
- **Descripción:** 1-2 líneas, la pregunta y 3 hashtags.
- **Video relacionado:** siempre el largo del mismo tema. Si es una serie sin largo, el Short siguiente o anterior de la serie. Es el único puente al largo, porque la voz ya no lo menciona.
- **Comentario fijado:** la pregunta de debate y el enlace al largo.
- **Ritmo de publicación:** de 1 a 3 Shorts al día, con al menos 3 h entre uno y otro. Nunca en ráfaga: los 9-10 Shorts que se subieron en una misma hora en noviembre de 2026 compitieron entre ellos por el primer grupo de espectadores.
- **Qué medir:** en Studio, «Se vio vs. se deslizó» de cada Short (la API no lo da). Como referencia de la comunidad, a partir de ~70 % YouTube suele empezar a empujarlo. Compáralo contra los Shorts anteriores.

## Miniaturas

- Reglas visuales: `MINIATURAS.md`.
- La miniatura **complementa** al título, nunca lo repite: una plantea la duda y el otro la refuerza.

## Cómo leer la prueba A/B

Deja correr la prueba hasta que YouTube declare ganador (de días a dos semanas). Gana la variante con más **tiempo de visualización por impresión**, no la de más clics.
