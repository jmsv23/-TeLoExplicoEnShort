"""Radar de tendencias: barrido de noticias y comunidad, saturación en YouTube y reporte puntuado.

./tl radar barrido   → research/radar/<fecha>/barrido.json + barrido.md (historias agrupadas)
./tl radar youtube   → research/radar/<fecha>/youtube.json (qué hay ya en YouTube para cada consulta)
./tl radar reporte   → valida reporte.json, calcula el puntaje, escribe reporte.md, historial y watchlist
"""
import json
import math
import re
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .proyecto import ROOT, die

RESEARCH = ROOT / "research"
RADAR = RESEARCH / "radar"
HISTORIAL = RADAR / "historial.json"
WATCHLIST = RESEARCH / "watchlist.md"

PESOS = {  # research-agent.md §7
    "demanda": 20, "momentum": 15, "oportunidad_tiempo": 10, "curiosidad": 15,
    "retencion": 10, "originalidad": 10, "credibilidad": 10, "mercado": 10,
}
# research-agent.md §5 → sello en pantalla (base/plantillas/fuentes.md)
CLASIFICACION = {
    "CONFIRMADO": ("CONFIRMADO", "oficial o evidencia primaria directa"),
    "REPORTADO": ("FILTRACIÓN", "medio serio con fuentes, sin anuncio oficial: «según <medio>». Pasa a CONFIRMADO con dos medios independientes"),
    "FILTRACION_CREIBLE": ("FILTRACIÓN", "insider con historial o evidencia; se cita quién lo dijo"),
    "RUMOR": ("FILTRACIÓN", "sin evidencia independiente: no puede ser el eje de un video"),
    "ESPECULACION": ("TEORÍA", "teoría o predicción; LECTURA si la interpretación es nuestra"),
    "DESMENTIDO": ("CONFIRMADO", "el desmentido es lo confirmado; el rumor original se nombra como rumor"),
}
URGENCIA = {
    "inmediata": "6-12 h", "alta": "24 h", "oportuna": "72 h",
    "proxima": "evento anunciado", "evergreen": "sin caducidad",
}
STOP = set("""a al and are as at be but by de del el en es for from has his how in is it its la las
lo los new of on or para por que se su the this to un una with y after over gets first will
what why who can just now more about into""".split())


# ---------------------------------------------------------------- utilidades

def _norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", t)


def _tokens(t):
    return {w for w in _norm(t).split() if len(w) > 2 and w not in STOP}


def _jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def _bx(args):
    r = subprocess.run(["bx", *args], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return {"_error": (r.stderr or r.stdout).strip()[:300]}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"_error": "respuesta no JSON"}


def _horas(page_age, age):
    """Edad en horas: page_age (ISO) si existe; si no, el texto «N hours/days ago»."""
    if page_age:
        try:
            d = datetime.fromisoformat(page_age.replace("Z", "+00:00"))
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            return max(0.0, (datetime.now(timezone.utc) - d).total_seconds() / 3600)
        except ValueError:
            pass
    m = re.match(r"(\d+)\s+(minute|hour|day|week|month)", age or "")
    if not m:
        return None
    n, u = int(m.group(1)), m.group(2)
    return n * {"minute": 1 / 60, "hour": 1, "day": 24, "week": 168, "month": 720}[u]


def _dir(fecha):
    d = RADAR / (fecha or date.today().isoformat())
    d.mkdir(parents=True, exist_ok=True)
    return d


def _historial():
    return json.loads(HISTORIAL.read_text()) if HISTORIAL.exists() else []


def _url_clave(u):
    return u.split("?")[0].split("#")[0].rstrip("/").lower()


def _claves(h):
    """Palabras de una historia reportada en cualquier idioma: titular, franquicia y slugs de las URLs de evidencia
    (los slugs vienen en el idioma del medio, así se reconoce la misma historia en el barrido en inglés)."""
    texto = " ".join([h.get("titular", ""), h.get("franquicia", "")] +
                     [re.sub(r"[-_/]", " ", _url_clave(u).split("/", 3)[-1]) for u in h.get("urls", [])])
    return sorted(w for w in _tokens(texto) if not w.isdigit() or len(w) == 4)


def _ya_reportado(tk, urls, hist):
    """Coincide si comparte una URL o si la mayoría de las palabras clave del titular del grupo están en la historia."""
    for h in hist:
        if urls & {_url_clave(u) for u in h.get("urls", [])}:
            return h["id"]
    mejor, sim = None, 0.0
    for h in hist:
        cl = set(h.get("claves") or _claves(h))
        comun = tk & cl
        s_ = len(comun) / min(len(tk), len(cl)) if tk and cl else 0
        if len(comun) >= 3 and s_ > sim:
            mejor, sim = h["id"], s_
    return mejor if sim >= 0.5 else None


def _videos_canal():
    out = []
    for f in sorted((ROOT / "videos").glob("*/video.json")):
        try:
            out.append({"slug": f.parent.name, "titulo": json.loads(f.read_text()).get("titulo", "")})
        except (OSError, json.JSONDecodeError):
            continue
    return out


# ---------------------------------------------------------------- barrido

def _consulta_noticias(c, freshness):
    args = ["news", c["q"], "--freshness", freshness, "--count", str(c.get("count", 20))]
    for s in c.get("sitios", []):
        args += ["--include-site", s]
    if c.get("idioma") == "es":
        args += ["--search-lang", "es", "--country", "MX"]
    data = _bx(args)
    if "_error" in data:
        return c, [], data["_error"]
    items = []
    for r in data.get("results", []):
        items.append({
            "titulo": r.get("title", ""), "url": r.get("url", ""),
            "medio": (r.get("profile") or {}).get("name") or (r.get("meta_url") or {}).get("hostname", ""),
            "descripcion": re.sub(r"<[^>]+>", "", r.get("description", ""))[:280],
            "horas": _horas(r.get("page_age"), r.get("age")), "vertical": c["vertical"], "tipo": "noticia",
        })
    return c, items, None


def _consulta_comunidad(c, freshness):
    data = _bx(["web", c["q"], "--result-filter", "discussions", "--freshness", freshness, "--count", "20"])
    if "_error" in data:
        return c, [], data["_error"]
    items = []
    for r in (data.get("discussions") or {}).get("results", []):
        d = r.get("data") or {}
        try:
            score = int(str(d.get("score", "0")).replace(",", ""))
        except ValueError:
            score = 0
        items.append({
            "titulo": d.get("title") or r.get("title", ""), "url": r.get("url", ""),
            "medio": d.get("forum_name", ""), "score": score, "comentarios": d.get("num_answers") or 0,
            "top_comment": (d.get("top_comment") or "")[:200],
            "horas": _horas(None, r.get("age")), "vertical": c["vertical"], "tipo": "comunidad",
        })
    return c, items, None


def _agrupar(items):
    """Agrupa notas sobre la misma historia: Dice ponderado por IDF entre titulares, enlace simple.
    Las palabras raras (nombres propios) pesan más que «trailer» o «marvel»."""
    toks = [_tokens(i["titulo"]) for i in items]
    n = len(items) or 1
    df = {}
    for t in toks:
        for w in t:
            df[w] = df.get(w, 0) + 1
    peso = lambda ws: sum(math.log(n / df[w]) for w in ws)
    orden = sorted(range(len(items)), key=lambda i: (items[i]["horas"] is None, items[i]["horas"] or 0))
    grupos = []
    for i in orden:
        mejor, sim = None, 0.0
        for g in grupos:
            s_ = max(2 * peso(toks[i] & toks[j]) / (peso(toks[i]) + peso(toks[j]) + 1e-9) for j in g)
            if s_ > sim:
                mejor, sim = g, s_
        if mejor is not None and sim >= 0.35:
            mejor.append(i)
        else:
            grupos.append([i])
    return [{"_tk": set().union(*(toks[j] for j in g)), "items": [items[j] for j in g]} for g in grupos]


def _temas_calientes(items, top=25):
    """Bigramas más repetidos en titulares de medios distintos: detecta la conversación aunque esté en dos idiomas."""
    cuenta = {}
    for it in items:
        ws = [w for w in _norm(it["titulo"]).split() if w not in STOP and len(w) > 1]
        for bg in {" ".join(ws[k:k + 2]) for k in range(len(ws) - 1)}:
            c = cuenta.setdefault(bg, {"notas": 0, "medios": set(), "score": 0})
            c["notas"] += 1
            c["medios"].add(it["medio"])
            c["score"] += it.get("score", 0)
    filas = [{"tema": k, "notas": v["notas"], "medios": len(v["medios"]), "reddit": v["score"]}
             for k, v in cuenta.items() if len(v["medios"]) >= 3]
    filas.sort(key=lambda f: (-f["medios"], -f["notas"]))
    return filas[:top]


GENERICAS = set("""box office trailer final official movie tv show series comic book weekend new game games
release date season episode teaser review first look cast netflix pelicula serie estreno lanza nuevo
oficial avance video studios""".split())


def _consultas_comunidad(cfg, temas, solo, max_temas=8):
    """Franquicias fijas de la config + los temas calientes del barrido (sin bigramas genéricos)."""
    qs = [c for c in cfg.get("comunidad", []) if not solo or c["vertical"] in solo]
    tope = len(qs) + max_temas
    ya = {_norm(c["q"]).strip() for c in qs}
    for t in temas:
        w1, w2 = t["tema"].split()
        if (w1 in GENERICAS and w2 in GENERICAS) or t["tema"] in ya or len(qs) >= tope:
            continue
        if any(t["tema"] in q or q in t["tema"] for q in ya):
            continue
        ya.add(t["tema"])
        qs.append({"vertical": "tema", "q": t["tema"]})
    return qs


def barrido(fecha=None, ventana="7d", solo=None):
    cfg = json.loads((RESEARCH / "radar.json").read_text())
    fresh = "pd" if ventana == "24h" else "pw"
    limite_h = {"24h": 30, "72h": 80, "7d": 180}[ventana]
    noticias = [c for c in cfg["noticias"] if not solo or c["vertical"] in solo]
    ruido = re.compile(cfg.get("ruido", "$^"), re.I)

    def correr(fn, consultas, fr):
        out, errs = [], []
        with ThreadPoolExecutor(max_workers=4) as ex:
            for c, its, err in ex.map(lambda c: fn(c, fr), consultas):
                if err:
                    errs.append({"consulta": c["q"], "error": err})
                out += its
        return out, errs

    def limpiar(items):
        vistos, out = set(), []
        for it in items:
            u = it["url"].split("?")[0].rstrip("/")
            if u in vistos or (it["horas"] is not None and it["horas"] > limite_h) or ruido.search(it["titulo"]):
                continue
            vistos.add(u)
            out.append(it)
        return out

    # 1) noticias
    notas, errores = correr(_consulta_noticias, noticias, fresh)
    notas = limpiar(notas)
    temas = _temas_calientes(notas)
    # 2) comunidad: franquicias + temas calientes (Brave solo trae hilos con consultas específicas)
    cons = _consultas_comunidad(cfg, temas, solo)
    hilos, e2 = correr(_consulta_comunidad, cons, "pw")
    errores += e2
    hilos = sorted(limpiar(hilos), key=lambda i: -i["score"])
    print(f"  {len(noticias)} consultas de noticias + {len(cons)} de comunidad · {len(notas)} notas, {len(hilos)} hilos · {len(errores)} errores")

    hist = _historial()
    vids = _videos_canal()
    grupos = _agrupar(notas)
    # cada hilo se pega a la historia con la que más palabras raras comparte (si comparte suficiente)
    for hl in hilos:
        tk = _tokens(hl["titulo"])
        g, sim = max(((g, _jaccard(tk, g["_tk"])) for g in grupos), key=lambda x: x[1], default=(None, 0))
        hl["historia"] = None
        if g is not None and sim >= 0.12 and len(tk & g["_tk"]) >= 2:
            g.setdefault("hilos", []).append(hl)
            hl["historia"] = id(g)
    historias = []
    for g in grupos:
        its, com = g["items"], g.get("hilos", [])
        medios = sorted({i["medio"] for i in its if i["medio"]})
        horas = [i["horas"] for i in its if i["horas"] is not None]
        tk = g["_tk"]
        vid = max(((v, _jaccard(tk, _tokens(v["titulo"]))) for v in vids), key=lambda x: x[1], default=(None, 0))
        historias.append({
            "titular": its[0]["titulo"],
            "verticales": sorted({i["vertical"] for i in its}),
            "notas": len(its),
            "medios": medios,
            "comunidad": {"hilos": len(com), "score": sum(i["score"] for i in com),
                          "comentarios": sum(int(i["comentarios"] or 0) for i in com)},
            "mas_reciente_h": round(min(horas), 1) if horas else None,
            "mas_antigua_h": round(max(horas), 1) if horas else None,
            "ya_reportado": _ya_reportado(_tokens(its[0]["titulo"]), {_url_clave(i["url"]) for i in its}, hist),
            "video_relacionado": vid[0]["slug"] if vid[0] and vid[1] >= 0.25 else None,
            "items": its + com,
        })
    # Tracción bruta: medios distintos × frescura + comunidad. Solo ordena el barrido; no es el puntaje.
    for h in historias:
        r = h["mas_reciente_h"] if h["mas_reciente_h"] is not None else 999
        fres = 1.0 if r <= 24 else 0.6 if r <= 72 else 0.3
        h["traccion"] = round(len(h["medios"]) * 2 * fres + min(h["comunidad"]["score"], 20000) / 1000, 1)
    historias.sort(key=lambda h: -h["traccion"])
    for hl in hilos:
        hl.pop("historia", None)

    d = _dir(fecha)
    (d / "barrido.json").write_text(json.dumps({
        "fecha": d.name, "ventana": ventana, "generado": datetime.now().isoformat(timespec="minutes"),
        "errores": errores, "temas_calientes": temas, "consultas_comunidad": [c["q"] for c in cons],
        "comunidad": hilos, "historias": historias}, ensure_ascii=False, indent=1))
    _barrido_md(d, ventana, historias, errores, temas, hilos)
    print(f"  {len(historias)} historias → {d.relative_to(ROOT)}/barrido.md")


def _barrido_md(d, ventana, historias, errores, temas, hilos, top=60):
    L = [f"# Barrido {d.name} · ventana {ventana}", "",
         "Ordenado por tracción bruta (medios distintos × frescura + score de Reddit). Es una pista para elegir qué investigar, no el puntaje final.",
         "La misma historia puede salir dos veces (inglés y español): júntalas al investigar.", ""]
    if errores:
        L += ["**Consultas con error:** " + "; ".join(f"`{e['consulta']}` ({e['error'][:80]})" for e in errores), ""]
    L += ["## Temas calientes (bigramas en ≥3 medios)", "",
          " · ".join(f"**{t['tema']}** {t['medios']}m/{t['notas']}n" + (f"/r{t['reddit']}" if t["reddit"] else "") for t in temas), ""]
    L += ["## Comunidad: hilos con más score (Reddit y foros, 7 días)", ""]
    L += [f"- {h['score']} pts · {h['comentarios']} com · {h['medio']} · {h['horas']:.0f} h · {h['titulo'][:120]} {h['url']}"
          for h in hilos[:25] if h["horas"] is not None] or ["- (sin hilos: Brave no devolvió discusiones)"]
    L += ["", f"## Historias (top {min(top, len(historias))} de {len(historias)}; el resto en barrido.json)", ""]
    for i, h in enumerate(historias[:top], 1):
        marcas = []
        if h["ya_reportado"]:
            marcas.append(f"ya en reporte: {h['ya_reportado']}")
        if h["video_relacionado"]:
            marcas.append(f"video del canal: {h['video_relacionado']}")
        c = h["comunidad"]
        L.append(f"### {i}. {h['titular']}")
        L.append(f"tracción {h['traccion']} · {', '.join(h['verticales'])} · {h['notas']} notas en {len(h['medios'])} medios"
                 + (f" · Reddit {c['hilos']} hilos, score {c['score']}, {c['comentarios']} comentarios" if c["hilos"] else "")
                 + (f" · hace {h['mas_reciente_h']} h" if h["mas_reciente_h"] is not None else "")
                 + (f" · **{'; '.join(marcas)}**" if marcas else ""))
        for it in h["items"][:4]:
            edad = f"{it['horas']:.0f} h" if it["horas"] is not None else "?"
            extra = f" · score {it['score']}" if it["tipo"] == "comunidad" else ""
            L.append(f"- [{it['medio']}] {it['titulo']} ({edad}{extra}) {it['url']}")
        if len(h["items"]) > 4:
            L.append(f"- … {len(h['items']) - 4} más en barrido.json")
        L.append("")
    (d / "barrido.md").write_text("\n".join(L))


# ---------------------------------------------------------------- YouTube

def _yt(q, n, semana=False):
    from urllib.parse import quote_plus
    # sp=EgIIAw%3D%3D: filtro «subidos esta semana» de la búsqueda de YouTube
    src = (f"https://www.youtube.com/results?search_query={quote_plus(q)}&sp=EgIIAw%253D%253D" if semana
           else f"ytsearch{n}:{q}")
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", str(n), src],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        return None
    return [{"titulo": e.get("title"), "canal": e.get("channel"), "vistas": e.get("view_count"),
             "duracion": e.get("duration"), "url": e.get("url")}
            for e in (json.loads(r.stdout).get("entries") or []) if e][:n]


_ES = re.compile(r"[¿¡ñáéíóú]|\b(el|la|los|las|que|qué|por|para|del|una|cómo|como|ahora|esto|pelicula|película)\b", re.I)


def _resumen_yt(vids):
    """Resumen de una búsqueda. Las vistas pueden faltar (YouTube no siempre las da en el listado): cuentan como n/d, no como 0."""
    con = sorted((v["vistas"] for v in vids if v["vistas"] is not None), reverse=True)
    return {"resultados": len(vids),
            "en_espanol": sum(1 for v in vids if _ES.search(v["titulo"] or "")),
            "shorts": sum(1 for v in vids if "/shorts/" in (v["url"] or "") or 0 < (v["duracion"] or 0) <= 60),
            "sin_vistas": len(vids) - len(con), "vistas_top3": con[:3],
            "con_100k": sum(1 for x in con if x >= 100_000),
            "canales": sorted({v["canal"] for v in vids if v["canal"]})[:12], "videos": vids[:8]}


def youtube(consultas, fecha=None, n=20):
    """Qué existe ya en YouTube para cada consulta, en dos cortes:
    - historico: relevancia de siempre (demanda acumulada del tema; incluye videos viejos);
    - semana: subidos en los últimos 7 días (la competencia real por la noticia → dimensión 'mercado')."""
    trabajos = [(q, sem) for q in consultas for sem in (False, True)]
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = dict(zip(trabajos, ex.map(lambda t: _yt(t[0], n, t[1]), trabajos)))
    out = {}
    for q in consultas:
        h, w = res[(q, False)], res[(q, True)]
        out[q] = {"historico": _resumen_yt(h) if h is not None else {"error": "yt-dlp falló"},
                  "semana": _resumen_yt(w) if w is not None else {"error": "yt-dlp falló"}}
        hh, ww = out[q]["historico"], out[q]["semana"]
        print(f"  «{q}»: histórico top {hh.get('vistas_top3')} ({hh.get('con_100k')} con 100k+) · "
              f"esta semana {ww.get('resultados')} videos ({ww.get('en_espanol')} en español), "
              f"{ww.get('con_100k')} con 100k+, top {ww.get('vistas_top3')}, {ww.get('sin_vistas')} sin dato de vistas")
    d = _dir(fecha)
    f = d / "youtube.json"
    prev = json.loads(f.read_text()) if f.exists() else {}
    prev.update(out)
    f.write_text(json.dumps(prev, ensure_ascii=False, indent=1))
    print(f"  → {f.relative_to(ROOT)}")


# ---------------------------------------------------------------- reporte

def puntaje(dims):
    return round(sum(float(dims[k]) * p for k, p in PESOS.items()) / 10)


def _validar(rep):
    errs = []
    ids = set()
    for h in rep.get("historias", []):
        hid = h.get("id", "?")
        ids.add(hid)
        if h.get("clasificacion") not in CLASIFICACION:
            errs.append(f"{hid}: clasificacion debe ser una de {list(CLASIFICACION)}")
        if h.get("urgencia") not in URGENCIA:
            errs.append(f"{hid}: urgencia debe ser una de {list(URGENCIA)}")
        dims = h.get("dimensiones", {})
        for k in PESOS:
            v = dims.get(k)
            if not isinstance(v, (int, float)) or not 0 <= v <= 10:
                errs.append(f"{hid}: dimensiones.{k} debe ser 0-10")
        if not 0 <= int(h.get("confianza", -1)) <= 100:
            errs.append(f"{hid}: confianza 0-100")
        ev = h.get("evidencia", [])
        if not ev or not all(str(e.get("url", "")).startswith("http") for e in ev):
            errs.append(f"{hid}: cada historia necesita evidencia con URL")
        # CONFIRMADO = fuente oficial o dos medios serios independientes (base/plantillas/fuentes.md)
        secundarias = {_norm(e.get("fuente", "")).split()[0] for e in ev if e.get("tipo") != "primaria" and e.get("fuente")}
        if h.get("clasificacion") == "CONFIRMADO" and not any(e.get("tipo") == "primaria" for e in ev) and len(secundarias) < 2:
            errs.append(f"{hid}: CONFIRMADO necesita una fuente primaria o dos medios independientes (o cambia a REPORTADO)")
        if len(h.get("contenido", {}).get("titulos", [])) < 3:
            errs.append(f"{hid}: faltan 3 títulos")
    for k, r in (rep.get("recomendaciones") or {}).items():
        if r and r.get("id") not in ids:
            errs.append(f"recomendaciones.{k}: id «{r.get('id')}» no está en historias")
    return errs


def reporte(fecha=None):
    d = _dir(fecha)
    f = d / "reporte.json"
    if not f.exists():
        die(f"falta {f.relative_to(ROOT)} (lo escribe el agente; formato en skills/radar/SKILL.md)")
    rep = json.loads(f.read_text())
    errs = _validar(rep)
    if errs:
        die("reporte.json no pasa la validación:\n  " + "\n  ".join(errs))
    for h in rep["historias"]:
        h["puntaje"] = puntaje(h["dimensiones"])
        h["sello"] = CLASIFICACION[h["clasificacion"]][0]
    rep["historias"].sort(key=lambda h: -h["puntaje"])
    f.write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    (d / "reporte.md").write_text(_reporte_md(rep))

    hist = [x for x in _historial() if x["id"] not in {h["id"] for h in rep["historias"]}]
    for h in rep["historias"]:
        e = {"id": h["id"], "titular": h["titular"], "franquicia": h.get("franquicia", ""), "fecha": rep["fecha"],
             "puntaje": h["puntaje"], "clasificacion": h["clasificacion"], "urls": [x["url"] for x in h["evidencia"]][:8]}
        e["claves"] = _claves(e)
        hist.append(e)
    HISTORIAL.write_text(json.dumps(hist, ensure_ascii=False, indent=1))
    _watchlist(rep)
    for h in rep["historias"]:
        print(f"  {h['puntaje']:>3}  {h['urgencia']:<10} {h['sello']:<11} {h['titular']}")
    print(f"  → {(d / 'reporte.md').relative_to(ROOT)} · historial {len(hist)} · {WATCHLIST.relative_to(ROOT)}")


def _reporte_md(rep):
    H = {h["id"]: h for h in rep["historias"]}
    L = [f"# Radar · {rep['fecha']}", "",
         f"**Ventana:** {rep.get('ventana', '7d')} · **Historias:** {len(H)}", "",
         "## Resumen", "", rep.get("resumen", ""), ""]
    nombres = {"publicar_ya": "Publicar ya", "largo": "Mejor largo", "short": "Mejor Short",
               "vigilar": "Historia a vigilar", "evergreen": "Evergreen conectado a la actualidad"}
    L += ["## Recomendaciones", ""]
    for k, n in nombres.items():
        r = (rep.get("recomendaciones") or {}).get(k)
        if r:
            L.append(f"- **{n}:** {H[r['id']]['titular']} ({H[r['id']]['puntaje']}/100). {r.get('porque', '')}")
    L += ["", "## Ranking", "", "| # | Historia | Puntaje | Urgencia | Sello | Confianza |", "|---|---|---|---|---|---|"]
    for i, h in enumerate(rep["historias"], 1):
        L.append(f"| {i} | {h['titular']} | {h['puntaje']} | {h['urgencia']} ({URGENCIA[h['urgencia']]}) | {h['sello']} | {h['confianza']} |")
    L.append("")
    for h in rep["historias"]:
        hz, c, dm = h.get("hallazgos", {}), h.get("contenido", {}), h["dimensiones"]
        L += [f"## {h['titular']}", "",
              f"- **Categoría:** {h.get('categoria', '')} · **Franquicia:** {h.get('franquicia', '')} · **Publicado:** {h.get('fecha_original', '')}",
              f"- **Clasificación:** {h['clasificacion']} → sello **{h['sello']}** · confianza {h['confianza']}/100: {h.get('confianza_razon', '')}",
              f"- **Puntaje:** {h['puntaje']}/100" + (" (cualitativo: sin datos medidos de demanda)" if h.get("cualitativo") else "")
              + " · " + ", ".join(f"{k} {v}" for k, v in dm.items()),
              f"- **Urgencia:** {h['urgencia']} ({URGENCIA[h['urgencia']]}): {h.get('urgencia_razon', '')}"]
        if h.get("spoiler"):
            L.append("- ⚠️ **Spoilers**")
        if h.get("senales"):
            L.append("- **Señales:** " + " · ".join(h["senales"]))
        L += ["", "### Hallazgos", ""]
        for k, n in [("que_paso", "Qué pasó"), ("que_es_nuevo", "Qué es nuevo"), ("por_que_importa", "Por qué importa"),
                     ("contexto", "Contexto"), ("reaccion", "Reacción del público"), ("interes_creciente", "¿Interés creciente?")]:
            if hz.get(k):
                L.append(f"- **{n}:** {hz[k]}")
        for k, n in [("confirmado", "Confirmado"), ("incierto", "Incierto")]:
            if hz.get(k):
                L.append(f"- **{n}:** " + "; ".join(hz[k]))
        L += ["", "### Contenido", ""]
        L += [f"- Título: {t}" for t in c.get("titulos", [])]
        for k, n in [("angulo", "Ángulo"), ("hook", "Hook"), ("formato", "Formato"), ("duracion", "Duración"), ("miniatura", "Miniatura")]:
            if c.get(k):
                L.append(f"- **{n}:** {c[k]}")
        if c.get("puntos"):
            L.append("- **Puntos:** " + " → ".join(c["puntos"]))
        if c.get("seguimiento"):
            L.append("- **Seguimiento:** " + "; ".join(c["seguimiento"]))
        L += ["", "### Evidencia", ""]
        for e in h["evidencia"]:
            L.append(f"- {e.get('fuente', '')}{' · ' + e['autor'] if e.get('autor') else ''} · {e.get('fecha', '')} · {e.get('tipo', '')} · {e.get('respalda', '')} · {e['url']}")
        L.append("")
    if rep.get("descartadas"):
        L += ["## Descartadas", ""] + [f"- {x['titular']}: {x['razon']}" for x in rep["descartadas"]] + [""]
    if rep.get("watchlist"):
        L += ["## Watchlist", ""] + [f"- {w.get('fecha') or 's/f'} · {w.get('tipo', '')} · {w['item']}" + (f": {w['nota']}" if w.get("nota") else "") for w in rep["watchlist"]] + [""]
    if rep.get("limites"):
        L += ["## Límites de este reporte", ""] + [f"- {x}" for x in rep["limites"]] + [""]
    return "\n".join(L)


def _watchlist(rep):
    """research/watchlist.md: una línea por pendiente, fusionando por texto; se quitan las fechas ya pasadas hace >7 días."""
    items = {}
    if WATCHLIST.exists():
        for ln in WATCHLIST.read_text().splitlines():
            m = re.match(r"- \[(.*?)\] \((.*?)\) (.*?)(?: — (.*))?$", ln)
            if m:
                items[_norm(m.group(3)).strip()] = {"fecha": m.group(1), "tipo": m.group(2), "item": m.group(3), "nota": m.group(4) or ""}
    for w in rep.get("watchlist", []):
        items[_norm(w["item"]).strip()] = {"fecha": w.get("fecha") or "s/f", "tipo": w.get("tipo", ""),
                                            "item": w["item"], "nota": w.get("nota", "") + f" (radar {rep['fecha']})"}
    corte = (date.today() - timedelta(days=7)).isoformat()
    vivos = [v for v in items.values() if v["fecha"] == "s/f" or v["fecha"] >= corte]
    vivos.sort(key=lambda v: (v["fecha"] == "s/f", v["fecha"]))
    L = ["# Watchlist del radar", "",
         "Rumores sin resolver, anuncios, eventos y estrenos a revisar en el próximo barrido. La actualiza `./tl radar reporte`; puedes editarla a mano.", ""]
    L += [f"- [{v['fecha']}] ({v['tipo']}) {v['item']}" + (f" — {v['nota']}" if v["nota"] else "") for v in vivos]
    WATCHLIST.write_text("\n".join(L) + "\n")


def main(a):
    if a.accion == "barrido":
        barrido(a.fecha, a.ventana, a.vertical)
    elif a.accion == "youtube":
        if not a.consultas:
            sys.exit("uso: ./tl radar youtube \"consulta 1\" \"consulta 2\" …")
        youtube(a.consultas, a.fecha, a.n)
    elif a.accion == "reporte":
        reporte(a.fecha)
