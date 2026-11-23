def prueba(S):
    w = S.w
    S.add("titulo", w("Seis actores"), "corte", kick="PREVIEW · ESMOQUIN", l1="SEIS ACTORES", l2="UN NOMBRE",
          t1=w("Seis actores"), t2=w("Un solo nombre"))
    S.add("foto", w("Y a todos"), "iris", img="connery-goldfinger-db5", kb="in", kick="1962", sello="ODIADOS",
          tsello=w("odiaron"))
    S.add("dato", w("Skyfall"), "latigo", img="craig-skyfall-londres", pre="$", num="1,108", suf=" M", cuenta=False,
          kick="SKYFALL · 2012 · CONFIRMADO", label="la más taquillera", tn=w("mil ciento ocho"), tl=w("la más taquillera"))
    S.add("foto", w("El próximo"), "zoom", img="pattinson-retrato", bn=False, kb="in", l2="¿A LA ALTURA?", t2=w("a la altura"))
