"""HOOK · Stormbreaker detenida → ¿quién puede con Doom? → promesa: equipos, poder y 7 duelos."""
from esc_largo._k import tag, still, fstill, clipsc, im, T1, TR, fondo

def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    fstill(s, "dm", T1, 10.6, (0, 0, 1920, 1080), S.t0 + 0.02, kb=S.peek("Entonces"), frm="B", scale=1.15)
    t = S.w("una mano")
    s.text("um", "¡CON UNA MANO!", "ono", "amarillo", 1400, 200, t, rot=-6)
    t = S.w("casi mata")
    s.text("cm", "EL HACHA QUE CASI MATA A THANOS", "kw", "papel", 960, 930, t, size=72, rot=-2)

    s = S.scene(S.w("Entonces"), bg="doom", enter="whip", color="doom")
    still(s, "dc", "lf/tr-doom-cerca", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], frm="R", scale=1.12)
    t = S.w("quién puede")
    s.text("qp", "¿QUIÉN PUEDE CON ÉL?", "ttl", "amarillo", 960, 880, t, size=130, rot=-4, misreg=True)
    s.sfx("braam", t, -6)

    s, c = clipsc(S, 0, tag_txt="PRIMER TRÁILER")
    s.text("sb", "STORMBREAKER… ¡DETENIDA!", "kw", "amarillo", 960, 960, c["start"] + 1.4, size=70, rot=-2, sfx=False)

    s = S.scene(S.w("Ya salió"), bg="papel", enter="halftone")
    still(s, "gr", "lf/lf04/grupo", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Hoy te"), scale=1.1)
    t = S.w("tráiler final")
    tag(s, "C", t)
    s.text("tf", "TRÁILER FINAL · 23 NOV", "kw", "amarillo", 960, 940, t, size=76, rot=-2)
    t = S.w("cada bando")
    s.text("cb", "¿QUIÉN EN CADA BANDO?", "ono", "rojo", 1400, 200, t, rot=-6)

    s = S.scene(S.w("Hoy te"), bg="papel", enter="pageflip")
    fondo(s, "bg", "lf/lf04/grupo", s.start + 0.02, S.peek("Y ojo"), dim=0.35)
    t = S.w("los equipos")
    s.img("e1", im("lf/lf04/grupo"), 60, 200, 580, 520, t - 0.1, frm="L", label="LOS EQUIPOS")
    t = S.w("qué tan poderoso")
    s.img("e2", im("lf/lf04/thor-dorado"), 670, 200, 580, 520, t - 0.1, frm="B", label="SU PODER")
    t = S.w("siete duelos")
    s.img("e3", im("lf/lf04/cyclops-sam"), 1280, 200, 580, 520, t - 0.1, frm="R", label="LOS DUELOS")
    s.text("7d", "7 DUELOS", "ttl", "rojo", 960, 880, t + 0.3, size=170, rot=-4, zoom=True)

    s = S.scene(S.w("Y ojo"), bg="tinta", enter="cut")
    still(s, "cs", "lf/lf04/rayo-ciclope", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.12)
    t = S.w("primera pelea")
    s.text("pp", "LA PRIMERA PELEA…", "kw", "papel", 960, 150, t, size=90, rot=-3)
    t = S.w("no es contra")
    s.text("ne", "¿NO ES CONTRA DOOM?", "ono", "amarillo", 960, 900, t, rot=-5, hold=1.2)
