"""Undertale 16:9 Landscape Template (1920x1080)."""
from ut_novel.templates.undertale_base import UndertaleBaseTemplate
from ut_novel.templates.registry import TemplateRegistry

@TemplateRegistry.register
class Undertale16x9Template(UndertaleBaseTemplate):
    """Classic Undertale 16:9 Landscape Layout (1920x1080)."""

    name: str = "undertale_16_9"
    screen_width: int = 1920
    screen_height: int = 1080
    box_width: int = 1560
    box_height: int = 340
    box_bottom_margin: int = 60
    font_size: int = 56
    line_spacing: int = 16
    text_margin_x: int = 60
    text_margin_y: int = 50
    portrait_size: int = 220
    portrait_margin_x: int = 50

