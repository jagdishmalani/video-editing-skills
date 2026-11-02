# Claude Code video-editing skills

Three personal Claude Code skills for editing short vertical Hindi/Hinglish videos.

| Skill | Trigger phrase | What it is |
|---|---|---|
| `kamal-editing/` | "kamal style" | Talking-head + news-graphics edit (punch-in zooms, dark info cards, photos, highlighted Hindi captions, SFX, ducked BGM) plus an asset workflow (Google / Wikimedia / Mixkit, ChatGPT-in-Chrome for missing images). |
| `lee-editing/` | "lee style" | Paper-craft Hinglish stickman explainer (illustrated scenes, marker annotations, cloud wipes, varied stickman actions). |
| `mckamal-editing/` | "mckamal style" | Hybrid of the two: speaker full screen with Kamal graphics, plus split-screen beats where the top half is a Lee-style animation explaining the audio while the speaker plays in the bottom half. |

## Install
Copy each folder into `~/.claude/skills/` and add the trigger lines from `CLAUDE.md.example` to `~/.claude/CLAUDE.md`.
Each skill folder has a `reference-code/` with the working ffmpeg + Python scripts (they use local paths from the author's PC; adapt them).
