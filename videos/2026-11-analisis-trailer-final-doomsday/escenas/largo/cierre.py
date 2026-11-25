"""12 · CIERRE: fecha del tráiler latino + pregunta + suscripción."""
from esc_largo._k import tv, still


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="ink")
    tv(s, "fe", 184.0, S.t0 + 0.02, S.peek("Y tú") - S.t0, slam=False)
    t = S.w("dieciséis de diciembre")
    s.text("16", "16 DIC · TRÁILER LATINO", "kw", "amarillo", 960, 940, t, size=70, rot=-2)
    t = S.w("muy poco")
    s.text("fd", "¡FALTA MUY POCO!", "ono", "rojo", 1450, 160, t, rot=-6)

    s = S.scene(S.w("Y tú"), bg="heroe", enter="whip")
    still(s, "dm", "doom-rayos", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.1)
    t = S.w("qué viste")
    s.globo("q", "¿QUÉ VISTE TÚ?", 120, 120, 620, 180, t, size=64, rot=-3)
    t = S.w("comentarios")
    s.text("cm", "¡COMENTA!", "ono", "amarillo", 1500, 200, t, rot=-6)
    t = S.w("suscríbete")
    s.text("sb", "¡SUSCRÍBETE!", "ttl", "rojo", 960, 900, t, size=140, rot=-4, zoom=True)
