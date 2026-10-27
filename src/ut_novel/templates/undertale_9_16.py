"""Undertale 9:16 Vertical Shorts/TikTok Template (1080x1920)."""
from ut_novel.templates.undertale_base import UndertaleBaseTemplate
from ut_novel.templates.registry import TemplateRegistry

@TemplateRegistry.register
class Undertale9x16Template(UndertaleBaseTemplate):
    """Undertale 9:16 Vertical Shorts Layout (1080x1920) avoiding bottom UI."""

    name: str = "undertale_9_16"
    screen_width: int = 1080
    screen_height: int = 1920
    box_width: int = 980
    box_height: int = 460
    box_bottom_margin: int = 280  # Keeps box clear of phone bottom UI/captions
    font_size: int = 46
    line_spacing: int = 14
    text_margin_x: int = 45
    text_margin_y: int = 45
    portrait_size: int = 170
    portrait_margin_x: int = 40

