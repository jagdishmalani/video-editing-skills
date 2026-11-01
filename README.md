# Claude Code video-editing skills

Two personal Claude Code skills for editing short vertical Hindi/Hinglish videos.

| Skill | Trigger phrase | What it is |
|---|---|---|
| `kamal-editing/` | "kamal style" | Talking-head + news-graphics edit (punch-in zooms, dark info cards, photos, highlighted Hindi captions, SFX, ducked BGM) plus an asset workflow (Google / Wikimedia / Mixkit, ChatGPT-in-Chrome for missing images). |
| `lee-editing/` | "lee style" | Paper-craft Hinglish stickman explainer (illustrated scenes, marker annotations, cloud wipes, varied stickman actions). |

## Install
Copy each folder into `~/.claude/skills/` and add the trigger lines from `CLAUDE.md.example` to `~/.claude/CLAUDE.md`.
Each skill folder has a `reference-code/` with the working ffmpeg + Python scripts (they use local paths from the author's PC; adapt them).
