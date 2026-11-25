"""CUATRO · pregunta + vuelta al inicio (bucle)."""
from esc_short_01._k import still, vid, T1
from esc_largo._k import im

def build(S):
    s = S.scene(S.t0, bg="rojo", enter="cut", color="rojo")
    s.img("t", im("lf/lf04/thor-azul"), 0, 0, 1080, 960, S.t0 + 0.02, frm="L", label=None, pos="50% 40%")
    s.img("d", im("lf/lf04/doom-rayos"), 0, 960, 1080, 960, S.t0 + 0.3, frm="R", label=None, pos="50% 40%")
    s.text("lt", "THOR", "ttl", "papel", 540, 760, S.t0 + 0.2, size=110, rot=-3, sfx=False)
    s.text("ld", "DOOM", "ttl", "doom", 540, 1200, S.t0 + 0.4, size=110, rot=-3, sfx=False)
    s.text("vs", "VS", "ttl", "amarillo", 540, 960, S.t0 + 0.5, size=240, rot=-8, misreg=True)
    t = S.w("alcanza")
    s.globo("q", "¿LE ALCANZA?", 140, 420, 800, 180, t, size=72, rot=-3)
    t = S.w("vuelve a detener")
    vid(s, "lp", T1, 4.6, t, S.t1 - t + 0.05, pos="55% 50%")
    s.text("cm", "COMENTA 👇", "kw", "amarillo", 540, 1700, t + 0.2, size=80, rot=-2)
