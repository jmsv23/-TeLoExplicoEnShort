---
name: investigar
description: Investiga un tema del canal y escribe investigacion/fuentes.md (datos con sello CONFIRMADO/TEORÍA/FILTRACIÓN/LECTURA) y brief.md. Úsala para investigar o validar la demanda de un tema, o para rehacer el brief de un video.
---

# Investigar y escribir el brief

Reglas del canal: `base/canal/LINEA-EDITORIAL.md`. Plantillas: `base/plantillas/fuentes.md` y `base/plantillas/brief.md`. `./tl nuevo` ya las copió al video.

## 1. Hechos

Si el tema salió del radar (`research/radar/<fecha>/reporte.json`), arranca de su `evidencia` y su `clasificacion`: el sello ya está asignado. Lo que falta es completar y cruzar las cifras.


- Busca con la skill `bx` (web + news). Para la noticia más reciente usa `news-search` con filtro de frescura.
- Prioridad de fuentes: oficial (estudio, editorial, desarrolladora, tráiler, comunicado) → medios serios (Variety, THR, Deadline, IGN, Polygon) → insiders con historial (marcar FILTRACIÓN) → fans y foros (marcar TEORÍA).
- Cada dato va a la tabla de `investigacion/fuentes.md` con su **sello**, URL y fecha. Un dato sin fuente no entra.
- Las cifras (taquilla, ventas, fechas) se cruzan con dos fuentes. Si no coinciden, anota las dos.
- Llena «Qué NO sabemos todavía»: de ahí sale el material honesto para TEORÍA y para los bucles abiertos.

Se completa cuando cada afirmación que usará el guion está en la tabla con sello y URL.

## 2. Demanda y ángulo

- Skill `youtube-trends` sobre el tema: autocompletado y tendencias. Ahí salen el ángulo y las palabras del título.
- Skill `channel-insights`: qué videos del canal retienen y qué búsquedas traen vistas. Úsalo para elegir entre ángulos.
- Revisa los 3-5 videos más vistos del tema en YouTube (skill `videos-search`): qué prometen y qué les falta. Ese hueco es nuestro ángulo.

## 3. Brief

Llena `brief.md`:
- **ángulo:** la tesis en una frase;
- **hook:** la frase de los primeros 3-5 s;
- **bucles abiertos;**
- **estructura del largo:** con la pregunta de debate a mitad y el cierre hacia el siguiente video;
- **ángulo propio de cada short:** cada uno es independiente y lleva al largo;
- **datos clave con sello;**
- **visual:** qué imágenes y clips harán falta;
- **demanda:** la evidencia.

Si el formato es serie, cada short necesita un gancho que se sostenga solo; si no hay suficientes, propón menos shorts.

Se completa cuando cada sección de la plantilla está llena con contenido de este tema.
