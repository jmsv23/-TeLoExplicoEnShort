"""Respaldo y restauración de las voces del canal (voces/<slug>/).

voces/<slug>/
  muestra.wav  muestra.txt     el audio de referencia y su transcripción (lo único no regenerable)
  perfil.json                  datos neutrales del proveedor: nombre en Voicebox, idioma, motor, parámetros de generación
  perfil.voicebox.json         el perfil tal cual lo devuelve Voicebox
  voicebox-export.zip          export nativo de Voicebox (POST /profiles/import lo restaura tal cual)
  origen.*                     (opcional) la grabación de donde salió la muestra
Con otro proveedor de TTS: clonar con muestra.wav + muestra.txt y ajustar motor/voz.py (cmd_audio).
"""
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from .proyecto import CONFIG, ROOT, die, voicebox_url
from .voz import vb, vb_profile

VOCES = ROOT / "voces"


def _curl_file(path_api, campo, archivo, extra=None):
    url = voicebox_url() + path_api
    cmd = ["curl", "-s", "-f", "-X", "POST", url, "-F", f"{campo}=@{archivo}"]
    for k, val in (extra or {}).items():
        cmd += ["--form-string", f"{k}={val}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        die(f"Voicebox POST {path_api} falló: {r.stderr or r.stdout}")
    return json.loads(r.stdout or "{}")


def respaldar(slug, nombre_voicebox):
    p = vb_profile(nombre_voicebox)
    d = VOCES / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "perfil.voicebox.json").write_text(json.dumps(p, ensure_ascii=False))
    (d / "voicebox-export.zip").write_bytes(vb("GET", f"/profiles/{p['id']}/export", raw=True))
    samples = vb("GET", f"/profiles/{p['id']}/samples")
    with tempfile.TemporaryDirectory() as t:
        with zipfile.ZipFile(d / "voicebox-export.zip") as z:
            z.extractall(t)
        wavs = sorted(Path(t).glob("samples/*.wav"))
        if wavs:
            shutil.copy(wavs[0], d / "muestra.wav")
    if samples:
        (d / "muestra.txt").write_text(samples[0]["reference_text"].strip() + "\n")
    prev = json.loads((d / "perfil.json").read_text()) if (d / "perfil.json").exists() else {}
    prev.update({"nombre_voicebox": p["name"], "descripcion": p.get("description"), "personalidad": p.get("personality"),
                 "idioma": p.get("language", "es"), "tipo": p.get("voice_type"), "motor": p.get("default_engine"),
                 "efectos": p.get("effects_chain"), "muestra": "muestra.wav", "texto_muestra": "muestra.txt",
                 "voicebox_id": p["id"]})
    prev.setdefault("generacion", {"normalize": True, "max_chunk_chars": 800, "crossfade_ms": 50, "personality": False})
    (d / "perfil.json").write_text(json.dumps(prev, ensure_ascii=False, indent=1) + "\n")
    print(f"✓ voces/{slug}: respaldada «{p['name']}» ({len(samples)} muestra/s)")


def restaurar(slug):
    d = VOCES / slug
    perfil = json.loads((d / "perfil.json").read_text())
    nombre = perfil["nombre_voicebox"]
    if any(p["name"] == nombre for p in vb("GET", "/profiles")):
        print(f"✓ «{nombre}» ya existe en Voicebox")
        return
    if (d / "voicebox-export.zip").exists():
        r = _curl_file("/profiles/import", "file", d / "voicebox-export.zip")
        print(f"✓ importada «{r.get('name', nombre)}» desde voicebox-export.zip")
        return
    body = {"name": nombre, "description": perfil.get("descripcion") or "", "language": perfil.get("idioma", "es")}
    p = vb("POST", "/profiles", body)
    _curl_file(f"/profiles/{p['id']}/samples", "file", d / "muestra.wav",
               {"reference_text": (d / "muestra.txt").read_text().strip()})
    print(f"✓ creada «{nombre}» desde muestra.wav")


def listar():
    for d in sorted(VOCES.iterdir()):
        if (d / "perfil.json").exists():
            p = json.loads((d / "perfil.json").read_text())
            print(f"  {d.name:22s} «{p['nombre_voicebox']}» · {p.get('motor')} · {p.get('descripcion', '')[:70]}")
