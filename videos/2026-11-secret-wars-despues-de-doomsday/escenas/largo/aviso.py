"""AVISO: historia del cómic."""
from esc_largo._k import tag


def build(S):
    s = S.scene(S.t0, bg="papel", enter="halftone")
    s.text("av", "UN AVISO RÁPIDO", "kw", "tinta", 960, 130, S.t0 + 0.05, size=70, rot=-2)
    t = S.w("historia del cómic")
    s.text("hc", "LA HISTORIA DEL CÓMIC", "kw", "rojo", 960, 300, t, size=100, rot=-3)
    t = S.w("Jonathan")
    s.text("hk", "HICKMAN · RIBIĆ", "ttl", "tinta", 960, 520, t, size=130, rot=-2)
    t = S.w("puede cambiar")
    s.globo("pc", "LA PELÍCULA PUEDE CAMBIAR", 560, 700, 800, 170, t, size=50, rot=2)
    t = S.w("confirmado")
    tag(s, "K", S.t0 + 0.1)
    s.sello("c", "CONFIRMADO", 560, 920, t, color="heroe", rot=-6, size=52)
    t = S.w("teoría")
    s.sello("tt", "TEORÍA", 1360, 920, t, color="multi", rot=5, size=52)
