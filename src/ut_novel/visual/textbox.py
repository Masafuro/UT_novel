"""Undertale-style dialog box renderer with RichChar support (colors and shaking)."""
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, List
import random
import os
from ut_novel.models import DialogBoxConfig
from ut_novel.parser.rich_text import RichChar

class DialogBoxRenderer:
    def __init__(self, config: Optional[DialogBoxConfig] = None):
        self.config = config or DialogBoxConfig()
        self._load_font()

    def _load_font(self):
        font_path = self.config.font_path
        if os.path.exists(font_path):
            self.font = ImageFont.truetype(font_path, self.config.font_size)
        else:
            self.font = ImageFont.load_default()

    def draw_pixel_box(self, draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, border_width: int):
        """Draw an Undertale-style pixel border rectangle."""
        draw.rectangle([x0, y0, x1, y1], fill=self.config.bg_color)
        bw = border_width
        
        # Horizontal lines
        draw.rectangle([x0 + bw, y0, x1 - bw, y0 + bw - 1], fill=self.config.border_color)
        draw.rectangle([x0 + bw, y1 - bw + 1, x1 - bw, y1], fill=self.config.border_color)
        
        # Vertical lines
        draw.rectangle([x0, y0 + bw, x0 + bw - 1, y1 - bw], fill=self.config.border_color)
        draw.rectangle([x1 - bw + 1, y0 + bw, x1, y1 - bw], fill=self.config.border_color)

    def render_rich_frame(
        self,
        base_image: Optional[Image.Image] = None,
        visible_rich_chars: Optional[List[RichChar]] = None,
        portrait_image: Optional[Image.Image] = None,
        is_speaking: bool = False,
        speaking_tick: int = 0,
        frame_index: int = 0,
        prefix_asterisk: bool = True
    ) -> Image.Image:
        """Render a frame with rich characters (color, shake) and animated portrait."""
        cfg = self.config
        
        if base_image is None:
            image = Image.new("RGBA", (cfg.screen_width, cfg.screen_height), (0, 0, 0, 255))
        else:
            image = base_image.copy()

        draw = ImageDraw.Draw(image)
        
        bx0 = cfg.box_left
        by0 = cfg.box_top
        bx1 = bx0 + cfg.box_width
        by1 = by0 + cfg.box_height

        # Draw box
        self.draw_pixel_box(draw, bx0, by0, bx1, by1, cfg.border_width)

        # Draw portrait if present
        text_start_x = bx0 + cfg.text_margin_x
        if portrait_image is not None:
            p_size = cfg.portrait_size
            p_x = bx0 + cfg.portrait_margin_x
            base_p_y = by0 + (cfg.box_height - p_size) // 2

            y_offset = 0
            if is_speaking:
                # 4-frame cycle: bob up on cycle 1
                cycle = (speaking_tick // 3) % 2
                if cycle == 1:
                    y_offset = -3

            resized_p = portrait_image.resize((p_size, p_size), Image.Resampling.NEAREST)
            p_y = base_p_y + y_offset
            image.paste(resized_p, (p_x, p_y), resized_p if resized_p.mode == "RGBA" else None)
            text_start_x = p_x + p_size + 40

        # Draw text characters
        text_y = by0 + cfg.text_margin_y
        asterisk_w = int(draw.textlength("* ", font=self.font)) if prefix_asterisk else 0

        # If we have characters to display
        if visible_rich_chars:
            line_idx = 0
            current_x = text_start_x + (asterisk_w if prefix_asterisk else 0)
            line_h = cfg.font_size + cfg.line_spacing

            # Draw the leading asterisk on the first line
            if prefix_asterisk:
                draw.text((text_start_x, text_y), "* ", font=self.font, fill=cfg.text_color)

            # Seeded RNG for consistent frame shaking
            rng = random.Random(frame_index * 1000)

            for char_idx, rc in enumerate(visible_rich_chars):
                if rc.char == "\n":
                    line_idx += 1
                    current_x = text_start_x + (asterisk_w if prefix_asterisk else 0)
                    continue

                ch_w = draw.textlength(rc.char, font=self.font)
                
                # Apply shake offset if enabled
                dx = 0
                dy = 0
                if rc.shake:
                    dx = rng.randint(-2, 2)
                    dy = rng.randint(-2, 2)

                draw_pos = (current_x + dx, text_y + line_idx * line_h + dy)
                draw.text(draw_pos, rc.char, font=self.font, fill=rc.color)
                current_x += int(ch_w)

        return image
