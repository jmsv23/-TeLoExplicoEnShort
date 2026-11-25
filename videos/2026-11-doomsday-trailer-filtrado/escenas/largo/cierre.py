"""CIERRE · ¿Real o falso?"""
from esc_largo._k import LFV, I, SV, tag


def build(S):
    s = S.scene(S.w("Es real"), bg="papel", enter="pageflip")
    s.svg("bal", SV + "balanza.svg", 960, 560, 1100, 688, s.start + 0.05, how="drop")
    t = S.w("dos versiones")
    s.globo("f1", "2 VERSIONES", 120, 120, 460, 160, t, size=52, rot=-3)
    t = S.w("repite el primer tráiler")
    s.globo("f2", "COPIA EL TRÁILER 1", 120, 320, 460, 160, t, size=46, rot=2)
    s.code(f'tl.to(q("#{s.id("bal")} [id$=brazo]"), {{ rotation: 8, transformOrigin: "800px 270px", duration: 0.6, ease: "back.out" }}, {s.T(t)});')
    t = S.w("acertaron")
    s.globo("r1", "ANTES ACERTARON", 1340, 120, 460, 160, t, size=46, rot=3)
    s.code(f'tl.to(q("#{s.id("bal")} [id$=brazo]"), {{ rotation: -4, transformOrigin: "800px 270px", duration: 0.6, ease: "back.out" }}, {s.T(t)});')
    t = S.w("veintitrés")
    s.text("fecha", "23-25 NOV", "ttl", "rojo", 1440, 880, t, size=120, rot=-4)
    tag(s, "R", t + 0.2)

    s = S.scene(S.w("Déjame"), bg="heroe", enter="ink")
    s.globo("cm", "¡COMENTA!", 1300, 560, 460, 180, s.start + 0.1, size=64, rot=4)
    t = S.w("real o falso")
    s.text("rf", "¿REAL O FALSO?", "ono", "amarillo", 960, 300, t, rot=-5, hold=2.0, zoom=True)
    t = S.w("aquí tienes")
    s.img("lf1", "lf/doomsday-poster.jpg", 560, 470, 800, 450, t, frm="B", pos="50% 40%", label="LO QUE DEBES SABER ANTES DE VER DOOMSDAY", rot=-1)
    t = S.w("Faltan treinta días")
    s.video("fecha", LFV + "lf-t08-fecha-17-dic.mp4", 0.2, t - 0.2, S.t1 - t + 0.2, 1380, 680, 480, 270, tag=None, rot=3)
    s.text("30", "FALTAN 30 DÍAS", "ttl", "amarillo", 960, 1000, t, size=90, rot=-3, misreg=True)
