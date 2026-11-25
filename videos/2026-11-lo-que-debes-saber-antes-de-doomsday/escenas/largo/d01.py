"""DATO 1 · Doom no es Tony Stark."""
from lib_h import pho, ph, svgimg, L


def build(S):
    # 1 · portada del dato
    s = S.scene(S.w("Dato uno"), bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 1", "ttl", "amarillo", 520, 230, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Iron Man")
    s.com("iron", "iron", 520, 640, 340, 408, t, how="pop")
    s.com("no", "forbidden", 520, 640, 420, 420, t + 0.35, how="stamp")
    t = S.w("Victor von Doom")
    s.com("doom", "doom", 1330, 600, 520, 645, t, how="drop")
    s.text("vvd", "VICTOR VON DOOM", "kw", "papel", 1330, 960, t + 0.2, size=96, rot=-4)
    t = S.w("Robert")
    s.img("rdj", "rdj-recorte.jpg", 90, 640, 300, 360, t, frm="L", pos="50% 20%", label="RDJ", rot=-4)

    # 2 · origen de los cómics: viñetas
    s = S.scene(S.w("Para entender"), bg="papel", enter="pageflip")
    s.cinta("cinta", "ORIGEN DE LOS CÓMICS", "multi", top=40, rot=-3, at=s.start + 0.1)
    t = S.w("Latveria")
    s.panel("v1", L.building(380, "") + '<div style="position:absolute;bottom:14px;width:100%;text-align:center;font:400 48px Anton">LATVERIA · POBRE</div>',
            70, 200, 560, 420, "papel", -2, t, "L")
    t = S.w("ciencia")
    s.com("gear", "gearAtom", 820, 410, 260, 260, t)
    t = S.w("magia")
    s.com("runes", "runes", 1100, 410, 260, 260, t)
    t = S.w("Reed Richards")
    s.img("reed", "a-reed.jpg", 1340, 200, 480, 420, t, frm="R", pos="50% 20%", label="REED RICHARDS")
    t = S.w("cálculos")
    s.panel("calc", '<div style="font:700 60px/1.1 Comic Neue;color:#0B0B14;text-align:center">E = mc²<br>+ ⚡ ≠ ☠<br><span style="color:#E8212B">¡ERROR!</span></div>',
            120, 660, 520, 340, "papel", 2, t, "B")
    t = S.w("explotó")
    s.text("boom", "¡KRAKOOM!", "ono", "rojo", 960, 760, t, rot=-8, hold=1.0, zoom=True)
    s.sfx("explosion", t, -4)
    t = S.w("máscara de metal")
    s.img("clasico", "lf/doom-comic-clasico.jpg", 1460, 560, 380, 480, t, frm="B", pos="50% 20%", label="DOOM · 1961")
    t = S.w("culpando")
    s.globo("culpa", "¡ES CULPA DE REED!", 700, 650, 520, 160, t, rot=2, size=44)

    # 3 · rey de Latveria + inmunidad
    s = S.scene(S.w("Hoy es el rey"), bg="doom", enter="halftone", color="doom")
    s.com("castle", "castle", 560, 560, 600, 520, s.start + 0.1, how="drop")
    s.com("crown", "crown", 560, 300, 300, 206, S.w("rey"), how="drop")
    t = S.w("inmunidad")
    s.sello("inm", "INMUNIDAD DIPLOMÁTICA", 1330, 360, t, color="tinta", rot=-6)
    t = S.w("guerra")
    s.text("guerra", "= GUERRA", "kw", "rojo", 1330, 560, t, size=130, rot=-4)
    t = S.w("Tony Stark")
    s.com("arc", "arcReactor", 1150, 820, 220, 220, t)
    t = S.w("Doctor Strange")
    s.com("rn", "runes", 1520, 820, 220, 220, t)
    t = S.w("Ciencia, magia y una corona")
    s.text("cmc", "CIENCIA · MAGIA · CORONA", "kw", "amarillo", 960, 980, t, size=84, rot=-2)

    # 4 · Kang cayó
    s = S.scene(S.w("Ahora"), bg="multi", enter="pageflip")
    t = S.w("Kang")
    s.img("kang", "lf/kang-poster.jpg", 120, 160, 560, 720, t, frm="L", pos="50% 25%", label="KANG")
    t = S.w("Dynasty")
    s.text("dyn", "THE KANG DYNASTY", "ttl", "papel", 1260, 330, t, size=110, rot=-3)
    s.draw("tach", "M820 300 L1700 380", "rojo", t + 0.5, w=34, dur=0.3)
    t = S.w("hormigas")
    s.text("ants", "¡¿HORMIGAS?!", "ono", "amarillo", 1260, 560, t, rot=6, hold=1.0)
    s.sfx("scratch", t, -4)
    t = S.w("culpable")
    s.panel("tit", '<div style="padding:20px 30px;font:400 60px/1.05 Anton;color:#0B0B14;text-align:left">2023: CULPABLE DE<br>AGRESIÓN Y ACOSO</div>',
            900, 720, 820, 220, "papel", -2, t, "B")
    t = S.w("cortó")
    s.sello("fuera", "FUERA", 1600, 760, t, color="rojo", rot=-12)

    # 5 · Comic-Con 2024: Russo + RDJ como Doom
    s = S.scene(S.w("Y en la"), bg="heroe", enter="halftone", color="amarillo")
    s.text("cc", "COMIC-CON 2024", "ttl", "amarillo", 960, 150, s.start + 0.1, size=110, rot=-3)
    t = S.w("hermanos Russo")
    s.img("russo", "russo.jpg", 120, 260, 640, 460, t, frm="L", pos="50% 30%", label="HERMANOS RUSSO", sub="DIRECTORES DE ENDGAME")
    t = S.w("reemplazo")
    s.img("rdj2", "rdj-recorte-alt.jpg", 1120, 260, 520, 600, t, frm="R", pos="50% 20%", label="ROBERT DOWNEY JR.")
    t = S.w("máscara verde")
    s.com("mk2", "doomMask", 1380, 560, 330, 385, t, how="drop")
    s.flash(t + 0.3)

    # 6 · clip «soy Doom»
    c = S.clip(0)
    s = S.scene(c["start"] - 0.35, bg="tinta", enter="ink")
    s.video("soy", c["src"], c["in"], c["start"], c["end"] - c["start"], 160, 90, 1600, 760, tag="TRÁILER", frm="B", slam=False)
    s.sfx("stinger", c["start"] + 1.6, -4)

    # 7 · ¿variante de Tony? Feige: NO
    s = S.scene(S.w("Y aquí viene"), bg="papel", enter="halftone", color="ciencia")
    t = S.w("Tony Stark malvado")
    s.com("iron2", "iron", 560, 520, 360, 432, t)
    s.globo("var", "¿UN TONY MALVADO?", 860, 160, 620, 200, t + 0.3, kind="nube", size=50)
    t = S.w("Faigui")
    s.img("feige", "a-feige.jpg", 1240, 380, 520, 560, t, frm="R", pos="50% 25%", label="KEVIN FEIGE")
    t = S.w("Empire")
    s.sello("emp", "EMPIRE", 1500, 300, t, color="tinta", rot=6)
    t = S.w("La respuesta es no")
    s.slab("blk", "tinta", t - 0.4, t + 0.05, pat=False)
    t2 = S.w("no", again=False)
    s.text("no", "NO.", "ttl", "rojo", 560, 520, t2, size=300, rot=-6, zoom=True)
    s.flash(t2)
    t = S.w("Victor von Doom")
    s.text("vvd2", "ES VICTOR VON DOOM", "kw", "amarillo", 960, 930, t, size=100, rot=-3)

    # 8 · Steve / Johnny
    s = S.scene(S.w("puso un ejemplo"), bg="heroe", enter="pageflip")
    t = S.w("Steve Rogers")
    s.img("steve", "a-cap.jpg", 140, 180, 620, 620, t, frm="L", pos="50% 20%", label="STEVE ROGERS")
    t = S.w("Johnny Storm")
    s.img("johnny", "a-johnny-evans.jpg", 1160, 180, 620, 620, t, frm="R", pos="50% 20%", label="JOHNNY STORM")
    s.text("neq", "≠", "ttl", "amarillo", 960, 480, t + 0.3, size=260, rot=0)
    t = S.w("Un actor, dos personajes")
    s.cap("cap", "UN ACTOR · DOS PERSONAJES", t, left=560, top=880, width=800)

    # 9 · 1961 vs 1963
    s = S.scene(S.w("Además"), bg="papel", enter="halftone", color="amarillo")
    t = S.w("mil novecientos sesenta y uno")
    s.img("ff5", "a-tos39.jpg", 160, 150, 760, 760, t, frm="L", pos="0% 50%")
    s.text("61", "DOOM: 1961", "ttl", "doom", 540, 980, t + 0.2, size=90, rot=-3)
    t = S.w("dos años antes")
    s.text("63", "IRON MAN: 1963", "ttl", "rojo", 1380, 980, t + 0.3, size=90, rot=3)
    s.panel("ts", pho("a-tos39.jpg", "100% 50%"), 1000, 150, 760, 760, "tinta", 2, t, "R")
    t = S.w("Ojo")
    s.cap("ojo", "OJO: NO DIJO QUE IRON MAN NO SALGA", t, left=360, top=40, width=1200)

    # 10 · guarda eso
    s = S.scene(S.w("Guarda eso"), bg="doom", enter="ink")
    s.com("doomb", "doom", 960, 520, 560, 694, s.start + 0.05, how="drop")
    t = S.w("la cara es de Tony")
    s.text("cara", "LA CARA ES DE TONY", "kw", "papel", 960, 120, t, size=96, rot=-3)
    t = S.w("el hombre es otro")
    s.text("otro", "EL HOMBRE ES OTRO", "kw", "amarillo", 960, 960, t, size=110, rot=-3, misreg=True)
    t = S.w("final de Endgame")
    s.raw(f'<div class="c" style="left:1560px;top:520px"><div id="{s.id("eg")}">{svgimg("endgame-logo.png", 500, 160, "filter:drop-shadow(6px 6px 0 #0B0B14)")}</div></div>')
    s.code(f'COM.popIn(tl, q("#{s.id("eg")}"), {s.T(t)}, {{ rot: 4 }});')
