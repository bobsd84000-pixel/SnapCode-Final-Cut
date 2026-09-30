# 🎬 SnapCode 3D — Brag Video Generation

This directory contains the output of the **`/brag`** skill test on SnapCode 3D.

## 📋 Files in This Directory

| File | Purpose |
|------|---------|
| **brag-plan.md** | Complete creative brief & storyboard (6 scenes, 18 seconds) |
| **brag-video.html** | Animated HTML source (ready to render into video) |
| **share-copy.txt** | Social media caption (1–3 sentences) |
| **render_video.py** | Python script to generate frames & MP4 |
| **render-video.js** | Node.js/Playwright alternative renderer |
| **create_brag_video.sh** | Bash helper for ffmpeg |
| **TEST-SUMMARY.md** | Full test results & environment notes |

## 🎯 Video Specifications

| Aspect | Value |
|--------|-------|
| **Duration** | 18 seconds (15–25s target) |
| **Resolution** | 1920×1080 (landscape) |
| **Frame Rate** | 30 fps |
| **Format** | MP4 (H.264) |
| **Tone** | Polished, technical premium |
| **Style** | Modern product launch video |

## 🎨 Creative Direction

**Hook:** "Snapcode 3D — 3D → Code"  
**Core Message:** Turn 3D captures into production-ready Three.js code instantly  
**Audience:** 3D artists, developers, creative technologists  

### Scene Breakdown

1. **Hook (0–2s):** Title + tagline reveal
2. **Upload (2–4s):** Drop zone interaction
3. **Processing (4–7s):** API processing visualization
4. **Preview (7–13s):** Live 3D preview (rotating ring)
5. **Code (13–16s):** Generated code panel
6. **CTA (16–18s):** Call-to-action

## 🚀 How to Render the Video

### Prerequisites

Choose one based on your environment:

#### Option 1: Python + FFmpeg (Recommended)
```bash
apt-get update
apt-get install -y ffmpeg python3-pil

cd brag-output
python3 render_video.py
```

#### Option 2: Node.js + Playwright
```bash
npm install
node render-video.js
```

#### Option 3: Direct FFmpeg
```bash
# If you have HTML content to render, use:
ffmpeg -f lavfi -i "color=navy:s=1920x1080:d=18" \
  -c:v libx264 -pix_fmt yuv420p brag.mp4
```

### Output

After rendering, you'll have:
- **`brag.mp4`** — The final 18-second video
- **`brag.jpg`** — Poster thumbnail (frame 0)
- **`frames/`** — Intermediate PNG frames (optional cleanup)

## 📱 Sharing

Use the content in **share-copy.txt**:

```
Snapcode 3D: Turn your 3D captures into Three.js code instantly. 
Built for artists and developers who want to take their 3D models 
straight to the web. Perfect for Armorpaint, photogrammetry, and 3D workflows.
```

Post on:
- Twitter/X with `brag.mp4`
- LinkedIn with poster + caption
- Email/Slack with direct link

## 🔧 Customization

Edit **brag-plan.md** to:
- Change tone (e.g., `chaotic`, `deadpan`, `cinematic`)
- Adjust duration (keep 15–25 seconds)
- Modify scene order or emphasis
- Update share caption

Then re-render with updated HTML or scripts.

## ✨ Skill Information

- **Skill:** `/brag` (full featured) or `/brag-slim` (lightweight)
- **Installed:** `.claude/skills/brag/`
- **Status:** Production ready
- **Last tested:** 2026-09-30

---

**Questions?** Check the skills documentation in `.claude/skills/brag/SKILL.md`
