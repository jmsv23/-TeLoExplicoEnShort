"""¿Y EN EL CINE? CONFIRMADO / TEORÍA."""
from esc_largo._k import SV, full, tag


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    s.text("cc", "CÓMIC  vs.  CINE", "ttl", "amarillo", 960, 540, S.t0 + 0.1, size=170, rot=-3, misreg=True)

    s = S.scene(S.w("Lo confirmado"), bg="heroe", enter="whip")
    tag(s, "C", s.start + 0.05)
    s.text("lc", "LO CONFIRMADO", "kw", "papel", 960, 120, s.start + 0.05, size=80, rot=-2)
    t = S.w("el villano")
    s.img("dm", "lf/tr-doom-cerca.jpg", 140, 220, 520, 560, t, frm="L", label="DOOM", pos="50% 35%")
    t = S.w("hermanos Russo")
    s.text("ru", "LOS RUSSO DIRIGEN LAS DOS", "kw", "amarillo", 1260, 300, t, size=64, rot=-2)
    t = S.w("la familia")
    s.img("re", "a-pedro.jpg", 760, 420, 380, 460, t, frm="B", label="REED")
    s.img("su", "a-vanessa.jpg", 1180, 420, 380, 460, t + 0.25, frm="B", label="SUE")
    t = S.w("Franklin")
    s.sello("fr", "FRANKLIN", 1640, 820, t, color="heroe", rot=6, size=50)

    s = S.scene(S.w("Lo que es teoría"), bg="multi", enter="whip", color="multi")
    tag(s, "T", s.start + 0.05)
    s.text("lt", "LO QUE ES TEORÍA", "kw", "amarillo", 960, 960, s.start + 0.05, size=80, rot=-2, out=S.peek("reiniciar") - 0.1)
    t = S.w("en la película")
    s.svg("bw", SV + "battleworld.svg", 520, 440, 900, 506, t - 0.3, how="pop")
    s.sello("t1", "¿BATTLEWORLD?", 520, 760, t, color="multi", rot=-6, size=52)
    t = S.w("Equis Men")
    s.img("xm", "a-ciclope.jpg", 1060, 130, 340, 420, t, frm="R", label="X-MEN")
    t = S.w("otros Spider-Man")
    s.img("sp", "a-tobey.jpg", 1440, 130, 340, 420, t, frm="R", label="SPIDER-MAN")
    t = S.w("se quede con")
    s.sello("t2", "¿LA FAMILIA ROBADA?", 1420, 640, t, color="multi", rot=4, size=48)
    t = S.w("reiniciar")
    s.text("rs", "¿REINICIO TOTAL?", "kw", "amarillo", 960, 960, t, size=90, rot=-3, zoom=True)

    s = S.scene(S.w("Porque así terminó"), bg="tinta", enter="cut")
    tag(s, "T", s.start + 0.05)
    full(s, "fam", 253, None, s.start + 0.02, s.start + 9, scale=1.1)
    t = S.w("Marvel Studios")
    s.text("ms", "¿Y MARVEL STUDIOS?", "kw", "amarillo", 960, 960, t, size=80, rot=-2)
