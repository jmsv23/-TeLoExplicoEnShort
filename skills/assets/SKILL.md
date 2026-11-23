---
name: assets
description: Busca, baja y registra imágenes y clips de un video en assets/manifest.json (búsqueda amplia con bx), corta las escenas y verifica calidad. Úsala para buscar fotos o clips, cortar escenas, reemplazar un asset malo o volver a bajar los assets de un video.
---

# Assets: imágenes y clips

`assets/manifest.json` es la fuente de verdad: en git solo va el manifiesto. Formato: `motor/assets.py`.

## 1. Lista de lo que hace falta

Sale del guion y del brief: por sección, qué imagen o clip necesita cada momento. Para cada plano piensa en la toma ideal (quién, qué gesto, qué época) antes de buscar.

## 2. Imágenes

1. Busca con la skill **`bx`** (búsqueda amplia: imágenes, páginas, wikis, prensa) y complementa con `images-search`. Hay varias consultas por necesidad: nombre + película o año, en inglés y en español, «still», «press photo», «key art», «HD».
2. Prefiere press kits oficiales, wikis de fandom en alta y medios grandes. Tamaño mínimo: 1000 px de ancho (1600+ para fondos a pantalla completa).
3. Si hay varias candidatas, ármate una hoja de contacto y elige mirando, no por el título.
4. Registra cada elegida: `./tl assets agregar-img <video> <id> <url-directa> --pagina <url> --fuente <sitio>`. Baja el archivo, lo pasa a jpg y lo anota con su tamaño.
   - El id va en minúsculas con guiones y dice qué se ve (`pattinson-batman-capucha`).
   - `--pin` si la URL puede desaparecer (CDN con token, redes sociales).

## 3. Clips

1. Busca fuentes con `bx` (videos) y `videos-search`: tráilers oficiales, escenas, gameplay, entrevistas. Agrégalas a `fuentes_video` del manifiesto (`{"id", "url"}`) y bájalas con `./tl assets fetch <video>`.
2. Para encontrar los momentos de una fuente larga usa la skill `gemini-video-map` (un mapa JSON por fuente). Para confirmar los tiempos exactos usa `./tl assets hoja <video> <fuente>` (1 fps).
3. Anota cada corte en `cortes`: `{"id", "fuente", "inicio", "fin", "tipo": "voz"|"broll", "zoom", "nota"}`.
   - `zoom` > 1 recorta hacia arriba para sacar subtítulos quemados; < -1 recorta al centro.
   - Escenas con sonido de 4 a 8 s (≤ 60 s en total).
4. `./tl assets cortar <video> [ids]`.

## 4. Verificar

`./tl assets verificar <video>` debe salir sin «falta» y sin imágenes chicas, salvo las que aceptes a propósito.
- Mira las imágenes de un vistazo: cara correcta, sin marca de agua, sin texto quemado que estorbe.
- Si hay imágenes sin URL directa: `./tl assets respaldar <video>`.

Se completa cuando cada imagen o clip que nombran las escenas existe en el manifiesto y en disco, y `verificar` no muestra problemas sin resolver. Después: `estado.assets = "hecho"`.
