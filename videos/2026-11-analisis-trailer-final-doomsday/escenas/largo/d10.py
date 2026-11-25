"""DETALLE 10 · El último plano: castillo en Nueva York → Battleworld; cierra «vidas robadas»."""
from esc_largo._k import tag, tv, still


def build(S):
    s = S.scene(S.w("Y el detalle diez"), bg="tinta", enter="cut")
    still(s, "cs", "castillo-ny", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Un castillo europeo"), frm="B", scale=1.35, x=-220, y=40)
    t = S.w("casi nadie vio")
    s.text("cn", "EL QUE CASI NADIE VIO", "kw", "amarillo", 960, 140, t, size=80, rot=-3)
    t = S.w("castillo")
    tag(s, "L", t)
    t = S.w("rascacielos")
    s.text("ny", "¿EN NUEVA YORK?", "ono", "amarillo", 1400, 900, t, rot=-6)

    s = S.scene(S.w("Un castillo europeo"), bg="multi", enter="halftone", color="multi")
    s.svg("bw", "lf/lf03-battleworld.svg", 960, 540, 1500, 900, s.start + 0.05, how="pop")
    t = S.w("se fusionan")
    s.text("fu", "¡MUNDOS FUSIONADOS!", "ono", "amarillo", 960, 140, t, rot=-5)
    t = S.w("En los cómics")
    tag(s, "T", t)
    t = S.w("Bátelguorld")
    s.text("bw2", "BATTLEWORLD", "ttl", "rojo", 960, 940, t, size=150, rot=-4, misreg=True)
    s.sfx("braam", t, -6)

    s = S.scene(S.w("Ahora sí"), bg="doom", enter="ink", color="doom")
    still(s, "dm", "doom-catedral", (360, 360, 1200, 560), s.start + 0.1, frm="B", kb=S.peek("primera prueba"))
    t = S.w("vidas robadas")
    s.text("vr", "VIDAS ROBADAS", "ttl", "papel", 960, 200, t, size=170, rot=-4, misreg=True)
    t = S.w("primera prueba")
    still(s, "st", "steve-peggy-porche", (360, 360, 1200, 560), t - 0.3, frm="B", label="PRUEBA N.º 1")
    t = S.w("devuelvan")
    s.text("dv", "¡DEVUÉLVANLO TODO!", "ono", "rojo", 960, 960, t, rot=-5, hold=1.2)
    s.shake("st", t + 0.3)
    s.sfx("explosion", t + 0.3, -6)
