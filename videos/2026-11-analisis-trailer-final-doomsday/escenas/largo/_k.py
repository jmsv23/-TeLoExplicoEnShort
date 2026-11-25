"""Piezas comunes de LF04 (análisis del tráiler final oficial).

TR  = el tráiler completo (con subtítulos ES quemados); los tiempos son segundos del tráiler.
I   = fotogramas fijos sacados del tráiler (assets/img/lf/lf04/*.jpg)
tag(s, k, at)          sello de estado arriba a la izquierda
clipsc(S, i, ...)      escena a pantalla casi completa para el i-ésimo clip CON AUDIO de la sección
tv(s, name, tin, at, dur, box)   trozo del tráiler sin audio dentro de una viñeta
still(s, name, f, box, at, kb)   fotograma fijo con ken burns hasta kb
"""
LFV = ""  # migrado: las fuentes viven en assets/video/<id>.mp4
TR = LFV + "lf04-trailer.mp4"
I = "lf/lf04/"
SV = "lf/lf02-"

ESTADO = {"C": ("CONFIRMADO", "heroe"), "T": ("TEORÍA", "multi"), "L": ("LECTURA", "rojo"),
          "K": ("DATO DE CÓMIC", "doom"), "F": ("FILTRACIÓN", "rojo")}
_n = [0]
FULL = (130, 60, 1660, 934)


def tag(s, k, at, out=None):
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, 230, 90, at, color=col, rot=-5, size=42, out=out)
    return s


def tv(s, name, tin, at, dur, box=FULL, tag_txt="TRÁILER FINAL", frm="R", slam=True, rot=0, pos="50% 50%"):
    l, t, w, h = box
    s.video(name, TR, tin, at, dur, l, t, w, h, tag=tag_txt, frm=frm, slam=slam, rot=rot, pos=pos)
    return s


def frame(t):
    """fotograma completo (sin recortar) del tráiler en t → archivo relativo a IMG (cacheado)."""
    import subprocess
    from lib_h import MOTION, IMG
    name = f"clip-{t:.2f}.jpg"
    dst = MOTION / IMG / I / name
    if not dst.exists():
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", str(MOTION / "assets/video" / TR),
                        "-frames:v", "1", "-q:v", "3", str(dst), "-y"], check=True)
    return I + name


def clipsc(S, i, bg="tinta", enter="ink", box=FULL, cap=None, cap_at=0.8):
    """escena del clip i con audio: el video ocupa casi toda la pantalla para que se lean los subtítulos quemados.
    Detrás del video van el primer y el último fotograma congelados (sin huecos negros antes y después)."""
    c = S.clip(i)
    s = S.scene(c["start"] - 0.3, bg=bg, enter=enter)
    l, t, w, h = box
    d = c["end"] - c["start"]
    s.panel(f"fa{i}", f'<img src="assets/img/{frame(c["in"] + 0.05)}" style="width:100%;height:100%;object-fit:cover" />', l, t, w, h, "tinta", 0, s.start + 0.02, "B")
    s.panel(f"fz{i}", f'<img src="assets/img/{frame(c["in"] + d - 0.08)}" style="width:100%;height:100%;object-fit:cover" />', l, t, w, h, "tinta", 0, None, "B", sfx=False)
    s.js.append(f'tl.fromTo(q("#{s.id(f"fz{i}")}"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.01 }}, {s.T(c["end"] - 0.02)});')
    s.video(f"clip{i}", c["src"], c["in"], c["start"], c["end"] - c["start"], l, t, w, h, tag="TRÁILER FINAL", frm="B", slam=False, bg="transparent")
    if cap:
        s.cap(f"cap{i}", cap, c["start"] + cap_at, left=60, top=60, width=900)
    return s, c


def still(s, name, f, box, at, kb=None, frm="R", label=None, pos="50% 50%", scale=1.12, x=0, y=0, rot=0):
    l, t, w, h = box
    s.img(name, I + f + ".jpg", l, t, w, h, at, frm=frm, pos=pos, label=label, rot=rot)
    if kb:
        s.kenburns(name, at + 0.2, kb, scale=scale, x=x, y=y)
    return s
