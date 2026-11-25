/* comic-h.js: variante HORIZONTAL (1920x1080) del tema cómic de Camino a Doomsday.
   Se carga DESPUÉS de comic.js y reemplaza solo lo que depende del tamaño del cuadro:
   COM.scene (transiciones), COM.speedLines, COM.panelSlam/panelSplit, COM.chrome.
   Agrega: COM.datoCounter (placa "DATO N / 15"), COM.progress (barra global), COM.sello (STAMP con rebote).
   Mismas reglas seek-safe que comic.js. Los Shorts verticales no cargan este archivo. */
(function () {
  "use strict";
  const COM = window.COM, EXP = window.EXP;
  const W = 1920, H = 1080, CX = 960, CY = 540;
  const C = COM.C;
  const arr = (x) => (Array.isArray(x) ? x : x && x.length !== undefined && !(x instanceof Element) ? Array.from(x) : [x]);
  const ir = (o) => (o && o.chain ? { immediateRender: false } : {});
  const ENTER = { halftone: 0.35, ink: 0.3, pageflip: 0.4, cover: 0.4, zoom: 0.3, whip: 0.25, cut: 0 };

  function overlayOf(el, cls, make, inside) {
    const host = inside ? el : el.parentNode;
    let ov = host.querySelector(":scope > ." + cls);
    if (!ov) {
      ov = document.createElement("div");
      ov.className = cls;
      if (make) make(ov);
      host.appendChild(ov);
    }
    return ov;
  }

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

  function scene(tl, el, start, end, o) {
    o = Object.assign({ enter: "cut", x: CX, y: CY, color: C.papel }, o || {});
    const d = ENTER[o.enter] || 0;
    EXP.scene(tl, el, start, end, { enter: "cut", dur: d, x: o.x, y: o.y });
    const t0 = Math.max(0, start - d);
    if (!d || o.enter === "cut") return tl;
    if (o.enter === "halftone") {
      const ov = overlayOf(el, "com-halftone", (n) => {
        n.style.backgroundImage = "radial-gradient(circle, " + o.color + " 7px, transparent 7.5px),radial-gradient(circle, " + o.color + " 7px, transparent 7.5px)";
        n.style.backgroundSize = "28px 28px";
        n.style.backgroundPosition = "0 0, 14px 14px";
      });
      tl.fromTo(el, { clipPath: "circle(0px at " + o.x + "px " + o.y + "px)" },
        { clipPath: "circle(2300px at " + o.x + "px " + o.y + "px)", ease: "power2.in", duration: d }, t0);
      tl.fromTo(ov, { clipPath: "circle(0px at " + o.x + "px " + o.y + "px)", visibility: "visible" },
        { clipPath: "circle(2450px at " + o.x + "px " + o.y + "px)", ease: "power2.in", duration: d }, t0);
      tl.set(ov, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "ink") {
      tl.set(el, { visibility: "hidden" }, t0);
      tl.set(el, { visibility: "visible" }, t0 + d * 0.45);
      const blob = overlayOf(el, "com-ink", (n) => {
        const s = 1200;
        n.style.width = s + "px"; n.style.height = s + "px";
        n.style.left = (o.x - s / 2) + "px"; n.style.top = (o.y - s / 2) + "px";
        n.innerHTML = '<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + " " + s + '"><path d="' + inkPath() + '"/></svg>';
      }, true);
      blob.querySelector("path").style.fill = o.inkColor || C.tinta;
      tl.fromTo(blob, { scale: 0, transformOrigin: "50% 50%", visibility: "visible" }, { scale: 3.4, ease: "power4.out", duration: d }, t0);
      tl.set(blob, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "pageflip") {
      tl.fromTo(el, { clipPath: `polygon(${W}px ${H}px, ${W}px ${H}px, ${W}px ${H}px)` },
        { clipPath: `polygon(${-W - 400}px ${H}px, ${W}px ${-W - 400}px, ${W}px ${H}px)`, ease: "power2.inOut", duration: d }, t0);
      const fold = overlayOf(el, "com-pagefold");
      tl.fromTo(fold, { clipPath: `polygon(${W}px ${H}px, ${W}px ${H}px, ${W}px ${H}px)`, opacity: 1, visibility: "visible" },
        { clipPath: `polygon(${-W - 400}px ${H}px, ${W}px ${-W - 400}px, ${-W - 400}px ${-W - 400}px)`, ease: "power2.inOut", duration: d }, t0);
      tl.to(fold, { opacity: 0, duration: d * 0.3, ease: "power1.in" }, t0 + d * 0.7);
      tl.set(fold, { visibility: "hidden" }, t0 + d + 0.01);
    } else if (o.enter === "cover") {
      tl.fromTo(el, { x: W, rotation: 4, transformOrigin: "50% 100%" }, { x: 0, rotation: 0, ease: "power4.out", duration: d }, t0);
    } else if (o.enter === "whip") {
      tl.fromTo(el, { x: W * 0.6, opacity: 0.4 }, { x: 0, opacity: 1, ease: "power3.out", duration: d }, t0);
    } else if (o.enter === "zoom") {
      tl.fromTo(el, { scale: 2.2, opacity: 0, transformOrigin: o.x + "px " + o.y + "px" }, { scale: 1, opacity: 1, ease: "power2.out", duration: d }, t0);
    }
    return tl;
  }

  function panelSlam(tl, el, at, o) {
    o = o || {};
    const from = o.from || "L";
    const rot = o.rot != null ? o.rot : 4;
    const dur = o.dur || 0.3;
    const off = { L: [-2400, 0], R: [2400, 0], T: [0, -1400], B: [0, 1400] }[from];
    arr(el).forEach((e, i) => {
      const t0 = at + i * (o.stagger || 0);
      tl.fromTo(e, { x: off[0], y: off[1], rotation: from === "L" || from === "T" ? -rot : rot },
        { x: 0, y: 0, rotation: 0, duration: dur, ease: "back.out(1.7)", ...ir(o) }, t0);
      tl.fromTo(e, { scale: 1.04 }, { scale: 1, duration: 0.08, ease: "power2.out", transformOrigin: "50% 50%", immediateRender: false }, t0 + dur);
    });
    return tl;
  }

  function panelSplit(tl, els, at, o) {
    o = o || {};
    const dirs = o.dirs || ["L", "R"];
    arr(els).forEach((e, i) => panelSlam(tl, e, at + i * (o.gap != null ? o.gap : 0.08), { from: dirs[i % dirs.length], rot: i % 2 ? 3.5 : -4.5 }));
    return tl;
  }

  function speedLines(tl, el, at, o) {
    o = o || {};
    const mode = o.mode || "radial";
    const n = o.n || 44;
    const r = EXP.rng(o.seed || 1);
    const cx = o.cx != null ? o.cx : CX, cy = o.cy != null ? o.cy : CY;
    const dur = o.dur == null ? 0.4 : o.dur;
    el.querySelectorAll(":scope > .rayito").forEach((x) => x.remove());
    for (let i = 0; i < n; i++) {
      const L = document.createElement("i");
      L.className = "rayito";
      if (o.color) L.style.background = o.color;
      el.appendChild(L);
      const len = 200 + r() * 360, wid = 10 + r() * 9;
      gsap.set(L, { width: len + "px", height: wid + "px" });
      let from, to, rot;
      if (mode === "radial") {
        const ang = (i / n) * 360 + r() * 12;
        const d1 = 1100 + r() * 700, d2 = 220 + r() * 300;
        const rad = (ang * Math.PI) / 180;
        from = [cx + Math.cos(rad) * d1, cy + Math.sin(rad) * d1];
        to = [cx + Math.cos(rad) * d2, cy + Math.sin(rad) * d2];
        rot = ang;
      } else {
        const dir = o.dir || "R";
        const horiz = dir === "R" || dir === "L";
        const cross = r() * (horiz ? H : W);
        const a1 = dir === "R" || dir === "D" ? -700 - r() * 500 : (horiz ? W : H) + 700;
        const a2 = dir === "R" || dir === "D" ? (horiz ? W : H) + 700 : -700 - r() * 500;
        rot = { R: 180, L: 0, D: 270, U: 90 }[dir];
        from = horiz ? [a1, cross] : [cross, a1];
        to = horiz ? [a2, cross] : [cross, a2];
      }
      gsap.set(L, { rotation: rot, transformOrigin: "0 50%" });
      tl.fromTo(L, { x: from[0], y: from[1], opacity: 0 }, { x: to[0], y: to[1], opacity: 1, duration: dur * 0.75, ease: "power3.in" }, at + r() * dur * 0.15);
      tl.to(L, { opacity: 0, duration: dur * 0.3, ease: "power1.in" }, at + dur * 0.72);
    }
    return tl;
  }

  // chrome horizontal: grano + flash + marca abajo a la izquierda (sin barra; la barra es COM.progress)
  function chrome(tl, stage) {
    COM.setup(stage);
    stage.classList.add("com-h");
    const c = stage.querySelector(":scope > .com-chrome");
    return { el: c, flash: c.querySelector(".com-flash") };
  }

  // placa "DATO N / 15": entra con slam desde abajo en `at`, sale en `until`
  function datoCounter(tl, el, at, until) {
    panelSlam(tl, el, at, { from: "B", rot: 3, dur: 0.3 });
    tl.set(el, { rotation: -2 }, at + 0.39);
    if (until != null) tl.to(el, { y: 200, duration: 0.25, ease: "power2.in" }, until - 0.25);
    return tl;
  }

  // barra de progreso global: frac0..frac1 a lo largo de [t0, t1] (cada parte del video es su propia composición)
  function progress(tl, el, t0, t1, f0, f1) {
    return tl.fromTo(el, { scaleX: f0 }, { scaleX: f1, ease: "none", duration: Math.max(0.01, t1 - t0) }, t0);
  }

  function sello(tl, el, at, o) {
    o = o || {};
    const rot = o.rot != null ? o.rot : -8;
    arr(el).forEach((e) => {
      tl.fromTo(e, { scale: 2.6, rotation: rot - 10, opacity: 0 }, { scale: 1, rotation: rot, opacity: 1, duration: 0.18, ease: "power4.in", ...ir(o) }, at);
      tl.fromTo(e, { x: -6 }, { x: 0, duration: 0.12, ease: "power2.out", immediateRender: false }, at + 0.18);
    });
    return tl;
  }

  Object.assign(COM, { scene, panelSlam, panelSplit, speedLines, chrome, datoCounter, progress, sello, W, H });
})();
