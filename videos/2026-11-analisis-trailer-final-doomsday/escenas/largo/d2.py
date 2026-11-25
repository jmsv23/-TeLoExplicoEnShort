"""DETALLE 2 · Los 4 Fantásticos tocan la puerta + «Éramos seis»."""
from esc_largo._k import I, tag, tv, clipsc, still


def build(S):
    s = S.scene(S.w("Detalle dos"), bg="tinta", enter="ink")
    still(s, "jar", "4f-jardin", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], scale=1.15)
    t = S.w("nave aterriza")
    s.text("vr", "¡VRRRMMM!", "ono", "amarillo", 1450, 200, t, rot=-6)
    t = S.w("Cuatro Fantásticos")
    s.text("4f", "LOS 4 FANTÁSTICOS", "ttl", "amarillo", 960, 900, t, size=120, rot=-4)
    tag(s, "C", t)

    clipsc(S, 0)

    s = S.scene(S.w("Y luego viene"), bg="papel", enter="pageflip")
    still(s, "rs", "reed-sue", (80, 120, 860, 520), s.start + 0.05, frm="L")
    t = S.w("más emotiva")
    s.text("em", "LA MÁS EMOTIVA", "kw", "rojo", 960, 80, t, size=70, rot=-2)
    t = S.w("chimenea")
    still(s, "jb", "johnny-ben", (980, 120, 860, 520), t - 0.2, frm="R")
    t = S.w("el hijo")
    still(s, "sa", "sala", (340, 600, 1240, 440), t - 0.1, frm="B", label="EL HIJO LOS VE")

    clipsc(S, 1)

    s = S.scene(S.w("Éramos seis.", again=True), bg="tinta", enter="cut")
    t = s.start
    cards = [("av-cap", "CAP"), ("av-ironman", "IRON MAN"), ("av-thor", "THOR"), ("av-hulk", "HULK"),
             ("av-viuda", "VIUDA NEGRA"), ("av-ojo", "OJO DE HALCÓN")]
    for k, (f, n) in enumerate(cards):
        s.img(f"v{k}", I + f + ".jpg", 75 + k * 300, 270, 270, 400, t + 0.12 * k, frm="B", pos="50% 20%",
              label=n, rot=(-2 if k % 2 else 2))
    t = S.w("en pasado")
    s.text("pa", "EN PASADO", "kw", "amarillo", 960, 160, t, size=90, rot=-3)
    t = S.w("Tony")
    s.code(f'tl.to(q("#{s.id("v1")}"), {{ filter: "grayscale(1) brightness(.45)", duration: 0.6 }}, {s.T(t)});')
    s.text("tn", "TONY YA NO ESTÁ", "kw", "papel", 960, 900, t + 0.2, size=80, rot=-2)
    s.sfx("heartbeat", t, -4)
