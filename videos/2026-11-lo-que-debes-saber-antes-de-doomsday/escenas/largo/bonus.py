"""BONUS · Dónde está cada Avenger (fichas de expediente)."""
from lib_h import pho, ph, svgimg, L

POS = [(70, 175), (535, 150), (1000, 175), (1465, 150)]


def build(S):
    s = S.scene(S.w("Y como te prometí"), bg="amarillo" if False else "heroe", enter="pageflip", pat="pat-benday-fuerte")
    s.text("t", "¿DÓNDE ESTÁ CADA AVENGER?", "ttl", "amarillo", 960, 420, s.start + 0.1, size=110, rot=-3, misreg=True)
    s.text("r", "¡RÁPIDO!", "ono", "rojo", 960, 700, S.w("Rápido"), rot=-6, hold=0.9)

    # grupos de 4 fichas por escena: (palabra que dispara, nombre, texto, img | None, phkey, estado, color)
    grupos = [
        [("Tony Stark", "TONY STARK", "Murió en Endgame", "a-ironman.jpg", None, "FUERA", "rojo"),
         ("Natasha", "NATASHA → YELENA", "Yelena lidera a los nuevos Vengadores", "a-yelena.jpg", None, "CONFIRMADA", "heroe"),
         ("Steve Rogers", "STEVE ROGERS", "Envejeció en el pasado… y vuelve", "a-cap.jpg", None, "CONFIRMADO", "heroe"),
         ("Sam Wilson", "SAM WILSON", "Capitán América", "a-samcap.jpg", None, "CONFIRMADO", "heroe")],
        [("Joaquín Torres", "JOAQUÍN TORRES", "El nuevo Halcón", None, "N-91", "CONFIRMADO", "heroe"),
         ("Bucky", "BUCKY", "Congresista y nuevo Vengador", "a-bucky.jpg", None, "CONFIRMADO", "heroe"),
         ("Thor", "THOR", "Adoptó a Love · rayos contra Doom", "a-thor.jpg", None, "CONFIRMADO", "heroe"),
         ("Bruce Banner", "BRUCE BANNER", "Hulk inteligente · hijo: Skaar", "a-bruce.jpg", None, "NO ANUNCIADO", "ceniza")],
        [("Clint Barton", "CLINT BARTON", "Retirado · el arco es de Kate Bishop", None, "N-92", "NO ANUNCIADO", "ceniza"),
         ("Doctor Strange", "DOCTOR STRANGE", "En la Dimensión Oscura con Clea", "a-strange.jpg", None, "NO ANUNCIADO", "ceniza"),
         ("Capitana Marvel", "CAPITANA MARVEL", "Después de The Marvels", None, "N-93", "NO ANUNCIADO", "ceniza"),
         ("Peter Parker", "SPIDER-MAN", "Nadie recuerda a Peter", "a-tom.jpg", None, "NO ANUNCIADO", "ceniza")],
        [("Scott Lang", "ANT-MAN + CASSIE", "Escapó del Reino Cuántico", None, "N-94", "CONFIRMADOS", "heroe"),
         ("Shuri", "SHURI + M'BAKU", "La nueva Pantera Negra", "lf/shuri-mbaku.jpg", None, "CONFIRMADOS", "heroe"),
         ("Wanda", "WANDA", "Vuelve de la mano de Doom", "a-scarlet.jpg", None, "CONFIRMADA", "heroe"),
         ("Loki sigue", "LOKI", "En su trono, sosteniendo todo", "a-loki.jpg", None, "CONFIRMADO", "heroe")],
    ]
    bgs = ["papel", "heroe", "ceniza", "multi"]
    for g, grupo in enumerate(grupos):
        s = S.scene(S.w(grupo[0][0], -0.3), bg=bgs[g], enter="pageflip" if g % 2 else "halftone", color="amarillo")
        tthor = S.peek("lanzando rayos") if g == 1 else None
        for k, (w, nom, txt, img, phk, est, col) in enumerate(grupo):
            t = s.start + 0.3 if k == 0 else S.w(w)
            x, y = POS[k]
            s.ficha(f"f{k}", nom, txt, img, x, y, t, estado=est, ecolor=col, rot=(-2, 1.5, -1.5, 2)[k], frm="B" if k % 2 else "T",
                    phkey=phk, phdesc="retrato pendiente")
        if g == 1:
            t = tthor
            s.video("thor", "lf-t07-thor-mjolnir.mp4", 6.0, t, 3.2, 560, 800, 800, 250, tag="TRÁILER · THOR VS. DOOM", frm="B")

    s = S.scene(S.w("James Rhodes", -0.3), bg="rojo", enter="ink", pat="pat-benday-fuerte")
    s.ficha("rh", "JAMES RHODES", "Durante años fue un Skrull", None, 120, 140, s.start + 0.3, estado="NO ANUNCIADO", ecolor="ceniza",
            rot=-2, phkey="N-96", phdesc="retrato de Don Cheadle / War Machine")
    t = S.w("Skrull")
    s.text("sk", "¡¿UN SKRULL?!", "ono", "amarillo", 1200, 360, t, rot=-6, hold=1.2)
    s.sfx("scratch", t, -4)
    t = S.w("Secret Invasion")
    s.cap("si", "SECRET INVASION", t, left=880, top=640, width=620)
