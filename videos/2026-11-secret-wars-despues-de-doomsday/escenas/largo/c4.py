"""CAPÍTULO 4 · LOS QUE RECUERDAN."""
from esc_largo._k import beat, capcard


def build(S):
    capcard(S, 4, "LOS QUE RECUERDAN", bg="heroe")
    beat(S, "la de los villanos", 80, fullscreen=True, ono="¡CLANK!", oc="amarillo", sfx="slam")
    beat(S, "Thanos y su grupo", 83, txt="THANOS Y LA CÁBALA (CON NAMOR)", tc="multi")
    beat(S, "matar a un Thor", 79, fullscreen=True, sfx="explosion")
    beat(S, "Strange llega", 91, txt="STRANGE INVESTIGA", tc="papel")
    beat(S, "Miles Morales", 92, txt="MILES RECUERDA", tc="rojo", zoom=True)
    beat(S, "otra balsa", 101, txt="LA BALSA DE LOS HÉROES", tc="amarillo")
    beat(S, "dormidos durante", 103, fullscreen=True, kscale=1.12)
    beat(S, "Star Lord", 104, txt="8 AÑOS DORMIDOS", tc="amarillo")
    beat(S, "les cuenta la verdad", 105, txt="DOOM AHORA ES DIOS", tc="doom")
    beat(S, "Mientras tanto", 97, 4, bg="doom-osc", txt="LA CARA DETRÁS DE LA MÁSCARA", tc="papel")
    beat(S, "tiene miedo", 98, 4, fullscreen=True, kscale=1.15)
    beat(S, "Miedo de que", 98, bg="tinta", txt="ALGUIEN MEJOR QUE ÉL", tc="rojo")
    beat(S, "una proyección", 120, txt="REED ESTÁ VIVO", tc="rojo", zoom=True, sfx="stinger")
    beat(S, "Doom baja en persona", 122, fullscreen=True, sfx="braam")
    beat(S, "Thanos se ríe", 123, txt="THANOS SE RÍE", tc="multi")
    beat(S, "Cíclope", 125, fullscreen=True, ono="¡FÉNIX!", oc="amarillo", sfx="explosion")
    beat(S, "le rompe el cuello", 126, bg="tinta", ono="¡CRACK!", oc="rojo", zoom=True)
    beat(S, "Strange actúa", 127, txt="¡DISPERSIÓN!", tc="amarillo", sfx="magic")
    beat(S, "Doom no lo puede creer", 128, txt="LA MANO DERECHA LO TRAICIONA", tc="papel")
    beat(S, "le tiene miedo a Reed", 128, fullscreen=True, kscale=1.15)
    beat(S, "Y Doom lo mata", 129, fullscreen=True, sfx="explosion")
