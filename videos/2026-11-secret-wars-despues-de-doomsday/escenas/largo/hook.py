"""00 · HOOK."""
from esc_largo._k import SV, beat, tag, vin, full


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    s.img("dm", "lf/tr-doom-cerca.jpg", 0, 0, 1920, 1080, S.t0 + 0.02, frm="B", pos="50% 40%")
    s.kenburns("dm", S.t0, S.peek("Pero") , scale=1.15)
    t = S.w("van a perder")
    tag(s, "T", t)
    s.text("pe", "¿VAN A PERDER?", "kw", "rojo", 960, 950, t, size=96, rot=-3)
    t = S.w("increíble poder")
    s.text("po", "¡DOOM!", "ono", "doom", 1450, 400, t + 0.2, rot=-8, hold=1.0, zoom=True)

    s = S.scene(S.w("Pero"), bg="tinta", enter="cut")
    s.flash(s.start + 0.05)
    s.sfx("whoosh", s.start, -4)
    s.text("pr", "PERO…", "kw", "papel", 960, 540, s.start + 0.1, size=150, rot=-3, out=S.peek("después") - 0.3)
    t = S.w("después")
    s.text("yd", "¿Y DESPUÉS?", "ttl", "amarillo", 960, 540, t - 0.2, size=220, rot=-4, misreg=True, zoom=True)

    beat(S, "Porque Marvel", 1, 1, k="K", bg="doom", enter="ink", txt="SECRET WARS · 2015", sfx="pageflip")
    beat(S, "multiverso entero", 38, fullscreen=True, ono="¡FIN!", sfx="explosion")
    beat(S, "en Dios", 269, bg="doom", txt="DIOS EMPERADOR DOOM", tc="papel")
    beat(S, "los pocos héroes", 220, fullscreen=True, sfx="riser")

    s = S.scene(S.w("Te lo cuento"), bg="papel", enter="pageflip")
    s.svg("map", SV + "mapa-caps.svg", 960, 560, 1800, 1012, s.start + 0.05, how="pop")
    s.code(f'tl.from(qa("#{s.id("map")} [id*=cap]"), {{ scale: 0, opacity: 0, duration: 0.25, stagger: 0.12, ease: "back.out(2)", transformOrigin: "50% 50%" }}, {s.T(s.start + 0.1)});')
    t = S.w("Vamos")
    tag(s, "K", t - 0.4)
    s.text("go", "¡VAMOS!", "ono", "rojo", 1620, 950, t, rot=-6, hold=0.8)
