"""DATO 10 · Los Cuatro Fantásticos vienen de otro universo."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato diez"), bg="ciencia", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 10", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Cuatro Fantásticos")
    s.img("ff", "a-fantastic4.jpg", 960, 120, 860, 560, t, frm="R", pos="50% 35%")
    t = S.w("seiscientos dieciséis")
    s.sello("616", "TIERRA-616: NO", 480, 560, t, color="rojo", rot=-6)
    t = S.w("ochocientos veintiocho")
    s.sello("828", "TIERRA-828", 480, 760, t, color="heroe", rot=-4, size=86)

    s = S.scene(S.w("retrofuturista"), bg="papel", enter="pageflip")
    s.img("fam", "lf/tr-sue-franklin.jpg", 80, 120, 860, 500, s.start + 0.05, frm="L", pos="50% 40%")
    t = S.w("Reed")
    for k, (f, lab, w) in enumerate([("a-pedro.jpg", "REED", "Reed"), ("a-vanessa.jpg", "SUE", "Sue"), ("a-joseph.jpg", "JOHNNY", "Johnny"), ("a-ebon.jpg", "BEN", "Ben")]):
        tt = t if k == 0 else S.w(w)
        s.img(f"m{k}", f, 1000 + (k % 2) * 430, 120 + (k // 2) * 430, 400, 400, tt, frm="R", pos="50% 25%", label=lab)
    t = S.w("héroes mundiales")
    s.text("60", "AÑOS 60 · RETROFUTURO", "kw", "ciencia", 510, 760, t, size=78, rot=-3)

    s = S.scene(S.w("Galactus"), bg="tinta", enter="halftone", color="multi")
    s.phpanel("gal", "N-48", "Galactus", "still de First Steps", 80, 80, 900, 900, s.start + 0.05, frm="L", label="GALACTUS")
    t = S.w("Franklin")
    s.img("fr", "lf/tr-sue-franklin.jpg", 1060, 140, 760, 460, t, frm="R", pos="50% 40%", label="FRANKLIN RICHARDS")
    t = S.w("más poderosos")
    s.text("pod", "UNO DE LOS SERES MÁS PODEROSOS", "kw", "amarillo", 1440, 720, t, size=58, rot=-3)
    t = S.w("reviviendo a Johnny")
    s.text("rev", "¡REVIVE A JOHNNY!", "ono", "ciencia", 1440, 900, t, rot=-6, hold=1.1)

    s = S.scene(S.w("Y en la escena"), bg="tinta", enter="ink")
    s.video("4y", "lf-c02-firststeps-4-anos.mp4", 0.0, s.start + 0.05, 2.6, 260, 120, 1400, 600, tag="POSCRÉDITOS · FIRST STEPS", slam=False)
    t = S.w("aparece Doom")
    s.sfx("heartbeat", t - 0.8, -3)
    s.video("df", "lf-c03-firststeps-doom-franklin.mp4", 0.2, t, 5.2, 160, 90, 1600, 700, tag="DOOM", frm="B")
    s.zoom(t + 0.3)
    s.sfx("stinger", t + 0.2, -4)
    t = S.w("Marvel no ha dicho")
    s.svg("mano", "lf/doom-mano-mascara.svg", 520, 820, 480, 400, t, how="slide", frm="L")
    s.sello("nc", "NO CONFIRMADO", 1400, 900, t + 0.3, color="rojo", rot=-6)
    t = S.w("damos por hecho")
    s.text("828", "¿DOOM VIVE EN LA 828?", "kw", "amarillo", 1300, 700, t, size=74, rot=-3)
