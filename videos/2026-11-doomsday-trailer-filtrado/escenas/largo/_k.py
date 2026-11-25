"""Piezas comunes de LF02: sello de estado (FILTRACIÓN / CONFIRMADO / TEORÍA) arriba a la izquierda."""
LFV = ""  # migrado: las fuentes viven en assets/video/<id>.mp4
I = "lf/lf02/"          # fotos y recortes de LF02
SV = "lf/lf02-"         # ilustraciones SVG de LF02

ESTADO = {"F": ("FILTRACIÓN", "rojo"), "C": ("CONFIRMADO", "heroe"), "T": ("TEORÍA", "multi"),
          "R": ("RUMOR", "multi"), "N": ("NO CONFIRMADO", "rojo"), "K": ("DE LOS CÓMICS", "tinta")}
_n = [0]


def tag(s, k, at, out=None):
    """sello de estado fijo arriba a la izquierda (zona libre: el contador va arriba a la derecha)."""
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, 250, 90, at, color=col, rot=-5, size=44, out=out)
    return s
