"""Miniaturas A/B del largo (1280x720) y portadas de los 6 Shorts (1080x1920). python3 gen.py"""
import subprocess
from pathlib import Path
A = "../../assets/img"
BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Price;src:url(../fonts/Pricedown.otf)}@font-face{font-family:Anton;src:url(../fonts/Anton.ttf)}
@font-face{font-family:Script;src:url(../fonts/Pacifico-Regular.ttf)}@font-face{font-family:Pix;src:url(../fonts/PressStart2P-Regular.ttf)}
*{margin:0;padding:0;box-sizing:border-box}body{width:__W__px;height:__H__px;overflow:hidden;position:relative;font-family:Anton}
.sky{position:absolute;inset:0;background:linear-gradient(180deg,#140826 0%,#2e0f4a 34%,#6b1b62 62%,#c23a5e 82%,#ff8a4c 100%)}
.p{font-family:Price;line-height:.86;color:#fff;-webkit-text-stroke:12px #0b0612;paint-order:stroke fill;text-shadow:0 9px 0 #0b0612}
.g{background:linear-gradient(180deg,#ffe08a,#ff8a3d 48%,#ff3f8f);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-stroke:0;text-shadow:none;
 filter:drop-shadow(0 7px 0 #0b0612) drop-shadow(0 0 3px #0b0612) drop-shadow(0 0 3px #0b0612)}
.panel{position:absolute;background:#0b0612;padding:8px;box-shadow:0 0 0 5px #fff,0 0 0 12px #0b0612,0 20px 50px rgba(0,0,0,.6);overflow:hidden}
.panel img{width:100%;height:100%;object-fit:cover;display:block}
.k{font-family:Anton;letter-spacing:.06em;color:#fff;background:#ff2f7f;padding:4px 26px 2px;display:inline-block;box-shadow:0 0 0 6px #0b0612,0 12px 30px rgba(0,0,0,.5)}
</style></head><body>"""


def page(name, w, h, body):
    f = Path(f"{name}.html")
    f.write_text(BASE.replace("__W__", str(w)).replace("__H__", str(h)) + body + "</body></html>")
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={Path(name + '.png').resolve()}", "--virtual-time-budget=4000", f"file://{f.resolve()}"],
                   capture_output=True)
    print("✓", name)


# A: Lucía (arte oficial) + GTA 1 pixelado · "1997 VS 2026"
page("miniatura-A", 1280, 720, f"""<div class="sky"></div>
<img src="{A}/lucia-corriendo.jpg" style="position:absolute;right:0;top:0;width:620px;height:720px;object-fit:cover;object-position:50% 20%">
<div style="position:absolute;right:560px;top:0;width:120px;height:720px;background:linear-gradient(90deg,rgba(46,15,74,1),rgba(46,15,74,0))"></div>
<div class="panel" style="left:46px;top:120px;width:400px;height:250px;transform:rotate(-4deg)"><img src="gta1.jpg"></div>
<div class="p" style="position:absolute;left:70px;top:330px;font-size:150px;transform:rotate(-4deg)">1997</div>
<div class="p g" style="position:absolute;left:330px;top:440px;font-size:120px;color:#ff4fa3">VS</div>
<div class="p g" style="position:absolute;left:470px;top:470px;font-size:210px">2026</div>
<div class="k" style="position:absolute;left:30px;top:14px;font-size:68px;transform:rotate(-4deg)">GTA 6 VS TODOS</div>""")

# B: Vice City 2002 vs 2026 + "¿EVOLUCIÓN O RETROCESO?"
page("miniatura-B", 1280, 720, f"""<div class="sky"></div>
<img src="vc2002.jpg" style="position:absolute;left:0;top:0;width:640px;height:720px;object-fit:cover;object-position:40% 50%">
<img src="{A}/jl-gasolinera.jpg" style="position:absolute;right:0;top:0;width:640px;height:720px;object-fit:cover;object-position:50% 45%">
<div style="position:absolute;left:632px;top:0;width:16px;height:720px;background:#0b0612;box-shadow:0 0 0 4px #fff"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,8,38,.0) 45%,rgba(20,8,38,.85))"></div>
<div class="p" style="position:absolute;left:40px;top:30px;font-size:120px">2002</div>
<div class="p g" style="position:absolute;right:40px;top:30px;font-size:120px">2026</div>
<div style="position:absolute;left:0;right:0;top:36px;text-align:center"><div class="k" style="font-size:80px">GTA 6</div></div>
<div class="p" style="position:absolute;left:0;right:0;bottom:150px;text-align:center;font-size:118px">¿EVOLUCIÓN</div>
<div class="p g" style="position:absolute;left:0;right:0;bottom:30px;text-align:center;font-size:132px">O RETROCESO?</div>""")

# Portadas de Shorts
SH = {
    "s1": ("vi-keyart", "50% 30%", "$3,790 M", "EN UN DÍA", "GTA 6 · RÉCORD"),
    "s2": ("jl-gasolinera", "50% 40%", "99 VS 5", "¿QUIÉN TIENE RAZÓN?", "GTA 6 · METACRITIC"),
    "s3": ("mft-arte", "30% 30%", "EL BARCO", "DE MICHAEL", "GTA 6 · EASTER EGG"),
    "s4": ("vi-policia-playa", "50% 40%", "LA POLICÍA", "YA NO TE VE", "GTA 6"),
    "s5": ("vi-neon", "50% 50%", "2002", "VS 2026", "GTA 6 · VICE CITY"),
    "s6": ("jl-armas", "50% 30%", "GTA V", "EMPEORÓ", "GTA 6 · CHOQUES"),
}
for k, (img, pos, l1, l2, kick) in SH.items():
    page(f"portada-{k}", 1080, 1920, f"""<div class="sky"></div>
<img src="{A}/{img}.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1250px;object-fit:cover;object-position:{pos}">
<div style="position:absolute;left:0;top:900px;width:1080px;height:360px;background:linear-gradient(180deg,rgba(20,8,38,0),rgba(46,15,74,1))"></div>
<div style="position:absolute;left:0;right:0;top:1110px;text-align:center"><div class="k" style="font-size:96px">{kick}</div></div>
<div class="p" style="position:absolute;left:0;right:0;top:1300px;text-align:center;font-size:190px">{l1}</div>
<div class="p g" style="position:absolute;left:0;right:0;top:1500px;text-align:center;font-size:180px">{l2}</div>""")
