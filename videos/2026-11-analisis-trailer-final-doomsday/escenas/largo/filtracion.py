"""11 · ¿Acertó la filtración? Marcador 4 ✅ · 4 🟡 · 5 ❌ (cierra el bucle 2)."""
from esc_largo._k import tag, still


def build(S):
    s = S.scene(S.t0, bg="papel", enter="pageflip")
    tag(s, "F", S.t0 + 0.1)
    rows = [("acertó", "THOR + STEVE", "✓", "heroe"), ("Cíclope", "CÍCLOPE", "✓", "heroe"), ("Bestia", "BESTIA", "✓", "heroe"),
            ("contador", "CONTADOR", "✓", "heroe"), ("Latveria", "ABRE EN LATVERIA", "✗", "rojo"),
            ("Wolverine", "WOLVERINE", "✗", "rojo"), ("Deadpool", "DEADPOOL", "✗", "rojo"), ("Loki", "LOKI", "✗", "rojo"),
            ("Magneto", "MAGNETO", "✗", "rojo")]
    for k, (w, txt, mk, col) in enumerate(rows):
        t = S.w(w)
        x, y = (520 if k < 4 else 1400), (260 + (k if k < 4 else k - 4) * 125)
        s.text(f"r{k}", f"{mk} {txt}", "kw", "tinta" if mk == "✓" else "rojo", x, y, t, size=62, rot=-2, how="pop", sfx=False)
        s.sfx("stamp" if mk == "✗" else "pop", t, -6)
    t = S.w("perdonarán")
    s.text("pd", "«ALGÚN DÍA ME PERDONARÁN» ✗", "kw", "rojo", 960, 950, t - 0.6, size=64, rot=-2)

    s = S.scene(S.w("Cuatro aciertos"), bg="tinta", enter="cut")
    s.text("sc", "4 / 13", "ttl", "amarillo", 960, 420, s.start + 0.05, size=300, rot=-4, misreg=True)
    t = S.w("guardó todo")
    s.text("cine", "¿GUARDADO PARA EL CINE?", "kw", "papel", 960, 760, t, size=70, rot=-2)
    t = S.w("puro cuento")
    s.text("pc", "…¿O PURO CUENTO?", "ono", "rojo", 960, 930, t, rot=-5)
