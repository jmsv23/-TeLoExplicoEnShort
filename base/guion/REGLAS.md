# Guion y escenas: reglas del canal

Las reglas editoriales (hook en 3-5 s, bucles abiertos, sellos, contador, pregunta a mitad, Short → largo) están en `base/canal/LINEA-EDITORIAL.md`. Aquí está **cómo se escribe** para que el motor lo produzca.

## Duración y extensión

| Pieza | Duración | Palabras de voz | Ritmo visual |
|---|---|---|---|
| Short | 45-58 s (máximo 60) | 120-150 | cambio de plano cada ≤ 1.5-3 s |
| Largo | 6-15 min | ~140 por minuto (menos si hay escenas con sonido) | escena de 3-6 s con 2-3 cambios internos |

`./tl estado <video>` cuenta las palabras de cada guion.

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
