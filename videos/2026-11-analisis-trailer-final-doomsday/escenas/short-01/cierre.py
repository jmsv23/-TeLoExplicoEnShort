from esc_short_01._k import tag, still


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    still(s, "cs", "castillo-ny", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.t1, pos="80% 50%", scale=1.15, frm="B")
    t = S.w("diez detalles")
    s.text("10", "+10 DETALLES", "ttl", "amarillo", 540, 520, t, size=130, rot=-4)
    t = S.w("casi nadie")
    s.text("q", "?", "ttl", "rojo", 760, 900, t, size=360, rot=8)
    t = S.w("video completo")
    s.text("vc", "VIDEO COMPLETO ↗", "kw", "papel", 540, 1500, t, size=84, rot=-3, zoom=True)
