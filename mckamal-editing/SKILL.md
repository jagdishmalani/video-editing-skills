---
name: mckamal-editing
description: "The user's 'McKamal style' / 'mckamal wali editing': a hybrid of Kamal style (talking-head + news graphics) and Lee style (paper-craft stickman animation). Mostly the speaker full screen with Kamal graphics, but at selected explanatory moments the TOP HALF of the screen switches to a Lee-style animated scene explaining the audio while the speaker keeps playing in the bottom half (split screen). Use when the user says 'mckamal style', 'mckamal wali editing', 'mckamal editing', 'mc kamal'."
---

# McKamal editing style (Kamal + Lee mix)

The user calls this **"McKamal style" / "mckamal wali editing"**. It was built for their second video (`second video/kamal new second.MP4`, a Hindi commentary on child-violence news and parenting) and delivered as `second_video_kamal_lee_mix.mp4`. They chat in Hinglish; answer in Hinglish.

## The one rule
Copy the **editing language only**. Script, hook, facts, photos, animation scenes, props and characters are new for every video. Never reuse the sample's content.

## Ingredients
This style = the `kamal-editing` skill (read it: base footage, zoom punch-ins, dark glass cards, captions, SFX, ducked BGM, asset workflow incl. ChatGPT-in-Chrome image generation) **plus** the `lee-editing` skill (paper-craft illustrated scenes, stickmen with varied actions, marker annotations, wipes). Invoke both skills' rules; this file only defines how they are combined.

## How the two are combined
1. **Default state = Kamal:** speaker full screen (1080x1920), jump-cut punch-in zooms, cards and chips in the top band (face sits in the lower ~70% when the speaker is close to the camera: check a frame first and keep graphics above the head top), highlighted captions, SFX, BGM.
2. **At 3-5 explanatory beats (roughly 40-60% of the runtime, each 6-13 s) switch to SPLIT SCREEN:**
   - Top 0-900 px: a Lee-style animated panel (1080x900) that visually explains what is being said (a scene with a background, stickmen acting, props, marker annotations, short Roman-Hinglish/English tags).
   - Bottom 900-1920 px: the speaker keeps playing, shrunk so head+shoulders fit: crop 1080x1360 from source y=330, scale to 810x1020, centred over a blurred, darkened copy of the same footage (1080x1020). Captions move to the very bottom (smaller margin, ~84 pt).
   - Thin gold divider line at y=895-905. The animation panel slides in from the top (~0.3 s) and out (~0.25 s) with a whoosh SFX at each end; the speaker panel jumps in.
   - While split, hide Kamal's PNG cards and ASS chips that fall inside the split window (the animation carries the meaning); captions stay.
3. **Pick split beats** where there is a story/scene/concept to show (an incident, a comparison, a crowd/opinion, a how-to), and keep numbers/names/emotional punchlines full-screen with Kamal graphics. Keep the hook and the ending full-screen (ending: slow push-in + dim).
4. **Animation content rules (Lee style):** each beat gets its own background (school, classroom, ECG screen, night city, home...) chosen from the script; multiple stickmen with distinct accessories (cap, bow, bun, tie, hat); different actions per beat (walking in/out, offering a heart, holding a phone, hand on a child's head, crowd pointing); marker graphics (big red X, alert triangles, hearts, clock, play icon, ECG line); paper-tape tags; a polaroid of a real location photo dropping in; clouds drifting; light grain; pop-in with overshoot.
5. **Sensitive topics (violence against children etc.):** never depict violence or injury. Show the situation through reactions (fear, anger marks, alert triangle, ECG, "NO!" with a crossed heart), text and neutral location photos. Tell the user this choice.

## Build recipe that worked on this PC (adapt, do not copy content)
- Folder `reference-code/` has the working scripts:
  - `build2.py`: full Kamal build for the second video (cards via PIL for Latin/numbers; Hindi via ASS with "Nirmala UI"; caption chunks from timed script segments; SFX list; ffmpeg graph with zoom punch-ins, overlays, ducked BGM).
  - `anim.py`: Lee-style animation panel renderer (PIL at 2x supersampling): backgrounds `bg_*`, a parametric `person()` stickman with IK arms and moods, props (`tag`, `heart`, `bigx`, `alert`, `phone`, `polaroid`), scenes A-D + ECG, written to `anim_panel.mp4` (black outside the split windows; wrapped in try/except so one bad frame cannot kill the render).
  - `mk3.py` -> generates `build3.py` from `build2.py`: adds `SPLITS`, hides cards/chips inside splits, `CapLow` caption style, extra whooshes, the speaker-panel branch (`split=2[va][vb]`), the animation overlay with slide in/out and the divider line.
  - Order: render `anim_panel.mp4` first (`python -I -X utf8 anim.py anim_panel.mp4`, ~4 min), then `build3.py out.mp4` (~3.5 min). Run in the background; check frames; say honestly what was not verified (audio not listened to).
- Timing: faster-whisper "small" with the script as `initial_prompt` and `word_timestamps=True` (decode wav to 16 kHz mono numpy). It failed on a noisy middle section: fall back to proportional character-weighted timing between reliable anchors and tell the user the sync there is approximate.
- Pitfalls hit: PIL fonts need size > 0 (guard pop-in scales of 0); `ImageDraw.rectangle` needs x1>=x0 (guard tiny scales); `python -I` does not add the script dir to `sys.path` (insert it manually); ffmpeg here needs `-/filter_complex file`.
- Assets: follow the `kamal-editing` asset workflow (Wikimedia Commons, Mixkit; ChatGPT in Chrome for missing images; keep `ATTRIBUTION.txt`).
