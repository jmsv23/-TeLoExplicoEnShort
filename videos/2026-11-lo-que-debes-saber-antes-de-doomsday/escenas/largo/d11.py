"""DATO 11 · Los X-Men."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato once"), bg="amarillo" if False else "rojo", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 11", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("X-Men")
    s.obj("x", L.xlogo(420), 1340, 520, t, how="drop")
    s.text("ya", "YA EXISTEN EN EL MCU", "kw", "papel", 520, 600, t + 0.3, size=90, rot=-4)

    s = S.scene(S.w("The Marvels"), bg="papel", enter="pageflip")
    s.phpanel("mon", "N-25", "Mónica Rambeau", "retrato o still de The Marvels", 80, 120, 620, 620, s.start + 0.05, frm="L", label="MÓNICA RAMBEAU")
    t = S.w("grieta")
    s.draw("gr", "M960 60 L900 300 L1010 460 L930 700 L990 1000", "multi", t, w=40, dur=0.5)
    s.sfx("glitch", t, -4)
    t = S.w("atrapada")
    s.sello("atr", "ATRAPADA DEL OTRO LADO", 1380, 200, t, color="multi", rot=-4)
    t = S.w("María")
    s.text("ma", "SU MADRE… ¡VIVA!", "kw", "heroe", 1380, 420, t, size=84, rot=-3)
    t = S.w("no sabe quién es")
    s.globo("q", "¿QUIÉN ERES?", 1180, 560, 460, 180, t, size=52, rot=2)
    t = S.w("Bestia")
    s.img("bes", "lf/mv-bestia.jpg", 1060, 760, 760, 300, t, frm="B", pos="60% 40%", label="BESTIA")

    c = S.clip(0)
    s = S.scene(c["start"] - 0.35, bg="tinta", enter="cut")
    s.video("mama", c["src"], c["in"], c["start"], c["end"] - c["start"], 260, 120, 1400, 640, tag="POSCRÉDITOS · THE MARVELS", frm="B")
    s.video("bes2", "lf-c05-marvels-bestia.mp4", 0.2, c["end"] + 0.2, 3.0, 260, 120, 1400, 640, tag="BESTIA", slam=False)

    s = S.scene(S.w("Es decir"), bg="multi", enter="halftone", color="multi")
    t = S.w("mutantes existen")
    s.text("mut", "UN UNIVERSO CON MUTANTES", "kw", "amarillo", 960, 160, t, size=96, rot=-3)
    t = S.w("sinopsis oficial")
    s.svg("tres", "lf/tres-universos-sin-texto.svg", 960, 560, 1600, 900, t, how="pop")
    t = S.w("colisionan")
    s.svg("tres2", "lf/tres-universos.svg", 960, 560, 1600, 900, t, how="none")
    s.code(f'tl.fromTo(q("#{s.id("tres2")}"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {s.T(t)});')
    s.flash(t)
    s.zoom(t + 0.05)
    s.sfx("explosion", t, -3)
    s.sello("syn", "«UNIVERSES COLLIDE» · SINOPSIS OFICIAL", 960, 990, t + 0.4, color="tinta", rot=-2, size=44)

    s = S.scene(S.w("Y Disney"), bg="papel", enter="pageflip")
    t = S.w("compró Fox")
    s.img("dis", "a-disney.jpg", 120, 90, 380, 220, t, frm="L", pos="50% 50%")
    s.img("fox", "a-fox.jpg", 560, 90, 380, 220, t + 0.2, frm="L", pos="50% 50%")
    s.text("2019", "2019", "ttl", "rojo", 1220, 200, t + 0.3, size=150, rot=-4)
    cast = [("Patrick Stewart", "a-xavier.jpg", "XAVIER"), ("Ian McKellen", "a-magneto.jpg", "MAGNETO"), ("James Marsden", "a-ciclope.jpg", "CÍCLOPE"),
            ("Alan Cumming", "a-nightcrawler.jpg", "NIGHTCRAWLER"), ("Kelsey Grammer", "a-bestia.jpg", "BESTIA"), ("Rebecca Romijn", "a-mistica.jpg", "MÍSTICA"),
            ("Channing Tatum", "a-gambit.jpg", "GAMBITO")]
    for k, (w, f, lab) in enumerate(cast):
        t = S.w(w)
        s.img(f"x{k}", f, 40 + k * 266, 380, 250, 330, t, frm="B", pos="50% 20%", label=lab, rot=(-3, 2, -2, 3, -1, 2, -3)[k])
    t = S.w("Magneto")
    s.img("mag", "lf/tr-magneto.jpg", 360, 740, 640, 320, t, frm="L", pos="50% 35%", label="MAGNETO · TRÁILER")
    t = S.w("Thor")
    s.img("thor", "lf/tr-thor-rayo.jpg", 1040, 740, 420, 320, t, frm="R", pos="50% 40%")
    t = S.w("misma película")
    s.sello("mis", "LA MISMA PELÍCULA", 1640, 900, t, color="rojo", rot=-8)
