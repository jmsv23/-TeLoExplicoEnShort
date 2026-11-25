"""DUELO 4 · Xavier vs la Bruja Escarlata (TEORÍA) + PREGUNTA DE DEBATE."""
from esc_largo._k import tag, still, barra, vs, im

def build(S):
    s = vs(S, S.t0, "a-xavier", "PROFESOR X", "a-scarlet", "BRUJA ESCARLATA", 4, bg="multi", posb="50% 20%")
    t = S.w("entra la teoría")
    tag(s, "T", t, x=960, y=990, size=60)

    s = S.scene(S.w("Si Doom"), bg="multi-osc", enter="ink", color="multi")
    still(s, "wl", "lf/tr-wanda-llora", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("En los cómics"), scale=1.1)
    t = S.w("entrar en su cabeza")
    s.text("ec", "¿QUIÉN ENTRA EN SU CABEZA?", "kw", "amarillo", 960, 150, t, size=80, rot=-3)
    t = S.w("mente más poderosa")
    s.img("xv", im("a-xavier"), 1340, 520, 480, 480, t - 0.1, frm="R", label="LA MENTE Nº 1")

    s = S.scene(S.w("En los cómics"), bg="papel", enter="pageflip")
    tag(s, "K", s.start + 0.1)
    still(s, "hm", "house-of-m-portada", (1180, 80, 640, 940), s.start + 0.1, frm="R", pos="50% 30%", kb=S.peek("Magia del caos"), scale=1.06, alt="a-scarlet")
    t = S.w("intentó contenerla")
    s.text("ic", "XAVIER INTENTÓ CONTENERLA…", "kw", "heroe", 560, 380, t, size=64, rot=-2)
    t = S.w("no lo logró")
    s.text("nl", "¡Y NO PUDO!", "ono", "rojo", 560, 560, t, rot=-6)
    t = S.w("realidad entera")
    s.text("re", "REESCRIBIÓ LA REALIDAD", "ttl", "multi", 560, 800, t, size=90, rot=-3)

    s = S.scene(S.w("Magia del caos"), bg="papel", enter="halftone")
    barra(s, "b1", "WANDA", 10, "multi", 300, 260, 1320, s.start + 0.1)
    barra(s, "b2", "XAVIER", 8, "heroe", 300, 380, 1320, S.peek("telepatía"))
    t = S.w("gana Wanda")
    s.sello("gw", "EN EL PAPEL: WANDA", 960, 590, t, color="multi", rot=-7, size=80)
    t = S.w("despertarla")
    s.text("dp", "SOLO TIENE QUE DESPERTARLA", "ttl", "heroe", 960, 820, t, size=90, rot=-3, misreg=True)

    # pregunta de debate (la del comentario fijado)
    s = S.scene(S.w("Y aquí te pregunto"), bg="rojo", enter="whip", color="rojo")
    still(s, "sv", "sentry-vacio", (110, 70, 1700, 940), s.start + 0.02, kb=S.t1, scale=1.12, alt="a-thunder")
    t = S.w("lado equivocado")
    s.globo("q", "SI SENTRY SE VUELVE MALO… ¿QUIÉN LO DETIENE?", 260, 760, 1400, 220, t, size=62, rot=-2)
    t = S.w("comentarios")
    s.text("cm", "¡COMENTA!", "ono", "amarillo", 1500, 180, t, rot=-6)
