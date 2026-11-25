"""CAPÍTULO 7 · LA GUERRA FINAL."""
from esc_largo._k import beat, capcard


def build(S):
    capcard(S, 7, "LA GUERRA FINAL", bg="rojo")
    beat(S, "guerra total", 198, fullscreen=True, ono="¡SMASH!", oc="doom", sfx="explosion")
    beat(S, "Un Hulk derriba", 200, txt="¡DERRIBADOS!", tc="rojo")
    beat(S, "se meten al castillo", 204, txt="REED SE INFILTRA", tc="papel")
    beat(S, "Ben Grimm despierta", 201, fullscreen=True, sfx="rumble")
    beat(S, "aplasta la nave", 205, ono="¡CRASH!", oc="amarillo", zoom=True)
    beat(S, "Franklin invoca", 203, fullscreen=True, sfx="braam")
    beat(S, "Ben mira a Franklin", 208, txt="EL NIÑO QUE VIO CRECER", tc="papel")
    beat(S, "se deja destruir", 208, fullscreen=True, kscale=1.15)
    beat(S, "Star Lord planta", 212, txt="UN PEDACITO DE GROOT", tc="doom")
    beat(S, "crece hasta destruir", 213, fullscreen=True, ono="¡YO SOY GROOT!", oc="doom", zoom=True, sfx="rumble")
    beat(S, "Valeria lleva a su madre", 214, txt="SUE VE LA VERDAD", tc="papel")
    beat(S, "Sue Storm se encuentra", 225, fullscreen=True)
    beat(S, "Thanos, por fin", 216, txt="«SOLO ERES UN HOMBRE»", tc="multi")
    beat(S, "la columna vertebral", 217, bg="tinta", ono="¡CRACK!", oc="rojo", zoom=True)
    beat(S, "un portal dorado", 220, fullscreen=True, kscale=1.15, sfx="riser")
    beat(S, "junto a Namor", 220, txt="BLACK PANTHER CON EL GUANTELETE", tc="amarillo")
