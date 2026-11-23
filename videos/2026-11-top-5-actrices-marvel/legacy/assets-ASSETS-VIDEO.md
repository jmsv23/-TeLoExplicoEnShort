# Assets: video (solo el video largo)

El **Short usa solo imágenes** (`ASSETS-IMG.md`). Los cortes salen de `cortar.py` → `video/cortes/` (1080p30). Las escenas con voz van normalizadas a -16 LUFS.

- **voz:** escena con sonido. El narrador se calla y la música baja a -18 dB. Las primarias suman **31.8 s** (límite: 60 s).
- **voz-alt:** alternativa si una primaria no funciona en el montaje.
- **broll:** se usa muda, dentro del marco blanco de la "foto impresa".

| Corte | Dur. | Tipo | Bloque | Qué se ve / oye | Fuente (seg.) |
|---|---|---|---|---|---|
| `cortes/zoe-idiotas.mp4` | 4.0s | voz | 5 Zoe | "I'm gonna die surrounded by the biggest idiots in the galaxy". 720p con subtítulo quemado: zoom 1.55 lo saca | [esc-gotg-idiotas](https://www.youtube.com/watch?v=Jb_eKuD7IR0) 0.0–3.97 |
| `cortes/zoe-gamora-rostro.mp4` | 3.5s | broll | 5 Zoe | primer plano de Gamora en la oscuridad | [esc-gotg-rescate](https://www.youtube.com/watch?v=S3wf3Pf_oEs) 133.0–136.5 |
| `cortes/zoe-gamora-flotando.mp4` | 3.0s | broll | 5 Zoe | Gamora flotando en el espacio | [esc-gotg-rescate](https://www.youtube.com/watch?v=S3wf3Pf_oEs) 4.0–7.0 |
| `cortes/portman-eat-my-hammer.mp4` | 5.0s | voz | 4 Portman | "Eat my hammer!" y el rayo | [esc-lovethunder-mighty](https://www.youtube.com/watch?v=2aphoPK_IpI) 261.0–266.0 |
| `cortes/portman-mighty-grito.mp4` | 4.0s | broll | 4 Portman | Jane grita con el martillo y lo lanza | [esc-lovethunder-mighty](https://www.youtube.com/watch?v=2aphoPK_IpI) 254.6–258.6 |
| `cortes/portman-transformacion.mp4` | 4.0s | broll | 4 Portman | el martillo llega y aparece la Poderosa Thor | [esc-lovethunder-mighty](https://www.youtube.com/watch?v=2aphoPK_IpI) 120.5–124.5 |
| `cortes/portman-cachetada-loki.mp4` | 1.6s | voz-alt | 4 Portman | "That's for New York". Fuente meme vertical con texto: solo si se recorta la banda de película | [esc-thor2-cachetada](https://www.youtube.com/watch?v=HeNUnl17hg4) 2.4–4.0 |
| `cortes/zendaya-call-me-mj.mp4` | 3.0s | voz | 3 Zendaya | "Thank you. My friends call me MJ." (desde 12 s hay un meme de The Office: no pasar) | [esc-homecoming-callmemj](https://www.youtube.com/watch?v=EwP5axvqkDM) 9.0–12.0 |
| `cortes/zendaya-lame-party.mp4` | 5.9s | voz | 3 Zendaya | "Can't believe you're at this lame party" / "But you're here too" / "Am I?". Subtítulo quemado: zoom | [esc-homecoming-mj](https://www.youtube.com/watch?v=_3UyRtHmaJc) 0.0–5.9 |
| `cortes/olsen-took-everything.mp4` | 5.9s | voz | 2 Olsen | "You took everything from me" / "I don't even know who you are" | [esc-endgame-wanda](https://www.youtube.com/watch?v=Pz6PiGzUhDQ) 4.5–10.4 |
| `cortes/olsen-levitando.mp4` | 4.5s | broll | 2 Olsen | Wanda se eleva con poder rojo | [esc-endgame-wanda](https://www.youtube.com/watch?v=Pz6PiGzUhDQ) 13.0–17.5 |
| `cortes/olsen-wakanda-poder.mp4` | 4.5s | broll | 2 Olsen | Wanda destroza a las bestias en Wakanda | [esc-iw-wanda-wakanda](https://www.youtube.com/watch?v=tb8-ZyqNUWQ) 6.0–10.5 |
| `cortes/olsen-wakanda-okoye.mp4` | 5.7s | voz-alt | 2 Olsen | Wanda llega; Okoye: "Why was she up there all this time?" | [esc-iw-wanda-wakanda](https://www.youtube.com/watch?v=tb8-ZyqNUWQ) 16.6–22.3 |
| `cortes/scarlett-on-hold.mp4` | 8.0s | voz | 1 Scarlett | "Let me put you on hold" y se libera de la silla. Subtítulo quemado: zoom | [esc-avengers-interrogatorio](https://www.youtube.com/watch?v=JyyGJk51n-0) 132.5–140.5 |
| `cortes/scarlett-interrogatorio-moron.mp4` | 7.1s | voz-alt | 1 Scarlett | "I'm in the middle of an interrogation. This moron is giving me everything." (WhisperX corre ~17 s antes aquí: tiempos por subtítulo) | [esc-avengers-interrogatorio](https://www.youtube.com/watch?v=JyyGJk51n-0) 115.5–122.6 |
| `cortes/scarlett-pasillo-camina.mp4` | 6.0s | broll | 1 Scarlett | Natasha avanza por el pasillo hacia cámara | [esc-ironman2-pasillo](https://www.youtube.com/watch?v=0lZYKVl49Ac) 107.0–113.0 |
| `cortes/scarlett-pasillo-desliza.mp4` | 3.5s | broll | 1 Scarlett | barrida por el piso | [esc-ironman2-pasillo](https://www.youtube.com/watch?v=0lZYKVl49Ac) 43.0–46.5 |
| `cortes/scarlett-pasillo-pose.mp4` | 3.0s | broll | 1 Scarlett | pose de pelea en el pasillo | [esc-ironman2-pasillo](https://www.youtube.com/watch?v=0lZYKVl49Ac) 24.0–27.0 |

## Cómo se eligieron

1. **Fuentes:** búsqueda de videos de Brave → yt-dlp (≤1080p, con audio). Las URLs están en `video/fuentes.tsv`.
2. **Transcripciones:** WhisperX (en) en `_transcripciones/`.
   - ⚠ En `esc-avengers-interrogatorio` WhisperX corre ~17 s antes que la imagen. Ahí mandan los subtítulos quemados.
3. **Mapas de Gemini** (`gemini_mapa.py`, gemini-3.1-flash-lite, media resolution MEDIUM, **una pasada por video**) en `_mapas/`.
   Se mapearon 8 videos: gotg-rescate, lovethunder-mighty, homecoming-mj, homecoming-final, endgame-wanda, iw-wanda-wakanda, avengers-interrogatorio e ironman2-pasillo.
   - `esc-homecoming-final` no tiene a MJ: se descarta.
4. **Clips cortos sin mapa** (≤25 s), revisados a 1–2 fps: gotg-idiotas, thor2-cachetada y homecoming-callmemj.
5. **Verificación a 1 fps** de cada destacado (`verificar_mapa.py` → `_hojas/verif-*.jpg`, `verif2-*.jpg`) y hoja final de cortes en `_hojas/cortes.jpg`.

## Notas

- **Subtítulos quemados:** zoe-idiotas, zendaya-lame-party y scarlett-* vienen de fuentes con subtítulos. `zoom` los recorta.
  - zoe-idiotas sale de un 720p con zoom 1.55: se ve suave. Úsalo dentro del marco de "foto impresa", no a pantalla completa.
- **portman-cachetada-loki** viene de un meme vertical con texto. Queda solo como alternativa; la escena con sonido de Portman es "Eat my hammer!".
- **Cambio frente al guion:** Portman usa *Love and Thunder* ("Eat my hammer!") en vez de la cachetada de *Thor 2*, porque no había una fuente limpia de la cachetada. Scarlett usa "Let me put you on hold" (el interrogatorio), y el pasillo de *Iron Man 2* va como b-roll.
