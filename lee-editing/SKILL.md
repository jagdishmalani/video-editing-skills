---
name: lee-editing
description: "The user's signature 'lee wali editing' / 'lee style' video editing style: a paper-craft Hinglish stickman explainer (vertical 9:16). Use whenever the user says 'lee wali editing', 'lee style', 'lee editing', or asks to edit a script/video in the style of their sample video. Apply the STYLE only; hook, script, backgrounds, objects and scenes are new for every video."
---

# Lee editing style (user's signature look)

The user calls this **"lee wali editing" / "lee style"**. It comes from their `sample video.mp4` (a helicopter / Earth-rotation explainer). They chat in Hinglish; answer in Hinglish.

## The one rule
Copy the **editing language only**. Never copy the sample's hook, script, scenes, characters or objects. For every new script, invent a NEW hook, NEW script-driven backgrounds, NEW props/objects and NEW scenes. Do not reuse earlier videos' visuals either.

## Inputs to confirm (ask only what is missing)
- Script/transcript (file or pasted text).
- Raw talking-head video available? Keep the user's original voice? (Default: keep the original audio if a raw video is given; otherwise ask about voiceover.)
- Output language of on-screen text: default Roman Hinglish (not Devanagari) unless the user says otherwise.

## Style definition
**Format:** 9:16 vertical, 30 fps, 60-90s. Hinglish narration.

**Look:** Every idea/beat gets its own illustrated "paper-craft" scene: flat 2D, visible paper grain/texture, soft gradients, outlines. Pick day/dusk/night colour grading to fit the script. Occasionally one key object is more realistic/textured against the flat scene (like the globe in the sample) to pull focus.

**Characters:**
- Simple stickman(s): round smiley head, white outer outline (sticker look). Several stickmen are allowed and encouraged when the script needs them (two people talking, crowd, hero vs villain, roles), each with a distinct look (hat, colour, size).
- NEVER loop one movement across the whole video (the user found a single idle/gesture cycle boring). Each scene gets its own action derived from the script: walking, running, jumping, pointing, picking up/holding props, reacting, sitting, turning, entering/leaving frame, interacting with scene props. Vary pose, angle (front/side/back), distance (wide/close-up) and speed; leave the character out of some shots (props + text only). Use ghost/dashed trails for jumps and an "X" floor marker where useful.

**Pacing:** shots 4-12s with continuous internal animation; few hard cuts; new scene/treatment every ~8-12s; one visual change or annotation per spoken line; one focus at a time.

**Motion:** parallax pan/scroll, camera tilt and zoom, small loops (clouds drift, steam, spinning parts), pop-in with overshoot/bounce then settle, vignette, light grain, spotlight cones.

**Transitions:** cloud/paper wipe; scalloped "postage stamp" border frame holding a mini scene; polaroid dropping in tilted then a red X for wrong guesses; frame-inside-frame inset.

**Typography and graphics:**
- Paper-tape/clip tag cards with an icon (e.g. clock) for key terms.
- Handwritten brush labels.
- Big numbers on a paper sign; red arrow labels (e.g. speed).
- Marker annotations: red circles/loops, ticks, crosses, dotted measure lines, hand-drawn "?", curved arrows pointing at things.
- Text short, one idea, appears exactly when spoken.

**Story pattern (adapt to the script, hook always new):** hook question -> fun/benefit -> "par aisa nahi hota, kyun?" -> everyday analogy acted out by stickman -> apply to the real topic with a big number reveal -> wrong guess crossed out -> conclusion + CTA pill ("Follow for more").

**Audio:** voice leads, consistent loudness (about -14 LUFS), tight pauses; add SFX (whoosh, pop, etc.) and a ducked BGM. The sample's SFX/music were not listened to (only loudness measured), so choose by judgement.

## How to build it (tools that worked on the user's PC)
- Windows, ffmpeg + Python 3.13 (faster-whisper, PIL). No AI image/TTS keys, GTX 1650 4GB, so illustrations must be drawn in code (PIL/SVG). Say honestly they will be a simpler version of the sample.
- Hindi/Devanagari text: render through ffmpeg `subtitles` (libass) with font "Nirmala UI" (`C:\Windows\Fonts\Nirmala.ttc`, copy into a local fonts dir and pass `fontsdir`). PIL without raqm cannot shape Devanagari.
- Word timing: faster-whisper "small" with `word_timestamps=True` and the script as `initial_prompt` gives usable timings. faster-whisper's own audio decode is broken on this PC (av version): load a 16 kHz mono wav via numpy and pass the array. Use `python -I -X utf8`.
- Free sounds/music: Mixkit (assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3; music assets.mixkit.co/music/<id>/<id>.mp3). Free photos: Wikimedia Commons API (credit CC BY-SA ones).
- ffmpeg here is a new build: use `-/filter_complex file` instead of `-filter_complex_script`.
- `reference-code/` in this skill folder has the working scripts from earlier builds: `stick.py` (stickman renderer with lip-sync from audio, paper-style cards, ASS captions, SFX/BGM mix), `stick2.py` (illustrated day/dusk/night parallax backgrounds + cloud wipes, monkey-patches stick.py), `build.py` (earlier pro edit with cards, zoom punch-ins, SFX/BGM ducking). They expect the user's earlier folder layout; adapt paths. Reuse the ideas/code, but rewrite scenes, props and character actions for each new script.
- Renders are slow (~10 min for 84s at 1080x1920); run them in the background and check frames before delivering. Never claim the video was watched/listened to if only frames were checked.
