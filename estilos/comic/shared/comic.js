/* window.COM: tema "comic" de la serie camino-a-doomsday (ver ../../camino-a-doomsday/_estilo.md).
   Complementa a EXP igual que REC complementa: se carga DESPUÉS de explicando.js, se activa con
   la clase .com en .exp-stage y no toca otras series. Mismas reglas: todo seek-safe (solo
   fromTo / to / set sobre el timeline pausado), sin Math.random (EXP.rng), sin repeat:-1 ni
   relojes. comic.js y comic-objects.js comparten window.COM (por eso el Object.assign y el
   arranque tolerante al orden de carga).

   ============================ API de COM ============================
   Todas las funciones reciben el timeline primero y el tiempo `at` (segundos) después.
   `el` acepta un elemento o una lista (helper arr). `{chain:true}` = immediateRender:false
   (para encadenar dos fromTo sobre la misma propiedad).

   COM.scene(tl, sceneEl, ini, fin, {enter, x, y, color})
       Visibilidad + CAM-DRIFT + BG-DRIFT los delega en EXP.scene(enter:"cut"); encima añade
       la transición de cómic en [ini - dur, ini]:
         enter:"halftone" (0.35 s) — barrido de puntos Ben-Day del color `color`; el círculo
                 de puntos va 150 px adelantado al clip de la escena; origen en x,y px.
         enter:"ink"      (0.3 s)  — mancha de tinta irregular (SVG estático) escala 0→3
                 (power4.out) cubre en ~45 % y la escena nueva aparece debajo.
         enter:"pageflip" (0.4 s)  — clip diagonal desde la esquina inferior derecha
                 (power2.inOut) + triángulo "doblez" papel con sombra dura que se desvanece.
         enter:"cover"    (0.4 s)  — la escena entra deslizada desde la derecha (x 1080→0,
                 power4.out) con rotación inicial 6°.
         enter:"zoom"     (0.3 s)  — la escena entra escalando 2.5→1 con opacidad (power2.out).
         enter:"cut"      — corte seco (igual que EXP.scene).
       Ej: COM.scene(tl, q("#v01-e4"), E("4")[0], E("4")[1], {enter:"ink", x:540, y:820});
   COM.panelSlam(tl, el, at, {from:"L"|"R"|"T"|"B", rot:4, dur:0.3, stagger, chain})
       PANEL-SLAM: entra desde fuera de pantalla con rotación 3–5°, rebote back.out(1.7) y
       squash 1.04→1 de 0.08 s al asentarse. Ej: COM.panelSlam(tl, panel, b("2.1"), {from:"R"});
   COM.panelSplit(tl, els, at, {dirs:["L","R","T"...], gap:0.08, rot})
       PANEL-SPLIT: panelSlam escalonado (gap s entre viñetas; rot alterna signo).
   COM.panelBreak(tl, el, at, {amt:1.35, chain})
       PANEL-BREAK: el elemento crece a `amt` por encima de su marco con back.out. CONTRATO:
       el PADRE del elemento debe tener overflow visible (un .panel normal trae overflow
       hidden y lo recortaría; usa un .panel--sin-sombra con style="overflow:visible" o saca
       el objeto del .panel y colócalo encima). Ej: COM.panelBreak(tl, escudo, b("4.3"));
   COM.onomato(tl, el, at, {rot:-6, hold:0.9, out:true})
       ONOMATO: escala 0→1.2→1 (elastic feel, 0.25 s total) manteniendo la rotación, salpica
       12 rayitos deterministas (COM.rng) alrededor 0.3 s y, si out, se va scale→0 tras `hold`.
       Ej: COM.onomato(tl, q("#v01-bam"), b("2.4"), {rot:-6, hold:0.9});
   COM.speedLines(tl, el, at, {dur:0.4, mode:"radial"|"parallel", dir:"L"|"R"|"U"|"D", n:36,
                               color, seed:1, until})
       SPEED-LINES: `el` es un contenedor 1080x1920 class="speed" ya en el DOM; crea N rayitos
       deterministas y los lanza hacia el centro (radial) o en la dirección `dir` (parallel).
       dur 0 o "loop" = bucle continuo seek-safe (fromTo largo con repeat; hay que pasar
       `until` = tiempo fin del bucle). Ej: COM.speedLines(tl, q("#v01-sl"), b("2.4"), {n:36});
   COM.zoomGolpe(tl, sceneEl, at, {amt:1.25, chain})
       ZOOM-GOLPE: scale del .rig 1→amt en 0.2 s (power4.out) + temblor mínimo y regreso a 1
       en 0.5 s (power2.inOut). CAPAS: usa el `scale` del .rig (misma capa que CAM-PUNCH de
       EXP — no llames los dos en el mismo instante; con chain encadenan) y el temblor va en
       x/y del .cam, que nadie más usa. Ej: COM.zoomGolpe(tl, scene, b("3.3"));
   COM.flashBlanco(tl, stageEl, at, {frames:4})
       FLASH-BLANCO: el overlay .com-flash (lo crea COM.setup) a opacidad 1 durante `frames`
       frames (4 = 0.133 s) y vuelve a 0. Ej: COM.flashBlanco(tl, stage, b("8.1"));
   COM.misreg(tl, el, at, {px:4, dur:0.15, chain})
       MISREG: desfase de contorno rojo/cian 3–4 px un instante (anima --mx/--my; el CSS
       [data-mis] los usa en text-shadow). Va en TEXTO (kw/ttl/ono/cinta/contador).
       Ej: COM.misreg(tl, ttl, b("3.3"), {px:4});
   COM.captionDrop(tl, el, at, {text, perChar:0.025, chain})
       CAPTION-DROP: la caja .cap cae a su esquina (y −200→0, back.out, 0.3 s) y escribe el
       texto letra a letra (typeOn). Si pasas `text`, reemplaza el contenido.
   COM.captionOut(tl, el, at)
       Sale la caja hacia arriba con fade 0.2 s.
   COM.counter(tl, el, at, n) / COM.counterPulse(tl, el, at)
       Muestra la placa .contador con "FALTAN n DÍAS" (entra con panelSlam desde arriba y
       queda inclinada −3°) / PULSE 1→1.15→1.
   Alias directos a EXP.* (sin lógica propia): COM.stamp, COM.wordPop, COM.pulse, COM.shake,
       COM.drawOn, COM.popIn, COM.popOut, COM.slideIn, COM.dropIn, COM.idleBob, COM.rng.
   COM.setup(stage) — una vez por video: añade .com, crea grano 4 %, marca, flash y los defs
       SVG del patrón Ben-Day (<pattern id="com-benday">); llama COM.mount(stage) si ya existe
       (comic-objects.js puede cargarse antes o después: es tolerante).
   COM.chrome(tl, stage, t) — como EXP.chrome pero SIN barra de progreso (la serie no la usa;
       no llames a EXP.chrome aquí) y con la marca del cómic abajo: anima la marca y devuelve
       { el, flash }. Ej: const ch = COM.chrome(tl, stage); */
(function () {
  "use strict";
  window.COM = window.COM || {};
  const EXP = window.EXP;
  const FRAME = 1 / 30;
  const W = 1080, H = 1920;

  // Paleta de la serie (igual que las variables de comic.css)
  const C = {
    tinta: "#0B0B14", papel: "#FFF3D6", heroe: "#1E5BFF", rojo: "#E8212B",
    amarillo: "#FFD400", doom: "#1FA85A", multi: "#8A2BE2", ciencia: "#00C8E8",
    ceniza: "#6B7280", doomOsc: "#0E5C32", multiOsc: "#4B1580",
  };

  const arr = (x) => (Array.isArray(x) ? x : x && x.length !== undefined && !(x instanceof Element) ? Array.from(x) : [x]);
  const ir = (o) => (o && o.chain ? { immediateRender: false } : {});

  // ---------------------------------------------------------------- overlays de escena
  // Crea (una vez por escena) un overlay full-screen DENTRO del stage (no de la escena, para
  // que el clip de la escena no lo recorte) o dentro de la escena (con inside=true).
  function overlayOf(el, cls, make, inside) {
    const host = inside ? el : el.parentNode; // el.parentNode = .exp-stage
    const sel = inside ? ":scope > ." + cls : ":scope > ." + cls;
    let ov = host.querySelector(sel);
    if (!ov) {
      ov = document.createElement("div");
      ov.className = cls;
      if (make) make(ov);
      host.appendChild(ov);
    }
    return ov;
  }

  // ---------------------------------------------------------------- escenas
  // Duraciones de las transiciones de cómic
  const ENTER = { halftone: 0.35, ink: 0.3, pageflip: 0.4, cover: 0.4, zoom: 0.3, cut: 0 };

  function scene(tl, el, start, end, o) {
    o = Object.assign({ enter: "cut", x: 540, y: 820, color: C.papel }, o || {});
    const d = ENTER[o.enter] || 0;
    // La visibilidad, CAM-DRIFT y BG-DRIFT los hace EXP.scene (enter "cut" + dur d → visible en start-d)
    EXP.scene(tl, el, start, end, { enter: "cut", dur: d, x: o.x, y: o.y });
    const t0 = Math.max(0, start - d);
    if (!d || o.enter === "cut") return tl;

    if (o.enter === "halftone") {
      // HALFTONE-WIPE: círculo de puntos del color `color` que barre desde (x,y); va 150 px
      // adelantado al clip de la escena para que se vea la trama a la cabeza del barrido.
      const ov = overlayOf(el, "com-halftone", (n) => {
        n.style.backgroundImage =
          "radial-gradient(circle, " + o.color + " 7px, transparent 7.5px)," +
          "radial-gradient(circle, " + o.color + " 7px, transparent 7.5px)";
        n.style.backgroundSize = "28px 28px";
        n.style.backgroundPosition = "0 0, 14px 14px";
      });
      tl.fromTo(el, { clipPath: "circle(0px at " + o.x + "px " + o.y + "px)" },
        { clipPath: "circle(2400px at " + o.x + "px " + o.y + "px)", ease: "power2.in", duration: d }, t0);
      tl.fromTo(ov, { clipPath: "circle(0px at " + o.x + "px " + o.y + "px)", visibility: "visible" },
        { clipPath: "circle(2560px at " + o.x + "px " + o.y + "px)", ease: "power2.in", duration: d }, t0);
      tl.set(ov, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "ink") {
      // INK-SPLASH: mancha negra irregular (SVG path estático, ~10 lóbulos) escala 0→3 con
      // power4.out; la escena nueva aparece (debajo) cuando la mancha ya la cubre.
      tl.set(el, { visibility: "hidden" }, t0); // gana al set de EXP por orden de inserción
      tl.set(el, { visibility: "visible" }, t0 + d * 0.45);
      const inkC = o.inkColor || C.tinta; // la mancha es tinta (negra) salvo inkColor explícito
      const blob = overlayOf(el, "com-ink", (n) => {
        const s = 1200;
        n.style.width = s + "px";
        n.style.height = s + "px";
        n.style.left = (o.x - s / 2) + "px";
        n.style.top = (o.y - s / 2) + "px";
        n.innerHTML = '<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + " " + s + '"><path d="' + inkPath() + '"/></svg>';
      }, true);
      blob.querySelector("path").style.fill = inkC;
      tl.fromTo(blob, { scale: 0, transformOrigin: "50% 50%", visibility: "visible" },
        { scale: 3, ease: "power4.out", duration: d }, t0);
      tl.set(blob, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "pageflip") {
      // PAGE-FLIP: la escena se revela con una diagonal que barre desde la esquina inferior
      // derecha; un triángulo "doblez" (papel + sombra dura) acompaña y se desvanece al final.
      tl.fromTo(el, { clipPath: "polygon(1080px 1920px, 1080px 1920px, 1080px 1920px)" },
        { clipPath: "polygon(-2020px 1920px, 1080px -1180px, 1080px 1920px)", ease: "power2.inOut", duration: d }, t0);
      const fold = overlayOf(el, "com-pagefold");
      tl.fromTo(fold, { clipPath: "polygon(1080px 1920px, 1080px 1920px, 1080px 1920px)", opacity: 1, visibility: "visible" },
        { clipPath: "polygon(-2020px 1920px, 1080px -1180px, -2020px -1180px)", ease: "power2.inOut", duration: d }, t0);
      tl.to(fold, { opacity: 0, duration: d * 0.3, ease: "power1.in" }, t0 + d * 0.7);
      tl.set(fold, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "cover") {
      // COVER-SLIDE: la escena nueva entra deslizando desde la derecha con 6° de giro.
      tl.fromTo(el, { x: W, rotation: 6, transformOrigin: "50% 100%" },
        { x: 0, rotation: 0, ease: "power4.out", duration: d }, t0);
    } else if (o.enter === "zoom") {
      // ZOOM-THRU cómic: la escena entra escalando 2.5→1 con opacidad.
      tl.fromTo(el, { scale: 2.5, opacity: 0, transformOrigin: "540px 820px" },
        { scale: 1, opacity: 1, ease: "power2.out", duration: d }, t0);
    }
    return tl;
  }

  // Mancha de tinta determinista: 10 lóbulos (radio ondulado) unidos con Catmull-Rom → Bézier.
  function inkPath() {
    const N = 10, cx = 600, cy = 600;
    const rr = (i) => 380 + 60 * Math.sin(i * 2.1) + 25 * Math.cos(i * 4.7);
    const pts = [];
    for (let i = 0; i < N; i++) {
      const a = (i / N) * Math.PI * 2;
      pts.push([cx + Math.cos(a) * rr(i), cy + Math.sin(a) * rr(i)]);
    }
    let p = "M " + pts[0][0].toFixed(1) + " " + pts[0][1].toFixed(1);
    for (let i = 0; i < N; i++) {
      const p0 = pts[(i - 1 + N) % N], p1 = pts[i], p2 = pts[(i + 1) % N], p3 = pts[(i + 2) % N];
      p += " C " + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + " " + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) +
        ", " + (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + " " + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) +
        ", " + p2[0].toFixed(1) + " " + p2[1].toFixed(1);
    }
    return p + " Z";
  }

  // ---------------------------------------------------------------- viñetas
  function panelSlam(tl, el, at, o) {
    o = o || {};
    const from = o.from || "L";
    const rot = o.rot != null ? o.rot : 4;
    const dur = o.dur || 0.3;
    const off = { L: [-1400, 0], R: [1400, 0], T: [0, -2100], B: [0, 2100] }[from];
    arr(el).forEach((e, i) => {
      const t0 = at + i * (o.stagger || 0);
      tl.fromTo(e, { x: off[0], y: off[1], rotation: from === "L" || from === "T" ? -rot : rot },
        { x: 0, y: 0, rotation: 0, duration: dur, ease: "back.out(1.7)", ...ir(o) }, t0);
      // squash de asentamiento 1.04→1 (no toca x/y/rotation: se suma sin pisar)
      tl.fromTo(e, { scale: 1.04 }, { scale: 1, duration: 0.08, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, t0 + dur);
    });
    return tl;
  }

  function panelSplit(tl, els, at, o) {
    o = o || {};
    const dirs = o.dirs || ["L", "R"];
    arr(els).forEach((e, i) => {
      panelSlam(tl, e, at + i * (o.gap != null ? o.gap : 0.08), { from: dirs[i % dirs.length], rot: i % 2 ? 3.5 : -4.5 });
    });
    return tl;
  }

  function panelBreak(tl, el, at, o) {
    o = o || {};
    return tl.fromTo(arr(el), { scale: 1 }, { scale: o.amt || 1.35, duration: 0.3, ease: "back.out(1.7)", transformOrigin: "50% 50%", ...ir(o) }, at);
  }

  // ---------------------------------------------------------------- onomatopeya
  // 12 rayitos alrededor del texto; posiciones deterministas (EXP.rng), medición de layout
  // hecha UNA vez al construir la composición (nunca dentro del timeline).
  function makeRayos(e, seed) {
    if (e._comRayos) return e._comRayos;
    const host = e.parentNode; // .c o .rig (position absolute)
    const cont = document.createElement("div");
    cont.className = "ono-rayos";
    const cx = (e.offsetLeft || 0) + (e.offsetWidth || 400) / 2;
    const cy = (e.offsetTop || 0) + (e.offsetHeight || 200) / 2;
    const r = EXP.rng(seed || 17);
    const rays = [];
    for (let i = 0; i < 12; i++) {
      const d = document.createElement("i");
      d.className = "rayito";
      d.style.width = (90 + r() * 110) + "px";
      d.style.height = "12px";
      cont.appendChild(d);
      gsap.set(d, { x: cx, y: cy, rotation: (i / 12) * 360 + r() * 24, transformOrigin: "0 50%", opacity: 0 });
      rays.push(d);
    }
    host.appendChild(cont);
    e._comRayos = rays;
    return rays;
  }

  function onomato(tl, el, at, o) {
    o = o || {};
    const rot = o.rot != null ? o.rot : -6;
    const hold = o.hold != null ? o.hold : 0.9;
    arr(el).forEach((e) => {
      tl.fromTo(e, { scale: 0, rotation: rot }, { scale: 1.2, rotation: rot, duration: 0.16, ease: "power3.out" }, at);
      tl.to(e, { scale: 1, duration: 0.11, ease: "power2.out" }, at + 0.16);
      const rays = makeRayos(e, o.seed || 17);
      rays.forEach((r, i) => {
        tl.fromTo(r, { scale: 0.2, opacity: 1 }, { scale: 1.5, opacity: 0, duration: 0.3, ease: "power3.out", immediateRender: false }, at + 0.02 + i * 0.004);
      });
      if (o.out !== false) tl.to(e, { scale: 0, duration: 0.16, ease: "power3.in" }, at + hold);
    });
    return tl;
  }

  // ---------------------------------------------------------------- líneas de velocidad
  function makeLineas(cont, n, color) {
    cont.querySelectorAll(":scope > .rayito").forEach((n2) => n2.remove());
    const out = [];
    for (let i = 0; i < n; i++) {
      const d = document.createElement("i");
      d.className = "rayito";
      if (color) d.style.background = color;
      cont.appendChild(d);
      out.push(d);
    }
    return out;
  }

  function speedLines(tl, el, at, o) {
    o = o || {};
    const mode = o.mode || "radial";
    const n = o.n || 36;
    const r = EXP.rng(o.seed || 1);
    const cx = 540, cy = 820;
    const dur = o.dur == null ? 0.4 : o.dur;
    const loop = dur === 0 || dur === "loop";
    const until = o.until != null ? o.until : at + 2;
    const period = o.period || 1.1;
    const lines = makeLineas(el, n, o.color);
    lines.forEach((L, i) => {
      const len = 150 + r() * 280;
      const wid = 10 + r() * 8;
      gsap.set(L, { width: len + "px", height: wid + "px" });
      let from, to, rot;
      if (mode === "radial") {
        // radiales: apuntan al centro (punta en el centro), entran desde fuera
        const ang = (i / n) * 360 + r() * 14;
        const d1 = 780 + r() * 720;
        const d2 = 140 + r() * 260;
        const rad = (ang * Math.PI) / 180;
        from = [cx + Math.cos(rad) * d1, cy + Math.sin(rad) * d1];
        to = [cx + Math.cos(rad) * d2, cy + Math.sin(rad) * d2];
        rot = ang;
      } else {
        // paralelas: cruzan toda la pantalla en la dirección dir
        const dir = o.dir || "R";
        const v = { R: [1, 0], L: [-1, 0], U: [0, -1], D: [0, 1] }[dir];
        const along = Math.atan2(v[1], v[0]) * 180 / Math.PI;
        rot = along + 180; // punta apuntando hacia adelante
        const perp = 1 - Math.abs(v[0]);
        const cross = perp ? r() * (v[0] ? H : W) : r() * (dir === "U" || dir === "D" ? W : H);
        const m1 = -600 - r() * 500, m2 = (dir === "R" || dir === "D" ? (v[0] ? W : H) : 0) + 600 + (dir === "L" || dir === "U" ? 0 : 0);
        const a1 = dir === "L" || dir === "U" ? m2 : m1;
        const a2 = dir === "L" || dir === "U" ? m1 : m2;
        from = v[0] ? [a1, cross] : [cross, a1];
        to = v[0] ? [a2, cross] : [cross, a2];
      }
      gsap.set(L, { rotation: rot, transformOrigin: "0 50%" });
      if (loop) {
        // bucle continuo SEEK-SAFE: fromTo con repeat (nada de repeat:-1) y capas desfasadas
        const off = (i / n) * period * 0.7;
        const reps = Math.max(0, Math.floor((until - at - off) / period) - 1);
        tl.fromTo(L, { x: from[0], y: from[1], opacity: o.loopOpacity || 0.8 },
          { x: to[0], y: to[1], duration: period, ease: "none", repeat: reps, immediateRender: false }, at + off);
      } else {
        const d = dur;
        tl.fromTo(L, { x: from[0], y: from[1], opacity: 0 },
          { x: to[0], y: to[1], opacity: 1, duration: d * 0.75, ease: "power3.in" }, at + r() * d * 0.15);
        tl.to(L, { opacity: 0, duration: d * 0.3, ease: "power1.in" }, at + d * 0.72);
      }
    });
    return tl;
  }

  // ---------------------------------------------------------------- golpes de cámara
  function zoomGolpe(tl, sceneEl, at, o) {
    o = o || {};
    const amt = o.amt || 1.25;
    const rig = sceneEl.querySelector(":scope > .cam > .rig") || sceneEl.querySelector(".rig");
    const cam = sceneEl.querySelector(":scope > .cam");
    // ZOOM-GOLPE anima el scale del .rig (misma capa que CAM-PUNCH de EXP: no llamar los dos
    // en el mismo instante) y el temblor va en x/y del .cam para no pisar ninguna escala.
    if (rig) {
      tl.fromTo(rig, { scale: 1 }, { scale: amt, duration: 0.2, ease: "power4.out", ...ir(o) }, at);
      tl.to(rig, { scale: 1, duration: 0.5, ease: "power2.inOut", immediateRender: false }, at + 0.2);
    }
    if (cam) {
      const temblor = [[-7, 4], [6, -5], [-4, 3], [0, 0]];
      temblor.forEach((t2, i) => {
        tl.to(cam, { x: t2[0], y: t2[1], duration: 0.05, ease: "none" }, at + 0.2 + i * 0.05);
      });
    }
    return tl;
  }

  function flashBlanco(tl, stageEl, at, o) {
    const frames = o && o.frames ? o.frames : 4;
    let f = stageEl.querySelector(":scope > .com-chrome > .com-flash") || stageEl.querySelector(".com-flash");
    if (!f) {
      setup(stageEl);
      f = stageEl.querySelector(".com-flash");
    }
    tl.set(f, { opacity: 1 }, at);
    tl.set(f, { opacity: 0 }, at + frames * FRAME);
    return tl;
  }

  // ---------------------------------------------------------------- misregistration
  function misreg(tl, el, at, o) {
    o = o || {};
    const px = o.px || 4;
    arr(el).forEach((e) => {
      e.setAttribute("data-mis", "");
      tl.fromTo(e, { "--mx": px + "px", "--my": Math.round(px * 0.6) + "px" },
        { "--mx": "0px", "--my": "0px", duration: o.dur || 0.15, ease: "power1.out", immediateRender: false }, at);
    });
    return tl;
  }

  // ---------------------------------------------------------------- caja del narrador
  function captionDrop(tl, el, at, o) {
    o = o || {};
    arr(el).forEach((e) => {
      if (o.text != null) e.textContent = o.text;
      tl.fromTo(e, { y: -200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.7)", ...ir(o) }, at);
      EXP.typeOn(tl, e, at + 0.3, { perChar: o.perChar || 0.025 });
    });
    return tl;
  }

  function captionOut(tl, el, at, o) {
    o = o || {};
    arr(el).forEach((e) => tl.to(e, { y: -(o.y || 120), opacity: 0, duration: 0.2, ease: "power2.in" }, at));
    return tl;
  }

  // ---------------------------------------------------------------- contador
  function counter(tl, el, at, n) {
    if (n != null) el.textContent = "FALTAN " + n + " DÍAS";
    panelSlam(tl, el, at, { from: "T", rot: 3, dur: 0.3 });
    // la placa queda inclinada −3° (el slam termina en 0 a at+0.38)
    tl.set(el, { rotation: -3 }, at + 0.39);
    return tl;
  }

  function counterPulse(tl, el, at) {
    return EXP.pulse(tl, el, at, { to: 1.15 });
  }

  // ---------------------------------------------------------------- setup / chrome
  // Una vez por video: clase .com, grano 4 %, marca, flash y defs SVG del patrón Ben-Day.
  // Tolera el orden de carga de comic-objects.js: si COM.mount ya existe lo llama; si no,
  // se llamará de nuevo (es idempotente) cuando el otro script monte.
  function mountObjects(stage) {
    if (typeof window.COM.mount === "function") {
      try { window.COM.mount(stage); } catch (e) { console.warn("COM.mount falló:", e); }
    }
  }
  function setup(stage) {
    if (!stage) return;
    if (stage.dataset.comSetup) { mountObjects(stage); return; }
    stage.dataset.comSetup = "1";
    stage.classList.add("com");
    const c = document.createElement("div");
    c.className = "com-chrome";
    // SIN barra de progreso: la serie no la usa (ver COM.chrome)
    c.innerHTML = '<div class="com-grano"></div><div class="com-marca">explicando</div><div class="com-flash"></div>';
    stage.appendChild(c);
    // defs SVG comunes: patrón Ben-Day <pattern id="com-benday"> (círculos tinta, 15/30 %)
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "0");
    svg.setAttribute("height", "0");
    svg.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
    svg.innerHTML =
      '<defs>' +
      '<pattern id="com-benday" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">' +
      '<circle cx="7" cy="7" r="7" fill="#0B0B14" opacity="0.15"/>' +
      '<circle cx="21" cy="21" r="7" fill="#0B0B14" opacity="0.15"/>' +
      "</pattern>" +
      '<pattern id="com-benday-fuerte" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">' +
      '<circle cx="7" cy="7" r="7" fill="#0B0B14" opacity="0.3"/>' +
      '<circle cx="21" cy="21" r="7" fill="#0B0B14" opacity="0.3"/>' +
      "</pattern>" +
      "</defs>";
    stage.appendChild(svg);
    mountObjects(stage);
  }

  // COM.chrome: como EXP.chrome pero SIN barra de progreso (la serie no la usa; no llames a
  // EXP.chrome) y con la marca "explicando" como sticker abajo (y 1560). Devuelve { el, flash }.
  function chrome(tl, stage, t) {
    setup(stage);
    const c = stage.querySelector(":scope > .com-chrome");
    const marca = c.querySelector(".com-marca");
    tl.fromTo(marca, { opacity: 0, y: 24 }, { opacity: 0.85, y: 0, duration: 0.3, ease: "back.out(2)" }, 1);
    return { el: c, flash: c.querySelector(".com-flash") };
  }

  // ---------------------------------------------------------------- alias a EXP.*
  const ALIAS = ["stamp", "wordPop", "pulse", "shake", "drawOn", "popIn", "popOut", "slideIn", "dropIn", "idleBob"];
  ALIAS.forEach((k) => {
    if (typeof EXP[k] === "function") window.COM[k] = EXP[k];
    else console.warn("COM: EXP." + k + " no existe; alias omitido");
  });

  Object.assign(window.COM, {
    C, scene, panelSlam, panelSplit, panelBreak, onomato, speedLines, zoomGolpe,
    flashBlanco, misreg, captionDrop, captionOut, counter, counterPulse, setup, chrome,
  });
  window.COM.rng = EXP.rng;
})();
