"""DOS · Doom la para sin moverse."""
from esc_short_01._k import tag, still, vid, T1
from esc_largo._k import frame

def build(S):
    s = S.scene(S.t0, bg="doom", enter="cut", color="doom")
    s.img("dm", frame(T1, 10.6), 0, 0, 1080, 1920, S.t0 + 0.02, frm="B", pos="70% 50%")
    s.kenburns("dm", S.t0 + 0.1, S.t1, scale=1.2)
    t = S.w("sin moverse")
    s.text("sm", "SIN MOVERSE", "ttl", "amarillo", 540, 470, t, size=150, rot=-4, misreg=True, zoom=True)
    t = S.w("centímetro")
    s.text("cm", "¡NI UN CENTÍMETRO!", "ono", "rojo", 540, 1500, t, size=104, rot=-6)
