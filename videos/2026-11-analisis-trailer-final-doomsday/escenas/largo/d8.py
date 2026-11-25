"""DETALLE 8 · «A mí, mis X-Men» + la polémica + robots con repulsores."""
from esc_largo._k import tag, tv, clipsc, still


def build(S):
    s = S.scene(S.w("Detalle ocho"), bg="doom", enter="ink", color="doom")
    still(s, "ej", "doom-ejercito", (110, 70, 1700, 940), s.start + 0.02, kb=S.clip(0)["start"], scale=1.12)
    t = S.w("ejército")
    s.text("ej2", "SU EJÉRCITO", "kw", "papel", 960, 900, t, size=90, rot=-3)

    clipsc(S, 0, bg="doom-osc")

    s = S.scene(S.w("Esta es la frase"), bg="tinta", enter="cut")
    tag(s, "C", s.start + 0.1)
    still(s, "cy", "ciclope", (60, 80, 1100, 920), s.start + 0.05, frm="L", pos="40% 30%")
    t = S.w("más famosa")
    s.text("mf", "LA FRASE MÁS FAMOSA", "kw", "amarillo", 1500, 140, t, size=64, rot=-3)
    t = S.w("serie animada")
    still(s, "gb", "gambito", (1200, 260, 640, 330), t - 0.4, frm="R", label="GÁMBITO")
    still(s, "ms", "mystique", (1200, 620, 640, 330), t + 0.2, frm="R", label="MYSTIQUE")
    t = S.w("la soltaron")
    s.text("sp", "¡EN EL TRÁILER!", "ono", "rojo", 620, 940, t, rot=-6)

    s = S.scene(S.w("Y aquí el fandom"), bg="papel", enter="pageflip")
    t = S.w("mejor momento")
    still(s, "ep0", "ciclope", (60, 160, 880, 600), t - 0.3, frm="L", pos="40% 40%")
    s.globo("ep", "¡ÉPICO!", 200, 120, 520, 180, t, size=80, rot=-4)
    t = S.w("robó")
    still(s, "sp0", "rayo-ciclope", (980, 160, 880, 600), t - 0.3, frm="R")
    s.globo("spo", "¡SPOILER!", 1200, 120, 520, 180, t, size=80, rot=4)
    t = S.w("de qué lado")
    s.text("lado", "¿DE QUÉ LADO ESTÁS?", "ttl", "rojo", 960, 960, t, size=100, rot=-3, zoom=True)
    t = S.w("comentarios")
    s.text("cm", "↓ COMENTA ↓", "kw", "amarillo", 1600, 860, t, size=60, rot=-4)

    s = S.scene(S.w("Y otro detalle"), bg="tinta", enter="cut")
    still(s, "rp", "robots-palmas", (110, 70, 1700, 940), s.start + 0.05, kb=S.peek("Así que"), frm="B", scale=1.15)
    t = S.w("no son Dumbots")
    s.text("nd", "NO SON DOOMBOTS", "kw", "papel", 960, 150, t, size=80, rot=-3)
    t = S.w("Centinelas")
    tag(s, "C", t)
    s.text("ce", "¡CENTINELAS!", "ono", "rojo", 960, 560, t, rot=-6, hold=1.2, zoom=True)
    t = S.w("cazadores de mutantes")
    s.text("cm", "CAZADORES DE MUTANTES", "kw", "amarillo", 960, 900, t, size=76, rot=-2)

    s = S.scene(S.w("Así que"), bg="doom", enter="ink", color="doom")
    still(s, "ej", "doom-ejercito", (80, 200, 1100, 700), s.start + 0.05, kb=S.t1, frm="L", scale=1.12)
    t = S.w("Vengadores tendrán")
    still(s, "gr", "grupo", (1220, 200, 620, 420), t, frm="R", label="VENGADORES")
    t = S.w("universo de los Equis Men")
    s.text("ux", "UNIVERSO X-MEN", "ttl", "amarillo", 1530, 720, t, size=90, rot=-4, misreg=True)
    t = S.w("usará a los Centinelas")
    s.text("cv", "CENTINELAS VS VENGADORES", "kw", "papel", 1500, 930, t, size=52, rot=-2)
    s.sfx("braam", t, -6)
