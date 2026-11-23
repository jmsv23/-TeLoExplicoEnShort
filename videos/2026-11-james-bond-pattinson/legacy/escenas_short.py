"""Dirección visual del Short (1080×1920). Cortes cada 1.5–3 s; misma estética Esmoquin."""


def short(S):
    w = S.w
    S.add("foto", w("Tenemos nuevo"), "corte", img="pattinson-007-primera-imagen", bn=False, kb="in", pos="62% 40%",
          kick="OFICIAL · 16 NOV 2026", l1="TENEMOS NUEVO", l2="JAMES BOND", t1=w("Tenemos nuevo"), t2=w("James Bond"), fs2=118)
    S.add("foto", w("y medio internet"), "latigo", img="pattinson-retrato", kb="r", pos="60% 30%",
          sello="¿LO ODIAN?", tsello=w("ya lo odia"), fsello=72)
    S.add("foto", w("Robert Pattinson"), "corte", img="pattinson-retrato", kb="in", pos="65% 30%",
          l2="PATTINSON", t2=w("Robert Pattinson") + 0.2, fs2=140)
    S.add("foto", w("Edward"), "corte", img="pattinson-crepusculo", kb="l", pos="40% 30%", kick="CREPÚSCULO · 2008")
    S.add("foto", w("Batman"), "corte", img="pattinson-batman", kb="r", pos="50% 30%", kick="THE BATMAN · 2022")
    S.add("foto", w("Y ahora"), "zoom", img="pattinson-007-logo", bn=False, kb="in", pos="68% 40%",
          l2="007", t2=w("cero cero siete"), fs2=230)
    S.add("comentarios", w("Unos dicen"), "barrido", img="pattinson-retrato", mw=780, fs=48,
          items=[("“El mejor actor de su generación”", "+", w("el mejor actor"), 100, 520),
                 ("“Ese no es Bond”", "-", w("ese no es Bond"), 150, 1000)])
    S.add("titulo", w("Pero espera"), "zoom", kick="PERO ESPERA", l1="ESTO", l2="YA PASÓ", t1=w("Esto ya pasó"),
          t2=w("ya pasó"), fs1=150, fs2=190)
    S.add("cita", w("A Sean Connery"), "latigo", img="connery-goldfinger-db5", texto="Un doble de acción con demasiado músculo.",
          autor="IAN FLEMING, SOBRE CONNERY", tq=w("un doble de acción"), ta=w("demasiado músculo"), fs=92, gap=0.09)
    S.add("dato", w("A Roger Moore"), "latigo", img="moore-silla-007", num="45", kick="MOORE · ¿MUY VIEJO?",
          label="años al debutar", tn=w("cuarenta y cinco"), tl=w("cuarenta y cinco") + 0.3, fsl=48)
    S.add("foto", w("A Daniel Craig"), "latigo", img="craig-2005-chaleco", kb="up", pos="50% 25%",
          kick="DANIEL CRAIG · 2005", l2="JAMES BLONDE", t2=w("James Blonde"), fs2=120)
    S.add("navegador", w("hicieron páginas web"), "zoom", img="craig-casino-esmoquin", titulo="PÁGINAS DE PROTESTA",
          urls=[("danielcraigisnotbond.com", w("páginas web")), ("craignotbond.com", w("sacarlo del papel"))])
    S.add("foto", w("Y qué pasó"), "zoom", video="craig-grua", bn=False, kb="in", kick="¿Y QUÉ PASÓ?")
    S.add("dato", w("Skyfall"), "corte", img="craig-skyfall-londres", pre="$", num="1,108", suf=" M", cuenta=False,
          kick="SKYFALL · 2012", label="la más taquillera de la saga", tn=w("Skyfall") + 0.25, tl=w("la más taquillera"), fs=160, fsl=40, tk=w("Skyfall"))
    S.add("foto", w("Y Pattinson ya vivió"), "latigo", img="pattinson-batman", kb="in", pos="50% 30%",
          kick="2019 · THE BATMAN", sello="PETICIÓN", tsello=w("pidieron"), fsello=72)
    S.add("escala", w("Así que te pregunto"), "iris", img="pattinson-007-logo", pos="68% 40%",
          pregunta="¿Pattinson llenará los zapatos de 007?", tq=w("te pregunto"), tn=w("del uno al diez"), fs=76)
    S.add("titulo", w("La historia completa"), "zoom", kick="VIDEO COMPLETO EN EL CANAL", l1="LOS SEIS", l2="EXPEDIENTES",
          t1=w("los seis"), t2=w("seis Bond") + 0.3, fs1=120, fs2=88)
