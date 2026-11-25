"""DETALLE 4 · Doom, las brujas y las «vidas robadas» (abre el bucle 1)."""
from esc_largo._k import tag, tv, clipsc, still, SV


def build(S):
    s = S.scene(S.w("Detalle cuatro"), bg="doom", enter="ink", color="doom")
    still(s, "dm", "doom-catedral", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Mucha gente"), scale=1.15, frm="B")
    t = S.w("Latveria")
    s.text("lt", "LATVERIA", "ttl", "amarillo", 960, 140, t, size=140, rot=-4, misreg=True)
    t = S.w("tres figuras")
    still(s, "bj0", "brujas", (1100, 520, 700, 420), t - 0.1, frm="R", label="3 FIGURAS")

    s = S.scene(S.w("Mucha gente"), bg="multi", enter="halftone", color="multi")
    tag(s, "T", s.start + 0.1)
    still(s, "br", "brujas", (110, 70, 1700, 940), s.start + 0.05, kb=S.peek("Y luego Doom"), scale=1.18)
    t = S.w("brujas")
    s.text("bj", "¿LAS BRUJAS DE LATVERIA?", "kw", "amarillo", 960, 140, t, size=78, rot=-3)
    t = S.w("Wanda")
    s.img("wa", "a-scarlet.jpg", 1400, 520, 400, 440, t, frm="R", label="¿WANDA?")
    t = S.w("Cómic Con")
    s.globo("cc", "SE VIO EN LA COMIC-CON", 160, 780, 640, 170, t, size=48, rot=-2)

    s = S.scene(S.w("Y luego Doom"), bg="tinta", enter="cut")
    still(s, "dc", "doom-rayos", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], scale=1.1)
    t = S.w("define la película")
    s.text("df", "LA FRASE CLAVE", "kw", "rojo", 960, 900, t, size=90, rot=-3)

    clipsc(S, 0, bg="doom-osc")

    s = S.scene(S.w("Vidas robadas.", again=True), bg="doom", enter="ink", color="doom")
    t = s.start
    s.text("vr", "VIDAS ROBADAS", "ttl", "papel", 960, 300, t + 0.05, size=170, rot=-4, misreg=True)
    s.sfx("braam", t, -5)
    still(s, "cm", "steve-peggy-porche", (460, 460, 1000, 520), s.start + 0.3, frm="B", label="¿UNA VIDA ROBADA?")
    t = S.w("Steve vive")
    t = S.w("Guarda esa frase")
    s.sello("gu", "🔁 GUÁRDALA", 1600, 900, t, color="rojo", rot=-8, size=60)
