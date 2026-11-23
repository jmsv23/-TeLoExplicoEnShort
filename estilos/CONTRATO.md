# Contrato de un estilo (plugin del motor)

Un estilo es una carpeta `estilos/<slug>/`:

| Archivo | Obligatorio | Qué es |
|---|---|---|
| `estilo.py` | sí | plugin: CSS, planos, transiciones, SFX y tratamiento de assets |
| `ESTILO.md` | sí | ficha: frontmatter (`nombre`, `voz`, `ejemplo`), cuándo usarlo, paleta, tipografía, motivos, reglas de movimiento |
| `miniatura.css` | sí | skin de los layouts de miniatura (`motor/miniaturas.py`); `{FONTS}` = esta carpeta `fonts/` |
| `fonts/` | sí | fuentes que usa (se copian al proyecto HyperFrames como `assets/fonts/`) |
| `preview.jpg` | sí | 4 frames del estilo en uso para la galería: de su video de referencia, o copia de `preview/preview.jpg` |
| `miniaturas.py` | no | layouts de miniatura propios: `def nombre(v, datos, w, h) -> body_html` |
| `preview/` | no | guion y escenas del preview de 10-15 s (los estilos nuevos de `nuevo-estilo`) |

## estilo.py

El motor (`motor/build.py`) inyecta estos nombres **antes** de ejecutar el módulo, así que se pueden usar a nivel de módulo:
- `W`, `H`: tamaño (1920×1080 o 1080×1920); `V`: True si es vertical;
- `AS`: `AS.img(id, bn=None)` y `AS.vid(id, bn=False)` devuelven la ruta del asset y lo registran para copiarlo;
- `esc`, `wspan(texto, cls)`, `norm`;
- `SFX`: lista de eventos `(t, efecto, dB)`;
- `HF`, `A_IMG`, `A_CUT`, `PIEZA`, `ESTILO_DIR`, `VIDEO`.

El módulo define:

```python
CSS = "..."                       # se inserta en cada sub-composición (#root, .shot, clases del estilo)
JS_HELPERS = "..."                # crea `tl` (gsap.timeline paused) y helpers de animación
def r_<tipo>(pid, sh, L): ...     # un plano: (html, js). sh["t"], sh["end"] absolutos; L(t) → tiempo local
                                  # sh["p"] = params de S.add; los planos "clip" reciben sh["clip_start"/"clip_end"]
TRANS = {"corte": 0.0, ...}       # entradas y su duración
def trans_js(pid, prev, kind, t): ...   # js de la entrada del plano (y salida del anterior)
def sfx_de(sh, primero): ...      # [(t_abs, efecto, dB)] que dispara el plano
BN_DEFAULT = False                # AS.img sin bn → ¿blanco y negro?
def IMG_VF(bn): ...               # filtro ffmpeg para preparar cada imagen
def VID_VF(bn): ...               # filtro para b-roll (None = copiar sin recodificar)
INDEX_BG = "#000"                 # fondo del index
GRANO_CSS = "..." | None          # capa de grano global
SFX_GAIN = {"whoosh": -21, ...}   # ganancia por efecto en la mezcla (archivos en audio-lib/sfx/)
PICO_ANTES = {"whoosh": -0.18}    # adelanto del pico del efecto respecto al evento
def post_shot(pid, sh, L, i): ... # opcional: html/js extra por plano (p. ej. entrada «flash»)
def index_extra(total): ...       # opcional: capas globales en el index (marca de agua, contador)
```

## Reglas que todo estilo cumple

- Ningún texto mide menos de 28 px en 1080p.
- Los sellos CONFIRMADO / TEORÍA / FILTRACIÓN / LECTURA tienen un plano o un parámetro (`sello=`) visible.
- Los elementos entran cuando la voz los nombra (`S.w`). Siempre hay algo nuevo cada 1.5-3 s.
- Las fuentes y la música son genéricas: nada de logos, tipografías ni temas registrados de una franquicia.
- Los planos y parámetros del estilo se pueden consultar con `./tl planos <slug>`.
