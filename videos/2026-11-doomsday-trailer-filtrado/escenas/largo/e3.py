"""ESCENA 3 · Cíclope contra Doom."""
from esc_largo._k import LFV, I, SV, tag


def build(S):
    s = S.scene(S.w("Escena tres"), bg="tinta", enter="cut")
    tag(s, "F", s.start + 0.1)
    t = S.w("Cíclope")
    s.video("cic", LFV + "lf-t11-ciclope-rayo.mp4", 0.0, t - 0.1, S.peek("Y Doom responde") - t + 0.1, 160, 130, 1600, 760, tag="TRÁILER OFICIAL")
    t = S.w("rayo óptico")
    s.draw("rayo", "M820 420 L1900 300", "rojo", t, w=60, dur=0.25)
    s.text("zap", "¡ZAAAP!", "ono", "rojo", 1400, 860, t + 0.1, rot=-6, hold=0.8)
    s.sfx("explosion", t, -6)

    s = S.scene(S.w("Y Doom responde"), bg="doom", enter="whip", color="doom")
    s.video("rayo", LFV + "lf-t11-ciclope-rayo.mp4", 1.3, s.start + 0.05, 2.0, 160, 130, 1600, 760, tag="TRÁILER", slam=False)
    t = S.w("casi mata")
    s.slab("r", "rojo", t - 0.05, t + 1.0)
    s.text("casi", "¡CASI!", "ono", "papel", 960, 540, t, rot=-8, hold=0.9, zoom=True)
    s.sfx("braam", t, -4)

    s = S.scene(S.w("Estos son"), bg="papel", enter="halftone")
    tag(s, "C", s.start + 0.1)
    for k, (f, n) in enumerate([("a-ciclope.jpg", "CÍCLOPE"), ("a-xavier.jpg", "XAVIER"), ("a-magneto.jpg", "MAGNETO"),
                                ("a-bestia.jpg", "BESTIA"), ("a-nightcrawler.jpg", "NIGHTCRAWLER")]):
        s.img(f"x{k}", f, 40 + k * 372, 140, 350, 420, s.start + 0.15 + k * 0.12, frm="T", label=n, rot=(-2, 2, -1, 2, -2)[k])
    t = S.w("Fox")
    s.svg("fox", "a-fox.jpg", 960, 620, 220, 100, t, how="pop")
    t = S.w("rumores")
    tag(s, "R", t)
    t = S.w("Tormenta")
    s.img("tor", I + "tormenta-fox.jpg", 330, 620, 520, 400, t, frm="B", pos="50% 30%", label="TORMENTA")
    t = S.w("Jean Grey")
    s.img("jg", I + "jean-grey-fox.webp", 1070, 620, 520, 400, t, frm="B", pos="60% 30%", label="JEAN GREY")
    t = S.w("aparecen")
    s.svg("de", SV + "sello-donde-estan.svg", 960, 820, 700, 252, t + 0.2, how="stamp", rot=-5)

    s = S.scene(S.w("Porque ese universo"), bg="multi", enter="ink", color="multi")
    tag(s, "T", s.start + 0.1)
    s.svg("u", "lf/tres-universos.svg", 960, 540, 1600, 900, s.start + 0.05, how="pop")
    t = S.w("sacrificado")
    s.text("sac", "¿SE SACRIFICARON?", "kw", "amarillo", 960, 980, t, size=84, rot=-3)

    s = S.scene(S.w("Si la primera pelea"), bg="rojo", enter="halftone", color="rojo")
    s.img("cc", I + "ciclope.jpg", 180, 120, 1100, 640, s.start + 0.05, frm="L", pos="55% 50%", rot=-2)
    t = S.w("más dura")
    s.text("md", "LA MÁS DURA", "ttl", "amarillo", 1500, 380, t, size=110, rot=-4)
    t = S.w("Por fin")
    s.cap("pf", "POR FIN, CÍCLOPE", t, left=1140, top=820, width=640)
