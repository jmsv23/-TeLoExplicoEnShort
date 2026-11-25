"""EPÍLOGO · LO QUE VIENE DESPUÉS."""
from esc_largo._k import beat


def build(S):
    s = S.scene(S.t0, bg="papel", enter="pageflip")
    s.text("8m", "8 MESES DESPUÉS", "ttl", "tinta", 960, 540, S.t0 + 0.1, size=170, rot=-3, misreg=True)
    beat(S, "Miles Morales", 246, txt="TIERRA PRIME", tc="amarillo")
    beat(S, "Peter Parker", 248, fullscreen=True)
    beat(S, "Wakanda", 243, txt="WAKANDA MIRA A LAS ESTRELLAS", tc="papel")
    beat(S, "no se queda con él", 250, txt="REED NO SE QUEDA CON EL PODER", tc="amarillo")
    beat(S, "reconstruir el multiverso", 252, fullscreen=True, kscale=1.12, sfx="magic")
    beat(S, "Un universo a la vez", 253, txt="UN UNIVERSO A LA VEZ", tc="amarillo")
    beat(S, "se quita la máscara", 254, fullscreen=True)
    beat(S, "está curada", 255, fullscreen=True, kscale=1.18)
    s = beat(S, "Doom se ríe", 255, bg="tinta", txt="DOOM SE RÍE", tc="doom")
