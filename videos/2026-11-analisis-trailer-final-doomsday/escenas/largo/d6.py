"""DETALLE 6 · El rayo dorado de Thor (Fuerza Odín, teoría)."""
from esc_largo._k import tag, tv, still


def build(S):
    s = S.scene(S.w("Detalle seis"), bg="tinta", enter="cut")
    tag(s, "L", s.start + 0.1)
    still(s, "az", "thor-azul", (60, 160, 880, 620), s.start + 0.05, frm="L", label="RAYO AZUL")
    still(s, "dr0", "doom-rayos", (980, 160, 880, 620), s.start + 0.5, frm="R", label="CONTRA DOOM")
    t = S.w("dorado")
    still(s, "do", "thor-dorado", (980, 160, 880, 620), t - 0.1, frm="R", label="RAYO DORADO")
    s.text("vs", "VS", "ttl", "rojo", 960, 430, t + 0.2, size=150, rot=-6)
    s.sfx("thunder", t, -6)

    s = S.scene(S.w("En un tráiler anterior"), bg="papel", enter="pageflip")
    still(s, "bq", "thor-dorado-bosque", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Y ojo"), scale=1.15, frm="B")
    t = S.w("Odín")
    s.text("od", "REZÁNDOLE A ODÍN", "kw", "papel", 960, 140, t, size=80, rot=-3)
    t = S.w("teoría")
    tag(s, "T", t)
    t = S.w("Fuerza Odín")
    s.text("fo", "¿FUERZA ODÍN?", "ttl", "amarillo", 960, 900, t, size=140, rot=-4, misreg=True)
    s.sfx("magic", t, -6)

    s = S.scene(S.w("Y ojo"), bg="heroe", enter="whip")
    still(s, "dz", "doom-rayos", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.1)
    t = S.w("rayo azul")
    s.text("ra", "CONTRA DOOM: AZUL", "kw", "papel", 960, 140, t, size=80, rot=-3)
    t = S.w("todavía no")
    s.text("tn", "¿Y EL DORADO?", "ono", "amarillo", 1450, 900, t, rot=-6)
