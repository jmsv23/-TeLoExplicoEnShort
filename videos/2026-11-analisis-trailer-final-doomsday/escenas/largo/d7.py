"""DETALLE 7 · Los héroes se pelean primero: Thunderbolts, Kate, Steve+Bucky, Cíclope vs Sam, Wakanda."""
from esc_largo._k import tag, tv, clipsc, still


def build(S):
    s = S.scene(S.w("Detalle siete"), bg="papel", enter="pageflip")
    tv(s, "tw", 102.8, s.start + 0.02, S.clip(0)["start"] - s.start, slam=False)
    t = S.w("Thunderbolts")
    s.text("tb", "THUNDERBOLTS*", "ttl", "rojo", 960, 140, t, size=120, rot=-4)
    t = S.w("nuevos Vengadores")
    s.text("nv", "= NUEVOS VENGADORES", "kw", "amarillo", 960, 900, t, size=80, rot=-2)

    clipsc(S, 0)

    s = S.scene(S.w("Ahí también"), bg="heroe", enter="whip")
    tag(s, "C", s.start + 0.1)
    still(s, "kt", "kate", (80, 140, 860, 560), s.start + 0.05, frm="L", label="KATE BISHOP")
    t = S.w("Jeili")
    s.text("hs", "HAILEE STEINFELD", "kw", "papel", 510, 820, t, size=60, rot=-2)
    t = S.w("abrazo")
    still(s, "ab", "abrazo", (980, 140, 860, 560), t - 0.1, frm="R", label="STEVE + BUCKY")
    t = S.w("Steve y Bucky")
    s.text("sb", "¡POR FIN!", "ono", "amarillo", 1410, 860, t, rot=-6)

    s = S.scene(S.w("Pero no todo"), bg="tinta", enter="cut")
    tag(s, "L", s.start + 0.1)
    still(s, "cs", "cyclops-sam", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(1)["start"], scale=1.1)
    t = S.w("Mansión X")
    s.text("mx", "¿LA MANSIÓN X?", "kw", "amarillo", 960, 140, t, size=80, rot=-3)
    t = S.w("Sam Wilson")
    s.text("zz", "¡ZZZAP!", "ono", "rojo", 1500, 880, t, rot=-6)

    clipsc(S, 1)

    s = S.scene(S.w("Es la regla"), bg="papel", enter="halftone")
    still(s, "gr", "cyclops-sam", (80, 200, 860, 600), s.start + 0.05, frm="L", label="X-MEN")
    still(s, "gr2", "abrazo", (980, 200, 860, 600), s.start + 0.4, frm="R", label="VENGADORES")
    s.text("vs", "VS", "ttl", "rojo", 960, 500, s.start + 0.6, size=180, rot=-6)
    t = S.w("regla de oro")
    s.text("ro", "REGLA DE ORO", "ttl", "rojo", 960, 120, t, size=110, rot=-3)
    t = S.w("entre ellos")
    s.text("ee", "¡PRIMERO ENTRE ELLOS!", "ono", "amarillo", 960, 950, t, rot=-5)
    s = S.scene(S.w("Y en Wakanda"), bg="tinta", enter="cut")
    still(s, "wk", "shuri", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(2)["start"], scale=1.1)
    t = S.w("Shuri")
    s.text("sh", "SHURI", "ttl", "amarillo", 400, 160, t, size=120, rot=-4)
    t = S.w("muro de agua")
    s.globo("ma", "¿Y ESE MURO DE AGUA?", 1100, 120, 700, 170, t, size=50, rot=3)

    clipsc(S, 2)
