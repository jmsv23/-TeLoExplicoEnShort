"""DATO 3 · La Línea Sagrada se rompe."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato tres"), bg="multi", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 3", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("puñalada")
    s.text("pu", "¡ZAS!", "ono", "rojo", 480, 560, t, rot=-10, hold=1.0)
    s.sfx("bam2", t, -3)
    t = S.w("Sylvie")
    s.img("syl", "a-sylvie.jpg", 1000, 140, 780, 520, t, frm="R", pos="50% 25%", label="SYLVIE")
    t = S.w("He Who Remains", again=False)
    s.phpanel("hwr", "N-05", "He Who Remains", "still de Loki T1", 1000, 700, 780, 300, t, frm="B", pos="50% 25%", label="HE WHO REMAINS")

    s = S.scene(S.w("Antes de eso"), bg="papel", enter="pageflip")
    t = S.w("una sola línea")
    s.draw("linea", "M80 540 L1840 540", "heroe", t, w=44, dur=0.8)
    t = S.w("Línea Sagrada")
    s.text("ls", "LA LÍNEA SAGRADA", "kw", "multi", 960, 380, t, size=120, rot=-3)
    t = S.w("TVA")
    s.sello("tva", "VIGILADA POR LA TVA", 960, 760, t, color="tinta", rot=-4)
    t = S.w("variante de Kang")
    s.img("kang", "a-kang.jpg", 1460, 640, 380, 380, t, frm="R", pos="50% 20%", label="VARIANTE DE KANG")

    s = S.scene(S.w("Cuando él cae"), bg="multi", enter="halftone", color="multi")
    s.obj("tree", L.branches(1600, 880), 960, 540, s.start + 0.05)
    s.code(f'COM.drawOn(tl, qa("#{s.id("tree")} .br"), {s.T(s.start + 0.1)}, {{ dur: 1.0 }});')
    t = S.w("explota")
    s.text("kra", "¡KRAKOOM!", "ono", "amarillo", 520, 260, t, rot=-8, hold=1.0, zoom=True)
    s.sfx("explosion", t, -4)
    t = S.w("sin control")
    s.text("sc", "SIN CONTROL", "kw", "papel", 1380, 900, t, size=110, rot=-4)
    t = S.w("Spider-Man")
    s.img("sp", "a-spider3.jpg", 1300, 120, 520, 330, t, frm="R", pos="50% 30%")
    t = S.w("Doctor Strange")
    s.img("st", "a-strange.jpg", 120, 640, 460, 330, t, frm="L", pos="50% 25%")

    s = S.scene(S.w("Es como un videojuego"), bg="heroe", enter="pageflip")
    s.obj("pad", L.gamepad(520), 480, 520, s.start + 0.1, bob=S.peek("Nuestra"))
    t = S.w("un solo guardado")
    s.panel("slot1", '<div style="font:400 64px Anton;color:#0B0B14">PARTIDA 1</div>', 960, 140, 820, 140, "amarillo", -2, t, "R")
    t = S.w("mil partidas")
    for k in range(6):
        s.panel(f"sl{k}", f'<div style="font:400 46px Anton;color:#FFF3D6">PARTIDA {[2, 47, 199, 616, 828, 999][k]}</div>',
                960 + (k % 2) * 420, 330 + (k // 2) * 170, 390, 130, ["multi", "rojo", "doom", "ciencia", "multi", "tinta"][k], (k % 3) - 1, t + k * 0.1, "R", sfx=k == 0)
    t = S.w("seiscientos dieciséis")
    s.sello("616", "NOSOTROS: TIERRA-616", 960, 960, t, color="heroe", rot=-4)
