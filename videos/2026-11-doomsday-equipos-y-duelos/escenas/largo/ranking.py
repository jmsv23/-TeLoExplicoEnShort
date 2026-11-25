"""RANKING FINAL · tabla de poder (LECTURA), 20 s."""
from esc_largo._k import tag, barra, fondo

def build(S):
    s = S.scene(S.t0, bg="papel", enter="pageflip")
    s.text("rk", "MI RANKING DE PODER", "ttl", "rojo", 960, 90, S.t0 + 0.1, size=110, rot=-3)
    tag(s, "L", S.t0 + 0.3, x=1650, y=100, size=44)
    s.text("q", "¿QUIÉN ES EL MÁS FUERTE?", "ono", "amarillo", 960, 560, S.t0 + 0.4, rot=-5, hold=1.0, out=S.peek("En la cima") - 0.1)
    filas = [("En la cima", [("LOKI", 10, "multi"), ("DOOM", 10, "doom")]),
             ("Justo debajo", [("SENTRY", 9, "amarillo"), ("THOR", 9, "heroe")]),
             ("Luego", [("XAVIER", 8, "heroe"), ("MAGNETO", 8, "rojo"), ("SUE", 8, "ciencia")]),
             ("al final", [("SAM", 4, "heroe"), ("BUCKY", 4, "ceniza"), ("YELENA", 3, "ceniza")])]
    pos = [(60, 0), (990, 0), (60, 1), (990, 1), (60, 2), (990, 2), (60, 3), (60, 4), (990, 4), (60, 5)]
    k = 0
    for frase, items in filas:
        t = S.w(frase)
        for j, (n, v, c) in enumerate(items):
            x, row = pos[k]
            barra(s, f"r{k}", n, v, c, x, 190 + row * 118, 870, t + 0.25 * j, h=96, lsize=46)
            k += 1
    S.w("no ganan por poder")
    s.text("ep", "¡GANAN POR ESTAR AHÍ!", "ono", "rojo", 1280, 950, S.w("estar ahí"), size=100, rot=-5)
