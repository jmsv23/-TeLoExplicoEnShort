from esc_short_01._k import tag, still


def build(S):
    s = S.scene(S.t0, bg="multi", enter="halftone", color="multi")
    tag(s, "T", S.t0 + 0.1)
    t = S.w("Vidas robadas")
    s.text("vr", "VIDAS ROBADAS", "kw", "papel", 540, 520, t, size=100, rot=-3)
    t = S.w("Como la de Steve")
    still(s, "sp", "steve-peggy-porche", (40, 640, 1000, 620), t - 0.1, frm="B", pos="60% 40%")
    s.draw("rama", "M 120 1420 C 360 1420 520 1520 640 1600", "#C99700", t + 0.3, w=20, dur=0.6)
    t = S.w("no era el suyo")
    s.draw("rama2", "M 640 1600 C 760 1680 860 1700 960 1700", "#1FA85A", t, w=24, dur=0.5)
    t = S.w("Coincidencia")
    s.text("co", "¿COINCIDENCIA?", "ono", "amarillo", 540, 1400, t, rot=-6)
    t = S.w("No creo")
    s.text("nc", "NO CREO.", "ttl", "rojo", 540, 1760, t, size=120, rot=-4)
