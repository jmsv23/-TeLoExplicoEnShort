#!/bin/bash
# Una corrida de Gemini por video (gemini_mapa.py se niega a repetir). Uso: bash mapear.sh
cd /home/jmsv23/projects/personal/content-creator
set -a; . ./.env; set +a
A=explicando/evolucion-del-gta/assets
declare -A C=(
 [gta6-tr1]="Hook y espera: primer tráiler de GTA 6 (Lucía en prisión, Vice City, Florida). Buscamos la frase inicial de Lucía y planos icónicos de Vice City."
 [gta6-tr2]="GTA 6: Jason y Lucía, Leonida, Vice City de día y de noche, autos, pantanos. B-roll espectacular."
 [gta6-launch]="GTA 6 ya salió: planos espectaculares de Leonida, persecuciones, Vice City."
 [gta1-gameplay]="GTA 1 de 1997 visto desde arriba, pixelado: autos, atropellos, policía persiguiendo."
 [gta2-gameplay]="GTA 2 de 1999: vista cenital, pandillas, policía."
 [gta3-intro]="GTA III 2001: primer GTA en 3D, Liberty City, Claude (no habla), patrullas."
 [vc-gameplay]="GTA Vice City 2002: neón, ochentas, Tommy Vercetti, autos, playa, agua (Tommy no sabe nadar)."
 [sa-intro]="San Andreas: intro de CJ llegando a Los Santos, la frase 'Ah shit, here we go again' en Grove Street."
 [sa-cuerpo]="San Andreas: CJ flaco, musculoso y gordo; gimnasio, comida. Mecánicas de cuerpo."
 [iv-roman]="GTA IV: llamada de Roman 'Niko, it's Roman, let's go bowling'."
 [iv-vs-v-fisica]="Comparación de física de autos GTA IV vs GTA V: choques, deformación, suspensión."
 [vi-vs-iv-fisica]="Comparación de física GTA 6 vs GTA IV: choques y deformación."
 [iv-euphoria]="GTA IV Euphoria: personajes que se tropiezan, se agarran de los autos, caídas realistas."
 [v-trailer]="GTA V tráiler oficial 2013: Los Santos, Michael, Franklin, Trevor."
 [v-mft]="GTA V: tráiler de Michael, Franklin y Trevor, cambio de personaje."
 [vi-policia]="GTA 6 sistema de policía: testigos, cámaras, estrellas, persecuciones, sexta estrella."
 [vi-barco]="GTA 6 easter egg: el velero de Michael (GTA V) afuera de la casa de Jason con el mapa de Los Santos en el GPS."
 [vi-gym]="GTA 6: Lucía en el gimnasio, transformación de cuerpo, regresa la mecánica de San Andreas."
 [vi-choques]="GTA 6 choques de autos realistas, deformación, piezas que se caen."
 [vc-vs-vi]="Vice City 2002 contra Vice City GTA 6, lado a lado, mismos lugares (Ocean Beach, hotel Ocean View)."
 [vi-manejo]="GTA 6 manejando por Vice City: calles, neón, playa, tráfico, gente."
)
for n in "${!C[@]}"; do
  [ -f "$A/video/$n.mp4" ] || { echo "falta $n"; continue; }
  [ -f "$A/_mapas/$n.json" ] && continue
  python3 -P $A/gemini_mapa.py "$n" "${C[$n]}" > "$A/_mapas/.$n.log" 2>&1 &
  while [ "$(jobs -r | wc -l)" -ge 5 ]; do sleep 2; done
done
wait
for n in "${!C[@]}"; do echo "$n: $(tail -1 $A/_mapas/.$n.log 2>/dev/null)"; done
