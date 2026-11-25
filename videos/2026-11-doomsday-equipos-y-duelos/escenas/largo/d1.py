"""DUELO 1 · Cíclope vs Sam Wilson (CONFIRMADO en el tráiler)."""
from esc_largo._k import tag, still, clipsc, barra, vs, im

def build(S):
    s = vs(S, S.t0, "a-samcap", "SAM WILSON", "a-ciclope", "CÍCLOPE", 1, bg="heroe")
    t = S.w("no es contra")
    s.text("nd", "¡NO ES CONTRA DOOM!", "ono", "rojo", 960, 980, t, rot=-4)

    clipsc(S, 0, cap="«DEJEN DE PELEARSE POR TONTERÍAS»", cap_at=2.5, tag_txt="TRÁILER FINAL")

    s = S.scene(S.w("Confirmado"), bg="papel", enter="halftone")
    still(s, "cs", "lf/lf04/cyclops-sam", (110, 70, 1700, 620), s.start + 0.02, kb=S.peek("Sam tiene"), scale=1.1)
    tag(s, "C", s.start + 0.1)
    t = S.w("mansión")
    s.text("mx", "¿LA MANSIÓN X?", "kw", "amarillo", 1450, 120, t, size=72, rot=-3)
    t = S.w("dos universos")
    s.text("du", "HÉROES DE 2 UNIVERSOS", "ttl", "heroe", 960, 820, t, size=100, rot=-3)
    t = S.w("enemigo es otro")
    s.text("eo", "¡EL ENEMIGO ES OTRO!", "ono", "rojo", 960, 980, t, rot=-5)

    s = S.scene(S.w("Sam tiene"), bg="tinta", enter="whip")
    s.img("sa", im("a-samcap"), 80, 120, 520, 700, s.start + 0.02, frm="L", label="SAM")
    s.img("cy", im("lf/lf04/rayo-ciclope"), 1320, 120, 520, 700, S.peek("Cíclope dispara") - 0.1, frm="R", label="CÍCLOPE")
    t = S.w("vibranio")
    barra(s, "b1", "SAM", 5, "heroe", 640, 300, 640, t)
    t = S.w("hombre normal")
    s.text("hn", "SIN TRAJE = HUMANO", "kw", "papel", 960, 200, t, size=56, rot=-2)
    t = S.w("Cíclope dispara")
    barra(s, "b2", "CÍCLOPE", 6, "rojo", 640, 420, 640, t + 0.2)
    t = S.w("gana Cíclope")
    s.sello("gc", "GANA CÍCLOPE", 960, 640, t, color="rojo", rot=-8, size=80)
    tag(s, "L", t + 0.2, x=960, y=760)
    t = S.w("alguien les grita")
    s.globo("gr", "«¡DEJEN DE PELEARSE!»", 600, 860, 720, 150, t, size=52, rot=-2)
