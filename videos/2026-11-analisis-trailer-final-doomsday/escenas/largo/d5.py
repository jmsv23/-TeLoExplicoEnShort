"""DETALLE 5 · Dos planetas en el cielo: incursión + Thor vs Doom."""
from esc_largo._k import tag, tv, still


def build(S):
    s = S.scene(S.w("Detalle cinco"), bg="tinta", enter="cut")
    tag(s, "L", s.start + 0.1)
    still(s, "ny", "planeta-ny", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Eso es"), scale=1.08)
    t = S.w("otro planeta")
    s.obj("aro", '<div style="width:300px;height:300px;border:14px solid #E8212B;border-radius:50%"></div>', 1480, 360, t, how="pop")
    s.text("op", "¡DOS PLANETAS!", "ono", "amarillo", 960, 900, t + 0.2, rot=-6)

    s = S.scene(S.w("Eso es"), bg="multi", enter="halftone", color="multi")
    s.img("inc", "lf/incursion.jpg", 110, 70, 1700, 940, s.start + 0.02, frm="B", pos="50% 50%")
    s.kenburns("inc", s.start + 0.2, S.peek("Justo después"), scale=1.15)
    t = S.w("incursión")
    s.text("in", "¡INCURSIÓN!", "ono", "amarillo", 960, 200, t, rot=-6, hold=1.0)
    s.sfx("rumble", t, -4)
    t = S.w("desaparecer")
    s.text("ds", "UNO DE LOS DOS DESAPARECE", "kw", "papel", 960, 900, t, size=70, rot=-2)
    t = S.w("Guerras Secretas")
    s.text("gs", "SECRET WARS", "ttl", "rojo", 1460, 560, t, size=110, rot=-6)

    s = S.scene(S.w("Justo después"), bg="tinta", enter="cut")
    tv(s, "tvd", 94.8, s.start + 0.02, S.t1 - s.start, slam=False)
    t = S.w("rayos azules")
    s.text("ra", "¡KRA-KOOM!", "ono", "amarillo", 1500, 180, t, rot=-6)
    s.sfx("thunder", t, -6)
    t = S.w("ni se mueve")
    s.text("ns", "DOOM NI SE MUEVE", "kw", "doom", 960, 920, t, size=80, rot=-3)
