"""CIERRE: pregunta + LF01 + suscripción."""
from esc_largo._k import full, tag, vin


def build(S):
    s = S.scene(S.t0, bg="doom-osc", enter="ink")
    full(s, "tr", 269, None, S.t0 + 0.02, S.t0 + 10, scale=1.08)
    t = S.w("merecía ganar")
    s.cap("pq", "¿DOOM MERECÍA GANAR?", t, left=460, top=860, width=1000)
    t = S.w("comentarios")
    s.text("cm", "¡COMENTA!", "ono", "amarillo", 1600, 300, t, rot=-6, hold=1.2)

    s = S.scene(S.w("Y si quieres repasar"), bg="papel", enter="pageflip")
    vin(s, "lf01", 266, None, s.start + 0.05, box=(160, 140, 1000, 560), frm="L", kb=s.start + 8)
    s.text("mt", "MIRA TAMBIÉN", "kw", "rojo", 660, 120, s.start + 0.1, size=64, rot=-3)
    s.text("lf", "LO QUE DEBES SABER ANTES DE VER DOOMSDAY", "kw", "tinta", 660, 760, s.start + 0.4, size=46, rot=-2)
    t = S.w("Suscríbete")
    s.text("sb", "¡SUSCRÍBETE!", "ttl", "rojo", 1440, 760, t, size=120, rot=-4, zoom=True)
    t = S.w("historia sigue")
    s.text("hs", "ESTA HISTORIA SIGUE…", "kw", "tinta", 960, 960, t, size=70, rot=-2)
