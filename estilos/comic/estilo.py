"""Estilo «comic» (Camino a Doomsday) — plugin con motor propio (contrato: estilos/CONTRATO.md → «motor propio»).

A diferencia de los estilos de planos (r_<tipo>), aquí las escenas se escriben con la API de escenas de
lib_h.py (S.scene(...) → s.text / s.panel / s.img / s.video / s.sello / s.cap / s.globo / s.ficha …), portada
del generador de los long-form LF01-LF04. Este módulo:
  - adapta build/timeline-<pieza>.json (./tl voz) al formato del motor,
  - carga escenas/<pieza>/ (un .py por sección con build(S); helpers en _k.py) o escenas/<pieza>.py (def <sec>(S)),
  - construye una composición por PARTE (grupo de secciones) y el index que las encadena,
  - y mezcla con su propio criterio (música por sección, SFX de cómic con variantes, ducking bajo clips).

Config por pieza en video.json → piezas[i]["comic"]:
  {"partes": [["p1", ["hook", "d1", "d2"]], ...],   # por defecto: 3 secciones por parte (largo) / todo junto (short)
   "dias": 24,                                        # contador «FALTAN N DÍAS» (null = sin contador)
   "placa": ["d(\\\\d+)", "DETALLE", 10]}              # placa «DETALLE N / 10» en las secciones que casen
Música en video.json → "musica": {"comic": {"hook": "hook", "d1": "misterio", ...}} (pistas audio-lib/musica/comic-<x>.wav).
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
import lib_h as LH  # noqa: E402

ROOT = AQUI.parents[1]
MUS = ROOT / "audio-lib/musica"
SFXD = ROOT / "audio-lib/sfx/comic"
GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"


# ------------------------------------------------------------------ timeline del canal → timeline del motor
def timeline_motor(v, pieza):
    tl = json.loads((v.build / f"timeline-{pieza}.json").read_text())
    if "words" in tl:  # ya viene en formato del motor (timeline.json de los LF migrados)
        return tl
    cortes = {}
    mf = v.dir / "assets/manifest.json"
    if mf.exists():
        cortes = {c["id"]: c for c in json.loads(mf.read_text()).get("cortes", [])}
    out = {"sections": {s["id"]: [s["start"], s["end"]] for s in tl["sections"]}, "words": [], "blocks": [], "clips": []}
    n = {}
    for b in tl["beats"]:
        if b["type"] == "vo":
            out["words"] += [[w, a, e, b["id"]] for w, a, e in b["words"]]
            out["blocks"].append({"id": b["id"], "sec": b["sec"], "type": "vo", "start": b["start"], "end": b["end"], "text": b["text"]})
        else:
            n[b["sec"]] = n.get(b["sec"], 0) + 1
            c = cortes.get(b["clip"], {})
            # el video mudo sale de la fuente completa (como en los LF): src + in del manifiesto; si no hay fuente, del corte
            src, tin = ((f"{c['fuente']}.mp4", c["inicio"]) if c.get("fuente") and (v.a_vid / f"{c['fuente']}.mp4").exists()
                        else (f"cortes/{b['clip']}.mp4", 0.0))
            d = b["end"] - b["start"]
            out["clips"].append({"id": b["id"], "sec": b["sec"], "clip": b["clip"], "src": src, "in": tin, "out": round(tin + d, 3),
                                 "start": b["start"], "end": b["end"]})
            out["blocks"].append({"id": b["id"], "sec": b["sec"], "type": "clip", "start": b["start"], "end": b["end"]})
    out["dur"] = tl.get("duration") or tl["sections"][-1]["end"]
    return out


# ------------------------------------------------------------------ escenas
def _registrar_paquete(nombre, d):
    init = d / "__init__.py"
    if not init.exists():
        init.write_text("")
    spec = importlib.util.spec_from_file_location(nombre, init, submodule_search_locations=[str(d)])
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)


def paquete(pieza):
    return "esc_" + pieza.replace("-", "_")


def cargador_escenas(v, pieza):
    """Registra los paquetes escenas/<pieza>/ de todo el video (los shorts importan helpers del largo:
    `from esc_largo._k import still`) y devuelve sid → build(S)."""
    ed = v.dir / "escenas"
    for d in sorted(p for p in ed.iterdir() if p.is_dir() and not p.name.startswith("_")) if ed.exists() else []:
        _registrar_paquete(paquete(d.name), d)
    if (ed / pieza).is_dir():
        return None  # lib_h importa <paquete>.<sid> y llama build(S)
    f = ed / f"{pieza}.py"
    if not f.exists() and v.vertical(pieza):
        f = ed / "shorts.py"
    if not f.exists():
        raise SystemExit(f"falta escenas/{pieza}/ (un .py por sección) o escenas/{pieza}.py")
    spec = importlib.util.spec_from_file_location(paquete(pieza) + "_mod", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def escena(sid):
        fn = getattr(mod, sid.replace("-", "_"), None)
        if fn is None:
            raise SystemExit(f"{f.name} no define def {sid.replace('-', '_')}(S)")
        return fn
    return escena


def cfg_pieza(v, pieza):
    return v.pieza(pieza).get("comic", {})


def partes_de(v, pieza, tl=None):
    c = cfg_pieza(v, pieza)
    if c.get("partes"):
        return [(n, list(s)) for n, s in c["partes"]]
    tl = tl or timeline_motor(v, pieza)
    sids = list(tl["sections"])
    if v.vertical(pieza):
        return [("s1", sids)]
    return [(f"p{i // 3 + 1}", sids[i:i + 3]) for i in range(0, len(sids), 3)]


def configurar(v, pieza, tl):
    c = cfg_pieza(v, pieza)
    parts = partes_de(v, pieza, tl)
    esc = cargador_escenas(v, pieza)
    LH.configurar(v.dir, tl, parts, secs=paquete(pieza), size=(1080, 1920) if v.vertical(pieza) else (1920, 1080),
                  dias=c.get("dias"), placa=tuple(c.get("placa") or (r"^$", "", 0)), cid=f"comic-{pieza}", escena=esc)
    return parts


# ------------------------------------------------------------------ build (lo llama motor/build.py)
def _enlazar(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.stat().st_mtime >= src.stat().st_mtime:
            return
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def build_pieza(v, pieza, hf, parte=None):
    """parte=None → todas las partes encadenadas en un index; parte=i → solo la i-ésima (render por partes)."""
    tl = timeline_motor(v, pieza)
    parts = configurar(v, pieza, tl)
    master = v.build / "audio" / pieza / "master.wav"
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(master)],
                                 capture_output=True, text=True).stdout)
    tl["dur"] = total
    sel = list(enumerate(parts)) if parte is None else [(parte, parts[parte])]
    (hf / "compositions").mkdir(parents=True, exist_ok=True)
    hosts, sfx, html_all, t0p = [], [], "", 0.0
    for i, (name, secs) in sel:
        LH.PH_USED.clear()
        P = LH.Part(name, secs).build()
        doc = P.html()
        (hf / "compositions" / f"{name}.html").write_text(doc)
        html_all += doc
        sfx += [ev for S in P.secs for ev in S.sfx]
        ph = len(LH.PH_USED)
        if parte is not None:
            t0p = P.t0
        hosts.append(f'<div id="{P.cid}" data-composition-id="{P.cid}" data-composition-src="compositions/{name}.html" '
                     f'data-start="{P.t0 - t0p:.3f}" data-duration="{P.t1 - P.t0:.3f}" data-track-index="1" '
                     f'data-width="{LH.W}" data-height="{LH.H}"></div>')
        nsc = sum(len(S.scenes) for S in P.secs)
        print(f"  {name:4s} {P.t0:7.1f}–{P.t1:7.1f}  {nsc:2d} escenas · {len([e for S in P.secs for e in S.sfx])} sfx"
              + (f" · {ph} PLACEHOLDER" if ph else ""))
    dur = total if parte is None else (parts[parte] and (P.t1 - P.t0))
    W, H = LH.W, LH.H
    (hf / "index.html").write_text(f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="{GSAP}"></script>
<link rel="stylesheet" href="shared/explicando.css" />
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#0B0B14}}</style>
</head><body>
<div id="main" data-composition-id="main" data-start="0" data-duration="{dur:.3f}" data-width="{W}" data-height="{H}" data-fps="30">
<audio id="voz" class="clip" data-start="0" data-duration="{dur:.3f}" data-track-index="0" data-volume="1" src="assets/audio/master.wav"></audio>
{chr(10).join(hosts)}
</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{paused:true}});</script>
</body></html>
""")
    if parte is None:
        (v.build / f"sfx-{pieza}.json").write_text(json.dumps(sfx, indent=0))
    # recursos: shared/ del estilo, imágenes y videos que nombra el HTML, audio maestro
    if (hf / "shared").exists():
        shutil.rmtree(hf / "shared")
    shutil.copytree(AQUI / "shared", hf / "shared")
    faltan = []
    for ref in sorted(set(re.findall(r'assets/(?:img|video)/[^"\')\s]+', html_all))):
        src = v.dir / ref
        if src.exists():
            _enlazar(src, hf / ref)
        else:
            faltan.append(ref)
    if faltan:
        print("  ⚠ faltan (se verán vacíos):\n    " + "\n    ".join(faltan[:20]))
    au = hf / "assets/audio"
    au.mkdir(parents=True, exist_ok=True)
    if parte is None:
        shutil.copy(master, au / "master.wav")
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t0p:.4f}", "-t", f"{dur:.4f}", "-i", str(master),
                        "-c:a", "pcm_s16le", str(au / "master.wav")], check=True)
    print(f"✓ {hf.name}: {len(sel)} parte(s) · {dur:.1f} s · estilo comic")
    return hf, len(parts)


# ------------------------------------------------------------------ mezcla propia (de lf.py cmd_mix)
def _dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def _ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def mezclar(v, pieza, video_mudo, salida):
    """voz+clips (master) + cama musical por sección (ducking bajo clips) + SFX de cómic → salida (-14 LUFS)."""
    tl = timeline_motor(v, pieza)
    master = v.build / "audio" / pieza / "master.wav"
    total = _dur(master)
    tmp = v.build / "audio" / pieza / ".mix"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    musica = (v.meta.get("musica") or {}).get("comic") or {}
    # 1) cama: tramos por pista con crossfade; la pista se repite si el tramo es largo
    runs = []
    for sid, (s0, s1) in tl["sections"].items():
        trk = musica.get(sid, musica.get("_defecto", "misterio"))
        if runs and runs[-1][0] == trk:
            runs[-1][2] = s1
        else:
            runs.append([trk, s0, s1])
    bed = None
    if musica:
        inputs, filt, labels, offset = [], [], [], {}
        for k, (trk, s0, s1) in enumerate(runs):
            src = MUS / f"comic-{trk}.wav"
            if not src.exists():
                raise SystemExit(f"falta audio-lib/musica/comic-{trk}.wav (ver PROMPTS.md)")
            Ld = s1 - s0 + 1.5
            start_in = offset.get(trk, 0.0)
            inputs += ["-stream_loop", "-1", "-i", src]
            filt.append(f"[{k}:a]atrim=start={start_in:.3f}:duration={Ld:.3f},asetpts=PTS-STARTPTS,"
                        f"afade=t=in:d=1.2,afade=t=out:st={Ld - 1.5:.3f}:d=1.5,adelay={int(s0 * 1000)}|{int(s0 * 1000)}[m{k}]")
            labels.append(f"[m{k}]")
            offset[trk] = (start_in + Ld) % max(1, _dur(src) - 2)
        filt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=duration={total:.3f}[bed]")
        vol = ["0.10"]  # ≈ -20 dB bajo voz; -32 dB bajo clips con audio
        for c in tl["clips"]:
            vol.append(f"if(between(t,{c['start'] - 0.2:.2f},{c['end'] + 0.2:.2f}),0.025,")
        expr = "".join(vol[1:]) + vol[0] + ")" * (len(vol) - 1)
        filt.append(f"[bed]volume='{expr}':eval=frame[bedv]")
        bed = tmp / "bed.wav"
        _ff(*inputs, "-filter_complex", ";".join(filt), "-map", "[bedv]", "-ar", "48000", "-ac", "2", bed)
    # 2) SFX: separación mínima por tipo, nada encima de un clip con audio, variantes en rotación ±3 % de tono
    evs = sorted([tuple(e) for e in json.loads((v.build / f"sfx-{pieza}.json").read_text())], key=lambda e: e[1])
    keep, last_t, last_any = [], {}, -9
    gap = {"slam": 1.2, "stamp": 0.9, "pop": 0.7, "bam": 1.0}
    for name, t, g in evs:
        if t - last_t.get(name, -9) < gap.get(name, 0.5) or t - last_any < 0.25:
            continue
        if any(c["start"] - 0.1 < t < c["end"] for c in tl["clips"]):
            continue
        if not list(SFXD.glob(f"{name}.wav")):
            continue
        keep.append((name, t, g))
        last_t[name], last_any = t, t
    sfx_files = []
    for bi in range(0, len(keep), 64):
        batch = keep[bi:bi + 64]
        ins, fl, lb = [], [], []
        for k, (name, t, g) in enumerate(batch):
            vs = sorted(SFXD.glob(f"{name}.wav")) + sorted(SFXD.glob(f"{name}-[0-9].wav"))
            ins += ["-i", vs[int(t * 7.13) % len(vs)]]
            ms = int(max(0, t) * 1000)
            rate = 1 + ((int(t * 3.7) % 5) - 2) * 0.015
            g2 = g - 8 - (3 if name in ("slam", "stamp") else 0)
            fl.append(f"[{k}:a]asetrate=44100*{rate:.3f},aresample=48000,volume={g2:.1f}dB,adelay={ms}|{ms}[s{k}]")
            lb.append(f"[s{k}]")
        fl.append(f"{''.join(lb)}amix=inputs={len(lb)}:normalize=0,apad=whole_dur={total:.3f},atrim=duration={total:.3f}[o]")
        f = tmp / f"sfx{bi}.wav"
        _ff(*ins, "-filter_complex", ";".join(fl), "-map", "[o]", "-ar", "48000", "-ac", "2", f)
        sfx_files.append(f)
    # 3) voz-clips + cama + sfx → loudnorm -14 LUFS, sobre el video mudo
    pistas = [master] + ([bed] if bed else []) + sfx_files
    ins = [x for f in pistas for x in ("-i", f)]
    n = len(pistas)
    mezcla = tmp / "mezcla.wav"
    _ff(*ins, "-filter_complex", f"{''.join(f'[{i}:a]' for i in range(n))}amix=inputs={n}:normalize=0,alimiter=limit=0.95,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11[o]", "-map", "[o]", "-ar", "48000", "-ac", "2", mezcla)
    if salida.exists():
        salida.unlink()
    _ff("-i", video_mudo, "-i", mezcla, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
        "-shortest", "-movflags", "+faststart", salida)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✓ {salida.name} · {len(keep)} SFX · {len(runs) if musica else 0} tramos de música")


# ------------------------------------------------------------------ catálogo (./tl planos comic)
def catalogo():
    print("Estilo comic · motor propio: escenas/<pieza>/<sec>.py con def build(S)  (o escenas/<pieza>.py con def <sec>(S))\n")
    print("  Sección S:   S.w(frase) inicio · S.we(frase) fin · S.peek(frase) sin mover el cursor · S.clip(i) · S.t0 / S.t1")
    print("               s = S.scene(t, bg=…, enter=…, color=…)   bg: " + ", ".join(LH.BG))
    for k in ("text", "panel", "img", "phpanel", "obj", "com", "svg", "video", "cinta", "cap", "globo", "sello", "ficha",
              "speed", "zoom", "flash", "shake", "pulse", "bob", "move", "kenburns", "slab", "draw", "out", "sfx", "raw"):
        f = getattr(LH.Scene, k)
        import inspect
        sig = str(inspect.signature(f)).replace("(s, ", "(")
        doc = " ".join((f.__doc__ or "").split())
        print(f"  s.{k}{sig}" + (f"  — {doc}" if doc else ""))
    print("\n  helpers SVG (import lib as L): " + ", ".join(n for n in dir(LH.L) if not n.startswith("_") and n.islower()
                                                       and callable(getattr(LH.L, n)) and n not in ("bt", "re", "pho")))
    print("  Ejemplo de referencia: videos/<lf04>/escenas/largo/ (y _k.py con still/tag/clipsc)")


# el motor genérico pide estos nombres aunque el estilo tenga motor propio
CSS = JS_HELPERS = ""
TRANS = {}
GRANO_CSS = None
INDEX_BG = "#0B0B14"
BN_DEFAULT = False


def IMG_VF(bn):
    return "scale='min(2400,iw)':-2"


def trans_js(*a):
    return ""


def sfx_de(*a):
    return []
