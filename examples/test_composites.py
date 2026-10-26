"""Test script to render Undertale dialogues overlaid on generated sample backgrounds."""
import os
import sys

sys.path.insert(0, os.path.abspath("src"))

from ut_novel.models import DialogBoxConfig
from ut_novel.visual.textbox import DialogBoxRenderer
from PIL import Image

def main():
    config = DialogBoxConfig(screen_width=1920, screen_height=1080)
    renderer = DialogBoxRenderer(config)
    os.makedirs("output", exist_ok=True)

    # 1. Toriel in Ruins
    ruins_bg = Image.open("assets/bg/ruins_hall.jpg").convert("RGBA").resize((1920, 1080))
    toriel_face = Image.open("assets/char/toriel/smile.jpg").convert("RGBA")
    
    text_toriel = "Hello, my child.\nWelcome to the RUINS."
    img1 = renderer.render_frame(
        base_image=ruins_bg,
        text=text_toriel,
        portrait_image=toriel_face
    )
    img1.save("output/composite_ruins_toriel.png")
    print("Saved output/composite_ruins_toriel.png")

    # 2. Sans in Snowy Forest
    snow_bg = Image.open("assets/bg/snowy_forest.jpg").convert("RGBA").resize((1920, 1080))
    sans_face = Image.open("assets/char/sans/grin.jpg").convert("RGBA")
    
    text_sans = "hey.\nyou look like you've been working\ndown to the bone."
    img2 = renderer.render_frame(
        base_image=snow_bg,
        text=text_sans,
        portrait_image=sans_face
    )
    img2.save("output/composite_snow_sans.png")
    print("Saved output/composite_snow_sans.png")

if __name__ == "__main__":
    main()
