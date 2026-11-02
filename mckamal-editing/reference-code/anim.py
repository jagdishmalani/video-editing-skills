import sys; sys.path.insert(0, ".")
import os, math, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

B = os.path.dirname(os.path.abspath(__file__)); os.chdir(B)
A = "C:/Users/jagdi/Downloads/kamal 1q23/assets"
W, H = 1080, 900
FPS = 30
DUR = 69.6
INK = (40, 32, 32); WHITE = (255, 255, 255)
RED = (214, 59, 47); GREEN = (40, 160, 90); YEL = (255, 208, 70); BLUE = (60, 120, 200); PINK = (235, 110, 160)
SPLITS = [(5.3, 14.9), (17.4, 26.5), (37.0, 50.5), (55.4, 65.5)]
S2 = 2
FB = "fonts/NotoSans-Bold.ttf"
def fnt(sz): return ImageFont.truetype(FB, sz)
def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def pop(u):   # 0..1 with overshoot
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    return 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2 if False else sm(u) * (1 + 0.25 * math.sin(u * math.pi))

# ------------------------------------------------------------ static backgrounds
def grad(top, bot, h=H):
    a = np.linspace(0, 1, h)[:, None, None]
    return np.repeat((np.array(top)[None, None, :] * (1 - a) + np.array(bot)[None, None, :] * a), W, axis=1).astype(np.uint8)

def L(d, pts, col=INK, wd=3): d.line(pts, fill=col + (255,), width=wd, joint="curve")

def grass(d, y0, y1, col, n=120, seed=1):
    rr = random.Random(seed); dk = tuple(max(0, c - 40) for c in col)
    for _ in range(n):
        x = rr.uniform(0, W); y = rr.uniform(y0, y1); h = rr.uniform(8, 20)
        L(d, [(x, y), (x - 4, y - h)], dk, 3); L(d, [(x, y), (x + 5, y - h * .8)], dk, 3)

def tree(d, x, y, s=1.0, col=(90, 160, 90)):
    d.rectangle((x - 8 * s, y - 90 * s, x + 8 * s, y), fill=(130, 90, 60, 255), outline=INK + (255,), width=2)
    for dx, dy, r in ((0, -130, 58), (-40, -100, 44), (40, -100, 44), (0, -78, 42)):
        d.ellipse((x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s), fill=col + (255,), outline=INK + (255,), width=2)

def bg_school():
    im = Image.fromarray(grad((120, 190, 235), (255, 238, 200))).convert("RGBA"); d = ImageDraw.Draw(im)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((130, 40, 330, 240), fill=(255, 245, 190, 200)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(30)))
    d.ellipse((190, 100, 270, 180), fill=(255, 247, 200, 255), outline=INK + (255,), width=3)
    pts = [(0, H)] + [(x, 560 + 40 * math.sin(x / 170)) for x in range(0, W + 40, 40)] + [(W, H)]
    d.polygon(pts, fill=(150, 200, 130, 255))
    d.rectangle((60, 270, 620, 650), fill=(245, 225, 190, 255), outline=INK + (255,), width=4)
    d.rectangle((40, 240, 640, 290), fill=(205, 100, 80, 255), outline=INK + (255,), width=4)
    d.rectangle((210, 180, 470, 245), fill=(250, 245, 235, 255), outline=INK + (255,), width=4)
    d.text((340, 212), "SCHOOL", font=fnt(46), fill=INK, anchor="mm")
    for r in range(2):
        for c in range(5):
            x = 100 + c * 105; y = 330 + r * 120
            d.rectangle((x, y, x + 70, y + 80), fill=(170, 215, 235, 255), outline=INK + (255,), width=3); L(d, [(x + 35, y), (x + 35, y + 80)], INK, 2)
    d.rectangle((300, 520, 380, 650), fill=(120, 80, 60, 255), outline=INK + (255,), width=3)
    L(d, [(560, 270), (560, 120)], INK, 5); d.polygon([(560, 120), (630, 140), (560, 160)], fill=(235, 120, 40, 255), outline=INK + (255,))
    d.rectangle((0, 650, W, H), fill=(190, 212, 120, 255)); L(d, [(0, 650), (W, 650)], INK, 4); grass(d, 670, 890, (190, 212, 120))
    tree(d, 900, 660, 1.3)
    return im.convert("RGB")

def bg_class():
    im = Image.new("RGBA", (W, H), (248, 232, 200, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 640, W, H), fill=(196, 150, 100, 255)); L(d, [(0, 640), (W, 640)], INK, 4)
    for x in range(-100, W + 200, 140): L(d, [(x, 640), (x - 90, H)], (150, 110, 70), 3)
    d.rectangle((90, 90, 720, 400), fill=(60, 90, 70, 255), outline=(120, 80, 50, 255), width=14); d.rectangle((90, 90, 720, 400), outline=INK + (255,), width=3)
    d.text((250, 190), "A  B  C", font=fnt(70), fill=(240, 240, 235), anchor="mm"); d.text((520, 290), "1 + 2 = 3", font=fnt(60), fill=(240, 240, 235), anchor="mm")
    d.rectangle((780, 110, 1000, 310), fill=(170, 215, 240, 255), outline=INK + (255,), width=5); L(d, [(890, 110), (890, 310)], INK, 4); L(d, [(780, 210), (1000, 210)], INK, 4)
    d.rectangle((900, 330, 1040, 650), fill=(130, 90, 60, 255), outline=INK + (255,), width=4); d.ellipse((1010, 490, 1026, 506), fill=(255, 215, 90, 255))
    for x in (60, 330):
        d.rectangle((x, 600, x + 180, 640), fill=(180, 130, 80, 255), outline=INK + (255,), width=3)
        L(d, [(x + 15, 640), (x + 15, 760)], INK, 5); L(d, [(x + 165, 640), (x + 165, 760)], INK, 5)
    return im.convert("RGB")

def bg_ecg():
    im = Image.new("RGB", (W, H), (28, 8, 18)); d = ImageDraw.Draw(im, "RGBA")
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(120, 30, 40, 70), width=1)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(120, 30, 40, 70), width=1)
    return im

def bg_judge():
    im = Image.fromarray(grad((90, 70, 140), (250, 170, 130))).convert("RGBA"); d = ImageDraw.Draw(im)
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((380, 320, 700, 640), fill=(255, 200, 150, 200)); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
    rr = random.Random(4)
    x = 0
    while x < W:
        w = rr.choice([90, 120, 150]); h = rr.choice([180, 260, 340]); d.rectangle((x, 650 - h, x + w, 650), fill=(95, 75, 125, 255), outline=INK + (255,), width=3)
        for yy in range(650 - h + 20, 640, 40):
            for xx in range(x + 14, x + w - 20, 30):
                if rr.random() < .4: d.rectangle((xx, yy, xx + 14, yy + 18), fill=(255, 220, 130, 255))
        x += w + 10
    d.rectangle((0, 650, W, H), fill=(110, 95, 130, 255)); L(d, [(0, 650), (W, 650)], INK, 4)
    return im.convert("RGB")

def bg_home():
    im = Image.new("RGBA", (W, H), (252, 236, 205, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 650, W, H), fill=(205, 160, 115, 255)); L(d, [(0, 650), (W, 650)], INK, 4)
    d.rectangle((90, 120, 330, 380), fill=(170, 215, 240, 255), outline=INK + (255,), width=5); L(d, [(210, 120), (210, 380)], INK, 4)
    d.polygon([(60, 100), (150, 100), (130, 400), (60, 400)], fill=(235, 130, 110, 255), outline=INK + (255,)); d.polygon([(270, 100), (360, 100), (360, 400), (290, 400)], fill=(235, 130, 110, 255), outline=INK + (255,))
    d.rectangle((760, 140, 980, 300), fill=(250, 245, 235, 255), outline=(120, 80, 50, 255), width=10); d.ellipse((840, 170, 900, 230), fill=(255, 210, 90, 255), outline=INK + (255,), width=3)
    d.rectangle((700, 520, 1060, 650), fill=(120, 150, 200, 255), outline=INK + (255,), width=4); d.rectangle((680, 470, 760, 650), fill=(105, 135, 185, 255), outline=INK + (255,), width=4)
    return im.convert("RGB")

BGS = {"school": bg_school(), "class": bg_class(), "ecg": bg_ecg(), "judge": bg_judge(), "home": bg_home()}

# ------------------------------------------------------------ person
L1, L2 = 135, 125
def ik(sh, tg):
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]; d = math.hypot(dx, dy); d = max(40, min(d, L1 + L2 - 2)); a = math.atan2(dy, dx)
    b = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    e1 = (sh[0] + L1 * math.cos(a - b), sh[1] + L1 * math.sin(a - b)); e2 = (sh[0] + L1 * math.cos(a + b), sh[1] + L1 * math.sin(a + b))
    return (e1 if e1[1] > e2[1] else e2), (sh[0] + d * math.cos(a), sh[1] + d * math.sin(a))

def person(d, cx, fy, k, t, lh=(-150, 120), rh=(150, 120), mood="neutral", face=1, walk=0.0, lean=0.0, acc=None, seed=0, bend=0.0):
    k = k * 1.28
    rnd = random.Random(int(t * 12) + seed)
    def P(x, y): return ((cx + x * face * k) * S2, (fy + y * k) * S2)
    def J(x, y, a=2.0): return (x + rnd.uniform(-a, a), y + rnd.uniform(-a, a))
    wd = max(4, 7 * k * 1.15)
    strokes = []
    hip = (lean * .3, -300 + bend * 90); neck = (lean, -550 + bend * 120); sh = (lean, -515 + bend * 110)
    # legs
    for sd in (-1, 1):
        ph = math.sin(walk * 6.0 + (0 if sd < 0 else math.pi)) if walk else 0
        foot = (sd * 60 + ph * 70, -max(0, ph) * 30 * (1 if walk else 0)); knee = ((hip[0] + foot[0]) / 2 + sd * 14, (hip[1] + foot[1]) / 2 - bend * 40)
        strokes.append(([J(*hip, 1), J(*knee, 1.5), J(*foot, 1)], wd)); strokes.append(([foot, (foot[0] + 34, foot[1] + 2)], wd + 2))
    strokes.append(([J(*neck, 1), J(lean * .6, (-550 - 300) / 2 + bend * 100, 1.5), J(*hip, 1)], wd))
    hands = []
    for tg in (lh, rh):
        e, h = ik(sh, (sh[0] + tg[0], sh[1] + tg[1]))
        strokes.append(([sh, J(*e, 1.5), J(*h, 1.5)], wd)); hands.append(h)
    for pts, w in strokes: d.line([P(*p) for p in pts], fill=WHITE + (255,), width=int((w + 7) * S2), joint="curve")
    for pts, w in strokes:
        q = [P(*p) for p in pts]; d.line(q, fill=INK + (255,), width=int(w * S2), joint="curve")
        for p in (q[0], q[-1]): d.ellipse((p[0] - w * S2 / 2, p[1] - w * S2 / 2, p[0] + w * S2 / 2, p[1] + w * S2 / 2), fill=INK + (255,))
    for h in hands:
        x, y = P(*h); r = 11 * k * S2 * 1.3; d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE + (255,), outline=INK + (255,), width=int(3 * S2 * max(.7, k)))
    # head
    hc = (neck[0] + lean * .4, -635 + bend * 120); R = 80
    x, y = P(*hc); r = R * k * S2
    d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=WHITE + (255,))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 252, 246, 255), outline=INK + (255,), width=int(wd * S2 * .9))
    def F(dx, dy): return P(hc[0] + dx * face, hc[1] + dy)
    es = {"scared": (10, 17), "angry": (8, 8), "sad": (8, 11), "shout": (9, 13)}.get(mood, (8, 12)); blink = (int(t * 30) % 90) < 3
    for ex in (-30, 30):
        px, py = F(ex, -8); ry = 2 if blink else es[1]; d.ellipse((px - es[0] * k * S2, py - ry * k * S2, px + es[0] * k * S2, py + ry * k * S2), fill=INK + (255,))
    bw = max(3, int(6 * k * S2))
    if mood == "angry": d.line([F(-48, -50), F(-14, -30)], fill=INK + (255,), width=bw); d.line([F(14, -30), F(48, -50)], fill=INK + (255,), width=bw)
    elif mood == "scared": d.line([F(-46, -42), F(-16, -50)], fill=INK + (255,), width=bw); d.line([F(16, -50), F(46, -42)], fill=INK + (255,), width=bw)
    elif mood == "sad": d.line([F(-46, -30), F(-16, -42)], fill=INK + (255,), width=bw); d.line([F(16, -42), F(46, -30)], fill=INK + (255,), width=bw)
    mx, my = F(0, 38)
    if mood in ("scared", "shout"):
        o = 0.5 + 0.5 * abs(math.sin(t * 9)); rx = 14 * k * S2 + 8 * o * k * S2; ry = (8 + 24 * o) * k * S2; d.ellipse((mx - rx, my - ry, mx + rx, my + ry), fill=INK + (255,))
    elif mood == "angry": d.line([F(-20, 44), F(0, 36), F(20, 44)], fill=INK + (255,), width=bw)
    elif mood == "sad": d.arc((mx - 22 * k * S2, my, mx + 22 * k * S2, my + 24 * k * S2), 200, 340, fill=INK + (255,), width=bw)
    elif mood == "happy": d.arc((mx - 26 * k * S2, my - 14 * k * S2, mx + 26 * k * S2, my + 14 * k * S2), 15, 165, fill=INK + (255,), width=bw)
    else: d.line([F(-16, 40), F(16, 40)], fill=INK + (255,), width=bw)
    if mood == "scared":
        sx, sy = F(70, -30 + (t * 90 % 60)); d.ellipse((sx - 8 * k * S2, sy - 12 * k * S2, sx + 8 * k * S2, sy + 12 * k * S2), fill=(120, 190, 235, 255))
    if mood == "angry":
        ax, ay = F(66, -70)
        for a_, b_ in ((-1, -1, 1, 1), (1, -1, -1, 1)) if False else (((-14, -14), (14, 14)), ((14, -14), (-14, 14))):
            d.line([(ax + a_[0] * k * S2 * 1.3, ay + a_[1] * k * S2 * 1.3), (ax + b_[0] * k * S2 * 1.3, ay + b_[1] * k * S2 * 1.3)], fill=RED + (255,), width=bw)
    # accessories
    if acc == "cap":
        d.pieslice((x - r, y - r, x + r, y + r), 180, 360, fill=BLUE + (255,), outline=INK + (255,), width=int(3 * S2 * k))
        d.rectangle((x + (0 if face > 0 else -r * 1.5), y - 6 * k * S2, x + (r * 1.5 if face > 0 else 0), y + 4 * k * S2), fill=BLUE + (255,), outline=INK + (255,), width=int(2 * S2))
    elif acc == "bow":
        for sd in (-1, 1): d.polygon([(x + 30 * k * S2 * face, y - r * .9), (x + (30 + sd * 46) * k * S2 * face, y - r * 1.15), (x + (30 + sd * 46) * k * S2 * face, y - r * .7)], fill=PINK + (255,), outline=INK + (255,))
    elif acc == "bun":
        d.ellipse((x - 26 * k * S2, y - r - 34 * k * S2, x + 26 * k * S2, y - r + 14 * k * S2), fill=(90, 60, 50, 255), outline=INK + (255,), width=int(3 * S2 * k))
    elif acc == "tie":
        tx, ty = P(lean * .9, -490 + bend * 110); d.polygon([(tx - 12 * k * S2, ty), (tx + 12 * k * S2, ty), (tx + 8 * k * S2, ty + 90 * k * S2), (tx, ty + 110 * k * S2), (tx - 8 * k * S2, ty + 90 * k * S2)], fill=RED + (255,), outline=INK + (255,))
    elif acc == "hat":
        d.rectangle((x - r * 1.1, y - r * 1.02, x + r * 1.1, y - r * .88), fill=GREEN + (255,), outline=INK + (255,), width=int(3 * S2 * k)); d.rectangle((x - r * .62, y - r * 1.6, x + r * .62, y - r * 1.0), fill=GREEN + (255,), outline=INK + (255,), width=int(3 * S2 * k))
    return [(( cx + h[0] * face * k), (fy + h[1] * k)) for h in hands], (cx + hc[0] * face * k, fy + hc[1] * k)

# ------------------------------------------------------------ props
def tag(d, x, y, text, col=YEL, sz=40, rot=0, s=1.0):
    if s < 0.05: return
    f = fnt(int(sz * S2 * s)); w = d.textlength(text, font=f); h = sz * S2 * s * 1.5
    X, Y = x * S2, y * S2
    d.rounded_rectangle((X - w / 2 - 24, Y - h / 2, X + w / 2 + 24, Y + h / 2), 14, fill=(253, 248, 232, 255), outline=INK + (255,), width=int(3 * S2))
    d.rectangle((X - w / 2 - 24, Y - h / 2 - 8, X + w / 2 + 24, Y - h / 2 + 10), fill=col + (230,))
    d.text((X, Y + 3), text, font=f, fill=INK, anchor="mm")

def heart(d, x, y, r, col=RED, wob=0):
    X, Y, R = x * S2, y * S2, r * S2
    d.ellipse((X - R * 1.0, Y - R * .9, X, Y + R * .1), fill=col + (255,)); d.ellipse((X, Y - R * .9, X + R * 1.0, Y + R * .1), fill=col + (255,))
    d.polygon([(X - R * 1.0, Y - R * .3), (X + R * 1.0, Y - R * .3), (X, Y + R * 1.05)], fill=col + (255,))

def bigx(d, x, y, r, col=RED, wd=16):
    X, Y, R = x * S2, y * S2, r * S2
    d.line([(X - R, Y - R), (X + R, Y + R)], fill=col + (255,), width=wd * S2); d.line([(X + R, Y - R), (X - R, Y + R)], fill=col + (255,), width=wd * S2)

def alert(d, x, y, s, t):
    k = 1 + 0.08 * math.sin(t * 10); X, Y = x * S2, y * S2; R = 70 * s * k * S2
    d.polygon([(X, Y - R), (X + R * .95, Y + R * .7), (X - R * .95, Y + R * .7)], fill=RED + (255,), outline=INK + (255,)); d.line([(X, Y - R * .35), (X, Y + R * .22)], fill=WHITE + (255,), width=int(12 * S2 * s)); d.ellipse((X - 7 * S2 * s, Y + R * .38, X + 7 * S2 * s, Y + R * .38 + 14 * S2 * s), fill=WHITE + (255,))

def cloud(d, x, y, s=1.0):
    for dx, dy, r in ((0, 0, 40), (45, 10, 34), (-45, 12, 30), (22, -18, 32)): d.ellipse(((x + dx - r * s) * S2, (y + dy - r * s) * S2, (x + dx + r * s) * S2, (y + dy + r * s) * S2), fill=(255, 255, 255, 240))
    d.rectangle(((x - 75 * s) * S2, (y + 4 * s) * S2, (x + 75 * s) * S2, (y + 44 * s) * S2), fill=(255, 255, 255, 240))

def phone(d, x, y, s=1.0, rot=0):
    if s < 0.3: return
    X, Y = x * S2, y * S2; w, h = 50 * s * S2, 90 * s * S2
    d.rounded_rectangle((X - w / 2, Y - h / 2, X + w / 2, Y + h / 2), 8 * S2, fill=(30, 32, 44, 255), outline=WHITE + (255,), width=3 * S2); d.rectangle((X - w / 2 + 6 * S2, Y - h / 2 + 10 * S2, X + w / 2 - 6 * S2, Y + h / 2 - 14 * S2), fill=(80, 140, 220, 255))

def polaroid(path, w, h, ang, focus=(0.5, 0.5)):
    m = 14; p = Image.open(path).convert("RGBA"); iw, ih = w - 2 * m, h - 2 * m
    sc = max(iw / p.width, ih / p.height); p = p.resize((int(p.width * sc) + 1, int(p.height * sc) + 1), Image.LANCZOS)
    x = int((p.width - iw) * focus[0]); y = int((p.height - ih) * focus[1]); p = p.crop((x, y, x + iw, y + ih))
    im = Image.new("RGBA", (w, h + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 26, w - 1, h + 25), fill=(255, 255, 255, 255), outline=INK + (255,), width=3); im.alpha_composite(p, (m, 26 + m))
    t = Image.new("RGBA", (110, 34), YEL + (200,)); im.alpha_composite(t, (w // 2 - 55, 6))
    return im.rotate(ang, expand=True, resample=Image.BICUBIC)
POL_A = polaroid(A + "/images/panchkula_sector17.jpg", 330, 240, 3, (0.5, 0.45))
POL_B = polaroid(A + "/images/anantapur_clock_tower.jpg", 330, 240, -3, (0.5, 0.4))

# ------------------------------------------------------------ scenes
def clouds_layer(d, t, n=3, y0=90):
    for i in range(n): cloud(d, (i * 420 + t * 26) % 1500 - 200, y0 + 40 * (i % 2) + 6 * math.sin(t + i), 0.9 + 0.2 * (i % 2))

def scene_A(t, base, d):
    u = t - 5.3; clouds_layer(d, t, 3)
    pu = pop((u - 0.3) / 0.6)
    if pu > 0:
        base_im = POL_A
        base.alpha_composite(base_im, (680, int(30 - (1 - pu) * 320)))
    # girl and boy
    gx = 330; gm = "neutral" if t < 8.5 else "scared"
    glh = (-150, 120); grh = (150, 120)
    if t >= 8.5: glh = (-130, -120 + 10 * math.sin(t * 18)); grh = (130, -120 - 10 * math.sin(t * 18))
    gs = pop((u - 0.6) / 0.5)
    if gs > 0.01: person(d, gx, 700, 0.40 * gs, t, glh, grh, gm, face=1, acc="bow", seed=1)
    # boy walks in
    bx = 930 - 330 * sm((t - 7.0) / 1.7) if t >= 7.0 else 1250
    bm = "angry" if t >= 8.6 else "neutral"; walking = 6.0 < t < 8.7
    blh = (-150, 120); brh = (150, 120)
    if t >= 8.7: brh = (-120 + 8 * math.sin(t * 20), -60); blh = (-90, 30)
    if bx < 1200: person(d, bx, 700, 0.43, t, blh, brh, bm, face=-1, walk=(t * 1.0 if walking else 0), acc="cap", seed=2)
    if t >= 7.0: tag(d, bx - 10 if bx < 1200 else 930, 360, "8 YRS", YEL, 34, s=min(1, pop((t - 7.0) / 0.4)))
    if t >= 8.55: tag(d, gx, 395, "6 YRS", PINK, 34, s=min(1, pop((t - 8.55) / 0.4)))
    if 11.3 <= t < 13.1: alert(d, 560, 250, 1.0, t)
    if t >= 13.1:
        pu2 = pop((t - 13.1) / 0.5); X, Y = 540 * S2, 300 * S2; R = 105 * pu2 * (1 + .05 * math.sin(t * 8)) * S2
        d.ellipse((X - R, Y - R, X + R, Y + R), fill=(25, 27, 40, 255), outline=RED + (255,), width=10 * S2)
        d.polygon([(X - R * .3, Y - R * .45), (X - R * .3, Y + R * .45), (X + R * .5, Y)], fill=WHITE + (255,))
        tag(d, 540, 470, "VIDEO", RED, 36, s=min(1, pu2))

def scene_B(t, base, d, dim):
    u = t - 17.4; clouds_layer(d, t, 0)
    pu = pop((u - 0.2) / 0.6)
    if pu > 0: base.alpha_composite(POL_B, (700, int(30 - (1 - pu) * 320)))
    gx = 480
    gm = "scared" if t >= 21.4 else ("angry" if 19.2 <= t < 20.1 else "neutral")
    glh = (-150, 120); grh = (150, 120)
    if t >= 21.4: glh = (-120, -110 + 8 * math.sin(t * 20)); grh = (120, -110 - 8 * math.sin(t * 20))
    face = 1;
    gs = pop((u - 0.2) / 0.5)
    if gs > 0.01: person(d, gx, 720, 0.52 * gs, t, glh, grh, gm, face=-1, acc="bun", seed=3, lean=(8 * math.sin(t * 14) if 19.2 <= t < 20.1 else 0))
    if t < 18.4: bx = 180
    elif t < 20.1: bx = 210
    elif t < 21.3: bx = 210 + 740 * sm((t - 20.1) / 1.2)
    elif t < 21.4: bx = 1300
    elif t < 22.4: bx = 1000 - 460 * sm((t - 21.4) / 1.0)
    else: bx = 540 + 6 * math.sin(t * 18)
    walking = (20.1 < t < 21.3) or (21.4 < t < 22.4)
    facing = 1 if t < 20.1 or (21.4 <= t) and False else 1
    face_b = 1 if (t < 20.1) else (-1 if t < 21.4 else -1)
    if 20.1 <= t < 21.3: face_b = 1
    bm = "angry" if t >= 20.1 else "happy"
    blh = (-150, 120); brh = (150, 120)
    if 18.4 <= t < 20.1: brh = (200, -80)
    elif t >= 22.4: brh = (-130 + 10 * math.sin(t * 22), -60); blh = (-100, 20)
    if bx < 1250: (hands, hc) = person(d, bx, 720, 0.52, t, blh, brh, bm, face=face_b, walk=(t if walking else 0), acc="cap", seed=4)
    if 18.4 <= t < 20.1: heart(d, 330 + 6 * math.sin(t * 8), 380, 42, RED)
    if 19.3 <= t < 20.1: bigx(d, 330, 390, 60, RED, 18)
    if 19.2 <= t < 20.1: tag(d, 480, 300, "NO!", RED, 40, s=min(1, pop((t - 19.2) / 0.3)))
    if t >= 17.4: tag(d, 480, 360, "14 YRS", PINK, 32, s=min(1, pop((t - 17.6) / 0.4))) if t < 18.4 else None
    if 22.9 <= t < 24.45:
        for i, x in enumerate((140, 940)): alert(d, x, 200 + 30 * (i % 2), 0.9, t + i)
    dim[0] = 0.25 * (0.5 + 0.5 * math.sin(t * 12)) if 22.9 <= t < 24.45 else 0

def scene_ecg(t, base, d):
    u = t - 24.5; X0 = 40
    pts = []; N = 220
    for i in range(N):
        x = X0 + i * (W - 80) / (N - 1); ph = (i / 18.0 - u * 1.6) % 1.0
        amp = max(0.12, 1.0 - u * 0.34)
        if ph < 0.12: yv = 0
        elif ph < 0.16: yv = -60 * amp
        elif ph < 0.2: yv = 140 * amp
        elif ph < 0.26: yv = -180 * amp
        elif ph < 0.30: yv = 40 * amp
        else: yv = 0
        pts.append((x * S2, (450 + yv) * S2))
    d.line(pts, fill=(80, 255, 140, 255), width=8 * S2, joint="curve")
    s = 1 + 0.12 * abs(math.sin(u * 5)); heart(d, 540, 250, 90 * s, RED)
    tag(d, 540, 700, "LIFE AT RISK", RED, 56, s=min(1, pop(u / 0.4)))

def scene_C(t, base, d):
    u = t - 37.0
    # lone girl
    gm = "sad" if t < 45.4 else "scared"
    gs = pop((u - 0.1) / 0.5)
    if gs > .01: person(d, 540, 720, 0.52 * gs, t, (-100, 140), (100, 140), gm, face=1, acc="bun", seed=5)
    crowd = [(110, 0.40), (260, 0.40), (820, 0.40), (970, 0.40)]
    for i, (x, k) in enumerate(crowd):
        ap = pop((t - (37.2 + 0.25 * i)) / 0.4)
        if ap < 0.01: continue
        angry = t >= 45.4
        sh = 8 * math.sin(t * 18 + i) if t >= 47.3 else 0
        rh = (-40, -150) if (t < 45.4 or True) else (0, 0)
        face = 1 if x < 540 else -1
        person(d, x, 700, k * ap, t, (-60, 90), (160 + sh, -60 + 14 * math.sin(t * 3 + i)), "angry" if angry else "shout", face=face, acc=("hat", "cap", "cap", "hat")[i], seed=10 + i)
        if not angry:
            px = x + (60 if face > 0 else -60); phone(d, px, 540 + 10 * math.sin(t * 4 + i), 0.9 * ap)
    # speech bubbles
    if 37.5 <= t < 41.3:
        for i, (x, txt) in enumerate(((160, "JUDGE!"), (900, "VERDICT?"))):
            if t >= 37.6 + 0.4 * i: tag(d, x, 330 + 14 * math.sin(t * 3 + i), txt, YEL, 34, s=min(1, pop((t - 37.6 - .4 * i) / 0.35)))
        if t >= 38.5:
            gx, gy = 540 * S2, 250 * S2; d.rectangle((gx - 70 * S2, gy - 30 * S2, gx + 20 * S2, gy + 10 * S2), fill=(140, 90, 55, 255), outline=INK + (255,), width=3 * S2); L(d, [(gx - 25 * S2, gy + 10 * S2), (gx + 60 * S2, gy + 70 * S2)], (140, 90, 55), 12 * S2)
    if 41.4 <= t < 45.3:
        tag(d, 540, 250, "\"Aajkal ki ladkiyan...\"", WHITE, 34, s=min(1, pop((t - 41.4) / 0.4)))
        bigx(d, 540, 460, 50, RED, 14)
    if 45.4 <= t < 47.3:
        tag(d, 540, 240, "HUM KHUD?", RED, 46, s=min(1, pop((t - 45.4) / 0.4)))
    if t >= 47.3:
        for i, (x, w, col) in enumerate(((220, "CASTE", (230, 120, 60)), (540, "GENDER", (200, 90, 160)), (860, "RELIGION", (90, 150, 220)))):
            tt = 47.4 + 0.8 * i
            if t >= tt: tag(d, x, 170 + 16 * math.sin(t * 5 + i), w, col, 42, s=min(1, pop((t - tt) / 0.4)))

def scene_D(t, base, d):
    u = t - 55.4; kp, kc = 0.58, 0.38
    px, cx = 400, 700
    # states
    lhP, rhP = (-120, 110), (150, 110); lhC, rhC = (-70, 120), (70, 120); mp = "happy"; mc = "happy"; fc = -1; cwalk = 0
    if t < 58.5:
        rhP = (cx - px - 20, -80 + 520 * kc / kp * 0 + 70)   # hand towards child's head
        rhP = (270, 60)
    elif t < 60.4:
        mc = "sad"; mp = "sad"; lhC = (-90, -10); rhC = (90, -10); fc = 1
        rhP = (210, 40)
    elif t < 62.8:
        mp = "neutral"; mc = "scared"; rhP = (190 + 20 * math.sin(t * 6), -30); lhC = (-90, 0); rhC = (-30, -110)
        fc = -1
    else:
        mp = "happy"; mc = "happy"; rhP = (260, 70); lhC = (-120, 60)
    ps = pop((u - 0.1) / 0.5)
    if ps > .01:
        hp, hcp = person(d, px, 720, kp * ps, t, lhP, rhP, mp, face=-1 if False else 1, acc="tie", seed=21, lean=6 * math.sin(t * 2))
    cs = pop((u - 0.3) / 0.5)
    if cs > .01: person(d, cx, 720, kc * cs, t, lhC, rhC, mc, face=fc, acc="bow", seed=22)
    # hearts + tags
    if t < 58.5:
        for i in range(6):
            tt = 55.5 + 0.45 * i
            if t >= tt and t < tt + 2.2:
                yy = 420 - (t - tt) * 110; xx = 550 + 40 * math.sin((t - tt) * 3 + i)
                heart(d, xx, yy, 24, (235, 90, 120))
        for lbl, tt, x, y in (("EMPATHY", 55.5, 200, 520 - 330 + 40), ("SYMPATHY", 56.3, 880, 170), ("SENSITIVITY", 57.0, 210, 270), ("MORALS", 57.7, 860, 270)):
            if t >= tt: tag(d, x, y, lbl, (110, 200, 140), 36, s=min(1, pop((t - tt) / 0.35)))
    elif t < 60.4:
        d.rectangle((830 * S2, 600 * S2, 1000 * S2, 640 * S2), fill=(210, 190, 160, 255), outline=INK + (255,), width=3 * S2)
        d.ellipse((860 * S2, 570 * S2, 970 * S2, 612 * S2), fill=(255, 250, 240, 255), outline=INK + (255,), width=3 * S2)
        d.text((915 * S2, 590 * S2), "FOOD", font=fnt(22 * S2), fill=INK, anchor="mm")
        tag(d, 540, 250 + 6 * math.sin(t * 4), "?", YEL, 70, s=min(1, pop((t - 58.6) / 0.3)))
    elif t < 62.8:
        pp = (px + 330 + 20 * math.sin(t * 6), 700 - 520 * kp / 1.0 * 0 - 395)
        if t < 62.1: phone(d, 640 + 20 * math.sin(t * 6) + max(0, (t - 61.6)) * 700, 350 - max(0, (t - 61.6)) * 300, 1.4)
        if t >= 61.2: bigx(d, 660, 355, 80, RED, 20)
        tag(d, 540, 190, "NO PHONE = SHORTCUT", RED, 34, s=min(1, pop((t - 60.5) / 0.4)))
    else:
        s = min(1, pop((t - 62.85) / 0.5)); X, Y, R = 540 * S2, 230 * S2, 70 * S2 * s
        d.ellipse((X - R, Y - R, X + R, Y + R), fill=(255, 252, 240, 255), outline=GREEN + (255,), width=8 * S2)
        a = (t - 62.85) * 3.0; d.line([(X, Y), (X + R * .7 * math.sin(a), Y - R * .7 * math.cos(a))], fill=INK + (255,), width=6 * S2); d.line([(X, Y), (X + R * .45 * math.sin(a / 6), Y - R * .45 * math.cos(a / 6))], fill=INK + (255,), width=8 * S2)
        for i in range(3): heart(d, 440 + i * 100, 370 - ((t * 60 + i * 30) % 90), 18, (235, 90, 120))
        tag(d, 540, 120, "TIME TOGETHER", GREEN, 36, s=min(1, pop((t - 63.0) / 0.4)))

def scene_of(t):
    if 5.3 <= t < 14.9: return "A"
    if 17.4 <= t < 24.5: return "B"
    if 24.5 <= t < 26.5: return "E"
    if 37.0 <= t < 50.5: return "C"
    if 55.4 <= t < 65.5: return "D"
    return None

def frame(t):
    sc = scene_of(t)
    bgk = {"A": "school", "B": "class", "E": "ecg", "C": "judge", "D": "home"}[sc]
    base = BGS[bgk].convert("RGBA")
    dyn = Image.new("RGBA", (W * S2, H * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(dyn)
    dim = [0]
    if sc == "A": scene_A(t, base, d)
    elif sc == "B": scene_B(t, base, d, dim)
    elif sc == "E": scene_ecg(t, base, d)
    elif sc == "C": scene_C(t, base, d)
    else: scene_D(t, base, d)
    base.alpha_composite(dyn.resize((W, H), Image.LANCZOS))
    if dim[0] > 0:
        ov = Image.new("RGBA", (W, H), (220, 30, 30, int(255 * dim[0]))); base.alpha_composite(ov)
    return base.convert("RGB")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "anim_panel.mp4"
    tmax = float(sys.argv[2]) if len(sys.argv) > 2 else DUR
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    black = bytes(W * H * 3)
    grain = (np.random.RandomState(9).rand(H, W) * 255).astype(np.uint8)
    last = None
    for f in range(int(tmax * FPS)):
        t = f / FPS
        if scene_of(t) is None: pr.stdin.write(black); continue
        try:
            fr = frame(t); last = fr
        except Exception as ex:
            print('ERR at', round(t, 2), repr(ex), flush=True); fr = last
        arr = np.asarray(fr).astype(np.int16) + ((grain.astype(np.int16) - 128) // 14)[..., None]
        pr.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    pr.stdin.close(); pr.wait()
