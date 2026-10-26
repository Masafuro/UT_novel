---
title: "Rich Effects & Video Background"
aspect_ratio: "16:9"
fps: 30
bg: "assets/bg/sample_for_bg_movie.mp4"

characters:
  toriel:
    name: "Toriel"
    voice_mode: "blip"
    voice: "assets/se/voice_high.wav"
    default_face: "smile"
    faces:
      smile: "assets/char/toriel/smile.jpg"
  sans:
    name: "sans"
    voice_mode: "blip"
    voice: "assets/se/voice_low.wav"
    default_face: "grin"
    faces:
      grin: "assets/char/sans/grin.jpg"
---

# Rich effects demonstration: shake, color, and inline wait

* toriel(smile): Stay calm, my child.[wait: 0.8] You are filled with [color: yellow]DETERMINATION[/color].
* sans(grin): hey. heard you've been working down to the [shake]bone[/shake].
* toriel(smile): Sans! That joke was an absolute [color: red]DISASTER[/color]!
