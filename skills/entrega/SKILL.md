---
name: entrega
description: Prepara lo necesario para publicar un video en YouTube (miniaturas A/B, portadas de shorts, títulos, descripción con capítulos, tags, comentario fijado) y corre el QA final hacia entrega/. Úsala para miniaturas, títulos, descripciones, QA o para registrar una URL publicada.
---

# Entrega: todo lo que se sube a YouTube

Reglas: `base/publicacion/REGLAS.md` y `base/publicacion/MINIATURAS.md`. Lo que el video quiera distinto va en `publicacion.override.md`, que gana sobre la base.

## 1. Miniaturas

1. Escribe `miniaturas.json` (ejemplo: `base/publicacion/miniaturas.ejemplo.json`):
   - largo → `miniatura-A` y `miniatura-B`, con ángulos distintos;
   - cada short → `portada-short-NN`.
   - Layouts: `hero`, `versus`, `portada`, o `html` propio con las clases del estilo.
2. `./tl miniaturas <video>` → `entrega/*.png`.
3. **Míralas** a tamaño de feed. ¿Se leen en chico? ¿La cara manda? ¿Complementan al título? Ajusta y repite.

## 2. PUBLICACION.md

Parte de `base/publicacion/PUBLICACION.template.md`, aplica las reglas y el override, y llena **cada pieza**:
- títulos A/B más uno de respaldo;
- descripción con capítulos: tiempos reales de `build/timeline-largo.json`, el inicio de cada sección con su título;
- tags del autocompletado (`youtube-trends`);
- comentario fijado;
- playlist;
- en cada short: título `#shorts`, descripción y «Video relacionado: el largo»;
- orden y calendario sugeridos.

## 3. QA y entrega

`./tl entrega <video>` corre el QA (duración, loudness, lint, miniaturas, PUBLICACION.md, enlaces short → largo, sellos y hojas a 1 fps) y, si no hay errores, deja los finales en `entrega/`.
- **Mira las hojas** que genera (`build/revision/`).
- Corrige cada error en su fase. `--forzar` solo si el usuario lo decide.

Se completa cuando `./tl qa <video>` termina sin errores y `entrega/` tiene cada pieza, cada miniatura y PUBLICACION.md.

## Después de publicar

El usuario pasa las URLs → `./tl publicado <video> <pieza> <url>` por cada pieza. Cuando todas están, el video queda `publicado` y entra a `./tl limpiar --todos-publicados`.
