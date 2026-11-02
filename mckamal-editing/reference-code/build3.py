import os, re, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

PROJ = "C:/Users/jagdi/Downloads/kamal 1q23"
A = PROJ + "/assets"
VID = PROJ + "/second video/kamal new second.MP4"
B = os.path.dirname(os.path.abspath(__file__))
os.chdir(B)
os.makedirs("cards", exist_ok=True)
DUR = 69.6
SPLITS = [(5.3, 14.9), (17.4, 26.5), (37.0, 50.5), (55.4, 65.5)]
def insplit(t): return any(a <= t < b for a, b in SPLITS)

GOLD = (255, 197, 49); RED = (255, 69, 58); GREEN = (46, 213, 115); WHITE = (255, 255, 255)
GLASS = (12, 14, 24, 220)
def font(sz): return ImageFont.truetype("fonts/NotoSans-Bold.ttf", sz)

def card(w, h, border=GOLD, r=30):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=GLASS, outline=border + (255,), width=4)
    return im, d
def ctext(d, cx, cy, s, sz, fill=WHITE, stroke=0):
    d.text((cx, cy), s, font=font(sz), fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0))
def photo(path, w, h, r=26, focus=(0.5, 0.5), border=GOLD):
    im = Image.open(path).convert("RGBA")
    sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    im = im.crop((x, y, x + w, y + h))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w - 1, h - 1), r, outline=border + (255,), width=5)
    return out

# ---------------- cards (Latin/numbers only; Hindi goes through ASS) ----------------
photo(A + "/images/panchkula_sector17.jpg", 560, 250, focus=(0.5, 0.45), border=RED).save("cards/panchkula.png")
photo(A + "/images/anantapur_clock_tower.jpg", 560, 250, focus=(0.5, 0.4), border=RED).save("cards/anantapur.png")
for name, num, col in (("age8", "8 YRS", GOLD), ("age6", "6 YRS", GOLD), ("age14", "14 YRS", GOLD)):
    im, d = card(210, 130, col); ctext(d, 105, 68, num, 50, col, 2); im.save(f"cards/{name}.png")
im, d = card(700, 210, RED); ctext(d, 350, 62, "SOCIAL MEDIA", 66, WHITE); ctext(d, 350, 147, "= JUDGE", 78, RED); im.save("cards/judge.png")
for name, word in (("caste", "CASTE"), ("gender", "GENDER"), ("religion", "RELIGION")):
    im, d = card(320, 130, RED); ctext(d, 160, 66, word, 50 if len(word) > 6 else 56, WHITE); im.save(f"cards/{name}.png")
for name, word in (("empathy", "EMPATHY"), ("sympathy", "SYMPATHY")):
    im, d = card(440, 110, GREEN); ctext(d, 220, 56, word, 54, WHITE); im.save(f"cards/{name}.png")
# phone with red cross
im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((90, 20, 210, 280), 22, fill=(20, 22, 34, 235), outline=WHITE + (255,), width=6)
d.rounded_rectangle((102, 50, 198, 240), 8, fill=(60, 120, 200, 255)); d.ellipse((140, 248, 160, 268), outline=WHITE + (255,), width=3)
d.line((60, 60, 240, 250), fill=RED + (255,), width=18); d.line((240, 60, 60, 250), fill=RED + (255,), width=18)
im.save("cards/phone_x.png")
# clock + heart (time together)
im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.ellipse((30, 30, 270, 270), fill=(20, 22, 34, 235), outline=GREEN + (255,), width=10)
d.line((150, 150, 150, 70), fill=WHITE + (255,), width=10); d.line((150, 150, 210, 180), fill=WHITE + (255,), width=10)
d.ellipse((140, 140, 160, 160), fill=GOLD + (255,))
im.save("cards/clock.png")

# (png, tin, tout, x|None, y)
CARDS_ALL = [
    ("panchkula", 5.30, 12.50, None, 110),
    ("age8", 7.00, 13.00, 40, 135),
    ("age6", 8.55, 13.00, 830, 135),
    ("anantapur", 15.45, 24.40, None, 110),
    ("age14", 17.55, 20.00, 40, 135),
    ("judge", 37.00, 41.30, None, 140),
    ("caste", 47.40, 50.40, 30, 120),
    ("gender", 48.20, 50.40, 380, 120),
    ("religion", 49.00, 50.40, 730, 120),
    ("empathy", 55.50, 58.30, 60, 120),
    ("sympathy", 56.30, 58.30, 580, 120),
    ("phone_x", 60.45, 62.70, 60, 110),
    ("clock", 62.85, 65.40, 60, 110),
]
CARDS = [c for c in CARDS_ALL if not insplit(c[1])]
SZ = {n: Image.open(f"cards/{n}.png").size for n, *_ in CARDS}

# ---------------- captions from timed segments ----------------
SEG = [
(0.0,1.7,"बच्चे पैदा करना बंद करो,"),(1.8,3.4,"क्योंकि नहीं तो आप उन्हें पाल सकते हो,"),(3.5,5.0,"नहीं आज ऐसा माहौल है।"),
(5.2,6.9,"पंचकुला के एक स्कूल में"),(7.0,8.5,"आठ साल का बच्चा"),(8.6,9.7,"छह साल की बच्ची को"),(9.8,11.2,"टेबल पर पटक पटक के"),
(11.3,13.0,"पत्थर से इतनी बुरी तरीके से मारता है"),(13.1,15.0,"कि वो वीडियो देख लो तो आपकी रूह कांप उठेगी।"),
(15.2,17.3,"वहीं आंध्र प्रदेश के अनंतपुर में"),(17.5,18.4,"एक चौदह साल की बच्ची"),(18.4,20.0,"एक लड़के का प्रपोजल ठुकरा देती है"),
(20.1,21.3,"तो उसके क्लासरूम में"),(21.4,22.9,"घुसकर उसको chain saw से"),(22.9,24.4,"इतना मारता है कि एक हाथ तक कट जाता है।"),
(24.5,26.4,"और अभी वो जिंदगी खतरे में है।"),(26.7,29.7,"हम उम्मीद करते हैं कि दोनों जिंदगियां खतरे से बाहर आ जाएं।"),
(30.0,33.8,"लेकिन उस सदमे से कब बाहर आएंगी या पूरी जिंदगी उस सदमे में निकाल देंगी"),
(33.9,36.9,"जिसका फायदा न जाने कितने ही राक्षस उठाएंगे।"),(37.0,41.3,"एक तो आज का माहौल ऐसा है कि सोशल मीडिया पर सब judge बने बैठे हैं।"),
(41.4,45.3,"उन्हें पता है एक खबर सुनकर वो डिसाइड कर लेते हैं कि आजकल की लड़कियां तो ऐसी होती हैं।"),
(45.4,47.2,"जबकि हम खुद क्रिमिनल माइंडसेट के हैं।"),(47.3,50.4,"जब हमारे अंदर कास्ट, जेंडर और रिलिजन के बेस पर इतनी नफरत भरी हुई है, तो अपराधी तो हैं ही"),
(50.5,52.8,"अगर आपको बच्चे पैदा करने का शौक है"),(52.9,55.2,"तो आपमें इतनी कूबत होनी चाहिए कि आप उनको"),
(55.3,58.3,"एम्पथी, सिम्पैथी, संवेदनशीलता, नैतिकता ये सब चीजें सिखा सकें।"),(58.5,60.3,"और जब बच्चा खाना नहीं खाए"),
(60.4,62.7,"तो उसको फोन देकर डिस्ट्रैक्ट करने की बजाय"),(62.8,65.4,"ऐसी चीजें सिखाने और उसके साथ टाइम बिताने का दम होना चाहिए।"),
(65.5,67.7,"वरना बड़े होकर वो बच्चे गालियां तो देंगे ही,"),(67.8,69.5,"जैसा आप में से अधिकतर लोग दे रहे हैं।")]

def wlen(w): return max(2, len(re.sub(r"[^\w]", "", w)))
words = []   # (start, text)
for (a, b, txt) in SEG:
    toks = txt.split(); tot = sum(wlen(t) for t in toks); c = 0
    for t in toks:
        words.append((a + (b - a) * c / tot, t)); c += wlen(t)
chunks = []; cur = []
def flush():
    global cur
    if cur: chunks.append((cur[0][0], " ".join(t for _, t in cur))); cur = []
for i, (s, t) in enumerate(words):
    if cur and (len(cur) >= 3 or sum(len(x) for _, x in cur) + len(t) > 20 or (i and any(words[i][0] - words[i - 1][0] > 0.9 for _ in [0]))):
        flush()
    cur.append((s, t))
    if t[-1] in "।,?" : flush()
flush()
HL = ["आठ साल", "छह साल", "चौदह साल", "पंचकुला", "अनंतपुर", "आंध्र प्रदेश", "रूह कांप उठेगी", "chain saw", "हाथ तक कट", "खतरे में", "सदमे", "राक्षस",
      "judge", "क्रिमिनल माइंडसेट", "कास्ट", "जेंडर", "रिलिजन", "नफरत", "एम्पथी,", "सिम्पैथी,", "संवेदनशीलता,", "नैतिकता", "फोन", "गालियां", "बच्चे पैदा करना बंद करो,", "प्रपोजल"]

def T(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def hl(txt):
    for w in HL: txt = txt.replace(w, r"{\c&H31C5FF&}" + w + r"{\c&HFFFFFF&}")
    return txt

ev = []
for i, (t, s) in enumerate(chunks):
    end = chunks[i + 1][0] if i + 1 < len(chunks) else DUR - 0.2
    end = min(end, t + 2.3)
    ev.append(f"Dialogue: 1,{T(t)},{T(end)},{('CapLow' if insplit(t) else 'Cap')},,0,0,0,,{{\\an2\\fad(40,0)\\fscx86\\fscy86\\t(0,110,\\fscx100\\fscy100)}}{hl(s)}")

def E(t0, t1, text, style, x, y, extra=""):
    ev.append(f"Dialogue: 0,{T(t0)},{T(t1)},{style},,0,0,0,,{{\\an5\\move({x},{y-40},{x},{y},0,250)\\fad(150,120){extra}}}{text}")
RB = "&H2A2AE0&"; DK = "&H20262E&"; GB = "&H3C9A1F&"
def chip(t0, t1, text, x, y, col=RB, sz=56):
    if insplit(t0): return
    E(t0, t1, text, "Lab", x, y, rf"\3c{col}\fs{int(sz*1.2)}")

chip(0.00, 2.20, "बच्चे पैदा करना बंद करो?", 540, 215, RB, 62)
chip(2.40, 4.95, "आज का माहौल", 540, 215, DK, 58)
chip(5.40, 12.40, "पंचकुला · हरियाणा", 540, 330, DK, 36)
chip(7.00, 13.00, "बच्चा", 145, 300, DK, 38)
chip(8.55, 13.00, "बच्ची", 935, 300, DK, 38)
chip(14.15, 15.15, "रूह कांप उठेगी", 540, 215, RB, 56)
chip(15.55, 24.40, "अनंतपुर · आंध्र प्रदेश", 540, 325, DK, 34)
chip(17.55, 20.00, "बच्ची", 145, 300, DK, 38)
chip(18.90, 20.05, "प्रपोजल ठुकराया", 540, 385, RB, 40)
chip(20.10, 23.30, "क्लासरूम में हमला", 540, 385, RB, 40)
chip(23.30, 24.45, "एक हाथ कट गया", 540, 385, RB, 40)
chip(24.50, 26.50, "जिंदगी खतरे में", 540, 215, RB, 62)
chip(26.70, 29.70, "उम्मीद: दोनों बाहर आएं", 540, 215, GB, 52)
chip(30.00, 33.85, "सदमे से कब निकलेंगी?", 540, 215, DK, 54)
chip(33.95, 36.95, "फायदा उठाएंगे राक्षस", 540, 215, RB, 56)
chip(37.00, 41.30, "सब बने बैठे हैं judge", 540, 390, DK, 40)
chip(41.40, 45.30, "“आजकल की लड़कियां ऐसी होती हैं”", 540, 215, DK, 46)
chip(45.40, 47.30, "हम खुद क्रिमिनल माइंडसेट के?", 540, 215, RB, 50)
chip(47.40, 50.40, "नफरत भरी हुई है", 540, 310, RB, 50)
chip(50.50, 52.85, "बच्चे पैदा करने का शौक?", 540, 215, DK, 54)
chip(52.90, 55.30, "इतनी कूबत होनी चाहिए", 540, 215, GB, 56)
chip(57.00, 58.30, "संवेदनशीलता", 280, 280, GB, 44)
chip(57.70, 58.30, "नैतिकता", 800, 280, GB, 44)
chip(58.50, 60.35, "बच्चा खाना नहीं खाए?", 540, 215, DK, 54)
chip(60.45, 62.75, "फोन देना = शॉर्टकट", 720, 250, RB, 38)
chip(62.85, 65.45, "सिखाओ + साथ में टाइम दो", 720, 250, GB, 34)
chip(65.50, 67.70, "वरना गालियां तो मिलेंगी ही", 540, 215, RB, 52)

ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Nirmala UI,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,50,50,250,1
Style: CapLow,Nirmala UI,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,50,50,55,1
Style: Lab,Nirmala UI,50,&H00FFFFFF,&H00FFFFFF,&H002A2AE0,&H00000000,1,0,0,0,100,100,0,0,3,16,0,5,40,40,40,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(ev) + "\n"
open("cap.ass", "w", encoding="utf-8-sig").write(ASS)

# ---------------- SFX ----------------
SFX = [
 (0.00,"impact_trailer",.55),(0.05,"whoosh_cinematic_fast",.5),(2.40,"whoosh_air",.4),(5.25,"whoosh_air",.5),(7.00,"notification_pop",.55),(8.55,"notification_pop",.55),
 (13.10,"suspense_bass",.45),(14.15,"glass_hit_suspense",.55),(15.40,"whoosh_cinematic_fast",.5),(17.55,"notification_pop",.55),(20.10,"whoosh_air",.4),
 (23.30,"impact_big_cinematic",.4),(24.50,"heartbeat_ambience",.9),(24.55,"suspense_bass",.5),(26.65,"whoosh_air",.35),(30.00,"glass_hit_suspense",.45),
 (33.95,"suspense_bass",.5),(37.00,"notification_pop",.6),(41.40,"whoosh_air",.45),(45.40,"glass_hit_suspense",.5),(47.40,"notification_pop",.55),
 (48.20,"notification_pop",.55),(49.00,"notification_pop",.55),(50.45,"whoosh_cinematic_fast",.5),(55.50,"notification_pop",.5),(56.30,"notification_pop",.5),
 (57.00,"notification_pop",.5),(57.70,"notification_pop",.5),(60.40,"whoosh_air",.5),(62.80,"whoosh_air",.5),(65.50,"impact_trailer",.5),
 (67.75,"suspense_bass",.6),(14.85,"whoosh_air",.45),(17.30,"whoosh_air",.45),(26.45,"whoosh_air",.45),(36.90,"whoosh_air",.45),(55.30,"whoosh_air",.45),(67.80,"impact_big_cinematic",.5),
]

# ---------------- ffmpeg ----------------
inputs = ["-i", VID, "-i", A + "/music/bgm_fallen_asper_film_score.mp3"]
for _, f, _v in SFX:
    d_ = "music" if False else "sounds"
    inputs += ["-i", f"{A}/{d_}/{f}.mp3"]
c0 = 2 + len(SFX)
for (n, a, b, x, y) in CARDS: inputs += ["-loop", "1", "-framerate", "30", "-t", f"{b - a + .1:.2f}", "-i", f"cards/{n}.png"]
AN = c0 + len(CARDS)
inputs += ["-i", "anim_panel.mp4"]

ZB = [(0, 1.0), (1.8, 1.06), (5.2, 1.0), (7.0, 1.05), (11.9, 1.0), (15.2, 1.06), (20.1, 1.0), (24.5, 1.08), (26.7, 1.0), (30.0, 1.06), (34.0, 1.0),
      (37.0, 1.05), (41.0, 1.0), (44.5, 1.07), (48.5, 1.0), (50.5, 1.06), (55.5, 1.0), (58.5, 1.06), (62.8, 1.0), (65.5, 1.07), (67.7, 1.0)]
z = "1"; prev = 1.0
for t, v in ZB[1:]:
    z += f"+({v - prev:.3f})*gte(t,{t})"; prev = v
z += "+0.15*min(1,max(0,(t-67.7)/1.9))"

F = []
F.append(f"[0:v]fps=30,split=2[va][vb];[va]scale=w='trunc(1080*({z})/2)*2':h=-2:eval=frame,crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.40',"
         "eq=contrast=1.07:saturation=1.12:brightness=-0.015,unsharp=5:5:0.5,vignette=PI/6,setsar=1,format=yuv420p[v0]")
cur = "v0"
for i, (n, a, b, x, y) in enumerate(CARDS):
    D = b - a; w, h = SZ[n]; xx = x if x is not None else (1080 - w) // 2
    F.append(f"[{c0 + i}:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1,fade=t=out:st={D - 0.22:.2f}:d=0.22:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    F.append(f"[{cur}][c{i}]overlay=x={xx}:y='{y}-40*pow(1-min(1,(t-{a})/0.25),2)':enable='between(t,{a},{b})':format=auto[o{i}]")
    cur = f"o{i}"
EN = "+".join(f"between(t,{a},{b})" for a, b in SPLITS)
F.append("[vb]split=2[vb1][vb2];[vb1]crop=1080:1020:0:520,boxblur=28:2,eq=brightness=-0.12[pbg];[vb2]crop=1080:1360:0:330,scale=810:1020[pfg];[pbg][pfg]overlay=135:0,format=yuv420p[pan]")
F.append(f"[{cur}][pan]overlay=x=0:y=900:enable='gte({EN},1)'[ps]")
TS = "+".join(f"{a}*between(t,{a},{b})" for a, b in SPLITS); TE = "+".join(f"{b}*between(t,{a},{b})" for a, b in SPLITS)
F.append(f"[{AN}:v]format=yuv420p[anp]")
F.append(f"[ps][anp]overlay=x=0:y='-900*max(pow(max(0,1-(t-({TS}))/0.3),2),pow(max(0,1-(({TE})-t)/0.25),2))':enable='gte({EN},1)'[ps2]")
F.append(f"[ps2]drawbox=x=0:y=895:w=iw:h=10:color=0xFFC531:t=fill:enable='gte({EN},1)'[ps3]")
cur = "ps3"
F.append(f"[{cur}]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.30:t=fill:enable='gte(t,67.7)',subtitles=cap.ass:fontsdir=fonts,"
         f"drawbox=x=0:y=1908:w='iw*t/{DUR}':h=12:color=0xFFC531:t=fill[vout]")
F.append("[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,equalizer=f=3500:t=q:w=1:g=2,loudnorm=I=-15:TP=-1.5:LRA=9,asplit=2[vk][vm]")
F.append(f"[1:a]atrim=0:{DUR},volume=0.5,afade=t=in:st=0:d=1.5,afade=t=out:st={DUR-2.3}:d=2.3[bgm]")
F.append("[bgm][vk]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[bgd]")
labels = ["vm", "bgd"]
for i, (t, f, v) in enumerate(SFX):
    ms = int(t * 1000)
    F.append(f"[{2 + i}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}]")
    labels.append(f"s{i}")
F.append("".join(f"[{l}]" for l in labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.95[aout]")
open("graph.txt", "w", encoding="utf-8").write(";\n".join(F))
out = sys.argv[1] if len(sys.argv) > 1 else "out2.mp4"
cmd = ["ffmpeg", "-y", "-v", "error", "-stats"] + inputs + ["-/filter_complex", "graph.txt", "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart"] + sys.argv[2:] + [out]
print(len(inputs) // 2, "inputs; chunks:", len(chunks))
subprocess.run(cmd, check=True)
