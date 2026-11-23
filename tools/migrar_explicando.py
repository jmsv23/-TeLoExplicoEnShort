#!/usr/bin/env python3
"""Migra un video de content-creator/explicando/ al formato del canal (una sola vez por video).

    python3 tools/migrar_explicando.py james-bond            # fuentes (git) + media local (hardlinks, ignorada)
    python3 tools/migrar_explicando.py james-bond --sin-media

Fuentes que pasan a git: guion (guion_*.py → guion/<pieza>.md), escenas, brief/notas, PUBLICACION.md,
manifiesto de assets (fuentes de video, cortes, imágenes con su página) y legacy/ (scripts viejos, solo referencia).
Media local (ignorada): assets/img, assets/video/cortes y música/SFX como hardlinks (solo se leen);
build/audio y build/timeline-*.json como copia (el motor los reescribe).
"""
import ast
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/home/jmsv23/projects/personal/content-creator/explicando")

VIDEOS = {
    "james-bond": dict(slug="2026-11-james-bond-pattinson", estilo="bond", fecha="2026-11-19",
                       titulo="El nuevo James Bond es Robert Pattinson", formato="largo+short",
                       piezas={"largo": "largo", "short": "short-01"},
                       musica={"tema": "bond-tema-principal.wav", "fondo": "bond-tema-fondo.wav",
                               "largo": {"fondo_desde": "noticia", "fondo_offset": -1.5, "tema_entra": "tras_primer_clip",
                                         "tema_desde": 70.0, "gain_tema": -12, "gain_fondo": -14, "gain_cierre": -14.5},
                               "short": {"tema_desde": 60.0, "gain": -12, "fade_in": 0.6, "fade_out": 2.5}},
                       musica_src={"bond-tema-principal.wav": "tema-principal.wav", "bond-tema-fondo.wav": "tema-fondo.wav"}),
    "evolucion-del-gta": dict(slug="2026-11-evolucion-del-gta", estilo="leonida", fecha="2026-11-22",
                              titulo="La evolución del GTA (1997 → GTA 6)", formato="largo+serie",
                              piezas={"largo": "largo", **{f"s{i}": f"short-0{i}" for i in range(1, 7)}},
                              musica={"tema": "leonida-synthwave.wav", "fondo": "leonida-fondo-loop.wav",
                                      "largo": {"fondo_desde": "origen", "gain_fondo": -15}},
                              musica_src={"leonida-synthwave.wav": "opcion-A-synthwave.wav", "leonida-fondo-loop.wav": "fondo-loop.wav"}),
    "top-5-actrices-marvel-mas-guapas": dict(slug="2026-11-top-5-actrices-marvel", estilo="portada", fecha="2026-11-20",
                                             titulo="Top 5 actrices de Marvel", formato="largo+short",
                                             piezas={"largo": "largo", "short": "short-01"},
                                             musica={"tema": "portada-runway.wav", "fondo": "portada-fondo.wav",
                                                     "largo": {"fondo_desde": "n5", "gain_fondo": -15}},
                                             musica_src={"portada-runway.wav": "opcion-A-runway.wav", "portada-fondo.wav": "A-fondo.wav"}),
    "mejores-momentos-de-gta6": dict(slug="2026-11-mejores-momentos-gta6", estilo="facecam", fecha="2026-11-21",
                                     titulo="Top 12 momentos de streamers en GTA 6", formato="largo+serie",
                                     piezas={"largo": "largo", "s1": "short-01", "s2": "short-02"},
                                     musica={"tema": "leonida-synthwave.wav", "fondo": "leonida-fondo-loop.wav",
                                             "largo": {"fondo_desde": "n12", "fondo_offset": -0.5, "gain_fondo": -17}},
                                     musica_src={}),
}


def link(a, b):
    """Hardlink (mismo disco: no duplica espacio); si no se puede, copia."""
    b.parent.mkdir(parents=True, exist_ok=True)
    if b.exists() or b.is_symlink():
        b.unlink()
    a = a.resolve()
    try:
        os.link(a, b)
    except OSError:
        shutil.copy2(a, b)


def link_tree(a, b, copiar=False):
    if not a.exists():
        return 0
    n = 0
    for f in a.rglob("*"):
        if f.is_file():
            dst = b / f.relative_to(a)
            if copiar:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
            else:
                link(f, dst)
            n += 1
    return n


def guion_md(py, pieza):
    mod = {}
    exec(compile(py.read_text(), str(py), "exec"), mod)
    out = ["---", f"pieza: {pieza}", f"direccion: {json.dumps(mod.get('DIRECCION', ''), ensure_ascii=False)}", "---", "",
           f"> Migrado de {py.relative_to(SRC)}. Una línea = un bloque de voz; [clip: x] = escena con sonido.", ""]
    for s in mod["SECCIONES"]:
        out.append(f"## {s['id']} · {s.get('titulo', s['id'])}")
        for tipo, val in s["beats"]:
            out.append(f"[clip: {val}]" if tipo == "clip" else val.replace("\n", " ").strip())
        out.append("")
    return "\n".join(out)


def cortes_de(cortar_py):
    if not cortar_py.exists():
        return [], {}
    t = ast.parse(cortar_py.read_text())
    cortes, vmap = [], {}
    for n in t.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "V":
            vmap = ast.literal_eval(n.value)
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CORTES":
            raw = ast.literal_eval(n.value)
            if isinstance(raw, dict):  # nombre: (video, ini, fin)
                for k, (vid, a, b) in raw.items():
                    cortes.append({"id": k, "fuente": vmap.get(vid, vid), "inicio": a, "fin": b, "tipo": "voz"})
            else:
                for x in raw:
                    c = {"id": x[0], "fuente": x[1], "inicio": x[2], "fin": x[3], "tipo": x[4], "bloque": x[5]}
                    if len(x) == 8:
                        c["zoom"], c["nota"] = x[6], x[7]
                    else:
                        c["nota"] = x[6]
                    cortes.append(c)
    return cortes, vmap


def imagenes_de(adir):
    filas = {}
    md = adir / "ASSETS-IMG.md"
    if md.exists():
        for line in md.read_text().splitlines():
            m = re.match(r"^\|\s*`img/([^`]+)`.*\|\s*([^|]+?)\s*\|\s*\[link\]\(([^)]+)\)\s*\|$", line)
            if m:
                filas[Path(m.group(1)).stem] = {"fuente": m.group(2), "pagina": m.group(3)}
    por_pagina = {}
    for j in sorted((adir / "_busqueda").glob("*.json")) if (adir / "_busqueda").exists() else []:
        try:
            for r in json.loads(j.read_text()):
                if isinstance(r, dict) and r.get("page") and r.get("img"):
                    por_pagina.setdefault(r["page"], r["img"])
        except (ValueError, TypeError):
            pass
    out = []
    for f in sorted((adir / "img").glob("*")) if (adir / "img").exists() else []:
        if not f.is_file():
            continue
        fila = filas.get(f.stem, {})
        url = por_pagina.get(fila.get("pagina"))
        out.append({"id": f.stem, "archivo": f"img/{f.name}", "url": url, "pagina": fila.get("pagina"),
                    "fuente": fila.get("fuente"), "pin": url is None})
    return out


def fuentes_video(adir, vmap):
    out = []
    tsv = adir / "video/fuentes.tsv"
    if tsv.exists():
        for line in tsv.read_text().splitlines():
            if "\t" in line and not line.startswith("#"):
                k, url = line.split("\t")[:2]
                out.append({"id": k.strip(), "url": url.strip()})
    for vid in vmap.values():
        m = re.search(r"_([A-Za-z0-9_-]{11})$", vid)
        if m:
            out.append({"id": vid, "url": f"https://www.youtube.com/watch?v={m.group(1)}"})
    return out


def main():
    old = sys.argv[1]
    media = "--sin-media" not in sys.argv
    cfg = VIDEOS[old]
    S, D = SRC / old, ROOT / "videos" / cfg["slug"]
    P = S / "_prod"
    D.mkdir(parents=True, exist_ok=True)
    # ---------------------------------------------------------------- guion + escenas
    (D / "guion").mkdir(exist_ok=True)
    (D / "escenas").mkdir(exist_ok=True)
    for viejo, nuevo in cfg["piezas"].items():
        (D / "guion" / f"{nuevo}.md").write_text(guion_md(P / f"guion_{viejo}.py", nuevo))
    if (P / "escenas_largo.py").exists():
        shutil.copy(P / "escenas_largo.py", D / "escenas/largo.py")
    if (P / "escenas_short.py").exists():
        shutil.copy(P / "escenas_short.py", D / "escenas/short-01.py")
    if (P / "escenas_shorts.py").exists():
        shutil.copy(P / "escenas_shorts.py", D / "escenas/shorts.py")
    # ---------------------------------------------------------------- textos
    for f in ("brief.md",):
        if (S / f).exists():
            shutil.copy(S / f, D / f)
    inv = D / "investigacion"
    inv.mkdir(exist_ok=True)
    for f in ("idea.md", "propuesta.md", "instrucciones.md", "INVESTIGACION_PREVIA.md"):
        if (S / f).exists():
            shutil.copy(S / f, inv / f)
    if (S / "research").exists():
        for f in (S / "research").glob("*.json"):
            if f.stat().st_size < 500_000:  # los dumps grandes de yt-dlp se regeneran; los créditos están en sources.csv
                shutil.copy(f, inv / f.name)
    if (S / "sources.csv").exists():
        shutil.copy(S / "sources.csv", inv / "sources.csv")
    if (S / "moments.csv").exists():
        shutil.copy(S / "moments.csv", inv / "moments.csv")
    (D / "entrega").mkdir(exist_ok=True)
    for f in ("PUBLICACION.md", "PLAYLIST-GTA.md"):
        if (S / "entrega" / f).exists():
            shutil.copy(S / "entrega" / f, D / "entrega" / f)
    # ---------------------------------------------------------------- legacy (solo referencia)
    lg = D / "legacy"
    lg.mkdir(exist_ok=True)
    for f in list(P.glob("*.py")) + list(P.glob("*.sh")):
        shutil.copy(f, lg / f.name)
    if (S / "_estilo.md").exists():
        shutil.copy(S / "_estilo.md", lg / "_estilo.md")
    for f in (S / "largo/guion.md", S / "short/guion.md"):
        if f.exists():
            shutil.copy(f, lg / f"guion-legible-{f.parent.name}.md")
    mini = P / "miniatura"
    if mini.exists():
        (lg / "miniatura").mkdir(exist_ok=True)
        for f in list(mini.glob("*.py")) + list(mini.glob("*.html")):
            shutil.copy(f, lg / "miniatura" / f.name)
    A = S / "assets"
    for f in list(A.glob("*.py")) + list(A.glob("*.md")) + list(A.glob("*.sh")):
        shutil.copy(f, lg / f"assets-{f.name}")
    # ---------------------------------------------------------------- manifiesto de assets
    cortes, vmap = cortes_de(A / "cortar.py")
    manifest = {"_nota": "Fuente de verdad de los assets. Los archivos se ignoran en git: ./tl assets fetch los vuelve a bajar "
                         "y ./tl assets cortar los corta. pin=true → sin URL directa: respaldar con ./tl assets respaldar.",
                "imagenes": imagenes_de(A), "fuentes_video": fuentes_video(A, vmap), "cortes": cortes}
    (D / "assets").mkdir(exist_ok=True)
    (D / "assets/manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    # ---------------------------------------------------------------- video.json
    piezas = []
    for viejo, nuevo in cfg["piezas"].items():
        pz = {"id": nuevo, "tipo": "largo" if nuevo == "largo" else "short"}
        if nuevo == "largo" and len(list(P.glob("hf-largo-p*"))) > 1:
            pz["partes"] = 3
        piezas.append(pz)
    meta = {"titulo": cfg["titulo"], "fecha": cfg["fecha"], "formato": cfg["formato"], "estilo": cfg["estilo"],
            "voz": None, "serie": None, "piezas": piezas, "musica": cfg["musica"],
            "estado": {"investigacion": "hecho", "brief": "aprobado", "guion": "aprobado", "assets": "hecho",
                       "voz": "hecho", "montaje": "hecho", "entrega": "hecho", "publicado": None},
            "youtube": {}, "migrado_de": f"content-creator/explicando/{old}"}
    if (D / "video.json").exists():
        prev = json.loads((D / "video.json").read_text())
        meta["youtube"] = prev.get("youtube", {})
        meta["estado"]["publicado"] = prev.get("estado", {}).get("publicado")
    (D / "video.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"✓ fuentes → videos/{cfg['slug']} · {len(manifest['imagenes'])} imágenes · {len(cortes)} cortes")
    if not media:
        return
    # ---------------------------------------------------------------- media local (ignorada)
    n = link_tree(A / "img", D / "assets/img") + link_tree(A / "video/cortes", D / "assets/video/cortes")
    for viejo, nuevo in cfg["piezas"].items():
        # build/ se reescribe al regenerar: copia (un hardlink haría que ffmpeg -y pise el original)
        n += link_tree(P / "audio" / viejo, D / "build/audio" / nuevo, copiar=True)
        t = P / f"timeline-{viejo}.json"
        if t.exists():
            shutil.copy2(t, D / f"build/timeline-{nuevo}.json")
    for nuevo, viejo in cfg["musica_src"].items():
        if (P / "audio/musica" / viejo).exists():
            link(P / "audio/musica" / viejo, ROOT / "audio-lib/musica" / nuevo)
    for f in (P / "audio/sfx").glob("*"):
        if f.suffix == ".wav" and not (ROOT / "audio-lib/sfx" / f.name).exists():
            link(f, ROOT / "audio-lib/sfx" / f.name)
    picos = ROOT / "audio-lib/sfx/picos.json"
    cur = json.loads(picos.read_text()) if picos.exists() else {}
    if (P / "audio/sfx/picos.json").exists():
        for k, val in json.loads((P / "audio/sfx/picos.json").read_text()).items():
            cur.setdefault(k, val)
        picos.write_text(json.dumps(cur, indent=1))
    print(f"✓ media local: {n} archivos enlazados")


if __name__ == "__main__":
    main()
