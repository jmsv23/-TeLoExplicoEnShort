"""DATO 2 · Steve Rogers dejó un problema."""
from lib_h import pho, ph, svgimg, L


def gems(w=900):
    cols = ["#1E5BFF", "#FFD400", "#E8212B", "#8A2BE2", "#1FA85A", "#F28C28"]
    g = "".join(f'<polygon points="{80+k*150},40 {125+k*150},100 {80+k*150},160 {35+k*150},100" fill="{c}" stroke="#0B0B14" stroke-width="8" stroke-linejoin="round"/>' for k, c in enumerate(cols))
    return L.svgbox("0 0 940 200", g, w, int(w * 200 / 940))


def build(S):
    s = S.scene(S.w("Dato dos"), bg="heroe", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 2", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Steve Rogers")
    s.img("cap", "a-cap.jpg", 1060, 120, 700, 760, t, frm="R", pos="50% 20%", label="STEVE ROGERS")
    t = S.w("sin resolver")
    s.sello("sr", "PROBLEMA SIN RESOLVER", 520, 560, t, color="rojo", rot=-7)

    s = S.scene(S.w("Al terminar"), bg="papel", enter="pageflip")
    t = S.w("Gemas")
    s.obj("gems", gems(1000), 960, 200, t, how="pop")
    s.phpanel("devuelve", "N-03a", "Steve devuelve las gemas", "still de Endgame (Steve con el maletín)", 90, 360, 820, 560, S.w("momento exacto"), frm="L")
    t = S.w("se quedó en el pasado")
    s.phpanel("baile", "N-03b", "Steve y Peggy bailando", "still final de Endgame", 1010, 360, 820, 560, t, frm="R", label="PEGGY CARTER")
    s.text("pas", "SE QUEDÓ EN EL PASADO", "kw", "amarillo", 960, 960, t + 0.3, size=90, rot=-3)

    s = S.scene(S.w("Es tierno"), bg="doom", enter="halftone", color="doom")
    s.text("tierno", "TIERNO…", "kw", "papel", 560, 200, s.start + 0.05, size=120, rot=-4)
    t = S.w("costo")
    s.sello("costo", "PERO TIENE UN COSTO", 1300, 210, t, color="rojo", rot=-6)
    t = S.w("Russo")
    s.img("russo", "russo.jpg", 90, 380, 520, 420, t, frm="L", pos="50% 30%", label="SEGÚN LOS RUSSO")
    t = S.w("realidad ramificada")
    s.obj("br", L.branches(1100, 610), 1240, 600, t, how="pop")
    s.code(f'COM.drawOn(tl, qa("#{s.id("br")} .br"), {s.T(t + 0.1)}, {{ dur: 0.9 }});')
    s.text("rr", "REALIDAD RAMIFICADA", "kw", "amarillo", 1240, 960, t + 0.4, size=96, rot=-3)
    s.sfx("magic", t, -6)

    s = S.scene(S.w("Y esto importa"), bg="papel", enter="pageflip")
    t = S.w("Anciano")
    s.img("anc", "a-ancient.jpg", 120, 160, 600, 640, t, frm="L", pos="50% 25%", label="LA ANCIANA")
    t = S.w("Bruce Banner")
    s.img("bruce", "a-bruce.jpg", 1200, 160, 600, 640, t, frm="R", pos="50% 25%", label="BRUCE BANNER")
    t = S.w("crea ramas nuevas")
    s.globo("reg", "CAMBIAR EL PASADO CREA RAMAS NUEVAS", 620, 760, 680, 240, t, rot=-2, size=46)
    s.sello("regla", "LA REGLA", 960, 140, t + 0.4, color="multi", rot=-5)

    s = S.scene(S.w("ejemplo clarísimo"), bg="multi", enter="halftone", color="multi")
    t = S.w("dos mil doce")
    s.text("2012", "2012", "ttl", "amarillo", 420, 200, t, size=200, rot=-5, misreg=True)
    t = S.w("Teseracto")
    s.phpanel("tes", "N-04", "Se pierde el Teseracto", "still de Endgame (2012, Nueva York)", 90, 360, 760, 560, t, frm="L")
    s.obj("cubo", L.svgbox("0 0 300 300", '<polygon points="150,20 270,85 270,215 150,280 30,215 30,85" fill="#1E5BFF" stroke="#0B0B14" stroke-width="10"/><polygon points="150,20 270,85 150,150 30,85" fill="#00C8E8" stroke="#0B0B14" stroke-width="8"/><path d="M150 150 V280" stroke="#0B0B14" stroke-width="8"/>', 260, 260), 1000, 300, t + 0.2)
    t = S.w("Loki lo agarra")
    s.img("loki", "a-loki.jpg", 1140, 300, 640, 620, t, frm="R", pos="50% 20%", label="LOKI 2012")
    t = S.w("escapa")
    s.text("zap", "¡ZAP!", "ono", "amarillo", 1000, 640, t, rot=8, hold=0.8)
    s.sfx("zap", t, -4)
    t = S.w("nunca fue capturado")
    s.sello("rama", "NACE OTRA RAMA", 960, 980, t, color="tinta", rot=-4)

    s = S.scene(S.w("Un solo error"), bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.obj("br2", L.branches(900, 500), 560, 560, s.start + 0.1)
    s.code(f'COM.drawOn(tl, qa("#{s.id("br2")} .br"), {s.T(s.start + 0.2)}, {{ dur: 0.8 }});')
    t = S.w("Doom")
    s.com("doom", "doom", 1440, 560, 440, 546, t, how="drop")
    t = S.w("le hizo")
    s.globo("q", "¿Y SI ESA REALIDAD LE HIZO ALGO A DOOM?", 360, 90, 900, 220, t - 1.2, kind="nube", size=46, rot=2)
    t = S.w("Guarda esa pregunta")
    s.sello("gp", "GUARDA ESTA PREGUNTA", 640, 960, t, color="rojo", rot=-4)
    s.sfx("heartbeat", t, -4)
