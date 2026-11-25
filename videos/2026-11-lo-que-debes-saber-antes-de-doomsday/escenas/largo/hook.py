"""HOOK + PROMESA."""
from lib_h import pho, ph, svgimg, L

LFV = ""  # migrado: las fuentes viven en assets/video/<id>.mp4


def build(S):
    # 1 · trono de Latveria (clip real, sin audio) + contador
    s = S.scene(S.t0, bg="tinta", enter="cut")
    s.video("trono", LFV + "lf-t01-latveria-victor-listo.mp4", 0.5, S.t0 + 0.05, S.peek("problema") - S.t0 - 0.2,
            110, 90, 1700, 760, slam=False, tint=None)
    s.kenburns("trono", S.t0, S.peek("problema"), scale=1.08)
    t = S.w("treinta y tres")
    s.text("33", "33 DÍAS", "ttl", "amarillo", 960, 470, t, size=220, rot=-4, misreg=True)
    t = S.w("Avengers")
    s.raw(f'<div class="c" style="left:960px;top:760px"><div id="{s.id("logo")}">{svgimg("doomsday-logo.png", 760, 190, "filter:drop-shadow(8px 8px 0 #0B0B14)")}</div></div>')
    s.code(f'COM.popIn(tl, q("#{s.id("logo")}"), {s.T(t)}, {{ rot: -3 }});')
    s.sfx("braam", t, -6)

    # 2 · pila de títulos que se sale de la pantalla
    s = S.scene(S.w("problema", -0.2), bg="papel", enter="halftone", color="rojo")
    covers = ["a-strange-poster.jpg", "a-brave.jpg", "a-thunder.jpg", "a-fantastic4.jpg", "a-visionquest.jpg",
              "a-lokilogo.jpg", "a-spider3.jpg", "a-redhulk.jpg", "a-xavier.jpg", "a-wanda.jpg", "a-thor.jpg", "a-kang.jpg"]
    t0 = S.w("entender")
    for k, c in enumerate(covers):
        x = 140 + (k % 6) * 290
        y = 120 + (k // 6) * 400
        s.img(f"p{k}", c, x, y, 260, 360, t0 + k * 0.16, frm="T" if k % 2 else "B", rot=(-3, 2, -2, 3)[k % 4])
    t = S.w("más de treinta")
    s.text("mas30", "+30 TÍTULOS", "ono", "rojo", 960, 540, t, rot=-7, hold=1.6, zoom=True)

    # 3 · yo ya lo hice → 15 datos
    s = S.scene(S.w("No tienes"), bg="heroe", enter="pageflip")
    s.cap("cap1", "NO TIENES QUE VERLO TODO", S.t0 + 0.01 if False else s.start + 0.1, left=80, top=80, width=760)
    t = S.w("Yo ya lo hice")
    s.globo("yo", "YO YA LO HICE", 1120, 150, 600, 220, t, rot=3)
    t = S.w("quince")
    s.text("15", "15", "ttl", "amarillo", 760, 600, t, size=420, rot=-6, misreg=True, zoom=True)
    s.text("datos", "DATOS", "kw", "papel", 1240, 640, t + 0.25, rot=-6)
    for k in range(15):
        s.raw(f'<div class="c" style="left:{170 + k*112}px;top:930px"><div id="{s.id(f"c{k}")}" style="width:92px;height:92px;background:#FFD400;border:6px solid #0B0B14;box-shadow:6px 6px 0 #0B0B14;font:400 52px/80px Anton;text-align:center;color:#0B0B14">{k+1}</div></div>')
        s.code(f'COM.popIn(tl, q("#{s.id(f"c{k}")}"), {s.T(t + 0.5 + k*0.06)}, {{ rot: {(-8, 6)[k % 2]} }});')
    t = S.w("sentido")
    s.sello("sent", "TODO TIENE SENTIDO", 960, 280, t, color="tinta", rot=-4)

    # 4 · "escucha esta frase" → clip «vidas robadas»
    t = S.w("escucha")
    s = S.scene(t, bg="tinta", enter="ink", x=960, y=540)
    s.text("esc", "¡ESCUCHA!", "ono", "amarillo", 960, 520, t + 0.05, rot=-6, hold=0.8)
    c = S.clip(0)
    s.video("vidas", c["src"], c["in"], c["start"], c["end"] - c["start"], 210, 110, 1500, 640, tag="TRÁILER OFICIAL", frm="B")
    s.globo("g", "VIDAS ROBADAS", 1180, 760, 560, 200, c["start"] + 1.0, rot=-3, size=56)

    # 5 · ¿robadas por quién? Doom dibujado
    s = S.scene(S.w("Robadas"), bg="doom", enter="halftone", color="doom", pat="pat-benday-fuerte")
    s.svg("doom", "lf/doom-frente.svg", 520, 600, 620, 806, s.start + 0.05, how="drop", bob=S.peek("Vamos"))
    s.globo("q", "¿ROBADAS POR QUIÉN?", 980, 140, 780, 230, s.start + 0.2, kind="nube", size=60, rot=2)
    t = S.w("devolver")
    s.text("dev", "¿QUÉ QUIERE DEVOLVER?", "kw", "amarillo", 1370, 560, t, size=96, rot=-5)
    t = S.w("Al final")
    s.cap("fin", "LA RESPUESTA, AL FINAL", t, left=1060, top=760, width=700)
    t = S.w("héroes más queridos")
    s.slab("rojo", "rojo", t - 0.05, t + 0.9)
    s.text("q2", "¿QUIÉN?", "ono", "papel", 960, 540, t, rot=-8, hold=0.8)
    s.sfx("heartbeat", t, -2)

    # 6 · mapa del video
    s = S.scene(S.w("Vamos en orden"), bg="papel", enter="pageflip")
    items = [("villano", "EL VILLANO", "doom"), ("multiverso", "EL MULTIVERSO", "multi"), ("bandos", "LOS BANDOS", "heroe"),
             ("Doom prepara", "EL PLAN DE DOOM", "rojo"), ("cada Avenger", "BONUS: LOS AVENGERS", "amarillo")]
    for k, (word, lab, col) in enumerate(items):
        t = S.w(word)
        inner = f'<div style="font:400 64px/1.05 Anton;color:{"#0B0B14" if col == "amarillo" else "#FFF3D6"};text-align:center;padding:10px;-webkit-text-stroke:0">{lab}</div>'
        s.panel(f"m{k}", inner, 70 + k * 362, 300 + (k % 2) * 60, 330, 420, col, rot=(-3, 2, -2, 3, -1)[k], at=t, frm="B")
        s.text(f"n{k}", str(k + 1) if k < 4 else "+", "ttl", "amarillo", 235 + k * 362, 270 + (k % 2) * 60, t + 0.1, size=110, rot=-6, sfx=False)
    t = S.w("Empezamos")
    s.text("go", "¡EMPEZAMOS!", "ono", "rojo", 960, 880, t, rot=-5, hold=1.2)
