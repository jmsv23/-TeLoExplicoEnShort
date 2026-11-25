"""CAPÍTULO 1 · EL FIN DE TODO."""
from esc_largo._k import SV, beat, capcard, tag


def build(S):
    capcard(S, 1, "EL FIN DE TODO", bg="rojo")
    beat(S, "se estaba muriendo", 261, txt="EL MULTIVERSO SE MUERE", tc="rojo")

    s = S.scene(S.w("empezaron a chocar"), bg="multi-osc", enter="ink")
    tag(s, "K", s.start + 0.05)
    s.svg("dt", SV + "dos-tierras.svg", 960, 520, 1800, 1012, s.start + 0.05, how="pop")
    t = S.w("incursión")
    s.code(f'tl.to(q("#{s.id("dt")} [id$=t616]"), {{ x: 220, duration: 0.6, ease: "power2.in" }}, {s.T(t - 0.4)});')
    s.code(f'tl.to(q("#{s.id("dt")} [id$=t1610]"), {{ x: -220, duration: 0.6, ease: "power2.in" }}, {s.T(t - 0.4)});')
    s.code(f'tl.to(q("#{s.id("dt")} [id$=choque]"), {{ opacity: 1, duration: 0.1 }}, {s.T(t + 0.2)});')
    s.shake("dt", t + 0.2, amp=16)
    s.sfx("explosion", t + 0.2, -4)
    t = S.w("mueren las dos")
    s.text("md", "…O MUEREN LAS DOS", "kw", "amarillo", 960, 980, t - 0.3, size=72, rot=-2)

    beat(S, "Durante años", 262, txt="LOS GENIOS FALLARON", tc="papel")
    beat(S, "solo quedan dos", 7, bg="tinta", txt="SOLO QUEDAN 2", tc="rojo", zoom=True)
    beat(S, "El nuestro", 8, txt="TIERRA-616 VS. TIERRA-1610")
    beat(S, "empieza la guerra", 265, fullscreen=True, ono="¡GUERRA!", sfx="explosion")
    beat(S, "construye una balsa", 259, txt="LA BALSA SALVAVIDAS", tc="papel")
    beat(S, "Reed Richards malvado", 9, bg="multi", txt="EL HACEDOR = REED MALVADO", tc="amarillo")
    beat(S, "Thanos", 83, bg="multi-osc", ono="THANOS", oc="multi")
    beat(S, "una masacre", 20, fullscreen=True, sfx="explosion")
    beat(S, "Cíclope", 30, 4, fullscreen=True, ono="¡FÉNIX!", oc="amarillo", sfx="riser")
    beat(S, "La balsa despega", 31, txt="LA BALSA DESPEGA", tc="papel")
    beat(S, "una grieta", 33, fullscreen=True, ono="¡CRACK!", sfx="rumble")
    beat(S, "Sue Storm", 34, txt="SUE · LA COSA · LOS NIÑOS", tc="rojo")
    beat(S, "Reed lo ve todo", 36, fullscreen=True, kscale=1.15)

    s = S.scene(S.w("Las dos Tierras se tocan"), bg="tinta", enter="cut")
    s.text("st", "LAS DOS TIERRAS SE TOCAN", "kw", "amarillo", 960, 540, s.start + 0.05, size=96, rot=-3, out=S.peek("se acaba") - 0.1)
    s.flash(s.start + 0.6)
    s.sfx("explosion", s.start + 0.6, -2)
    t = S.w("se acaba")
    s.text("fm", "FIN DEL MULTIVERSO", "ttl", "papel", 960, 540, t + 0.2, size=150, rot=-2)
