#!/usr/bin/env python3
"""Mapa de MOMENTOS de una recopilación de streamers con Gemini (gemini-3.1-flash-lite, MEDIA_RESOLUTION_MEDIUM).

Adaptado de evolucion-del-gta/assets/gemini_mapa.py.
REGLA: una sola corrida por video. Si ya existe _mapas/<video>.json, se niega a correr.
Solo reintenta la subida, nunca la llamada de análisis.

Uso (desde content-creator/, para cargar la key sin imprimirla):
  set -a; . ./.env; set +a
  python3 -P explicando/mejores-momentos-de-gta6/assets/gemini_mapa.py 01_es_streamers_6wA7C9ooKUc
"""
import csv, json, mimetypes, os, re, subprocess, sys, time, urllib.request
from fractions import Fraction
from pathlib import Path

MODELO = "gemini-3.1-flash-lite"
BASE = "https://generativelanguage.googleapis.com"
AQUI = Path(__file__).parent
PROY = AQUI.parent
PAD_PALABRA = 0.15

SISTEMA = """Eres editor de un canal de YouTube en español sobre videojuegos. Estamos armando un TOP de los mejores
momentos de streamers jugando GTA 6 (lanzado el 19 nov 2026): un video largo de ~12 min tipo ranking y 2 Shorts.
Tu trabajo es mapear UNA recopilación y separar cada momento individual con tiempos exactos, para elegir los
más graciosos, sorprendentes o virales. Aquí la cara del streamer (facecam) y su reacción SON el contenido.
Analiza la línea de tiempo COMPLETA (inicio, medio y final), no solo el principio."""

CONTEXTO_USUARIO = """VIDEO METADATA CONTEXT:
- Filename: "{archivo}"
- MIME Type: {mime}
- Total Duration: {dur_s} seconds ({dur_hms})
- FPS: {fps}
- Resolution: {ancho}x{alto}

STRICT TECHNICAL CONSTRAINTS:
1. **Boundary Check:** NO timestamp can exceed {dur_s} seconds ({dur_hms}).
2. **Format:** All timestamps "HH:MM:SS" (e.g. "00:01:30"). Never MM:SS:frames.
3. **Full coverage:** "momentos" must cover the whole video in order, from 00:00:00 to {dur_hms}; intros,
   transitions, end screens also go in "momentos" with retencion 1.
4. **Speech padding:** start slightly before the first word of the setup and end ~0.5 s after the punchline/
   reaction finishes. Never cut a word or the reaction.

CAPÍTULOS QUE PUSO QUIEN SUBIÓ EL VIDEO (pistas, pueden estar desfasados o faltar):
{capitulos}

QUÉ DEVOLVER (JSON del esquema):
- "momentos": cada momento individual (normalmente 8-60 s): streamer (nombre si se ve/oye en pantalla, overlay
  o capítulo; si no, "desconocido"), título corto en español, qué pasa (setup → remate) en una frase concreta,
  tipo, retención 1-10 (10 = imposible no verlo, lo comparte cualquiera), si se entiende sin contexto,
  idioma hablado, frase clave LITERAL (la que lo hace gracioso, en su idioma original), si hay facecam,
  overlays ajenos (marca de agua del recopilador, subtítulos quemados, emojis, texto, logos).
  - "short_vertical": ¿funciona en un Short 9:16 recortando el gameplay + facecam? true/false.
  - "riesgo": "ninguno" o motivo (desnudos/club de striptease, violencia explícita contra civiles muy gráfica,
    insultos racistas, música con derechos sonando fuerte, contenido de otro juego, momento repetido de otro video).
- "mejores": los 6 a 10 MEJORES momentos del video, de mejor a peor, con inicio/fin ajustados al tramo más
  apretado que conserva setup + remate + reacción (5 a 40 s), y "hook": la primera línea de texto que pondrías
  en pantalla para engancharlo, en español, máx 7 palabras.
"""

HMS = {"type": "string", "description": "HH:MM:SS"}
SCHEMA = {
    "type": "object",
    "properties": {
        "resumen": {"type": "string", "description": "Qué contiene la recopilación, 2-3 frases en español"},
        "duracion": HMS,
        "momentos": {"type": "array", "items": {"type": "object", "properties": {
            "inicio": HMS, "fin": HMS,
            "streamer": {"type": "string"},
            "titulo": {"type": "string"},
            "que_pasa": {"type": "string"},
            "tipo": {"type": "string", "enum": ["humor", "fail", "susto", "epico", "asombro_graficos", "bug",
                                                 "easter_egg", "reaccion", "intro_transicion", "otro"]},
            "retencion": {"type": "integer", "description": "1-10"},
            "se_entiende_solo": {"type": "boolean"},
            "idioma": {"type": "string", "enum": ["es", "en", "otro", "sin_voz"]},
            "frase_clave": {"type": "string"},
            "facecam": {"type": "boolean"},
            "overlays": {"type": "string", "description": "overlays ajenos o 'ninguno'"},
            "short_vertical": {"type": "boolean"},
            "riesgo": {"type": "string"},
        }, "required": ["inicio", "fin", "streamer", "titulo", "que_pasa", "tipo", "retencion", "se_entiende_solo",
                        "idioma", "frase_clave", "facecam", "overlays", "short_vertical", "riesgo"]}},
        "mejores": {"type": "array", "items": {"type": "object", "properties": {
            "inicio": HMS, "fin": HMS,
            "streamer": {"type": "string"},
            "titulo": {"type": "string"},
            "por_que": {"type": "string"},
            "retencion": {"type": "integer", "description": "1-10"},
            "hook": {"type": "string"},
        }, "required": ["inicio", "fin", "streamer", "titulo", "por_que", "retencion", "hook"]}},
    },
    "required": ["resumen", "duracion", "momentos", "mejores"],
}


def sonda(video):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=r_frame_rate,width,height:format=duration", "-of", "json", str(video)],
                                  capture_output=True, text=True).stdout)
    st = j["streams"][0]
    return {"dur": float(j["format"]["duration"]), "fps": round(float(Fraction(st["r_frame_rate"])), 3),
            "ancho": st["width"], "alto": st["height"]}


def hms(t):
    t = max(0, int(round(t)))
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def smart_parse(texto, dur):
    partes = [float(p or 0) for p in re.sub(r"[^0-9:.]", "", str(texto)).split(":")]
    if len(partes) == 3:
        std = partes[0] * 3600 + partes[1] * 60 + partes[2]
        if std <= dur + 5:
            return min(std, dur), False
    if len(partes) >= 2:
        corr = partes[0] * 60 + partes[1] + (partes[2] / 100 if len(partes) > 2 else 0)
        if corr <= dur:
            return corr, len(partes) == 3
    if len(partes) == 1:
        return min(partes[0], dur), False
    return dur, True


def palabras(nombre):
    p = AQUI / "_transcripciones" / f"{nombre}.json"
    if not p.exists():
        return []
    return [w for s in json.loads(p.read_text())["sentences"] for w in s["words"]
            if isinstance(w.get("start"), (int, float)) and isinstance(w.get("end"), (int, float)) and w["end"] > w["start"]]


def ajustar_a_palabras(ini, fin, ws, dur):
    if not ws:
        return ini, fin, False
    dist = lambda t, w: w["start"] - t if t < w["start"] else (t - w["end"] if t > w["end"] else 0)
    wi = min(ws, key=lambda w: dist(ini, w))
    wf = min(ws, key=lambda w: dist(fin, w))
    ni, nf = max(0, wi["start"] - PAD_PALABRA), min(dur, wf["end"] + PAD_PALABRA)
    if nf <= ni or dist(ini, wi) > 2 or dist(fin, wf) > 2:
        return ini, fin, False
    # solo expandir: nunca recortar el tramo que Gemini marcó (no cortar la reacción)
    return round(min(ini, ni), 2), round(max(fin, nf), 2), True


def normalizar(data, dur, ws):
    for lista in ("momentos", "mejores"):
        for it in data.get(lista, []):
            a, ca = smart_parse(it["inicio"], dur)
            b, cb = smart_parse(it["fin"], dur)
            if b < a:
                a, b = b, a
            it["inicio_s"], it["fin_s"] = round(a, 2), round(b, 2)
            if ca or cb:
                it["_tiempo_corregido"] = True
            if lista == "mejores":
                it["inicio_s"], it["fin_s"], it["_ajustado_a_palabras"] = ajustar_a_palabras(a, b, ws, dur)
    return data


def capitulos(nombre):
    filas = [r for r in csv.DictReader(open(PROY / "moments.csv")) if Path(r["file"]).stem == nombre]
    if not filas:
        return "(sin capítulos)"
    return "\n".join(f"- {hms(float(r['start_seconds']))}–{hms(float(r['end_seconds']))} {r['moment']}" for r in filas)


def req(url, data=None, headers=None, method=None):
    h = {"x-goog-api-key": os.environ["GEMINI_API_KEY"], **(headers or {})}
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=900) as resp:
        return resp.headers, resp.read()


def subir(path):
    mime = mimetypes.guess_type(path)[0] or "video/mp4"
    size = path.stat().st_size
    for intento in range(3):
        try:
            h, _ = req(f"{BASE}/upload/v1beta/files", json.dumps({"file": {"display_name": path.stem[:40]}}).encode(), {
                "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(size), "X-Goog-Upload-Header-Content-Type": mime,
                "Content-Type": "application/json"})
            _, body = req(h["x-goog-upload-url"], path.read_bytes(), {
                "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"})
            f = json.loads(body)["file"]
            break
        except Exception as e:
            print(f"subida falló ({e}), reintento {intento + 1}/3"); time.sleep(5)
    else:
        sys.exit("no se pudo subir el video")
    while f.get("state") == "PROCESSING":
        time.sleep(5)
        _, body = req(f"{BASE}/v1beta/{f['name']}")
        f = json.loads(body)
    if f.get("state") != "ACTIVE":
        sys.exit(f"el archivo quedó en estado {f.get('state')}")
    return f, mime


def main():
    nombre = sys.argv[1]
    out = AQUI / "_mapas" / f"{nombre}.json"
    if out.exists():
        sys.exit(f"YA EXISTE {out}: una sola corrida por video. No se vuelve a gastar.")
    out.parent.mkdir(exist_ok=True)
    video = PROY / "videos" / f"{nombre}.mp4"
    m = sonda(video)
    t0 = time.time()
    f, mime = subir(video)
    print(f"subido {f['name']} en {time.time() - t0:.0f}s; analizando con {MODELO} ({hms(m['dur'])})…")
    texto = CONTEXTO_USUARIO.format(archivo=video.name, mime=mime, dur_s=f"{m['dur']:.2f}", dur_hms=hms(m["dur"]),
                                    fps=m["fps"], ancho=m["ancho"], alto=m["alto"], capitulos=capitulos(nombre))
    body = {
        "systemInstruction": {"parts": [{"text": SISTEMA}]},
        "contents": [{"role": "user", "parts": [{"text": texto},
                                                {"fileData": {"mimeType": mime, "fileUri": f["uri"]}}]}],
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": SCHEMA,
                             "mediaResolution": "MEDIA_RESOLUTION_MEDIUM", "temperature": 0.2},
    }
    try:
        _, raw = req(f"{BASE}/v1beta/models/{MODELO}:generateContent", json.dumps(body).encode(),
                     {"Content-Type": "application/json"})
    finally:
        try:
            req(f"{BASE}/v1beta/{f['name']}", method="DELETE")
        except Exception:
            pass
    r = json.loads(raw)
    (out.parent / f".{nombre}.raw.json").write_text(raw.decode())
    data = normalizar(json.loads(r["candidates"][0]["content"]["parts"][0]["text"]), m["dur"], palabras(nombre))
    cubre = max((p["fin_s"] for p in data["momentos"]), default=0)
    if cubre < 0.9 * m["dur"]:
        print(f"⚠ AVISO: los momentos solo cubren hasta {hms(cubre)} de {hms(m['dur'])}")
    data["_meta"] = {"modelo": MODELO, "media_resolution": "MEDIUM", "video": video.name, "sonda": m,
                     "uso": r.get("usageMetadata"), "seg": round(time.time() - t0, 1)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    u = r.get("usageMetadata", {})
    print(f"ok → {out}  momentos {len(data['momentos'])}  tokens: entrada {u.get('promptTokenCount')}, salida {u.get('candidatesTokenCount')}")


if __name__ == "__main__":
    main()
