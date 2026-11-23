"""Hoja de contactos de cuadros sueltos: python3 hoja.py salida.jpg video:t video:t ...  (o video:a-b para 1 fps)"""
import subprocess, sys
from PIL import Image, ImageDraw
out, specs = sys.argv[1], sys.argv[2:]
cuadros = []
for s in specs:
    v, t = s.rsplit(":", 1)
    ts = [float(t)] if "-" not in t else [x for x in range(int(float(t.split("-")[0])), int(float(t.split("-")[1])) + 1)]
    for x in ts:
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(x), "-i", f"video/{v}.mp4" if "/" not in v else v, "-frames:v", "1",
                            "-vf", "scale=320:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if r.stdout:
            import io
            cuadros.append((f"{v.split('/')[-1]} {x}", Image.open(io.BytesIO(r.stdout)).convert("RGB")))
cols = 6
w = 320; h = max(i.height for _, i in cuadros) + 22
img = Image.new("RGB", (cols * w, ((len(cuadros) + cols - 1) // cols) * h), "black")
d = ImageDraw.Draw(img)
for k, (lab, im) in enumerate(cuadros):
    x, y = (k % cols) * w, (k // cols) * h
    img.paste(im, (x, y)); d.text((x + 4, y + im.height + 4), lab, fill="yellow")
img.save(out, quality=75)
