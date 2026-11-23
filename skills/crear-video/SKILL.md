---
name: crear-video
description: Produce un video nuevo del canal de punta a punta (investigación → brief → guion → assets → voz → montaje → entrega) con 3 pausas de aprobación. Úsala cuando pidan «crea/haz un video de X», «un short de X» o «una serie de shorts sobre X».
---

# Crear un video

Coordinas el flujo. Cada fase tiene su skill con el detalle: invócala cuando llegues a ella. `video.json → estado` registra el avance, así que si el video ya existe (`./tl estado`), retómalo desde la primera fase pendiente.

## 0. Arranque: tema, formato y estilo

1. Haz una investigación rápida del tema (10-15 min de búsqueda; skill `investigar`, paso 1) para poder proponer.
2. Pregunta con `AskUserQuestion`, todo en una sola ronda:
   - **Formato:**
     - `largo+short`: largo + 1 short (el estándar, va primero como recomendado);
     - `largo+serie`: largo + serie de shorts;
     - `short`: solo un short;
     - `serie`: serie de shorts sin largo.
   - **Estilo:** los 2 de `estilos/INDEX.md` que mejor encajan con el tema, con el porqué. Agrega «otro / crear uno nuevo» (→ skill `nuevo-estilo`).
   - **Número de shorts**, solo en las series: propón 3-6 según cuántos ángulos fuertes salieron.
3. `./tl nuevo <slug> --titulo "…" --formato … --estilo … [--shorts N]`. El slug va en minúsculas con guiones y sin fecha (la fecha la pone el comando).

Se completa cuando existe `videos/AAAA-MM-<slug>/video.json` con el formato y el estilo elegidos.

## 1. Investigación y brief → ⏸ pausa 1

Skill `investigar`. Deja `investigacion/fuentes.md` con los datos sellados y `brief.md`. Presenta el brief en el chat de forma resumida: ángulo, hook, estructura, ángulo de cada short, demanda y datos con sello dudoso.

**Espera la aprobación.** Lo que el usuario cambie se aplica antes de seguir. Después: `estado.investigacion = "hecho"` y `estado.brief = "aprobado"`.

## 2. Guion → ⏸ pausa 2

Skill `guion`. Escribe `guion/<pieza>.md` de cada pieza. Presenta en el chat el guion de cada pieza (en el largo, el hook y la estructura con 1 línea por sección; el texto completo está en el archivo) con su conteo de palabras y la duración estimada.

**Espera la aprobación.** Después: `estado.guion = "aprobado"`.

## 3. Producción (sin pausas)

En este orden. Cada paso tiene su criterio de terminado en su skill:
1. `assets`: imágenes y clips en el manifiesto, bajados, cortados y verificados.
2. `montaje`: escenas por pieza, voz, música, render draft y revisión a 1 fps de cada pieza, corrigiendo hasta que se vea bien.
3. `entrega`, primera parte: miniaturas y PUBLICACION.md.

Las series de shorts largas se pueden repartir a workers de Orca (skill `orchestration`). Tú diriges y validas cada pieza con su hoja a 1 fps.

## 4. Borrador → ⏸ pausa 3

Muestra la hoja a 1 fps de cada pieza y las miniaturas juntas. Da las rutas de los drafts (`build/render/<pieza>-final.draft.mp4`) para que el usuario los vea. Resume lo que falte o lo que no esté seguro.

**Espera la aprobación** o la lista de cambios. Aplica los cambios y vuelve a mostrar solo lo que cambió.

## 5. Final y entrega

1. `./tl render <video>` en calidad final.
2. Skill `entrega`: QA sin errores, `./tl entrega <video>` y `entrega/` completa.

Se completa cuando `entrega/` tiene cada pieza, las miniaturas y PUBLICACION.md, y `./tl qa` termina sin errores.

Cierra con lo siguiente: qué subir y en qué orden, el recordatorio de pasar las URLs (`./tl publicado <video> <pieza> <url>`), y la oferta del resumen en audio.
