"""Short vertical (1080x1920) de LF04."""
from esc_largo._k import TR, I, ESTADO, _n, frame


def tag(s, k, at, out=None):
    _n[0] += 1
    txt, col = ESTADO[k]
    s.sello(f"tag{_n[0]}", txt, 250, 330, at, color=col, rot=-5, size=46, out=out)
    return s


def still(s, name, f, box, at, kb=None, frm="R", label=None, pos="50% 50%", scale=1.12, x=0, y=0, rot=0):
    l, t, w, h = box
    s.img(name, I + f + ".jpg", l, t, w, h, at, frm=frm, pos=pos, label=label, rot=rot)
    if kb:
        s.kenburns(name, at + 0.2, kb, scale=scale, x=x, y=y)
    return s


def clipsc(S, i, bg="tinta", enter="ink"):
    c = S.clip(i)
    s = S.scene(c["start"] - 0.25, bg=bg, enter=enter)
    d = c["end"] - c["start"]
    for k, (ft, at) in enumerate([(c["in"] + 0.05, s.start + 0.02), (c["in"] + d - 0.08, None)]):
        s.panel(f"f{k}{i}", f'<img src="assets/img/{frame(ft)}" style="width:100%;height:100%;object-fit:cover" />', 20, 640, 1040, 585, "tinta", 0, at, "B", sfx=False)
    s.js.append(f'tl.fromTo(q("#{s.id(f"f1{i}")}"), {{ autoAlpha: 0 }}, {{ autoAlpha: 1, duration: 0.01 }}, {s.T(c["end"] - 0.02)});')
    s.video(f"clip{i}", c["src"], c["in"], c["start"], c["end"] - c["start"], 20, 640, 1040, 585, tag="TRÁILER FINAL", frm="B", slam=False, bg="transparent")
    return s, c
