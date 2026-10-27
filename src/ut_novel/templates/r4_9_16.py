"""R4 (Ridge Racer Type 4) 9:16 Vertical Shorts Briefing Template (1080x1920)."""
from ut_novel.templates.r4_base import R4BaseTemplate
from ut_novel.templates.registry import TemplateRegistry

@TemplateRegistry.register
class R4_9x16_Template(R4BaseTemplate):
    """
    R4 (Ridge Racer Type 4) authentic 9:16 Vertical Shorts Meeting Screen Template.
    Optimized for mobile viewports while preserving the 4-layer aesthetic:
    - Layer 1: R4 yellow outer frame
    - Layer 2: Inner scenery viewport with white boundary
    - Layer 3: Central thick-bordered character portrait on yellow backdrop
    - Layer 4: Dark charcoal dialogue box with '*Message' tab header above mobile safe area
    """

    name: str = "r4_9_16"
    screen_width: int = 1080
    screen_height: int = 1920

    # Layer 1 & 2: Outer Frame & Inner Viewport
    margin_x: int = 35
    margin_y: int = 50
    inner_border_width: int = 3

    # Layer 3: Central Portrait Box
    portrait_width: int = 380
    portrait_height: int = 420
    portrait_top: int = 440
    portrait_border_width: int = 6

    # Layer 4: Dialogue Box with *Message tab
    box_height: int = 460
    box_bottom_margin: int = 320  # Keeps box clear of phone captions & controls
    tab_width: int = 240
    tab_height: int = 44
    tab_offset_x: int = 25
    tab_corner_radius: int = 8

    # Typography
    font_size: int = 38
    tab_font_size: int = 26
    line_spacing: int = 20
    text_margin_x: int = 45
    text_margin_y: int = 45
