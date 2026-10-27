"""Base class for R4 (Ridge Racer Type 4) 4-Layer Dialogue Templates."""
import os
import random
from typing import Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from ut_novel.templates.base import BaseTemplate
from ut_novel.parser.rich_text import RichChar
from ut_novel.parser.word_wrap import WordWrapper

class R4BaseTemplate(BaseTemplate):
    """
    R4 (Ridge Racer Type 4) 4-Layer Architecture Template.
    - Layer 1: Outer background color frame (R4 Yellow mat)
    - Layer 2: Inner background image viewport with white border line
    - Layer 3: Center portrait box (thick black border with solid yellow backdrop)
    - Layer 4: Foreground dialogue box with characteristic '*Message' index tab
    """

    # Layer 1 & 2 Config
    outer_bg_color: Tuple[int, int, int] = (255, 255, 255)       # Solid White outer mat frame
    inner_border_color: Tuple[int, int, int] = (0, 0, 0)         # Crisp black border line
    inner_border_width: int = 3
    margin_x: int
    margin_y: int

    # Layer 3 Config (Portrait)
    portrait_width: int
    portrait_height: int
    portrait_top: int
    portrait_border_width: int = 6
    portrait_border_color: Tuple[int, int, int] = (0, 0, 0)    # Thick black border
    portrait_bg_color: Tuple[int, int, int] = (255, 255, 255)  # Solid White portrait backdrop

    # Layer 4 Config (Message Box)
    box_height: int
    box_bottom_margin: int
    box_bg_color: Tuple[int, int, int] = (55, 55, 58)          # Dark charcoal gray
    box_border_color: Tuple[int, int, int] = (255, 255, 255)   # White outline
    box_border_width: int = 3
    tab_width: int = 240
    tab_height: int = 44
    tab_offset_x: int = 20
    tab_title: str = "*Message"
    tab_corner_radius: int = 8

    # Typography
    text_color: Tuple[int, int, int] = (255, 255, 255)
    font_size: int = 42
    tab_font_size: int = 28
    line_spacing: int = 22
    text_margin_x: int = 50
    text_margin_y: int = 45

    # Audio & Typography Defaults
    default_blip_sound: str = "assets/se/r4_click.wav"
    prefix: str = ""

    @property
    def font_path(self) -> str:
        if os.path.exists("assets/fonts/R4Font-Bold.ttc"):
            return "assets/fonts/R4Font-Bold.ttc"
        if os.path.exists("assets/fonts/ModernSans-Bold.ttf"):
            return "assets/fonts/ModernSans-Bold.ttf"
        return "assets/fonts/PixelOperator.ttf"

    @property
    def tab_font_path(self) -> str:
        if os.path.exists("assets/fonts/ModernSans-Bold.ttf"):
            return "assets/fonts/ModernSans-Bold.ttf"
        return self.font_path

    @property
    def inner_viewport(self) -> Tuple[int, int, int, int]:
        """Returns (x0, y0, x1, y1) for Layer 2 inner viewport."""
        return (
            self.margin_x,
            self.margin_y,
            self.screen_width - self.margin_x,
            self.screen_height - self.margin_y
        )

    @property
    def box_bounds(self) -> Tuple[int, int, int, int]:
        """Returns (bx0, by0, bx1, by1) for Layer 4 dialogue box."""
        vx0, vy0, vx1, vy1 = self.inner_viewport
        bx0 = vx0 + 20
        bx1 = vx1 - 20
        by1 = vy1 - self.box_bottom_margin
        by0 = by1 - self.box_height
        return (bx0, by0, bx1, by1)

    def get_tab_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        if os.path.exists(self.tab_font_path):
            return ImageFont.truetype(self.tab_font_path, self.tab_font_size)
        return ImageFont.load_default()

    def wrap_text(self, rich_chars: List[RichChar], has_portrait: bool = False) -> List[RichChar]:
        font = self.get_font()
        bx0, by0, bx1, by1 = self.box_bounds
        max_w = (bx1 - bx0) - self.text_margin_x * 2
        wrapper = WordWrapper(font, max_width=max_w, asterisk_indent=0)
        return wrapper.wrap_rich_chars(rich_chars, prefix_asterisk=False)

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
        # ========================================================
        # Layer 1: Outer Background Color Mat
        # ========================================================
        canvas = Image.new("RGB", (self.screen_width, self.screen_height), self.outer_bg_color)
        draw = ImageDraw.Draw(canvas)

        # ========================================================
        # Layer 2: Inner Background Viewport
        # ========================================================
        vx0, vy0, vx1, vy1 = self.inner_viewport
        vw = vx1 - vx0
        vh = vy1 - vy0

        if base_image is not None:
            # Scale & crop background image to fit the inner viewport exactly
            bg_scaled = base_image.resize((self.screen_width, self.screen_height), Image.Resampling.BICUBIC)
            bg_crop = bg_scaled.crop((vx0, vy0, vx1, vy1))
            canvas.paste(bg_crop, (vx0, vy0))
        else:
            # Fallback inner scenery
            draw.rectangle([vx0, vy0, vx1, vy1], fill=(20, 25, 35))

        # White border around inner viewport
        draw.rectangle([vx0, vy0, vx1, vy1], outline=self.inner_border_color, width=self.inner_border_width)

        # ========================================================
        # Layer 3: Central Portrait Box
        # ========================================================
        if portrait_image is not None:
            pw, ph = self.portrait_width, self.portrait_height
            px0 = (self.screen_width - pw) // 2
            py0 = self.portrait_top
            px1 = px0 + pw
            py1 = py0 + ph
            bw = self.portrait_border_width

            # Solid yellow backdrop for portrait
            draw.rectangle([px0, py0, px1, py1], fill=self.portrait_bg_color)

            # Resize character portrait to fill inside the thick black border
            p_inner_w = pw - bw * 2
            p_inner_h = ph - bw * 2

            y_offset = 0
            if is_speaking:
                cycle = (speaking_tick // 4) % 2
                if cycle == 1:
                    y_offset = -2

            resized_p = portrait_image.resize((p_inner_w, p_inner_h), Image.Resampling.BILINEAR)
            paste_pos = (px0 + bw, py0 + bw + y_offset)
            if resized_p.mode == "RGBA":
                canvas.paste(resized_p, paste_pos, resized_p)
            else:
                canvas.paste(resized_p, paste_pos)

            # Solid black border around portrait
            draw.rectangle([px0, py0, px1, py1], outline=self.portrait_border_color, width=bw)

        if not show_textbox:
            return canvas

        # ========================================================
        # Layer 4: Foreground Dialogue Box with *Message Tab
        # ========================================================
        bx0, by0, bx1, by1 = self.box_bounds
        line_w = self.box_border_width
        b_col = self.box_border_color
        bg_col = self.box_bg_color

        tx0 = bx0 + self.tab_offset_x
        tx1 = tx0 + self.tab_width
        ty0 = by0 - self.tab_height
        rad = self.tab_corner_radius

        # 1. Fill main box & tab with dark charcoal gray
        draw.rectangle([bx0, by0, bx1, by1], fill=bg_col)
        draw.rounded_rectangle([tx0, ty0, tx1, by0 + rad], radius=rad, fill=bg_col)

        # 2. Draw crisp white outlines
        # Bottom, left, and right lines of main box
        draw.line([(bx0, by1), (bx1, by1)], fill=b_col, width=line_w)
        draw.line([(bx0, by0), (bx0, by1)], fill=b_col, width=line_w)
        draw.line([(bx1, by0), (bx1, by1)], fill=b_col, width=line_w)

        # Top line segments of main box (excluding tab width)
        draw.line([(bx0, by0), (tx0, by0)], fill=b_col, width=line_w)
        draw.line([(tx1, by0), (bx1, by0)], fill=b_col, width=line_w)

        # Tab top outline with rounded corners
        draw.line([(tx0, ty0 + rad), (tx0, by0)], fill=b_col, width=line_w)
        draw.line([(tx0 + rad, ty0), (tx1 - rad, ty0)], fill=b_col, width=line_w)
        draw.line([(tx1, ty0 + rad), (tx1, by0)], fill=b_col, width=line_w)
        draw.arc([tx0, ty0, tx0 + rad * 2, ty0 + rad * 2], start=180, end=270, fill=b_col, width=line_w)
        draw.arc([tx1 - rad * 2, ty0, tx1, ty0 + rad * 2], start=270, end=360, fill=b_col, width=line_w)

        # 3. Draw Tab Header Text (*Message)
        tab_font = self.get_tab_font()
        draw.text((tx0 + 16, ty0 + 8), self.tab_title, font=tab_font, fill=self.text_color)

        # 4. Draw Dialogue Text Characters
        font = self.get_font()
        text_x = bx0 + self.text_margin_x
        text_y = by0 + self.text_margin_y

        if visible_rich_chars:
            line_idx = 0
            current_x = text_x
            line_h = self.font_size + self.line_spacing

            rng = random.Random(frame_index * 1000)

            for rc in visible_rich_chars:
                if rc.char == "\n":
                    line_idx += 1
                    current_x = text_x
                    continue

                ch_w = draw.textlength(rc.char, font=font)

                dx = 0
                dy = 0
                if rc.shake:
                    dx = rng.randint(-2, 2)
                    dy = rng.randint(-2, 2)

                draw_pos = (current_x + dx, text_y + line_idx * line_h + dy)
                draw.text(draw_pos, rc.char, font=font, fill=rc.color)
                current_x += int(ch_w)

        return canvas
