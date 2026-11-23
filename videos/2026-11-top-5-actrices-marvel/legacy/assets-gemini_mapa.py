#!/usr/bin/env python3
"""Mapa de escenas de UN video con Gemini (gemini-3.1-flash-lite, media resolution MEDIUM).

REGLA: una sola corrida por video. Si ya existe _mapas/<video>.json, se niega a correr.
No reintenta la llamada de análisis (solo la subida del archivo).

Tiempos (patrón de fenix-clipper/workers/gemini-process):
  1. ffprobe mide duración, FPS y time_base, y van al prompt como "VIDEO METADATA CONTEXT".
  2. Restricciones duras: ningún tiempo pasa de la duración y todos van en HH:MM:SS.
  3. smart_parse() usa la duración como ancla para recuperar formatos mal puestos (MM:SS:ff como HH:MM:SS).
  4. Los fragmentos con sonido se ajustan a las palabras de WhisperX (_transcripciones/<video>.json).

Uso (desde content-creator/, para cargar la key sin imprimirla):
  set -a; . ./.env; set +a
  python3 -P explicando/top-5-actrices-marvel-mas-guapas/assets/gemini_mapa.py esc-endgame-wanda "contexto del bloque del guion"
"""
import json, mimetypes, os, re, subprocess, sys, time, urllib.request
from fractions import Fraction
from pathlib import Path

MODELO = "gemini-3.1-flash-lite"
BASE = "https://generativelanguage.googleapis.com"
AQUI = Path(__file__).parent
PAD_PALABRA = 0.15  # margen hacia afuera al ajustar a una palabra (igual que fenix-clipper)

SISTEMA = """Eres editor de video para un canal de YouTube en español sobre cine. Estamos haciendo un video
de ~8 minutos: el top 5 de actrices de Marvel (Zoe Saldaña, Natalie Portman, Zendaya, Elizabeth Olsen y
Scarlett Johansson), con estética de revista de moda. Buscamos momentos donde la actriz luzca y brille.
Tu trabajo es mapear una escena y elegir fragmentos MUY cortos que retengan la atención del espectador.
Inspecciona cuadros del inicio, del medio y del final del video antes de responder: analiza la línea de
tiempo COMPLETA, no solo el principio."""

CONTEXTO_USUARIO = """VIDEO METADATA CONTEXT:
- Filename: "{archivo}"
- MIME Type: {mime}
- Total Duration: {dur_s} seconds ({dur_hms})
- FPS: {fps}
- TIMEBASE: {timebase}
- Resolution: {ancho}x{alto}

STRICT TECHNICAL CONSTRAINTS:
1. **Boundary Check:** NO timestamp (start or end) can exceed {dur_s} seconds ({dur_hms}).
2. **Format:** All timestamps must be in "HH:MM:SS" format (e.g., "00:01:30"). Never MM:SS:frames.
3. **Full coverage:** "planos" must start at 00:00:00 and the last one must end at {dur_hms}, with no gaps.
4. **Speech padding:** for a fragment that contains dialogue, start slightly before the first word and end
   about 0.5 s after the last word finishes. Never cut a word.

CONTEXTO DEL BLOQUE DEL GUION donde se usará esta escena:
{contexto}

QUÉ DEVOLVER (JSON del esquema):
- "planos": momentos consecutivos de 5 a 20 s que cubran TODO el video. Describe en español lo que pasa
  visualmente, en una frase concreta.
- "destacados": entre 4 y 8 fragmentos de 2 a 8 s cada uno, ordenados de mejor a peor, espectaculares,
  icónicos o fáciles de entender sin contexto (alguien que no vio la película debe captar qué pasa en
  3 segundos). Prefiere fragmentos que empiecen y terminen en un corte de plano.
  - uso="escena_con_sonido": el audio original aporta (una frase memorable, un golpe sonoro claro).
  - uso="broll_mudo": funciona sin audio, como fondo mientras habla un narrador.
  - Indica si encaja con el contexto del guion y por qué.
- "evitar": tramos que NO deben usarse: logos, marcas de agua, texto sobreimpreso, placas finales,
  negros, planos borrosos o confusos, contenido violento explícito.
- Si hay diálogo en inglés, transcríbelo literal en "dialogo".
"""

HMS = {"type": "string", "description": "HH:MM:SS"}
SCHEMA = {
    "type": "object",
    "properties": {
        "resumen": {"type": "string", "description": "Qué pasa en la escena, 2-3 frases en español"},
        "duracion": HMS,
        "planos": {"type": "array", "items": {"type": "object", "properties": {
            "inicio": HMS, "fin": HMS,
            "descripcion": {"type": "string"},
            "actriz_visible": {"type": "boolean"},
            "tipo": {"type": "string", "enum": ["dialogo", "persecucion", "pelea", "explosion", "acrobacia",
                                                 "vehiculo", "establecimiento", "reaccion", "humor", "otro"]},
            "intensidad": {"type": "integer", "description": "1 calma - 5 máxima acción"},
            "audio": {"type": "string", "enum": ["dialogo", "musica", "efectos", "mixto", "silencio"]},
            "dialogo": {"type": "string", "description": "Diálogo literal en inglés o cadena vacía"},
        }, "required": ["inicio", "fin", "descripcion", "actriz_visible", "tipo", "intensidad", "audio", "dialogo"]}},
        "destacados": {"type": "array", "items": {"type": "object", "properties": {
            "inicio": HMS, "fin": HMS,
            "titulo": {"type": "string", "description": "Nombre corto del momento, en español"},
            "por_que_retiene": {"type": "string"},
            "uso": {"type": "string", "enum": ["escena_con_sonido", "broll_mudo"]},
            "retencion": {"type": "integer", "description": "1-10, qué tanto engancha"},
            "se_entiende_solo": {"type": "boolean"},
            "corte_limpio": {"type": "boolean", "description": "Empieza y termina en corte de plano"},
            "encaja_guion": {"type": "string", "description": "Cómo apoya el contexto del guion, o 'no encaja'"},
        }, "required": ["inicio", "fin", "titulo", "por_que_retiene", "uso", "retencion",
                        "se_entiende_solo", "corte_limpio", "encaja_guion"]}},
        "evitar": {"type": "array", "items": {"type": "object", "properties": {
            "inicio": HMS, "fin": HMS, "motivo": {"type": "string"},
        }, "required": ["inicio", "fin", "motivo"]}},
    },
    "required": ["resumen", "duracion", "planos", "destacados", "evitar"],
}


# ---------- tiempos ----------

def sonda(video):
    """Duración, FPS, time_base y tamaño con ffprobe."""
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=r_frame_rate,time_base,width,height:format=duration", "-of", "json",
                                   str(video)], capture_output=True, text=True, check=True).stdout)
    st = j["streams"][0]
    return {"dur": float(j["format"]["duration"]), "fps": round(float(Fraction(st["r_frame_rate"])), 3),
            "timebase": st["time_base"], "ancho": st["width"], "alto": st["height"]}


def hms(t):
    t = max(0, int(round(t)))
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def smart_parse(texto, dur):
    """HH:MM:SS, MM:SS, MM:SS:ff o SS → segundos, usando la duración como ancla (port de timeSanitize.ts)."""
    partes = [float(p or 0) for p in re.sub(r"[^0-9:.]", "", str(texto)).split(":")]
    if len(partes) == 3:
        std = partes[0] * 3600 + partes[1] * 60 + partes[2]
        if std <= dur + 5:
            return min(std, dur), False
    if len(partes) >= 2:  # MM:SS:ff puesto como HH:MM:SS
        corr = partes[0] * 60 + partes[1] + (partes[2] / 100 if len(partes) > 2 else 0)
        if corr <= dur:
            return corr, len(partes) == 3
    if len(partes) == 1:
        return min(partes[0], dur), False
    print(f"⚠ tiempo irrecuperable: {texto} (duración {dur:.0f}s); se recorta al final")
    return dur, True


def palabras(nombre):
    p = AQUI / "_transcripciones" / f"{nombre}.json"
    if not p.exists():
        return []
    return [w for s in json.loads(p.read_text())["sentences"] for w in s["words"]
            if isinstance(w.get("start"), (int, float)) and isinstance(w.get("end"), (int, float)) and w["end"] > w["start"]]


def ajustar_a_palabras(ini, fin, ws, dur):
    """Ajusta inicio/fin a la palabra más cercana, con margen hacia afuera (port de refineTimestampRangeToTranscript)."""
    if not ws:
        return ini, fin, False
    dist = lambda t, w: w["start"] - t if t < w["start"] else (t - w["end"] if t > w["end"] else 0)
    wi = min(ws, key=lambda w: dist(ini, w))
    wf = min(ws, key=lambda w: dist(fin, w))
    ni, nf = max(0, wi["start"] - PAD_PALABRA), min(dur, wf["end"] + PAD_PALABRA)
    # solo si la palabra cae cerca (≤2 s) y el rango sigue siendo válido
    if nf <= ni or dist(ini, wi) > 2 or dist(fin, wf) > 2:
        return ini, fin, False
    return round(ni, 2), round(nf, 2), True


def normalizar(data, dur, ws):
    """Agrega inicio_s/fin_s saneados; marca correcciones y ajustes a palabras."""
    for lista in ("planos", "destacados", "evitar"):
        for it in data.get(lista, []):
            a, ca = smart_parse(it["inicio"], dur)
            b, cb = smart_parse(it["fin"], dur)
            if b < a:
                a, b = b, a
            it["inicio_s"], it["fin_s"] = round(a, 2), round(b, 2)
            if ca or cb:
                it["_tiempo_corregido"] = True
            if lista == "destacados" and it.get("uso") == "escena_con_sonido":
                it["inicio_s"], it["fin_s"], it["_ajustado_a_palabras"] = ajustar_a_palabras(a, b, ws, dur)
    return data


# ---------- API ----------

def req(url, data=None, headers=None, method=None):
    h = {"x-goog-api-key": os.environ["GEMINI_API_KEY"], **(headers or {})}
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=600) as resp:
        return resp.headers, resp.read()


def subir(path):
    mime = mimetypes.guess_type(path)[0] or "video/mp4"
    size = path.stat().st_size
    for intento in range(3):
        try:
            h, _ = req(f"{BASE}/upload/v1beta/files", json.dumps({"file": {"display_name": path.stem}}).encode(), {
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
        time.sleep(4)
        _, body = req(f"{BASE}/v1beta/{f['name']}")
        f = json.loads(body)
    if f.get("state") != "ACTIVE":
        sys.exit(f"el archivo quedó en estado {f.get('state')}")
    return f, mime


def main():
    nombre, contexto = sys.argv[1], sys.argv[2]
    out = AQUI / "_mapas" / f"{nombre}.json"
    if out.exists():
        sys.exit(f"YA EXISTE {out}: una sola corrida por video. No se vuelve a gastar.")
    out.parent.mkdir(exist_ok=True)
    video = AQUI / "video" / f"{nombre}.mp4"
    m = sonda(video)
    t0 = time.time()
    f, mime = subir(video)
    print(f"subido {f['name']} en {time.time() - t0:.0f}s; analizando con {MODELO} ({hms(m['dur'])}, {m['fps']} fps)…")
    texto = CONTEXTO_USUARIO.format(archivo=video.name, mime=mime, dur_s=f"{m['dur']:.2f}", dur_hms=hms(m["dur"]),
                                    fps=m["fps"], timebase=m["timebase"], ancho=m["ancho"], alto=m["alto"],
                                    contexto=contexto)
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
    data = normalizar(json.loads(r["candidates"][0]["content"]["parts"][0]["text"]), m["dur"], palabras(nombre))
    cubre = max((p["fin_s"] for p in data["planos"]), default=0)
    if cubre < 0.9 * m["dur"]:
        print(f"⚠ AVISO: los planos solo cubren hasta {hms(cubre)} de {hms(m['dur'])}: verificar tiempos a mano")
    data["_meta"] = {"modelo": MODELO, "media_resolution": "MEDIUM", "video": video.name, "sonda": m,
                     "uso": r.get("usageMetadata"), "seg": round(time.time() - t0, 1), "contexto": contexto}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    u = r.get("usageMetadata", {})
    print(f"ok → {out}  tokens: entrada {u.get('promptTokenCount')}, salida {u.get('candidatesTokenCount')}")


if __name__ == "__main__":
    main()
