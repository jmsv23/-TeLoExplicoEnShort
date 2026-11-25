"""DATO 12 · El misterio de los diez anillos."""
from lib_h import pho, ph, svgimg, L


def rings(w=620):
    g = "".join(f'<circle cx="{150 + (k % 5) * 80}" cy="{120 + (k // 5) * 110}" r="34" fill="none" stroke="#0B0B14" stroke-width="22"/>'
                f'<circle cx="{150 + (k % 5) * 80}" cy="{120 + (k // 5) * 110}" r="34" fill="none" stroke="#F28C28" stroke-width="12"/>' for k in range(10))
    return L.svgbox("0 0 620 300", g, w, int(w * 300 / 620))


def build(S):
    s = S.scene(S.w("Dato doce"), bg="tinta", enter="ink")
    s.text("d", "DATO 12", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("misterio")
    s.text("mis", "UN MISTERIO SIN RESOLVER", "kw", "papel", 520, 560, t, size=80, rot=-4)
    t = S.w("Shang Chi")
    s.phpanel("sc", "N-17", "Shang-Chi y Wenwu", "still o póster de Shang-Chi", 1000, 120, 820, 560, t, frm="R", label="SHANG-CHI")
    t = S.w("diez anillos")
    s.obj("r", rings(640), 1400, 860, t)
    t = S.w("mil años")
    s.text("1000", "1000 AÑOS", "ttl", "amarillo", 520, 820, t, size=130, rot=-4)

    s = S.scene(S.w("Al final"), bg="papel", enter="pageflip")
    t = S.w("se sacrifica")
    s.text("sac", "SE SACRIFICA", "kw", "rojo", 560, 200, t, size=100, rot=-4)
    t = S.w("le pasa los anillos")
    s.obj("r2", rings(760), 560, 560, t)
    t = S.w("Wong")
    s.img("ring", "lf/sc-anillos.jpg", 1060, 120, 760, 460, t, frm="R", pos="50% 40%", label="POSCRÉDITOS")
    t = S.w("Bruce Banner")
    s.img("bru", "a-bruce.jpg", 1060, 620, 360, 400, t, frm="B", pos="50% 20%", label="BANNER")
    t = S.w("Capitana Marvel")
    s.phpanel("car", "N-93", "Capitana Marvel", "retrato de Brie Larson", 1460, 620, 360, 400, t, frm="B", label="CAROL")
    t = S.w("más antiguos")
    s.sello("ant", "MÁS ANTIGUOS DE LO QUE CREÍAN", 600, 940, t, color="tinta", rot=-3, size=44)

    c0, c1 = S.clip(0), S.clip(1)
    s = S.scene(c0["start"] - 0.35, bg="tinta", enter="cut")
    s.video("v1", c0["src"], c0["in"], c0["start"], c0["end"] - c0["start"], 260, 120, 1400, 640, tag="POSCRÉDITOS · SHANG-CHI", frm="B")
    s.video("v2", c1["src"], c1["in"], c1["start"], c1["end"] - c1["start"], 260, 120, 1400, 640, tag="«¿A DÓNDE?»", slam=False)

    s = S.scene(S.w("Los anillos emiten"), bg="multi", enter="halftone", color="multi")
    s.obj("r3", rings(560), 420, 560, s.start + 0.05)
    s.draw("sig", "M700 560 C900 420 1100 700 1300 520", "amarillo", s.start + 0.3, w=20, dur=0.6)
    s.text("q", "?", "ttl", "amarillo", 1500, 520, s.start + 0.8, size=420, rot=8)
    s.sfx("zap", s.start + 0.3, -6)
    t = S.w("Cinco años")
    s.text("5", "5 AÑOS SIN RESPUESTA", "kw", "papel", 960, 160, t, size=96, rot=-3)
    t = S.w("reparto")
    s.sello("conf", "SHANG-CHI: CONFIRMADO", 960, 960, t, color="heroe", rot=-3)
