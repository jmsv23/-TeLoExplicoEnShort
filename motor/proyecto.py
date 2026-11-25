"""Rutas, configuración y lectura de un video (video.json + guion/*.md).

Todo el motor pasa por aquí para saber dónde está cada cosa. Un video vive en videos/<slug>/ y una «pieza»
es cada render que sale de él: "largo" (16:9) o "short-NN" (9:16).
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config.json").read_text())
if os.environ.get("VOICEBOX_URL"):
    CONFIG["voicebox"]["url"] = os.environ["VOICEBOX_URL"]
    CONFIG["voicebox"]["url_local"] = None   # VOICEBOX_URL manda: sin respaldo

_VB = []


def voicebox_url():
    """URL de Voicebox: primero la remota (config.json → voicebox.url); si no responde en
    `probe_s` segundos, la local (voicebox.url_local). Se decide una vez por comando."""
    if _VB:
        return _VB[0]
    import urllib.request
    cfg = CONFIG["voicebox"]
    candidatos = [u for u in (cfg.get("url"), cfg.get("url_local")) if u]
    for u in candidatos:
        try:
            with urllib.request.urlopen(u.rstrip("/") + "/profiles", timeout=cfg.get("probe_s", 3)):
                pass
        except Exception:
            print(f"· Voicebox no responde en {u}", file=sys.stderr)
            continue
        if u != candidatos[0]:
            print(f"· usando Voicebox local: {u}", file=sys.stderr)
        _VB.append(u.rstrip("/"))
        return _VB[0]
    _VB.append(candidatos[0].rstrip("/"))   # ninguno responde: que el error salga con la remota
    return _VB[0]


def die(msg):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def resolver_video(nombre):
    """Acepta el slug completo (2026-11-james-bond), el slug sin fecha (james-bond) o una ruta."""
    p = Path(nombre)
    if (p / "video.json").exists():
        return p.resolve()
    vids = ROOT / "videos"
    if (vids / nombre / "video.json").exists():
        return vids / nombre
    hits = [d for d in vids.iterdir() if d.is_dir() and re.sub(r"^\d{4}-\d{2}-", "", d.name) == nombre]
    hits = hits or [d for d in vids.iterdir() if d.is_dir() and nombre in d.name]
    if len(hits) == 1:
        return hits[0]
    die(f"no encuentro el video «{nombre}»" + (f" (ambiguo: {', '.join(h.name for h in hits)})" if hits else ""))


class Video:
    def __init__(self, nombre):
        self.dir = resolver_video(nombre)
        self.slug = self.dir.name
        self.meta_path = self.dir / "video.json"
        self.meta = json.loads(self.meta_path.read_text())
        self.build = self.dir / "build"
        self.a_img = self.dir / "assets/img"
        self.a_vid = self.dir / "assets/video"
        self.a_cut = self.dir / "assets/video/cortes"
        self.entrega = self.dir / "entrega"

    # ---------------------------------------------------------------- piezas
    @property
    def piezas(self):
        return [p["id"] for p in self.meta["piezas"]]

    def pieza(self, pid):
        for p in self.meta["piezas"]:
            if p["id"] == pid:
                return p
        die(f"{self.slug}: no hay pieza «{pid}» (hay: {', '.join(self.piezas)})")

    def vertical(self, pid):
        return self.pieza(pid)["tipo"] == "short"

    def seleccion(self, sel):
        """None/'todas' → todas; 'largo' / 'short-01' / 'short-01,short-02' / 'shorts'."""
        if sel in (None, "todas", "all"):
            return self.piezas
        if sel == "shorts":
            return [p for p in self.piezas if self.vertical(p)]
        out = sel.split(",")
        for p in out:
            self.pieza(p)
        return out

    # ---------------------------------------------------------------- estilo y voz (cadena base → estilo → video)
    @property
    def estilo(self):
        return self.meta["estilo"]

    def estilo_dir(self):
        d = ROOT / "estilos" / self.estilo
        if not (d / "estilo.py").exists():
            die(f"el estilo «{self.estilo}» no existe en estilos/ (ver estilos/INDEX.md)")
        return d

    def voz(self):
        """Slug de voz en voces/: video.json → estilo (ESTILO.md frontmatter 'voz') → config."""
        if self.meta.get("voz"):
            return self.meta["voz"]
        fm = frontmatter((self.estilo_dir() / "ESTILO.md").read_text())[0]
        return fm.get("voz") or CONFIG["voz_default"]

    def perfil_voz(self):
        slug = self.voz()
        f = ROOT / "voces" / slug / "perfil.json"
        if not f.exists():
            die(f"la voz «{slug}» no está respaldada en voces/")
        return json.loads(f.read_text())

    def pronunciacion(self):
        base = json.loads((ROOT / "base/pronunciacion.json").read_text())["reglas"]
        extra = self.meta.get("pronunciacion", [])
        reglas = {a: b for a, b in base}
        reglas.update({a: b for a, b in extra})
        return sorted(reglas.items(), key=lambda kv: -len(kv[0]))  # «Amazon MGM» antes que «Amazon»

    def tts_text(self, t):
        for a, b in self.pronunciacion():
            t = re.sub(rf"\b{re.escape(a)}\b", b, t)
        return re.sub(r"\s+", " ", t).strip()

    # ---------------------------------------------------------------- guion
    def guion(self, pid):
        f = self.dir / "guion" / f"{pid}.md"
        if not f.exists():
            die(f"falta {f.relative_to(ROOT)}")
        return parse_guion(f.read_text(), f)

    def guardar(self):
        self.meta_path.write_text(json.dumps(self.meta, ensure_ascii=False, indent=1) + "\n")

    def marcar(self, fase, valor, pieza=None):
        est = self.meta.setdefault("estado", {})
        if pieza:
            est.setdefault(fase, {})
            if not isinstance(est[fase], dict):
                est[fase] = {}
            est[fase][pieza] = valor
        else:
            est[fase] = valor
        self.guardar()


# -------------------------------------------------------------------- formato del guion
def frontmatter(txt):
    """Frontmatter mínimo `clave: valor` (una línea por clave). Devuelve (dict, resto)."""
    m = re.match(r"^---\n(.*?)\n---\n?", txt, re.S)
    if not m:
        return {}, txt
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fm[k.strip()] = v
    return fm, txt[m.end():]


def parse_guion(txt, path="guion"):
    """guion/<pieza>.md → {"direccion": str, "secciones": [{id, titulo, beats: [("vo", texto) | ("clip", nombre)]}]}

    ## <id> · <título>          abre una sección (el id amarra las escenas: def <id>(S) en escenas/<pieza>.py)
    Una línea = un bloque de voz (se genera y se alinea por separado).
    [clip: nombre]              escena con sonido original (assets/video/cortes/<nombre>.mp4); el narrador calla.
    > nota / <!-- -->           comentarios: no se leen.
    """
    fm, body = frontmatter(txt)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    secs = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(">") or s.startswith("# "):
            continue
        m = re.match(r"^##\s+([a-z0-9][a-z0-9_-]*)\s*(?:·\s*(.*))?$", s)
        if m:
            secs.append({"id": m.group(1), "titulo": (m.group(2) or m.group(1)).strip(), "beats": []})
            continue
        if not secs:
            die(f"{path}: hay texto antes de la primera sección (## id · título)")
        m = re.match(r"^\[clip:\s*([^\]]+)\]$", s)
        secs[-1]["beats"].append(("clip", m.group(1).strip()) if m else ("vo", s))
    if not secs:
        die(f"{path}: el guion no tiene secciones")
    return {"direccion": fm.get("direccion", ""), "meta": fm, "secciones": secs}


def palabras_guion(g):
    return sum(len(v.split()) for s in g["secciones"] for t, v in s["beats"] if t == "vo")
