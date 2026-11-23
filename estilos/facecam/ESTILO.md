---
nombre: Facecam Leonida
voz: narrador-comics
ejemplo: 2026-11-mejores-momentos-gta6
---

# Estilo «Facecam Leonida»

**Cuándo usarlo:** recopilaciones de momentos de streamers o clips de gameplay con sonido original (top N momentos). Familia visual de leonida, pero el protagonista es el clip: panel con subtítulos que tapan los quemados y rótulo «#N · STREAMER».

**Video de referencia:** `videos/2026-11-mejores-momentos-gta6/`. Su render publicado es el preview del estilo.

Planos, entradas y SFX: `./tl planos facecam`. Los parámetros de cada plano están en la función `r_<tipo>` de `estilo.py`.
Miniaturas: `miniatura.css` (skin de los layouts `hero`, `versus` y `portada`).

## Estética

- **Fondo:** cielo de atardecer de Leonida (morado `#1a0b2e` → magenta → naranja) con grano en overlay al 5 %.
- **Tipografía:**
  - Pricedown con contorno negro grueso para los títulos;
  - Anton para las etiquetas (fondo rosa `#ff2f7f`);
  - Pacifico para los acentos;
  - Press Start 2P para lo retro.
- **Paneles tipo carátula de GTA:** borde negro grueso con filo blanco y un leve giro.
- **Acentos:** rosa, naranja y cian. Las fotos van a color, con +4 % de contraste y +8 % de saturación.
- **Entradas:** panel, látigo, crece, iris y flash (destello blanco con golpe).
- **SFX:** whoosh, golpe, obturador, papel y lápiz.

## Propio de facecam

- `clip`: en 16:9 el momento sale de un panel girado y llena la pantalla; en 9:16 es un panel 4:3 sobre el cielo.
  - Params: `tag` (#N · STREAMER, fijo todo el clip), `subs=[(ini, fin, texto)]` y `titulo` (9:16, arriba).
- Los subtítulos van en una tarjeta oscura que **tapa los subtítulos quemados** de la fuente.
- Los clips se citan con el canal de origen en la descripción (créditos en `investigacion/sources.csv`).
