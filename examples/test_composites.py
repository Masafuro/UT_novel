"""Test script to render dialogues overlaid on generated sample backgrounds."""
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

    # 1. Dev Girl in Ruins
    ruins_bg = Image.open("assets/bg/ruins_hall.jpg").convert("RGBA").resize((1920, 1080))
    girl_face = Image.open("assets/char/dev_girl_1/smile.jpg").convert("RGBA")
    
    text_girl = "Hello, explorer!\nWelcome to the ancient ruins."
    img1 = renderer.render_frame(
        base_image=ruins_bg,
        text=text_girl,
        portrait_image=girl_face
    )
    img1.save("output/composite_ruins_girl.png")
    print("Saved output/composite_ruins_girl.png")

    # 2. Dev Boy in Snowy Forest
    snow_bg = Image.open("assets/bg/snowy_forest.jpg").convert("RGBA").resize((1920, 1080))
    boy_face = Image.open("assets/char/dev_boy_1/smile.jpg").convert("RGBA")
    
    text_boy = "hey.\nyou look like you've been working\nhard on your code."
    img2 = renderer.render_frame(
        base_image=snow_bg,
        text=text_boy,
        portrait_image=boy_face
    )
    img2.save("output/composite_snow_boy.png")
    print("Saved output/composite_snow_boy.png")

if __name__ == "__main__":
    main()
