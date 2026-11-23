#!/bin/bash
# Build + render + mezcla de todas las piezas. Uso: bash render_todo.sh [pieza ...]
cd "$(dirname "$0")"
export HYPERFRAMES_CACHE_DIR=/tmp/claude-1000/-home-jmsv23-projects-personal-content-creator/cc89c6ad-24f9-4693-ae21-76f7a024d42a/scratchpad/hfcache
P=${@:-s1 s2 largo}
for p in $P; do
  rtk proxy python3 build.py $p 2>&1 | grep -E "✓|Error|falta"
  (cd hf-$p && rtk proxy npx hyperframes render -o ../render/$p-video.mp4 --skill hyperframes --workers ${WORKERS:-2} 2>&1 | grep -iE "error|✓|done|rendered" | tail -2)
  python3 mezcla.py $p 2>&1 | tail -1
done
