from esc_short_01._k import tag, still, clipsc


def build(S):
    s = S.scene(S.t0, bg="tinta", enter="ink")
    still(s, "rs", "hijo-peggy", (0, 0, 1080, 1920), S.t0 + 0.02, kb=S.peek("Mientras tanto"), pos="55% 40%", frm="B")
    t = S.w("consecuencias")
    s.text("cn", "CONSECUENCIAS", "ttl", "rojo", 540, 1500, t, size=120, rot=-4)
    s = S.scene(S.w("Mientras tanto"), bg="doom", enter="ink", color="doom")
    still(s, "dm", "doom-catedral", (0, 0, 1080, 1920), s.start + 0.02, kb=S.clip(0)["start"], pos="50% 40%", frm="B")
    t = S.w("vidas robadas")
    s.text("vr", "VIDAS ROBADAS", "ttl", "papel", 540, 1500, t, size=130, rot=-4, misreg=True)
    s, c = clipsc(S, 0, bg="doom-osc")
    s.text("dv", "¡DEVUÉLVANLAS!", "ono", "amarillo", 540, 1450, c["start"] + 2.5, rot=-6)
