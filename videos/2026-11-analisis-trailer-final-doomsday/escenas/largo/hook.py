"""00 · HOOK: la tesis (culpa de Steve) + clip «consecuencias» + promesa de detalles y marcador de la filtración."""
from lib_h import svgimg
from esc_largo._k import TR, I, tag, tv, clipsc, still


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    still(s, "doom", "doom-catedral", (0, 0, 1920, 1080), S.t0 + 0.02, kb=S.peek("Según"), frm="B", scale=1.1)
    t = S.w("villano")
    s.text("vil", "EL VILLANO…", "kw", "papel", 960, 140, t, size=96, rot=-3)
    t = S.w("no es solo Doom")
    s.text("nod", "¿NO ES SOLO DOOM?", "ono", "amarillo", 960, 900, t, rot=-5, hold=1.0)
    s = S.scene(S.w("Según"), bg="papel", enter="whip")
    still(s, "stv", "steve-barba", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], frm="L", scale=1.15, pos="50% 30%")
    t = S.w("tráiler final")
    tag(s, "C", t)
    t = S.w("decisión")
    s.sello("culpa", "¡FUE SU CULPA!", 1350, 820, t + 0.4, color="rojo", rot=-8, size=88)
    s.sfx("braam", t, -6)

    s, c = clipsc(S, 0, cap="«…TENDRÍAN CONSECUENCIAS»", cap_at=1.6)

    s = S.scene(S.w("Marvel por fin"), bg="doom", enter="ink", color="doom")
    tv(s, "tit", 162.8, s.start + 0.05, S.peek("Y trae") - s.start, (160, 120, 1600, 840), tag_txt="ÚLTIMO TRÁILER", slam=False)
    t = S.w("último tráiler")
    s.text("ult", "¡EL ÚLTIMO!", "ono", "amarillo", 960, 940, t, rot=-5)
    # ráfaga de 4 viñetas
    s = S.scene(S.w("Y trae"), bg="papel", enter="pageflip")
    t = S.w("hijo")
    still(s, "h", "hijo", (80, 80, 860, 440), t - 0.1, frm="L", label="SU HIJO", pos="50% 35%")
    t = S.w("pelea")
    still(s, "p", "cyclops-sam", (980, 80, 860, 440), t - 0.1, frm="R", label="VENGADORES VS EQUIS MEN".replace("EQUIS ", "X-"))
    t = S.w("Miólnir")
    still(s, "m", "steve-mjolnir", (80, 560, 860, 440), t - 0.1, frm="L", label="¿EL MJOLNIR?", pos="45% 50%")
    t = S.w("último plano")
    still(s, "c", "castillo-ny", (980, 560, 860, 440), t - 0.1, frm="R", label="???")
    t = S.w("nadie notó")
    s.text("q", "?", "ttl", "rojo", 1410, 780, t, size=300, rot=8)

    s = S.scene(S.w("Además"), bg="tinta", enter="cut")
    s.img("lf2", "lf/doomsday-poster.jpg", 260, 150, 760, 520, s.start + 0.05, frm="L", pos="50% 40%", label="LA FILTRACIÓN", rot=-2)
    t = S.w("filtración")
    s.svg("sf", SV_FILT, 640, 420, 620, 224, t, how="stamp", rot=-8)
    t = S.w("cuánto acertó")
    s.text("sc", "? / 13", "ttl", "amarillo", 1420, 420, t, size=220, rot=-4, misreg=True)
    t = S.w("detalle por detalle")
    s.text("dd", "10 DETALLES", "kw", "rojo", 960, 900, t, size=110, rot=-3, zoom=True)


SV_FILT = "lf/lf02-sello-filtrado.svg"
