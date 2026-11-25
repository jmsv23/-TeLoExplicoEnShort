#!/usr/bin/env python3
"""Migra los long-form de Camino a Doomsday (motor _lf de content-creator/explicando) al estilo «comic».

    python3 tools/migrar_doomsday.py lf04          # LF04 largo + su short (lf04s)
    python3 tools/migrar_doomsday.py lf01|lf02|lf03

Fuentes (git): guion/<pieza>.md (reconstruido del guion.md original con la misma lógica de bloques de vo.py),
escenas/<pieza>/ (specs secsNN con imports reescritos), manifiesto (fuentes de video + cortes con audio + imágenes usadas),
video.json (partes, contador, placa, música por sección, pronunciación), brief/publicación y legacy/.
Media local (ignorada): imágenes y videos (hardlinks), timeline + voz-clips del render publicado (copias en build/).
"""
import importlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = Path("/home/jmsv23/projects/personal/content-creator/explicando")
LFD = EXP / "_motion/compositions/camino-a-doomsday/_lf"
MOTION = EXP / "_motion"
IMGS = MOTION / "assets/images/camino-a-doomsday"
VIDS = MOTION / "assets/video"

VIDEOS = {
    "lf04": dict(slug="2026-11-analisis-trailer-final-doomsday", fecha="2026-11-23",
                 titulo="Análisis del tráiler final de Avengers: Doomsday", formato="largo+short",
                 piezas=[("lf04", "largo"), ("lf04s", "short-01")]),
    "lf02": dict(slug="2026-11-doomsday-trailer-filtrado", fecha="2026-11-16",
                 titulo="Avengers: Doomsday — el tráiler final filtrado", formato="largo", piezas=[("lf02", "largo")]),
    "lf01": dict(slug="2026-11-lo-que-debes-saber-antes-de-doomsday", fecha="2026-11-14",
                 titulo="Lo que debes saber antes de ver Avengers: Doomsday", formato="largo", piezas=[("lf01", "largo")]),
    "lf03": dict(slug="2026-11-secret-wars-despues-de-doomsday", fecha="2026-11-20",
                 titulo="¿Qué pasa después de Doomsday? Secret Wars", formato="largo", piezas=[("lf03", "largo")]),
}


def cfg_de(lfid):
    os.environ["LFID"] = lfid
    sys.path.insert(0, str(LFD))
    import lfcfg
    importlib.reload(lfcfg)
    return lfcfg.C, lfcfg.LF


def link(a, b):
    b.parent.mkdir(parents=True, exist_ok=True)
    if b.exists():
        b.unlink()
    try:
        os.link(a, b)
    except OSError:
        shutil.copy2(a, b)


def bloques(C, LF):
    """Misma lógica que _lf/vo.py cmd_blocks: guion.md → [{type, sec, text | clips}] (+ títulos de sección)."""
    src = (LF / "guion.md").read_text()
    a = src.index("## 3. Guion")
    b = src.index("## 4.", a) if "## 4." in src[a:] else len(src)
    body = src[a:b]
    items, sec, mk, titulos = [], None, 0, {}
    for line in body.splitlines():
        if line.startswith("###"):
            sec = C["section_id"](line)
            titulos[sec] = re.sub(r"\s*\(\d+:\d+.*$", "", line.lstrip("#").strip())
            continue
        if line.startswith("> ") and "Convención" not in line:
            txt = line[2:].strip()
            if txt in C["replace_clips"]:
                items.append({"type": "clip", "sec": sec, "clips": C["replace_clips"][txt]})
                continue
            items.append({"type": "vo", "sec": sec, "text": txt})
            for end, clips in C["after_clips"].items():
                if txt.endswith(end):
                    items.append({"type": "clip", "sec": sec, "clips": clips})
        elif line.startswith("- *("):
            items.append({"type": "clip", "sec": sec, "clips": C["marker_clips"][mk]})
            mk += 1
    blocks = []
    for it in items:
        if it["type"] == "vo" and blocks and blocks[-1]["type"] == "vo" and blocks[-1]["sec"] == it["sec"] \
                and len(blocks[-1]["text"]) + len(it["text"]) < 900:
            blocks[-1]["text"] += " " + it["text"]
        else:
            blocks.append(dict(it))
    return blocks, titulos


def main():
    key = sys.argv[1]
    V = VIDEOS[key]
    D = ROOT / "videos" / V["slug"]
    for sub in ("guion", "escenas", "assets", "entrega", "investigacion", "legacy", "build"):
        (D / sub).mkdir(parents=True, exist_ok=True)
    manifest = {"_nota": "Migrado de Camino a Doomsday (motor _lf). Imágenes: fotogramas, recortes e ilustraciones propias "
                         "(sin URL: respaldar con ./tl assets respaldar). Fuentes de video: los archivos originales del motor.",
                "imagenes": [], "fuentes_video": [], "cortes": []}
    piezas, musica, pron = [], {}, {}
    secs_alias = {}
    for lfid, pieza in V["piezas"]:
        C, _ = cfg_de(lfid)
        secs_alias[C["secs"]] = "esc_" + pieza.replace("-", "_")
    for lfid, pieza in V["piezas"]:
        C, LF = cfg_de(lfid)
        blocks, titulos = bloques(C, LF)
        # ---------------- guion
        out = ["---", f"pieza: {pieza}", f"direccion: {json.dumps(C['direccion'], ensure_ascii=False)}", "---", "",
               f"> Migrado de {LF.relative_to(EXP)}/guion.md (motor _lf, {lfid}). Una línea = un bloque de voz.", ""]
        prev, nclip = None, 0
        for bl in blocks:
            if bl["sec"] != prev:
                out += ["", f"## {bl['sec']} · {titulos.get(bl['sec'], bl['sec'])}"]
                prev = bl["sec"]
            if bl["type"] == "vo":
                out.append(bl["text"].replace("🔁", "").strip())
            else:
                for src, a, b in bl["clips"]:
                    nclip += 1
                    cid = f"{pieza}-c{nclip:02d}"
                    fuente = Path(src).stem
                    out.append(f"[clip: {cid}]")
                    manifest["cortes"].append({"id": cid, "fuente": fuente, "inicio": a, "fin": b, "tipo": "voz",
                                               "bloque": bl["sec"]})
                    if fuente not in {f["id"] for f in manifest["fuentes_video"]}:
                        manifest["fuentes_video"].append({"id": fuente, "url": None, "archivo_original": f"_motion/assets/video/{src}"})
                        link(VIDS / src, D / "assets/video" / f"{fuente}.mp4")
        (D / "guion" / f"{pieza}.md").write_text("\n".join(out).replace("\n\n\n", "\n\n") + "\n")
        # ---------------- escenas (specs con imports reescritos)
        ed = D / "escenas" / pieza
        if ed.exists():
            shutil.rmtree(ed)
        shutil.copytree(LFD / C["secs"], ed, ignore=shutil.ignore_patterns("__pycache__"))
        for f in ed.glob("*.py"):
            s = f.read_text()
            for viejo, nuevo in secs_alias.items():
                s = re.sub(rf"\bfrom {viejo}\.", f"from {nuevo}.", s)
            s = s.replace('LFV = "camino-a-doomsday/lf/"', 'LFV = ""  # migrado: las fuentes viven en assets/video/<id>.mp4')
            s = s.replace("assets/images/camino-a-doomsday/", "assets/img/")
            # videos citados directo en las specs ("camino-a-doomsday/lf/x.mp4") → assets/video/x.mp4
            for ref in set(re.findall(r'"(?:camino-a-doomsday/lf/)?([\w.-]+\.mp4)"', s)):
                if (VIDS / "camino-a-doomsday/lf" / ref).exists():
                    link(VIDS / "camino-a-doomsday/lf" / ref, D / "assets/video" / ref)
                    if Path(ref).stem not in {x["id"] for x in manifest["fuentes_video"]}:
                        manifest["fuentes_video"].append({"id": Path(ref).stem, "url": None,
                                                          "archivo_original": f"_motion/assets/video/camino-a-doomsday/lf/{ref}"})
            s = s.replace('"camino-a-doomsday/lf/', '"')
            # decisiones a mano que vivían junto al guion (p. ej. vinetas-elegidas.json de LF03): van con las escenas
            s = s.replace('LF / "vinetas-elegidas.json"', 'Path(__file__).with_name("vinetas-elegidas.json")')
            if "Path(__file__)" in s and "from pathlib import Path" not in s:
                s = "from pathlib import Path\n" + s
            f.write_text(s)
        if (LF / "vinetas-elegidas.json").exists():
            shutil.copy2(LF / "vinetas-elegidas.json", ed / "vinetas-elegidas.json")
        # ---------------- timeline + voz del render publicado (build/, ignorado)
        tl = json.loads((LF / "timeline.json").read_text())
        for c in tl["clips"]:
            c["src"] = f"{Path(c['src']).stem}.mp4"
        (D / "build" / f"timeline-{pieza}.json").write_text(json.dumps(tl, ensure_ascii=False))
        (D / "build/audio" / pieza).mkdir(parents=True, exist_ok=True)
        shutil.copy2(LF / "audio/voz-clips.wav", D / "build/audio" / pieza / "master.wav")
        # ---------------- pieza
        pz = {"id": pieza, "tipo": "short" if C.get("size", (1920, 1080))[1] > 1080 else "largo",
              "comic": {"partes": [[n, s] for n, s in C["parts"]], "dias": C["dias"], "placa": list(C["placa"])}}
        if pz["tipo"] == "largo" and len(C["parts"]) > 1:
            pz["partes"] = True
        g = {k2: C[k1] for k1, k2 in (("gap_sec", "seccion"), ("gap_clip", "clip"), ("tail", "cola")) if k1 in C}
        if g:
            pz["gaps"] = g
        if C.get("clip_lufs"):
            pz["clip_lufs"] = C["clip_lufs"]
        piezas.append(pz)
        musica.update(C["music"])
        pron.update({a: b for a, b in C["tts_fix"]})
        # ---------------- textos y legacy
        shutil.copy2(LF / "guion.md", D / "legacy" / f"guion-original-{pieza}.md")
        if (LF / "brief.md").exists() and pieza == "largo":
            shutil.copy2(LF / "brief.md", D / "brief.md")
        for f in ("publicacion.md",):
            if (LF / f).exists():
                shutil.copy2(LF / f, D / "entrega" / ("PUBLICACION.md" if pieza == "largo" else f"PUBLICACION-{pieza}.md"))
        if (LF / "video.es.srt").exists():
            shutil.copy2(LF / "video.es.srt", D / "entrega" / f"{pieza}.es.srt")
        for f in (LF / "miniatura").glob("*") if (LF / "miniatura").exists() else []:
            if f.suffix in (".html", ".py", ".md", ".json"):
                (D / "legacy/miniatura").mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, D / "legacy/miniatura" / f.name)
            elif f.suffix in (".png", ".jpg"):
                link(f, D / "entrega" / f.name)
        if (LF / "mapa").exists():
            (D / "assets/mapa").mkdir(parents=True, exist_ok=True)
            for f in (LF / "mapa").rglob("*"):
                if f.is_file():
                    link(f, D / "assets/mapa" / f.relative_to(LF / "mapa"))
        if (LF / "analisis").exists():
            for f in (LF / "analisis").glob("*"):
                if f.is_file() and f.suffix in (".md", ".json", ".txt") and f.stat().st_size < 500_000:
                    shutil.copy2(f, D / "investigacion" / f"analisis-{f.name}")
    # ---------------- imágenes: todo el árbol de la serie como hardlinks; el manifiesto lista las que usa el HTML
    for f in IMGS.rglob("*"):
        if f.is_file():
            link(f, D / "assets/img" / f.relative_to(IMGS))
    # ---------------- música y SFX de cómic (compartidos)
    LF0 = cfg_de(V["piezas"][0][0])[1]
    for f in (LF0 / "audio/musica").glob("lf-*.wav"):
        link(f, ROOT / "audio-lib/musica" / f"comic-{f.stem[3:]}.wav")
    for f in (LF0 / "audio/sfx").glob("*.wav"):
        link(f, ROOT / "audio-lib/sfx/comic" / f.name)
    meta = {"titulo": V["titulo"], "fecha": V["fecha"], "formato": V["formato"], "estilo": "comic", "voz": None,
            "serie": "camino-a-doomsday", "piezas": piezas, "musica": {"comic": musica},
            "pronunciacion": [[a, b] for a, b in pron.items()],
            "estado": {"investigacion": "hecho", "brief": "aprobado", "guion": "aprobado", "assets": "hecho",
                       "voz": "hecho", "montaje": "hecho", "entrega": "hecho", "publicado": None},
            "youtube": {}, "migrado_de": f"content-creator/explicando/_motion/compositions/camino-a-doomsday/_lf ({key})"}
    mj = D / "video.json"
    if mj.exists():
        prev = json.loads(mj.read_text())
        meta["youtube"], meta["estado"]["publicado"] = prev.get("youtube", {}), prev.get("estado", {}).get("publicado")
    mj.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    (D / "assets/manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    if not (D / "miniaturas.json").exists():
        (D / "miniaturas.json").write_text("[]\n")
    print(f"✓ videos/{V['slug']} · {len(piezas)} pieza(s) · {len(manifest['cortes'])} cortes · {len(manifest['fuentes_video'])} fuentes")


def registrar_imagenes(slug):
    """Después del build: deja en el manifiesto solo las imágenes que el HTML usa (y quita del disco las demás)."""
    D = ROOT / "videos" / slug
    html = "".join(f.read_text() for f in (D / "build").glob("hf-*/compositions/*.html"))
    usadas = sorted(set(re.findall(r'assets/img/([^"\')\s]+)', html)))
    m = json.loads((D / "assets/manifest.json").read_text())
    m["imagenes"] = [{"id": Path(u).with_suffix("").as_posix(), "archivo": f"img/{u}", "url": None, "pagina": None,
                      "fuente": "Camino a Doomsday (fotograma/recorte/ilustración)", "pin": True} for u in usadas]
    (D / "assets/manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n")
    keep = {D / "assets/img" / u for u in usadas}
    borradas = 0
    for f in list((D / "assets/img").rglob("*")):
        if f.is_file() and f not in keep:
            f.unlink()
            borradas += 1
    print(f"✓ {len(usadas)} imágenes usadas en el manifiesto · {borradas} hardlinks sin usar quitados")


if __name__ == "__main__":
    if sys.argv[1] == "--imagenes":
        registrar_imagenes(sys.argv[2])
    else:
        main()
