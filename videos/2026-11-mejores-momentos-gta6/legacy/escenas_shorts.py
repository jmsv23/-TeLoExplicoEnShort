"""Dirección visual de los 2 Shorts (9:16). Una función por Short. Cierran con "cta" hacia el largo (TOP 12)."""
from escenas_largo import SUBS

DUR_LARGO = "9:18"


def corrido(nombre, off, dur):
    """Subtítulos del corte largo desplazados al corte del Short (off = inicio_short - inicio_largo)."""
    out = []
    for a, b, t in SUBS[nombre]:
        a, b = a - off, b - off
        if b > 0.3 and a < dur - 0.3:
            out.append((max(0.0, a), min(dur, b), t))
    return out


def cta(S, frase, kick="LOS OTROS 11", titulo="EN MI CANAL"):
    S.add("cta", S.w(frase), "flash", video="lirik-perro", desde=12, kick=kick, titulo=titulo, en_mini="TOP 12", dur=DUR_LARGO,
          tt=S.w(frase) + 0.6)


def s1(S):
    w = S.w
    S.add("rank", w("Esperó trece años"), "corte", num="1", kick="EL MOMENTO MÁS VIRAL DE GTA VI", nombre="ILLOJUAN",
          sub="Esperó 13 años… y lo borró en directo.", video="illo-borra", desde=31, tn=w("Esperó") + 0.05, tt=w("trece años"), ts=w("Lo abrió"))
    S.add("titulo", w("y lo borró"), "flash", kick="GTA VI", l1="Y LO", l2="BORRÓ", t1=w("y lo"), t2=w("borró"), fs2=260)
    S.add("panel", w("IlloJuan quiso"), "panel", video="illo-borra", desde=0, kick="MEMORIA MUSCULAR", tk=w("memoria muscular"),
          titulo="¿CERRAR O ELIMINAR?", tt=w("botón de eliminar"), fst=120)
    b = S.clip_beat("illo-borra-s")
    S.add("clip", b["start"] - 0.3, "corte", clip="illo-borra-s", tag="#1 · ILLOJUAN", titulo="BORRÓ GTA VI", cam=(44, 310, 296, 306),
          subs=corrido("illo-borra", 21.0, b["end"] - b["start"]))
    cta(S, "Y este es solo")


def s2(S):
    w = S.w
    S.add("titulo", w("Tres streamers"), "corte", kick="PRIMER DÍA", l1="3 STREAMERS QUE", l2="GTA VI HUMILLÓ", t1=w("Tres streamers"),
          t2=w("humilló"), fs2=170)
    for nombre, frase, clip, desde, sub, n, off, tag, cam in (
            ("KAI CENAT", "Kai Cenat quiso", "kai-techo-s", 0, "Quiso bajar rápido de una azotea.", "1", 4.5, "KAI CENAT", (4, 430, 386, 230)),
            ("PAPAPLATTE", "Papaplatte vio", "papa-gas-s", 0, "Vio una gasolinera… y tuvo una idea.", "2", 7.5, "PAPAPLATTE", (1476, 100, 440, 340)),
            ("WILLYREX", "Y Willyrex", "willy-coco-s", 0, "Se metió al agua sin ver al caimán.", "3", 9.0, "WILLYREX", (1540, 250, 360, 326))):
        S.add("rank", w(frase), "flash", num=n, pref="", kick=f"HUMILLADO {n} DE 3", nombre=nombre, sub=sub, video=clip, desde=desde,
              tn=w(frase) + 0.05, tt=w(frase) + 0.3, ts=w(frase) + 0.6)
        b = S.clip_beat(clip)
        S.add("clip", b["start"] - 0.3, "corte", clip=clip, tag=tag, cam=cam, subs=corrido(clip.removesuffix("-s"), off, b["end"] - b["start"]))
    cta(S, "Y ninguno llegó", kick="¿Y EL #1?", titulo="TOP 12 EN MI CANAL")
