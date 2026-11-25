"""ACTO 4 · DOOM MUEVE SUS FICHAS."""
from lib_h import pho, L


def build(S):
    s = S.scene(S.t0, bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.cinta("acto", "ACTO 4", "tinta", top=110, rot=-4, at=s.start + 0.05)
    rec = [("a-samcap.jpg", "SAM"), ("a-thunder.jpg", "NUEVOS VENGADORES"), ("a-fantastic4.jpg", "TIERRA-828"), ("a-xavier.jpg", "X-MEN"), ("lf/sc-anillos.jpg", "ANILLOS")]
    for k, (f, lab) in enumerate(rec):
        s.img(f"r{k}", f, 90 + k * 356, 300, 320, 300, s.start + 0.3 + k * 0.08, frm="T", pos="50% 30%", label=lab, rot=(-3, 2, -2, 3, -1)[k])
    t = S.w("materiales de la película")
    s.text("doom", "DOOM MUEVE SUS FICHAS", "ttl", "amarillo", 960, 820, t, size=130, rot=-4, misreg=True, zoom=True)
    s.sfx("stinger", t, -6)
