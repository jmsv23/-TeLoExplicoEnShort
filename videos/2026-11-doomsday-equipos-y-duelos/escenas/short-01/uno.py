"""UNO · Stormbreaker en el pecho de Thanos (Infinity War)."""
from esc_short_01._k import tag, still

def build(S):
    s = S.scene(S.t0, bg="tinta", enter="whip")
    still(s, "it", "thor-stormbreaker-thanos", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.t1, pos="50% 50%", scale=1.15, frm="B", alt="lf/tr-thor-rayo")
    s.text("sb", "STORMBREAKER", "ttl", "amarillo", 540, 470, S.t0 + 0.1, size=130, rot=-4)
    t = S.w("en el pecho")
    s.text("ep", "¡EN EL PECHO DE THANOS!", "ono", "rojo", 540, 1400, t, size=104, rot=-5)
    t = S.w("guantelete completo")
    s.sello("gc", "CON EL GUANTELETE", 540, 1620, t, color="rojo", rot=-7, size=72)
    tag(s, "C", t + 0.2)
