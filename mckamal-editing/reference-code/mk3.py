s=open("build2.py",encoding="utf-8").read()
def rep(a,b,cnt=1):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,cnt)
rep("DUR = 69.6\n","DUR = 69.6\nSPLITS = [(5.3, 14.9), (17.4, 26.5), (37.0, 50.5), (55.4, 65.5)]\ndef insplit(t): return any(a <= t < b for a, b in SPLITS)\n")
rep("# (png, tin, tout, x|None, y)\nCARDS = [","# (png, tin, tout, x|None, y)\nCARDS_ALL = [")
rep("SZ = {n:","CARDS = [c for c in CARDS_ALL if not insplit(c[1])]\nSZ = {n:")
# chip skip inside splits
lines=s.split("\n")
for i,l in enumerate(lines):
    if l.startswith("def chip("):
        head,body=l.split("): ",1)
        lines[i]=head+"):\n    if insplit(t0): return\n    "+body
s="\n".join(lines)
rep("},Cap,,0,0,0,,{{","},{('CapLow' if insplit(t) else 'Cap')},,0,0,0,,{{")
rep("Style: Lab,Nirmala UI,50,","Style: CapLow,Nirmala UI,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,3,2,50,50,55,1\nStyle: Lab,Nirmala UI,50,")
rep('(67.75,"suspense_bass",.6),','(67.75,"suspense_bass",.6),(14.85,"whoosh_air",.45),(17.30,"whoosh_air",.45),(26.45,"whoosh_air",.45),(36.90,"whoosh_air",.45),(55.30,"whoosh_air",.45),')
rep('for (n, a, b, x, y) in CARDS: inputs += ["-loop", "1", "-framerate", "30", "-t", f"{b - a + .1:.2f}", "-i", f"cards/{n}.png"]',
    'for (n, a, b, x, y) in CARDS: inputs += ["-loop", "1", "-framerate", "30", "-t", f"{b - a + .1:.2f}", "-i", f"cards/{n}.png"]\nAN = c0 + len(CARDS)\ninputs += ["-i", "anim_panel.mp4"]')
rep('F.append(f"[0:v]fps=30,scale=','F.append(f"[0:v]fps=30,split=2[va][vb];[va]scale=')
blk='''EN = "+".join(f"between(t,{a},{b})" for a, b in SPLITS)
F.append("[vb]split=2[vb1][vb2];[vb1]crop=1080:1020:0:520,boxblur=28:2,eq=brightness=-0.12[pbg];[vb2]crop=1080:1360:0:330,scale=810:1020[pfg];[pbg][pfg]overlay=135:0,format=yuv420p[pan]")
F.append(f"[{cur}][pan]overlay=x=0:y=900:enable='gte({EN},1)'[ps]")
TS = "+".join(f"{a}*between(t,{a},{b})" for a, b in SPLITS); TE = "+".join(f"{b}*between(t,{a},{b})" for a, b in SPLITS)
F.append(f"[{AN}:v]format=yuv420p[anp]")
F.append(f"[ps][anp]overlay=x=0:y='-900*max(pow(max(0,1-(t-({TS}))/0.3),2),pow(max(0,1-(({TE})-t)/0.25),2))':enable='gte({EN},1)'[ps2]")
F.append(f"[ps2]drawbox=x=0:y=895:w=iw:h=10:color=0xFFC531:t=fill:enable='gte({EN},1)'[ps3]")
cur = "ps3"
'''
rep('F.append(f"[{cur}]drawbox=x=0:y=0',blk+'F.append(f"[{cur}]drawbox=x=0:y=0')
open("build3.py","w",encoding="utf-8").write(s)
