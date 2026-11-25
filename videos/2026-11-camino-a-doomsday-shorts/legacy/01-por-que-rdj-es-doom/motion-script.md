# Motion script · 01 · ¿Por qué Robert Downey Jr. es Doctor Doom?

- **Guion**: `guion-tts.md` (133 palabras, 51.9 s medidos con la voz "narrador comics")
- **Estilo**: `../_estilo.md` (reemplaza `_base/estilo-visual.md`). Cómic que se mueve, Ben-Day, viñetas, onomatopeyas, cortes ≤ 1.2 s, nada quieto > 0.4 s. **Sin Moni.**
- **Analogía visual central**: **"el jugador"**, una silueta de futbolista sin cara (óvalo liso `papel` con contorno `tinta`) que lleva una camiseta. Camiseta azul `heroe` con una "A" = Avengers. Camiseta verde `doom` con una "D" = Doom. Misma cabeza, otra camiseta. Sale en E6 (cambia de camiseta) y regresa **terminado** en E9 (camiseta verde, el balón entra a la portería azul).
- **Objetos/personajes** (todos dibujados en tinta, ver `OBJ` en `comic-objects.js`): portada de cómic, silueta de Kang (corona/casco, `multi`), X roja, casco de Iron Man (rojo/dorado, solo el casco), máscara de Doom + capucha + capa verde, corona, castillo de Latveria, engranaje+átomo, runas/pentagrama, cómic abierto, emblema "4", jugador + camisetas, contrato "FICHAJE", balón, portería, cámara de cine + claqueta, silla de director, reactor de arco (círculo `ciencia`), pantalla de cine, calendario, portada "N.º 02".
- **Fotos** (solo recorte pequeño, trama de puntos, marco de viñeta, ≤ 2 s): una foto de RDJ en 2.3 y el logo de Endgame en 7.4 (`assets/`).
- **Paleta del video**: `multi` (Kang) → `papel` (reemplazo) → `doom` (revela) → `heroe` (los 4) → `papel`/`rojo` (no es Tony) → `papel` (analogía) → `ciencia`/`ceniza` (Russo) → negro/`ciencia` (giro) → `doom` (cara) → `papel` (payback) → `doom`/`rojo` (fecha) → `papel` (CTA, eco de la portada).
- **Fijos en todo el video**: contador `FALTAN 36 DÍAS` (placa arriba a la derecha, aparece en 2.1, `PULSE` en 10.3); marca "explicando" pequeña abajo; grano de impresión 4 %.
- **Caja del narrador** (amarilla, esquina cortada, `CAPTION-DROP`, 3–6 palabras, se mueve de esquina en cada escena): texto en cada beat donde la columna Visual dice `CAP "…"`.
- **Idea de loop**: el último frame (portada "N.º 02") repite la composición del primero (portada "N.º 01": logo arriba, número, silueta al centro, precio GRATIS).
- **Fecha de cálculo del contador**: 12 nov 2026 → 36 días (se recalcula al publicar).

---

## Escena 1 · Portada · S1 · 0.0–3.5s
Fondo: `multi` con trama Ben-Day al 15 %. Portada de cómic a pantalla casi completa (marco `tinta` 10 px).

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 1.1 | 0.0 | — (primer frame) | Portada: logo "CAMINO A DOOMSDAY" arriba (Anton, `amarillo`), cuadro "N.º 01 DE 11", "GRATIS" en circulito rojo, silueta de Kang (`multi` oscuro, corona) al centro. Cinta diagonal `rojo` "MARVEL CAMBIÓ A KANG POR TONY" | Portada `PANEL-SLAM` en el frame 1; cinta `STAMP` en el frame 3; silueta `IDLE-BOB`; trama en movimiento | slam |
| 1.2 | 0.5 | "Marvel **despidió** a Kang…" | X roja gigante tacha la silueta de Kang; `ONOMATO` "¡FUERA!" (`rojo`, pegatina `papel`) | X `STAMP`; Kang `SHAKE`; `ONOMATO` + `SPEED-LINES` | bam |
| 1.3 | 1.1 | "…a **Kang**," | Cinta `multi` "KANG" cruza en diagonal; `CAP "EL VILLANO DEL MULTIVERSO"` | Cinta `SLIDE-IN-L` rápida; `CAPTION-DROP` | whoosh |
| 1.4 | 2.0 | "…su gran **villano**…" | La silueta de Kang se agrieta y se rompe en 6 pedazos de tinta que caen | Grietas `DRAW-ON` 0.2 s; pedazos `DROP-OUT` con rotación | glass-crack |

**Transición →** `HALFTONE-WIPE` en `papel` (0.35 s) desde el centro, `whoosh`.

## Escena 2 · El reemplazo · S1 · 3.5–8.9s
Fondo: `papel` con trama. Contador `FALTAN 36 DÍAS` entra arriba a la derecha.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 2.1 | 3.8 | "Y lo **reemplazó** con…" | `PANEL-SPLIT` en dos: izquierda viñeta vacía con huella de Kang; derecha viñeta `ceniza` con silueta gris y "?" enorme. Contador entra | 2 `PANEL-SLAM` (izq. y der., 0.08 s de diferencia) | slam |
| 2.2 | 4.7 | "…con **Robert** Downey…" | Cinta `rojo` con "ROBERT DOWNEY JR." (Anton, 2 renglones, `papel` con contorno `tinta`) sobre la viñeta derecha | `WORD-POP` por palabra (Robert, Downey, Junior) | pop ×3 |
| 2.3 | 5.4 | "…**Junior.**" | Foto pequeña de RDJ recortada (marco de viñeta inclinado 4°, trama de puntos) sale del "?" y se queda 1.6 s. `CAP "EL ACTOR"` | Foto `PANEL-SLAM` pequeña, `MISREG`; sale con `POP-OUT` en 2.4 | ding |
| 2.4 | 6.1 | "**Pero** ojo:" | Corte duro. `ONOMATO` "¡PERO OJO!" (Bangers `amarillo`) sobre fondo `rojo` (golpe ≤ 1.5 s) con líneas de velocidad | `ZOOM-GOLPE`; `SPEED-LINES`; texto `SHAKE` | record-scratch |
| 2.5 | 7.8 | "…no vuelve como **Iron** Man." | Casco de Iron Man (rojo/dorado, 480 px) en viñeta `papel` inclinada; aparece con brillo de ojos `ciencia` | Casco `PANEL-SLAM` desde arriba; ojos `PULSE`; `IDLE-BOB` | whoosh |
| 2.6 | 8.4 | "…Iron **Man.**" | Círculo-tachado `rojo` (símbolo de prohibido) sobre el casco, texto "NO" | Símbolo `STAMP`; casco `SHAKE` | buzzer |

**Transición →** `INK-SPLASH` (mancha negra que llena la pantalla y revela `doom`), 0.3 s, `ink`.

## Escena 3 · Entra Doom · S2 · 9.0–14.9s
Fondo: `doom` verde con trama oscura; viñeta única en ángulo bajo.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 3.1 | 9.1 | "**Vuelve** como Victor von Doom." | Máscara de Doom + capucha verde oscuro + capa que ondea, en contrapicado, sube desde abajo hasta ocupar el cuadro; ojos de la máscara se encienden | Doom `SLIDE-IN-B` con `back.out`; capa `WAVE`; `SPEED-LINES` hacia arriba | stinger |
| 3.2 | 9.8 | "…**Victor** von Doom." | Placa Anton "VICTOR VON DOOM" abajo: tres palabras que entran una por una | `WORD-POP` por palabra (Victor, von, Doom) | pop ×3 |
| 3.3 | 10.9 | "**Doctor Doom.**" | `ONOMATO` "¡DOCTOR DOOM!" Anton 220 px `amarillo` con contorno `tinta`, pegatina `papel`; la máscara retrocede | `ZOOM-GOLPE` en "Doom"; `MISREG`; `SHAKE` | bam |
| 3.4 | 12.0 | "**Rey** de Latveria," | `PANEL-SPLIT` en 3 viñetas verticales. Viñeta 1: corona + castillo de Latveria, cinta "REY DE LATVERIA" | `PANEL-SLAM` viñeta 1 | slam |
| 3.5 | 13.1 | "…**genio** científico…" | Viñeta 2 (fondo `ciencia`): engranaje + átomo, rótulo "GENIO CIENTÍFICO". `CAP "TECNOLOGÍA"` | `PANEL-SLAM` viñeta 2; engranaje gira | slam |
| 3.6 | 14.1 | "…y **hechicero.**" | Viñeta 3 (fondo `multi`): pentagrama/runas con brillo, mano abierta, rótulo "HECHICERO" | `PANEL-SLAM` viñeta 3; runas `PULSE` | zap |

**Transición →** `PAGE-FLIP` (la esquina se dobla y revela la página azul), 0.4 s, `page-flip`.

## Escena 4 · Su archienemigo · S2 · 14.9–18.4s
Fondo: `heroe` azul con trama.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 4.1 | 15.3 | "En los **cómics**," | Cómic abierto, grande; en sus dos páginas, a la izquierda la máscara de Doom (verde) y a la derecha el emblema "4" azul. `CAP "EN LOS CÓMICS"` | Cómic `PANEL-SLAM` girado 5°; páginas con `PAGE-FLIP` ligero | page-flip |
| 4.2 | 16.1 | "…es el **archienemigo** de…" | Corte a pantalla dividida diagonal: Doom (verde) a la izquierda, emblema "4" (azul) a la derecha, rayo rojo en medio. Cinta `rojo` "ARCHIENEMIGO" | `PANEL-SPLIT` diagonal; cinta `STAMP`; `SPEED-LINES` desde el centro | stinger |
| 4.3 | 17.0 | "…los **Cuatro Fantásticos.**" | El emblema "4" crece y rompe su viñeta; `ONOMATO` "¡BAM!" Rótulo "LOS 4 FANTÁSTICOS" | `PANEL-BREAK`; `ZOOM-GOLPE` en "Fantásticos" (17.3); `ONOMATO` | bam |

**Transición →** `HALFTONE-WIPE` en `papel` desde la derecha, 0.35 s.

## Escena 5 · No es Tony · S2 · 18.4–23.0s
Fondo: `papel` con trama; luego `rojo` 1.4 s en 5.3.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 5.1 | 18.5 | "No es **Tony** Stark…" | Casco de Iron Man (rojo/dorado) grande, centrado, con rótulo "TONY STARK" en Anton y X roja encima (STRIKE) | Casco `PANEL-SLAM`; X `STAMP` en "Stark" (19.1) | buzzer |
| 5.2 | 19.7 | "…con **armadura** nueva." | El casco se "transforma": MISREG y chasquido, aparece la máscara de Doom en su lugar con signo "?" grande. `CAP "¿ARMADURA NUEVA?"` | Casco→máscara con `MISREG` + `FLASH-BLANCO` 2 frames; "?" `POP-IN` | clank |
| 5.3 | 20.9 | "Es **otro personaje**" | `record-scratch`: la pantalla se divide en dos; izquierda casco, derecha máscara de Doom, y arriba de ambos la misma cabeza lisa (óvalo `papel`) que salta de uno a otro | `PANEL-SPLIT` vertical; cabeza `FLOW` de lado a lado; cinta `rojo` "OTRO PERSONAJE" | record-scratch |
| 5.4 | 21.9 | "…con el **mismo rostro.**" | La cabeza lisa se queda en el centro y un resaltador `amarillo` la rodea; texto "MISMO ROSTRO" con `STAMP` | `HIGHLIGHT` sobre la cabeza; `STAMP`; `ZOOM-GOLPE` suave | ding |

**Transición →** `PAGE-FLIP` a `papel` limpio (0.4 s).

## Escena 6 · La analogía: el futbolista fichado · S2 · 23.0–30.5s
Fondo: `papel` con líneas de campo muy sutiles. Objetos: el jugador, balón, portería, contrato, camisetas.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 6.1 | 23.4 | "**Piénsalo** como…" | Nube de pensamiento (con burbujas) arriba: "PIÉNSALO ASÍ". Fondo `papel` | Nube `POP-IN`; burbujas escalonadas | pop |
| 6.2 | 24.1 | "…un **futbolista**…" | El jugador (cabeza lisa, camiseta azul "A") entra de lado con un pase y patea el balón, 600 px, pose heroica de tres cuartos | `SLIDE-IN-L` con anticipación; balón `FLOW` en arco; `IDLE-BOB` | whoosh |
| 6.3 | 24.8 | "…**fichado** por…" | Contrato "FICHAJE" cae sobre el jugador y una pluma firma; sello `rojo` "¡FICHADO!" | Contrato `DROP-IN` + squash; firma `DRAW-ON`; sello `STAMP` | stamp |
| 6.4 | 25.5 | "…el **rival:**" | Escudo del equipo rival (verde "D") aparece a la derecha; flecha curva `doom` hacia él. `CAP "EL RIVAL"` | Escudo `PANEL-SLAM`; flecha `DRAW-ON` | slam |
| 6.5 | 26.3 | "**Misma cara,**" | Zoom a la cabeza lisa; aro `amarillo` + texto "MISMA CARA" | Aro `DRAW-ON`; texto `WORD-POP` por palabra; `ZOOM-GOLPE` | ding |
| 6.6 | 27.5 | "…otra **camiseta,**" | La camiseta azul "A" sale volando y la verde "D" se pone sobre el cuerpo del jugador (el jugador salta). `ONOMATO` "¡ZAP!" | `SWAP` de camisetas con arco; `ONOMATO`; `SQUASH` en el jugador | zap |
| 6.7 | 28.4 | "…**objetivos**" | Nueva composición: el jugador (camiseta verde) frente a la portería AZUL ("héroes"), el balón apuntando a ella; flecha roja punteada. | `SLIDE-IN-R`; flecha `DRAW-ON` | whoosh |
| 6.8 | 29.7 | "…totalmente **distintos.**" | Texto "OTRO OBJETIVO" en cinta `rojo`; la portería azul `SHAKE` | cinta `STAMP`; portería `SHAKE` | bam |

**Transición →** `HALFTONE-WIPE` en `ciencia` (0.35 s), `whoosh`.

## Escena 7 · Los hermanos Russo · S2 · 30.5–35.4s
Fondo: `ciencia` cian con trama; la marca "detrás de cámaras" tipo etiqueta.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 7.1 | 31.2 | "Y detrás de **cámaras**" | Cámara de cine clásica dibujada con tinta, con claqueta: sale una claqueta que da el golpe. Cinta `amarillo` "DETRÁS DE CÁMARAS" | Cámara `PANEL-SLAM`; claqueta `SHAKE` con clap | clap |
| 7.2 | 32.0 | "…están los **hermanos**" | Dos sillas de director con cada una una silueta distinta (dos hermanos), una cámara a cada lado | Sillas `SLIDE-IN-L/R` con `back.out` | whoosh |
| 7.3 | 32.6 | "…**Russo,**" | Rótulo "RUSSO" Anton 240 px, `amarillo` con sombra dura | `ONOMATO`-estilo `STAMP`; `MISREG` | stamp |
| 7.4 | 33.4 | "…los mismos que dirigieron" | Viñeta pequeña con trama de puntos y el logo de Endgame; `CAP "LOS DE ENDGAME"` | Viñeta `PANEL-SLAM`; `ZOOM-GOLPE` suave en "Endgame" (34.4) | ding |

> Silencio visual de 0.5 s antes del giro (34.8–35.3). La música (cuando se agregue) se corta.

## Escena 8 · El giro · S3 · 35.5–42.7s
Fondo: negro `tinta` con trama; luego `heroe`; luego `doom`.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 8.1 | 35.6 | "**Tony** Stark se sacrificó…" | `FLASH-BLANCO` y luego fondo `tinta`; un solo reactor de arco (círculo `ciencia` con anillos) latiendo al centro. `CAP "TONY STARK"` | `FLASH-BLANCO` 4 frames; reactor `PULSE` doble; `ZOOM-GOLPE` | heartbeat |
| 8.2 | 36.4 | "…se **sacrificó**…" | El reactor parpadea y se apaga (se pone `ceniza`); aparece onomatopeya pequeña "SNAP" | `FILL` a `ceniza`; `ONOMATO` | snap |
| 8.3 | 37.3 | "…para **salvar** el universo." | Luz `heroe` crece como explosión plana desde el reactor y llena la pantalla; estrellas. Rótulo "SALVÓ EL UNIVERSO" | Círculo `GROW` 0→2.5; `SPEED-LINES` radiales | zap |
| 8.4 | 38.7 | "**Ahora** su cara…" | `INK-SPLASH` verde (`doom`) | `INK-SPLASH` | ink |
| 8.5 | 39.2 | "…su **cara** será…" | La cabeza lisa (la misma de 5.4) aparece y la máscara de Doom cae encima: `ONOMATO` "¡KLANG!" | Máscara `DROP-IN` con squash; `CAM-PUNCH`; `SHAKE` | clank |
| 8.6 | 39.8 | "…la **peor** amenaza…" | Cinta `rojo` "LA PEOR AMENAZA" cruza; Doom se agranda, ojos encendidos | `SPEED-LINES`; cinta `SLIDE-IN-R`; Doom `GROW` | stinger |
| 8.7 | 41.8 | "…en **pantalla.**" | Marco de pantalla de cine (cortinas `rojo`) con la silueta de Doom enorme dentro | Cortinas se abren con `PANEL-SLAM`; Doom `SLIDE-IN-B` | whoosh |

**Transición →** `HALFTONE-WIPE` en `papel` (0.35 s).

## Escena 9 · Payback: mismo jugador · S3 · 42.7–45.3s
Fondo: `papel` con líneas de campo. Es el MISMO dibujo de la escena 6, ahora completo.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 9.1 | 42.8 | "**Mismo** jugador," | El jugador (camiseta verde "D") en la misma pose que 6.6, sonriendo con tinta. Rótulo "MISMO JUGADOR" | `PANEL-SLAM`; `IDLE-BOB` | slam |
| 9.2 | 43.9 | "…**camiseta** del…" | La camiseta "D" crece y se llena de color con una chispa; rótulo "CAMISETA RIVAL" | `PULSE`; `MISREG` | ding |
| 9.3 | 44.6 | "…**rival.**" | El jugador patea y el balón entra a la portería azul (red que se mueve), `ONOMATO` "¡GOL!" `rojo`. La portería ahora está llena de balones/red rota | balón `FLOW`; red `SHAKE`; `ONOMATO`; `CAM-PUNCH` | bam |

**Transición →** `ZOOM-THRU` por la portería, 0.3 s.

## Escena 10 · La fecha · S3 · 45.3–48.5s
Fondo: `doom` con trama y rayos; luego `rojo` 1 s.

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 10.1 | 45.4 | "**Avengers:**" | Logo de Avengers: Doomsday (`assets/comun/avengers-doomsday-logo.png`) sobre placa de cómic | Placa `PANEL-SLAM` con rotación | slam |
| 10.2 | 46.4 | "**Doomsday**" | Palabra "DOOMSDAY" Anton 260 px `amarillo`, sombra dura, con grietas | `ONOMATO`; `ZOOM-GOLPE` | stinger |
| 10.3 | 47.3 | "…llega el **dieciocho**…" | Hoja de calendario "18 DIC 2026" cae y se sella; el contador `FALTAN 36 DÍAS` pulsa | Calendario `DROP-IN`; sello `rojo` `STAMP`; contador `PULSE` | stamp |

**Transición →** `COVER-SLIDE` (la siguiente portada entra desde la derecha), 0.4 s.

## Escena 11 · CTA y loop · S4 · 48.5–51.9s
Fondo: `multi` con trama (mismo encuadre que la escena 1).

| # | t (s) | Voz (disparador) | Visual | Movimiento | SFX |
|---|---|---|---|---|---|
| 11.1 | 48.6 | "**Sigue** la serie:" | Portada "N.º 02 DE 11" (misma composición que la portada 1: logo arriba, número, silueta al centro) entra deslizándose. Cinta "SIGUE LA SERIE" | `COVER-SLIDE`; cinta `STAMP` | whoosh |
| 11.2 | 49.7 | "…en el **siguiente,**" | La portada se acomoda, aparece un botón de cómic "SIGUIENTE ▶" que pulsa. `CAP "EN EL SIGUIENTE"` | Botón `PULSE`; `CAPTION-DROP` | tick |
| 11.3 | 51.2 | "…quién es **Doom**" | En la portada, la silueta de la máscara de Doom (verde) abre los ojos; rótulo "¿QUIÉN ES DOCTOR DOOM?" | Ojos `PULSE`; texto `WORD-POP` | stinger |

---

## Notas de producción

- **Conteo**: 11 escenas, 49 beats en 51.9 s (un beat cada ~1.05 s).
- **Texto en pantalla**: nunca transcribe la narración; solo nombres, golpes y rótulos de 2–5 palabras.
- **Música**: pendiente (el pipeline no la mezcla aún). Cuando exista: orquestal-electrónica 120–135 BPM a −20 dB; corte de 0.5 s en 34.8–35.3.
- **Riesgos**:
  - Rostros: ninguno dibujado; la cabeza "lisa" es el recurso de personaje. La única foto real es RDJ en 2.3 (≤ 2 s) y el logo de Endgame en 7.4.
  - Colores: el verde `doom` solo en Doom y su plan; `heroe` azul solo en héroes/Avengers.
  - La escena 6 y la 9 deben ser el mismo dibujo (mismo jugador, mismo balón y portería).
  - Las escenas 3 y 8 cargan mucho: mantener máximo 3 objetos grandes y 1 onomatopeya a la vez.
