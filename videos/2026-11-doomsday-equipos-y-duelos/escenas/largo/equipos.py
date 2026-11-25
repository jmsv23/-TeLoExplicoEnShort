"""LOS HÉROES · 5 equipos con fichas + homenaje a Patrick Stewart + Loki aparte."""
from esc_largo._k import tag, still, fstill, im, TR, fondo

def fichas(s, items, y=260, x0=70, gap=460, step=0.0):
    """items: [(name, nombre, texto, img, t)]"""
    for k, (n, nom, txt, i, t) in enumerate(items):
        s.ficha(n, nom, txt, im(i), x0 + k * gap, y, t, rot=(-2 if k % 2 else 2))

def build(S):
    s = S.scene(S.t0, bg="heroe", enter="whip", color="heroe")
    still(s, "gr", "lf/lf04/grupo", (110, 70, 1700, 940), S.t0 + 0.02, kb=S.peek("Primero"), scale=1.1)
    t = S.w("los héroes")
    s.text("lh", "LOS HÉROES", "ttl", "amarillo", 960, 150, t, size=150, rot=-4)
    t = S.w("cinco")
    s.text("5", "¡SON 5 EQUIPOS!", "ono", "rojo", 960, 900, t, rot=-5)

    # 1 · Vengadores de Sam
    s = S.scene(S.w("Primero"), bg="papel", enter="pageflip")
    fondo(s, "bg1", (TR, 109.0), s.start + 0.02, S.peek("Shuri"), dim=0.35)
    s.text("t1", "1 · VENGADORES DE SAM", "kw", "heroe", 960, 110, s.start + 0.1, size=84, rot=-2, sfx=False)
    fichas(s, [("f1", "SAM WILSON", "el nuevo Capitán América", "a-samcap", S.w("Sam")),
               ("f2", "THOR", "dios del trueno", "a-thor", S.w("Thor")),
               ("f3", "SHANG-CHI", "los diez anillos", "lf/sc-anillos", S.w("Shang")),
               ("f4", "ANT-MAN", "Scott Lang", "ant-man", S.w("Ánt"))])
    s = S.scene(S.w("Shuri"), bg="heroe", enter="whip", color="heroe")
    s.img("sh", im("lf/lf04/shuri"), 60, 120, 820, 520, s.start + 0.02, frm="L", label="SHURI · WAKANDA")
    t = S.w("nuevo Falcon")
    s.text("fa", "+ M'BAKU + NUEVO FALCON", "kw", "papel", 470, 760, t, size=56, rot=-2)
    t = S.w("Kate")
    s.img("kt", im("lf/lf04/kate"), 1000, 120, 860, 620, t - 0.1, frm="R", label="KATE BISHOP", pos="50% 35%")
    t = S.w("primera vez")
    s.sello("nu", "¡NUEVA EN EL TRÁILER!", 1430, 860, t, color="rojo", rot=-7, size=60)
    s = S.scene(S.w("sorpresa"), bg="tinta", enter="cut")
    still(s, "sm", "lf/lf04/steve-mjolnir", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Segundo"), pos="45% 40%")
    t = S.w("Steve Rogers")
    s.text("sr", "¡STEVE ROGERS VUELVE!", "ttl", "amarillo", 960, 150, t, size=110, rot=-4)
    t = S.w("Mjolnir")
    s.text("mj", "¿CON EL MJOLNIR?", "ono", "rojo", 1400, 900, t, rot=-6)

    # 2 · Nuevos Vengadores
    s = S.scene(S.w("Segundo"), bg="ceniza", enter="pageflip")
    fondo(s, "bg2", (TR, 107.2), s.start + 0.02, S.peek("Ghost"), dim=0.35)
    s.text("t2", "2 · NUEVOS VENGADORES", "kw", "amarillo", 960, 110, s.start + 0.1, size=84, rot=-2, sfx=False)
    t = S.w("Thunderbolts")
    s.text("ex", "(EX THUNDERBOLTS*)", "kw", "papel", 960, 200, t, size=50, rot=-1, sfx=False)
    fichas(s, [("g1", "YELENA", "Viuda Negra", "a-yelena", S.w("Yelena")),
               ("g2", "BUCKY", "brazo de metal", "a-bucky", S.w("Bucky")),
               ("g3", "RED GUARDIAN", "súper soldado ruso", "a-redguardian", S.w("Red")),
               ("g4", "US AGENT", "John Walker", "a-walker", S.w("Iu Es"))], y=300)
    s = S.scene(S.w("Ghost"), bg="tinta", enter="cut")
    s.img("gh", im("a-ghost"), 80, 140, 560, 760, s.start + 0.02, frm="L", label="GHOST", pos="50% 20%")
    t = S.w("Sentry")
    still(s, "se", "sentry-thunderbolts", (700, 100, 1140, 860), t - 0.1, frm="R", label="SENTRY", pos="50% 30%", kb=S.peek("Tercero"), alt="a-thunder")
    t = S.w("más peligroso")
    s.sello("mp", "EL MÁS PELIGROSO", 1270, 880, t, color="rojo", rot=-7, size=70)

    # 3 · 4 Fantásticos
    s = S.scene(S.w("Tercero"), bg="ciencia", enter="whip", color="ciencia")
    still(s, "4f", "lf/lf04/4f-jardin", (110, 70, 1700, 940), s.start + 0.02, kb=S.peek("Cuarto"), scale=1.12)
    s.text("t3", "3 · CUATRO FANTÁSTICOS", "kw", "amarillo", 960, 110, s.start + 0.1, size=84, rot=-2, sfx=False)
    t = S.w("Reed")
    s.text("rs", "REED · SUE · JOHNNY · BEN", "kw", "papel", 960, 820, t, size=64, rot=-2)
    t = S.w("propio universo")
    s.text("ou", "¡DE OTRO UNIVERSO!", "ono", "amarillo", 1250, 300, t, size=110, rot=-6)

    # 4 · X-Men
    s = S.scene(S.w("Cuarto"), bg="papel", enter="pageflip")
    fondo(s, "bg4", (TR, 141.0), s.start + 0.02, S.peek("Nightcrawler"), dim=0.4)
    s.text("t4", "4 · LOS X-MEN DE SIEMPRE", "kw", "rojo", 960, 110, s.start + 0.1, size=84, rot=-2, sfx=False)
    fichas(s, [("x1", "MAGNETO", "amo del metal", "a-magneto", S.w("Magneto")),
               ("x2", "CÍCLOPE", "rayo óptico", "a-ciclope", S.w("Cíclope")),
               ("x3", "MYSTIQUE", "cambia de forma", "a-mistica", S.w("Mystique")),
               ("x4", "BESTIA", "genio y fuerza", "a-bestia", S.w("Bestia"))])
    s = S.scene(S.w("Nightcrawler"), bg="heroe", enter="whip", color="heroe")
    s.img("nc", im("a-nightcrawler"), 80, 140, 560, 760, s.start + 0.02, frm="L", label="NIGHTCRAWLER")
    t = S.w("Gámbito")
    s.img("gb", im("lf/lf04/gambito"), 680, 140, 560, 760, t - 0.1, frm="B", label="GÁMBITO")
    t = S.w("profesor")
    s.img("xv", im("a-xavier"), 1280, 140, 560, 760, t - 0.1, frm="R", label="PROFESOR X")

    # homenaje
    s = S.scene(S.w("Una nota"), bg="tinta", enter="cut", pat="")
    still(s, "ps", "a-xavier", (560, 90, 800, 760), s.start + 0.05, kb=S.peek("Y quinto"), frm="B", pos="50% 25%", scale=1.06)
    t = S.w("Patrick Stewart")
    s.text("ps", "SIR PATRICK STEWART · 1940–2026", "kw", "papel", 960, 950, t, size=64, rot=0, how="pop", sfx=False)
    t = S.w("Cada vez")
    s.text("gr", "GRACIAS, PROFESOR", "kw", "amarillo", 960, 120, t, size=60, rot=0, how="pop", sfx=False)

    # 5 · Talokan + Loki
    s = S.scene(S.w("Y quinto"), bg="heroe", enter="whip", color="heroe")
    fondo(s, "bg5", "namor", s.start + 0.02, S.peek("Namor"), dim=0.45)
    s.text("t5", "5 · TALOKAN", "kw", "amarillo", 520, 110, s.start + 0.1, size=84, rot=-2, sfx=False)
    t = S.w("Namor")
    s.img("nm", im("namor", "lf/shuri-mbaku"), 80, 200, 820, 720, t - 0.1, frm="L", label="NAMOR", pos="50% 25%")
    t = S.w("Loki")
    s.img("lk", im("loki-cuernos"), 1000, 200, 840, 720, t - 0.1, frm="R", label="LOKI · JUEGA SOLO", pos="50% 35%")
    t = S.w("sostiene")
    s.text("sm", "¡SOSTIENE EL MULTIVERSO!", "ono", "amarillo", 1420, 960, t, rot=-5)
