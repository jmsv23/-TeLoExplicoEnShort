"""00 · HOOK + ADVERTENCIA."""
from lib_h import svgimg
from esc_largo._k import LFV, I, SV, tag


def build(S):
    # 1 · trono de Latveria + ¡FILTRADO!
    s = S.scene(S.t0, bg="tinta", enter="cut")
    s.video("trono", LFV + "lf-t01-latveria-victor-listo.mp4", 0.5, S.t0 + 0.02, S.peek("Pero ojo") - S.t0, 0, 0, 1920, 1080, slam=False)
    s.kenburns("trono", S.t0, S.peek("Pero ojo"), scale=1.12)
    t = S.w("filtró")
    s.svg("filt", SV + "sello-filtrado.svg", 960, 420, 900, 324, t, how="stamp", rot=-6)
    s.sfx("stamp", t + 0.1, -2)
    t = S.w("Avengers")
    s.raw(f'<div class="c" style="left:960px;top:780px"><div id="{s.id("logo")}">{svgimg("doomsday-logo.png", 760, 190, "filter:drop-shadow(8px 8px 0 #0B0B14)")}</div></div>')
    s.code(f'COM.popIn(tl, q("#{s.id("logo")}"), {s.T(t)}, {{ rot: -3 }});')
    s.sfx("braam", t, -6)

    # 2 · foro anónimo + cinta NO CONFIRMADO
    s = S.scene(S.w("Pero ojo"), bg="ceniza", enter="whip")
    s.svg("foro", SV + "foro-anonimo.svg", 960, 560, 1700, 956, s.start + 0.02, how="pop")
    s.kenburns("foro", s.start, S.peek("Si es real"), scale=1.06)
    t = S.w("no lo ha publicado")
    s.text("np", "MARVEL NO LO HA PUBLICADO", "kw", "rojo", 960, 120, t, size=78, rot=-3)
    t = S.w("Four chan")
    s.globo("4c", "VIENE DE FOUR CHAN", 1240, 300, 560, 170, t, rot=3, size=50)
    t = S.w("pinzas")
    s.text("pz", "¡CON PINZAS!", "ono", "amarillo", 960, 880, t, rot=-6, hold=1.0, zoom=True)

    # 3 · semáforo: qué es qué
    s = S.scene(S.w("Si es real"), bg="tinta", enter="cut")
    s.video("ruinas", LFV + "lf-t10-ciudad-ruinas.mp4", 0.0, s.start, S.peek("ejército") - s.start - 0.1, 160, 120, 1600, 760, tag="TRÁILER OFICIAL")
    t = S.w("universo entero")
    s.text("cae", "¡CAE UN UNIVERSO!", "ono", "rojo", 960, 900, t, rot=-5, hold=0.9)
    t = S.w("ejército")
    s.video("cent", LFV + "lf-t06-soy-doom-centinelas.mp4", 3.0, t - 0.1, S.peek("una frase") - t, 260, 140, 1400, 700, tag="TRÁILER", slam=False)
    s.text("mill", "MILLONES", "ttl", "amarillo", 960, 900, t + 0.3, size=160, rot=-4, misreg=True)
    t = S.w("una frase")
    s.img("cerca", "lf/tr-doom-cerca.jpg", 360, 140, 1200, 680, t - 0.1, frm="B", pos="50% 40%")
    s.globo("gl", "…", 1300, 120, 360, 200, t + 0.3, size=110, rot=4)

    s = S.scene(S.w("Te cuento"), bg="papel", enter="pageflip")
    s.svg("sem", SV + "semaforo.svg", 960, 260, 1120, 380, s.start + 0.05, how="drop")
    t = S.w("filtración")
    tag(s, "F", t)
    t = S.w("sabemos")
    s.svg("mapa", SV + "mapa-escenas.svg", 960, 720, 960, 540, t - 0.2, how="pop")
    t = S.w("Vamos")
    s.text("go", "¡VAMOS!", "ono", "rojo", 1500, 900, t, rot=-6, hold=0.8)
