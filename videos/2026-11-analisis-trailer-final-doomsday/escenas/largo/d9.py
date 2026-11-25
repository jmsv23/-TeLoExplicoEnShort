"""DETALLE 9 · El Mjolnir y el «sabes que sí»."""
from esc_largo._k import tag, tv, clipsc, still


def build(S):
    s = S.scene(S.w("Detalle nueve"), bg="tinta", enter="cut")
    still(s, "tit", "thor-flojo", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], scale=1.1)
    t = S.w("después del título")
    s.text("pt", "ESCENA POST-TÍTULO", "kw", "amarillo", 960, 140, t, size=80, rot=-3)

    clipsc(S, 0)

    s = S.scene(S.w("Steve tiene"), bg="heroe", enter="whip")
    tag(s, "C", s.start + 0.1)
    still(s, "mj", "steve-mjolnir", (60, 120, 1100, 800), s.start + 0.05, frm="L", pos="40% 50%")
    t = S.w("le molesta")
    s.text("lm", "«SABES QUE SÍ»", "kw", "papel", 610, 960, t, size=72, rot=-3)
    t = S.w("Pero espera")
    s.obj("eg", '<div class="globo" style="position:relative;width:600px;height:220px;font-size:64px;display:flex;align-items:center;justify-content:center">ENDGAME: ¡LO SABÍA!</div>', 1500, 420, t + 0.2, how="pop", rot=4)
    t = S.w("feliz")
    s.text("fz", "FELIZ", "ono", "amarillo", 1500, 700, t, rot=-6)

    s = S.scene(S.w("Entonces"), bg="multi", enter="halftone", color="multi")
    still(s, "ss", "steve-sabes", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.12)
    t = S.w("chiste")
    s.text("ch", "¿UN CHISTE?", "kw", "amarillo", 960, 140, t, size=90, rot=-3)
    t = S.w("teoría loca")
    tag(s, "T", t)
    t = S.w("Loki")
    s.obj("lk", __import__("lib").loki_helmet(420), 1500, 560, t, how="pop", rot=-6)
    s.text("lk2", "¿LOKI DISFRAZADO?", "ttl", "doom", 960, 930, t + 0.2, size=110, rot=-4, misreg=True)
