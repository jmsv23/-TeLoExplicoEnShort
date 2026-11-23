---
name: montaje
description: Genera la voz (Voicebox), la música y el render de las piezas de un video y los revisa a 1 fps hasta que se ven bien. Úsala para generar o regenerar voz, música o renders, o para corregir algo que se ve mal en un video.
---

# Montaje: voz → música → render → revisión

Todo con `./tl` (`./tl <cmd> -h`). La pieza se omite para hacer todas, o se elige con `largo`, `short-01` o `shorts`.

## 1. Voz

`./tl voz <video> [pieza]` genera el audio por bloque, lo alinea con WhisperX y arma `master.wav` y el timeline.
- La voz sale de la cadena video.json → estilo → `config.json` (`narrador-comics`). Si Voicebox no tiene el perfil: `./tl voces restaurar <slug>`.
- Escucha el arranque de cada pieza y los nombres propios. Si un nombre suena mal, agrégalo a `pronunciacion` en video.json y corre `./tl voz <video> <pieza>`: solo se regeneran los bloques que cambiaron.
- El aviso «revisar: X (N sin avance)» significa que la alineación se perdió en ese bloque. Regenera ese bloque (cambia una coma, o `--force`).

## 2. Música

Se configura en `video.json → "musica"`: tema, fondo y cues (claves en `motor/mezcla.py`).
- Reusa una pista de `audio-lib/musica/` si encaja con el estilo (`PROMPTS.md`).
- Si no hay una que encaje, genera 1 pista con la skill `music-generate`, guárdala en `audio-lib/musica/<estilo>-<nombre>.wav` y anota el prompt en `PROMPTS.md`. Genera opciones A/B/C solo si el usuario las pide.
- Siempre es música original y genérica, nunca el tema de una franquicia.

## 3. Render y revisión

1. `./tl render <video> <pieza> --draft`.
2. `./tl hoja <video> <pieza>` y **mira la hoja** (`build/revision/<pieza>.jpg`, 1 fps). Revisa:
   - el texto se lee y nada mide menos de 28 px;
   - nada queda tapado ni cortado;
   - cada plano entra cuando la voz lo dice;
   - no hay pantallas vacías ni negras de más de 1 s;
   - hay un cambio cada 1.5-3 s;
   - los sellos aparecen donde el guion afirma algo;
   - el contador es correcto;
   - las caras están bien encuadradas (`pos=`).
3. Corrige en `escenas/<pieza>.py` (o el asset) y repite.
4. Escucha un tramo de la mezcla: la voz por encima de la música, sin saltos de volumen en los clips.
5. Si cambiaste el guion, vuelve a correr la voz antes del render.

Se completa cuando la hoja a 1 fps de cada pieza pasa toda la lista del paso 2. Después: `estado.voz` y `estado.montaje`.

Un largo que se cae o tarda demasiado se renderiza por partes: `"partes": 3` en su pieza de video.json.
