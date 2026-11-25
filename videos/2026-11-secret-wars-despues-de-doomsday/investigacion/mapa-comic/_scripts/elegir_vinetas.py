#!/usr/bin/env python3
"""Elige con Gemini (solo texto) la viñeta que mejor ilustra cada beat de los specs de LF03.

  python3 elegir_vinetas.py            # todas las secciones
  python3 elegir_vinetas.py c3 c4      # solo esas

Lee los beat(S, "frase", pág, …) de _motion/compositions/camino-a-doomsday/_lf/secs03/*.py, busca la oración del
guion que contiene la frase y le pasa a Gemini las viñetas de las páginas cercanas (descripción, personajes,
nº de globos, proporción). Escribe <LF03>/vinetas-elegidas.json: {"<sec>|<frase>": [pág, n, "motivo"]}.
_k.beat() usa esa elección si existe (si no, la viñeta de mayor valor_video de la página indicada).
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

MAPA = Path(__file__).resolve().parent.parent
LF = MAPA.parent
SECS = LF.parents[2] / "_motion/compositions/camino-a-doomsday/_lf/secs03"
OUT = LF / "vinetas-elegidas.json"
GUION = (LF / "guion.md").read_text()
NARR = [l[2:].strip() for l in GUION.split("## 3. Guion")[1].split("## 4.")[0].splitlines() if l.startswith("> ")]
FIX = {"Chalá": "T'Challa", "Grut": "Groot", "Jíkman": "Hickman"}


def oracion(frase):
    f = frase
    for a, b in FIX.items():
        f = f.replace(a, b)
    for l in NARR:
        if f.lower() in l.lower():
            return l
    return frase


def panel_info(p):
    jf = MAPA / "json" / f"page-{p:03d}.json"
    if not jf.exists():
        return []
    d = json.loads(jf.read_text())
    if d["tipo"] not in ("historia", "portada", "portada_alternativa"):
        return []
    out = []
    for v in d["vinetas"]:
        if not v.get("recorte"):
            continue
        y0, x0, y1, x1 = v["bbox"]
        asp = ((x1 - x0) * d["ancho"]) / max(1, (y1 - y0) * d["alto"])
        area = (x1 - x0) * (y1 - y0) / 1e6
        if area < 0.04:
            continue
        out.append({"id": f"{p}:{v['n']}", "desc": v["descripcion"], "personajes": v["personajes"][:6],
                    "globos": sum(1 for t in v["textos"] if t["tipo"] != "sfx"), "aspecto": round(asp, 2),
                    "valor": v["valor_video"]})
    return out


def beats(sec):
    src = (SECS / f"{sec}.py").read_text()
    return [(m.group(1), int(m.group(2))) for m in re.finditer(r'beat\(S, "([^"]+)", (\d+)', src)]


def gemini(prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return json.loads(r["candidates"][0]["content"]["parts"][0]["text"])


def main():
    secs = sys.argv[1:] or [f.stem for f in sorted(SECS.glob("*.py")) if not f.stem.startswith("_")]
    res = json.loads(OUT.read_text()) if OUT.exists() else {}
    for sec in secs:
        bs = beats(sec)
        if not bs:
            continue
        pages = sorted({q for _, p in bs for q in range(p - 4, p + 5) if 1 <= q <= 282})
        cands = [c for p in pages for c in panel_info(p)]
        items = [{"key": f"{sec}|{f}", "frase_ancla": f, "oracion_narrada": oracion(f), "pagina_sugerida": p} for f, p in bs]
        prompt = (
            "Eres editor de un video explicativo de YouTube (16:9) que narra el cómic Secret Wars (2015). Para cada BEAT "
            "elige la viñeta de CANDIDATAS que mejor ilustra visualmente la oración narrada en el momento de la frase ancla.\n"
            "Criterios, en orden: 1) que muestre exactamente lo que se dice (personaje o acción correctos); 2) imagen clara "
            "y fuerte; 3) pocos globos de texto; 4) aspecto entre 0.9 y 2.4 (encaja en pantalla horizontal); "
            "5) NO repetir la misma viñeta en dos beats de la lista. La página sugerida es orientativa.\n"
            'Responde JSON: [{"key": "...", "id": "pág:n", "motivo": "breve"}] con un elemento por beat.\n\n'
            f"BEATS:\n{json.dumps(items, ensure_ascii=False)}\n\nCANDIDATAS:\n{json.dumps(cands, ensure_ascii=False)}")
        for e in gemini(prompt):
            p, n = e["id"].split(":")
            res[e["key"]] = [int(p), int(n), e.get("motivo", "")]
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(f"✓ {sec}: {len(bs)} beats · {len(cands)} candidatas")


if __name__ == "__main__":
    main()
