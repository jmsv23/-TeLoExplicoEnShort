/* window.COM.OBJ: objetos SVG de cómic para la serie "Camino a Doomsday" (ver ../../camino-a-doomsday/_estilo.md).
   Cada objeto es una FUNCIÓN (opts) que devuelve un string SVG; el contenedor (px) define el tamaño.
   Se monta con COM.mount(root) sobre elementos <div data-com="nombre" data-opts='{"…":"…"}'></div>.
   No toca window.COM si ya existe (comic.js lo complementa): aquí solo se agregan OBJ y mount.
   Reglas: seek-safe (sin Math.random, sin Date.now, sin repeat:-1, sin CSS animado);
   tinta #0B0B14 en contornos de 8 px (6 en detalles), rellenos planos de la paleta, sin degradados ni blur;
   sombra dura = copia del contorno desplazada (8,8) rellena de tinta, detrás del objeto;
   trama Ben-Day con <pattern> (ids únicos por instancia vía contador uid). */
(function () {
  "use strict";

  var INK = "#0B0B14", PAPEL = "#FFF3D6", HEROE = "#1E5BFF", ROJO = "#E8212B", AMAR = "#FFD400",
      DOOM = "#1FA85A", DOOM_O = "#0E5C32", MULTI = "#8A2BE2", MULTI_O = "#4B1580",
      CIEN = "#00C8E8", CENI = "#6B7280", OJOS_DOOM = "#D8FF3D",
      CENI_CLARO = "#98A2B0", BLANCO = "#FFFFFF";
  let uid = 0;

  /* trazo de tinta: w px, esquinas y capas redondeadas */
  function S(w) { return 'stroke="' + INK + '" stroke-width="' + w + '" stroke-linejoin="round" stroke-linecap="round"'; }
  /* envoltura de cada SVG */
  function svg(vb, inner) {
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + vb + '" style="width:100%;height:100%;overflow:visible;display:block">' + inner + "</svg>";
  }
  /* sombra dura: silueta desplazada (8,8), detrás de todo */
  function sh(d) { return '<path d="' + d + '" transform="translate(8 8)" fill="' + INK + '"/>'; }
  /* trama de puntos Ben-Day (ids únicos por instancia) */
  function bday(id) {
    return '<pattern id="com-bd-' + id + '" width="16" height="16" patternUnits="userSpaceOnUse">' +
      '<circle cx="4" cy="4" r="3" fill="' + INK + '"/><circle cx="12" cy="12" r="3" fill="' + INK + '"/></pattern>';
  }
  function bdRef(id) { return 'url(#com-bd-' + id + ')'; }
  /* rng determinista local (sin Math.random): mulberry32 */
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  /* letras en bloque para camisetas: "A" | "D" → path (fill-rule evenodd), centrada en (cx,cy), alto h */
  function letraPath(l, cx, cy, h) {
    if (l === "D") {
      return "M" + (cx - 0.30 * h) + " " + (cy - 0.5 * h) + " L" + (cx + 0.02 * h) + " " + (cy - 0.5 * h) +
        " A" + (0.30 * h) + " " + (0.5 * h) + " 0 0 1 " + (cx + 0.02 * h) + " " + (cy + 0.5 * h) +
        " L" + (cx - 0.30 * h) + " " + (cy + 0.5 * h) + " Z " +
        "M" + (cx - 0.16 * h) + " " + (cy - 0.32 * h) + " L" + (cx - 0.02 * h) + " " + (cy - 0.32 * h) +
        " A" + (0.18 * h) + " " + (0.32 * h) + " 0 0 1 " + (cx - 0.02 * h) + " " + (cy + 0.32 * h) +
        " L" + (cx - 0.16 * h) + " " + (cy + 0.32 * h) + " Z";
    }
    /* "A" por defecto */
    return "M" + (cx - 0.42 * h) + " " + (cy + 0.5 * h) + " L" + (cx - 0.16 * h) + " " + (cy - 0.5 * h) +
      " L" + (cx + 0.16 * h) + " " + (cy - 0.5 * h) + " L" + (cx + 0.42 * h) + " " + (cy + 0.5 * h) +
      " L" + (cx + 0.15 * h) + " " + (cy + 0.5 * h) + " L" + (cx + 0.09 * h) + " " + (cy + 0.16 * h) +
      " L" + (cx - 0.09 * h) + " " + (cy + 0.16 * h) + " L" + (cx - 0.15 * h) + " " + (cy + 0.5 * h) + " Z " +
      "M" + (cx - 0.10 * h) + " " + (cy + 0.02 * h) + " L" + cx + " " + (cy - 0.20 * h) +
      " L" + (cx + 0.10 * h) + " " + (cy + 0.02 * h) + " Z";
  }
  function letra(l, cx, cy, h, fill) {
    return '<path d="' + letraPath(l || "A", cx, cy, h) + '" fill-rule="evenodd" fill="' + (fill || BLANCO) + '" ' + S(6) + "/>";
  }
  /* camiseta compartida: la usa COM.OBJ.jersey (300×320) y el pecho de player */
  function jerseyShape(w, h) { /* silueta de camiseta en caja w×h */
    var sw = w * 0.28; // ancho de manga
    return {
      cuerpo: "M" + (0.18 * w) + " " + (0.16 * h) + " L" + (0.82 * w) + " " + (0.16 * h) +
        " L" + w + " " + (0.38 * h) + " L" + (0.86 * w) + " " + (0.50 * h) + " L" + (0.78 * w) + " " + (0.42 * h) +
        " L" + (0.78 * w) + " " + (0.92 * h) + " C" + (0.78 * w) + " " + h + " " + (0.22 * w) + " " + h + " " + (0.22 * w) + " " + (0.92 * h) +
        " L" + (0.22 * w) + " " + (0.42 * h) + " L" + (0.14 * w) + " " + (0.50 * h) + " L0 " + (0.38 * h) + " Z",
      cuello: "M" + (0.42 * w) + " " + (0.16 * h) + " Q" + (0.5 * w) + " " + (0.30 * h) + " " + (0.58 * w) + " " + (0.16 * h),
      sw: sw
    };
  }

  /* ================= 1. kang: busto de villano genérico (armadura multi-oscuro) ================= */
  function kang() {
    var id = ++uid;
    var spikes = "M120 78 L138 16 L168 74 Z M175 72 L200 8 L226 72 Z M234 74 L262 20 L280 78 Z";
    var helmet = "M100 150 L112 60 L288 60 L300 150 L292 252 L268 312 L132 312 L108 252 Z";
    var finL = "M100 200 L34 84 L96 232 Z", finR = "M300 200 L366 84 L304 232 Z";
    var cuerpo = "M140 312 L260 312 L268 352 L342 382 L360 472 L360 500 L40 500 L40 472 L58 382 L132 352 Z";
    return svg("0 0 400 500",
      '<defs>' + bday(id) + "</defs>" +
      sh(spikes + " " + helmet + " " + finL + " " + finR + " " + cuerpo) +
      '<g class="k-cuerpo">' +
      '<path d="' + spikes + '" fill="' + MULTI_O + '" ' + S(6) + "/>" +
      '<path d="' + finL + finR + '" fill="' + MULTI + '" ' + S(6) + "/>" +
      '<path d="' + helmet + '" fill="' + MULTI_O + '" ' + S(8) + "/>" +
      '<path d="' + cuerpo + '" fill="' + MULTI_O + '" ' + S(8) + "/>" +
      /* detalles multi: placa del pecho y líneas de panel */
      '<path d="M200 372 L246 402 L200 462 L154 402 Z" fill="' + MULTI + '" ' + S(6) + "/>" +
      '<path d="M126 390 L146 420 M274 390 L254 420" stroke="' + MULTI + '" stroke-width="6" stroke-linecap="round" fill="none"/>' +
      '<path d="M170 120 L230 120 M148 160 L252 160" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      "</g>" +
      /* ranura de ojos brillante (dos rects amarillos) */
      '<g class="k-ojos">' +
      '<rect x="138" y="202" width="54" height="30" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="208" y="202" width="54" height="30" fill="' + AMAR + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 2. iron: casco de Iron Man (solo casco, frente) ================= */
  function iron() {
    var id = ++uid;
    var casco = "M95 190 C95 88 142 40 200 40 C258 40 305 88 305 190 L305 300 C305 382 268 432 200 448 C132 432 95 382 95 300 Z";
    var placa = "M132 128 L268 128 L276 244 C276 334 242 402 200 424 C158 402 124 334 124 244 Z";
    return svg("0 0 400 480",
      '<defs>' + bday(id) + "</defs>" +
      sh(casco) +
      '<g class="i-casco">' +
      '<path d="' + casco + '" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<path d="' + placa + '" fill="' + AMAR + '" ' + S(8) + "/>" +
      /* líneas de panel: cresta y laterales */
      '<path d="M200 42 L200 126 M150 58 L112 126 M250 58 L288 126 M200 250 L200 330" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      /* ranura de boca */
      '<rect x="176" y="338" width="48" height="14" rx="6" fill="' + INK + '"/>' +
      "</g>" +
      /* ranuras de ojos ciencia, anguladas */
      '<g class="i-ojos">' +
      '<path d="M148 240 L196 224 L200 250 L152 262 Z" fill="' + CIEN + '" ' + S(6) + "/>" +
      '<path d="M252 240 L204 224 L200 250 L248 262 Z" fill="' + CIEN + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 3. doom: busto de Doctor Doom en contrapicado (el objeto clave) =================
     Orden: d-capa → torso/hombreras (sin clase, no se animan) → d-capucha → d-mascara → d-ojos. */
  function doom() {
    var id = ++uid;
    var capa = "M250 190 C170 205 120 250 100 320 C85 380 75 470 70 592 L150 546 L196 606 L250 572 L304 606 L350 546 L430 592 C425 470 415 380 400 320 C380 250 330 205 250 190 Z";
    var torso = "M250 430 L195 448 L185 600 L315 600 L305 448 Z";
    var homL = "M195 445 L110 470 L80 556 L118 600 L206 586 L216 500 Z";
    var homR = "M305 445 L390 470 L420 556 L382 600 L294 586 L284 500 Z";
    var capucha = "M250 48 C158 48 108 128 102 236 C98 326 135 422 250 444 C365 422 402 326 398 236 C392 128 342 48 250 48 Z";
    var interior = "M250 88 C182 88 142 156 138 242 C135 316 168 392 250 404 C332 392 365 316 362 242 C358 156 318 88 250 88 Z";
    var mascara = "M250 105 C198 105 165 140 158 196 L150 272 C146 352 180 414 250 422 C320 414 354 352 350 272 L342 196 C335 140 302 105 250 105 Z";
    var ojoL = "M162 215 L232 232 L228 258 L158 246 Z";
    var ojoR = "M338 215 L268 232 L272 258 L342 246 Z";
    return svg("0 0 500 620",
      '<defs>' + bday(id) + "</defs>" +
      '<g class="d-capa">' +
      sh(capa) +
      '<path d="' + capa + '" fill="' + DOOM_O + '" ' + S(8) + "/>" +
      '<path d="M212 244 L184 520 M250 218 L250 540 M288 244 L316 520" stroke="' + INK + '" stroke-width="6" fill="none" opacity="0.55"/>' +
      "</g>" +
      /* torso y hombreras de armadura (estáticos) */
      '<path d="' + torso + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<path d="M250 456 L250 594 M212 470 L212 588 M288 470 L288 588" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      '<path d="' + homL + homR + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<circle cx="120" cy="552" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="170" cy="544" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="380" cy="552" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="330" cy="544" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      /* capucha: exterior doom + interior oscuro */
      '<g class="d-capucha">' +
      '<path d="' + capucha + '" fill="' + DOOM + '" ' + S(8) + "/>" +
      '<path d="' + interior + '" fill="' + DOOM_O + '" ' + S(6) + "/>" +
      "</g>" +
      /* máscara de metal */
      '<g class="d-mascara">' +
      '<path d="' + mascara + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<path d="M205 145 L295 145 L288 192 L212 192 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M172 226 L214 216 L208 302 L178 296 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M328 226 L286 216 L292 302 L322 296 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M216 332 L284 332 L279 392 L221 392 Z" fill="' + CENI_CLARO + '"/>' +
      /* rendijas de nariz y boca */
      '<rect x="239" y="262" width="9" height="26" fill="' + INK + '"/>' +
      '<rect x="252" y="262" width="9" height="26" fill="' + INK + '"/>' +
      '<rect x="210" y="332" width="80" height="26" rx="5" fill="' + INK + '"/>' +
      /* remaches */
      '<circle cx="172" cy="250" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="328" cy="250" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="250" cy="136" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="198" cy="396" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="302" cy="396" r="7" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      "</g>" +
      /* ranuras de ojos duras y brillantes */
      '<g class="d-ojos">' +
      '<path d="' + ojoL + '" fill="' + OJOS_DOOM + '" ' + S(8) + "/>" +
      '<path d="' + ojoR + '" fill="' + OJOS_DOOM + '" ' + S(8) + "/>" +
      "</g>");
  }

  /* ================= 4. doomMask: solo la máscara, de frente ================= */
  function doomMask() {
    var id = ++uid;
    var mascara = "M180 95 C128 95 98 128 92 180 L85 254 C81 328 112 384 180 394 C248 384 279 328 275 254 L268 180 C262 128 232 95 180 95 Z";
    return svg("0 0 360 420",
      '<defs>' + bday(id) + "</defs>" +
      sh(mascara) +
      '<g class="d-mascara">' +
      '<path d="' + mascara + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<path d="M138 132 L222 132 L216 176 L144 176 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M104 206 L146 196 L140 278 L110 272 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M256 206 L214 196 L220 278 L250 272 Z" fill="' + CENI_CLARO + '"/>' +
      '<path d="M148 292 L212 292 L207 350 L153 350 Z" fill="' + CENI_CLARO + '"/>' +
      '<rect x="171" y="236" width="8" height="24" fill="' + INK + '"/>' +
      '<rect x="181" y="236" width="8" height="24" fill="' + INK + '"/>' +
      '<rect x="143" y="296" width="74" height="24" rx="5" fill="' + INK + '"/>' +
      '<circle cx="106" cy="226" r="6" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="254" cy="226" r="6" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="180" cy="112" r="6" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="132" cy="362" r="6" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      '<circle cx="228" cy="362" r="6" fill="' + CENI_CLARO + '" ' + S(4) + "/>" +
      "</g>" +
      '<g class="d-ojos">' +
      '<path d="M96 188 L162 204 L158 228 L92 218 Z" fill="' + OJOS_DOOM + '" ' + S(8) + "/>" +
      '<path d="M264 188 L198 204 L202 228 L268 218 Z" fill="' + OJOS_DOOM + '" ' + S(8) + "/>" +
      "</g>");
  }

  /* ================= 5. crown: corona de picos amarilla con joyas rojas ================= */
  function crown() {
    var d = "M30 152 L62 40 L112 112 L160 28 L208 112 L258 40 L290 152 Z M30 152 L290 152 L290 200 L30 200 Z";
    return svg("0 0 320 220",
      sh(d) +
      '<path d="' + d + '" fill="' + AMAR + '" ' + S(8) + "/>" +
      '<circle cx="95" cy="176" r="13" fill="' + ROJO + '" ' + S(6) + "/>" +
      '<circle cx="160" cy="176" r="13" fill="' + ROJO + '" ' + S(6) + "/>" +
      '<circle cx="225" cy="176" r="13" fill="' + ROJO + '" ' + S(6) + "/>");
  }

  /* ================= 6. castle: castillo de Latveria ================= */
  function castle() {
    var id = ++uid;
    var torreL = "M60 210 L140 210 L140 440 L60 440 Z";
    var techoL = "M48 210 L152 210 L100 96 Z";
    var torreR = "M380 210 L460 210 L460 440 L380 440 Z";
    var techoR = "M368 210 L472 210 L420 96 Z";
    var torreC = "M225 80 L295 80 L295 154 L225 154 Z";
    var techoC = "M213 80 L307 80 L260 38 Z";
    var alcazar = "M180 152 L180 118 L208 118 L208 136 L234 136 L234 118 L260 118 L260 136 L286 136 L286 118 L314 118 L314 136 L340 136 L340 152 L340 440 L180 440 Z";
    var bandera = "M260 40 L260 8 M260 8 L318 16 L260 34";
    return svg("0 0 520 440",
      '<defs>' + bday(id) + "</defs>" +
      sh(torreL + " " + techoL + " " + torreR + " " + techoR + " " + torreC + " " + techoC + " " + alcazar) +
      /* bandera con L (parte c-bandera) */
      '<g class="c-bandera">' +
      '<path d="M260 44 L260 8" stroke="' + INK + '" stroke-width="6" stroke-linecap="round" fill="none"/>' +
      '<path d="M262 8 L318 16 L262 34 Z" fill="' + ROJO + '" ' + S(6) + "/>" +
      '<path d="M276 13 L276 28 L292 28" stroke="' + INK + '" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</g>" +
      '<path d="' + torreL + torreR + torreC + alcazar + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<path d="' + techoL + techoR + techoC + '" fill="' + DOOM + '" ' + S(8) + "/>" +
      /* ventanas amarillas */
      '<rect x="88" y="258" width="22" height="36" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="410" y="258" width="22" height="36" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="198" y="200" width="20" height="32" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="250" y="196" width="20" height="38" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="302" y="200" width="20" height="32" fill="' + AMAR + '" ' + S(6) + "/>" +
      '<rect x="250" y="98" width="18" height="26" fill="' + AMAR + '" ' + S(6) + "/>" +
      /* puerta en arco */
      '<path d="M235 440 L235 362 C235 332 285 332 285 362 L285 440 Z" fill="' + INK + '" ' + S(6) + "/>" +
      /* líneas de piedra */
      '<path d="M64 300 L136 300 M64 352 L136 352 M384 300 L456 300 M384 352 L456 352 M184 330 L336 330" stroke="' + INK + '" stroke-width="4" fill="none" opacity="0.45"/>');
  }

  /* ================= 7. gearAtom: engranaje ciencia con átomo ================= */
  function gearAtom() {
    var id = ++uid;
    var R1 = 192, R2 = 156, N = 8, paso = 2 * Math.PI / N, pts = [];
    for (var i = 0; i < N; i++) {
      var a = i * paso;
      pts.push([a - 0.11, R1], [a + 0.11, R1], [a + 0.11, R2], [a + paso - 0.11, R2]);
    }
    var d = pts.map(function (p, k) {
      var x = 200 + p[1] * Math.cos(p[0]), y = 200 + p[1] * Math.sin(p[0]);
      return (k ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1);
    }).join(" ") + " Z";
    return svg("0 0 400 400",
      '<defs>' + bday(id) + "</defs>" +
      '<g class="g-engranaje">' +
      sh(d) +
      '<path d="' + d + '" fill="' + CIEN + '" ' + S(8) + "/>" +
      '<circle cx="200" cy="200" r="118" fill="' + PAPEL + '" ' + S(8) + "/>" +
      "</g>" +
      '<g class="g-atomo">' +
      '<g transform="rotate(0 200 200)"><ellipse cx="200" cy="200" rx="98" ry="30" fill="none" ' + S(6) + "/>" +
      '<circle cx="' + (200 + 98 * Math.cos(0.7)).toFixed(1) + '" cy="' + (200 + 30 * Math.sin(0.7)).toFixed(1) + '" r="9" fill="' + INK + '"/></g>' +
      '<g transform="rotate(60 200 200)"><ellipse cx="200" cy="200" rx="98" ry="30" fill="none" ' + S(6) + "/></g>" +
      '<g transform="rotate(120 200 200)"><ellipse cx="200" cy="200" rx="98" ry="30" fill="none" ' + S(6) + "/>" +
      '<circle cx="' + (200 + 98 * Math.cos(2.4)).toFixed(1) + '" cy="' + (200 + 30 * Math.sin(2.4)).toFixed(1) + '" r="9" fill="' + INK + '"/></g>' +
      '<circle cx="200" cy="200" r="22" fill="' + ROJO + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 8. runes: círculo mágico multi con pentagrama y runas ================= */
  function runes() {
    var id = ++uid, cx = 200, cy = 200;
    /* pentagrama: puntos a r132 conectados cada 2 */
    var P = [];
    for (var k = 0; k < 5; k++) {
      var ang = (-90 + k * 72) * Math.PI / 180;
      P.push([cx + 132 * Math.cos(ang), cy + 132 * Math.sin(ang)]);
    }
    var estrella = "M" + P[0].map(function (v) { return v.toFixed(1); }).join(" ") +
      " L" + P[2].map(function (v) { return v.toFixed(1); }).join(" ") +
      " L" + P[4].map(function (v) { return v.toFixed(1); }).join(" ") +
      " L" + P[1].map(function (v) { return v.toFixed(1); }).join(" ") +
      " L" + P[3].map(function (v) { return v.toFixed(1); }).join(" ") + " Z";
    /* 12 runas rectas sobre la banda multi */
    var runas = "";
    for (var i = 0; i < 12; i++) {
      var a = (i * 30 + 15) * Math.PI / 180, t = i % 3;
      var r0 = 158, r1 = 182, rm = 170;
      var dir = [Math.cos(a), Math.sin(a)], per = [-Math.sin(a), Math.cos(a)];
      var p0 = [cx + r0 * dir[0], cy + r0 * dir[1]], p1 = [cx + r1 * dir[0], cy + r1 * dir[1]];
      var pm = [cx + rm * dir[0], cy + rm * dir[1]];
      if (t === 0) runas += '<path d="M' + p0.map(function (v) { return v.toFixed(1); }).join(" ") + " L" + p1.map(function (v) { return v.toFixed(1); }).join(" ") + '" stroke="' + PAPEL + '" stroke-width="6" stroke-linecap="round" fill="none"/>';
      else if (t === 1) runas += '<path d="M' + (pm[0] - 14 * per[0]).toFixed(1) + " " + (pm[1] - 14 * per[1]).toFixed(1) + " L" + (pm[0] + 14 * per[0]).toFixed(1) + " " + (pm[1] + 14 * per[1]).toFixed(1) + '" stroke="' + PAPEL + '" stroke-width="6" stroke-linecap="round" fill="none"/>';
      else runas += '<path d="M' + p0.map(function (v) { return v.toFixed(1); }).join(" ") + " L" + pm.map(function (v) { return v.toFixed(1); }).join(" ") + " L" + (pm[0] + 10 * per[0]).toFixed(1) + " " + (pm[1] + 10 * per[1]).toFixed(1) + '" stroke="' + PAPEL + '" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>';
    }
    return svg("0 0 400 400",
      '<defs>' + bday(id) + "</defs>" +
      '<g class="r-circulo">' +
      '<circle cx="200" cy="200" r="192" fill="none" ' + S(8) + "/>" +
      '<circle cx="200" cy="200" r="170" fill="none" stroke="' + MULTI + '" stroke-width="24"/>' +
      '<circle cx="200" cy="200" r="158" fill="none" ' + S(8) + "/>" +
      '<path d="' + estrella + '" fill="none" ' + S(8) + "/>" +
      runas +
      "</g>" +
      /* brillo plano amarillo en el centro (círculos concéntricos, sin blur) */
      '<g class="r-brillo">' +
      '<circle cx="200" cy="200" r="72" fill="' + AMAR + '" opacity="0.25"/>' +
      '<circle cx="200" cy="200" r="48" fill="' + AMAR + '" opacity="0.45"/>' +
      '<circle cx="200" cy="200" r="26" fill="' + AMAR + '" opacity="0.9"/>' +
      '<circle cx="200" cy="200" r="11" fill="' + BLANCO + '"/>' +
      "</g>");
  }

  /* ================= 9. fourEmblem: emblema del 4 sobre órbita ================= */
  function fourEmblem() {
    var id = ++uid;
    var cuatro = "M205 75 L250 75 L250 290 L205 290 L205 235 L95 235 L95 190 L205 75 Z M130 190 L205 112 L205 190 Z";
    return svg("0 0 360 360",
      '<defs>' + bday(id) + "</defs>" +
      sh("M180 48 A132 132 0 1 0 180.1 48 Z") +
      '<ellipse cx="180" cy="180" rx="168" ry="58" fill="none" ' + S(8) + ' transform="rotate(-18 180 180)"/>' +
      '<g class="f-cuatro">' +
      '<circle cx="180" cy="180" r="132" fill="' + HEROE + '" ' + S(8) + "/>" +
      '<path d="' + cuatro + '" fill-rule="evenodd" fill="' + BLANCO + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 10. comicOpen: cómic abierto de frente ================= */
  function comicOpen() {
    var id = ++uid;
    var izq = "M350 66 C260 46 120 44 60 62 L60 458 C130 474 280 474 350 462 Z";
    var der = "M350 66 C440 46 580 44 640 62 L640 458 C570 474 420 474 350 462 Z";
    return svg("0 0 700 520",
      '<defs>' + bday(id) + "</defs>" +
      sh(izq + " " + der) +
      '<g class="co-izq">' +
      '<path d="' + izq + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M342 78 C338 84 336 92 336 104 L336 424 C336 438 340 450 348 460 Z" fill="' + bdRef(id) + '"/>' +
      '<rect x="95" y="105" width="205" height="140" fill="' + BLANCO + '" ' + S(6) + "/>" +
      '<rect x="95" y="272" width="205" height="158" fill="' + BLANCO + '" ' + S(6) + "/>" +
      "</g>" +
      '<g class="co-der">' +
      '<path d="' + der + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M358 78 C362 84 364 92 364 104 L364 424 C364 438 360 450 352 460 Z" fill="' + bdRef(id) + '"/>' +
      '<rect x="400" y="105" width="205" height="140" fill="' + BLANCO + '" ' + S(6) + "/>" +
      '<rect x="400" y="272" width="205" height="158" fill="' + BLANCO + '" ' + S(6) + "/>" +
      "</g>" +
      '<path d="M350 66 L350 462" stroke="' + INK + '" stroke-width="8" fill="none"/>' +
      /* rects de referencia para poner objetos encima (invisibles) */
      '<rect class="co-izq-zona" x="95" y="105" width="205" height="325" fill="none"/>' +
      '<rect class="co-der-zona" x="400" y="105" width="205" height="325" fill="none"/>');
  }

  /* ================= 11. player: futbolista cuerpo completo, patada de tres cuartos =================
     opts.color: "heroe" (por defecto) | "doom" · opts.letra: "A" | "D".
     Cabeza LISA: óvalo papel sin rasgos, trama Ben-Day en el lado de la sombra.
     Pecho usa la misma forma que COM.OBJ.jersey (para el SWAP de camisetas). */
  function player(opts) {
    var id = ++uid;
    opts = opts || {};
    var color = opts.color === "doom" ? DOOM : HEROE;
    var letraN = opts.letra === "D" ? "D" : "A";
    var cabeza = "M185 42 C220 42 233 68 233 98 C233 128 220 154 185 154 C150 154 137 128 137 98 C137 68 150 42 185 42 Z";
    var cuello = "M172 150 L198 150 L202 182 L168 182 Z";
    var torso = "M128 192 L250 186 L262 330 L140 338 Z";
    var mangaL = "M128 202 L94 256 L120 278 L150 246 Z";
    var anteL = "M94 256 L120 278 L100 334 L74 312 Z";
    var mangaR = "M248 192 L300 172 L310 204 L256 224 Z";
    var anteR = "M300 172 L330 118 L306 106 L280 168 Z";
    var shorts = "M140 338 L262 330 L272 420 L215 428 L200 392 L188 428 L128 420 Z";
    var muslo = "M215 420 L270 434 L288 472 L232 464 Z";
    var espinilla = "M278 464 L312 450 L336 548 L306 556 Z";
    var botaK = "M304 540 L354 528 L370 560 L322 578 L296 560 Z";
    var pierna = "M146 428 L176 428 L172 590 L142 590 Z";
    var botaP = "M128 590 L176 590 L184 626 L112 626 C104 626 108 590 128 590 Z";
    return svg("0 0 380 700",
      "<defs>" + bday(id) + "</defs>" +
      sh(cabeza + " " + torso + " " + shorts + " " + pierna + " " + botaP + " " + espinilla + " " + botaK) +
      '<g class="p-cuerpo">' +
      '<path d="' + cuello + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      /* brazo trasero (detrás del torso) */
      '<path d="' + mangaL + '" fill="' + color + '" ' + S(8) + "/>" +
      '<path d="' + anteL + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<circle cx="87" cy="326" r="13" fill="' + PAPEL + '" ' + S(6) + "/>" +
      "</g>" +
      /* cabeza lisa (sin rasgos) */
      '<g class="p-cabeza">' +
      '<path d="' + cabeza + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M185 42 C220 42 233 68 233 98 C233 128 220 154 185 154 C206 140 213 122 213 98 C213 74 206 56 185 42 Z" fill="' + bdRef(id) + '"/>' +
      "</g>" +
      /* brazo delantero levantado */
      '<path d="' + mangaR + '" fill="' + color + '" ' + S(8) + "/>" +
      '<path d="' + anteR + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<circle cx="318" cy="108" r="13" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<g class="p-camiseta">' +
      '<path d="' + torso + '" fill="' + color + '" ' + S(8) + "/>" +
      letra(letraN, 195, 264, 92, BLANCO) +
      "</g>" +
      '<g class="p-cuerpo">' +
      /* pierna de apoyo */
      '<path d="' + pierna + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<rect x="138" y="556" width="38" height="12" fill="' + INK + '"/>' +
      '<path d="' + botaP + '" fill="' + INK + '" ' + S(6) + "/>" +
      '<path d="' + shorts + '" fill="' + INK + '" ' + S(8) + "/>" +
      "</g>" +
      /* pierna de patada */
      '<g class="p-pierna-patada">' +
      '<path d="' + muslo + '" fill="' + INK + '" ' + S(8) + "/>" +
      '<path d="' + espinilla + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<path d="M302 522 L334 512 L336 526 L304 536 Z" fill="' + INK + '"/>' +
      '<path d="' + botaK + '" fill="' + INK + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 12. jersey: camiseta suelta (para SWAP) ================= */
  function jersey(opts) {
    opts = opts || {};
    var color = opts.color === "doom" ? DOOM : HEROE;
    var letraN = opts.letra === "D" ? "D" : "A";
    var j = jerseyShape(300, 320);
    return svg("0 0 300 320",
      sh(j.cuerpo) +
      '<g class="j-camiseta">' +
      '<path d="' + j.cuerpo + '" fill="' + color + '" ' + S(8) + "/>" +
      '<path d="' + j.cuello + '" fill="none" ' + S(6) + "/>" +
      '<path d="M120 60 Q150 84 180 60 L180 74 Q150 98 120 74 Z" fill="' + BLANCO + '" ' + S(6) + "/>" +
      letra(letraN, 150, 190, 104, BLANCO) +
      "</g>");
  }

  /* ================= 13. crest: escudo del equipo rival (D de Doom) ================= */
  function crest() {
    var escudo = "M140 18 L252 42 L248 192 C246 264 205 307 140 330 C75 307 34 264 32 192 L28 42 Z";
    return svg("0 0 280 340",
      sh(escudo) +
      '<g class="cr-escudo">' +
      '<path d="' + escudo + '" fill="' + DOOM + '" ' + S(8) + "/>" +
      '<path d="M140 42 L230 62 L226 190 C224 250 192 286 140 306 C88 286 56 250 54 190 L50 62 Z" fill="none" ' + S(6) + "/>" +
      letra("D", 140, 180, 148, BLANCO) +
      "</g>");
  }

  /* ================= 14. contract: hoja de contrato con firma ================= */
  function contract() {
    var id = ++uid;
    var hoja = "M45 25 L325 25 L375 75 L375 495 L45 495 Z";
    return svg("0 0 420 520",
      '<defs>' + bday(id) + "</defs>" +
      sh(hoja) +
      '<g class="ct-hoja">' +
      '<path d="' + hoja + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M325 25 L325 75 L375 75 Z" fill="' + CENI + '" ' + S(6) + "/>" +
      '<text x="95" y="112" font-family="Anton, Impact, sans-serif" font-size="62" fill="' + INK + '">FICHAJE</text>' +
      '<path d="M80 160 L340 160 M80 190 L340 190 M80 220 L340 220 M80 250 L268 250" stroke="' + INK + '" stroke-width="4" fill="none" opacity="0.6"/>' +
      '<circle cx="300" cy="300" r="44" fill="none" ' + S(6) + ' stroke-dasharray="12 10"/>' +
      '<path d="M90 402 L330 402" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      /* firma garabato, DRAW-ON (pathLength=1) */
      '<path class="ct-firma" d="M95 392 C120 348 142 396 166 360 C186 330 202 386 226 356 C246 330 262 382 286 358 C300 344 312 372 324 360" fill="none" ' + S(6) + ' pathLength="1"/>' +
      "</g>");
  }

  /* ================= 15. ball: balón clásico tinta y papel ================= */
  function ball() {
    var id = ++uid, cx = 100, cy = 100;
    var pent = "", radios = "", parches = "";
    for (var k = 0; k < 5; k++) {
      var a = ((-90 + k * 72) * Math.PI) / 180;
      /* pentágono central */
      pent += (k ? "L" : "M") + (cx + 26 * Math.cos(a)).toFixed(1) + " " + (cy + 26 * Math.sin(a)).toFixed(1) + " ";
      /* radios del pentágono al borde */
      radios += '<path d="M' + (cx + 26 * Math.cos(a)).toFixed(1) + " " + (cy + 26 * Math.sin(a)).toFixed(1) +
        " L" + (cx + 84 * Math.cos(a)).toFixed(1) + " " + (cy + 84 * Math.sin(a)).toFixed(1) + '" stroke="' + INK + '" stroke-width="6" fill="none"/>';
      /* parche hexagonal en el borde entre este radio y el siguiente */
      var a2 = ((-90 + k * 72 + 72) * Math.PI) / 180;
      parches += '<path d="M' + (cx + 88 * Math.cos(a + 0.28)).toFixed(1) + " " + (cy + 88 * Math.sin(a + 0.28)).toFixed(1) +
        " A88 88 0 0 1 " + (cx + 88 * Math.cos(a2 - 0.28)).toFixed(1) + " " + (cy + 88 * Math.sin(a2 - 0.28)).toFixed(1) +
        " L" + (cx + 64 * Math.cos(a2 - 0.22)).toFixed(1) + " " + (cy + 64 * Math.sin(a2 - 0.22)).toFixed(1) +
        " A64 64 0 0 0 " + (cx + 64 * Math.cos(a + 0.22)).toFixed(1) + " " + (cy + 64 * Math.sin(a + 0.22)).toFixed(1) +
        ' Z" fill="' + INK + '" ' + S(6) + "/>";
    }
    pent += "Z";
    return svg("0 0 200 200",
      "<defs>" + bday(id) + "</defs>" +
      '<circle cx="108" cy="108" r="88" fill="' + INK + '"/>' +
      '<g class="b-balon">' +
      '<circle cx="100" cy="100" r="88" fill="' + PAPEL + '" ' + S(8) + "/>" +
      radios + parches +
      '<path d="' + pent + '" fill="' + INK + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 16. goal: portería tres cuartos · opts.rota = red rota con agujero ================= */
  function goal(opts) {
    opts = opts || {};
    var rota = !!opts.rota;
    var id = ++uid;
    /* plano de fondo (red) en papel 60 % */
    var fondo = "M150 170 L560 170 L560 412 L150 412 Z";
    var agujero = "M300 268 L382 258 L402 320 L368 356 L310 350 Z";
    var red = "";
    if (!rota) {
      for (var x = 205; x < 560; x += 60) red += '<path d="M' + x + " 170 L" + x + " 412" + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
      for (var y = 218; y < 412; y += 48) red += '<path d="M150 ' + y + " L560 " + y + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
    } else {
      var hx = [300, 382, 402, 368, 310]; /* polígono del agujero (arriba) */
      for (var x = 205; x < 560; x += 60) {
        if (x > 285 && x < 405) {
          red += '<path d="M' + x + " 170 L" + x + " 250" + '" stroke="' + INK + '" stroke-width="4" fill="none"/>' +
                 '<path d="M' + x + " 366 L" + x + " 412" + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
        } else red += '<path d="M' + x + " 170 L" + x + " 412" + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
      }
      for (var y = 218; y < 412; y += 48) {
        if (y > 240 && y < 370) {
          red += '<path d="M150 ' + y + " L296 " + y + '" stroke="' + INK + '" stroke-width="4" fill="none"/>' +
                 '<path d="M400 ' + y + " L560 " + y + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
        } else red += '<path d="M150 ' + y + " L560 " + y + '" stroke="' + INK + '" stroke-width="4" fill="none"/>';
      }
    }
    /* profundidad: líneas del marco frontal al trasero */
    var prof = '<path d="M90 122 L150 170 M610 122 L560 170 M90 436 L150 412 M610 436 L560 412" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      '<path d="M150 170 L150 412 M560 170 L560 412" stroke="' + INK + '" stroke-width="6" fill="none"/>';
    return svg("0 0 700 520",
      "<defs>" + bday(id) + "</defs>" +
      '<g class="g-red">' +
      sh(fondo) +
      '<path d="' + fondo + (rota ? " " + agujero : "") + '" fill="' + PAPEL + '" fill-opacity="0.6" fill-rule="evenodd" ' + S(6) + "/>" +
      red + prof +
      (rota ? '<path d="M300 268 L382 258 L402 320 L368 356 L310 350 Z" fill="none" ' + S(5) + ' stroke-dasharray="14 9"/>' : "") +
      "</g>" +
      '<g class="g-postes">' +
      '<rect x="146" y="166" width="18" height="250" fill="' + HEROE + '" ' + S(6) + "/>" +
      '<rect x="552" y="166" width="18" height="250" fill="' + HEROE + '" ' + S(6) + "/>" +
      '<rect x="146" y="166" width="424" height="18" fill="' + HEROE + '" ' + S(6) + "/>" +
      '<rect x="76" y="104" width="36" height="336" fill="' + HEROE + '" ' + S(8) + "/>" +
      '<rect x="588" y="104" width="36" height="336" fill="' + HEROE + '" ' + S(8) + "/>" +
      '<rect x="76" y="104" width="548" height="36" fill="' + HEROE + '" ' + S(8) + "/>" +
      "</g>");
  }

  /* ================= 17. filmCamera: cámara de cine de carrete ================= */
  function filmCamera() {
    var id = ++uid;
    var cuerpo = "M95 175 L365 175 L365 395 L95 395 Z";
    return svg("0 0 520 460",
      "<defs>" + bday(id) + "</defs>" +
      sh("M88 95 A62 62 0 1 0 88.1 95 Z M253 95 A62 62 0 1 0 253.1 95 Z " + cuerpo + " M365 255 L455 255 L455 315 L365 315 Z") +
      /* carretes arriba */
      '<g class="fc-carrete-1">' +
      '<circle cx="150" cy="95" r="62" fill="' + CENI + '" ' + S(8) + "/>" +
      '<circle cx="150" cy="95" r="22" fill="' + INK + '" ' + S(6) + "/>" +
      '<path d="M150 95 L150 44 M150 95 L196 118 M150 95 L104 118" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      "</g>" +
      '<g class="fc-carrete-2">' +
      '<circle cx="315" cy="95" r="62" fill="' + CENI + '" ' + S(8) + "/>" +
      '<circle cx="315" cy="95" r="22" fill="' + INK + '" ' + S(6) + "/>" +
      '<path d="M315 95 L315 44 M315 95 L361 118 M315 95 L269 118" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      "</g>" +
      /* cuerpo gris con panel oscuro y lente amarilla */
      '<path d="' + cuerpo + '" fill="' + CENI + '" ' + S(8) + "/>" +
      '<rect x="115" y="195" width="150" height="180" fill="' + INK + '" ' + S(6) + "/>" +
      '<circle cx="190" cy="285" r="34" fill="' + AMAR + '" ' + S(8) + "/>" +
      '<circle cx="190" cy="285" r="12" fill="' + INK + '"/>' +
      '<path d="M115 214 L265 214" stroke="' + INK + '" stroke-width="6" fill="none"/>' +
      /* lente hacia la derecha */
      '<rect x="365" y="255" width="90" height="60" fill="' + CENI + '" ' + S(8) + "/>" +
      '<circle cx="455" cy="285" r="30" fill="' + INK + '" ' + S(8) + "/>");
  }

  /* ================= 18. clapper: claqueta (pivote de cl-tapa: esquina inferior-izquierda (40,150);
     rotar con gsap transformOrigin: "0% 100%") ================= */
  function clapper() {
    var id = ++uid;
    /* franjas diagonales de una banda (x0,y0,x1,y1, fase) */
    function franjas(x0, y0, x1, y1, fase) {
      var s = "";
      for (var x = x0 - 60 + fase; x < x1 + 60; x += 72) {
        s += '<path d="M' + x + " " + y1 + " L" + (x + 26) + " " + y0 + " L" + (x + 58) + " " + y0 + " L" + (x + 32) + " " + y1 + ' Z" fill="' + INK + '" clip-path="url(#com-cl-' + id + "-" + (fase ? "t" : "b") + ')"/>';
      }
      return s;
    }
    var clip = '<clipPath id="com-cl-' + id + '-b"><rect x="40" y="150" width="360" height="48"/></clipPath>' +
      '<clipPath id="com-cl-' + id + '-t"><rect x="40" y="104" width="360" height="46"/></clipPath>';
    return svg("0 0 420 380",
      "<defs>" + bday(id) + clip + "</defs>" +
      sh("M40 150 L400 150 L400 362 L40 362 Z") +
      /* base */
      '<g class="cl-base">' +
      '<rect x="40" y="150" width="360" height="212" fill="' + INK + '" ' + S(8) + "/>" +
      '<rect x="40" y="150" width="360" height="48" fill="' + PAPEL + '" ' + S(8) + "/>" +
      franjas(40, 150, 400, 198, 0) +
      "</g>" +
      /* bisagra */
      '<circle cx="46" cy="150" r="9" fill="' + CENI + '" ' + S(6) + "/>" +
      /* tapa (cerrada; girar desde su esquina inferior-izquierda) */
      '<g class="cl-tapa">' +
      '<rect x="40" y="104" width="360" height="46" fill="' + PAPEL + '" ' + S(8) + "/>" +
      franjas(40, 104, 400, 150, 36) +
      "</g>");
  }

  /* ================= 19. directorChair: silla de director · opts.silueta = figura sentada ================= */
  function directorChair(opts) {
    opts = opts || {};
    var id = ++uid;
    return svg("0 0 380 520",
      "<defs>" + bday(id) + "</defs>" +
      sh("M58 64 L98 64 L98 340 L58 340 Z M282 64 L322 64 L322 340 L282 340 Z M98 92 L282 92 L282 268 L98 268 Z M90 296 L290 296 L290 332 L90 332 Z M58 458 L322 458 L322 492 L58 492 Z") +
      /* patas en X (madera) */
      '<path d="M78 345 L302 462 M302 345 L78 462" stroke="' + INK + '" stroke-width="20" fill="none"/>' +
      '<path d="M78 345 L302 462 M302 345 L78 462" stroke="' + AMAR + '" stroke-width="12" fill="none"/>' +
      '<rect x="58" y="458" width="264" height="34" fill="' + AMAR + '" ' + S(8) + "/>" +
      '<g class="dc-silla">' +
      /* postes de madera */
      '<rect x="58" y="64" width="40" height="276" fill="' + AMAR + '" ' + S(8) + "/>" +
      '<rect x="282" y="64" width="40" height="276" fill="' + AMAR + '" ' + S(8) + "/>" +
      /* lona roja: respaldo y asiento */
      '<rect x="98" y="92" width="184" height="176" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<rect x="90" y="296" width="200" height="36" fill="' + ROJO + '" ' + S(8) + "/>" +
      /* apoyabrazos */
      '<rect x="28" y="286" width="72" height="26" fill="' + AMAR + '" ' + S(8) + "/>" +
      '<rect x="280" y="286" width="72" height="26" fill="' + AMAR + '" ' + S(8) + "/>" +
      "</g>" +
      /* silueta sentada opcional (cabeza lisa) */
      (opts.silueta
        ? '<circle cx="190" cy="158" r="42" fill="' + INK + '"/>' +
          '<path d="M138 272 C138 214 160 198 190 198 C220 198 242 214 242 272 Z" fill="' + INK + '"/>'
        : ""));
  }

  /* ================= 20. arcReactor: reactor de arco ================= */
  function arcReactor() {
    var id = ++uid, cx = 200, cy = 200;
    /* 10 segmentos del anillo exterior */
    var segs = "";
    for (var k = 0; k < 10; k++) {
      var a0 = (k * 36 + 3) * Math.PI / 180, a1 = (k * 36 + 33) * Math.PI / 180;
      var p = [
        [cx + 186 * Math.cos(a0), cy + 186 * Math.sin(a0)],
        [cx + 186 * Math.cos(a1), cy + 186 * Math.sin(a1)],
        [cx + 152 * Math.cos(a1), cy + 152 * Math.sin(a1)],
        [cx + 152 * Math.cos(a0), cy + 152 * Math.sin(a0)]
      ];
      segs += '<path d="M' + p.map(function (q) { return q[0].toFixed(1) + " " + q[1].toFixed(1); }).join(" L") + ' Z" fill="' + CENI + '" ' + S(6) + "/>";
    }
    /* 10 muescas del anillo intermedio */
    var muescas = "";
    for (k = 0; k < 10; k++) {
      var b = (k * 36 + 18) * Math.PI / 180;
      var q0 = [cx + 108 * Math.cos(b), cy + 108 * Math.sin(b)];
      muescas += '<path d="M' + q0.map(function (v) { return v.toFixed(1); }).join(" ") +
        ' l12 0 l-6 16 Z" fill="' + INK + '" transform="rotate(' + (k * 36 + 18) + " " + q0[0].toFixed(1) + " " + q0[1].toFixed(1) + ')"/>';
    }
    return svg("0 0 400 400",
      "<defs>" + bday(id) + "</defs>" +
      /* resplandor plano (círculos concéntricos, sin blur) */
      '<g class="ar-luz">' +
      '<circle cx="200" cy="200" r="192" fill="' + CIEN + '" opacity="0.16"/>' +
      '<circle cx="200" cy="200" r="160" fill="' + CIEN + '" opacity="0.22"/>' +
      '<circle cx="200" cy="200" r="132" fill="' + CIEN + '" opacity="0.28"/>' +
      "</g>" +
      '<g class="ar-anillos">' +
      '<circle cx="208" cy="208" r="169" fill="none" stroke="' + INK + '" stroke-width="30"/>' +
      segs +
      '<circle cx="200" cy="200" r="141" fill="none" ' + S(8) + "/>" +
      '<circle cx="200" cy="200" r="128" fill="none" stroke="' + CIEN + '" stroke-width="20"/>' +
      '<circle cx="200" cy="200" r="115" fill="none" ' + S(8) + "/>" +
      muescas +
      "</g>" +
      '<g class="ar-nucleo">' +
      '<circle cx="200" cy="200" r="62" fill="' + BLANCO + '" ' + S(8) + "/>" +
      '<circle cx="200" cy="200" r="30" fill="#B9F1FF" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 21. cinemaScreen: pantalla de cine vertical con cortinas ================= */
  function cinemaScreen() {
    var id = ++uid;
    /* telón superior festoneado */
    var valance = "M60 60 L640 60 L640 112 Q604 148 568 112 Q532 148 496 112 Q460 148 424 112 Q388 148 352 112 Q316 148 280 112 Q244 148 208 112 Q172 148 136 112 Q100 148 60 112 Z";
    return svg("0 0 700 900",
      "<defs>" + bday(id) + "</defs>" +
      sh("M60 60 L640 60 L640 840 L60 840 Z") +
      '<g class="cs-pantalla">' +
      '<rect x="60" y="60" width="580" height="780" fill="' + CENI + '" ' + S(8) + "/>" +
      '<rect x="130" y="130" width="440" height="640" fill="' + INK + '" ' + S(8) + "/>" +
      /* zona de proyección: luz plana (trapecios blancos translúcidos, sin blur) */
      '<path d="M252 130 L448 130 L520 770 L180 770 Z" fill="' + BLANCO + '" opacity="0.10"/>' +
      '<path d="M302 130 L398 130 L440 770 L260 770 Z" fill="' + BLANCO + '" opacity="0.08"/>' +
      "</g>" +
      '<g class="cs-cortina-izq">' +
      '<path d="M60 60 L186 60 C170 150 176 250 160 340 C178 430 168 540 184 630 C166 720 178 792 160 840 L60 840 Z" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<path d="M112 120 C104 260 116 420 106 560 C112 660 108 740 112 820 M148 110 C140 240 150 430 142 580 C146 690 144 760 146 830" stroke="' + INK + '" stroke-width="6" fill="none" opacity="0.5"/>' +
      "</g>" +
      '<g class="cs-cortina-der">' +
      '<path d="M640 60 L514 60 C530 150 524 250 540 340 C522 430 532 540 516 630 C534 720 522 792 540 840 L640 840 Z" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<path d="M588 120 C596 260 584 420 594 560 C588 660 592 740 588 820 M552 110 C560 240 550 430 558 580 C554 690 556 760 554 830" stroke="' + INK + '" stroke-width="6" fill="none" opacity="0.5"/>' +
      "</g>" +
      '<path d="' + valance + '" fill="' + ROJO + '" ' + S(8) + "/>");
  }

  /* ================= 22. calendar: calendario · opts.mes "DIC" · opts.dia "18" · opts.anio "2026" ================= */
  function calendar(opts) {
    opts = opts || {};
    var mes = opts.mes || "DIC", dia = opts.dia || "18", anio = opts.anio || "2026";
    var hoja = "M30 82 C30 74 36 68 46 68 L374 68 C384 68 390 74 390 82 L390 438 C390 448 384 454 374 454 L46 454 C36 454 30 448 30 438 Z";
    var cabecera = "M30 82 C30 74 36 68 46 68 L374 68 C384 68 390 74 390 82 L390 172 L30 172 Z";
    return svg("0 0 420 480",
      sh("M30 68 L390 68 L390 454 L30 454 Z") +
      /* anillas detrás */
      '<rect x="112" y="36" width="34" height="56" rx="10" fill="' + CENI + '" ' + S(6) + "/>" +
      '<rect x="274" y="36" width="34" height="56" rx="10" fill="' + CENI + '" ' + S(6) + "/>" +
      '<g class="ca-hoja">' +
      '<path d="' + hoja + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="' + cabecera + '" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<text x="210" y="142" font-family="Anton, Impact, sans-serif" font-size="64" fill="' + PAPEL + '" text-anchor="middle">' + mes + "</text>" +
      "</g>" +
      '<g class="ca-numero">' +
      '<text x="210" y="356" font-family="Anton, Impact, sans-serif" font-size="200" fill="' + INK + '" text-anchor="middle">' + dia + "</text>" +
      '<text x="210" y="430" font-family="Anton, Impact, sans-serif" font-size="52" fill="' + CENI + '" text-anchor="middle">' + anio + "</text>" +
      "</g>");
  }

  /* ================= 23. forbidden: símbolo de prohibido (banda roja 36 px) ================= */
  function forbidden() {
    var id = ++uid;
    var banda = "M87 61 L339 313 L313 339 L61 87 Z";
    return svg("0 0 400 400",
      "<defs>" + bday(id) + "</defs>" +
      /* sombra dura: solo la banda (el anillo rojo se queda plano para no ensuciar) */
      '<path d="' + banda + '" transform="translate(8 8)" fill="' + INK + '"/>' +
      '<g class="fb-simbolo">' +
      '<circle cx="178" cy="178" r="176" fill="none" ' + S(8) + "/>" +
      '<circle cx="178" cy="178" r="160" fill="none" stroke="' + ROJO + '" stroke-width="36"/>' +
      '<circle cx="178" cy="178" r="144" fill="none" ' + S(8) + "/>" +
      '<path d="' + banda + '" fill="' + ROJO + '" ' + S(8) + "/>" +
      "</g>");
  }

  /* ================= 24. xMark: X roja estilo pincel · cada trazo con pathLength=1 para DRAW-ON
     (en cada grupo, el 1.er path es el contorno de tinta y el 2.º el trazo rojo) ================= */
  function xMark() {
    var id = ++uid;
    var t1 = "M96 96 C170 168 232 232 304 304";
    var t2 = "M304 96 C232 168 168 232 96 304";
    function trazo(d, cls) {
      return '<g class="' + cls + '">' +
        '<path d="' + d + '" fill="none" stroke="' + INK + '" stroke-width="62" stroke-linecap="round" pathLength="1"/>' +
        '<path d="' + d + '" fill="none" stroke="' + ROJO + '" stroke-width="44" stroke-linecap="round" pathLength="1"/>' +
        "</g>";
    }
    return svg("0 0 400 400",
      "<defs>" + bday(id) + "</defs>" +
      /* sombra dura desplazada */
      '<path d="' + t1 + '" fill="none" stroke="' + INK + '" stroke-width="44" stroke-linecap="round" transform="translate(10 10)" opacity="0.55"/>' +
      '<path d="' + t2 + '" fill="none" stroke="' + INK + '" stroke-width="44" stroke-linecap="round" transform="translate(10 10)" opacity="0.55"/>' +
      trazo(t1, "x-1") + trazo(t2, "x-2"));
  }

  /* ================= 25. faceless: cabeza lisa y hombros (para máscara cayendo encima) ================= */
  function faceless() {
    var id = ++uid;
    var cabeza = "M130 42 C172 42 194 76 194 122 C194 168 168 206 130 206 C92 206 66 168 66 122 C66 76 88 42 130 42 Z";
    var cuello = "M108 196 L152 196 L156 240 L104 240 Z";
    var hombros = "M26 336 C32 278 58 246 104 238 L156 238 C202 246 228 278 234 336 L234 340 L26 340 Z";
    return svg("0 0 260 340",
      "<defs>" + bday(id) + "</defs>" +
      sh(cabeza + " " + hombros) +
      '<g class="fl-cabeza">' +
      '<path d="' + cuello + '" fill="' + PAPEL + '" ' + S(6) + "/>" +
      '<path d="' + cabeza + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M130 42 C172 42 194 76 194 122 C194 168 168 206 130 206 C150 190 160 160 160 122 C160 84 150 58 130 42 Z" fill="' + bdRef(id) + '"/>' +
      '<path d="' + hombros + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<path d="M162 240 C204 250 224 278 232 336 L172 336 C168 300 164 268 162 240 Z" fill="' + bdRef(id) + '"/>' +
      "</g>");
  }

  /* ================= 26a. speechBubble: globo de diálogo (texto lo pone el HTML encima) ================= */
  function speechBubble() {
    var id = ++uid;
    var cuerpo = "M130 42 L392 42 C454 42 484 78 484 134 C484 190 454 226 392 226 L252 226 L172 302 L196 226 L130 226 C68 226 38 190 38 134 C38 78 68 42 130 42 Z";
    return svg("0 0 520 340",
      "<defs>" + bday(id) + "</defs>" +
      sh(cuerpo) +
      '<g class="sb-cuerpo"><path d="' + cuerpo + '" fill="' + PAPEL + '" ' + S(8) + "/></g>");
  }

  /* ================= 26b. thoughtCloud: nube de pensamiento con 3 burbujas ================= */
  function thoughtCloud() {
    var id = ++uid, cx = 286, cy = 172, N = 10, pts = [];
    for (var i = 0; i < N; i++) {
      var a = -Math.PI / 2 + (i * 2 * Math.PI) / N + (i % 2 ? 0.10 : -0.08);
      var rx = 228 * (1 + 0.05 * Math.cos(2 * a)), ry = 126 * (1 + 0.06 * Math.sin(2 * a));
      pts.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]);
    }
    var d = "M" + pts[0].map(function (v) { return v.toFixed(1); }).join(" ");
    for (i = 1; i <= N; i++) {
      var p = pts[i % N], prev = pts[i - 1];
      var r = 0.62 * Math.hypot(p[0] - prev[0], p[1] - prev[1]);
      d += " A" + r.toFixed(1) + " " + r.toFixed(1) + " 0 0 1 " + p[0].toFixed(1) + " " + p[1].toFixed(1);
    }
    d += " Z";
    return svg("0 0 560 380",
      "<defs>" + bday(id) + "</defs>" +
      sh(d) +
      '<g class="tc-cuerpo">' +
      '<path d="' + d + '" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<circle cx="108" cy="304" r="34" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<circle cx="62" cy="338" r="22" fill="' + PAPEL + '" ' + S(8) + "/>" +
      '<circle cx="26" cy="360" r="13" fill="' + PAPEL + '" ' + S(6) + "/>" +
      "</g>");
  }

  /* ================= 27. coverFrame: marco de portada de cómic ================= */
  function coverFrame() {
    var id = ++uid;
    return svg("0 0 760 1080",
      "<defs>" + bday(id) + "</defs>" +
      '<g class="cv-fondo">' +
      '<rect x="22" y="22" width="716" height="1036" fill="' + PAPEL + '" stroke="' + INK + '" stroke-width="16" stroke-linejoin="round"/>' +
      '<rect x="56" y="56" width="648" height="968" fill="none" ' + S(8) + "/>" +
      /* esquinas de tinta */
      '<rect x="22" y="22" width="30" height="30" fill="' + INK + '"/>' +
      '<rect x="708" y="22" width="30" height="30" fill="' + INK + '"/>' +
      '<rect x="22" y="1028" width="30" height="30" fill="' + INK + '"/>' +
      '<rect x="708" y="1028" width="30" height="30" fill="' + INK + '"/>' +
      "</g>" +
      /* banda superior vacía para el logo */
      '<rect x="120" y="76" width="520" height="88" fill="none" ' + S(8) + "/>" +
      '<g class="cv-numero-caja">' +
      '<rect x="56" y="56" width="150" height="82" fill="' + AMAR + '" ' + S(8) + "/>" +
      "</g>" +
      '<g class="cv-precio">' +
      '<circle cx="632" cy="948" r="80" fill="' + ROJO + '" ' + S(8) + "/>" +
      '<text x="632" y="966" font-family="Anton, Impact, sans-serif" font-size="44" fill="' + PAPEL + '" text-anchor="middle">GRATIS</text>' +
      "</g>");
  }

  /* ================= 28. bolt: rayo rojo para el choque ================= */
  function bolt() {
    var id = ++uid;
    var d = "M170 10 L60 250 L132 250 L90 490 L252 220 L172 220 L242 10 Z";
    return svg("0 0 300 500",
      "<defs>" + bday(id) + "</defs>" +
      sh(d) +
      '<g class="bo-rayo"><path d="' + d + '" fill="' + ROJO + '" ' + S(8) + "/></g>");
  }

  /* ================= 29. star: destello de impacto de 8 puntas ================= */
  function star() {
    var id = ++uid, r = rng(20261218), cx = 130, cy = 130, pts = [];
    for (var i = 0; i < 8; i++) {
      var a = (-90 + i * 45) * Math.PI / 180 + (r() - 0.5) * 0.18;
      var R = 116 + (r() - 0.5) * 26;
      var b = a + 45 * Math.PI / 360;
      var rr = 46 + (r() - 0.5) * 12;
      pts.push([a, R], [b, rr]);
    }
    var d = pts.map(function (p, k) {
      return (k ? "L" : "M") + (cx + p[1] * Math.cos(p[0])).toFixed(1) + " " + (cy + p[1] * Math.sin(p[0])).toFixed(1);
    }).join(" ") + " Z";
    return svg("0 0 260 260",
      "<defs>" + bday(id) + "</defs>" +
      sh(d) +
      '<g class="st-explosion"><path d="' + d + '" fill="' + AMAR + '" ' + S(8) + "/></g>");
  }

  /* ================= 30. splat: mancha de tinta con lóbulos (INK-SPLASH) ================= */
  function splat() {
    var id = ++uid, r = rng(1900), cx = 260, cy = 260;
    var P = [];
    for (var i = 0; i < 12; i++) {
      var a = (i * 30 + (r() - 0.5) * 18) * Math.PI / 180;
      var R = 150 + (r() - 0.5) * 44;
      P.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]);
    }
    var d = "M" + ((P[11][0] + P[0][0]) / 2).toFixed(1) + " " + ((P[11][1] + P[0][1]) / 2).toFixed(1);
    for (i = 0; i < 12; i++) {
      var q = P[i], n = P[(i + 1) % 12];
      d += " Q" + q[0].toFixed(1) + " " + q[1].toFixed(1) + " " + ((q[0] + n[0]) / 2).toFixed(1) + " " + ((q[1] + n[1]) / 2).toFixed(1);
    }
    d += " Z";
    var gotas = "";
    for (i = 0; i < 6; i++) {
      var b = (i * 60 + r() * 30) * Math.PI / 180, rr = 210 + r() * 46;
      gotas += '<circle cx="' + (cx + rr * Math.cos(b)).toFixed(1) + '" cy="' + (cy + rr * Math.sin(b)).toFixed(1) + '" r="' + (7 + r() * 9).toFixed(1) + '" fill="' + INK + '"/>';
    }
    return svg("0 0 520 520",
      "<defs>" + bday(id) + "</defs>" +
      '<g class="sp-mancha">' +
      '<path d="' + d + '" fill="' + INK + '"/>' +
      /* lóbulos salientes */
      '<circle cx="' + (cx + 188 * Math.cos(0.4)).toFixed(1) + '" cy="' + (cy + 188 * Math.sin(0.4)).toFixed(1) + '" r="34" fill="' + INK + '"/>' +
      '<circle cx="' + (cx + 196 * Math.cos(2.4)).toFixed(1) + '" cy="' + (cy + 196 * Math.sin(2.4)).toFixed(1) + '" r="28" fill="' + INK + '"/>' +
      '<circle cx="' + (cx + 182 * Math.cos(4.3)).toFixed(1) + '" cy="' + (cy + 182 * Math.sin(4.3)).toFixed(1) + '" r="31" fill="' + INK + '"/>' +
      gotas +
      "</g>");
  }

  /* ================= registro (sin pisar window.COM si ya existe) ================= */
  var COM = (typeof window !== "undefined" && window.COM) || {};
  if (typeof window !== "undefined") window.COM = COM;
  var OBJ = COM.OBJ || {};
  OBJ.kang = kang; OBJ.iron = iron; OBJ.doom = doom; OBJ.doomMask = doomMask; OBJ.crown = crown;
  OBJ.castle = castle; OBJ.gearAtom = gearAtom; OBJ.runes = runes; OBJ.fourEmblem = fourEmblem;
  OBJ.comicOpen = comicOpen; OBJ.player = player; OBJ.jersey = jersey; OBJ.crest = crest;
  OBJ.contract = contract; OBJ.ball = ball; OBJ.goal = goal; OBJ.filmCamera = filmCamera;
  OBJ.clapper = clapper; OBJ.directorChair = directorChair; OBJ.arcReactor = arcReactor;
  OBJ.cinemaScreen = cinemaScreen; OBJ.calendar = calendar; OBJ.forbidden = forbidden;
  OBJ.xMark = xMark; OBJ.faceless = faceless; OBJ.speechBubble = speechBubble;
  OBJ.thoughtCloud = thoughtCloud; OBJ.coverFrame = coverFrame; OBJ.bolt = bolt;
  OBJ.star = star; OBJ.splat = splat;
  COM.OBJ = OBJ;

  /* monta todos los [data-com] del root: data-com="nombre" + data-opts='{"color":"doom"}' (JSON).
     No hace nada si el elemento ya está montado (data-mounted). */
  COM.mount = function (root) {
    if (!root || !root.querySelectorAll) return;
    var els = root.querySelectorAll("[data-com]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.hasAttribute("data-mounted")) continue;
      el.setAttribute("data-mounted", "1");
      var fn = OBJ[el.getAttribute("data-com")];
      if (!fn) continue; /* nombre desconocido: no monta */
      var opts = {};
      var raw = el.getAttribute("data-opts");
      if (raw) { try { opts = JSON.parse(raw); } catch (e) { opts = {}; } }
      el.innerHTML = fn(opts);
      el.classList.add("com-obj");
    }
  };
})();
