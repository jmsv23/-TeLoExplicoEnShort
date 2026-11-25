"""TRES · rayos dorados = Fuerza Odín (TEORÍA)."""
from esc_short_01._k import tag, still

def build(S):
    s = S.scene(S.t0, bg="tinta", enter="whip")
    still(s, "td", "lf/lf04/thor-dorado-bosque", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.peek("La teoría"), pos="50% 45%", frm="B")
    t = S.w("tráiler final")
    tag(s, "C", t)
    t = S.w("rayos dorados")
    s.text("rd", "¡RAYOS DORADOS!", "ono", "amarillo", 540, 1450, t, size=104, rot=-6)
    s = S.scene(S.w("La teoría"), bg="multi", enter="cut", color="multi")
    still(s, "td2", "lf/lf04/thor-dorado", (0, 0, 1080, 1920), s.start + 0.02, kb=S.t1, pos="50% 40%", frm="B", scale=1.18)
    tag(s, "T", s.start + 0.1)
    t = S.w("Fuerza Odín")
    s.text("fo", "LA FUERZA ODÍN", "ttl", "amarillo", 540, 1400, t, size=130, rot=-4, misreg=True)
    t = S.w("no la ha visto")
    s.text("nv", "…Y DOOM NO LA HA VISTO", "kw", "papel", 540, 1620, t, size=66, rot=-2)
