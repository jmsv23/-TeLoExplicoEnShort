"""DUELO 3 · Loki vs las brujas de Latveria (TEORÍA)."""
from esc_largo._k import tag, still, barra, vs, im

def build(S):
    s = vs(S, S.t0, "loki-cuernos", "LOKI", "lf/lf04/brujas", "LAS BRUJAS", 3, bg="multi", posa="50% 35%", posb="50% 40%")
    t = S.w("Magia contra magia")
    s.text("mm", "¡MAGIA VS MAGIA!", "ono", "amarillo", 960, 990, t, rot=-5)

    s = S.scene(S.w("Nadie sabe"), bg="multi-osc", enter="ink", color="multi")
    still(s, "br", "lf/lf04/doom-catedral", (110, 70, 1700, 620), s.start + 0.02, kb=S.peek("Y del otro"), scale=1.12)
    t = S.w("teoría más fuerte")
    tag(s, "T", t)
    t = S.w("Wanda")
    s.img("w", im("a-wanda"), 80, 720, 540, 330, t - 0.1, frm="L", label="¿WANDA?", pos="50% 30%")
    t = S.w("Clea")
    s.panel("c", '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;font:400 110px/1 Bangers;color:#FFD400">¿CLEA?<span style="font:700 30px/1.1 Comic Neue;color:#FFF3D6;margin-top:10px">hechicera de la Dimensión Oscura</span></div>', 690, 720, 540, 330, "multi", 0, t - 0.1, "B")
    t = S.w("Sylvie")
    s.img("sy", im("a-sylvie"), 1300, 720, 540, 330, t - 0.1, frm="R", label="¿SYLVIE?", pos="50% 25%")

    s = S.scene(S.w("Y del otro"), bg="multi", enter="whip", color="multi")
    still(s, "ar", "lf/arbol", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Si Doom"), scale=1.1)
    t = S.w("dios de las historias")
    s.text("dh", "EL DIOS DE LAS HISTORIAS", "ttl", "amarillo", 960, 150, t, size=110, rot=-3)
    t = S.w("todas las ramas")
    s.text("tr", "SOSTIENE TODAS LAS RAMAS", "kw", "papel", 960, 880, t, size=72, rot=-2)
    t = S.w("ComicBook")
    s.sello("n1", "AMENAZA N.º 1", 1500, 520, t + 0.4, color="multi", rot=-8, size=80)
    tag(s, "T", t + 0.6, x=1500, y=660, size=40)

    s = S.scene(S.w("Si Doom"), bg="doom", enter="ink", color="doom")
    still(s, "lk", "loki-trono", (80, 120, 860, 760), s.start + 0.02, frm="L", label="LOKI", pos="50% 40%")
    still(s, "dc", "lf/lf04/doom-catedral", (980, 120, 860, 760), s.start + 0.3, frm="R", label="DOOM")
    t = S.w("pasar por él")
    s.text("pp", "PRIMERO, LOKI", "ttl", "amarillo", 960, 960, t, size=100, rot=-3)
    t = S.w("necesita brujas")
    s.text("nb", "¡NECESITA BRUJAS!", "ono", "rojo", 960, 520, t, rot=-6, hold=1.2)
