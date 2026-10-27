---
title: "The Ancient Ruins Expedition"
aspect_ratio: "16:9"
fps: 30
bg: "assets/bg/ruins_hall.jpg"
bgm: "assets/bgm/ruins_theme.wav"
bgm_volume: 0.4

# 1. Opening Splash Screen (Mount Ebott Title)
splash_start:
  image: "assets/bg/title_mount_ebott.jpg"
  duration: 3.0
  fade_in: 0.6
  fade_out: 0.6
  transition: "fade_black"

# 2. Ending Splash Screen (Golden Flowers Epilogue)
splash_end:
  image: "assets/bg/title_golden_flowers.jpg"
  duration: 3.0
  fade_in: 0.6
  fade_out: 0.8
  transition: "fade_black"

characters:
  narrator:
    name: ""
    voice_mode: "blip"
    voice: "assets/se/voice_default.wav"

  dev_girl_1:
    name: "Emma"
    voice_mode: "blip"
    voice: "assets/se/voice_high.wav"
    default_face: "smile"
    faces:
      smile: "assets/char/dev_girl_1/smile.jpg"

  dev_boy_1:
    name: "Alex"
    voice_mode: "blip"
    voice: "assets/se/voice_low.wav"
    default_face: "smile"
    faces:
      smile: "assets/char/dev_boy_1/smile.jpg"
---

# Expedition Sequence

* narrator: Deep inside the forgotten cavern, two explorers reached an ancient gateway...
* dev_girl_1(smile): Look around, Alex![wait: 0.5] These stone corridors have been preserved for centuries.
* dev_boy_1(smile): hey. watch your step. the ancient ground feels a bit [shake]shaky[/shake] under our feet.
* dev_girl_1(smile): You are right. Keep your [color: #00ccff]courage[/color] high and stay alert!
* narrator: A warm golden light glimmers further down the hall.[wait: 0.6] [se: save]The discovery fills you with [color: #ffff00][shake]DETERMINATION[/shake][/color].
