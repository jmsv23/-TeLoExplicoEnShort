"""CIERRE · qué ver + CTA."""
from lib_h import pho, ph, svgimg, L

LISTA = [("Endgame", "endgame-logo.png", "ENDGAME"), ("Loki", "a-lokilogo.jpg", "LOKI T1 Y T2"), ("Doctor Strange", "a-strange-poster.jpg", "MULTIVERSO DE LA LOCURA"),
         ("Sin camino a casa", "a-spider3.jpg", "NO WAY HOME"), ("First Steps", "a-fantastic4.jpg", "FIRST STEPS"), ("Thunderbolts", "a-thunder.jpg", "THUNDERBOLTS*"),
         ("Un nuevo mundo", "a-brave.jpg", "UN NUEVO MUNDO"), ("The Marvels", None, "THE MARVELS (POSCRÉDITOS)")]


def build(S):
    s = S.scene(S.w("Si te faltan"), bg="papel", enter="pageflip")
    s.text("t", "LO QUE SÍ TIENES QUE VER", "ttl", "rojo", 960, 90, s.start + 0.1, size=86, rot=-2)
    for k, (w, f, lab) in enumerate(LISTA):
        try:
            t = S.w(w)
        except SystemExit:
            t = S.w(w.split()[0])
        x, y = 60 + (k % 4) * 460, 190 + (k // 4) * 400
        if f:
            s.img(f"l{k}", f, x, y, 420, 360, t, frm="T" if k % 2 else "B", pos="50% 35%", label=f"{k+1}. {lab}", rot=(-2, 1.5, -1.5, 2)[k % 4])
        else:
            s.phpanel(f"l{k}", "N-25b", "The Marvels", "póster de The Marvels", x, y, 420, 360, t, frm="B", label=f"{k+1}. {lab}")
    t = S.w("tiempo extra")
    s.sello("ext", "+ EXTRA: WANDAVISION · SHANG-CHI · DÍAS DEL FUTURO PASADO", 960, 1000, t, color="multi", rot=-1, size=34)

    s = S.scene(S.w("Marvel nos hizo"), bg="doom", enter="ink", pat="pat-benday-fuerte")
    s.svg("dm", "lf/doom-frente.svg", 400, 600, 560, 728, s.start + 0.05, how="drop", bob=S.t1)
    t = S.w("quince datos")
    s.text("15", "15 DATOS ✓", "ttl", "amarillo", 1200, 200, t, size=130, rot=-4)
    t = S.w("comentarios")
    s.globo("q1", "¿CUÁL TE SORPRENDIÓ MÁS?", 860, 340, 880, 180, t, size=50)
    t = S.w("robó la vida")
    s.globo("q2", "¿QUIÉN LE ROBÓ LA VIDA A DOOM?", 860, 560, 900, 180, t, kind="globo", size=48, rot=2)
    t = S.w("like")
    s.text("like", "👍 LIKE", "kw", "papel", 1080, 840, t, size=90, rot=-4) if False else s.sello("like", "DALE LIKE", 1040, 840, t, color="heroe", rot=-6)
    t = S.w("suscríbete")
    s.sello("sus", "SUSCRÍBETE", 1500, 840, t, color="rojo", rot=5)
    t = S.w("diecisiete de diciembre")
    s.video("fecha", "lf-t08-fecha-17-dic.mp4", 0.2, t - 0.3, 3.4, 760, 120, 1080, 600, tag="17 DE DICIEMBRE", frm="R")
