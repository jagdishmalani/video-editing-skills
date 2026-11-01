import os, re, sys, math, random, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJ = r"C:/Users/jagdi/Downloads/kamal 1q23"
A = PROJ + "/assets"
B = os.path.dirname(os.path.abspath(__file__))
os.chdir(B)
os.makedirs("cards_s", exist_ok=True)
SCR = os.path.abspath("..")
OUT = sys.argv[1] if len(sys.argv) > 1 else "stick_out.mp4"
ONLY_BASE = "--base-only" in sys.argv
TLIM = None
for i, a in enumerate(sys.argv):
    if a == "--t": TLIM = float(sys.argv[i + 1])

INK = (28, 28, 32); PAPER = (253, 253, 252)
RED = (214, 59, 47); GREEN = (40, 160, 90); YEL = (255, 216, 77); NAVY = (40, 52, 90)
FB = "fonts/NotoSans-Bold.ttf"
def font(sz): return ImageFont.truetype(FB, sz)

# ------------------------------------------------------------------ paper cards
def shadowed(im, off=(7, 9), blur=7, op=70):
    w, h = im.size
    out = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sh.putalpha(im.split()[3].point(lambda v: op if v > 0 else 0))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh, (6 + off[0], 6 + off[1]))
    out.alpha_composite(im, (6, 6))
    return out

def pcard(w, h, border=INK, r=22, fill=(255, 254, 249)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill + (255,), outline=border + (255,), width=5)
    return im, d

def ctext(d, cx, cy, s, sz, fill=INK):
    d.text((cx, cy), s, font=font(sz), fill=fill, anchor="mm")

def underline(d, x0, x1, y, col=YEL, wd=16):
    pts = [(x0 + (x1 - x0) * i / 10, y + 3 * math.sin(i * 1.7)) for i in range(11)]
    d.line(pts, fill=col + (200,), width=wd)

def num_card(name, w, h, text, col, sz, strike=None):
    im, d = pcard(w, h)
    if strike:
        f = font(58); ctext(d, w // 2, int(h * .27), strike, 58, (140, 140, 145))
        tw = d.textlength(strike, font=f)
        d.line((w // 2 - tw / 2 - 10, int(h * .30), w // 2 + tw / 2 + 10, int(h * .24)), fill=RED + (255,), width=8)
        ctext(d, w // 2, int(h * .67), text, sz, col)
    else:
        ctext(d, w // 2, int(h * .64), text, sz, col)
        tw = d.textlength(text, font=font(sz))
        underline(d, w // 2 - tw / 2, w // 2 + tw / 2, int(h * .64) + sz * .45, YEL if col != YEL else RED, 14)
    shadowed(im).save(f"cards_s/{name}.png")

def polaroid(path, w, h, angle, focus=(0.5, 0.5), tape=True, border=INK):
    m = 16
    p = Image.open(path).convert("RGBA")
    iw, ih = w - 2 * m, h - 2 * m
    sc = max(iw / p.width, ih / p.height)
    p = p.resize((int(p.width * sc) + 1, int(p.height * sc) + 1), Image.LANCZOS)
    x = int((p.width - iw) * focus[0]); y = int((p.height - ih) * focus[1])
    p = p.crop((x, y, x + iw, y + ih))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), fill=(255, 255, 255, 255), outline=border + (255,), width=4)
    im.alpha_composite(p, (m, m))
    d.rectangle((m - 1, m - 1, m + iw, m + ih), outline=(60, 60, 65, 255), width=2)
    if tape:
        t = Image.new("RGBA", (130, 40), YEL + (190,)); td = ImageDraw.Draw(t)
        for i in range(0, 130, 12): td.line((i, 0, i + 6, 40), fill=(255, 255, 255, 60), width=3)
        t = t.rotate(-5, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(t, (w // 2 - t.width // 2, -14)) if False else None
        big = Image.new("RGBA", (w, h + 30), (0, 0, 0, 0)); big.alpha_composite(im, (0, 30))
        big.alpha_composite(t, (w // 2 - t.width // 2, 8)); im = big
    im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    return shadowed(im)

def draw_cards():
    num_card("price100", 900, 300, "\u20b9100 Cr", INK, 150)
    num_card("price6", 900, 300, "\u20b96 Cr", GREEN, 140, strike="\u20b9100 Cr")
    num_card("p616", 900, 300, "\u20b96.16 Cr", GREEN, 140)
    num_card("rent180", 900, 300, "\u20b91.80 Cr", RED, 140)
    num_card("years3", 760, 300, "3 YEARS", INK, 120)
    num_card("pct75", 470, 330, "75%", RED, 150)
    num_card("pct100", 470, 330, "100%", GREEN, 130)
    polaroid(PROJ + "/Danik Bhaskar report.jpg", 290, 520, -3, (0.5, 0.0)).save("cards_s/report.png")
    polaroid(SCR + "/ias.png", 860, 484, 1.5).save("cards_s/couple.png")
    # two cities
    im = Image.new("RGBA", (960, 440), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    a = polaroid(A + "/images/alwar_city.jpg", 450, 410, -2.5); b = polaroid(A + "/images/udaipur_city_palace.jpg", 450, 410, 2.5, (0.35, 0.5))
    big = Image.new("RGBA", (960, 470), (0, 0, 0, 0)); big.alpha_composite(a, (0, 20)); big.alpha_composite(b, (500, 20)); big.save("cards_s/cities.png")
    v = polaroid(PROJ + "/Villa png.png", 860, 500, -1.5, (0.5, 0.55))
    d = ImageDraw.Draw(v)
    bx, by = v.width - 330, v.height - 230
    d.ellipse((bx, by, bx + 210, by + 210), fill=(255, 254, 249, 255), outline=RED + (255,), width=7)
    ctext(d, bx + 105, by + 105, "40", 120, RED)
    v.save("cards_s/villa.png")
    # calendar
    im = Image.new("RGBA", (640, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 639, 399), 26, fill=(255, 254, 249, 255), outline=INK + (255,), width=5)
    d.rounded_rectangle((0, 0, 639, 110), 26, fill=RED + (255,), outline=INK + (255,), width=5); d.rectangle((5, 70, 634, 110), fill=RED + (255,))
    ctext(d, 320, 58, "MARCH 2026", 62, (255, 255, 255)); ctext(d, 320, 255, "27", 230, INK)
    shadowed(im).save("cards_s/date.png")
    # ACB stamp
    im = Image.new("RGBA", (760, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 740, 380), 24, outline=RED + (255,), width=14, fill=(255, 254, 249, 255))
    ctext(d, 380, 150, "ACB", 190, RED); ctext(d, 380, 295, "30 OCT 2026", 80, INK)
    shadowed(im.rotate(5, resample=Image.BICUBIC, expand=True)).save("cards_s/acb.png")
    polaroid(A + "/images/bhajanlal_sharma.jpg", 380, 490, 2, (0.5, 0.15)).save("cards_s/bhajan.png")
    im, d = pcard(380, 490); d.ellipse((85, 110, 295, 320), outline=INK + (255,), width=6, fill=(250, 245, 225, 255)); ctext(d, 190, 215, "SP", 105, INK)
    shadowed(im.rotate(-2, resample=Image.BICUBIC, expand=True)).save("cards_s/pant.png")
    im, d = pcard(400, 440, GREEN)
    lg = Image.open(A + "/images/inc_logo.png").convert("RGBA")
    sc = min(340 / lg.width, 380 / lg.height); lg = lg.resize((int(lg.width * sc), int(lg.height * sc)), Image.LANCZOS)
    im.alpha_composite(lg, ((400 - lg.width) // 2, (440 - lg.height) // 2))
    shadowed(im).save("cards_s/inc.png")

# ------------------------------------------------------------------ character
FPS = 30
N = int(83.8 * FPS)
w_ = wave.open(SCR + "/a.wav"); sr = w_.getframerate()
aud = np.frombuffer(w_.readframes(w_.getnframes()), dtype=np.int16).astype(np.float32) / 32768
hop = sr // FPS
env = np.array([np.sqrt(np.mean(aud[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(N)])
env = np.clip(env / (np.percentile(env, 92) + 1e-6), 0, 1.2)
sm = np.zeros_like(env); p = 0
for i, v in enumerate(env):
    p = 0.55 * p + 0.45 * v; sm[i] = p
env = np.clip(sm, 0, 1)

MOODS = [(0, "shock"), (5.8, "think"), (7.4, "explain"), (33.1, "skeptic"), (40.5, "angry"), (58.4, "skeptic"),
         (62.0, "explain"), (66.0, "angry"), (69.8, "skeptic"), (72.8, "smirk"), (79.4, "shrug")]
CX = 540
HEAD = (CX, 870); R = 80; NECK = 950; HIP = 1200; FOOT = 1500
SH = (CX, 985); L1, L2 = 135, 125

def smooth(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def targets(mood, t):
    s = math.sin; c = math.cos
    if mood == "shock":
        j = 6 * s(t * 30)
        return (CX - 250 + j, 790), (CX + 250 - j, 790)
    if mood == "think":
        return (CX - 85, 1085), (CX + 45, 962 + 3 * s(t * 3))
    if mood == "explain":
        return (CX - 175, 1120 + 25 * s(t * 2.3)), (CX + 215 + 25 * s(t * 1.7), 840 + 70 * s(t * 2.9))
    if mood == "skeptic":
        return (CX - 115, 1160), (CX + 215, 1010 + 40 * s(t * 2.2))
    if mood == "angry":
        j = 7 * s(t * 24)
        return (CX - 165, 1030 + j), (CX + 165, 1030 - j)
    if mood == "smirk":
        return (CX - 190, 1110 + 20 * s(t * 1.8)), (CX + 200, 1020 + 30 * s(t * 2.4))
    return (CX - 255, 1030 + 10 * s(t * 3)), (CX + 255, 1030 - 10 * s(t * 3))  # shrug

def tgt_blend(t):
    idx = max(i for i, (a, _) in enumerate(MOODS) if a <= t)
    cur = MOODS[idx][1]; ta = MOODS[idx][0]
    L, Rr = targets(cur, t)
    if idx > 0:
        k = smooth((t - ta) / 0.4)
        pl, pr = targets(MOODS[idx - 1][1], t)
        L = (pl[0] + (L[0] - pl[0]) * k, pl[1] + (L[1] - pl[1]) * k)
        Rr = (pr[0] + (Rr[0] - pr[0]) * k, pr[1] + (Rr[1] - pr[1]) * k)
    return cur, L, Rr

def ik(sh, tg, side):
    dx, dy = tg[0] - sh[0], tg[1] - sh[1]
    d = math.hypot(dx, dy); d = min(d, L1 + L2 - 2); d = max(d, 40)
    a = math.atan2(dy, dx)
    cosb = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    b = math.acos(max(-1, min(1, cosb)))
    ang = a + side * -b if False else a + (b if side > 0 else -b) * -1 * -1
    # elbow bends downward/outward
    e1 = (sh[0] + L1 * math.cos(a - b), sh[1] + L1 * math.sin(a - b))
    e2 = (sh[0] + L1 * math.cos(a + b), sh[1] + L1 * math.sin(a + b))
    elbow = e1 if e1[1] > e2[1] else e2
    hand = (sh[0] + d * math.cos(a), sh[1] + d * math.sin(a))
    return elbow, hand

S2 = 2
Y0, HH = 700, 880   # character strip (abs y0, height)

def build_bg():
    bg = Image.new("RGB", (1080, 1920), PAPER); d = ImageDraw.Draw(bg, "RGBA")
    for x in range(0, 1080, 54): d.line((x, 0, x, 1920), fill=(76, 90, 105, 12), width=1)
    for y in range(0, 1920, 54): d.line((0, y, 1080, y), fill=(76, 90, 105, 12), width=1)
    return bg

def render_char(f):
    t = f / FPS
    rnd = random.Random(f // 3)
    def J(p, a=2.2): return (p[0] + rnd.uniform(-a, a), p[1] + rnd.uniform(-a, a))
    im = Image.new("RGBA", (1080 * S2, HH * S2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def P(p): return ((p[0]) * S2, (p[1] - Y0) * S2)
    def line(pts, wd=7, col=INK, a=2.0):
        q = [P(J(p, a)) for p in pts]
        d.line(q, fill=col + (255,), width=int(wd * S2), joint="curve")
        for p in (q[0], q[-1]): d.ellipse((p[0] - wd * S2 / 2, p[1] - wd * S2 / 2, p[0] + wd * S2 / 2, p[1] + wd * S2 / 2), fill=col + (255,))
    mood, tl, tr = tgt_blend(t)
    sway = 6 * math.sin(t * 1.6); bob = 4 * math.sin(t * 3.1)
    lean = {"shock": -12, "think": 8, "explain": 0, "skeptic": 10, "angry": -10, "smirk": 6, "shrug": 0}[mood]
    cx = CX + sway
    # floor shadow
    sx, sy = P((cx, FOOT + 8))
    d.ellipse((sx - 190 * S2 / 1.3, sy - 14, sx + 190 * S2 / 1.3, sy + 14), fill=(0, 0, 0, 28))
    # legs
    hip = (cx + lean * .3, HIP)
    for side, off in ((-1, -70), (1, 70)):
        foot = (cx + off + sway * .3, FOOT)
        knee = ((hip[0] + foot[0]) / 2 + side * 16, (HIP + FOOT) / 2)
        line([hip, knee, foot], 7)
        fx, fy = P(foot); d.ellipse((fx - 10 * S2 + side * 8 * S2, fy - 4 * S2, fx + 22 * S2 + side * 8 * S2, fy + 8 * S2), fill=INK + (255,)) if False else None
        line([foot, (foot[0] + side * 34, foot[1] + 2)], 9)
    # torso
    neck = (cx + lean, NECK + bob * .3)
    mid = (cx + lean * .6, (NECK + HIP) / 2)
    line([neck, mid, hip], 7)
    # arms
    shl = (neck[0] - 6, neck[1] + 34); shr = (neck[0] + 6, neck[1] + 34)
    for side, tg, sh in ((-1, tl, shl), (1, tr, shr)):
        e, h = ik(sh, (tg[0] + sway, tg[1]), side)
        line([sh, e, h], 7)
        hx, hy = P(h); d.ellipse((hx - 13 * S2, hy - 10 * S2, hx + 13 * S2, hy + 10 * S2), fill=(255, 255, 255, 255), outline=INK + (255,), width=int(5 * S2 / 1.5))
    # head
    hc = (neck[0] + lean * .5, HEAD[1] + bob)
    hx, hy = P(hc)
    d.ellipse((hx - R * S2, hy - R * S2, hx + R * S2, hy + R * S2), fill=(255, 255, 255, 255))
    # wobbly outline
    pts = []
    for k in range(0, 37):
        an = k / 36 * 2 * math.pi
        rr = R + rnd.uniform(-1.8, 1.8)
        pts.append(P((hc[0] + rr * math.cos(an), hc[1] + rr * math.sin(an))))
    d.line(pts, fill=INK + (255,), width=int(7 * S2), joint="curve")
    # face
    gx = 6 * math.sin(t * .9)
    def F(dx, dy): return P((hc[0] + dx + gx * .3, hc[1] + dy))
    eyes = {"shock": (10, 16), "think": (8, 11), "explain": (8, 12), "skeptic": (8, 8), "angry": (8, 9), "smirk": (8, 10), "shrug": (8, 12)}[mood]
    blink = (f % 95) in (0, 1, 2)
    for ex in (-30, 30):
        px, py = F(ex + gx, -10)
        ry = 2 if blink else eyes[1]
        d.ellipse((px - eyes[0] * S2, py - ry * S2, px + eyes[0] * S2, py + ry * S2), fill=INK + (255,))
    def brow(x0, y0, x1, y1): d.line([F(x0, y0), F(x1, y1)], fill=INK + (255,), width=int(6 * S2))
    if mood == "shock":
        brow(-46, -42, -16, -50); brow(16, -50, 46, -42)
    elif mood == "think":
        brow(-46, -30, -16, -32); brow(16, -48, 46, -40)
    elif mood == "angry":
        brow(-48, -50, -14, -30); brow(14, -30, 48, -50)
    elif mood == "skeptic":
        brow(-46, -32, -16, -34); brow(16, -54, 46, -44)
    elif mood == "smirk":
        brow(-46, -36, -16, -38); brow(16, -42, 46, -36)
    elif mood == "shrug":
        brow(-46, -34, -16, -46); brow(16, -46, 46, -34)
    else:
        brow(-46, -38, -16, -40); brow(16, -40, 46, -38)
    a = float(env[min(f, N - 1)])
    mx, my = F(0, 38)
    if a > 0.10:
        rx = 15 + 12 * a; ry = 4 + 24 * a
        d.ellipse((mx - rx * S2, my - ry * S2, mx + rx * S2, my + ry * S2), fill=INK + (255,))
        if a > 0.5: d.ellipse((mx - rx * S2 * .55, my + ry * S2 * .1, mx + rx * S2 * .55, my + ry * S2 * .85), fill=(214, 100, 100, 255))
    else:
        if mood in ("smirk", "explain"): d.arc((mx - 24 * S2, my - 12 * S2, mx + 24 * S2, my + 12 * S2), 15, 165, fill=INK + (255,), width=int(6 * S2))
        elif mood in ("angry", "skeptic", "think"): d.line([F(-20, 40), F(0, 36), F(20, 42)], fill=INK + (255,), width=int(6 * S2))
        else: d.line([F(-18, 38), F(18, 38)], fill=INK + (255,), width=int(6 * S2))
    # accents
    if mood == "shock":
        for ang_ in (-35, -10, 15):
            for sd in (-1, 1):
                x1 = hc[0] + sd * (R + 22) * math.cos(math.radians(ang_)); y1 = hc[1] - 10 + (R + 22) * math.sin(math.radians(ang_)) - 40
                x2 = hc[0] + sd * (R + 52) * math.cos(math.radians(ang_)); y2 = hc[1] - 10 + (R + 52) * math.sin(math.radians(ang_)) - 40
                d.line([P((x1, y1)), P((x2, y2))], fill=INK + (255,), width=int(5 * S2))
        sxp, syp = P((hc[0] + 70, hc[1] - 30 + (t * 90 % 60)))
        d.ellipse((sxp - 8 * S2, syp - 12 * S2, sxp + 8 * S2, syp + 12 * S2), fill=(120, 190, 235, 255))
    if mood == "think":
        d.text(P((hc[0] + 95, hc[1] - 110 + 6 * math.sin(t * 3))), "?", font=ImageFont.truetype(FB, 110 * S2), fill=RED + (255,), anchor="mm")
    if mood == "angry":
        ax, ay = hc[0] + 62, hc[1] - 66
        for dx_, dy_, ex_, ey_ in ((-14, -14, 14, 14), (14, -14, -14, 14)):
            d.line([P((ax + dx_, ay + dy_)), P((ax + ex_, ay + ey_))], fill=RED + (255,), width=int(6 * S2))
    return im.resize((1080, HH), Image.LANCZOS)

def render_base():
    bg = build_bg()
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
           "-i", PROJ + "/raw video.MOV", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(TLIM or 83.8), "base_s.mp4"]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int((TLIM or 83.8) * FPS)
    for f in range(n):
        fr = bg.copy()
        ch = render_char(f)
        fr.paste(ch, (0, Y0), ch)
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait()

if __name__ == "__main__":
    draw_cards()
    render_base()
    if ONLY_BASE: sys.exit(0)
    src = open("build.py", encoding="utf-8").read()
    i0 = src.index("# ---------- timeline"); i1 = src.index("# ---------- ffmpeg");
    sec = src[i0:i1].replace("cards/", "cards_s/").replace("cap.ass", "cap_s.ass")
    g = dict(globals()); exec(sec, g)
    ass = open("cap_s.ass", encoding="utf-8-sig").read()
    ass = re.sub(r"Style: Cap,.*", r"Style: Cap,Nirmala UI,92,&H001E1E1E,&H001E1E1E,&H00FDFDFC,&H00000000,1,0,0,0,100,100,0,0,1,6,0,2,50,50,300,1", ass)
    ass = re.sub(r"Style: Big,.*", r"Style: Big,Nirmala UI,120,&H001E1E1E,&H001E1E1E,&H00FDFDFC,&H00000000,1,0,0,0,100,100,0,0,1,9,0,5,40,40,40,1", ass)
    ass = ass.replace("&H31C5FF&", "&H2F3BD6&").replace(r"{\c&HFFFFFF&}", r"{\c&H1E1E1E&}")
    ass = ass.replace(r"\3c&H20262E&", r"\1c&H1E1E1E&\3c&H4DD8FF&")
    open("cap_s.ass", "w", encoding="utf-8-sig").write(ass)
    # ffmpeg stage
    rest = src[i1:]
    rest = rest.replace('VID = PROJ + "/raw video.MOV"', 'VID = "base_s.mp4"').replace("cards/", "cards_s/")
    rest = re.sub(r'F\.append\(f"\[0:v\]scale=.*?format=yuv420p\[v0\]"\)', 'F.append("[0:v]setsar=1,format=yuv420p[v0]")', rest, flags=re.S)
    rest = rest.replace("drawbox=x=0:y=0:w=iw:h=ih:color=black@0.35:t=fill:enable='gte(t,79.4)',subtitles=cap.ass", "subtitles=cap_s.ass")
    g2 = dict(g); exec(rest, g2)
