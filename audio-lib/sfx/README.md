# SFX compartidos

Son pequeños y los usan todos los estilos, así que se versionan. `picos.json` guarda en qué segundo cae el pico de cada efecto, para que la mezcla alinee ese pico con el evento.
- Cada estilo fija su ganancia en `SFX_GAIN` y su adelanto en `PICO_ANTES` (`estilo.py`).
- Para agregar un efecto: genéralo con la skill `soundeffect`, normalízalo a -3 dBFS de pico, guárdalo aquí como `<nombre>.wav` y agrega su pico a `picos.json`.

| Efecto | Uso típico |
|---|---|
| whoosh, whoosh-rapido | transiciones (iris, zoom, barrido, látigo) |
| golpe | revelaciones, cifras, flash |
| sello | sellos (CONFIRMADO, PETICIÓN…) |
| tick | datos que aparecen en una ficha |
| teclas | URL que se escribe |
| riser | subida antes de un clímax |
| obturador | flash de cámara (portada) |
| papel, lapiz | pase de página, círculo de lápiz (portada) |
