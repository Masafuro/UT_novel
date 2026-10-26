"""Milestone 1 Preview Script: Render a static Undertale dialogue frame."""
import os
import sys

# Ensure src is in sys.path
sys.path.insert(0, os.path.abspath("src"))

from ut_novel.models import DialogBoxConfig
from ut_novel.visual.textbox import DialogBoxRenderer
from PIL import Image, ImageDraw

def main():
    print("Initializing DialogBoxRenderer...")
    config = DialogBoxConfig()
    renderer = DialogBoxRenderer(config)
    
    # Create a dummy portrait for testing (e.g. 8-bit smiley)
    p_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(p_img)
    # Simple retro white face
    p_draw.rectangle([10, 10, 90, 90], outline=(255, 255, 255), width=4)
    p_draw.rectangle([30, 30, 40, 40], fill=(255, 255, 255))
    p_draw.rectangle([60, 30, 70, 40], fill=(255, 255, 255))
    p_draw.line([(30, 70), (70, 70)], fill=(255, 255, 255), width=4)

    # 1. Render frame without portrait
    text_sample = "Hello, human.\nWelcome to the underground."
    img_no_portrait = renderer.render_frame(text=text_sample)
    os.makedirs("output", exist_ok=True)
    img_no_portrait.save("output/m1_test_no_portrait.png")
    print("Saved output/m1_test_no_portrait.png")

    # 2. Render frame with portrait
    img_portrait = renderer.render_frame(text=text_sample, portrait_image=p_img)
    img_portrait.save("output/m1_test_portrait.png")
    print("Saved output/m1_test_portrait.png")
    print("Milestone 1 verification successful!")

if __name__ == "__main__":
    main()
