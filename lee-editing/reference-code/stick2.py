import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
src = open("stick.py", encoding="utf-8").read()

NEWBASE = r'''
INKL = (70, 55, 50)
W2 = 1500   # wide static layer
THEMES = [
    (0.0, 5.8, dict(sky=((120, 190, 235), (255, 236, 190)), sun=(820, 380, 90, (255, 245, 200)), hill=(150, 200, 130), ground=(196, 214, 120), mid="villas", pal=((245, 225, 190), (230, 130, 90), (250, 245, 235)), stars=False)),
    (5.8, 17.3, dict(sky=((135, 200, 238), (250, 238, 205)), sun=(260, 330, 80, (255, 248, 210)), hill=(160, 205, 150), ground=(185, 210, 130), mid="city", pal=((235, 215, 180), (205, 110, 90), (245, 240, 228)), stars=False)),
    (17.3, 33.1, dict(sky=((110, 185, 230), (255, 240, 200)), sun=(760, 300, 85, (255, 244, 190)), hill=(140, 195, 135), ground=(205, 205, 120), mid="villas", pal=((250, 230, 200), (225, 140, 80), (255, 250, 240)), stars=False)),
    (33.1, 40.5, dict(sky=((250, 170, 120), (255, 224, 170)), sun=(300, 700, 110, (255, 210, 130)), hill=(190, 165, 125), ground=(200, 180, 120), mid="gov", pal=((240, 215, 180), (180, 90, 70), (250, 240, 225)), stars=False)),
    (40.5, 53.5, dict(sky=((240, 150, 120), (252, 214, 160)), sun=(780, 640, 100, (255, 200, 120)), hill=(185, 150, 120), ground=(196, 168, 112), mid="gov", pal=((236, 208, 176), (170, 84, 66), (248, 236, 220)), stars=False)),
    (53.5, 72.8, dict(sky=((22, 28, 70), (70, 60, 110)), moon=(240, 330, 70), hill=(50, 50, 90), ground=(52, 60, 78), mid="gov", pal=((86, 80, 120), (60, 50, 90), (255, 220, 120)), stars=True)),
    (72.8, 79.4, dict(sky=((120, 90, 150), (245, 160, 140)), sun=(540, 760, 120, (255, 190, 150)), hill=(110, 90, 130), ground=(110, 100, 120), mid="city", pal=((150, 120, 160), (110, 80, 120), (255, 210, 150)), stars=False)),
    (79.4, 99.0, dict(sky=((18, 20, 52), (60, 40, 90)), moon=(800, 330, 80), hill=(40, 40, 80), ground=(42, 44, 66), mid="gov", pal=((70, 66, 108), (50, 44, 84), (255, 210, 110)), stars=True)),
]
WIPES = [t[0] for t in THEMES[1:]]
rng0 = random.Random(7)

def L(d, pts, col=INKL, wd=3): d.line(pts, fill=col + (255,), width=wd, joint="curve")

def house(d, x, y, w, h, wall, roof, light, flat=False, night=False):
    d.rectangle((x, y, x + w, y + h), fill=wall + (255,), outline=INKL + (255,), width=3)
    if flat:
        d.rectangle((x - 6, y - 14, x + w + 6, y), fill=roof + (255,), outline=INKL + (255,), width=3)
    else:
        d.polygon([(x - 10, y), (x + w / 2, y - h * 0.45), (x + w + 10, y)], fill=roof + (255,), outline=INKL + (255,))
    n = max(1, int(w // 70))
    for i in range(n):
        wx = x + 14 + i * (w - 28) / n + 4
        d.rectangle((wx, y + 20, wx + 26, y + 52), fill=(light if night else (170, 215, 235)) + (255,), outline=INKL + (255,), width=2)
    d.rectangle((x + w / 2 - 14, y + h - 52, x + w / 2 + 14, y + h), fill=(120, 80, 60, 255), outline=INKL + (255,), width=2)

def tree(d, x, y, s=1.0, col=(90, 160, 90)):
    d.rectangle((x - 8 * s, y - 80 * s, x + 8 * s, y), fill=(130, 90, 60, 255), outline=INKL + (255,), width=2)
    for dx, dy, r in ((0, -120, 55), (-38, -92, 42), (38, -92, 42), (0, -70, 40)):
        d.ellipse((x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s), fill=col + (255,), outline=INKL + (255,), width=2)

def palm(d, x, y, s=1.0):
    pts = [(x, y), (x + 14 * s, y - 70 * s), (x + 8 * s, y - 140 * s)]
    L(d, pts, (120, 85, 60), int(9 * s))
    top = pts[-1]
    for a in (-160, -120, -75, -30, 15, 200):
        ex = top[0] + math.cos(math.radians(a)) * 80 * s; ey = top[1] + math.sin(math.radians(a)) * 45 * s - 6
        d.polygon([top, ((top[0] + ex) / 2, (top[1] + ey) / 2 - 18 * s), (ex, ey)], fill=(70, 150, 90, 255), outline=INKL + (255,))

def govt(d, cx, y, w, h, pal, night):
    wall, roof, light = pal
    d.rectangle((cx - w / 2, y, cx + w / 2, y + h), fill=wall + (255,), outline=INKL + (255,), width=3)
    d.polygon([(cx - w / 2 - 12, y), (cx, y - 80), (cx + w / 2 + 12, y)], fill=roof + (255,), outline=INKL + (255,))
    cols = 6
    for i in range(cols):
        x = cx - w / 2 + 28 + i * (w - 56) / (cols - 1)
        d.rectangle((x - 8, y + 20, x + 8, y + h - 20), fill=(255, 255, 255, 120) if not night else (130, 120, 170, 200), outline=INKL + (255,), width=2)
    for k in range(4):
        d.rectangle((cx - w / 2 - 14 - k * 10, y + h + k * 10, cx + w / 2 + 14 + k * 10, y + h + k * 10 + 10), fill=(220, 215, 205, 255) if not night else (80, 76, 110, 255), outline=INKL + (255,), width=2)
    d.ellipse((cx - 30, y - 150, cx + 30, y - 90), fill=wall + (255,), outline=INKL + (255,), width=3)
    d.ellipse((cx - 22, y - 142, cx + 22, y - 98), fill=(255, 250, 235, 255) if not night else light + (255,), outline=INKL + (255,), width=2)
    L(d, [(cx, y - 120), (cx, y - 134)]); L(d, [(cx, y - 120), (cx + 12, y - 118)])
    L(d, [(cx + w / 2 - 20, y - 10), (cx + w / 2 - 20, y - 150)], INKL, 3)
    d.polygon([(cx + w / 2 - 20, y - 150), (cx + w / 2 + 34, y - 136), (cx + w / 2 - 20, y - 122)], fill=(235, 120, 40, 255), outline=INKL + (255,))

def cityb(d, x, y, w, h, wall, light, night):
    d.rectangle((x, y, x + w, y + h), fill=wall + (255,), outline=INKL + (255,), width=3)
    for yy in range(int(y + 18), int(y + h - 18), 36):
        for xx in range(int(x + 12), int(x + w - 20), 30):
            on = (rng0.random() < 0.45)
            d.rectangle((xx, yy, xx + 16, yy + 20), fill=(light if (night and on) else (180, 215, 235)) + (255,), outline=INKL + (255,), width=1)

def make_static(th, seed):
    rr = random.Random(seed); global rng0; rng0 = rr
    im = Image.new("RGBA", (W2, 1920), (0, 0, 0, 255)); d = ImageDraw.Draw(im, "RGBA")
    (t1, t2) = th["sky"]
    a = np.linspace(0, 1, 1500)[:, None, None]
    sky = (np.array(t1)[None, None, :] * (1 - a) + np.array(t2)[None, None, :] * a)
    sk = np.repeat(sky, W2, axis=1).astype(np.uint8)
    full = np.zeros((1920, W2, 3), np.uint8); full[:1500] = sk; full[1500:] = np.array(t2)
    im = Image.fromarray(full).convert("RGBA"); d = ImageDraw.Draw(im, "RGBA")
    if "sun" in th:
        x, y, r, c = th["sun"]
        g = Image.new("RGBA", (W2, 1920), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse((x - r * 2.4, y - r * 2.4, x + r * 2.4, y + r * 2.4), fill=c + (90,)); g = g.filter(ImageFilter.GaussianBlur(40)); im.alpha_composite(g)
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (255,), outline=(255, 255, 255, 120), width=4)
    if "moon" in th:
        x, y, r = th["moon"]
        g = Image.new("RGBA", (W2, 1920), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse((x - r * 2, y - r * 2, x + r * 2, y + r * 2), fill=(255, 245, 200, 70)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(35)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 240, 205, 255), outline=INKL + (255,), width=3)
        d.ellipse((x - r * .4, y - r * .5, x - r * .1, y - r * .2), fill=(228, 216, 180, 255))
    # hills
    pts = [(0, 1920)]
    for x in range(0, W2 + 60, 60): pts.append((x, 1170 + 60 * math.sin(x / 210 + seed) + 30 * math.sin(x / 90)))
    pts.append((W2, 1920)); d.polygon(pts, fill=th["hill"] + (255,)); L(d, pts[1:-1], INKL, 3)
    night = th["stars"]
    pal = th["pal"]
    gy = 1380
    if th["mid"] == "villas":
        x = 20
        while x < W2 - 120:
            w = rr.choice([150, 180, 210]); h = rr.choice([150, 190, 230])
            house(d, x, gy - h, w, h, pal[0], pal[1], pal[2], flat=rr.random() < .4, night=night)
            x += w + rr.choice([40, 70, 110])
            if rr.random() < .5: palm(d, x - 25, gy, rr.uniform(.9, 1.3)); x += 60
    elif th["mid"] == "city":
        x = 10
        while x < W2 - 100:
            w = rr.choice([110, 140, 170]); h = rr.choice([260, 340, 430, 520])
            cityb(d, x, gy - h, w, h, pal[0] if rr.random() < .5 else pal[1], pal[2], night); x += w + rr.choice([8, 20])
        govt(d, 760, gy - 280, 330, 280, (pal[0], pal[1], pal[2]), night)
    else:
        govt(d, 640, gy - 330, 520, 330, pal, night)
        for tx in (140, 1210): tree(d, tx, gy + 20, 1.2, (80, 150, 90) if not night else (50, 90, 90))
    # ground
    d.rectangle((0, gy, W2, 1920), fill=th["ground"] + (255,)); L(d, [(0, gy), (W2, gy)], INKL, 4)
    for i in range(160):
        gx = rr.uniform(0, W2); gyy = rr.uniform(gy + 30, 1900); hh = rr.uniform(10, 26)
        L(d, [(gx, gyy), (gx - 4, gyy - hh)], tuple(max(0, c - 40) for c in th["ground"]), 3); L(d, [(gx, gyy), (gx + 5, gyy - hh * .8)], tuple(max(0, c - 40) for c in th["ground"]), 3)
    # path
    d.polygon([(560, gy), (700, gy), (900, 1920), (360, 1920)], fill=tuple(min(255, c + 25) for c in th["ground"]) + (110,))
    return im.convert("RGB")

def make_clouds(night):
    im = Image.new("RGBA", (2600, 700), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rr = random.Random(3)
    for i in range(9):
        x = rr.uniform(0, 2400); y = rr.uniform(40, 560); s = rr.uniform(.7, 1.5)
        col = (255, 255, 255, 235) if not night else (120, 120, 170, 170)
        for dx, dy, r in ((0, 0, 50), (55, 12, 42), (-55, 14, 38), (28, -22, 40)):
            d.ellipse((x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s), fill=col)
        d.rectangle((x - 95 * s, y + 4 * s, x + 95 * s, y + 52 * s), fill=col)
    return im

def make_noise():
    rr = np.random.RandomState(5)
    n = rr.rand(48, 27)
    img = Image.fromarray((n * 255).astype(np.uint8)).resize((1080, 1920), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    a = np.asarray(img).astype(np.float32) / 255
    a = (a - a.min()) / (a.max() - a.min())
    grain = (np.random.RandomState(9).rand(1920, 1080) * 255).astype(np.uint8)
    return a, Image.fromarray(grain).convert("RGB")

def render_base2():
    statics = [make_static(th, i + 1) for i, (_, _, th) in enumerate(THEMES)]
    clouds = [make_clouds(th["stars"]) for (_, _, th) in THEMES]
    blot, grain = make_noise()
    grain_a = Image.new("L", (1080, 1920), 14)
    papercol = np.array([248, 247, 240], np.float32)
    star_rr = random.Random(11); STARS = [(star_rr.uniform(0, 1080), star_rr.uniform(0, 1000), star_rr.uniform(1.5, 3.5), star_rr.uniform(0, 6)) for _ in range(70)]
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
           "-i", PROJ + "/raw video.MOV", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(TLIM or 83.8), "base_s.mp4"]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int((TLIM or 83.8) * FPS)
    for f in range(n):
        t = f / FPS
        idx = max(i for i, (a, b, _) in enumerate(THEMES) if a <= t)
        a0, b0, th = THEMES[idx]
        # parallax pan of static layer
        off = int(210 + 120 * math.sin(t * 0.35 + idx) + (t - a0) * 6)
        off = max(0, min(W2 - 1080, off))
        fr = statics[idx].crop((off, 0, off + 1080, 1920))
        fr = fr.convert("RGBA")
        cl = clouds[idx]; cx = int((t * 28) % 1500)
        fr.alpha_composite(cl.crop((cx, 0, cx + 1080, 700)), (0, 60 + int(10 * math.sin(t))))
        if th["stars"]:
            d = ImageDraw.Draw(fr, "RGBA")
            for sx, sy, sr, ph in STARS:
                al = int(120 + 120 * math.sin(t * 2 + ph))
                d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=(255, 250, 220, max(40, al)))
        fr = fr.convert("RGB")
        # wipe transition (paper cloud wipe)
        dist = min([abs(t - w) for w in WIPES] + [9])
        if dist < 0.45:
            c = 1 - dist / 0.45
            c = c * c * (3 - 2 * c)
            al = np.clip(c * 1.7 - blot * 0.7, 0, 1)[..., None]
            arr = np.asarray(fr).astype(np.float32)
            arr = arr * (1 - al) + papercol * al
            fr = Image.fromarray(arr.astype(np.uint8))
        fr.paste(grain, (0, 0), grain_a)
        ch = render_char(f)
        fr.paste(ch, (0, Y0), ch)
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait()
'''

marker = "def render_base():"
src = src.replace(marker, NEWBASE + "\n" + marker, 1)
src = src.replace("    render_base()\n    if ONLY_BASE", "    render_base2()\n    if ONLY_BASE", 1)
src = src.replace('"cards_s/"', '"cards_s/"')
g = {"__name__": "__main__", "__file__": os.path.join(HERE, "stick.py")}
exec(compile(src, "stick_run", "exec"), g)
