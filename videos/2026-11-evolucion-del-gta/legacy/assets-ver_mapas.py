import json,sys,glob
from pathlib import Path
for f in sorted(glob.glob(str(Path(__file__).parent/"_mapas/*.json"))):
    n=Path(f).stem
    if len(sys.argv)>1 and n not in sys.argv[1:]: continue
    d=json.load(open(f))
    print(f"## {n} ({d['_meta']['sonda']['dur']:.0f}s)")
    for x in d.get("destacados",[]):
        print(f"  {x.get('inicio_s',0):6.1f}-{x.get('fin_s',0):6.1f} {x.get('uso','')[:6]} {x.get('titulo','')+' · '+x.get('por_que_retiene','')[:70]}")
    for x in d.get("planos",[]):
        print(f"   p {x['inicio_s']:6.1f}-{x['fin_s']:6.1f} {x['descripcion'][:100]}" + (f" «{x['dialogo'][:60]}»" if x.get("dialogo") else ""))
    ev=d.get("evitar",[])
    if ev: print("  evitar:", "; ".join(f"{e.get('inicio_s',0):.0f}-{e.get('fin_s',0):.0f} {e.get('motivo','')[:40]}" for e in ev)[:300])
