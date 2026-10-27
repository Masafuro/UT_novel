from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple

@dataclass
class SplashConfig:
    """Configuration for a splash screen (intro/outro)."""
    image: str
    duration: float = 3.0
    fade_in: float = 0.5
    fade_out: float = 0.5
    transition: str = "fade_black"  # "fade_black" or "cut"

@dataclass
class DialogBoxConfig:
    """Configuration for the dialog box layout and style."""
    screen_width: int = 1920
    screen_height: int = 1080
    box_width: int = 1560
    box_height: int = 340
    box_bottom_margin: int = 60
    border_width: int = 6
    border_color: Tuple[int, int, int] = (255, 255, 255)
    bg_color: Tuple[int, int, int] = (0, 0, 0)
    font_path: str = "assets/fonts/PixelOperator.ttf"
    font_size: int = 56
    text_color: Tuple[int, int, int] = (255, 255, 255)
    text_margin_x: int = 60
    text_margin_y: int = 50
    line_spacing: int = 16
    portrait_size: int = 220
    portrait_margin_x: int = 50

    @property
    def box_left(self) -> int:
        return (self.screen_width - self.box_width) // 2

    @property
    def box_top(self) -> int:
        return self.screen_height - self.box_height - self.box_bottom_margin

    @classmethod
    def get_preset(cls, aspect_ratio: str = "16:9") -> "DialogBoxConfig":
        """Get standard preset configuration for 16:9 (Landscape) or 9:16 (Shorts/Vertical)."""
        aspect_ratio = aspect_ratio.strip().replace(" ", "")
        if aspect_ratio == "9:16":
            # Optimized for YouTube Shorts / TikTok / Reels (1080x1920)
            return cls(
                screen_width=1080,
                screen_height=1920,
                box_width=980,
                box_height=460,
                box_bottom_margin=280,  # Avoid bottom action bar/captions on phones
                border_width=6,
                font_size=46,
                text_margin_x=45,
                text_margin_y=45,
                line_spacing=14,
                portrait_size=170,
                portrait_margin_x=40
            )
        else:
            # Standard 16:9 (1920x1080)
            return cls(
                screen_width=1920,
                screen_height=1080,
                box_width=1560,
                box_height=340,
                box_bottom_margin=60,
                border_width=6,
                font_size=56,
                text_margin_x=60,
                text_margin_y=50,
                line_spacing=16,
                portrait_size=220,
                portrait_margin_x=50
            )

@dataclass
class CharacterConfig:
    name: str
    voice_mode: str = "blip"  # "blip" or "tts"
    blip_sound: str = "assets/se/voice_default.wav"
    tts_provider: str = "gtts"  # "gtts" or "custom"
    tts_voice_id: Optional[str] = None
    tts_speed: float = 1.0
    font_path: Optional[str] = None
    default_face: Optional[str] = None
    faces: Dict[str, str] = field(default_factory=dict)
