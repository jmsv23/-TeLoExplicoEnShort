/* Complemento VERTICAL del kit cómic (ver comic-v.css): COM.sello, COM.progress (no-op), COM.datoCounter (no-op). */
(function () {
  const arr = (el) => (el && el.length !== undefined && !el.nodeType ? Array.from(el) : [el]).filter(Boolean);
  function sello(tl, el, at, o) {
    o = o || {};
    const rot = o.rot != null ? o.rot : -8;
    arr(el).forEach((e) => {
      tl.fromTo(e, { scale: 2.6, rotation: rot - 10, opacity: 0 }, { scale: 1, rotation: rot, opacity: 1, duration: 0.18, ease: "power4.in" }, at);
      tl.fromTo(e, { x: -6 }, { x: 0, duration: 0.12, ease: "power2.out", immediateRender: false }, at + 0.18);
    });
    return tl;
  }
  const noop = (tl) => tl;
  if (!COM.sello) COM.sello = sello;
  if (!COM.progress) COM.progress = noop;
  if (!COM.datoCounter) COM.datoCounter = noop;
})();
