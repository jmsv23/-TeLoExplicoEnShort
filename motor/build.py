"""Proyecto HyperFrames de una pieza: build/timeline-<pieza>.json + escenas/<pieza>.py + el estilo del video.

Cada sección del guion es una sub-composición. Dentro, los planos (shots) que declara escenas/<pieza>.py
se encadenan con las transiciones del estilo, y los elementos aparecen cuando la voz los nombra
(S.w("frase") = tiempo real de la frase en la alineación de WhisperX).

El estilo (estilos/<slug>/estilo.py) es un plugin: aporta CSS, helpers JS, los renderers r_<tipo>,
TRANS/trans_js, sfx_de y el tratamiento de imagen. El motor le inyecta W, H, V, AS, esc, wspan, norm,
HF, A_IMG, A_CUT, PIEZA, SFX, ESTILO_DIR y VIDEO antes de usarlo. Contrato completo: estilos/CONTRATO.md.
"""
import html
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import unicodedata

from .proyecto import CONFIG, ROOT, die
from .voz import dur


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", s)


def esc(s):
    return html.escape(str(s), quote=True)


def wspan(text, cls="w"):
    return " ".join(f'<span class="{cls}">{esc(x)}</span>' for x in text.split())


def ff(*args):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *map(str, args)], check=True)


# -------------------------------------------------------------------- assets usados por la pieza
class Assets:
    def __init__(self, v, hf, estilo):
        self.v, self.hf, self.E = v, hf, estilo
        self.used = {}

    def _bn(self, bn):
        return getattr(self.E, "BN_DEFAULT", False) if bn is None else bn

    def img(self, name, bn=None):
        bn = self._bn(bn)
        key = f"img/{name}{'-bn' if bn else ''}.jpg"
        self.used[key] = ("img", name, bn)
        return "assets/" + key

    def vid(self, name, bn=False):
        key = f"video/{name}{'-bn' if bn else ''}.mp4"
        self.used[key] = ("vid", name, bn)
        return "assets/" + key

    def prepare(self, master, t0=None, tot=None):
        E, faltan = self.E, []
        for key, (kind, name, bn) in self.used.items():
            out = self.hf / "assets" / key
            out.parent.mkdir(parents=True, exist_ok=True)
            if kind == "img":
                src = next((p for p in sorted(self.v.a_img.glob(f"{name}.*")) if p.suffix.lower() in
                            (".jpg", ".jpeg", ".png", ".webp", ".avif")), None)
            else:
                src = self.v.a_cut / f"{name}.mp4"
                src = src if src.exists() else None
            if src is None:
                faltan.append(f"{kind} {name}")
                continue
            if out.exists() and out.stat().st_mtime > src.stat().st_mtime:
                continue
            if kind == "img":
                ff("-i", src, "-vf", E.IMG_VF(bn), "-q:v", "3", out)
            else:
                vf = E.VID_VF(bn) if hasattr(E, "VID_VF") else None
                if vf:
                    ff("-i", src, "-an", "-vf", vf, "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out)
                else:
                    ff("-i", src, "-an", "-c:v", "copy", out)
        if faltan:
            die("faltan assets (ver assets/manifest.json → ./tl assets fetch):\n  " + "\n  ".join(faltan))
        fd = self.hf / "assets/fonts"
        fd.mkdir(parents=True, exist_ok=True)
        fonts = E.ESTILO_DIR / "fonts"
        for f in (fonts.iterdir() if fonts.exists() else []):
            shutil.copy(f, fd / f.name)
        au = self.hf / "assets/audio"
        au.mkdir(parents=True, exist_ok=True)
        if t0 is not None:
            ff("-ss", f"{t0:.4f}", "-t", f"{tot:.4f}", "-i", master, "-c:a", "pcm_s16le", au / "master.wav")
        else:
            shutil.copy(master, au / "master.wav")


# -------------------------------------------------------------------- sección / anclas
class Seccion:
    def __init__(self, sec, beats, tts_text):
        self.id, self.t0, self.t1 = sec["id"], sec["start"], sec["end"]
        self.beats = [b for b in beats if b["sec"] == self.id]
        self.words = [(norm(w), s, e) for b in self.beats if b["type"] == "vo" for w, s, e in b["words"]]
        self.shots = []
        self._tts = tts_text

    def w(self, frase, n=1, after=None, end=False):
        """Tiempo absoluto de la n-ésima aparición de la frase (desde 'after'). end=True → fin de la frase."""
        ws = self.words
        after = self.t0 if after is None else after
        for variante in (frase, self._tts(frase)):
            q = [x for x in norm(variante).split() if x]
            k = 0
            for i in range(len(ws) - len(q) + 1):
                if ws[i][1] + 1e-3 < after:
                    continue
                if all(ws[i + j][0] == q[j] for j in range(len(q))):
                    k += 1
                    if k == n:
                        return ws[i + len(q) - 1][2] if end else ws[i][1]
        raise KeyError(f"[{self.id}] no encuentro «{frase}»")

    def clip_beat(self, name):
        for b in self.beats:
            if b["type"] == "clip" and b["clip"] == name:
                return b
        raise KeyError(f"[{self.id}] no hay clip {name}")

    def add(self, tipo, t, entrada="fundido", **p):
        self.shots.append(dict(tipo=tipo, t=max(self.t0, t - 0.12), entrada=entrada, p=p))
        return self


def cargar(nombre, path, contexto=None):
    """Importa un .py suelto. `contexto` se inyecta antes de ejecutarlo (el estilo usa W/H/V al importarse)."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    for k, val in (contexto or {}).items():
        setattr(mod, k, val)
    spec.loader.exec_module(mod)
    return mod


def cargar_estilo(v, pieza, hf):
    d = v.estilo_dir()
    V = v.vertical(pieza)
    W, H = (1080, 1920) if V else (1920, 1080)
    ctx = dict(V=V, W=W, H=H, esc=esc, wspan=wspan, norm=norm, HF=hf, A_IMG=v.a_img, A_CUT=v.a_cut, PIEZA=pieza,
               ESTILO_DIR=d, VIDEO=v, SFX=[])
    E = cargar(f"estilo_{v.estilo.replace('-', '_')}", d / "estilo.py", ctx)
    E.AS = Assets(v, hf, E)
    E.RENDER = {k[2:]: f for k, f in vars(E).items() if k.startswith("r_") and callable(f)}
    return E


def build_section(E, S):
    shots = sorted(S.shots, key=lambda s: s["t"])
    for i, sh in enumerate(shots):
        nxt = shots[i + 1] if i + 1 < len(shots) else None
        sh["end"] = (nxt["t"] + E.TRANS[nxt["entrada"]] + 0.05) if nxt else S.t1 + 0.4
        if sh["tipo"] == "clip":
            b = S.clip_beat(sh["p"]["clip"])
            sh["clip_start"], sh["clip_end"] = b["start"], b["end"]
    du = S.t1 - S.t0 + 0.5
    L = lambda t: max(0.0, t - S.t0)  # noqa: E731
    body, js = [], [E.JS_HELPERS]
    for i, sh in enumerate(shots):
        E.SFX.extend(E.sfx_de(sh, i == 0))
        pid = f"{S.id}-s{i:02d}"
        if sh["tipo"] not in E.RENDER:
            die(f"[{S.id}] el estilo {E.VIDEO.estilo} no tiene el plano «{sh['tipo']}» (tiene: {', '.join(sorted(E.RENDER))})")
        inner, j = E.RENDER[sh["tipo"]](pid, sh, L)
        if hasattr(E, "post_shot"):
            h2, j2 = E.post_shot(pid, sh, L, i)
            inner, j = inner + h2, j + j2
        vis = ";opacity:1" if i == 0 and sh["entrada"] == "corte" and L(sh["t"]) < 0.05 else ""
        body.append(f'<div id="{pid}" class="shot" style="z-index:{i + 1}{vis}">{inner}</div>')
        prev = f"{S.id}-s{i - 1:02d}" if i else None
        js.append(E.trans_js(pid, prev, sh["entrada"], L(sh["t"])))
        js.append(j)
        js.append(f'tl.set("#{pid}",{{opacity:0}},{L(sh["end"]):.3f});')
    js.append(f'tl.set({{}},{{}},{du:.3f});window.__timelines["{S.id}"] = tl;')
    doc = (f'<template>\n<style>{E.CSS}</style>\n'
           f'<div id="root" data-composition-id="{S.id}" data-width="{E.W}" data-height="{E.H}" data-layout-allow-overflow data-layout-allow-overlap>\n'
           + "\n".join(body) +
           '\n</div>\n<script>\n' + "\n".join(js) + '\n</script>\n</template>\n')
    (E.HF / "compositions").mkdir(parents=True, exist_ok=True)
    (E.HF / "compositions" / f"{S.id}.html").write_text(doc)
    return du


def escenas_de(v, pieza):
    f = v.dir / "escenas" / f"{pieza}.py"
    if not f.exists() and v.vertical(pieza):
        f = v.dir / "escenas" / "shorts.py"
    if not f.exists():
        die(f"falta escenas/{pieza}.py")
    if str(f.parent) not in sys.path:
        sys.path.insert(0, str(f.parent))  # las escenas de los shorts pueden importar datos de escenas/largo.py
    return cargar(f"escenas_{pieza.replace('-', '_')}", f)


def proyecto_hf(hf, nombre):
    hfv = CONFIG["hyperframes"]
    hf.mkdir(parents=True, exist_ok=True)
    (hf / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True}, "authoringSkill": "hyperframes"}, indent=2))
    (hf / "package.json").write_text(json.dumps({
        "name": nombre, "private": True, "type": "module",
        "scripts": {k: f"npx --yes hyperframes@{hfv} {k}" for k in ("preview", "check", "render")}}, indent=2))


def build(v, pieza, parte=None):
    """parte=(a, b) → solo las secciones [a, b) en su propio proyecto hf-<pieza>-p<a> (renders largos por partes).
    Con un estilo de motor propio, parte = índice de su parte."""
    tl_path = v.build / f"timeline-{pieza}.json"
    if not tl_path.exists():
        die(f"falta {tl_path.relative_to(ROOT)}: corre antes ./tl voz {v.slug} {pieza}")
    tl = json.loads(tl_path.read_text())
    suf = "" if parte is None else f"-p{parte[0] if isinstance(parte, tuple) else parte}"
    hf = v.build / f"hf-{pieza}{suf}"
    proyecto_hf(hf, hf.name)
    E = cargar_estilo(v, pieza, hf)
    if hasattr(E, "build_pieza"):  # estilo con motor propio (p. ej. comic): devuelve (hf, nº de partes)
        return E.build_pieza(v, pieza, hf, parte)
    esc_mod = escenas_de(v, pieza)
    master = v.build / "audio" / pieza / "master.wav"
    total = dur(master)
    secs = tl["sections"]
    t0p, totp = 0.0, None
    if parte:
        a, b = parte
        secs = secs[a:b]
        fps = CONFIG["fps"]
        t0p = round(secs[0]["start"] * fps) / fps
        fin = secs[-1]["end"] if b < len(tl["sections"]) else total
        totp = round(fin * fps) / fps - t0p
    hosts = []
    for sec in secs:
        S = Seccion(sec, tl["beats"], v.tts_text)
        fn = getattr(esc_mod, S.id.replace("-", "_"), None)
        if fn is None:
            die(f"escenas/{pieza}.py no define def {S.id.replace('-', '_')}(S)")
        fn(S)
        d = min(build_section(E, S), total - S.t0)
        if parte:
            d = min(d, t0p + totp - S.t0)
        hosts.append(f'<div id="{S.id}" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" '
                     f'data-start="{S.t0 - t0p:.3f}" data-duration="{d:.3f}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="{E.W}" data-height="{E.H}" style="z-index:{len(hosts) + 1}"></div>')
        print(f"  {S.id:12s} {S.t0:7.1f}–{S.t1:7.1f}  {len(S.shots):2d} planos")
    if parte:
        total = totp
    W, H, bg = E.W, E.H, getattr(E, "INDEX_BG", "#000")
    grano = getattr(E, "GRANO_CSS", None)
    grano_div = (f'<div id="grano" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="9" data-layout-ignore></div>'
                 if grano else "")
    extra = E.index_extra(total) if hasattr(E, "index_extra") else ""
    index = f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{bg}}}
#main{{position:relative;width:100%;height:100%;background:{bg}}}
{('#grano{' + grano + '}') if grano else ''}</style>
</head><body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
<audio id="voz" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0" data-volume="1" src="assets/audio/master.wav"></audio>
{chr(10).join(hosts)}
{grano_div}{extra}
</div>
<script>window.__timelines = window.__timelines || {{}}; const tl = gsap.timeline({{paused:true}}); tl.set({{}},{{}},{total:.3f}); window.__timelines["main"] = tl;</script>
</body></html>
"""
    (hf / "index.html").write_text(index)
    if not parte:
        (v.build / f"sfx-{pieza}.json").write_text(json.dumps(sorted(E.SFX), indent=0))
    E.AS.prepare(master, t0p if parte else None, totp)
    print(f"✓ {hf.name}: {len(hosts)} secciones · {total:.1f} s · {len(E.AS.used)} assets · estilo {v.estilo}")
    return hf, len(tl["sections"])


def catalogo(slug):
    """Planos (r_<tipo>) con su docstring, transiciones y SFX de un estilo, sin necesidad de un video."""
    d = ROOT / "estilos" / slug
    if not (d / "estilo.py").exists():
        die(f"no existe estilos/{slug}/estilo.py")
    ctx = dict(V=False, W=1920, H=1080, esc=esc, wspan=wspan, norm=norm, HF=d, A_IMG=d, A_CUT=d, PIEZA="largo",
               ESTILO_DIR=d, VIDEO=None, SFX=[])
    E = cargar(f"cat_{slug}", d / "estilo.py", ctx)
    if hasattr(E, "catalogo"):
        return E.catalogo()
    print(f"Estilo {slug} · planos para S.add(tipo, t, entrada, **params)\n")
    for k, f in vars(E).items():
        if k.startswith("r_") and callable(f):
            doc = " ".join((f.__doc__ or "").split())
            print(f"  {k[2:]:14s} {doc}")
    print(f"\n  entradas: {', '.join(E.TRANS)}")
    print(f"  SFX: {', '.join(getattr(E, 'SFX_GAIN', {}))}")
