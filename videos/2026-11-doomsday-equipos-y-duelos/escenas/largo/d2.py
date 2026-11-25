"""DUELO 2 · Magneto vs los Centinelas (LECTURA)."""
from esc_largo._k import tag, still, barra, vs, im

def build(S):
    s = vs(S, S.t0, "a-magneto", "MAGNETO", "lf/tr-doom-centinelas", "CENTINELAS", 2, bg="ceniza", posb="50% 50%")
    t = S.w("injusto")
    s.text("ij", "¡CASI INJUSTO!", "ono", "amarillo", 960, 980, t, rot=-5)

    s = S.scene(S.w("El ejército"), bg="doom", enter="ink", color="doom")
    still(s, "rb", "lf/lf04/robots-palmas", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Y el mutante"), scale=1.12)
    t = S.w("robots gigantes")
    s.text("rg", "ROBOTS GIGANTES DE METAL", "kw", "papel", 960, 150, t, size=80, rot=-3)
    t = S.w("cazar mutantes")
    s.text("cm", "¡CAZAMUTANTES!", "ono", "rojo", 1400, 900, t, rot=-6)

    s = S.scene(S.w("Y el mutante"), bg="heroe", enter="whip", color="heroe")
    still(s, "mg", "lf/tr-magneto", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Mi lectura"), scale=1.1)
    t = S.w("controla el metal")
    s.text("cm", "CONTROLA EL METAL", "ttl", "amarillo", 960, 880, t, size=120, rot=-4, misreg=True)
    t = S.w("Días del futuro")
    tag(s, "C", t)
    s.img("df", im("magneto-dofp-centinelas", "lf/tr-magneto"), 1180, 120, 640, 420, t, frm="R", label="DÍAS DEL FUTURO PASADO", sub="2014", pos="50% 40%")
    t = S.w("Casa Blanca")
    s.text("cb", "¡YA LO HIZO!", "ono", "amarillo", 1500, 640, t, rot=-6)

    s = S.scene(S.w("Mi lectura"), bg="papel", enter="halftone")
    tag(s, "L", s.start + 0.1)
    barra(s, "b1", "MAGNETO", 9, "heroe", 300, 300, 1320, s.start + 0.3)
    barra(s, "b2", "CENTINELAS", 6, "doom", 300, 420, 1320, s.start + 0.6)
    t = S.w("voltearle")
    s.text("vt", "VOLTEA AL EJÉRCITO", "ttl", "heroe", 960, 650, t, size=110, rot=-3)
    t = S.w("no es tonto")
    s.img("dm", im("lf/tr-doom-cerca"), 1300, 560, 560, 460, t, frm="R", label="PERO DOOM…")
    t = S.w("también es de metal")
    s.text("am", "¡ARMADURA DE METAL!", "ono", "rojo", 600, 900, t, rot=-5)
    t = S.w("Ese sí")
    s.text("es", "MAGNETO VS DOOM", "kw", "amarillo", 600, 1010, t, size=60, rot=-2)
