"""CAPÍTULO 2 · DOOM SE VUELVE DIOS."""
from esc_largo._k import SV, beat, capcard, tag


def build(S):
    capcard(S, 2, "DOOM SE VUELVE DIOS", bg="doom")
    beat(S, "Doom no estaba ahí", 4, txt="DOOM ESTABA EN OTRO LUGAR", tc="doom")
    beat(S, "unos seres llamados", 6, bg="tinta", txt="LOS BEYONDERS", tc="amarillo", sfx="braam")
    beat(S, "Los creadores", 140, txt="LOS CREADORES… Y DESTRUCTORES", tc="papel")
    beat(S, "el Hombre Molécula", 138, bg="ceniza", txt="EL HOMBRE MOLÉCULA = LA BOMBA", tc="rojo")
    beat(S, "hizo lo impensable", 141, fullscreen=True, sfx="riser")
    beat(S, "una sola bomba", 142, ono="¡BOOM!", oc="rojo", zoom=True, sfx="explosion")
    beat(S, "se quedó con su poder", 143, bg="doom", txt="TODO SU PODER", tc="amarillo", zoom=True)

    s = S.scene(S.w("los pedazos"), bg="multi-osc", enter="ink")
    tag(s, "K", s.start + 0.05)
    s.svg("bw", SV + "battleworld.svg", 960, 540, 1920, 1080, s.start + 0.05, how="pop")
    s.code(f'tl.from(qa("#{s.id("bw")} .dom"), {{ opacity: 0, scale: 0.6, duration: 0.3, stagger: 0.18, transformOrigin: "960px 560px", ease: "back.out(1.6)" }}, {s.T(s.start + 0.1)});')
    s.code(f'tl.from(q("#{s.id("bw")} [id$=titulo]"), {{ opacity: 0, y: 60, duration: 0.3 }}, {s.T(S.peek("solo planeta"))});')
    s.sfx("magic", s.start + 0.2, -6)
    s.kenburns("bw", s.start, s.start + 9, scale=1.06)

    beat(S, "nunca hubo otra cosa", 266, fullscreen=True, pos="50% 30%")
    beat(S, "Doom creó el mundo", 269, bg="doom", txt="DIOS EMPERADOR DOOM", tc="papel", zoom=True, sfx="braam")
