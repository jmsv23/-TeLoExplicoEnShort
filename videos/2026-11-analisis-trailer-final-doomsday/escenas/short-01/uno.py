from esc_short_01._k import tag, still


def build(S):
    s = S.scene(S.t0, bg="ceniza", enter="halftone")
    still(s, "gm", "gemas", (40, 560, 1000, 760), S.t0 + 0.05, kb=S.peek("Pues ahora"), frm="B", scale=1.2)
    t = S.w("se quedó en el pasado")
    s.text("sq", "SE QUEDÓ EN EL PASADO", "kw", "papel", 540, 1440, t, size=70, rot=-3)
    s = S.scene(S.w("Pues ahora"), bg="papel", enter="pageflip")
    tag(s, "C", s.start + 0.1)
    still(s, "cm", "camioneta", (40, 460, 1000, 420), s.start + 0.1, frm="L", pos="50% 50%")
    t = S.w("barba")
    still(s, "bb", "steve-barba", (40, 900, 1000, 420), t - 0.2, frm="R", pos="50% 25%", label="¡BARBA!")
    t = S.w("hijo")
    still(s, "hj", "hijo", (40, 1340, 1000, 420), t - 0.2, frm="L", pos="50% 30%", label="SU HIJO")
    t = S.w("no sabe")
    s.text("ns", "NO SABE NADA", "ono", "rojo", 540, 1690, t + 0.6, rot=-6)
