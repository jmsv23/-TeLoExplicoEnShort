# Miniaturas y portadas

## Reglas visuales

- **3-5 palabras** grandes. Se tienen que leer en una miniatura de 168 px de ancho.
- **Una sola cara protagonista**, con emoción visible, ocupando de ⅓ a ½ del cuadro.
- **Contraste:** texto claro sobre fondo oscuro o al revés. La palabra clave va con el acento del estilo.
- **Complementa al título**, nunca lo repite: plantea la duda o el dato que el título no dice.
- **Largo:** 1280×720, siempre A y B. Las variantes cambian el ángulo, no solo el color.
- **Short:** portada 1080×1920. El texto va en el tercio bajo, por encima de la zona de botones (y < 1650 px).
- Marca de agua del canal: la pone YouTube (`base/canal/identidad/marca-agua-youtube.png`). No se mete en la miniatura.

## Cómo se arman (base → estilo → video)

1. **Base:** estas reglas y los layouts genéricos del motor (`motor/miniaturas.py`):
   - `hero`: foto a la derecha, texto a la izquierda, fila opcional de caras;
   - `versus`: dos fotos con etiqueta y frase abajo;
   - `portada`: Short, foto arriba y texto abajo.
2. **Estilo:** `estilos/<slug>/miniatura.css` da la piel de las clases. Un estilo puede agregar layouts propios en `estilos/<slug>/miniaturas.py`.
3. **Video:** `miniaturas.json` con los datos de cada miniatura (ejemplo: `miniaturas.ejemplo.json`).
   - Para una composición que ningún layout cubre: `{"id": …, "pieza": …, "html": "miniaturas/x.html"}` con el `<body>` a mano. Usa las clases del estilo y `{IMG}` para la carpeta de imágenes.

`./tl miniaturas <video>` → `entrega/<id>.png`. Antes de entregar, mira las miniaturas juntas a tamaño de feed.
