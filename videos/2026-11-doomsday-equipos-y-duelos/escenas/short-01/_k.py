"""Short vertical (1080x1920): Thor vs Doctor Doom."""
from esc_largo._k import ESTADO, _n, im, frame, T1, TR

def tag(s, k, at, out=None, x=250, y=330, size=46):
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, x, y, at, color=col, rot=-5, size=size, out=out)
    return s

def still(s, name, i, box, at, kb=None, frm="R", label=None, pos="50% 50%", scale=1.12, x=0, y=0, rot=0, alt=None):
    l, t, w, h = box
    s.img(name, im(i, alt), l, t, w, h, at, frm=frm, pos=pos, label=label, rot=rot)
    if kb:
        s.kenburns(name, at + 0.2, kb, scale=scale, x=x, y=y)
    return s

def vid(s, name, src, tin, at, dur, box=(0, 0, 1080, 1920), pos="50% 50%", tag_txt=None):
    l, t, w, h = box
    s.video(name, src, tin, at, dur, l, t, w, h, tag=tag_txt, frm="B", slam=False, pos=pos)
    return s

def clipsc(S, i, bg="tinta", enter="cut", box=(0, 560, 1080, 1080), pos="62% 50%"):
    c = S.clip(i)
    s = S.scene(c["start"] - 0.2, bg=bg, enter=enter)
    l, t, w, h = box
    d = c["end"] - c["start"]
    s.panel(f"fa{i}", f'<img src="assets/img/{frame(c["src"], c["in"] + 0.05)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}" />', l, t, w, h, "tinta", 0, s.start + 0.02, "B", sfx=False)
    s.video(f"clip{i}", c["src"], c["in"], c["start"], d, l, t, w, h, tag="TRÁILER", frm="B", slam=False, bg="transparent", pos=pos)
    return s, c
