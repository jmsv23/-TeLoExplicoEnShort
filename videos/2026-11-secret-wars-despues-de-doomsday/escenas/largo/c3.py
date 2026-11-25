"""CAPÍTULO 3 · BIENVENIDOS A BATTLEWORLD."""
from esc_largo._k import SV, beat, capcard, tag


def build(S):
    capcard(S, 3, "BIENVENIDOS A BATTLEWORLD", bg="multi")

    s = S.scene(S.w("Cada región"), bg="multi-osc", enter="ink")
    tag(s, "K", s.start + 0.05)
    s.svg("bw", SV + "battleworld.svg", 960, 540, 1920, 1080, s.start + 0.02, how="pop")
    for k, w in enumerate(["Era de Apocalipsis", "zombis", "Ultrón"]):
        t = S.w(w)
        s.code(f'COM.pulse(tl, q("#{s.id("bw")} [id$=dom{[1, 0, 2][k]}]"), {s.T(t)}, {{ to: 1.08 }});')
        s.sfx("pop", t, -8)
    s.kenburns("bw", s.start, s.start + 8, scale=1.1)
    t = S.w("un Barón")
    s.text("ba", "UN BARÓN POR REINO", "kw", "amarillo", 960, 980, t, size=70, rot=-2)

    beat(S, "La policía", 44, txt="EL CUERPO DE THORS", tc="amarillo", ono="¡KRAKOOM!", oc="heroe", sfx="thunder")
    beat(S, "su martillo", 192, fullscreen=True)
    beat(S, "Doctor Strange", 88, txt="SHERIFF STRANGE", tc="papel")
    beat(S, "el Escudo", 72, txt="EL ESCUDO", tc="rojo", sfx="rumble")
    beat(S, "Zombis", 74, fullscreen=True, ono="¡ZOMBIS!", oc="doom")
    beat(S, "Antorcha Humana", 96, 4, bg="tinta", txt="SÍ: ES EL SOL", tc="amarillo")
    beat(S, "Literalmente", 96, 5, fullscreen=True, ono="¡LITERAL!", oc="amarillo", zoom=True)

    s = S.scene(S.w("Pero lo más perturbador"), bg="tinta", enter="cut")
    t = S.w("su familia")
    s.text("fa", "SU FAMILIA", "ttl", "rojo", 960, 540, t, size=180, rot=-3, misreg=True)

    beat(S, "Doom vive en su castillo", 172, txt="LA FAMILIA ROBADA", tc="rojo")
    beat(S, "Franklin y Valeria", 174, fullscreen=True, kscale=1.12)
    beat(S, "Ninguno recuerda", 173, txt="NO RECUERDAN OTRA VIDA", tc="papel")
    beat(S, "la venganza perfecta", 95, bg="doom-osc", txt="LA VENGANZA PERFECTA", tc="doom")
    beat(S, "algo enterrado", 52, fullscreen=True, sfx="riser")
    beat(S, "más viejo", 69, txt="MÁS VIEJO QUE EL MUNDO", tc="amarillo", zoom=True)
