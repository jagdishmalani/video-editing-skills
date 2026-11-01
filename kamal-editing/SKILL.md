---
name: kamal-editing
description: "The user's 'Kamal style' / 'kamal wali editing': professional talking-head + news-graphics editing of a raw vertical video (full-screen speaker, jump-cut punch-in zooms, dark glass info cards, photos, Hindi captions with highlighted keywords, SFX, ducked dark BGM). Includes the asset workflow: find images/sounds on Google/Wikimedia/Mixkit, and generate missing images via ChatGPT in a Chrome tab. Use when the user says 'kamal style', 'kamal wali editing', 'kamal editing' or 'kamal style me edit karo'."
---

# Kamal editing style

The user calls this **"Kamal style" / "kamal wali editing"**. It is the professional edit built on their raw talking-head video `raw video.MOV` -> `final_edit.mp4` (Hindi news-explainer about an IAS couple's property deal). They chat in Hinglish; answer in Hinglish.

## The one rule
Copy the **editing language only**. Script, hook, facts, photos, cards and sounds are new for every video. Never reuse the sample's content (names, numbers, photos) in a new video.

## Inputs to confirm (ask only what is missing)
- Raw video file (the speaker stays on screen, original voice kept) and the script/transcript (ask the user to paste it, or transcribe; see tools below).
- Aspect ratio: default 9:16, 1080x1920, 30 fps.

## Style definition
**Base footage:** the speaker's raw video full screen, original audio. Do not cut unless there are real long pauses/mistakes. Light grade: contrast ~1.07, saturation ~1.15, slight sharpen, vignette.

**Camera:** jump-cut punch-ins at each sentence change (hard cut between 1.0x and ~1.07-1.10x; 1.12x on big moments), alternating, never smooth-zoom through the whole video. Slow push-in (to ~1.16x) over the final line with a slight dim for suspense.

**Graphics (upper part of the frame, never covering the face; the face sits in the lower 60%):**
- Dark glass rounded cards with a thin gold/red/green border for numbers and facts (strike-through old value then new value, big count/percent numbers).
- Photos/evidence in rounded framed cards: news clipping, people, places, documents, with name chips or labels.
- Special cards as needed: calendar/date card, stamp (e.g. ACB), logo card, monogram placeholder when no photo exists.
- Coloured label chips (red/dark) above or under cards for names and terms.
- Each element slides ~40px down while fading in (~0.25s), fades out; one focus at a time; roughly one graphic per fact.
- Full-width thin progress bar along the bottom.

**Captions:** bottom area (above the shirt/hands zone, ~y 1450-1650 on 1080x1920), 2-4 word chunks, bold white with black outline, tiny pop-in scale (86% -> 100%), key words (numbers, names, emotional words) in yellow/gold. Hindi in Devanagari when the speech is Hindi.

**Sound:**
- Voice cleanup: high-pass 80 Hz, light compression, presence EQ, loudnorm (~ -15 LUFS).
- SFX on every graphic: impact hit on the opening/hook and big reveals, coins for money, camera shutter for photos, paper slide for documents, glass hit/suspense bass for questions, whoosh for transitions, notification pop for stats, tick-tock + suspense bass for the ending.
- BGM: dark/mysterious track at low level, side-chain ducked under the voice, fade in at the start and out over the last ~2s.

**Pacing/structure:** hook with the biggest number or question in the first second, fact -> graphic -> sound, question beats get a zoom + glass hit, ending with a dimmed push-in and the unanswered question.

## When animation is needed
If a point needs real animation (explaining a concept, a process, motion), insert a short animated cut-in in the **Lee style**: invoke the `lee-editing` skill and use its paper-craft illustrated scene + stickman + marker annotations for that part, then return to the speaker. Keep it short (a few seconds) and make it a clean cut/wipe in and out.

## Assets: find them yourself (do not ask the user to supply them)
The user has authorised downloading the assets needed for these videos. For each download, state source and filename in the message; do not ask them to fetch things. Always keep an `ATTRIBUTION.txt` of sources/licences in the assets folder.

1. **Photos/logos of real people, places, organisations:**
   - First try Wikimedia Commons via its API (`commons.wikimedia.org/w/api.php`, generator=search, namespace 6, prop=imageinfo with url|size|extmetadata; fetch the URL; note licence; credit CC BY-SA ones).
   - Then Google Images / news sites in a Chrome tab (claude-in-chrome tools; load via ToolSearch first). Prefer official/press/government images. Be careful with news-agency copyright and tell the user when an image is copyrighted.
2. **Sound effects and music:** Mixkit (SFX pages `mixkit.co/free-sound-effects/<category>/`, direct file `assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`; music `mixkit.co/free-stock-music/mood/dark/`, direct file `assets.mixkit.co/music/<id>/<id>.mp3`). Also Pixabay/YouTube Audio Library in the browser if needed. Categories used before: money, impact, paper, camera, whoosh, typing, alarm, suspense, notification.
3. **Missing image -> generate it with ChatGPT in Chrome:** if an asset (object, illustration, scene, prop, person-like illustration) cannot be found, open `chatgpt.com` in a Chrome tab with the claude-in-chrome tools, write a clear image prompt (subject, style, aspect ratio, transparent/plain background if needed), generate, then save/download the image into the project assets folder. Rules:
   - If ChatGPT is not signed in or asks for login/captcha/payment, stop and ask the user to sign in; never type passwords or solve captchas.
   - Never put the user's private data in prompts. Do not generate realistic fake photos of real people presented as real evidence; use illustrations/placeholders and label them.
   - Check the generated image before using it; regenerate if text/faces are wrong.
4. Put everything under `assets/images`, `assets/sounds`, `assets/music` in the project folder, with readable file names.

## Build tools that worked on this PC
- Windows; ffmpeg + Python 3.13 (faster-whisper, PIL). No GPU AI stack (GTX 1650 4GB).
- ffmpeg here is a new build: use `-/filter_complex file`, not `-filter_complex_script`.
- Hindi captions/labels: ffmpeg `subtitles` (libass) with font "Nirmala UI" (copy `C:\Windows\Fonts\Nirmala.ttc` into a local fonts dir, `fontsdir=`); PIL cannot shape Devanagari. Latin/number cards can be drawn with PIL (NotoSans-Bold).
- Timing: faster-whisper small with `word_timestamps=True`, script as `initial_prompt`; decode audio to 16 kHz mono wav with ffmpeg and pass a numpy array (its built-in decode is broken here). Run Python with `-I -X utf8`.
- `reference-code/build.py` is the full working pipeline of this style (cards via PIL, ASS captions, zoom punch-ins, overlay slide/fade, SFX/BGM mix with sidechain ducking, progress bar); `build_toon.py` is the toon-filter variant. Paths and content are from the sample video: adapt, do not copy content.
- Render in the background (~4 min for 84s at 1080x1920 for this style), check frames, and say honestly what was and was not verified (e.g. audio not listened to).
