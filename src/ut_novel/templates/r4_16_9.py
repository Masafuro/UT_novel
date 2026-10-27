"""R4 (Ridge Racer Type 4) 16:9 Cinematic Briefing Template (1920x1080)."""
from ut_novel.templates.r4_base import R4BaseTemplate
from ut_novel.templates.registry import TemplateRegistry

@TemplateRegistry.register
class R4_16x9_Template(R4BaseTemplate):
    """
    R4 (Ridge Racer Type 4) authentic 16:9 Meeting Screen Template.
    Accurately reproduces the 4-layer architecture:
    - Layer 1: R4 yellow outer frame
    - Layer 2: Inner scenery viewport with white boundary
    - Layer 3: Central thick-bordered character portrait on yellow backdrop
    - Layer 4: Dark charcoal dialogue box with '*Message' tab header
    """

    name: str = "r4_16_9"
    screen_width: int = 1920
    screen_height: int = 1080

    # Layer 1 & 2: Outer Frame & Inner Viewport
    margin_x: int = 55
    margin_y: int = 35
    inner_border_width: int = 3

    # Layer 3: Central Portrait Box
    portrait_width: int = 380
    portrait_height: int = 420
    portrait_top: int = 110
    portrait_border_width: int = 6

    # Layer 4: Dialogue Box with *Message tab
    box_height: int = 290
    box_bottom_margin: int = 25
    tab_width: int = 240
    tab_height: int = 44
    tab_offset_x: int = 25
    tab_corner_radius: int = 8

    # Typography
    font_size: int = 42
    tab_font_size: int = 28
    line_spacing: int = 22
    text_margin_x: int = 50
    text_margin_y: int = 45
