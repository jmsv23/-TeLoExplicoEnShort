"""DATO 14 · Los Centinelas."""
from lib_h import pho, ph, svgimg, L


def build(S):
    s = S.scene(S.w("Dato catorce"), bg="tinta", enter="ink")
    s.text("d", "DATO 14", "ttl", "amarillo", 420, 140, s.start + 0.05, size=130, rot=-5, misreg=True)
    t = S.w("Doom levantando")
    s.video("cent", "lf-t06-soy-doom-centinelas.mp4", 3.2, t, 5.0, 160, 230, 1600, 680, tag="TRÁILER", frm="B")
    s.sfx("rumble", t + 0.2, -3)
    t = S.w("Centinelas")
    s.text("cen", "¡CENTINELAS!", "ono", "rojo", 960, 980, t, rot=-5, hold=1.6)

    s = S.scene(S.w("Para entender"), bg="papel", enter="pageflip")
    s.phpanel("dofp", "N-19a", "Días del futuro pasado", "póster o logo de X-Men: DOFP", 80, 100, 560, 820, s.start + 0.05, frm="L")
    t = S.w("futuro de pesadilla")
    s.phpanel("fut", "N-19b", "El futuro de los Centinelas", "still de DOFP (Centinelas dominando)", 700, 100, 1140, 560, t, frm="R")
    t = S.w("robots gigantes")
    s.img("cn", "lf/tr-doom-centinelas.jpg", 700, 700, 560, 300, t, frm="B", pos="80% 30%", label="CENTINELA")
    t = S.w("también a los humanos")
    s.sello("hum", "Y A LOS HUMANOS", 1560, 860, t, color="rojo", rot=-6)

    s = S.scene(S.w("La única solución"), bg="heroe", enter="halftone", color="heroe")
    t = S.w("Wolverine")
    s.img("wol", "a-wolverine.jpg", 100, 120, 520, 620, t, frm="L", pos="50% 20%", label="WOLVERINE")
    t = S.w("mil novecientos setenta y tres")
    s.text("73", "1973", "ttl", "amarillo", 360, 870, t, size=180, rot=-5)
    t = S.w("Mística")
    s.img("mis", "a-mistica.jpg", 700, 120, 520, 620, t, frm="B", pos="50% 20%", label="MÍSTICA")
    t = S.w("Bolívar Trask")
    s.phpanel("trask", "N-19c", "Bolívar Trask", "retrato de Peter Dinklage en DOFP", 1300, 120, 520, 620, t, frm="R", label="BOLÍVAR TRASK")
    t = S.w("ADN")
    s.text("adn", "SU ADN = CENTINELAS QUE SE ADAPTAN", "kw", "papel", 1200, 900, t, size=60, rot=-3)

    s = S.scene(S.w("No sabemos"), bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.img("dc", "lf/tr-doom-centinelas.jpg", 100, 90, 1720, 760, s.start + 0.05, frm="B", pos="50% 45%")
    s.kenburns("dc", s.start, S.t1, scale=1.1)
    t = S.w("enemigo perfecto")
    s.text("ep", "EL ENEMIGO PERFECTO DE LOS X-MEN", "kw", "amarillo", 960, 960, t, size=80, rot=-3)
    s.sello("tr", "DEL TRÁILER", 1600, 180, t + 0.3, color="tinta", rot=8)
