# @TeLoExplicoEnShort: producción de videos del canal

Canal de YouTube de cultura pop (cómics y superhéroes, cine, videojuegos) en español, con tono explicativo/noticias. Aquí se produce cada video de punta a punta: investigación → brief → guion → assets → voz → montaje → entrega. Todo es para este canal y nada más.

## Cuando te pidan un video

«Crea un video de X», «hagamos un video sobre X» o «un short de X»: invoca la skill **`crear-video`**. Ella pregunta el formato y el estilo, crea la carpeta y lleva el video por las fases con 3 pausas para aprobación.

Para rehacer una sola fase de un video que ya existe, usa su skill directamente:

| Fase | Skill | Ejemplos de pedido |
|---|---|---|
| investigación + brief | `investigar` | «investiga más el ángulo de X», «rehaz el brief» |
| guion + escenas | `guion` | «reescribe el short 2», «cambia el hook» |
| imágenes y clips | `assets` | «busca mejores fotos de Y», «corta otra escena» |
| voz, música, render | `montaje` | «regenera la voz», «renderiza el largo» |
| miniaturas, títulos, descripción, QA | `entrega` | «rehaz la miniatura», «otro título para el short» |
| estilo visual nuevo | `nuevo-estilo` | «agrega un estilo basado en esta referencia» |

## Capas: base → estilo → video

Cada regla vive en **un solo lugar**. Un video solo escribe lo que lo hace distinto.

- **Base del canal** (`base/`)
  - `canal/LINEA-EDITORIAL.md`: nicho, tono y reglas de viralidad.
  - `guion/REGLAS.md`: formato del guion y cómo se escribe para TTS.
  - `publicacion/`: títulos, descripción, tags, miniaturas y plantilla de PUBLICACION.md.
  - `pronunciacion.json`: cómo dice el TTS los nombres propios.
  - `canal/identidad/`: arte activo, 03_sello.
- **Estilo** (`estilos/<slug>/`)
  - La galería está en `estilos/INDEX.md`.
  - Cada estilo es un plugin del motor (`estilo.py`) más su ficha (`ESTILO.md`), su skin de miniaturas (`miniatura.css`) y sus fuentes.
  - El contrato del plugin está en `estilos/CONTRATO.md`.
- **Video** (`videos/AAAA-MM-<slug>/`)
  - `video.json` es la fuente de verdad: formato, estilo, voz, piezas, música, estado de cada fase y URLs.
  - Personalizaciones: `pronunciacion` en video.json, `publicacion.override.md`, layouts y textos de `miniaturas.json`.

Una **pieza** es cada render que sale de un video: `largo` (16:9) o `short-NN` (9:16).

## Motor y CLI

`./tl -h` lista los comandos (`nuevo`, `estado`, `voz`, `build`, `render`, `hoja`, `miniaturas`, `qa`, `entrega`, `publicado`, `limpiar`, `regenerar`, `assets …`, `voces …`), y cada uno acepta `-h`. Su código está en `motor/`.

## Git: solo lo que no se regenera

- **Se versiona:** texto y decisiones (guiones, escenas, brief, investigación, video.json, manifiestos, PUBLICACION.md), estilos, muestras de voz, SFX y prompts de música.
- **Queda fuera** (ver `.gitignore`): `build/`, los archivos de `assets/`, los mp4/png de `entrega/` y la música generada. `./tl regenerar <video>` los reconstruye.
- **Limpieza:** `./tl limpiar --todos-publicados` dice primero cuánto libera, y solo borra con `--si`. Antes de pasar `--si`, confírmalo con el usuario.

## Cosas que no se ven en el código

- **Voicebox** corre en `192.168.0.52:17493` (`config.json`; `VOICEBOX_URL` lo sobreescribe).
  - Si falta un perfil: `./tl voces restaurar <slug>`.
  - Si cambias de proveedor de TTS, `voces/<slug>/` tiene la muestra original y su texto.
- **HyperFrames** desde la terminal del agente: `rtk proxy npx hyperframes …`, porque rtk rompe el `npx hyperframes` sin proxy. El motor ya lo llama sin rtk.
- **Revisar video a 1 fps como máximo** (`./tl hoja`, `./tl assets hoja`): ahorra tokens. Para mapear fuentes largas usa la skill `gemini-video-map`.
- **Sellos de veracidad:** CONFIRMADO / TEORÍA / FILTRACIÓN / LECTURA. Nunca presentes un rumor como hecho. El sello sale de `investigacion/fuentes.md` y se usa igual en el guion y en pantalla.
- **Origen del proyecto:** los videos de noviembre 2026 se migraron desde `~/projects/personal/content-creator/explicando/`. Esa carpeta es el archivo original: solo se lee, nunca se edita.
