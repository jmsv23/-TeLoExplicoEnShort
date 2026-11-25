"""CAPÍTULO 6 · LA REBELIÓN."""
from esc_largo._k import beat, capcard


def build(S):
    capcard(S, 6, "LA REBELIÓN", bg="rojo")
    beat(S, "Un profeta", 180, txt="EL PROFETA", tc="amarillo")
    beat(S, "Es Maximus", 181, txt="EL PROFETA = MAXIMUS", tc="papel", zoom=True)
    beat(S, "abre una brecha", 184, fullscreen=True, sfx="rumble")
    beat(S, "Rey de los Muertos", 186, txt="EL REY DE LOS MUERTOS", tc="doom", sfx="braam")
    beat(S, "ejército de zombis", 187, fullscreen=True, ono="¡GRRR!", oc="doom")
    beat(S, "se traicionan", 190, txt="LOS BARONES SE TRAICIONAN", tc="rojo")
    beat(S, "Jane Foster", 194, txt="DOOM NO ES DIOS", tc="amarillo")
    beat(S, "Les mintió", 193, fullscreen=True)
    beat(S, "se dan vuelta", 267, fullscreen=True, ono="¡KRAKOOM!", oc="heroe", sfx="thunder")
    beat(S, "Maestro", 197, fullscreen=True, sfx="braam")
