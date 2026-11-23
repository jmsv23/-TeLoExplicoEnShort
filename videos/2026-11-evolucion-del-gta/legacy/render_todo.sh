#!/bin/bash
# Build + render + mezcla de todas las piezas. Uso: bash render_todo.sh [pieza ...]
cd "$(dirname "$0")"
export HYPERFRAMES_CACHE_DIR=/tmp/claude-1000/-home-jmsv23-projects-personal-content-creator/e52a7c54-083b-4f75-a6ad-2f9809e415a5/scratchpad/hfcache
P=${@:-s1 s2 s3 s4 s5 s6 largo}
for p in $P; do
  rtk proxy python3 build.py $p 2>&1 | grep -E "✓|Error|falta"
  (cd hf-$p && rtk proxy npx hyperframes render -o ../render/$p-video.mp4 --skill hyperframes --workers ${WORKERS:-2} 2>&1 | grep -iE "error|✓|done|rendered" | tail -2)
  python3 mezcla.py $p 2>&1 | tail -1
done
