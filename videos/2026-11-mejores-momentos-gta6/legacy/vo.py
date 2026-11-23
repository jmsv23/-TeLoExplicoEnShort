#!/usr/bin/env python3
"""Voz y línea de tiempo de Mejores momentos GTA 6 (largo + shorts s1, s2).

    python3 vo.py largo audio [--force]   # Voicebox "narrador comics", un wav por bloque (cache por sha)
    python3 vo.py largo words             # WhisperX por bloque + alineación con el texto
    python3 vo.py largo master            # audio/largo/master.wav (voz + escenas) + timeline-largo.json
    python3 vo.py largo all
(igual con "short")
"""
import argparse, hashlib, importlib, importlib.util, json, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JB = HERE.parent
ROOT = JB.parent  # explicando/
CORTES = JB / "assets/video/cortes"
sys.path.insert(0, str(HERE))

spec = importlib.util.spec_from_file_location("explicando", ROOT / ".claude/skills/explicando/scripts/explicando.py")
X = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0]]
spec.loader.exec_module(X)
sys.argv = _argv

PERFIL = "narrador comics"
GAP_BLOQUE, GAP_SECCION, GAP_CLIP = 0.28, 0.6, 0.3
SR = 48000

# pronunciación para el TTS (en pantalla se usa el texto original)
TTS_FIX = [
    ("GTA", "ge te a"), ("IlloJuan", "Íyo Juan"), ("Rubius", "Rúbius"), ("Willyrex", "Wílirex"), ("Kai Cenat", "Kái Sénat"),
    ("IShowSpeed", "Ái Shou Spíd"), ("Speed", "Spíd"), ("LIRIK", "Lírik"), ("CaseOh", "Kéis Óu"), ("TheBurntPeanut", "De Bérnt Pínat"),
    ("VanossGaming", "Vanós Géiming"), ("Papaplatte", "Pápaplate"), ("Bigfoot", "Bígfut"), ("streamers", "estrímers"),
    ("streamer", "estrímer"), ("San Andreas", "San Andréas"), ("Florida", "Flórida"), ("directo", "directo"),
]


def tts_text(t):
    for a, b in TTS_FIX:
        t = re.sub(rf"\b{re.escape(a)}\b", b, t)
    return re.sub(r"\s+", " ", t).strip()


def guion(pieza):
    return importlib.import_module(f"guion_{pieza}")


def bloques(pieza):
    g = guion(pieza)
    out = []
    for s in g.SECCIONES:
        n = 0
        for tipo, val in s["beats"]:
            if tipo == "vo":
                n += 1
                out.append({"type": "vo", "id": f"{s['id']}-{n:02d}", "sec": s["id"], "text": val, "tts": tts_text(val)})
            else:
                out.append({"type": "clip", "id": f"{s['id']}-clip-{val}", "sec": s["id"], "clip": val})
    return out, g.DIRECCION


def cmd_audio(pieza, force):
    d = HERE / "audio" / pieza
    d.mkdir(parents=True, exist_ok=True)
    blocks, direccion = bloques(pieza)
    cfg = X.CONFIG["voicebox"]
    prof = X.vb_profile(PERFIL)
    X.vb("GET", "/health")
    for b in blocks:
        if b["type"] != "vo":
            continue
        wav, meta = d / f"{b['id']}.wav", d / f"{b['id']}.json"
        sha = hashlib.sha256(f"{b['tts']}|{prof['id']}|{direccion}".encode()).hexdigest()[:16]
        if wav.exists() and meta.exists() and not force and json.loads(meta.read_text()).get("sha") == sha:
            continue
        body = {"profile_id": prof["id"], "text": b["tts"], "language": cfg["idioma"], "personality": False,
                "normalize": cfg["normalize"], "max_chunk_chars": cfg["max_chunk_chars"],
                "crossfade_ms": cfg["crossfade_ms"], "instruct": direccion}
        t0 = time.time()
        gen = X.vb("POST", "/generate", body)
        while gen["status"] not in ("completed", "failed", "error", "cancelled"):
            if time.time() - t0 > cfg["timeout_s"]:
                X.die(f"{b['id']}: Voicebox tardó demasiado")
            time.sleep(1)
            gen = X.vb("GET", f"/history/{gen['id']}")
        if gen["status"] != "completed":
            X.die(f"{b['id']}: falló: {gen.get('error')}")
        wav.write_bytes(X.vb("GET", f"/audio/{gen['id']}", raw=True, timeout=300))
        dur = X.ffprobe_dur(wav)
        w = len(b["tts"].split())
        meta.write_text(json.dumps({"sha": sha, "dur": dur, "palabras": w, "gen": gen["id"]}))
        print(f"✓ {b['id']}: {dur:.1f} s · {w / dur:.2f} pal/s ({time.time() - t0:.0f} s)", flush=True)


WX_PY = Path.home() / ".local/share/uv/tools/whisperx/bin/python"


def cmd_words(pieza, force):
    """Alineación forzada del texto TTS exacto (los años en palabras se alinean bien, a diferencia de la transcripción libre)."""
    d = HERE / "audio" / pieza
    blocks, _ = bloques(pieza)
    for b in blocks:
        if b["type"] == "vo":
            f = d / f"{b['id']}.tts.txt"
            if force or not f.exists() or f.read_text() != b["tts"]:
                f.write_text(b["tts"])
    r = subprocess.run([str(WX_PY), str(HERE / "forzar.py"), str(d)], capture_output=True, text=True)
    if r.returncode:
        X.die("alineación forzada falló:\n" + r.stderr[-2000:])
    malos = []
    for b in blocks:
        if b["type"] != "vo":
            continue
        fz = json.loads((d / f"{b['id']}.forced.json").read_text())
        orig, tts = b["text"].split(), b["tts"].split()
        words = [[orig[i] if len(orig) == len(tts) else w, s_, e] for i, (w, s_, e) in enumerate(fz["words"])]
        # control: palabras sin avance de tiempo (aligner perdido)
        quietas = sum(1 for i in range(1, len(words)) if words[i][1] <= words[i - 1][1])
        if quietas > max(2, len(words) // 8):
            malos.append(f"{b['id']} ({quietas} sin avance)")
        (d / f"{b['id']}.words.json").write_text(json.dumps({"dur": fz["dur"], "words": words}, ensure_ascii=False))
    print("✓ palabras (alineación forzada)" + (f" · revisar: {', '.join(malos)}" if malos else ""))


def cmd_master(pieza):
    d = HERE / "audio" / pieza
    blocks, _ = bloques(pieza)
    parts, t, prev_sec, tl = [], 0.0, None, {"beats": [], "sections": []}

    def sil(s):
        nonlocal t
        if s > 0:
            p = d / f".sil-{int(s * 1000)}.wav"
            if not p.exists():
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo",
                                "-t", f"{s:.3f}", str(p)], check=True)
            parts.append(p)
            t += s

    for i, b in enumerate(blocks):
        if prev_sec is not None:
            sil(GAP_SECCION if b["sec"] != prev_sec else (GAP_CLIP if "clip" in (b["type"], blocks[i - 1]["type"]) else GAP_BLOQUE))
        if b["sec"] != prev_sec:
            if tl["sections"]:
                tl["sections"][-1]["end"] = round(t, 3)
            tl["sections"].append({"id": b["sec"], "start": round(t, 3)})
        prev_sec = b["sec"]
        if b["type"] == "vo":
            src = d / f"{b['id']}.wav"
            w = json.loads((d / f"{b['id']}.words.json").read_text())
            dur = X.ffprobe_dur(src)
            tl["beats"].append({"type": "vo", "id": b["id"], "sec": b["sec"], "start": round(t, 3), "end": round(t + dur, 3),
                                "text": b["text"], "words": [[x, round(t + s, 3), round(t + e, 3)] for x, s, e in w["words"]]})
        else:
            mp4 = CORTES / f"{b['clip']}.mp4"
            if not mp4.exists():
                X.die(f"falta el corte {mp4}")
            src = d / f".clip-{b['clip']}.wav"
            # escenas al mismo nivel que la narración (~-20 LUFS): si quedan más fuertes, la voz se percibe baja tras normalizar
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mp4), "-vn", "-af", "loudnorm=I=-20:TP=-2:LRA=11:linear=true",
                            "-ac", "2", "-ar", str(SR), str(src)], check=True)
            dur = X.ffprobe_dur(mp4)
            tl["beats"].append({"type": "clip", "id": b["id"], "sec": b["sec"], "clip": b["clip"],
                                "start": round(t, 3), "end": round(t + dur, 3)})
        norm = d / f".n-{src.stem}.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-ac", "2", "-ar", str(SR), str(norm)], check=True)
        parts.append(norm)
        t += dur
    sil(1.5)
    tl["sections"][-1]["end"] = round(t, 3)
    tl["duration"] = round(t, 3)
    lst = d / ".concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le",
                    str(d / "master.wav")], check=True)
    (HERE / f"timeline-{pieza}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    print(f"✓ master {t:.1f} s ({t / 60:.1f} min) · {len(tl['beats'])} beats → timeline-{pieza}.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pieza", choices=["largo", "s1", "s2"])
    ap.add_argument("cmd", choices=["audio", "words", "master", "all"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.cmd in ("audio", "all"):
        cmd_audio(a.pieza, a.force)
    if a.cmd in ("words", "all"):
        cmd_words(a.pieza, a.force)
    if a.cmd in ("master", "all"):
        cmd_master(a.pieza)
