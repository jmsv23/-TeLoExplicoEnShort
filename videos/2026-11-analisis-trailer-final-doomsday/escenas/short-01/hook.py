from esc_short_01._k import tag, still


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    still(s, "st", "steve-barba", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.peek("empezó"), pos="52% 30%", scale=1.08, frm="B")
    t = S.w("tráiler final")
    s.text("tf", "TRÁILER FINAL", "kw", "amarillo", 540, 520, t, size=90, rot=-3)
    t = S.w("empezó")
    still(s, "dm", "doom-rayos", (0, 960, 1080, 960), t - 0.2, frm="B", pos="45% 50%")
    t = S.w("Steve Rogers")
    s.sello("cu", "¡FUE SU CULPA!", 540, 960, t - 0.3, color="rojo", rot=-8, size=100)
    s.sfx("braam", t, -6)
