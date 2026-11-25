from esc_short_01._k import tag, still, clipsc


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    still(s, "jr", "4f-jardin", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.clip(0)["start"], pos="45% 50%", frm="B")
    t = S.w("Cuatro Fantásticos")
    s.text("4f", "¡LOS 4 FANTÁSTICOS!", "ttl", "amarillo", 540, 1500, t, size=110, rot=-4)
    s, c = clipsc(S, 0)
    s.text("pa", "«¿ERAS UN SUPERHÉROE?»", "kw", "amarillo", 540, 460, c["start"] + 0.4, size=64, rot=-3)
    s.text("6", "ÉRAMOS SEIS", "ttl", "papel", 540, 1420, c["start"] + 5.0, size=130, rot=-4, misreg=True)
