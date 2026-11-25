"""CAPÍTULO 8 · REED CONTRA DOOM."""
from esc_largo._k import beat, capcard


def build(S):
    capcard(S, 8, "REED CONTRA DOOM", bg="doom")
    beat(S, "con todo lo que tienen", 221, fullscreen=True, ono="¡KA-BOOM!", oc="amarillo", sfx="explosion")
    beat(S, "destroza el Guantelete", 224, fullscreen=True)
    beat(S, "qué ganó", 230, txt="¿QUÉ GANASTE?", tc="papel")
    beat(S, "una distracción", 231, txt="ERA UNA DISTRACCIÓN", tc="amarillo", zoom=True, sfx="stinger")
    beat(S, "El verdadero plan", 228, txt="LLEGAR AL HOMBRE MOLÉCULA", tc="papel")
    beat(S, "intenta traicionarlo", 229, fullscreen=True)
    beat(S, "frente a frente", 274, fullscreen=True, pos="50% 35%", sfx="braam")
    beat(S, "casi todo su poder", 234, txt="PELEA JUSTA", tc="rojo")
    beat(S, "A puños", 235, fullscreen=True, ono="¡POW!", oc="amarillo", sfx="slam")
    beat(S, "entre las ruinas", 236, fullscreen=True, ono="¡THWAK!", oc="rojo")
    beat(S, "tú me robaste", 233, txt="«ME ROBASTE A MI FAMILIA»", tc="papel")
    beat(S, "la pregunta", 237, 4, bg="tinta", txt="«¿LO HABRÍAS HECHO MEJOR?»", tc="amarillo")
    beat(S, "Y Reed responde", 238, 1, bg="tinta", txt="«SÍ»", tc="papel", zoom=True)
    beat(S, "lo admite", 238, 2, bg="tinta", txt="«SÍ. MALDITO SEAS»", tc="rojo", sfx="stinger")
    beat(S, "toma el poder", 239, fullscreen=True, sfx="riser")
    s = beat(S, "desaparece", None, bg="papel", enter="cut")
    s.flash(s.start + 0.05)
    s.text("fin", "ADIÓS, BATTLEWORLD", "ttl", "tinta", 960, 540, s.start + 0.3, size=150, rot=-3)
    s.sfx("explosion", s.start, -2)
