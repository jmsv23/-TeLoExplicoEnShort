"""DATO 15 · El motivo de Doom (cierra el bucle del hook)."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato quince"), bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 15", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("prometí")
    s.sello("pr", "LO QUE TE PROMETÍ", 480, 420, t, color="tinta", rot=-5)
    t = S.w("Por qué Doom")
    s.svg("doom", "lf/doom-espaldas.svg", 1240, 540, 1280, 720, t, how="pop")
    t = S.w("monstruo")
    s.text("mon", "¿NO SIEMPRE FUE UN MONSTRUO?", "kw", "papel", 960, 980, t, size=76, rot=-3)

    c = S.clip(0)
    s = S.scene(c["start"] - 0.35, bg="tinta", enter="cut")
    s.video("am", c["src"], c["in"], c["start"], c["end"] - c["start"], 260, 140, 1400, 620, tag="TRÁILER", frm="B")
    s.cap("cap", "«ANTES ERA AMABLE Y AFECTUOSO»", c["start"] + 0.6, left=520, top=820, width=900)

    s = S.scene(S.w("Y luego Doom"), bg="doom", enter="halftone", color="doom")
    s.com("doom", "doom", 960, 560, 560, 694, s.start + 0.05, how="drop")
    t = S.w("Fíjate bien")
    s.text("fij", "¡FÍJATE BIEN!", "ono", "amarillo", 960, 920, t, rot=-5, hold=1.0)
    s.sfx("riser", t, -6)

    c0, c1 = S.clip(1), S.clip(2)
    s = S.scene(c0["start"] - 0.35, bg="tinta", enter="cut")
    s.video("viv", c0["src"], c0["in"], c0["start"], c0["end"] - c0["start"], 260, 140, 1400, 620, tag="TRÁILER", frm="B")
    s.video("bebe", c1["src"], c1["in"], c1["start"], c1["end"] - c1["start"], 260, 140, 1400, 620, tag="TRÁILER", slam=False)
    s.zoom(c1["start"] + 0.3, amt=1.22)
    s.flash(c1["start"] + 0.3)
    s.text("st", "¿STEVE?", "ono", "amarillo", 1500, 860, c1["start"] + 0.6, rot=6, hold=2.5, sfx=False)
    s.cap("vr", "«VIDAS ROBADAS… TIENEN QUE DEVOLVERLAS»", c1["start"] + 4.8, left=420, top=830, width=1100)

    s = S.scene(S.w("Steve Rogers"), bg="heroe", enter="ink")
    s.img("sb", "lf/tr-steve-bebe.jpg", 100, 90, 1000, 620, s.start + 0.05, frm="L", pos="50% 35%", label="STEVE ROGERS · CON UN BEBÉ")
    t = S.w("la teoría")
    s.sello("teo", "TEORÍA", 1500, 220, t, color="rojo", rot=-8, size=80)
    t = S.w("responsable")
    s.text("resp", "¿STEVE ES EL RESPONSABLE?", "kw", "amarillo", 1460, 480, t, size=64, rot=-4)
    t = S.w("Peggy")
    s.panel("pg", svgimg("lf/mini-comic-steve.svg", 660, 286), 1160, 640, 700, 330, "papel", 2, t, "R")
    t = S.w("No está confirmado")
    s.sello("nc", "NO CONFIRMADO", 600, 900, t, color="tinta", rot=-4)

    s = S.scene(S.w("Pero dejaría"), bg="doom", enter="halftone", color="doom")
    t = S.w("conquistar el mundo")
    s.com("doom", "doom", 520, 560, 520, 645, t, how="drop")
    s.draw("tach", "M820 300 L1700 330", "rojo", S.peek("Querría recuperar"), w=28, dur=0.3)
    s.text("conq", "CONQUISTAR EL MUNDO", "kw", "papel", 1260, 300, t + 0.1, size=84, rot=-2)
    t = S.w("Querría recuperar")
    s.text("rec", "RECUPERAR LO QUE LE ROBARON", "kw", "amarillo", 1260, 560, t, size=76, rot=-3, misreg=True)
    t = S.w("golpe duro")
    s.img("cap", "lf/tr-steve-cerca.jpg", 1000, 700, 640, 340, t, frm="B", pos="50% 30%")
    t = S.w("error más grande")
    s.sello("err", "¿EL ERROR MÁS GRANDE DE SU VIDA?", 960, 1000, t, color="rojo", rot=-3, size=44)

    s = S.scene(S.w("Y todo se une"), bg="tinta", enter="ink")
    items = [("pasado cambiado", "lf/tr-steve-bebe.jpg", "PASADO CAMBIADO"), ("multiverso roto", "lf/incursion.jpg", "MULTIVERSO ROTO"),
             ("Loki sosteniendo", "lf/arbol.jpg", "LOKI SOSTIENE"), ("un hombre", "lf/tr-doom-cerca.jpg", "UN HOMBRE…")]
    for k, (w, f, lab) in enumerate(items):
        t = S.w(w)
        s.img(f"u{k}", f, 60 + k * 462, 200, 430, 560, t, frm="T", pos="50% 35%", label=lab, rot=(-3, 2, -2, 3)[k])
    t = S.w("que cree que es suyo")
    s.text("suyo", "…QUE QUIERE LO QUE CREE SUYO", "kw", "doom", 960, 900, t, size=80, rot=-3, misreg=True, zoom=True)
    s.sfx("braam", t, -4)
