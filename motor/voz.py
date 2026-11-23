"""Voz y línea de tiempo de una pieza.

    audio   Voicebox, un wav por bloque del guion (caché por sha de texto + perfil + dirección)
    words   alineación forzada (wav2vec2 de WhisperX) del texto TTS exacto contra cada wav
    master  build/audio/<pieza>/master.wav (voz + escenas con sonido) + build/timeline-<pieza>.json

Las escenas con sonido ([clip: x] en el guion) se cortan antes en assets/video/cortes/x.mp4.
"""
import hashlib
import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from .proyecto import CONFIG, ROOT, die

SR = 48000


def vb(method, path, body=None, raw=False, timeout=120):
    url = CONFIG["voicebox"]["url"].rstrip("/") + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read() if raw else json.load(r)
    except urllib.error.HTTPError as e:
        die(f"Voicebox {method} {path} → {e.code}: {e.read().decode()[:400]}")
    except urllib.error.URLError as e:
        die(f"Voicebox no responde en {url} ({e.reason}). ¿Está abierta la app? (VOICEBOX_URL para otro host)")


def vb_profile(name):
    profs = vb("GET", "/profiles")
    for p in profs:
        if p["name"] == name or p["id"] == name:
            return p
    die(f"el perfil «{name}» no existe en Voicebox. Restáuralo: ./tl voz-restaurar <slug>. "
        f"Perfiles: {', '.join(p['name'] for p in profs)}")


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout)


def bloques(v, pieza):
    g = v.guion(pieza)
    out = []
    for s in g["secciones"]:
        n = 0
        for tipo, val in s["beats"]:
            if tipo == "vo":
                n += 1
                out.append({"type": "vo", "id": f"{s['id']}-{n:02d}", "sec": s["id"], "text": val, "tts": v.tts_text(val)})
            else:
                out.append({"type": "clip", "id": f"{s['id']}-clip-{val}", "sec": s["id"], "clip": val})
    return out, g["direccion"]


def cmd_audio(v, pieza, force=False):
    d = v.build / "audio" / pieza
    d.mkdir(parents=True, exist_ok=True)
    blocks, direccion = bloques(v, pieza)
    cfg = CONFIG["voicebox"]
    perfil = v.perfil_voz()
    prof = vb_profile(perfil["nombre_voicebox"])
    gen_cfg = perfil.get("generacion", {})
    vb("GET", "/health")
    for b in blocks:
        if b["type"] != "vo":
            continue
        wav, meta = d / f"{b['id']}.wav", d / f"{b['id']}.json"
        sha = hashlib.sha256(f"{b['tts']}|{prof['id']}|{direccion}".encode()).hexdigest()[:16]
        if wav.exists() and meta.exists() and not force and json.loads(meta.read_text()).get("sha") == sha:
            continue
        body = {"profile_id": prof["id"], "text": b["tts"], "language": perfil.get("idioma", "es"),
                "personality": gen_cfg.get("personality", False), "normalize": gen_cfg.get("normalize", True),
                "max_chunk_chars": gen_cfg.get("max_chunk_chars", 800), "crossfade_ms": gen_cfg.get("crossfade_ms", 50),
                "instruct": direccion}
        t0 = time.time()
        gen = vb("POST", "/generate", body)
        while gen["status"] not in ("completed", "failed", "error", "cancelled"):
            if time.time() - t0 > cfg["timeout_s"]:
                die(f"{b['id']}: Voicebox tardó demasiado")
            time.sleep(1)
            gen = vb("GET", f"/history/{gen['id']}")
        if gen["status"] != "completed":
            die(f"{b['id']}: falló: {gen.get('error')}")
        wav.write_bytes(vb("GET", f"/audio/{gen['id']}", raw=True, timeout=300))
        du = dur(wav)
        w = len(b["tts"].split())
        meta.write_text(json.dumps({"sha": sha, "dur": du, "palabras": w, "gen": gen["id"], "voz": v.voz()}))
        print(f"✓ {b['id']}: {du:.1f} s · {w / du:.2f} pal/s ({time.time() - t0:.0f} s)", flush=True)


def cmd_words(v, pieza, force=False):
    d = v.build / "audio" / pieza
    blocks, _ = bloques(v, pieza)
    for b in blocks:
        if b["type"] == "vo":
            f = d / f"{b['id']}.tts.txt"
            if force or not f.exists() or f.read_text() != b["tts"]:
                f.write_text(b["tts"])
    py = Path(CONFIG["whisperx_python"]).expanduser()
    r = subprocess.run([str(py), str(Path(__file__).parent / "forzar.py"), str(d)], capture_output=True, text=True)
    if r.returncode:
        die("alineación forzada falló:\n" + r.stderr[-2000:])
    malos = []
    for b in blocks:
        if b["type"] != "vo":
            continue
        fz = json.loads((d / f"{b['id']}.forced.json").read_text())
        orig, tts = b["text"].split(), b["tts"].split()
        words = [[orig[i] if len(orig) == len(tts) else w, s_, e] for i, (w, s_, e) in enumerate(fz["words"])]
        quietas = sum(1 for i in range(1, len(words)) if words[i][1] <= words[i - 1][1])
        if quietas > max(2, len(words) // 8):
            malos.append(f"{b['id']} ({quietas} sin avance)")
        (d / f"{b['id']}.words.json").write_text(json.dumps({"dur": fz["dur"], "words": words}, ensure_ascii=False))
    print(f"✓ {pieza}: palabras alineadas" + (f" · revisar: {', '.join(malos)}" if malos else ""))


def ff(*args):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *map(str, args)], check=True)


def cmd_master(v, pieza):
    d = v.build / "audio" / pieza
    blocks, _ = bloques(v, pieza)
    gaps = CONFIG["gaps"]
    parts, t, prev_sec, tl = [], 0.0, None, {"beats": [], "sections": []}

    def sil(s):
        nonlocal t
        if s > 0:
            p = d / f".sil-{int(s * 1000)}.wav"
            if not p.exists():
                ff("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo", "-t", f"{s:.3f}", p)
            parts.append(p)
            t += s

    for i, b in enumerate(blocks):
        if prev_sec is not None:
            sil(gaps["seccion"] if b["sec"] != prev_sec else
                (gaps["clip"] if "clip" in (b["type"], blocks[i - 1]["type"]) else gaps["bloque"]))
        if b["sec"] != prev_sec:
            if tl["sections"]:
                tl["sections"][-1]["end"] = round(t, 3)
            tl["sections"].append({"id": b["sec"], "start": round(t, 3)})
        prev_sec = b["sec"]
        if b["type"] == "vo":
            src = d / f"{b['id']}.wav"
            w = json.loads((d / f"{b['id']}.words.json").read_text())
            du = dur(src)
            tl["beats"].append({"type": "vo", "id": b["id"], "sec": b["sec"], "start": round(t, 3), "end": round(t + du, 3),
                                "text": b["text"], "words": [[x, round(t + s, 3), round(t + e, 3)] for x, s, e in w["words"]]})
        else:
            mp4 = v.a_cut / f"{b['clip']}.mp4"
            if not mp4.exists():
                die(f"falta el corte {mp4.relative_to(ROOT)} (./tl assets cortar {v.slug})")
            src = d / f".clip-{b['clip']}.wav"
            # escenas al nivel de la narración (~-20 LUFS): si quedan más fuertes la voz se percibe baja al normalizar
            ff("-i", mp4, "-vn", "-af", "loudnorm=I=-20:TP=-2:LRA=11:linear=true", "-ac", "2", "-ar", SR, src)
            du = dur(mp4)
            tl["beats"].append({"type": "clip", "id": b["id"], "sec": b["sec"], "clip": b["clip"],
                                "start": round(t, 3), "end": round(t + du, 3)})
        norm = d / f".n-{src.stem}.wav"
        ff("-i", src, "-ac", "2", "-ar", SR, norm)
        parts.append(norm)
        t += du
    sil(1.5)
    tl["sections"][-1]["end"] = round(t, 3)
    tl["duration"] = round(t, 3)
    lst = d / ".concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", d / "master.wav")
    (v.build / f"timeline-{pieza}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    print(f"✓ {pieza}: master {t:.1f} s ({t / 60:.1f} min) · {len(tl['beats'])} beats")
    return t
