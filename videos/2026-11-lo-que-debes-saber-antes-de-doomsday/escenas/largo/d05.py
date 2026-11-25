"""DATO 5 · Doctor Strange, Wanda y el Darkhold."""
from lib_h import pho, ph, svgimg, L


def darkhold(w=380):
    g = ('<rect x="30" y="20" width="300" height="380" rx="16" fill="#3A1C1C" stroke="#0B0B14" stroke-width="10"/>'
         '<rect x="50" y="40" width="260" height="340" rx="8" fill="none" stroke="#E8212B" stroke-width="6"/>'
         '<path d="M180 120 L230 200 L180 280 L130 200 Z" fill="#E8212B" stroke="#0B0B14" stroke-width="7"/>'
         '<ellipse cx="180" cy="200" rx="22" ry="14" fill="#FFD400" stroke="#0B0B14" stroke-width="5"/>')
    return L.svgbox("0 0 360 420", g, w, int(w * 420 / 360))


def build(S):
    s = S.scene(S.w("Dato cinco"), bg="rojo", enter="ink", pat="pat-benday-fuerte")
    s.text("d", "DATO 5", "ttl", "amarillo", 480, 200, s.start + 0.05, size=150, rot=-5, misreg=True)
    t = S.w("Wanda")
    s.img("wanda", "a-wanda.jpg", 1060, 120, 700, 760, t, frm="R", pos="50% 20%", label="WANDA MAXIMOFF")
    t = S.w("heroína a villana")
    s.text("hv", "HEROÍNA → VILLANA", "kw", "papel", 520, 600, t, size=100, rot=-5)

    s = S.scene(S.w("Después de perder"), bg="papel", enter="pageflip")
    s.phpanel("wv", "N-07a", "WandaVision: el Hex", "still o logo de WandaVision", 90, 120, 900, 600, S.w("Wanda Vision"), frm="L")
    t = S.w("Hex")
    s.obj("hex", L.svgbox("0 0 600 400", '<path d="M40 360 A260 300 0 0 1 560 360 Z" fill="#E8212B" fill-opacity=".35" stroke="#E8212B" stroke-width="14"/><path d="M40 360 H560" stroke="#0B0B14" stroke-width="12"/><rect x="250" y="250" width="100" height="110" fill="#FFF3D6" stroke="#0B0B14" stroke-width="8"/><polygon points="240,255 300,205 360,255" fill="#FFD400" stroke="#0B0B14" stroke-width="8"/>', 760, 507), 1420, 420, t)
    t = S.w("todo un pueblo")
    s.text("pue", "UN PUEBLO ATRAPADO", "kw", "rojo", 1420, 820, t, size=84, rot=-4)
    t = S.w("vida perfecta")
    s.phpanel("fam", "N-07b", "Wanda, Visión, Billy y Tommy", "still de WandaVision", 160, 760, 760, 300, t, frm="B")

    s = S.scene(S.w("Pero hay un costo"), bg="multi", enter="halftone", color="rojo")
    s.sello("costo", "CIENTOS DE INOCENTES", 960, 160, S.w("cientos"), color="rojo", rot=-4)
    t = S.w("Agatha")
    s.phpanel("aga", "N-07c", "Agatha Harkness", "still de WandaVision", 120, 300, 620, 620, t, frm="L", label="AGATHA")
    t = S.w("Darkhold")
    s.obj("dh", darkhold(380), 1320, 560, t, how="drop")
    s.text("dhl", "EL DARKHOLD", "kw", "rojo", 1320, 940, t + 0.3, size=96, rot=-3)
    s.sfx("magic", t, -4)
    t = S.w("corrompe")
    s.shake("dh", t, amp=18, dur=0.6)

    s = S.scene(S.w("Multiverse of Madness"), bg="tinta", enter="ink")
    s.img("mom", "a-strange-poster.jpg", 100, 100, 640, 880, s.start + 0.05, frm="L", pos="50% 30%")
    t = S.w("cruzar universos")
    s.img("wan2", "lf/tr-wanda-llora.jpg", 820, 120, 1000, 560, t, frm="R", pos="40% 40%", label="LA BRUJA ESCARLATA")
    t = S.w("casi destruye")
    s.text("casi", "¡CASI DESTRUYE EL MULTIVERSO!", "kw", "amarillo", 1320, 800, t, size=72, rot=-3)
    t = S.w("ya no es la heroína")
    s.sello("vill", "VILLANA", 1320, 960, t, color="rojo", rot=-8)
