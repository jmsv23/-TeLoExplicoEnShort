# Guion y escenas: reglas del canal

Las reglas editoriales (hook en 3-5 s, bucles abiertos, sellos, contador, pregunta a mitad, Short → largo) están en `base/canal/LINEA-EDITORIAL.md`. Aquí está **cómo se escribe** para que el motor lo produzca.

## Duración y extensión

| Pieza | Duración | Palabras de voz | Ritmo visual |
|---|---|---|---|
| Short | 20-35 s (máximo 45) | 55-95 | cambio de plano cada ≤ 1-1.5 s |
| Largo | 6-15 min | ~140 por minuto (menos si hay escenas con sonido) | escena de 3-6 s con 2-3 cambios internos |

`./tl estado <video>` cuenta las palabras de cada guion.

## Shorts: pasar el primer filtro de YouTube

YouTube enseña cada Short a un primer grupo de gente y solo lo empuja si ese grupo se queda, lo repite y lo comparte. Hasta el 20 de noviembre de 2026, los 46 Shorts del canal se quedaron en ese primer grupo: una mediana de 1,201 vistas, cualquiera que fuera el tema o la hora. Las señales fueron:

- solo el 46 % de las vistas eran con permanencia;
- la retención al 10 % del video estaba en 0.2-0.5 contra Shorts parecidos;
- entre el 9 y el 35 % llegaba al final;
- hubo 20 compartidos en 50,000 vistas.

Las reglas salen de ese diagnóstico.

1. **Una sola idea por Short**, no una lista de 6 datos. Si el tema da para varias ideas, haz varios Shorts o un largo.
2. **El segundo 0 ya es el gancho.** La voz arranca en el primer fotograma con la promesa concreta («Rockstar escondió ESTO en GTA 6»), no con el tema («Tráiler final»). El texto en pantalla repite la promesa en grande. Prohibido abrir con un plano fijo u oscuro: algo se mueve o cambia antes de 1 s.
3. **Imagen real y personas.** Usa clips en movimiento, caras y momentos humanos reconocibles. El Short que más jaló fue un streamer real borrando GTA 6 (2,576 vistas). Las fotos fijas con zoom son lo último que se usa.
4. **El final regresa al inicio.** La última frase se conecta con la primera para que el Short se repita, sin despedida. **Prohibido cerrar con «en el video completo, en mi canal»**: avisa que ya terminó y la gente desliza. El largo se enlaza con «Video relacionado» y en el comentario fijado (`base/publicacion/REGLAS.md`), no con la voz.
5. **Pregunta de debate a la mitad** o una opinión polémica. Los comentarios y compartidos son la señal que falta. El Top 5 de actrices, que tenía pregunta, sacó 4.4 % de likes y 7 comentarios.
6. **Revisa los primeros 3 s a 1 fps** (`./tl hoja`) antes de dar el Short por bueno. Si los 3 primeros fotogramas son casi iguales, rehaz el gancho.

## guion/<pieza>.md

```markdown
---
pieza: short-01
direccion: "Narrador de cine para redes, con energía y aplomo: gancho seco, ritmo rápido, remates con intención."
---

## short · Short
Tenemos nuevo James Bond, y medio internet ya lo odia.
Robert Pattinson. Edward de Crepúsculo. Batman. Y ahora, cero cero siete.
[clip: craig-shaken]
```

- `## <id> · <título>` abre una **sección**.
  - El id (minúsculas, guiones) amarra las escenas: `def <id>(S)` en `escenas/<pieza>.py`, con `-` → `_`.
  - En el largo, la última sección se llama `cierre`. La música de cierre se ancla ahí.
- **Una línea = un bloque de voz.** Cada bloque se genera y se alinea por separado. Usa 1-3 frases y menos de 800 caracteres.
- `[clip: <id>]` mete una escena con sonido original (`assets/video/cortes/<id>.mp4`). El narrador calla mientras suena.
- `direccion` es la instrucción de actuación para el TTS (tono, energía, ritmo). Va una por pieza.
- `> nota` y `<!-- -->` son comentarios y no se leen.

## Escribir para TTS

- **Números y siglas en palabras**, como se dicen: «cero cero siete», «mil novecientos noventa y siete», «ge te a seis».
- **Nombres propios:** si el TTS los dice mal, agrégalos a `video.json → "pronunciacion": [["Villeneuve", "Vilnév"]]`. Si el nombre volverá a salir en el canal, súbelo a `base/pronunciacion.json`. El texto en pantalla y la alineación siguen usando la forma original.
- **Frases cortas.** El remate va al final de la línea.
- **Signos de interrogación y exclamación** completos: el TTS los entona.

## escenas/<pieza>.py

La dirección visual. Hay una función por sección, y cada plano entra cuando la voz dice su frase:

```python
def short(S):
    w = S.w                     # w("frase") → segundo real en que la voz la dice (alineación de WhisperX)
    S.add("foto", w("Tenemos nuevo"), "corte", img="pattinson-007-primera-imagen", kick="OFICIAL · 16 NOV 2026",
          l1="TENEMOS NUEVO", l2="JAMES BOND", t1=w("Tenemos nuevo"), t2=w("James Bond"))
    S.add("dato", w("A Roger Moore"), "latigo", img="moore-silla-007", num="45", label="años al debutar", tn=w("cuarenta y cinco"))
```

- `S.add(tipo, t, entrada, **params)`:
  - `tipo` es un plano del estilo.
  - `entrada` es una transición del estilo (`TRANS`).
  - Los params son del plano.
- `S.w(frase, n=1, after=None, end=False)` busca la n-ésima aparición de la frase; `end=True` devuelve su fin. Acepta la forma original o la de TTS.
- `img=` y `video=` son ids de `assets/manifest.json`. `S.add("clip", …, clip="<id>")` es la escena con sonido del guion.
- Los shorts de una serie pueden compartir `escenas/shorts.py` (una función por sección) e importar datos del largo con `from largo import X`.
- **Catálogo de planos del estilo:** `./tl planos <estilo>`, con sus params y transiciones.
- Primero `./tl build`, después `./tl render --draft`. Revisa siempre a 1 fps (`./tl hoja`).
