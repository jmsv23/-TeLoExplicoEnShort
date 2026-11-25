"""CAPÍTULO 5 · EL SECRETO BAJO EL CASTILLO."""
from esc_largo._k import SV, beat, capcard, tag


def build(S):
    capcard(S, 5, "EL SECRETO BAJO EL CASTILLO", bg="ceniza")
    beat(S, "un funeral", 132, fullscreen=True)
    beat(S, "un cuarto escondido", 136, txt="UN CUARTO ESCONDIDO", tc="papel")
    beat(S, "Calvo", 137, txt="EL HOMBRE MOLÉCULA", tc="amarillo")

    s = S.scene(S.w("la fuente"), bg="tinta", enter="ink")
    tag(s, "K", s.start + 0.05)
    s.svg("en", SV + "energia.svg", 960, 540, 1920, 1080, s.start + 0.02, how="pop")
    s.code(f'tl.fromTo(q("#{s.id("en")} [id$=rayo]"), {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: 0.8, ease: "power1.inOut" }}, {s.T(s.start + 0.3)});')
    s.sfx("zap", s.start + 0.3, -4)
    t = S.w("deja de ser Dios")
    s.sello("cl", "LA CLAVE", 1500, 860, t, color="rojo", rot=-8, size=64)

    beat(S, "adivina quién", 162, txt="PETER Y MILES", tc="rojo")
    beat(S, "le dio de comer", 164, fullscreen=True, ono="¡ÑAM!", oc="amarillo")
    beat(S, "empieza a agrietarse", 155, txt="VALERIA DUDA", tc="papel", sfx="glitch")
    beat(S, "Los dos Reed", 159, txt="ALIANZA: REED + EL HACEDOR", tc="amarillo")
    beat(S, "Black Panther y Namor", 169, bg="tinta")
    beat(S, "Guantelete del Infinito", 171, txt="UN GUANTELETE QUE FUNCIONA", tc="amarillo", sfx="magic", zoom=True)
    beat(S, "llegó hasta el Escudo", 150, fullscreen=True)
    beat(S, "Es Ben Grimm", 176, txt="EL ESCUDO = LA COSA", tc="rojo", zoom=True, sfx="stinger")
    beat(S, "gigante de piedra", 177, fullscreen=True, kscale=1.12)
