"""CIERRE · si Doom gana se acaban todos los mundos → video de Secret Wars."""
from esc_largo._k import still, im

def build(S):
    s = S.scene(S.t0, bg="doom", enter="ink", color="doom")
    still(s, "cn", "lf/lf04/castillo-ny", (110, 70, 1700, 940), S.t0 + 0.02, kb=S.peek("Esa es"), scale=1.12)
    t = S.w("Doom gana")
    s.text("dg", "SI DOOM GANA…", "kw", "papel", 960, 150, t, size=100, rot=-3)
    t = S.w("Se acaban todos")
    s.text("st", "¡SE ACABAN TODOS!", "ono", "rojo", 960, 880, t, rot=-5, hold=1.2)

    s = S.scene(S.w("Esa es"), bg="multi", enter="whip", color="multi")
    still(s, "bw", "lf/battleworld", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.1, pos="50% 40%")
    t = S.w("Secret Wars")
    s.text("sw", "SECRET WARS", "ttl", "amarillo", 960, 160, t, size=170, rot=-4, misreg=True)
    t = S.w("este video")
    s.text("ev", "▶ VE ESTE VIDEO", "kw", "papel", 960, 900, t, size=90, rot=-2, zoom=True)
