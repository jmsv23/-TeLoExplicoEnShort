"""DATO 6 · Loki sostiene el multiverso."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato seis"), bg="multi", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 6", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Loki")
    s.img("loki", "a-loki.jpg", 1060, 120, 700, 760, t, frm="R", pos="50% 20%", label="LOKI")
    t = S.w("rey del multiverso")
    s.obj("crown", '<div data-com="crown" style="width:340px;height:234px"></div>', 1410, 120, t, how="drop")
    s.text("rey", "EL REY DEL MULTIVERSO", "kw", "papel", 520, 600, t, size=90, rot=-5)

    s = S.scene(S.w("Al final de su serie"), bg="tinta", enter="halftone", color="multi")
    s.phpanel("telar", "N-09", "El Telar Temporal", "still de Loki T2", 90, 100, 900, 600, s.start + 0.05, frm="L")
    t = S.w("tantas líneas")
    s.obj("tr", L.branches(820, 450), 1420, 360, t)
    s.code(f'COM.drawOn(tl, qa("#{s.id("tr")} .br"), {s.T(t)}, {{ dur: 0.7 }});')
    t = S.w("destruir todas las alternativas")
    s.text("des", "¡ERA PARA DESTRUIRLAS!", "kw", "rojo", 1340, 760, t, size=84, rot=-4)
    s.sfx("record-scratch" if False else "scratch", t, -6)

    s = S.scene(S.w("Loki se sacrifica"), bg="multi", enter="ink")
    s.img("arbol", "lf/arbol.jpg", 60, 60, 1800, 960, s.start + 0.05, frm="B", pos="50% 40%")
    s.kenburns("arbol", s.start, S.peek("Por qué es tan importante"), scale=1.1)
    t = S.w("árbol del multiverso")
    s.text("arb", "EL ÁRBOL DEL MULTIVERSO", "kw", "amarillo", 960, 900, t, size=100, rot=-3)
    t = S.w("dios de las historias")
    s.sello("dios", "DIOS DE LAS HISTORIAS", 520, 180, t, color="multi", rot=-6)
    t = S.w("eternidad")
    s.text("sol", "SOLO. PARA SIEMPRE.", "ttl", "papel", 1380, 200, t, size=90, rot=3)

    s = S.scene(S.w("Por qué es tan importante"), bg="doom", enter="halftone", color="doom")
    t = S.w("controlar")
    s.com("doom", "doom", 520, 560, 520, 645, t, how="drop")
    s.text("csd", "¿CONTROLAR · SALVAR · DESTRUIR?", "kw", "amarillo", 1280, 200, t + 0.2, size=70, rot=-3)
    t = S.w("pasar por Loki")
    s.img("lok2", "lf/tr-loki.jpg", 1000, 330, 820, 460, t, frm="R", pos="50% 40%", label="LOKI · EN EL TRÁILER")
    t = S.w("Hiddleston")
    s.sello("conf", "CONFIRMADO", 1640, 800, t, color="heroe", rot=-10)
    t = S.w("cada Avenger")
    s.panel("alf", '<div style="font:400 60px/1.05 Anton;color:#0B0B14;text-align:center;padding:12px">¿DÓNDE ESTÁ CADA AVENGER?<br><span style="color:#E8212B">→ AL FINAL</span></div>',
            560, 820, 800, 200, "amarillo", -2, t, "B")
