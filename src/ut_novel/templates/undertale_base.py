"""Base class for Undertale-style pixel dialogue templates."""
import random
import os
from typing import Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from ut_novel.templates.base import BaseTemplate
from ut_novel.parser.rich_text import RichChar
from ut_novel.parser.word_wrap import WordWrapper

class UndertaleBaseTemplate(BaseTemplate):
    """Abstract base for Undertale-style pixel dialogue boxes."""

    # Configurable in subclasses
    box_width: int
    box_height: int
    box_bottom_margin: int
    border_width: int = 6
    border_color: Tuple[int, int, int] = (255, 255, 255)
    bg_color: Tuple[int, int, int] = (0, 0, 0)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    text_margin_x: int
    text_margin_y: int
    line_spacing: int
    portrait_size: int
    portrait_margin_x: int

    default_blip_sound: str = "assets/se/voice_default.wav"
    prefix: str = "* "

    @property
    def font_path(self) -> str:
        return "assets/fonts/PixelOperator.ttf"

    @property
    def box_left(self) -> int:
        return (self.screen_width - self.box_width) // 2

    @property
    def box_top(self) -> int:
        return self.screen_height - self.box_height - self.box_bottom_margin

    def wrap_text(self, rich_chars: List[RichChar], has_portrait: bool = False) -> List[RichChar]:
        """Wrap rich characters to fit within this template's text area."""
        font = self.get_font()
        max_w = self.box_width - self.text_margin_x * 2
        if has_portrait:
            max_w -= (self.portrait_size + 40)

        asterisk_w = int(font.getlength(self.prefix)) if self.prefix else 0
        wrapper = WordWrapper(font, max_width=max_w, asterisk_indent=asterisk_w)
        return wrapper.wrap_rich_chars(rich_chars, prefix_asterisk=bool(self.prefix))

    def draw_pixel_box(self, draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, border_width: int):
        """Draw an Undertale-style pixel border rectangle."""
        draw.rectangle([x0, y0, x1, y1], fill=self.bg_color)
        bw = border_width

        # Horizontal lines
        draw.rectangle([x0 + bw, y0, x1 - bw, y0 + bw - 1], fill=self.border_color)
        draw.rectangle([x0 + bw, y1 - bw + 1, x1 - bw, y1], fill=self.border_color)

        # Vertical lines
        draw.rectangle([x0, y0 + bw, x0 + bw - 1, y1 - bw], fill=self.border_color)
        draw.rectangle([x1 - bw + 1, y0 + bw, x1, y1 - bw], fill=self.border_color)

    def render_frame(
        self,
        base_image: Optional[Image.Image] = None,
        visible_rich_chars: Optional[List[RichChar]] = None,
        speaker_name: Optional[str] = None,
        portrait_image: Optional[Image.Image] = None,
        is_speaking: bool = False,
        speaking_tick: int = 0,
        frame_index: int = 0,
        show_textbox: bool = True
    ) -> Image.Image:
        """Render a single frame with pixel box, portrait bobbing, and text effects."""
        if base_image is None:
            image = Image.new("RGBA", (self.screen_width, self.screen_height), (0, 0, 0, 255))
        else:
            image = base_image.copy()

        if not show_textbox:
            return image

        draw = ImageDraw.Draw(image)
        font = self.get_font()

        bx0 = self.box_left
        by0 = self.box_top
        bx1 = bx0 + self.box_width
        by1 = by0 + self.box_height

        # Draw box
        self.draw_pixel_box(draw, bx0, by0, bx1, by1, self.border_width)

        # Draw portrait if present
        text_start_x = bx0 + self.text_margin_x
        if portrait_image is not None:
            p_size = self.portrait_size
            p_x = bx0 + self.portrait_margin_x
            base_p_y = by0 + (self.box_height - p_size) // 2

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
        text_y = by0 + self.text_margin_y
        prefix_str = self.prefix
        prefix_w = int(draw.textlength(prefix_str, font=font)) if prefix_str else 0

        if visible_rich_chars:
            line_idx = 0
            current_x = text_start_x + prefix_w
            line_h = self.font_size + self.line_spacing

            # Draw the leading asterisk on the first line
            if prefix_str:
                draw.text((text_start_x, text_y), prefix_str, font=font, fill=self.text_color)

            # Seeded RNG for consistent frame shaking
            rng = random.Random(frame_index * 1000)

            for rc in visible_rich_chars:
                if rc.char == "\n":
                    line_idx += 1
                    current_x = text_start_x + prefix_w
                    continue

                ch_w = draw.textlength(rc.char, font=font)

                # Apply shake offset if enabled
                dx = 0
                dy = 0
                if rc.shake:
                    dx = rng.randint(-2, 2)
                    dy = rng.randint(-2, 2)

                draw_pos = (current_x + dx, text_y + line_idx * line_h + dy)
                draw.text(draw_pos, rc.char, font=font, fill=rc.color)
                current_x += int(ch_w)

        return image

