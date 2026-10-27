"""Abstract Base Class for Video Dialogue Templates."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union
from PIL import Image, ImageFont
import os
from ut_novel.parser.rich_text import RichChar
from ut_novel.parser.word_wrap import WordWrapper

class BaseTemplate(ABC):
    """
    A self-contained template defining screen dimensions, UI geometry, typography,
    sound effects, and frame rendering logic.
    """

    # Template metadata & canvas resolution
    name: str
    screen_width: int
    screen_height: int
    font_size: int
    default_blip_sound: str = "assets/se/voice_default.wav"
    prefix: str = ""

    @property
    def font_path(self) -> str:
        """Path to default typography font file."""
        return "assets/fonts/PixelOperator.ttf"

    def get_font(self) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
        """Loads and returns the template font."""
        if os.path.exists(self.font_path):
            return ImageFont.truetype(self.font_path, self.font_size)
        return ImageFont.load_default()

    @abstractmethod
    def wrap_text(self, rich_chars: List[RichChar], has_portrait: bool = False) -> List[RichChar]:
        """Wrap rich characters to fit within this template's text area."""
        pass

    @abstractmethod
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
        """
        Renders a single video frame with text, character portrait, and decorations.
        """
        pass
