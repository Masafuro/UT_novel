# UT_novel 💬🎬

An **Undertale-style dialogue and background video generator** that renders high-definition dialogue videos (1080p MP4) directly from **Markdown script files**.

Supports both **Classic 8-bit Voice Blips (peep-peep text sounds)** and **English AI Text-To-Speech (TTS)** with automatic lip-sync, word wrapping, inline emotion tags, looping background videos, and multi-aspect ratio layouts (16:9 Landscape & 9:16 Vertical Shorts/TikTok).

---

## ✨ Features

- **Markdown-Driven Video Generation**: Write simple, intuitive Markdown scripts to produce ready-to-publish MP4 videos.
- **Undertale Aesthetic**: Authentic pixel-bordered dialogue box, pixel fonts (PixelOperator/Determination), and retro character portraits.
- **Dual Voice Modes**:
  - `blip`: Classic Undertale text sounds (letters trigger blips, spaces are silent, punctuation pauses).
  - `tts`: English AI speech synthesis with **automatic audio-driven typing speed & lip-sync** (Bobbing animation while speaking, neutral when silent).
- **English Word Wrapping**: Intelligently breaks lines at word boundaries so text never gets awkwardly split mid-word.
- **Inline Special Effect Tags**:
  - `[shake]...[/shake]`: Shaking text effect on specific words.
  - `[color: yellow]` / `[color: red]` / `[color: #hex]`: Custom text colors.
  - `[wait: 0.8]`: Dramatic mid-sentence pauses.
  - `[se: sound_name]`: Trigger custom sound effects at exact word timings.
- **Looping Video Backgrounds**: Seamlessly loops MP4 background footage behind the dialogue box.
- **Splash Screens & Cinematic Transitions**: Full-screen opening/ending splash screens without dialogue boxes, featuring smooth black fade-in and fade-out transitions.
- **Multi-Aspect Ratio**:
  - `16:9` (1920x1080): YouTube standard landscape video.
  - `9:16` (1080x1920): YouTube Shorts, TikTok, and Instagram Reels layout.
- **Background Music (BGM)**: Automatic looping and smooth fade-out at the end of the video.

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

### 2. Basic Command

Render a Markdown dialogue script to MP4:

```bash
# Standard 16:9 Landscape
python3 -m ut_novel.cli render --script examples/dialogue_ruins.md -o output/video.mp4

# Vertical 9:16 (YouTube Shorts / TikTok)
python3 -m ut_novel.cli render --script examples/shorts_encounter.md -o output/shorts.mp4

# Fast preview mode (render only the first 5 seconds)
python3 -m ut_novel.cli render --script examples/shorts_encounter.md -o output/preview.mp4 --preview-sec 5.0
```

---

## 📝 Markdown Script Syntax

A `.md` script file consists of YAML Frontmatter followed by dialogue lines.

### Example: `script.md`

```markdown
---
title: "Underground Encounter"
aspect_ratio: "16:9"       # "16:9" or "9:16" (Shorts)
fps: 30
bg: "assets/bg/ruins_hall.jpg"      # Static image or looping MP4 video
bgm: "assets/bgm/ruins_theme.wav"   # Background music
bgm_volume: 0.5                     # 0.0 to 1.0

# Optional Full-screen Splash Screens (no dialogue box)
splash_start:
  image: "assets/bg/title_mount_ebott.jpg"
  duration: 2.5
  fade_in: 0.5
  fade_out: 0.5
  transition: "fade_black"

splash_end:
  image: "assets/bg/ruins_hall.jpg"
  duration: 2.0
  fade_in: 0.5
  fade_out: 0.5
  transition: "fade_black"

characters:
  dev_girl_1:
    name: "Emma"
    voice_mode: "tts"               # "tts" or "blip"
    tts:
      provider: "gtts"
      voice_id: "uk"                # British accent ("uk", "us", etc.)
    default_face: "smile"
    faces:
      smile: "assets/char/dev_girl_1/smile.jpg"

  dev_boy_1:
    name: "Alex"
    voice_mode: "blip"
    voice: "assets/se/voice_low.wav" # 8-bit blip sound
    default_face: "smile"
    faces:
      smile: "assets/char/dev_boy_1/smile.jpg"
---

# Lines with speakers and facial expressions:

* dev_girl_1(smile): Welcome, traveler![wait: 0.5] Always stay filled with [color: yellow]DETERMINATION[/color].
* dev_boy_1(smile): hey. don't look so [shake]rattled[/shake]. take a break and check your map.
* dev_girl_1(smile): Good advice, Alex![wait: 0.4] Let us continue forward together.
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
│   ├── bg/                  # Background images & videos
│   ├── bgm/                 # Background music loops
│   ├── char/                # Character portraits (dev_boy_1, dev_girl_1)
│   ├── fonts/               # Pixel fonts (PixelOperator.ttf)
│   └── se/                  # Voice blips and sound effects
├── examples/
│   ├── dialogue_ruins.md    # Voice blip multi-dialogue sample
│   ├── dialogue_tts.md      # Dual AI English TTS dialogue sample
│   ├── dialogue_m5_rich.md  # Video background + Rich tags demo
│   ├── shorts_encounter.md  # 9:16 Vertical YouTube Shorts sample
│   ├── full_feature_blip_showcase.md          # 16:9 Full feature blip showcase
│   └── full_feature_blip_showcase_vertical.md # 9:16 Shorts full feature blip showcase
├── src/ut_novel/
│   ├── audio/               # Blip generator, TTS providers, BGM mixer
│   ├── encoder/             # FFmpeg raw pipe encoder
│   ├── parser/              # Frontmatter, RichText, WordWrapping
│   ├── visual/              # Dialog box renderer, BG video looper
│   ├── engine.py            # Unified NovelEngine pipeline
│   ├── models.py            # Configurations & Aspect Ratio presets
│   └── cli.py               # CLI command interface
└── memo/PLAN/               # Complete project plan & milestones
```

---

## 📜 License
MIT License
