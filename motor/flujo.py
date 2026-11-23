"""Ciclo de vida de un video: nuevo → estado → qa → entrega → publicado → limpiar / regenerar."""
import datetime
import json
import os
import re
import shutil

from .proyecto import CONFIG, ROOT, Video, die, palabras_guion
from .voz import dur

FASES = ["investigacion", "brief", "guion", "assets", "voz", "montaje", "entrega", "publicado"]
FORMATOS = {"largo+short": (True, 1), "largo+serie": (True, None), "short": (False, 1), "serie": (False, None)}


# -------------------------------------------------------------------- nuevo
def nuevo(slug, titulo, formato, estilo, shorts=None, serie=None, voz=None):
    if formato not in FORMATOS:
        die(f"formato «{formato}» no existe: {', '.join(FORMATOS)}")
    if not (ROOT / "estilos" / estilo / "estilo.py").exists():
        die(f"el estilo «{estilo}» no existe (ver estilos/INDEX.md)")
    con_largo, n = FORMATOS[formato]
    n = n or shorts or 3
    hoy = datetime.date.today()
    d = ROOT / "videos" / f"{hoy:%Y-%m}-{slug}"
    if d.exists():
        die(f"ya existe {d.relative_to(ROOT)}")
    piezas = ([{"id": "largo", "tipo": "largo"}] if con_largo else []) + \
             [{"id": f"short-{i:02d}", "tipo": "short", "slug": None} for i in range(1, n + 1)]
    for sub in ("investigacion", "guion", "escenas", "assets", "entrega"):
        (d / sub).mkdir(parents=True)
    meta = {"titulo": titulo, "fecha": f"{hoy}", "formato": formato, "estilo": estilo, "voz": voz, "serie": serie,
            "piezas": piezas, "musica": {}, "pronunciacion": [],
            "estado": {f: None for f in FASES}, "youtube": {}}
    (d / "video.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    pl = ROOT / "base/plantillas"
    (d / "brief.md").write_text((pl / "brief.md").read_text().replace("{TITULO}", titulo).replace("{FORMATO}", formato)
                                .replace("{ESTILO}", estilo))
    (d / "investigacion/fuentes.md").write_text((pl / "fuentes.md").read_text().replace("{TITULO}", titulo))
    (d / "assets/manifest.json").write_text(json.dumps({"imagenes": [], "fuentes_video": [], "cortes": []}, indent=1) + "\n")
    (d / "miniaturas.json").write_text("[]\n")
    print(f"✓ {d.relative_to(ROOT)} · {formato} · {len(piezas)} piezas · estilo {estilo}")
    return d


# -------------------------------------------------------------------- estado
def tam(p):
    if not p.exists():
        return 0
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def gb(n):
    return f"{n / 1e9:.1f} GB" if n > 1e9 else f"{n / 1e6:.0f} MB"


def estado(nombre=None):
    vids = [Video(nombre)] if nombre else [Video(d.name) for d in sorted((ROOT / "videos").iterdir()) if (d / "video.json").exists()]
    for v in vids:
        est = v.meta.get("estado", {})
        marcas = []
        for f in FASES:
            x = est.get(f)
            ok = bool(x) and (all(x.values()) if isinstance(x, dict) else True)
            marcas.append(("✓" if ok else "·") + f[:4])
        peso = tam(v.build) + tam(v.dir / "assets") + tam(v.entrega)
        print(f"{v.slug:42s} {v.meta['formato']:12s} {v.estilo:9s} {' '.join(marcas)}  {gb(peso)}")
        if nombre:
            for p in v.piezas:
                g = v.dir / "guion" / f"{p}.md"
                pal = palabras_guion(v.guion(p)) if g.exists() else 0
                fin = v.build / "render" / f"{p}-final.mp4"
                print(f"   {p:10s} guion {'✓ ' + str(pal) + ' pal.' if pal else '—':14s} "
                      f"timeline {'✓' if (v.build / f'timeline-{p}.json').exists() else '—'}  "
                      f"render {'✓ %.0f s' % dur(fin) if fin.exists() else '—':9s} "
                      f"youtube {v.meta.get('youtube', {}).get(p) or '—'}")


# -------------------------------------------------------------------- QA
def nombre_entrega(v, p):
    pz = v.pieza(p)
    if pz["tipo"] == "largo":
        return "largo.mp4"
    return f"{p}-{pz['slug']}.mp4" if pz.get("slug") else f"{p}.mp4"


def qa(v, piezas=None, hojas=True):
    """Gate antes de entregar. Devuelve (errores, avisos). Las hojas de contacto quedan en build/revision/ para mirarlas."""
    from .render import hoja, lint, loudness
    errores, avisos = [], []
    lim = CONFIG["duracion"]
    ln = CONFIG["loudness"]
    for p in piezas or v.piezas:
        fin = v.build / "render" / f"{p}-final.mp4"
        if not fin.exists():
            errores.append(f"{p}: no hay render final (./tl render {v.slug} {p})")
            continue
        d = dur(fin)
        if v.vertical(p) and d > lim["short_max"]:
            errores.append(f"{p}: dura {d:.1f} s (máximo de un Short: {lim['short_max']} s)")
        if not v.vertical(p) and not lim["largo_min"] <= d <= lim["largo_max"]:
            avisos.append(f"{p}: dura {d / 60:.1f} min (objetivo {lim['largo_min'] // 60}-{lim['largo_max'] // 60} min)")
        i, tp = loudness(fin)
        if i is None:
            avisos.append(f"{p}: no pude medir loudness")
        else:
            if abs(i - ln["I"]) > 1.5:
                errores.append(f"{p}: loudness {i:.1f} LUFS (objetivo {ln['I']})")
            if tp > ln["TP"] + 0.5:
                avisos.append(f"{p}: true peak {tp:.1f} dBTP")
        hf = v.build / f"hf-{p}"
        if hf.exists():
            ok, txt = lint(hf)
            if not ok:
                avisos.append(f"{p}: hyperframes lint: {txt[-300:]}")
        if hojas:
            hoja(fin, v.build / "revision" / f"{p}.jpg")
    pub = v.entrega / "PUBLICACION.md"
    if not pub.exists():
        errores.append("falta entrega/PUBLICACION.md (skill entrega)")
    else:
        txt = pub.read_text()
        for p in piezas or v.piezas:
            if nombre_entrega(v, p) not in txt and p not in txt:
                errores.append(f"PUBLICACION.md no menciona {nombre_entrega(v, p)}")
        con_largo = any(not v.vertical(p) for p in v.piezas)
        if con_largo and any(v.vertical(p) for p in v.piezas) and not re.search(r"(?i)video relacionado|video largo|historia completa", txt):
            errores.append("PUBLICACION.md: los Shorts deben llevar al largo (Video relacionado → largo)")
    minis = {it["id"]: it for it in json.loads((v.dir / "miniaturas.json").read_text())} if (v.dir / "miniaturas.json").exists() else {}
    for p in piezas or v.piezas:
        tiene = [m for m in minis.values() if m["pieza"] == p]
        if not v.vertical(p) and len(tiene) < 2:
            avisos.append(f"{p}: el largo lleva miniatura A y B (prueba A/B); hay {len(tiene)}")
        if v.vertical(p) and not tiene:
            avisos.append(f"{p}: falta la portada del Short en miniaturas.json")
        for m in tiene:
            if not (v.entrega / f"{m['id']}.png").exists():
                errores.append(f"falta entrega/{m['id']}.png (./tl miniaturas {v.slug})")
    fu = v.dir / "investigacion/fuentes.md"
    if not fu.exists() or not re.search(r"CONFIRMADO|TEORÍA|FILTRACIÓN|LECTURA", fu.read_text()):
        avisos.append("investigacion/fuentes.md no tiene datos sellados (CONFIRMADO/TEORÍA/FILTRACIÓN/LECTURA)")
    for e in errores:
        print("  ✗", e)
    for a in avisos:
        print("  ⚠", a)
    if hojas:
        print(f"  → mirar las hojas a 1 fps en {(v.build / 'revision').relative_to(ROOT)}/")
    print("✓ QA sin errores" if not errores else f"✗ QA: {len(errores)} errores")
    return errores, avisos


def entrega(v, forzar=False):
    errores, _ = qa(v)
    if errores and not forzar:
        die("corrige los errores de QA antes de entregar (o --forzar)")
    v.entrega.mkdir(exist_ok=True)
    for p in v.piezas:
        fin = v.build / "render" / f"{p}-final.mp4"
        if fin.exists():
            dst = v.entrega / nombre_entrega(v, p)
            if dst.exists():
                dst.unlink()
            os.link(fin, dst)
            print(f"✓ entrega/{dst.name}")
    v.marcar("entrega", "hecho")


def publicado(v, pieza, url):
    v.pieza(pieza)
    v.meta.setdefault("youtube", {})[pieza] = url
    v.guardar()
    todas = all(v.meta["youtube"].get(p) for p in v.piezas)
    v.marcar("publicado", f"{datetime.date.today()}" if todas else None)
    print(f"✓ {pieza} → {url}" + ("  · video completo publicado" if todas else ""))


# -------------------------------------------------------------------- limpieza
def plan_limpieza(v):
    from .assets import RESPALDO, manifest
    m = manifest(v)
    borrar, conservar = [], []
    for sub in (v.build, v.dir / "assets/_hojas", v.dir / "assets/_candidatos", v.a_vid):
        if sub.exists():
            borrar.append(sub)
    sin_copia = {i["archivo"] for i in m["imagenes"]
                 if not i.get("url") and not (RESPALDO / v.slug / i["archivo"]).exists()}
    for f in (v.a_img.iterdir() if v.a_img.exists() else []):
        (conservar if f"img/{f.name}" in sin_copia else borrar).append(f)
    for f in (v.entrega.iterdir() if v.entrega.exists() else []):
        if f.suffix.lower() in (".mp4", ".png", ".jpg", ".mp3", ".wav") or f.is_dir():
            borrar.append(f)
    return borrar, conservar


def limpiar(nombres, si=False, forzar=False):
    total = 0
    for n in nombres:
        v = Video(n)
        if not v.meta.get("estado", {}).get("publicado") and not forzar:
            print(f"  · {v.slug}: no está publicado (marca con ./tl publicado, o --forzar)")
            continue
        borrar, conservar = plan_limpieza(v)
        t = sum(tam(p) for p in borrar)
        total += t
        print(f"  {v.slug}: libera {gb(t)}" + (f" · conserva {len(conservar)} imágenes sin URL ni respaldo "
                                               f"(./tl assets respaldar {v.slug})" if conservar else ""))
        if si:
            for p in borrar:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
            v.marcar("limpio", f"{datetime.date.today()}")
    print(("✓ liberado " if si else "→ se liberarían ") + gb(total) + ("" if si else "  (repite con --si para borrar)"))


def videos_publicados():
    out = []
    for d in sorted((ROOT / "videos").iterdir()):
        if (d / "video.json").exists() and json.loads((d / "video.json").read_text()).get("estado", {}).get("publicado"):
            out.append(d.name)
    return out


def regenerar(v, piezas=None, draft=False):
    """Reconstruye lo regenerable desde las fuentes versionadas: assets → voz → render → miniaturas."""
    from . import assets as A
    from . import miniaturas as M
    from .render import render
    from .voz import cmd_audio, cmd_master, cmd_words
    A.fetch(v)
    A.cortar(v)
    for p in v.seleccion(piezas):
        cmd_audio(v, p)
        cmd_words(v, p)
        cmd_master(v, p)
        render(v, p, draft=draft)
    if (v.dir / "miniaturas.json").exists():
        M.render(v)
