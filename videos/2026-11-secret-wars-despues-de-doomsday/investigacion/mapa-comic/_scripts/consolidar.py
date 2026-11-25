#!/usr/bin/env python3
"""Paso 2: consolida mapa/json/page-*.json en índices navegables.

  python3 consolidar.py            # índices deterministas (sin API)
  python3 consolidar.py --eventos  # además, línea de tiempo de eventos por número con Gemini (solo texto)

Salida en mapa/:
  paginas.json        índice plano (página, número de cómic corregido, tipo, resumen, personajes, eventos)
  personajes.json     personaje -> páginas y nº de líneas
  etiquetas.json      etiqueta -> viñetas (ordenadas por valor_video)
  historia.md         por número: páginas, resumen por página y (con --eventos) eventos clave
  assets.md           mejores viñetas por etiqueta con su recorte
  guion-fuente.md     diálogo completo en orden (quién: texto original / traducción), para escribir guiones
"""
import json, os, re, sys, urllib.request
from collections import defaultdict
from pathlib import Path

MAPA = Path(__file__).resolve().parent.parent
J = MAPA / "json"


def canon(nombre):
    n = re.sub(r"\s*\(.*?\)\s*", " ", nombre).strip()
    alias = {"Dios Emperador Doom": "Doctor Doom", "Doctor Doom / Dios Emperador Doom": "Doctor Doom", "Doom": "Doctor Doom",
             "Reed Richards": "Mister Fantástico", "Sheriff Strange": "Doctor Strange", "Mujer Invisible": "Sue Storm",
             "Sue Storm / Mujer Invisible": "Sue Storm", "T'Challa": "Black Panther", "Owen Reece": "Hombre Molécula"}
    n = n.split(" / ")[0].strip() if n not in alias else n
    return alias.get(n, n)


def cargar():
    pags = [json.loads(f.read_text()) for f in sorted(J.glob("page-*.json"))]
    # Número de cómic por rangos de página, fijados a mano (2026-11-18) con las páginas de título
    # "0N" y, para #8 y #9 (sin página de título en este PDF), la sinopsis de cada número.
    # El modelo marcaba como título los separadores internos (46, 84, 94, 99, 152, 245).
    for p in pags:
        p["numero"] = next((n for a, b, n in NUMEROS if a <= p["pagina"] <= b), None)
    return pags


# (desde, hasta, número). None = material del tomo (portada, créditos, galería de portadas).
NUMEROS = [(1, 3, None), (4, 40, 1), (41, 85, 2), (86, 108, 3), (109, 129, 4), (130, 150, 5),
           (151, 177, 6), (178, 197, 7), (198, 220, 8), (221, 255, 9), (256, 265, 0), (266, 282, None)]


def llamar_texto(prompt, modelo="gemini-3.5-flash"):
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                                 data=json.dumps(body).encode(), headers={
                                     "Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["candidates"][0]["content"]["parts"][0]["text"]


def main():
    eventos = "--eventos" in sys.argv
    pags = cargar()
    idx, pers, etq = [], defaultdict(lambda: {"paginas": set(), "lineas": 0}), defaultdict(list)
    for p in pags:
        idx.append({k: p.get(k) for k in ["pagina", "numero", "tipo", "resumen", "lugar", "personajes", "eventos_clave", "archivo"]})
        for c in p.get("personajes", []):
            pers[canon(c)]["paginas"].add(p["pagina"])
        for v in p["vinetas"]:
            for t in v["textos"]:
                if t["tipo"] in ("dialogo", "pensamiento"):
                    pers[canon(t["quien"])]["lineas"] += 1
            for e in v.get("etiquetas", []):
                etq[e].append({"pagina": p["pagina"], "numero": p["numero"], "n": v["n"], "valor": v["valor_video"],
                               "recorte": v.get("recorte"), "descripcion": v["descripcion"], "prompt_en": v["prompt_en"]})
    (MAPA / "paginas.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1))
    pj = {k: {"paginas": sorted(v["paginas"]), "apariciones": len(v["paginas"]), "lineas": v["lineas"]}
          for k, v in sorted(pers.items(), key=lambda kv: -len(kv[1]["paginas"]))}
    (MAPA / "personajes.json").write_text(json.dumps(pj, ensure_ascii=False, indent=1))
    ej = {k: sorted(v, key=lambda x: -x["valor"]) for k, v in sorted(etq.items(), key=lambda kv: -len(kv[1]))}
    (MAPA / "etiquetas.json").write_text(json.dumps(ej, ensure_ascii=False, indent=1))

    # guion-fuente.md: diálogo en orden de lectura
    por_num = defaultdict(list)
    for p in pags:
        por_num[p["numero"]].append(p)
    g = ["# Secret Wars (2015): diálogo en orden\n", "Formato: `quien: original` / _traducción_. Solo páginas de historia.\n"]
    for num, ps in por_num.items():
        g.append(f"\n## Número {num}\n")
        for p in ps:
            if p["tipo"] != "historia":
                continue
            g.append(f"\n### Pág. {p['pagina']} · {p.get('lugar') or ''}\n_{p['resumen']}_\n")
            for v in p["vinetas"]:
                g.append(f"- **V{v['n']}** ({v['descripcion']})")
                for t in v["textos"]:
                    if t["tipo"] == "sfx":
                        continue
                    g.append(f"  - {t['quien']}: {t['texto']} / _{t.get('texto_es', '')}_")
    (MAPA / "guion-fuente.md").write_text("\n".join(g) + "\n")

    # historia.md
    h = ["# Secret Wars (2015): mapa de la historia\n"]
    for num, ps in por_num.items():
        rango = f"págs. {ps[0]['pagina']}–{ps[-1]['pagina']}"
        h.append(f"\n## Número {num} ({rango})\n" if num is not None else "\n## Material del tomo (portada, créditos, galería de portadas)\n")
        if eventos and num is not None:
            resumenes = "\n".join(f"p{p['pagina']}: {p['resumen']} | eventos: {'; '.join(p['eventos_clave'])}"
                                  for p in ps if p["tipo"] == "historia")
            h.append(llamar_texto(
                "A partir de estos resúmenes por página del número " + str(num) + " de Secret Wars (2015), escribe en español "
                "una lista de 6 a 12 EVENTOS CLAVE en orden cronológico. Formato por línea: "
                "`- **Evento** (págs. X–Y): una o dos frases.` Sin introducción.\n\n" + resumenes).strip() + "\n")
        h.append("\n<details><summary>Página por página</summary>\n")
        for p in ps:
            h.append(f"- **{p['pagina']}** [{p['tipo']}] {p['resumen']}")
        h.append("\n</details>\n")
    (MAPA / "historia.md").write_text("\n".join(h) + "\n")

    # assets.md
    a = ["# Assets: mejores viñetas por etiqueta\n", "Ordenadas por valor_video. Recortes en `vinetas/`.\n"]
    for e, vs in ej.items():
        top = [v for v in vs if v["valor"] >= 4][:8]
        if not top:
            continue
        a.append(f"\n## {e} ({len(vs)} viñetas)\n")
        for v in top:
            a.append(f"- `{v['recorte']}` ★{v['valor']} #{v['numero']}: {v['descripcion']}")
    (MAPA / "assets.md").write_text("\n".join(a) + "\n")
    print(f"{len(pags)} páginas, {len(pj)} personajes, {len(ej)} etiquetas")


if __name__ == "__main__":
    main()
