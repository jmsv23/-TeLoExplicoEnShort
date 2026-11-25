"""ACTO 3 · LOS BANDOS (tarjeta de acto + recap)."""
from lib_h import pho, L


def build(S):
    s = S.scene(S.t0, bg="heroe", enter="pageflip", pat="pat-benday-fuerte")
    s.cinta("acto", "ACTO 3", "amarillo", top=110, rot=-4, at=s.start + 0.05)
    t = S.w("cómo se rompió todo")
    rec = [("a-cap.jpg", "STEVE"), ("a-sylvie.jpg", "LÍNEA ROTA"), ("a-spider3.jpg", "PAREDES"), ("a-wanda.jpg", "WANDA"), ("a-loki.jpg", "LOKI")]
    for k, (f, lab) in enumerate(rec):
        s.img(f"r{k}", f, 90 + k * 356, 300, 320, 300, t + k * 0.08, frm="T", pos="50% 25%", label=lab, rot=(-3, 2, -2, 3, -1)[k])
    t = S.w("los que se enfrentan")
    s.text("ban", "LOS BANDOS", "ttl", "amarillo", 960, 820, t, size=180, rot=-4, misreg=True, zoom=True)
