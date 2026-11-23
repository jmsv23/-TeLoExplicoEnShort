"""Preview de un estilo: un mini-video de 10-15 s con el pipeline real (voz → build → render → hoja).

estilos/<slug>/preview/
  guion.md      texto de prueba (formato de base/guion/REGLAS.md; una sección)
  escenas.py    escenas de esa sección con los planos del estilo
  img/          imágenes de prueba (ids = nombre de archivo sin extensión)
  vertical      (archivo vacío opcional) → preview 9:16; si no, 16:9
Trabaja en estilos/<slug>/_trabajo/ (ignorado) y deja preview/preview.mp4 + preview/preview.jpg (4 frames).
"""
import json
import shutil
import subprocess

from .proyecto import ROOT, Video, die


def preview(slug, draft=True):
    d = ROOT / "estilos" / slug
    pv = d / "preview"
    for f in ("guion.md", "escenas.py"):
        if not (pv / f).exists():
            die(f"falta estilos/{slug}/preview/{f}")
    vertical = (pv / "vertical").exists()
    pieza = "short-01" if vertical else "largo"
    w = d / "_trabajo"
    for sub in ("guion", "escenas", "assets/img"):
        (w / sub).mkdir(parents=True, exist_ok=True)
    (w / "video.json").write_text(json.dumps({
        "titulo": f"Preview {slug}", "formato": "short" if vertical else "largo+short", "estilo": slug, "voz": None,
        "piezas": [{"id": pieza, "tipo": "short" if vertical else "largo"}], "musica": {}, "estado": {}}, indent=1))
    shutil.copy(pv / "guion.md", w / "guion" / f"{pieza}.md")
    shutil.copy(pv / "escenas.py", w / "escenas" / f"{pieza}.py")
    for f in (pv / "img").glob("*") if (pv / "img").exists() else []:
        shutil.copy(f, w / "assets/img" / f.name)
    v = Video(str(w))
    from .render import hoja, render
    from .voz import cmd_audio, cmd_master, cmd_words
    cmd_audio(v, pieza)
    cmd_words(v, pieza)
    cmd_master(v, pieza)
    fin = render(v, pieza, draft=draft)
    shutil.copy(fin, pv / "preview.mp4")
    h = hoja(fin, w / "hoja.jpg")
    # 4 frames repartidos → preview.jpg de la galería
    from .voz import dur
    t = dur(fin)
    ins, fc = [], ""
    for i, x in enumerate((0.15, 0.4, 0.65, 0.9)):
        ins += ["-ss", f"{t * x:.2f}", "-i", str(fin)]
        fc += f"[{i}:v]scale={360 if vertical else 640}:-2[v{i}];"
    fc += "[v0][v1][v2][v3]hstack=inputs=4" if vertical else "[v0][v1]hstack[a];[v2][v3]hstack[b];[a][b]vstack"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-frames:v", "1", "-q:v", "4",
                    str(pv / "preview.jpg")], check=True)
    print(f"✓ preview de {slug}: estilos/{slug}/preview/preview.mp4 · hoja {h.relative_to(ROOT)} · estilos/{slug}/preview/preview.jpg")
