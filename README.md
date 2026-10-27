# UT_novel 💬🎬

A **Multi-Template Dialogue & Background Video Generator** that renders high-definition dialogue videos (1080p MP4) directly from **Markdown script files**.

Supports **Undertale 8-bit retro aesthetic** and **R4 (Ridge Racer Type 4) cinematic briefing HUD**, dual voice modes (Classic 8-bit Voice Blips & English AI TTS with automatic lip-sync), word wrapping, inline emotion tags, looping background videos, and dedicated 16:9 Landscape & 9:16 Vertical (Shorts/TikTok) layouts.

---

## ✨ Features

- **Markdown-Driven Video Generation**: Write simple, intuitive Markdown scripts to produce ready-to-publish MP4 videos.
- **Multi-Template Architecture**:
  - **`undertale_16_9` / `undertale_9_16`**: Authentic Undertale pixel-bordered dialogue box, pixel fonts (PixelOperator), and retro character portraits.
  - **`r4_16_9` / `r4_9_16`**: Ridge Racer Type 4 inspired dark semi-transparent slit window, vibrant R4 racing yellow accents, modern sans-serif typography, and tactical HUD header bars.
- **Dual Voice Modes**:
  - `blip`: Character text sounds (Retro 8-bit blips for Undertale, crisp cyber click SE for R4).
  - `tts`: English AI speech synthesis with **automatic audio-driven typing speed & lip-sync** (Bobbing animation or HUD focus while speaking).
- **English Word Wrapping**: Intelligently breaks lines at word boundaries so text never gets awkwardly split mid-word.
- **Inline Special Effect Tags**:
  - `[shake]...[/shake]`: Shaking text effect on specific words.
  - `[color: yellow]` / `[color: red]` / `[color: #hex]`: Custom text colors.
  - `[wait: 0.8]`: Dramatic mid-sentence pauses.
  - `[se: sound_name]`: Trigger custom sound effects at exact word timings.
- **Looping Video Backgrounds**: Seamlessly loops MP4 background footage behind the dialogue box.
- **Splash Screens & Cinematic Transitions**: Full-screen opening/ending splash screens without dialogue boxes, featuring smooth black fade-in and fade-out transitions.
- **Multi-Aspect Ratio Dedicated Templates**:
  - `16:9` (1920x1080): YouTube standard landscape video.
  - `9:16` (1080x1920): YouTube Shorts, TikTok, and Instagram Reels layout with mobile UI safety padding.
- **Background Music (BGM)**: Automatic looping and smooth fade-out at the end of the video.

---

## 🎨 Available Templates

You can list all registered templates with:

```bash
python3 -m ut_novel.cli templates
```

| Template ID | Resolution | Style & UI Layout | Typography & Prefix | Sound Effect (Blip) |
| :--- | :--- | :--- | :--- | :--- |
| **`undertale_16_9`** | 1920×1080 | Bottom-centered pixel double-border box | PixelOperator (56pt), `* ` | Retro 8-bit Voice Blip |
| **`undertale_9_16`** | 1080×1920 | Square-proportioned pixel box (bottom 280px safe margin) | PixelOperator (46pt), `* ` | Retro 8-bit Voice Blip |
| **`r4_16_9`** | 1920×1080 | Authentic 4-layer R4 meeting screen (Yellow mat frame + inner white viewport + central thick-bordered portrait + `*Message` tab box) | Modern Sans Bold (42pt), Clean | Tight Cyber UI Click |
| **`r4_9_16`** | 1080×1920 | Authentic 4-layer R4 meeting screen for vertical Shorts (safe-area margins avoiding mobile controls) | Modern Sans Bold (38pt), Clean | Tight Cyber UI Click |

---

## 🚀 Quick Start

### 1. Requirements & Installation

```bash
# System dependency
sudo apt install -y ffmpeg

# Python dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Basic Commands

Render a Markdown dialogue script to MP4:

```bash
# 1. Undertale 16:9 Landscape
python3 -m ut_novel.cli render --script examples/dialogue_ruins.md -o output/ruins.mp4

# 2. Undertale 9:16 Vertical Shorts
python3 -m ut_novel.cli render --script examples/shorts_encounter.md -o output/shorts.mp4

# 3. R4 (Ridge Racer Type 4) 16:9 Landscape Briefing
python3 -m ut_novel.cli render --script examples/r4_briefing_16_9.md -o output/r4_16_9.mp4

# 4. R4 (Ridge Racer Type 4) 9:16 Vertical Shorts Briefing
python3 -m ut_novel.cli render --script examples/r4_briefing_9_16.md -o output/r4_9_16.mp4

# Override template from command line
python3 -m ut_novel.cli render --script examples/dialogue_ruins.md -o output/override.mp4 --template r4_16_9

# Fast preview mode (render only the first 3 seconds)
python3 -m ut_novel.cli render --script examples/r4_briefing_16_9.md -o output/preview.mp4 --preview-sec 3.0
```

---

## 📝 Markdown Script Syntax

A `.md` script file consists of YAML Frontmatter followed by dialogue lines.

### Example: `r4_briefing_16_9.md`

```markdown
---
title: "PAC Racing Club - Stage 01 Briefing"
template: "r4_16_9"                 # "r4_16_9", "r4_9_16", "undertale_16_9", "undertale_9_16"
fps: 30
bg: "assets/bg/r4_paddock_night.jpg"# Static image or looping MP4 video
bgm: "assets/bgm/ruins_theme.wav"   # Background music
bgm_volume: 0.4                     # 0.0 to 1.0

characters:
  emma:
    name: "Emma"
    voice_mode: "blip"
    default_face: "smile"
    faces:
      smile: "assets/char/dev_girl_1/r4_smile.png"
---

* emma(smile): Listen up, ace.[wait: 0.4] Track temperature is dropping fast tonight.
* emma(smile): Keep your focus sharp and [color: yellow]warm up the tires[/color] on the formation lap.
* emma(smile): The crew tuned your machine to perfection.[wait: 0.4] Bring us the [shake]VICTORY[/shake]!
```

### Inline Tag Reference

| Tag | Purpose | Example |
| :--- | :--- | :--- |
| `[wait: seconds]` | Pause typing temporarily | `Wait for it...[wait: 0.8]Boo!` |
| `[color: name/#hex]` | Change color of enclosed text | `You have [color: yellow]DETERMINATION[/color].` |
| `[shake]...[/shake]` | Tremble and shake words | `I am [shake]SO ANGRY[/shake]!` |
| `[se: sound_name]` | Trigger an SE at this word | `Watch out![se: hit]` |
| `[voice: file.wav]` | Attach a pre-recorded audio file | `* narrator: [voice: "clip.wav"] Silence.` |

---

## 📁 Repository Structure

```text
UT_novel/
├── assets/
│   ├── bg/                  # Background images & videos (ruins, r4_paddock, etc.)
│   ├── bgm/                 # Background music loops
│   ├── char/                # Character portraits (dev_boy_1, dev_girl_1, r4_commander)
│   ├── fonts/               # Pixel fonts (PixelOperator.ttf) & Modern fonts (ModernSans-Bold.ttf)
│   └── se/                  # Voice blips (voice_default.wav) & R4 click (r4_click.wav)
├── examples/
│   ├── dialogue_ruins.md    # Undertale 16:9 sample
│   ├── shorts_encounter.md  # Undertale 9:16 Shorts sample
│   ├── r4_briefing_16_9.md  # R4 16:9 Landscape briefing
│   └── r4_briefing_9_16.md  # R4 9:16 Vertical Shorts briefing
├── src/ut_novel/
│   ├── templates/           # ★ Multi-template Architecture
│   │   ├── base.py          # BaseTemplate abstract class
│   │   ├── registry.py      # TemplateRegistry
│   │   ├── undertale_16_9.py# Undertale 16:9 implementation
│   │   ├── undertale_9_16.py# Undertale 9:16 implementation
│   │   ├── r4_16_9.py       # R4 16:9 implementation
│   │   └── r4_9_16.py       # R4 9:16 implementation
│   ├── audio/               # Blip generator, TTS providers, BGM mixer
│   ├── encoder/             # FFmpeg raw pipe encoder
│   ├── parser/              # Frontmatter, RichText, WordWrapping
│   ├── engine.py            # Clean Template-driven NovelEngine pipeline
│   └── cli.py               # CLI command interface
└── memo/PLAN/               # Complete project plan & milestones
```

---

## 📜 License
MIT License
