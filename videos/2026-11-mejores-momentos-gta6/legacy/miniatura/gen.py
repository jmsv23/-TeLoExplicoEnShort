"""Miniaturas A/B del largo (1280x720) y portadas de los 2 Shorts (1080x1920). python3 gen.py"""
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
.k{font-family:Anton;letter-spacing:.06em;color:#fff;background:#ff2f7f;padding:6px 18px;display:inline-block;box-shadow:0 0 0 4px #0b0612}
</style></head><body>"""


def page(name, w, h, body):
    f = Path(f"{name}.html")
    f.write_text(BASE.replace("__W__", str(w)).replace("__H__", str(h)) + body + "</body></html>")
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={Path(name + '.png').resolve()}", "--virtual-time-budget=4000", f"file://{f.resolve()}"],
                   capture_output=True)
    print("✓", name)



# A: la cara de IlloJuan + "BORRÓ GTA 6 EN DIRECTO"
page("miniatura-A", 1280, 720, """<div class="sky"></div>
<img src="illo-full.jpg" style="position:absolute;inset:0;width:1280px;height:720px;object-fit:cover;filter:blur(3px) brightness(.55)">
<div class="panel" style="left:40px;top:70px;width:560px;height:580px;transform:rotate(-3deg)"><img src="illo-cara.jpg" style="object-position:50% 30%"></div>
<div class="k" style="position:absolute;left:660px;top:70px;font-size:40px;transform:rotate(2deg)">EN PLENO DIRECTO</div>
<div class="p" style="position:absolute;left:650px;top:170px;font-size:190px;transform:rotate(2deg)">BORRÓ</div>
<div class="p g" style="position:absolute;left:650px;top:360px;font-size:230px;transform:rotate(2deg)">GTA 6</div>
<div class="p" style="position:absolute;right:40px;bottom:30px;font-size:70px;color:#ff4fa3">TOP 12</div>""")

# B: el perro en moto de agua + "¿UN PERRO MANEJANDO?"
page("miniatura-B", 1280, 720, """<div class="sky"></div>
<img src="perro-18.jpg" style="position:absolute;inset:0;width:1280px;height:720px;object-fit:cover;object-position:50% 60%;transform:scale(1.35);transform-origin:52% 62%">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,8,38,.75) 0%,rgba(20,8,38,0) 38%,rgba(20,8,38,0) 62%,rgba(20,8,38,.85) 100%)"></div>
<div class="p" style="position:absolute;left:0;right:0;top:26px;text-align:center;font-size:120px">¿UN PERRO</div>
<div class="p g" style="position:absolute;left:0;right:0;bottom:120px;text-align:center;font-size:140px">MANEJANDO?</div>
<div class="k" style="position:absolute;left:50%;bottom:34px;transform:translateX(-50%);font-size:40px;white-space:nowrap">TOP 12 MOMENTOS DE STREAMERS EN GTA 6</div>""")

SH = {
    "s1": ("illo-cara.jpg", "50% 30%", "BORRÓ", "GTA 6", "EN PLENO DIRECTO"),
    "s2": ("explosion.jpg", "50% 50%", "3 STREAMERS", "HUMILLADOS", "GTA 6 · PRIMER DÍA"),
}
for k, (img, pos, l1, l2, kick) in SH.items():
    page(f"portada-{k}", 1080, 1920, f"""<div class="sky"></div>
<img src="{img}" style="position:absolute;left:0;top:0;width:1080px;height:1250px;object-fit:cover;object-position:{pos}">
<div style="position:absolute;left:0;right:0;top:900px;height:360px;background:linear-gradient(180deg,rgba(46,15,74,0),rgba(46,15,74,1))"></div>
<div class="k" style="position:absolute;left:60px;top:1230px;font-size:52px;transform:rotate(-2deg)">{kick}</div>
<div class="p" style="position:absolute;left:0;right:0;top:1340px;text-align:center;font-size:{150 if len(l1) > 8 else 210}px">{l1}</div>
<div class="p g" style="position:absolute;left:0;right:0;top:1560px;text-align:center;font-size:{170 if len(l2) > 8 else 240}px">{l2}</div>""")
