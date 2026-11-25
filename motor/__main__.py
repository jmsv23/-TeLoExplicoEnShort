"""CLI del canal: ./tl <comando> ...   (./tl -h para la lista; cada comando acepta -h)

<video> acepta el slug completo (2026-11-james-bond-pattinson), sin fecha (james-bond-pattinson) o un fragmento único.
[piezas]: largo | short-01 | short-01,short-02 | shorts | (vacío = todas)
"""
import argparse
import sys

from . import assets as A
from . import flujo as F
from . import miniaturas as M
from . import voces as VO
from .proyecto import Video, die


def main():
    ap = argparse.ArgumentParser(prog="tl", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    def cmd(nombre, ayuda, video=True, piezas=False):
        p = sp.add_parser(nombre, help=ayuda)
        if video:
            p.add_argument("video")
        if piezas:
            p.add_argument("piezas", nargs="?")
        return p

    p = sp.add_parser("nuevo", help="crea videos/AAAA-MM-<slug>/ con su esqueleto")
    p.add_argument("slug")
    p.add_argument("--titulo", required=True)
    p.add_argument("--formato", required=True, choices=list(F.FORMATOS))
    p.add_argument("--estilo", required=True)
    p.add_argument("--shorts", type=int, help="número de shorts (formatos de serie)")
    p.add_argument("--serie")
    p.add_argument("--voz")
    p = sp.add_parser("estado", help="tabla de videos y fases (con <video>: detalle por pieza)")
    p.add_argument("video", nargs="?")

    p = cmd("voz", "Voicebox + alineación + master (+ timeline)", piezas=True)
    p.add_argument("--force", action="store_true", help="regenera aunque el texto no haya cambiado")
    p.add_argument("--solo", choices=["audio", "words", "master"])
    cmd("build", "genera el proyecto HyperFrames de la pieza (sin renderizar)", piezas=True)
    p = cmd("render", "build + render + mezcla → build/render/<pieza>-final.mp4", piezas=True)
    p.add_argument("--draft", action="store_true")
    p.add_argument("--workers", type=int)
    p = cmd("hoja", "hoja de contacto a 1 fps del render final → build/revision/", piezas=True)
    p.add_argument("--cada", type=float, default=1.0)
    p = cmd("miniaturas", "renderiza miniaturas.json → entrega/*.png")
    p.add_argument("ids", nargs="*")
    cmd("qa", "gate de calidad (duración, loudness, lint, publicación, miniaturas, hojas 1 fps)", piezas=True)
    p = cmd("entrega", "QA + copia los finales a entrega/")
    p.add_argument("--forzar", action="store_true")
    p = cmd("publicado", "registra la URL de YouTube de una pieza")
    p.add_argument("pieza")
    p.add_argument("url")
    p = sp.add_parser("limpiar", help="borra lo regenerable de videos publicados (muestra cuánto libera; --si para borrar)")
    p.add_argument("videos", nargs="*")
    p.add_argument("--todos-publicados", action="store_true")
    p.add_argument("--si", action="store_true")
    p.add_argument("--forzar", action="store_true", help="aunque no esté publicado")
    p = cmd("regenerar", "reconstruye lo regenerable (assets, voz, render, miniaturas)", piezas=True)
    p.add_argument("--draft", action="store_true")

    p = sp.add_parser("assets", help="fetch | cortar | agregar-img | verificar | respaldar | hoja")
    p.add_argument("accion", choices=["fetch", "cortar", "agregar-img", "verificar", "respaldar", "hoja"])
    p.add_argument("video")
    p.add_argument("args", nargs="*", help="cortar: ids · agregar-img: <id> <url> · hoja: <fuente>")
    p.add_argument("--pagina")
    p.add_argument("--fuente")
    p.add_argument("--pin", action="store_true")
    p.add_argument("--force", action="store_true")

    p = sp.add_parser("preview", help="renderiza el preview de 10-15 s de un estilo (gate de nuevo-estilo)")
    p.add_argument("estilo")
    p.add_argument("--final", action="store_true", help="calidad final en vez de draft")
    p = sp.add_parser("planos", help="catálogo de planos, entradas y SFX de un estilo")
    p.add_argument("estilo")
    p = sp.add_parser("voces", help="listar | respaldar <slug> <nombre en Voicebox> | restaurar <slug>")
    p.add_argument("accion", choices=["listar", "respaldar", "restaurar"])
    p.add_argument("args", nargs="*")
    p = sp.add_parser("radar", help="barrido | youtube <consultas…> | reporte  (research/radar/<fecha>/)")
    p.add_argument("accion", choices=["barrido", "youtube", "reporte"])
    p.add_argument("consultas", nargs="*", help="youtube: consultas a buscar")
    p.add_argument("--fecha", help="carpeta research/radar/<fecha> (default: hoy)")
    p.add_argument("--ventana", choices=["24h", "72h", "7d"], default="7d", help="barrido: antigüedad máxima")
    p.add_argument("--vertical", nargs="*", help="barrido: solo cine | tv | comics | videojuegos | es")
    p.add_argument("-n", type=int, default=20, help="youtube: resultados por consulta")

    a = ap.parse_args()
    c = a.cmd
    if c == "nuevo":
        F.nuevo(a.slug, a.titulo, a.formato, a.estilo, a.shorts, a.serie, a.voz)
    elif c == "estado":
        F.estado(a.video)
    elif c == "voz":
        from .voz import cmd_audio, cmd_master, cmd_words
        v = Video(a.video)
        for p_ in v.seleccion(a.piezas):
            if a.solo in (None, "audio"):
                cmd_audio(v, p_, a.force)
            if a.solo in (None, "words"):
                cmd_words(v, p_, a.force)
            if a.solo in (None, "master"):
                cmd_master(v, p_)
            v.marcar("voz", "hecho", p_)
    elif c == "build":
        from .build import build
        v = Video(a.video)
        for p_ in v.seleccion(a.piezas):
            build(v, p_)
    elif c == "render":
        from .render import render
        v = Video(a.video)
        for p_ in v.seleccion(a.piezas):
            render(v, p_, a.workers, a.draft)
            if not a.draft:
                v.marcar("montaje", "hecho", p_)
    elif c == "hoja":
        from .render import hoja
        v = Video(a.video)
        for p_ in v.seleccion(a.piezas):
            f = v.build / "render" / f"{p_}-final.mp4"
            if not f.exists():  # sin render final: revisa el draft
                f = v.build / "render" / f"{p_}-final.draft.mp4"
            if not f.exists():
                die(f"{p_}: no hay render (./tl render {v.dir.name} {p_} --draft)")
            hoja(f, v.build / "revision" / f"{p_}.jpg", a.cada)
    elif c == "miniaturas":
        M.render(Video(a.video), a.ids or None)
    elif c == "qa":
        v = Video(a.video)
        err, _ = F.qa(v, v.seleccion(a.piezas))
        sys.exit(1 if err else 0)
    elif c == "entrega":
        F.entrega(Video(a.video), a.forzar)
    elif c == "publicado":
        F.publicado(Video(a.video), a.pieza, a.url)
    elif c == "limpiar":
        vids = F.videos_publicados() if a.todos_publicados else a.videos
        if not vids:
            sys.exit("no hay videos publicados (./tl publicado <video> <pieza> <url>)" if a.todos_publicados
                     else "indica videos o --todos-publicados")
        F.limpiar(vids, a.si, a.forzar)
    elif c == "regenerar":
        F.regenerar(Video(a.video), a.piezas, a.draft)
    elif c == "assets":
        v = Video(a.video)
        if a.accion == "fetch":
            A.fetch(v)
        elif a.accion == "cortar":
            A.cortar(v, a.args or None, a.force)
        elif a.accion == "agregar-img":
            if len(a.args) != 2:
                sys.exit("uso: ./tl assets agregar-img <video> <id> <url> [--pagina URL --fuente sitio --pin]")
            A.agregar_img(v, a.args[0], a.args[1], a.pagina, a.fuente, a.pin)
        elif a.accion == "verificar":
            A.verificar(v)
        elif a.accion == "respaldar":
            A.respaldar(v)
        elif a.accion == "hoja":
            A.hoja_fuente(v, a.args[0])
    elif c == "preview":
        from .preview import preview
        preview(a.estilo, not a.final)
    elif c == "planos":
        from .build import catalogo
        catalogo(a.estilo)
    elif c == "voces":
        if a.accion == "listar":
            VO.listar()
        elif a.accion == "respaldar":
            VO.respaldar(a.args[0], a.args[1])
        elif a.accion == "restaurar":
            VO.restaurar(a.args[0])
    elif c == "radar":
        from . import radar
        radar.main(a)


if __name__ == "__main__":
    main()
