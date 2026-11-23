---
name: nuevo-estilo
description: Agrega un estilo visual reusable a la galería (estilos/) a partir de referencias (videos, imágenes, capturas o un video viejo del canal) más una entrevista corta con el usuario. Entra al INDEX solo si su preview se aprueba. Úsala cuando pidan crear o agregar un estilo, o «hazlo como esta referencia».
---

# Nuevo estilo

Un estilo es un plugin del motor más su ficha. El contrato está en `estilos/CONTRATO.md` y la galería en `estilos/INDEX.md`.

## 1. Analizar las referencias

- **Video:** skill `gemini-video-map` para el mapa de planos, y hojas de contacto a 1 fps (`./tl assets hoja` sirve con cualquier mp4) para mirar los frames clave.
- **Imágenes y capturas:** léelas directamente.
- **Un video viejo del canal:** su `escenas/` y el `ESTILO.md` de su estilo.

Saca y anota en `estilos/<slug>/_trabajo/analisis.md`:
- paleta con hex;
- tipografía: rol → fuente libre equivalente (Google Fonts), nunca la fuente registrada de una marca;
- composición y recursos gráficos (marcos, texturas, grano, viñetas);
- ritmo de cortes (s por plano);
- transiciones;
- tratamiento de foto y video (color, B/N, contraste);
- sonido (tipo de música y SFX).

Se completa cuando cada punto tiene un valor concreto sacado de las referencias, o un «no se ve» explícito.

## 2. Ficha propuesta y entrevista

Presenta la ficha en el chat: paleta, tipografía, motivos, movimiento, sonido y temas para los que sirve. Después entrevista al usuario con `AskUserQuestion`, en 1-2 rondas y 5-8 preguntas en total, cada una con una recomendación:
1. ¿Para qué temas se usa? ¿Qué lo distingue de los estilos que ya hay?
2. Intensidad del movimiento: sobrio / dinámico / frenético.
3. ¿Qué evitar? (recursos de la referencia que no quiere)
4. ¿Fotos a color o B/N? ¿Clips a pantalla completa o en marco?
5. Voz: `narrador-comics`, `explicando-mejorado` u otra (`./tl voces listar`).
6. Música: el tipo y si se reusa alguna de `audio-lib/musica/PROMPTS.md`.
7. Nombre y slug.

Se completa cuando cada pregunta tiene respuesta del usuario y la ficha queda ajustada a esas respuestas.

## 3. Construir

1. **Parte del estilo existente más parecido.** Copia `estilos/<base>/estilo.py` y `miniatura.css`. Ya traen un motor probado de planos, transiciones y SFX.
   - Reescribe los tokens del CSS, las fuentes (a `fonts/`), el tratamiento de imagen (`IMG_VF`, `BN_DEFAULT`), `INDEX_BG`/`GRANO_CSS` y las transiciones.
   - Ajusta los planos: borra los que no aplican, cambia su HTML y CSS a la nueva estética y agrega los propios del estilo.
   - Cada `r_<tipo>` lleva un docstring de una línea con sus params. Eso es lo que muestra `./tl planos`.
2. `ESTILO.md`: frontmatter (`nombre`, `voz`, `ejemplo`), cuándo usarlo y la ficha completa (paleta, tipografía, motivos, movimiento, fotos/clips, sonido).
3. `miniatura.css`: la skin de los layouts `hero`, `versus` y `portada` con la nueva estética.
4. `preview/`:
   - `guion.md`: 2-4 líneas de prueba sobre un tema del canal, con un dato sellado.
   - `escenas.py`: usa 4-6 planos distintos y al menos 2 entradas.
   - `img/`: 3-5 imágenes libres o del canal.
   - `vertical`: archivo vacío si el estilo es sobre todo para shorts.

Se completa cuando `./tl planos <slug>` lista cada plano con su docstring y `./tl preview <slug>` renderiza sin errores.

## 4. Gate: preview aprobado

1. `./tl preview <slug>`. Mira la hoja (`estilos/<slug>/_trabajo/hoja.jpg`) y corrige hasta que cumpla las reglas de `CONTRATO.md` y la ficha.
2. Renderiza también una miniatura de prueba: puedes usar un video existente cambiando temporalmente `estilo`, o una carpeta `_trabajo` con `miniaturas.json`.
3. Muestra al usuario la ruta de `preview/preview.mp4`, el `preview.jpg` y la miniatura. **Espera su aprobación.** Si pide cambios, repite desde el paso 3.

Al aprobar:
- copia `preview/preview.jpg` a `estilos/<slug>/preview.jpg` y agrega la fila a `estilos/INDEX.md` (slug, nombre, temas, voz, preview);
- borra `_trabajo/`;
- haz commit del estilo si el usuario lo pide.

Se completa cuando el usuario aprobó el preview y el estilo está en el INDEX.
