"""EL BANDO DE DOOM · confirmado (Doom, Centinelas, brujas) + reclutados (Hulk, Wanda) = TEORÍA."""
from esc_largo._k import tag, still, clipsc, im, fondo

def build(S):
    s = S.scene(S.t0, bg="doom", enter="ink", color="doom")
    fondo(s, "bg", "lf/lf04/doom-catedral", S.t0 + 0.02, S.clip(0)["start"], dim=0.35)
    s.text("ob", "EL BANDO DE DOOM", "ttl", "amarillo", 960, 110, S.t0 + 0.1, size=120, rot=-4)
    t = S.w("confirmado")
    tag(s, "C", t, x=260, y=240)
    t = S.w("Doom")
    s.img("d1", im("lf/tr-doom-cerca"), 60, 300, 580, 600, t - 0.1, frm="L", label="DOOM")
    t = S.w("Centinelas")
    s.img("d2", im("lf/tr-doom-centinelas"), 670, 300, 580, 600, t - 0.1, frm="B", label="CENTINELAS", pos="50% 50%")
    t = S.w("tres brujas")
    s.img("d3", im("lf/lf04/brujas"), 1280, 300, 580, 600, t - 0.1, frm="R", label="3 BRUJAS", pos="50% 40%")

    clipsc(S, 0, bg="doom-osc", tag_txt="ADELANTO D23")

    s = S.scene(S.w("Y luego"), bg="doom-osc", enter="whip", color="doom")
    fondo(s, "bg2", "a-visionquest", s.start + 0.02, S.peek("Pero cuidado"), dim=0.3)
    s.text("rc", "LOS «RECLUTADOS»", "kw", "amarillo", 960, 110, s.start + 0.1, size=90, rot=-3)
    t = S.w("Endgame Encore")
    s.img("hk", im("a-bruce"), 100, 230, 760, 640, t - 0.1, frm="L", label="BANNER / HULK", sub="ENDGAME ENCORE", pos="50% 25%")
    t = S.w("Bruja Escarlata")
    s.img("wd", im("a-scarlet"), 1060, 230, 760, 640, t - 0.1, frm="R", label="BRUJA ESCARLATA", sub="VISIONQUEST", pos="50% 20%")
    t = S.w("despierta")
    s.globo("gd", "«DESPIERTA… TU PODER SERÁ MÍO»", 560, 880, 800, 150, t, size=46, rot=-2)

    s = S.scene(S.w("Pero cuidado"), bg="papel", enter="halftone")
    still(s, "ol", "a-olsen-crop", (1100, 120, 700, 840), s.start + 0.05, frm="R", label="ELIZABETH OLSEN", pos="50% 25%")
    t = S.w("ninguna fuente")
    s.sello("nc", "NADA OFICIAL", 520, 300, t, color="rojo", rot=-8, size=90)
    t = S.w("no sale")
    s.globo("ns", "«NO SALGO EN DOOMSDAY»", 1150, 840, 620, 140, t, size=48, rot=2)
    t = S.w("son teoría")
    tag(s, "T", t, x=520, y=520, size=80)
    t = S.w("muy fuerte")
    s.text("mf", "MUY FUERTE… PERO TEORÍA", "kw", "multi", 520, 760, t, size=64, rot=-3)
