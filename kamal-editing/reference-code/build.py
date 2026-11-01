import os, re, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJ = r"C:/Users/jagdi/Downloads/kamal 1q23"
A = PROJ + "/assets"
B = os.path.dirname(os.path.abspath(__file__))
os.chdir(B)
os.makedirs("cards", exist_ok=True)

GOLD = (255, 197, 49); RED = (255, 69, 58); GREEN = (46, 213, 115); WHITE = (255, 255, 255)
GLASS = (12, 14, 24, 215)
FB = "fonts/NotoSans-Bold.ttf"

def font(sz): return ImageFont.truetype(FB, sz)

def card(w, h, r=34, border=GOLD):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=GLASS, outline=border + (255,), width=4)
    return im, d

def ctext(d, cx, cy, s, sz, fill=WHITE, stroke=0):
    f = font(sz)
    d.text((cx, cy), s, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0))

def photo(path, w, h, r=26, focus=(0.5, 0.5)):
    im = Image.open(path).convert("RGBA")
    sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    im = im.crop((x, y, x + w, y + h))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    return out

def framed(path, w, h, border=GOLD, focus=(0.5, 0.5)):
    im, d = card(w, h, 30, border)
    p = photo(path, w - 16, h - 16, 24, focus)
    im.alpha_composite(p, (8, 8))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 30, outline=border + (255,), width=5)
    return im

def num_card(name, w, h, text, col, sz, strike=None, border=None):
    im, d = card(w, h, 34, border or col)
    if strike:
        f = font(60); ctext(d, w // 2, int(h * .27), strike, 60, (170, 170, 175))
        tw = d.textlength(strike, font=f)
        d.line((w // 2 - tw / 2 - 8, int(h * .27), w // 2 + tw / 2 + 8, int(h * .27)), fill=RED + (255,), width=7)
        ctext(d, w // 2, int(h * .66), text, sz, col, 3)
    else:
        ctext(d, w // 2, int(h * .62), text, sz, col, 3)
    im.save(f"cards/{name}.png")

# ---------- cards ----------
num_card("price100", 900, 300, "\u20b9100 Cr", GOLD, 150)
num_card("price6", 900, 300, "\u20b96 Cr", GREEN, 140, strike="\u20b9100 Cr")
num_card("p616", 900, 300, "\u20b96.16 Cr", GREEN, 140)
num_card("rent180", 900, 300, "\u20b91.80 Cr", GOLD, 140)
num_card("years3", 760, 300, "3 YEARS", WHITE, 120, border=GREEN)
num_card("pct75", 470, 330, "75%", GOLD, 150)
num_card("pct100", 470, 330, "100%", GREEN, 130)

framed(A + "/../Danik Bhaskar report.jpg", 290, 520, RED, (0.5, 0.0)).save("cards/report.png")

# couple (avif -> png already converted in scratchpad)
framed("../ias.png", 860, 484, GOLD).save("cards/couple.png")

# two cities
im, d = card(960, 440, 34, GOLD)
im.alpha_composite(photo(A + "/images/alwar_city.jpg", 450, 410, 24), (15, 15))
im.alpha_composite(photo(A + "/images/udaipur_city_palace.jpg", 450, 410, 24, (0.35, 0.5)), (495, 15))
# dark strip for labels
strip = Image.new("RGBA", (960, 90), (0, 0, 0, 0)); ImageDraw.Draw(strip).rectangle((0, 0, 960, 90), fill=(0, 0, 0, 140))
im.alpha_composite(strip, (0, 340))
ImageDraw.Draw(im).rounded_rectangle((0, 0, 959, 439), 34, outline=GOLD + (255,), width=5)
im.save("cards/cities.png")

# villa + 40 badge
im = framed(PROJ + "/Villa png.png", 860, 500, GOLD, (0.5, 0.55))
d = ImageDraw.Draw(im)
d.rounded_rectangle((580, 300, 840, 480), 30, fill=(12, 14, 24, 235), outline=GOLD + (255,), width=4)
ctext(d, 710, 390, "40", 140, GOLD, 3)
im.save("cards/villa.png")

# date calendar
im = Image.new("RGBA", (640, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((0, 0, 639, 399), 34, fill=(245, 245, 247, 255))
d.rounded_rectangle((0, 0, 639, 110), 34, fill=RED + (255,)); d.rectangle((0, 70, 639, 110), fill=RED + (255,))
ctext(d, 320, 58, "MARCH 2026", 62, WHITE)
ctext(d, 320, 255, "27", 230, (20, 22, 30))
im.save("cards/date.png")

# ACB stamp
im = Image.new("RGBA", (760, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((20, 20, 740, 380), 28, outline=RED + (255,), width=14, fill=(12, 14, 24, 215))
ctext(d, 380, 150, "ACB", 190, RED, 2)
ctext(d, 380, 295, "30 OCT 2026", 80, WHITE)
im = im.rotate(5, resample=Image.BICUBIC, expand=False)
im.save("cards/acb.png")

# Bhajan lal
framed(A + "/images/bhajanlal_sharma.jpg", 380, 490, GOLD, (0.5, 0.15)).save("cards/bhajan.png")

# Sudhansh Pant monogram
im, d = card(380, 490, 34, GOLD)
d.ellipse((85, 110, 295, 320), fill=(40, 46, 70, 255), outline=GOLD + (255,), width=5)
ctext(d, 190, 215, "SP", 105, GOLD)
im.save("cards/pant.png")

# INC logo card
im = Image.new("RGBA", (400, 440), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((0, 0, 399, 439), 34, fill=(255, 255, 255, 255), outline=(40, 160, 70, 255), width=6)
lg = Image.open(A + "/images/inc_logo.png").convert("RGBA")
sc = min(340 / lg.width, 380 / lg.height); lg = lg.resize((int(lg.width * sc), int(lg.height * sc)), Image.LANCZOS)
im.alpha_composite(lg, ((400 - lg.width) // 2, (440 - lg.height) // 2))
im.save("cards/inc.png")

# ---------- timeline ----------
# (png, tin, tout, x or None(center), y)
CARDS = [
    ("price100", 0.80, 2.35, None, 170),
    ("price6", 2.35, 5.75, None, 170),
    ("report", 7.30, 10.60, None, 150),
    ("couple", 11.00, 16.45, None, 150),
    ("cities", 19.70, 21.45, None, 170),
    ("villa", 21.40, 22.85, None, 140),
    ("p616", 23.75, 26.10, None, 170),
    ("rent180", 28.65, 31.30, None, 170),
    ("years3", 31.35, 33.10, None, 170),
    ("date", 40.50, 44.30, None, 150),
    ("pct75", 50.15, 53.95, 50, 170),
    ("pct100", 51.75, 53.95, 560, 170),
    ("acb", 55.00, 58.40, None, 150),
    ("bhajan", 59.90, 61.55, None, 125),
    ("pant", 62.35, 64.55, None, 125),
    ("inc", 73.30, 75.00, None, 170),
    ("inc", 77.60, 79.45, None, 170),
]
SZ = {}
for n, *_ in CARDS: SZ[n] = Image.open(f"cards/{n}.png").size

# captions: (start, text)  -- end = next start (max 2.2s)
CAPS = """0.00|इस आईएएस कपल ने
0.80|सौ करोड़ की प्रॉपर्टी
1.85|मात्र छह करोड़ में
2.85|खरीद ली,
3.45|और वो पैसा भी
4.20|अगले तीन साल में
4.85|वापस आ जाएगा।
5.80|तो आखिर कैसे
6.35|हुआ ये चमत्कार?
7.35|अभी दैनिक भास्कर की
8.25|एक रिपोर्ट में खुलासा
9.15|किया गया कि
9.60|1993 बैच के
10.60|आईएएस ऑफिसर
11.50|शिखर अग्रवाल,
12.35|उनकी पत्नी
13.00|प्रसाका माथुर,
14.00|दो बेटे,
14.75|उनके सास-ससुर—
16.30|इन सबके नाम
17.40|गोयल फैशंस
18.20|प्राइवेट लिमिटेड से
19.40|अलवर और उदयपुर में
20.65|40 अलग-अलग
21.40|कॉटेज व विला
22.10|खरीदे गए।
22.70|कीमत तय की गई
23.80|मात्र 6.16
24.90|करोड़ रुपये।
26.05|और वापस
26.60|गोयल फैशंस को
27.45|ये रेंट पर
28.15|दे दिया गया,
28.70|मात्र 1.80
29.90|करोड़ रुपये की कीमत पर।
31.35|तो तीन साल में
32.35|पैसा बराबर।
33.10|अब इसमें
33.75|दिक्कत क्या है?
34.65|ये साहब अभी
35.20|राजस्थान गवर्नमेंट में
36.50|इन्वेस्ट,
37.25|डीएमआईसी,
38.25|रीको जैसे
38.95|छोटे-छोटे पदों पर थे।
40.50|तो जब 27 मार्च 2026
42.15|को इनकी अलवर वाली
43.05|प्रॉपर्टीज की रजिस्ट्री हुई,
44.20|उसी दिन
45.00|गोयल फैशंस को
46.20|रीप्स योजना के तहत
47.55|एक पैकेज अनाउंस किया गया,
48.85|जिसमें
49.35|स्टेट टैक्स का
50.20|75 प्रतिशत सब्सिडी
51.80|और 100 प्रतिशत
52.60|बिजली फ्री।
53.55|रिपोर्ट के आने के
54.35|कुछ दिन बाद,
55.00|30 अक्टूबर को
55.85|इसकी जांच के आदेश
56.85|एसीबी को दे दिए गए हैं।
58.40|लेकिन इसमें
59.05|सियासत कहाँ है?
59.90|भजनलाल सरकार को
61.05|चलाने के लिए
61.65|दिल्ली से भेजे गए
62.40|सुधांश पंत की
63.20|पिछले साल वापसी हो गई।
64.50|बताया जाता है
65.40|कि उसका कारण था
66.15|सीएमओ से उनका टकराव।
67.30|उस वक्त सीएमओ में
68.45|एसीएस थे शिखर साहब।
69.80|तो क्या इस रिपोर्ट के
70.95|बाहर आने में
71.50|उस टकराव का योगदान
72.30|तो नहीं?
72.80|योगदान तो
73.35|कांग्रेस का भी
74.05|हो सकता था।
74.80|इतने बड़े करप्शन के
75.80|मुद्दे को सड़क का
76.70|आंदोलन बनाया जाए,
77.60|लेकिन कांग्रेस ने
78.40|ऐसा कुछ नहीं किया।
79.40|तो क्या मान लिया
80.20|जाए कि हमाम में
81.00|सब…"""
caps = [(float(a), b) for a, b in (l.split("|") for l in CAPS.splitlines())]
HL = ["छह करोड़", "6.16", "1.80", "40", "1993", "75 प्रतिशत", "100 प्रतिशत", "27 मार्च 2026", "30 अक्टूबर",
      "शिखर अग्रवाल", "प्रसाका माथुर", "गोयल फैशंस", "एसीबी", "सुधांश पंत", "भजनलाल", "कांग्रेस", "चमत्कार",
      "सियासत", "फ्री", "सब…", "सौ करोड़", "रजिस्ट्री", "रीप्स योजना", "वापस आ जाएगा", "पैसा बराबर", "टकराव"]

def T(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def hl(txt):
    for w in HL:
        txt = txt.replace(w, r"{\c&H31C5FF&}" + w + r"{\c&HFFFFFF&}")
    return txt

ev = []
def E(t0, t1, text, style, x=None, y=None, extra="", slide=True):
    pos = ""
    if x is not None:
        pos = (r"\move(%d,%d,%d,%d,0,250)" % (x, y - 40, x, y)) if slide else (r"\pos(%d,%d)" % (x, y))
    ev.append(f"Dialogue: 0,{T(t0)},{T(t1)},{style},,0,0,0,,{{\\an5{pos}\\fad(150,120){extra}}}{text}")

# captions
for i, (t, s) in enumerate(caps):
    end = caps[i + 1][0] if i + 1 < len(caps) else 83.0
    end = min(end, t + 2.3)
    ev.append(f"Dialogue: 1,{T(t)},{T(end)},Cap,,0,0,0,,{{\\an2\\fad(40,0)\\fscx86\\fscy86\\t(0,110,\\fscx100\\fscy100)}}{hl(s)}")

# labels (style Lab = boxed chip). colour box via \3c
def chip(t0, t1, text, x, y, col="&H2A2AE0&", sz=50):
    E(t0, t1, text, "Lab", x, y, rf"\3c{col}\fs{int(sz*1.2)}")

chip(0.80, 5.70, "प्रॉपर्टी की कीमत", 540, 130)
chip(7.30, 10.60, "दैनिक भास्कर की रिपोर्ट", 540, 120)
chip(10.90, 16.45, "आईएएस कपल", 540, 122, "&H2A2AE0&")
chip(11.60, 16.40, "शिखर अग्रवाल", 280, 580, "&H20262E&", 44)
chip(13.00, 16.40, "प्रसाका माथुर", 800, 580, "&H20262E&", 44)
chip(17.35, 19.55, "गोयल फैशंस\\Nप्राइवेट लिमिटेड", 540, 330, "&H2A2AE0&", 54)
chip(19.95, 21.45, "अलवर", 270, 570, "&H20262E&", 46)
chip(20.25, 21.45, "उदयपुर", 750, 570, "&H20262E&", 46)
chip(21.50, 22.85, "40 कॉटेज व विला", 360, 590, "&H2A2AE0&", 50)
chip(23.75, 26.10, "खरीद की कीमत", 540, 205, "&H20262E&", 44)
chip(28.65, 31.30, "रेंट — गोयल फैशंस को", 540, 205, "&H20262E&", 44)
chip(32.20, 33.10, "पैसा बराबर", 540, 400, "&H2A2AE0&", 56)
chip(36.50, 40.40, "इन्वेस्ट राजस्थान", 540, 230, "&H2A2AE0&", 54)
chip(37.25, 40.40, "डीएमआईसी", 540, 330, "&H2A2AE0&", 54)
chip(38.25, 40.40, "रीको", 540, 430, "&H2A2AE0&", 54)
chip(42.15, 44.30, "अलवर प्रॉपर्टीज की रजिस्ट्री", 540, 580, "&H20262E&", 44)
chip(46.15, 48.90, "रीप्स योजना\\Nका पैकेज", 540, 330, "&H2A2AE0&", 58)
chip(50.15, 53.95, "स्टेट टैक्स सब्सिडी", 285, 240, "&H20262E&", 38)
chip(51.75, 53.95, "बिजली फ्री", 795, 240, "&H20262E&", 40)
chip(55.90, 58.35, "जांच के आदेश", 540, 600, "&H2A2AE0&", 54)
E(58.40, 59.90, "{\\c&H31C5FF&}सियासत?", "Big", 540, 330, r"\fs150")
chip(59.90, 61.55, "भजनलाल सरकार", 540, 100, "&H2A2AE0&", 48)
chip(62.35, 64.55, "सुधांश पंत", 540, 100, "&H2A2AE0&", 52)
chip(63.10, 64.55, "पिछले साल वापसी", 540, 650, "&H20262E&", 42)
chip(66.15, 67.35, "सीएमओ से टकराव", 540, 330, "&H2A2AE0&", 58)
chip(67.40, 69.75, "CMO में ACS:\\Nशिखर अग्रवाल", 540, 330, "&H20262E&", 54)
chip(73.30, 75.00, "कांग्रेस", 540, 660, "&H20262E&", 48)
chip(77.60, 79.45, "कांग्रेस", 540, 660, "&H20262E&", 48)
E(80.85, 83.80, "{\\c&H31C5FF&}हमाम में सब…?", "Big", 540, 470, r"\fs112\t(0,300,\fscx108\fscy108)")

ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Nirmala UI,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,50,50,300,1
Style: Lab,Nirmala UI,50,&H00FFFFFF,&H00FFFFFF,&H002A2AE0,&H00000000,1,0,0,0,100,100,0,0,3,16,0,5,40,40,40,1
Style: Big,Nirmala UI,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,9,4,5,40,40,40,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(ev) + "\n"
open("cap.ass", "w", encoding="utf-8-sig").write(ASS)

# ---------- SFX ----------
SFX = [  # (time, file, vol)
    (0.00, "impact_trailer", .55), (0.75, "whoosh_cinematic_fast", .6), (2.30, "coins_clinking", .7),
    (5.70, "suspense_bass", .55), (7.25, "paper_slide", .8), (10.95, "camera_shutter", .8), (11.00, "whoosh_air", .5),
    (17.30, "notification_pop", .6), (19.65, "whoosh_fast_transition", .55), (21.35, "impact_big_cinematic", .4),
    (23.70, "coins_handling", .7), (28.55, "gold_coin_prize", .55), (31.30, "whoosh_air", .5), (32.30, "notification_pop", .6),
    (40.45, "impact_big_cinematic", .4), (46.10, "whoosh_cinematic_fast", .5), (50.10, "notification_pop", .6),
    (51.70, "notification_pop", .6), (54.95, "impact_trailer", .6), (58.35, "glass_hit_suspense", .6),
    (59.85, "whoosh_air", .5), (62.30, "whoosh_air", .5), (66.10, "glass_hit_suspense", .45), (73.25, "whoosh_air", .5),
    (77.55, "whoosh_air", .5), (79.40, "tick_tock", .8), (80.80, "suspense_bass", .6), (80.90, "impact_big_cinematic", .55),
]

# ---------- ffmpeg ----------
VID = PROJ + "/raw video.MOV"
inputs = ["-i", VID, "-i", A + "/music/bgm_selpan_mysterious_eerie.mp3"]
for _, f, _v in SFX: inputs += ["-i", f"{A}/sounds/{f}.mp3"]
c0 = 2 + len(SFX)
for (n, a, b, x, y) in CARDS: inputs += ["-loop", "1", "-framerate", "30", "-t", f"{b - a + .1:.2f}", "-i", f"cards/{n}.png"]

# zoom steps
ZB = [(0, 1.0), (5.8, 1.10), (7.35, 1.0), (9.6, 1.07), (13.0, 1.0), (17.4, 1.07), (22.7, 1.0), (26.05, 1.07),
      (31.35, 1.0), (33.1, 1.10), (35.2, 1.0), (40.5, 1.07), (44.2, 1.0), (49.3, 1.07), (53.55, 1.0), (55.0, 1.07),
      (58.4, 1.12), (59.9, 1.0), (64.5, 1.07), (69.8, 1.0), (72.8, 1.10), (74.8, 1.0), (77.6, 1.07), (79.4, 1.0)]
z = "1"
prev = 1.0
for t, v in ZB[1:]:
    z += f"+({v - prev:.3f})*gte(t,{t})"; prev = v
z += "+0.16*min(1,max(0,(t-79.4)/4.4))"

F = []
F.append(f"[0:v]scale=w='trunc(1080*({z})/2)*2':h=-2:eval=frame,crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.45',"
         "eq=contrast=1.07:saturation=1.15:brightness=-0.015,unsharp=5:5:0.5,vignette=PI/6,setsar=1,format=yuv420p[v0]")
cur = "v0"
for i, (n, a, b, x, y) in enumerate(CARDS):
    D = b - a
    w, h = SZ[n]
    xx = x if x is not None else (1080 - w) // 2
    F.append(f"[{c0 + i}:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1,fade=t=out:st={D - 0.22:.2f}:d=0.22:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    F.append(f"[{cur}][c{i}]overlay=x={xx}:y='{y}-40*pow(1-min(1,(t-{a})/0.25),2)':enable='between(t,{a},{b})':format=auto[o{i}]")
    cur = f"o{i}"
F.append(f"[{cur}]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.35:t=fill:enable='gte(t,79.4)',subtitles=cap.ass:fontsdir=fonts,"
         "drawbox=x=0:y=1908:w='iw*t/83.8':h=12:color=0xFFC531:t=fill[vout]")

# audio
F.append("[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2,loudnorm=I=-15:TP=-1.5:LRA=9,asplit=2[vk][vm]")
F.append("[1:a]atrim=0:84,volume=0.55,afade=t=in:st=0:d=1.5,afade=t=out:st=81.5:d=2.3[bgm]")
F.append("[bgm][vk]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[bgd]")
labels = ["vm", "bgd"]
for i, (t, f, v) in enumerate(SFX):
    ms = int(t * 1000)
    extra = ",aloop=loop=-1:size=2e9,atrim=0:4.4" if f == "tick_tock" else ""
    F.append(f"[{2 + i}:a]aformat=sample_rates=48000:channel_layouts=stereo{extra},volume={v},adelay={ms}|{ms}[s{i}]")
    labels.append(f"s{i}")
F.append("".join(f"[{l}]" for l in labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.95[aout]")

open("graph.txt", "w", encoding="utf-8").write(";\n".join(F))
out = sys.argv[1] if len(sys.argv) > 1 else "out.mp4"
extra_args = sys.argv[2:]
cmd = ["ffmpeg", "-y", "-v", "error", "-stats"] + inputs + ["-/filter_complex", "graph.txt", "-map", "[vout]", "-map", "[aout]",
       "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-t", "83.8", "-movflags", "+faststart"] + extra_args + [out]
print(" ".join(cmd[:6]), "...", len(inputs) // 2, "inputs")
subprocess.run(cmd, check=True)
