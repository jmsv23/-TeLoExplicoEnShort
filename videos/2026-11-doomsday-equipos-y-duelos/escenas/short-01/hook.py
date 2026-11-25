"""HOOK · desde el segundo 0: Thor carga el rayo (video en movimiento) → clip: Doom detiene Stormbreaker."""
from esc_short_01._k import tag, still, vid, clipsc, T1

def build(S):
    s = S.scene(S.t0, bg="tinta", enter="cut")
    vid(s, "th", T1, 4.6, S.t0 + 0.0, S.clip(0)["start"] - S.t0, pos="55% 50%")
    s.text("dd", "DOOM DETUVO…", "ttl", "amarillo", 540, 470, S.t0 + 0.05, size=120, rot=-4, sfx=False)
    t = S.w("una mano")
    s.text("um", "¡CON UNA MANO!", "ono", "amarillo", 540, 1450, t, size=104, rot=-6)
    t = S.w("casi mata")
    s.text("cm", "EL ARMA QUE CASI MATA A THANOS", "kw", "papel", 540, 1640, t, size=64, rot=-2)
    s, c = clipsc(S, 0)
    s.text("st", "STORMBREAKER", "ttl", "rojo", 540, 470, c["start"] + 0.3, size=130, rot=-4, misreg=True)
    tag(s, "C", c["start"] + 0.8, x=540, y=1760)
