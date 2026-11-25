"""ESCENA 7 · Millones de Doombots y la frase final (cierra el bucle con el clip «vidas robadas»)."""
from esc_largo._k import LFV, I, SV, tag


def build(S):
    s = S.scene(S.w("Escena siete"), bg="doom", enter="ink", color="doom", pat="pat-benday-fuerte")
    tag(s, "F", s.start + 0.1)
    t = S.w("Millones")
    t = min(t, s.start + 0.4)
    s.speed("sp", t, mode="radial", n=48, dur=1.2, color="#FFF3D6")
    for k, (x, y, w) in enumerate([(960, 560, 420), (560, 420, 260), (1360, 420, 260), (330, 300, 170), (1590, 300, 170),
                                   (760, 260, 150), (1160, 260, 150), (190, 600, 140), (1730, 600, 140)]):
        s.svg(f"db{k}", SV + "doombot.svg", x, y, w, int(w * 1.5), t + 0.08 * k, how="pop")
    s.text("fw", "¡FWOOOSH!", "ono", "amarillo", 960, 960, t + 0.3, rot=-5, hold=1.2)
    s.sfx("riser", t, -6)

    s = S.scene(S.w("En los cómics"), bg="papel", enter="halftone")
    tag(s, "K", s.start + 0.1)
    s.img("ej", I + "doombots-ejercito.jpg", 160, 90, 1600, 900, s.start + 0.05, frm="B", pos="50% 30%")
    s.kenburns("ej", s.start + 0.3, S.peek("Y la teoría"), scale=1.12)
    t = S.w("ejército personal")
    s.cap("su", "SU EJÉRCITO PERSONAL", t, left=60, top=60, width=640)

    s = S.scene(S.w("Y la teoría"), bg="heroe", enter="whip")
    tag(s, "T", s.start + 0.1)
    s.svg("map", SV + "mapa-ataque-616.svg", 760, 600, 1280, 720, s.start + 0.05, how="pop")
    t = S.w("Latveria")
    s.video("cent", LFV + "lf-t06-soy-doom-centinelas.mp4", 3.0, t - 0.1, 2.0, 1060, 120, 800, 450, tag="LATVERIA")
    t = S.w("seiscientos dieciséis")
    s.code("".join(f'COM.popIn(tl, q("#{s.id("map")} [id$=punto{k}]"), {s.T(t + 0.1 + k * 0.1)}, {{ rot: 0 }});' for k in range(1, 9)))
    t = S.w("cameos")
    s.text("cm", "¿CAMEOS?", "ono", "amarillo", 1500, 900, t, rot=-6, hold=0.9)

    s = S.scene(S.w("Después del título"), bg="tinta", enter="cut")
    t = S.w("contador")
    s.video("ct", LFV + "lf-t14-contador.mp4", 0.0, t - 0.2, S.peek("Algún día") - t + 0.3, 160, 90, 1600, 760, tag="TRÁILER OFICIAL")
    t = S.w("Algún día")
    s.svg("dm", "lf/doom-frente.svg", 1520, 620, 520, 676, t - 0.3, how="drop")
    s.globo("pd", "«ALGÚN DÍA ME PERDONARÁN…»", 200, 640, 1000, 230, t, size=58, rot=-2)
    s.sfx("heartbeat", t, -2)
    t = S.w("Perdonarlo")
    s.text("pq", "¿PERDONARLO POR QUÉ?", "kw", "amarillo", 960, 140, t, size=90, rot=-3, misreg=True)

    c = S.clip(0)
    s = S.scene(c["start"] - 0.35, bg="tinta", enter="ink")
    s.video("vr", c["src"], c["in"], c["start"], c["end"] - c["start"], 210, 110, 1500, 640, tag="TRÁILER OFICIAL", frm="B")
    s.cap("cap", "«VIDAS ROBADAS… TIENEN QUE DEVOLVERLAS»", c["start"] + 0.8, left=360, top=820, width=1200)

    s = S.scene(S.w("Doom no se ve"), bg="doom", enter="halftone", color="doom")
    tag(s, "T", s.start + 0.1)
    s.svg("mm", "lf/doom-mano-mascara.svg", 620, 560, 960, 800, s.start + 0.05, how="pop")
    t = S.w("salvar algo")
    s.text("sv", "SE CREE EL HÉROE", "kw", "amarillo", 1400, 300, t, size=96, rot=-4, misreg=True)
    t = S.w("destruir universos")
    s.text("du", "AUNQUE DESTRUYA UNIVERSOS", "kw", "papel", 1400, 560, t, size=66, rot=-3)
    t = S.w("pide perdón")
    s.cap("pp", "POR ESO PIDE PERDÓN", t, left=1060, top=820, width=760)
