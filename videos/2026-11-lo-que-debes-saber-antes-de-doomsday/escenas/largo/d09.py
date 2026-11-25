"""DATO 9 · Los nuevos Vengadores (Thunderbolts*)."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato nueve"), bg="tinta", enter="ink")
    s.text("d", "DATO 9", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Thunderbolts")
    s.img("tb", "a-thunder.jpg", 960, 120, 860, 520, t, frm="R", pos="50% 40%", label="THUNDERBOLTS*")
    t = S.w("Valentina")
    s.phpanel("val", "N-83", "Valentina Allegra de Fontaine", "retrato de Julia Louis-Dreyfus", 100, 380, 640, 600, t, frm="L", label="VALENTINA · CIA")

    s = S.scene(S.w("Yelena"), bg="papel", enter="pageflip")
    team = [("Yelena", "a-yelena.jpg", "YELENA"), ("Bucky", "a-bucky.jpg", "BUCKY"), ("Ghost", "a-ghost.jpg", "GHOST"),
            ("Guardián Rojo", "a-redguardian.jpg", "GUARDIÁN ROJO"), ("John Walker", "a-walker.jpg", "U.S. AGENT")]
    first = True
    for k, (word, f, lab) in enumerate(team):
        t = s.start + 0.05 if first else S.w(word)
        first = False
        s.img(f"t{k}", f, 70 + k * 360, 120, 330, 470, t, frm="T", pos="50% 20%", label=lab, rot=(-3, 2, -2, 3, -1)[k])
    t = S.w("Sentry")
    s.phpanel("sen", "N-84", "Bob / Sentry", "retrato de Lewis Pullman como Sentry", 520, 640, 520, 400, t, frm="B", label="SENTRY")
    t = S.w("The Void")
    s.text("void", "THE VOID", "ttl", "papel", 1430, 830, t, size=140, rot=-5, misreg=True)
    s.slab("ink", "tinta", t - 0.05, t + 0.35, pat=False)

    s = S.scene(S.w("Tras salvar"), bg="heroe", enter="halftone", color="amarillo")
    t = S.w("nuevos Vengadores")
    s.text("nv", "LOS NUEVOS VENGADORES", "kw", "amarillo", 960, 300, t, size=130, rot=-4, misreg=True)
    t = S.w("catorce meses")
    s.text("14", "14 MESES DESPUÉS", "ttl", "papel", 960, 640, t, size=110, rot=-2)
    t = S.w("espacio")
    s.sfx("riser", t - 1.0, -6)

    c = S.clip(0)
    s = S.scene(c["start"] - 0.35, bg="tinta", enter="cut")
    s.video("nave", c["src"], c["in"], c["start"], c["end"] - c["start"], 360, 140, 1200, 620, tag="POSCRÉDITOS · THUNDERBOLTS*", frm="B")

    s = S.scene(S.w("Una nave"), bg="ciencia", enter="halftone", color="ciencia")
    s.video("logo4", "lf-c01-thunderbolts-nave-4f.mp4", 19.5, s.start + 0.05, 5.0, 160, 120, 1100, 560, tag="EL 4 EN LA NAVE", frm="L")
    t = S.w("cuatro de los Cuatro Fantásticos")
    s.com("four", "fourEmblem", 1560, 380, 340, 340, t, how="pop")
    t = S.w("confirmación directa")
    s.sello("conf", "CONFIRMADO", 1540, 720, t, color="heroe", rot=-8)
    t = S.w("tocando el nuestro")
    s.text("toc", "SU UNIVERSO TOCA EL NUESTRO", "kw", "papel", 960, 960, t, size=80, rot=-2)
