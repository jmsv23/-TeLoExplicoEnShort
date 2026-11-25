/* Librería de movimiento de "Explicando" — window.EXP
   Implementa el catálogo de ../../_base/animacion.md. Todo es seek-safe: solo fromTo / to / set
   dentro del timeline pausado, sin Math.random ni relojes. Los tiempos vienen de
   assets/timings/<serie>/<video>.js (EXP.T), generados por `explicando.py tiempos`.

   Convención de capas para no pelear propiedades:
     .scene  → transiciones (x, opacity, clip-path, rotationY)        EXP.scene
     .cam    → CAM-DRIFT (scale lento)                                  EXP.scene
     .rig    → CAM-PUNCH / SHAKE de cámara                              EXP.camPunch
     elemento→ entradas/énfasis (scale, rotation, x, y)
     IDLE-BOB usa yPercent y SHAKE usa xPercent: se suman a x/y sin conflicto.
   Si un mismo elemento recibe dos fromTo sobre la misma propiedad, pasa {chain:true}
   al segundo (immediateRender:false) para que no pise el estado inicial. */
(function () {
  "use strict";
  const FRAME = 1 / 30;

  // ---------------------------------------------------------------- tiempos
  function T(compId) {
    const t = (window.EXP_T || {})[compId];
    if (!t) throw new Error("EXP: no hay tiempos para " + compId + " (corre `explicando.py tiempos`)");
    return t;
  }
  // Tiempo de un beat del motion script. Falla fuerte si el id no existe (evita beats mudos).
  function beat(t, id, offset) {
    if (!(id in t.b)) throw new Error("EXP: beat '" + id + "' no existe en timings");
    return t.b[id] + (offset || 0);
  }
  // Tiempo de la n-ésima aparición (0 = primera) de una palabra del guion.
  function word(t, text, nth) {
    const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9ñ]/g, "");
    const target = norm(text);
    let n = nth || 0;
    for (const w of t.w) {
      if (norm(w[0]) === target && n-- === 0) return w[1];
    }
    throw new Error("EXP: palabra '" + text + "' (#" + (nth || 0) + ") no está en el guion");
  }
  function q(root) {
    return (sel) => root.querySelector(sel);
  }
  function qa(root) {
    return (sel) => Array.from(root.querySelectorAll(sel));
  }

  // PRNG determinista (mulberry32) para variaciones "aleatorias" reproducibles
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const arr = (x) => (Array.isArray(x) ? x : x && x.length !== undefined && !(x instanceof Element) ? Array.from(x) : [x]);
  const ir = (o) => (o && o.chain ? { immediateRender: false } : {});

  // ---------------------------------------------------------------- escenas y transiciones
  // EXP.scene(tl, el, inicio, fin, { enter: 'cut'|'wipe'|'wipe-diag'|'whip-l'|'whip-r'|'whip-u'|'whip-d'|'zoom'|'flip',
  //                                   x, y (origen del wipe/zoom en px), dur, drift: true })
  // La transición ocurre en [inicio - dur, inicio]: la escena nueva entra ENCIMA de la anterior.
  const ENTER_DUR = { cut: 0, wipe: 0.35, "wipe-diag": 0.35, "whip-l": 0.25, "whip-r": 0.25, "whip-u": 0.25, "whip-d": 0.25, zoom: 0.4, flip: 0.4 };
  function scene(tl, el, start, end, o) {
    o = Object.assign({ enter: "cut", drift: true, x: 540, y: 820 }, o || {});
    const d = o.dur != null ? o.dur : ENTER_DUR[o.enter] || 0;
    const t0 = Math.max(0, start - d);
    const prev = tl._expPrev;
    tl.set(el, { visibility: "visible" }, t0);
    tl.set(el, { visibility: "hidden" }, end);
    const cam = el.querySelector(":scope > .cam");
    const bg = el.querySelector(":scope > .bg");
    if (o.drift && cam) tl.fromTo(cam, { scale: 1 }, { scale: 1.04, ease: "none", duration: end - t0 }, t0);
    if (bg) {
      const v = 18; // px por segundo, en diagonal
      tl.fromTo(bg, { backgroundPosition: "0px 0px" }, { backgroundPosition: v * (end - t0) + "px " + v * (end - t0) + "px", ease: "none", duration: end - t0 }, t0);
    }
    const W = 1080, H = 1920;
    switch (o.enter) {
      case "wipe":
        tl.fromTo(el, { clipPath: "circle(0px at " + o.x + "px " + o.y + "px)" }, { clipPath: "circle(2300px at " + o.x + "px " + o.y + "px)", ease: "power2.in", duration: d }, t0);
        break;
      case "wipe-diag":
        tl.fromTo(el, { clipPath: "polygon(0% 0%, 0% 0%, 0% 0%, 0% 0%)" }, { clipPath: "polygon(0% 0%, 220% 0%, 0% 220%, 0% 0%)", ease: "power2.inOut", duration: d }, t0);
        break;
      case "whip-l":
      case "whip-r":
      case "whip-u":
      case "whip-d": {
        const axis = o.enter === "whip-l" || o.enter === "whip-r" ? "x" : "y";
        // <dir> = hacia dónde barre la cámara: whip-r → lo nuevo entra por la derecha; whip-u → entra por arriba
        const sign = o.enter === "whip-r" || o.enter === "whip-d" ? 1 : -1;
        const dist = axis === "x" ? W : H;
        tl.fromTo(el, { [axis]: sign * dist, filter: "blur(24px)" }, { [axis]: 0, filter: "blur(0px)", ease: "power3.out", duration: d }, t0);
        if (prev) tl.fromTo(prev, { [axis]: 0, filter: "blur(0px)" }, { [axis]: -sign * dist, filter: "blur(24px)", ease: "power3.in", duration: d, immediateRender: false }, t0);
        break;
      }
      case "zoom":
        if (prev) {
          const pc = prev.querySelector(":scope > .cam") || prev;
          tl.to(pc, { scale: 7, transformOrigin: o.x + "px " + o.y + "px", ease: "power3.in", duration: d * 0.6 }, t0);
          tl.to(prev, { opacity: 0, duration: d * 0.2 }, t0 + d * 0.5);
        }
        tl.fromTo(el, { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, ease: "back.out(1.4)", duration: d * 0.6 }, t0 + d * 0.4);
        break;
      case "flip":
        if (prev) tl.fromTo(prev, { rotationY: 0, transformPerspective: 2400 }, { rotationY: 90, ease: "power2.in", duration: d / 2, immediateRender: false }, t0);
        tl.fromTo(el, { rotationY: -90, transformPerspective: 2400 }, { rotationY: 0, ease: "back.out(1.6)", duration: d / 2 }, t0 + d / 2);
        break;
    }
    tl._expPrev = el;
    return tl;
  }

  // Capa fija: marca, barra de progreso, grano, capa de FLASH. Devuelve { flash }.
  function chrome(tl, root, t) {
    const c = document.createElement("div");
    c.className = "exp-chrome";
    c.innerHTML = '<div class="exp-grano"></div><div class="exp-marca">explicando</div>' +
      '<div class="exp-progress"><i></i></div><div class="exp-flash"></div>';
    root.appendChild(c);
    tl.fromTo(c.querySelector(".exp-progress > i"), { scaleX: 0 }, { scaleX: 1, ease: "none", duration: t.dur }, 0);
    tl.fromTo(c.querySelector(".exp-marca"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 1);
    return { el: c, flash: c.querySelector(".exp-flash") };
  }

  // ---------------------------------------------------------------- entradas y salidas
  function popIn(tl, el, at, o) {
    o = o || {};
    return tl.fromTo(arr(el), { scale: 0, rotation: o.rot != null ? o.rot : -6, opacity: 1 },
      { scale: 1, rotation: 0, duration: o.dur || 0.35, ease: "back.out(1.7)", stagger: o.stagger || 0, ...ir(o) }, at);
  }
  function popOut(tl, el, at, o) {
    o = o || {};
    tl.to(arr(el), { scale: 1.1, duration: 0.07, ease: "power1.out", stagger: o.stagger || 0 }, at);
    return tl.to(arr(el), { scale: 0, duration: 0.13, ease: "power3.in", stagger: o.stagger || 0 }, at + 0.07);
  }
  function dropIn(tl, el, at, o) {
    o = o || {};
    const from = o.from != null ? o.from : -1100;
    arr(el).forEach((e, i) => {
      const t0 = at + i * (o.stagger || 0);
      tl.fromTo(e, { y: from, scaleX: 1, scaleY: 1 }, { y: 0, duration: 0.32, ease: "power2.in", ...ir(o) }, t0);
      tl.to(e, { scaleX: 1.15, scaleY: 0.85, duration: 0.07, ease: "power1.out", transformOrigin: "50% 100%" }, t0 + 0.32);
      tl.to(e, { scaleX: 1, scaleY: 1, duration: 0.18, ease: "back.out(3)" }, t0 + 0.39);
    });
    return tl;
  }
  function slideIn(tl, el, at, dir, o) {
    o = o || {};
    const d = { L: [-1200, 0], R: [1200, 0], T: [0, -1500], B: [0, 1500] }[dir || "R"];
    return tl.fromTo(arr(el), { x: d[0], y: d[1] }, { x: 0, y: 0, duration: o.dur || 0.4, ease: "back.out(1.3)", stagger: o.stagger || 0, ...ir(o) }, at);
  }
  function stamp(tl, el, at, o) {
    o = o || {};
    tl.fromTo(arr(el), { scale: 2.5, opacity: 0, rotation: o.rot != null ? o.rot : -4 },
      { scale: 1, opacity: 1, rotation: o.rot != null ? o.rot : -4, duration: 0.18, ease: "power4.in", ...ir(o) }, at);
    return shake(tl, el, at + 0.18, { amp: 8, dur: 0.18 });
  }
  // Parte el texto en <span class="ch"> (letras) o <span class="wd"> (palabras). Idempotente.
  function split(el, mode) {
    const cls = mode === "words" ? "wd" : "ch";
    if (el.dataset.expSplit === cls) return Array.from(el.querySelectorAll("." + cls));
    const out = [];
    const walk = (node) => {
      Array.from(node.childNodes).forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          const parts = mode === "words" ? n.textContent.split(/(\s+)/) : Array.from(n.textContent);
          parts.forEach((p) => {
            if (!p) return;
            if (/^\s+$/.test(p)) return frag.appendChild(document.createTextNode(p));
            const s = document.createElement("span");
            s.className = cls;
            s.textContent = p;
            frag.appendChild(s);
            out.push(s);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
    el.dataset.expSplit = cls;
    return out;
  }
  function typeOn(tl, el, at, o) {
    o = o || {};
    const chars = split(el, "chars");
    const step = o.perChar || 0.03;
    chars.forEach((c, i) => tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: FRAME }, at + i * step));
    return tl;
  }
  // WORD-POP: cada palabra entra con POP-IN. `times` = arreglo de tiempos (uno por palabra) o un
  // número inicial + stagger.
  function wordPop(tl, el, times, o) {
    o = o || {};
    const words = split(el, "words");
    words.forEach((w, i) => {
      const at = Array.isArray(times) ? times[Math.min(i, times.length - 1)] : times + i * (o.stagger || 0.12);
      popIn(tl, w, at, { dur: 0.3, rot: i % 2 ? 5 : -5 });
    });
    return tl;
  }
  function drawOn(tl, path, at, o) {
    o = o || {};
    arr(path).forEach((p) => {
      const len = p.getTotalLength ? p.getTotalLength() : 1000;
      tl.fromTo(p, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: o.dur || 0.5, ease: "power2.inOut", ...ir(o) }, at);
    });
    return tl;
  }
  // SPLAT: el elemento se infla y desaparece mientras salen partículas de su color.
  // `particles`: elementos ya puestos en el DOM (p. ej. 8 círculos) centrados sobre el objeto.
  function splat(tl, el, at, particles, o) {
    o = o || {};
    tl.to(arr(el), { scale: 1.3, opacity: 0, duration: 0.2, ease: "power2.out" }, at);
    if (particles) {
      const ps = arr(particles);
      const r = rng(o.seed || 7);
      ps.forEach((p, i) => {
        const ang = (i / ps.length) * Math.PI * 2 + r() * 0.5;
        const dist = (o.dist || 220) * (0.7 + r() * 0.6);
        tl.fromTo(p, { x: 0, y: 0, scale: 1, opacity: 1 }, { x: Math.cos(ang) * dist, y: Math.sin(ang) * dist, scale: 0, opacity: 0, duration: 0.35, ease: "power3.out" }, at);
      });
    }
    return tl;
  }

  // ---------------------------------------------------------------- énfasis
  function pulse(tl, el, at, o) {
    o = o || {};
    tl.to(arr(el), { scale: o.to || 1.08, duration: 0.09, ease: "power2.out" }, at);
    return tl.to(arr(el), { scale: 1, duration: 0.2, ease: "back.out(3)" }, at + 0.09);
  }
  function shake(tl, el, at, o) {
    o = o || {};
    const amp = o.amp || 10, dur = o.dur || 0.25, n = 6;
    arr(el).forEach((e) => {
      const w = e.offsetWidth || 100;
      const pct = (amp / w) * 100;
      for (let i = 0; i < n; i++) {
        tl.to(e, { xPercent: (i % 2 ? -1 : 1) * pct * (1 - i / n), duration: dur / n, ease: "none" }, at + (i * dur) / n);
      }
      tl.to(e, { xPercent: 0, duration: dur / n, ease: "none" }, at + dur);
    });
    return tl;
  }
  function wiggle(tl, el, at, o) {
    o = o || {};
    const a = o.deg || 4;
    [a, -a, a * 0.7, -a * 0.7, a * 0.4, 0].forEach((r, i) => tl.to(arr(el), { rotation: r, duration: 0.07, ease: "sine.inOut" }, at + i * 0.07));
    return tl;
  }
  // HIGHLIGHT: `bar` es un .hl-bar dentro de un .hl-wrap
  function highlight(tl, bar, at, o) {
    return tl.fromTo(arr(bar), { scaleX: 0 }, { scaleX: 1, duration: (o && o.dur) || 0.3, ease: "power2.out", ...ir(o) }, at);
  }
  // STRIKE: `bar` es un .strike-bar
  function strike(tl, bar, at, o) {
    return tl.fromTo(arr(bar), { scaleX: 0 }, { scaleX: 1, rotation: -6, duration: (o && o.dur) || 0.22, ease: "power3.out", ...ir(o) }, at);
  }
  // CAM-PUNCH sobre el .rig de una escena
  function camPunch(tl, rig, at, o) {
    o = o || {};
    tl.to(rig, { scale: 1 + (o.amt || 0.15), duration: 0.15, ease: "power3.out" }, at);
    return tl.to(rig, { scale: 1, duration: 0.45, ease: "back.out(2.2)" }, at + 0.15);
  }
  function flash(tl, chromeObj, at) {
    const f = chromeObj.flash || chromeObj;
    tl.set(f, { opacity: 1 }, at);
    return tl.set(f, { opacity: 0 }, at + 2 * FRAME);
  }
  function jiggleText(tl, el, at, o) {
    o = o || {};
    const chars = split(el, "chars");
    const dur = o.dur || 0.8;
    chars.forEach((c, i) => {
      const n = Math.max(1, Math.floor(dur / 0.1));
      for (let k = 0; k < n; k++) {
        tl.to(c, { y: ((k + i) % 2 ? -1 : 1) * (o.amp || 10), rotation: ((k + i) % 2 ? -1 : 1) * 6, duration: 0.1, ease: "sine.inOut" }, at + k * 0.1);
      }
      tl.to(c, { y: 0, rotation: 0, duration: 0.1 }, at + n * 0.1);
    });
    return tl;
  }

  // ---------------------------------------------------------------- transformaciones
  // MORPH: `a` se convierte en `b` (giro + escala cruzada con squash). Ambos en la misma posición.
  function morph(tl, a, b, at, o) {
    o = o || {};
    const d = o.dur || 0.4;
    tl.to(a, { scale: 0, rotation: 90, duration: d * 0.5, ease: "back.in(2)" }, at);
    tl.fromTo(b, { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: d * 0.6, ease: "back.out(2)", ...ir(o) }, at + d * 0.4);
    return tl;
  }
  // MULTIPLY: aparecen muchos clones (ya en el DOM) con stagger desde el centro del grupo.
  function multiply(tl, els, at, o) {
    o = o || {};
    return tl.fromTo(arr(els), { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2)", stagger: { each: o.stagger || 0.04, from: o.from || "center" }, ...ir(o) }, at);
  }
  function grow(tl, el, at, o) {
    o = o || {};
    return tl.fromTo(arr(el), { scaleY: 0, scaleX: 0.6, transformOrigin: o.origin || "50% 100%" },
      { scaleY: 1, scaleX: 1, duration: o.dur || 0.6, ease: "elastic.out(1, 0.55)", stagger: o.stagger || 0, ...ir(o) }, at);
  }
  function shrink(tl, el, at, o) {
    o = o || {};
    return tl.to(arr(el), { scale: o.to != null ? o.to : 0.5, duration: o.dur || 0.35, ease: "back.in(1.5)" }, at);
  }
  // FILL / DRAIN: `liquid` es un bloque con transform-origin abajo; from/to en 0..1
  function fill(tl, liquid, at, from, to, o) {
    o = o || {};
    return tl.fromTo(liquid, { scaleY: from, transformOrigin: "50% 100%" }, { scaleY: to, duration: o.dur || 0.8, ease: o.ease || "power2.out", ...ir(o) }, at);
  }
  // COUNT-UP / COUNT-DOWN con formato 18,250. o: {prefix, suffix, dur, decimals}
  function countUp(tl, el, at, from, to, o) {
    o = o || {};
    const fmt = (v) => (o.prefix || "") + Number(v).toLocaleString("en-US", { minimumFractionDigits: o.decimals || 0, maximumFractionDigits: o.decimals || 0 }) + (o.suffix || "");
    const st = { v: from };
    if (!o.chain) el.textContent = fmt(from);
    tl.fromTo(st, { v: from }, { v: to, duration: o.dur || 0.8, ease: "power2.out", onUpdate: () => (el.textContent = fmt(st.v)), ...ir(o) }, at);
    return pulse(tl, el, at + (o.dur || 0.8), { to: 1.12 });
  }
  function swap(tl, a, b, at, o) {
    o = o || {};
    const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    const dx = rb.left - ra.left, d = o.dur || 0.5, lift = o.lift || 160;
    tl.to(a, { x: "+=" + dx, duration: d, ease: "power2.inOut" }, at).to(a, { y: -lift, duration: d / 2, ease: "power2.out", yoyo: true, repeat: 1 }, at);
    tl.to(b, { x: "-=" + dx, duration: d, ease: "power2.inOut" }, at).to(b, { y: lift, duration: d / 2, ease: "power2.out", yoyo: true, repeat: 1 }, at);
    return tl;
  }
  // FLOW: cada elemento viaja de `from` a `to` ({x,y} relativos a su posición CSS) en arco.
  function flow(tl, els, at, from, to, o) {
    o = o || {};
    const d = o.dur || 0.6, lift = o.lift != null ? o.lift : 200;
    arr(els).forEach((e, i) => {
      const t0 = at + i * (o.stagger || 0.06);
      tl.fromTo(e, { x: from.x, opacity: 1 }, { x: to.x, duration: d, ease: "power1.inOut", ...ir(o) }, t0);
      const midY = Math.min(from.y, to.y) - lift;
      tl.fromTo(e, { y: from.y }, { y: midY, duration: d / 2, ease: "power2.out", ...ir(o) }, t0);
      tl.to(e, { y: to.y, duration: d / 2, ease: "power2.in" }, t0 + d / 2);
    });
    return tl;
  }

  // ---------------------------------------------------------------- ambiente
  // IDLE-BOB: flotan ±amp px en ciclos desfasados, de `from` a `to`. Usa yPercent.
  function idleBob(tl, els, from, to, o) {
    o = o || {};
    const amp = o.amp || 6, half = (o.cycle || 1.6) / 2;
    arr(els).forEach((e, i) => {
      const h = e.offsetHeight || 200;
      const pct = (amp / h) * 100;
      const t0 = from + ((i * 0.37) % half);
      const reps = Math.max(0, Math.floor((to - t0) / half) - 1);
      tl.fromTo(e, { yPercent: -pct }, { yPercent: pct, duration: half, ease: "sine.inOut", yoyo: true, repeat: reps, immediateRender: false }, t0);
    });
    return tl;
  }
  // BLINK: Moni parpadea cada 2–4 s (determinista por seed)
  function blink(tl, moniEl, from, to, o) {
    o = o || {};
    const lids = moniEl.querySelectorAll(".m-parpado");
    const r = rng(o.seed || 3);
    let t = from + 0.6 + r() * 1.2;
    while (t < to - 0.2) {
      tl.to(lids, { scaleY: 1, duration: 0.06, ease: "power1.in" }, t);
      tl.to(lids, { scaleY: 0, duration: 0.08, ease: "power1.out" }, t + 0.06);
      t += 2 + r() * 2;
    }
    return tl;
  }

  // ---------------------------------------------------------------- Moni
  const MONI_SVG =
    '<svg viewBox="-40 -40 280 280" xmlns="http://www.w3.org/2000/svg">' +
    '<g class="m-brazos" opacity="0">' +
    '<path d="M28 112 C0 100 -10 70 6 52 C14 44 26 48 30 58 C34 70 30 84 44 92" fill="#FFD23F" stroke="#141414" stroke-width="8" stroke-linejoin="round"/>' +
    '<path d="M172 112 C200 100 210 70 194 52 C186 44 174 48 170 58 C166 70 170 84 156 92" fill="#FFD23F" stroke="#141414" stroke-width="8" stroke-linejoin="round"/>' +
    "</g>" +
    '<circle cx="110" cy="110" r="82" fill="#141414"/>' +
    '<circle class="m-cuerpo" cx="100" cy="100" r="82" fill="#FFD23F" stroke="#141414" stroke-width="8"/>' +
    '<circle cx="100" cy="100" r="64" fill="none" stroke="#E0A800" stroke-width="5"/>' +
    '<path d="M48 70 Q58 44 86 34" fill="none" stroke="#FFF6E5" stroke-width="9" stroke-linecap="round" opacity="0.85"/>' +
    '<g class="m-cejas-miedo" opacity="0"><path d="M58 62 L86 70" stroke="#141414" stroke-width="7" stroke-linecap="round"/><path d="M142 62 L114 70" stroke="#141414" stroke-width="7" stroke-linecap="round"/></g>' +
    '<g class="m-cejas-arriba" opacity="0"><path d="M60 58 Q74 48 88 56" fill="none" stroke="#141414" stroke-width="7" stroke-linecap="round"/><path d="M112 56 Q126 48 140 58" fill="none" stroke="#141414" stroke-width="7" stroke-linecap="round"/></g>' +
    '<g class="m-ojo-izq"><ellipse cx="76" cy="88" rx="16" ry="20" fill="#fff" stroke="#141414" stroke-width="6"/><circle class="m-pupila" cx="79" cy="92" r="8" fill="#141414"/>' +
    '<ellipse class="m-parpado" cx="76" cy="88" rx="17" ry="21" fill="#FFD23F" stroke="#141414" stroke-width="6"/></g>' +
    '<g class="m-ojo-der"><ellipse cx="124" cy="88" rx="16" ry="20" fill="#fff" stroke="#141414" stroke-width="6"/><circle class="m-pupila" cx="127" cy="92" r="8" fill="#141414"/>' +
    '<ellipse class="m-parpado" cx="124" cy="88" rx="17" ry="21" fill="#FFD23F" stroke="#141414" stroke-width="6"/></g>' +
    '<path class="m-ojo-guino" d="M110 90 Q124 78 138 90" fill="none" stroke="#141414" stroke-width="7" stroke-linecap="round" opacity="0"/>' +
    '<g class="m-ojos-cerrados" opacity="0"><path d="M62 90 Q76 100 90 90" fill="none" stroke="#141414" stroke-width="7" stroke-linecap="round"/><path d="M110 90 Q124 100 138 90" fill="none" stroke="#141414" stroke-width="7" stroke-linecap="round"/></g>' +
    '<path class="m-boca-feliz" d="M74 120 Q100 152 126 120 Z" fill="#141414" stroke="#141414" stroke-width="6" stroke-linejoin="round"/>' +
    '<path class="m-boca-asustada" d="M76 132 q6 -8 12 0 t12 0 t12 0 t12 0" fill="none" stroke="#141414" stroke-width="6" stroke-linecap="round" opacity="0"/>' +
    '<ellipse class="m-boca-sorprendida" cx="100" cy="132" rx="11" ry="15" fill="#141414" opacity="0"/>' +
    '<ellipse class="m-boca-dormida" cx="100" cy="132" rx="6" ry="7" fill="#141414" opacity="0"/>' +
    '<g class="m-sudor" opacity="0"><path d="M156 52 q8 14 0 20 q-8 -6 0 -20" fill="#7FD3FF" stroke="#141414" stroke-width="4"/><path d="M168 78 q6 10 0 15 q-6 -5 0 -15" fill="#7FD3FF" stroke="#141414" stroke-width="4"/></g>' +
    '<g class="m-zzz" opacity="0" font-family="Bricolage Grotesque, sans-serif" font-weight="800" fill="#141414"><text x="150" y="40" font-size="34">z</text><text x="172" y="14" font-size="26">z</text></g>' +
    "</svg>";
  const PARTS = ["m-brazos", "m-cejas-miedo", "m-cejas-arriba", "m-ojo-izq", "m-ojo-der", "m-ojo-guino", "m-ojos-cerrados",
    "m-boca-feliz", "m-boca-asustada", "m-boca-sorprendida", "m-boca-dormida", "m-sudor", "m-zzz"];
  const EXPR = {
    feliz: ["m-ojo-izq", "m-ojo-der", "m-boca-feliz"],
    asustada: ["m-ojo-izq", "m-ojo-der", "m-cejas-miedo", "m-boca-asustada", "m-sudor"],
    sorprendida: ["m-ojo-izq", "m-ojo-der", "m-cejas-arriba", "m-boca-sorprendida"],
    guino: ["m-ojo-izq", "m-ojo-guino", "m-boca-feliz"],
    dormida: ["m-ojos-cerrados", "m-boca-dormida", "m-zzz"],
    musculosa: ["m-ojo-izq", "m-ojo-der", "m-boca-feliz", "m-brazos", "m-cejas-arriba"],
  };
  function setExprNow(el, expr) {
    const on = EXPR[expr];
    PARTS.forEach((p) => el.querySelectorAll("." + p).forEach((n) => n.setAttribute("opacity", on.includes(p) ? "1" : "0")));
  }
  // Monta Moni dentro de cada elemento [data-moni="expresión"] (o el que le pases).
  function mountMoni(root) {
    (root || document).querySelectorAll("[data-moni]").forEach((el) => {
      if (el.querySelector("svg")) return;
      el.classList.add("moni");
      el.innerHTML = MONI_SVG;
      setExprNow(el, el.dataset.moni || "feliz");
      gsap.set(el.querySelectorAll(".m-parpado"), { scaleY: 0, transformOrigin: "50% 0%" });
    });
  }
  // Cambia la expresión de Moni en `at`, con un saltito para que se note.
  function moni(tl, el, expr, at) {
    if (!EXPR[expr]) throw new Error("EXP: expresión de Moni desconocida: " + expr);
    const on = EXPR[expr];
    PARTS.forEach((p) => {
      const nodes = el.querySelectorAll("." + p);
      if (nodes.length) tl.set(nodes, { attr: { opacity: on.includes(p) ? 1 : 0 } }, at);
    });
    const svg = el.querySelector("svg");
    tl.to(svg, { scaleX: 1.1, scaleY: 0.9, duration: 0.06, transformOrigin: "50% 100%" }, at);
    tl.to(svg, { scaleX: 1, scaleY: 1, duration: 0.2, ease: "back.out(3)" }, at + 0.06);
    return tl;
  }

  // ---------------------------------------------------------------- objetos comunes (SVG)
  const OBJ = {
    check: '<svg class="check" viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="#1FCB7A" stroke="#141414" stroke-width="8"/><path class="draw" d="M34 62 L52 80 L88 42" fill="none" stroke="#141414" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    equis: '<svg class="check" viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" fill="#FF4B4B" stroke="#141414" stroke-width="8"/><path class="draw" d="M40 40 L80 80 M80 40 L40 80" fill="none" stroke="#141414" stroke-width="12" stroke-linecap="round"/></svg>',
    moneda: '<svg viewBox="0 0 100 100" width="100" height="100"><circle cx="54" cy="54" r="40" fill="#141414"/><circle cx="50" cy="50" r="40" fill="#FFD23F" stroke="#141414" stroke-width="6"/><text x="50" y="66" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="46" fill="#141414">$</text></svg>',
  };
  function mountObjs(root) {
    (root || document).querySelectorAll("[data-obj]").forEach((el) => {
      if (!el.firstElementChild && OBJ[el.dataset.obj]) el.innerHTML = OBJ[el.dataset.obj];
    });
  }

  // Monta todo lo declarativo de una composición (Moni, objetos).
  function setup(root) {
    mountMoni(root);
    mountObjs(root);
  }

  window.EXP = {
    T, beat, word, q, qa, rng, split, setup, scene, chrome,
    popIn, popOut, dropIn, slideIn, stamp, typeOn, wordPop, drawOn, splat,
    pulse, shake, wiggle, highlight, strike, camPunch, flash, jiggleText,
    morph, multiply, grow, shrink, fill, countUp, swap, flow,
    idleBob, blink, moni, mountMoni, OBJ, EXPR,
  };
})();
