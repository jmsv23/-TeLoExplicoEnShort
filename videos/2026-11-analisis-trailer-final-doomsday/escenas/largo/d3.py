"""DETALLE 3 · «Hicimos lo necesario»: el flashback y la rama de Steve."""
import lib as L
from esc_largo._k import tag, tv, clipsc, still


def build(S):
    s = S.scene(S.w("Detalle tres"), bg="ceniza", enter="halftone")
    still(s, "gm", "gemas", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Steve en la plataforma"), scale=1.2)
    t = S.w("blanco y negro")
    s.text("bn", "FLASHBACK", "kw", "papel", 960, 140, t, size=96, rot=-3)
    t = S.w("Gemas del Infinito")
    s.text("gi", "LAS GEMAS", "ono", "amarillo", 1450, 880, t, rot=-6)
    s = S.scene(S.w("Steve en la plataforma"), bg="tinta", enter="cut")
    still(s, "pl", "plataforma", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], scale=1.1)
    t = S.w("devolverlas")
    s.text("dv", "A DEVOLVERLAS", "kw", "amarillo", 960, 900, t, size=90, rot=-3)

    clipsc(S, 0)

    s = S.scene(S.w("Steve devolvió"), bg="papel", enter="pageflip")
    s.obj("lin", '<div style="width:1500px;height:18px;background:#0B0B14"></div>', 960, 340, s.start + 0.05, how="slide", frm="L")
    s.text("pr", "LÍNEA PRINCIPAL", "kw", "tinta", 420, 270, s.start + 0.3, size=48, rot=0)
    t = S.w("se quedó a vivir")
    s.draw("rama", "M 620 340 C 760 420 820 560 1000 700 S 1300 820 1540 820", "#C99700", t, w=18, dur=0.8)
    still(s, "cs", "camioneta", (1300, 600, 560, 340), t + 0.6, frm="R", label="LA CASA DE STEVE")
    t = S.w("la suya")
    s.text("rs", "RAMA DE STEVE", "ttl", "amarillo", 760, 880, t, size=100, rot=-4, misreg=True)

    s = S.scene(S.w("Y aquí está"), bg="tinta", enter="ink")
    tv(s, "cons", 64.4, s.start + 0.05, S.peek("Hay fans") - s.start, slam=False)
    t = S.w("consecuencias")
    s.text("cn", "CONSECUENCIAS", "ttl", "rojo", 960, 900, t, size=130, rot=-4)
    s = S.scene(S.w("Hay fans"), bg="multi", enter="halftone", color="multi")
    tag(s, "T", s.start + 0.1)
    s.draw("r2", "M 200 700 C 500 700 700 520 960 520", "#C99700", s.start + 0.1, w=18, dur=0.6)
    t = S.w("Víctor von Doom")
    s.draw("r3", "M 960 520 C 1150 520 1250 560 1380 560", "#1FA85A", t - 0.4, w=22, dur=0.6)
    s.img("dm", "lf/tr-doom-cerca.jpg", 1340, 300, 480, 520, t, frm="R", pos="50% 40%", label="DOOM")
    t = S.w("teoría")
    s.text("ts", "¿LA RAMA CAMBIÓ A DOOM?", "kw", "amarillo", 700, 880, t, size=72, rot=-3)
