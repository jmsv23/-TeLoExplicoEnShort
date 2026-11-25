#!/usr/bin/env python3
"""Mapa estructurado de Secret Wars (2015) página por página con Gemini.

Uso (desde cualquier carpeta, con GEMINI_API_KEY en el entorno):
  python3 mapear.py paginas 6 40 120 --modelo gemini-3.1-flash-lite --out ../_piloto/lite
  python3 mapear.py todo --modelo gemini-3.5-flash            # las 282, retoma donde quedó
  python3 mapear.py recortar [--out DIR]                      # recorta viñetas desde los JSON
  python3 mapear.py hoja 6 40 --out ../_piloto/lite           # hoja de revisión con recuadros

Salida por página: <out>/json/page-NNN.json ; viñetas: <out>/vinetas/page-NNN-vN.jpg
"""
import argparse, base64, concurrent.futures as cf, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

MAPA = Path(__file__).resolve().parent.parent
PAGINAS = MAPA / "paginas"
API = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"

REPARTO = """Reparto probable (usa estos nombres canónicos para 'quien'):
Mister Fantástico (Reed Richards, Tierra-616), El Hacedor (Reed Richards Ultimate), Doctor Doom / Dios Emperador Doom (Victor von Doom),
Doctor Strange (Sheriff Strange), Hombre Molécula (Owen Reece), Sue Storm / Mujer Invisible, Valeria Richards, Franklin Richards,
Black Panther (T'Challa), Namor, Thanos, Cisne Negro (Black Swan), Cíclope (con el Fénix), Capitana Marvel (Carol Danvers),
Thor (Jane Foster), Thor Corps (varios Thors), Star-Lord, Spider-Man (Peter Parker), Spider-Man (Miles Morales),
Maximus / El Profeta, Mister Siniestro, Apocalipsis, Maestro, Madelyne Pryor, la Cosa (Ben Grimm) / El Escudo, Antorcha Humana,
Proxima Midnight, Corvus Glaive, Manifold, Iron Man, Capitán América, Bestia, Black Bolt, Viuda Negra, Rocket, Groot, Galactus,
Capitán Britania / James Braddock, Bruja Escarlata, Hulk. Si no reconoces a alguien escribe una descripción breve entre corchetes,
p.ej. "[soldado de Doom]". Narración en cajas sin personaje = "Narrador"."""

PROMPT = """Eres un archivista de cómics. Analiza esta página del tomo recopilatorio "Secret Wars" (2015, Jonathan Hickman y Esad Ribić), edición en INGLÉS.
Página {page} de 282 del PDF{doble}.

{reparto}

Instrucciones:
1. Clasifica la página en 'tipo'.
2. Si tipo == "historia": describe TODAS las viñetas en orden de lectura (izquierda→derecha, arriba→abajo).
   Para cada viñeta transcribe TODOS los textos (globos, cajas de narración, pensamientos, onomatopeyas, letreros) EXACTAMENTE como aparecen, en orden, con 'quien' lo dice (sigue la cola del globo).
   En 'texto' va el original en inglés sin corregir (normaliza solo las mayúsculas a ortografía normal). En 'texto_es' va una traducción natural al español latino.
3. Si NO es historia (portada, portada alternativa, créditos, extra, publicidad, índice): devuelve UNA sola viñeta que cubra la imagen completa, con descripción, prompt_en y valor_video; 'textos' solo con el título o texto principal si lo hay.
4. 'bbox' = [ymin, xmin, ymax, xmax] normalizado 0-1000 sobre la imagen completa, ajustado al borde de la viñeta.
5. 'valor_video' 1-5: qué tan buena es la imagen para ilustrar un video explicativo (5 = imagen icónica, clara, de un momento clave).
6. 'etiquetas': eventos/conceptos en kebab-case (ej. "ultima-incursion", "balsa", "muerte-strange", "battleworld", "thor-corps", "el-escudo", "doom-dios", "hombre-molecula", "familia-doom").
7. 'prompt_en': prompt visual breve en inglés que describa la composición (sin nombres de marca si no hace falta).
8. 'numero_comic': número de Secret Wars (0-9) al que pertenece la página si lo puedes inferir (portada, créditos o continuidad); si no, null.
Todo lo demás en español."""

TXT = {"type": "OBJECT", "properties": {
    "tipo": {"type": "STRING", "enum": ["dialogo", "narracion", "pensamiento", "sfx", "letrero"]},
    "quien": {"type": "STRING"}, "texto": {"type": "STRING"}, "texto_es": {"type": "STRING"}}, "required": ["tipo", "quien", "texto", "texto_es"]}
VIN = {"type": "OBJECT", "properties": {
    "n": {"type": "INTEGER"},
    "bbox": {"type": "ARRAY", "items": {"type": "INTEGER"}},
    "descripcion": {"type": "STRING"}, "prompt_en": {"type": "STRING"},
    "personajes": {"type": "ARRAY", "items": {"type": "STRING"}},
    "lugar": {"type": "STRING"}, "tono": {"type": "STRING"},
    "valor_video": {"type": "INTEGER"},
    "etiquetas": {"type": "ARRAY", "items": {"type": "STRING"}},
    "textos": {"type": "ARRAY", "items": TXT}},
    "required": ["n", "bbox", "descripcion", "prompt_en", "personajes", "valor_video", "etiquetas", "textos"]}
SCHEMA = {"type": "OBJECT", "properties": {
    "tipo": {"type": "STRING", "enum": ["historia", "portada", "portada_alternativa", "creditos", "titulo_capitulo", "extra", "publicidad", "indice", "otro"]},
    "numero_comic": {"type": "INTEGER", "nullable": True},
    "resumen": {"type": "STRING"}, "lugar": {"type": "STRING"},
    "personajes": {"type": "ARRAY", "items": {"type": "STRING"}},
    "eventos_clave": {"type": "ARRAY", "items": {"type": "STRING"}},
    "vinetas": {"type": "ARRAY", "items": VIN}},
    "required": ["tipo", "resumen", "personajes", "eventos_clave", "vinetas"]}


def pagina(n):
    return PAGINAS / f"page-{n:03d}.jpg"


def llamar(modelo, img, prompt, intentos=5):
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(img.read_bytes()).decode()}},
        {"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "responseSchema": SCHEMA, "temperature": 0.2}}
    for i in range(intentos):
        try:
            req = urllib.request.Request(API.format(m=modelo), data=json.dumps(body).encode(), headers={
                "Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            return json.loads(r["candidates"][0]["content"]["parts"][0]["text"]), r.get("usageMetadata", {})
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as e:
            msg = e.read().decode()[:300] if isinstance(e, urllib.error.HTTPError) else repr(e)
            print(f"  reintento {i+1} ({msg})", file=sys.stderr)
            time.sleep(min(60, 4 * 2 ** i))
    raise RuntimeError("sin respuesta")


def procesar(n, modelo, out):
    dest = out / "json" / f"page-{n:03d}.json"
    if dest.exists():
        return n, "ya"
    img = pagina(n)
    w, h = Image.open(img).size
    doble = " (página DOBLE horizontal: trátala como una sola escena ancha)" if w > h else ""
    t0 = time.time()
    data, uso = llamar(modelo, img, PROMPT.format(page=n, doble=doble, reparto=REPARTO))
    data.update({"pagina": n, "archivo": f"paginas/{img.name}", "ancho": w, "alto": h, "doble": w > h,
                 "_modelo": modelo, "_tokens": uso.get("totalTokenCount"), "_seg": round(time.time() - t0, 1)})
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    return n, f"{data['tipo']} #{data.get('numero_comic')} {len(data['vinetas'])} viñetas {data['_seg']}s {data['_tokens']}tok"


def recortar(out, pad=6):
    vd = out / "vinetas"
    vd.mkdir(parents=True, exist_ok=True)
    total = 0
    for jf in sorted((out / "json").glob("page-*.json")):
        d = json.loads(jf.read_text())
        im = Image.open(MAPA / d["archivo"]).convert("RGB")
        W, H = im.size
        for v in d["vinetas"]:
            b = v.get("bbox") or []
            if len(b) != 4:
                continue
            y0, x0, y1, x1 = b
            box = (max(0, x0 * W // 1000 - pad), max(0, y0 * H // 1000 - pad),
                   min(W, x1 * W // 1000 + pad), min(H, y1 * H // 1000 + pad))
            if box[2] - box[0] < 40 or box[3] - box[1] < 40:
                continue
            name = f"page-{d['pagina']:03d}-v{v['n']}.jpg"
            im.crop(box).save(vd / name, quality=92)
            v["recorte"] = f"vinetas/{name}"
            total += 1
        jf.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    print(f"{total} viñetas recortadas en {vd}")


def hoja(nums, out, ancho=520):
    """Páginas con los recuadros dibujados, lado a lado, para revisión."""
    tiles = []
    for n in nums:
        jf = out / "json" / f"page-{n:03d}.json"
        if not jf.exists():
            continue
        d = json.loads(jf.read_text())
        im = Image.open(MAPA / d["archivo"]).convert("RGB")
        W, H = im.size
        dr = ImageDraw.Draw(im)
        for v in d["vinetas"]:
            if len(v.get("bbox") or []) != 4:
                continue
            y0, x0, y1, x1 = v["bbox"]
            dr.rectangle([x0 * W / 1000, y0 * H / 1000, x1 * W / 1000, y1 * H / 1000], outline=(255, 0, 255), width=6)
            dr.text((x0 * W / 1000 + 10, y0 * H / 1000 + 6), str(v["n"]), fill=(255, 0, 255),
                    font=ImageFont.load_default(size=60))
        im.thumbnail((ancho, ancho * 2))
        tiles.append(im)
    if not tiles:
        return
    hmax = max(t.height for t in tiles)
    sheet = Image.new("RGB", (sum(t.width for t in tiles) + 10 * len(tiles), hmax), "white")
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0))
        x += t.width + 10
    p = out / "hoja.jpg"
    sheet.save(p, quality=80)
    print(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["paginas", "todo", "recortar", "hoja"])
    ap.add_argument("nums", nargs="*", type=int)
    ap.add_argument("--modelo", default="gemini-3.5-flash")
    ap.add_argument("--out", default=str(MAPA))
    ap.add_argument("--hilos", type=int, default=4)
    a = ap.parse_args()
    out = Path(a.out).resolve()
    if a.accion == "recortar":
        return recortar(out)
    if a.accion == "hoja":
        return hoja(a.nums, out)
    nums = a.nums if a.accion == "paginas" else list(range(1, len(list(PAGINAS.glob("page-*.jpg"))) + 1))
    fallos = []
    with cf.ThreadPoolExecutor(a.hilos) as ex:
        futs = {ex.submit(procesar, n, a.modelo, out): n for n in nums}
        for f in cf.as_completed(futs):
            try:
                n, s = f.result()
                print(f"page {n:03d}: {s}", flush=True)
            except Exception as e:
                fallos.append(futs[f])
                print(f"page {futs[f]:03d}: FALLO {e}", flush=True)
    print(f"listo. fallos: {sorted(fallos)}")


if __name__ == "__main__":
    main()
