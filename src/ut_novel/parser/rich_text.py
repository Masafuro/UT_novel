"""Rich text parser supporting inline tags: [wait], [color], [shake], [se]."""
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

COLOR_MAP = {
    "yellow": (255, 255, 0),
    "red": (255, 50, 50),
    "blue": (0, 162, 232),
    "green": (50, 255, 50),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "white": (255, 255, 255),
}

def parse_color(color_str: str) -> Tuple[int, int, int]:
    color_str = color_str.strip().lower()
    if color_str in COLOR_MAP:
        return COLOR_MAP[color_str]
    if color_str.startswith("#"):
        hex_val = color_str.lstrip("#")
        if len(hex_val) == 6:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            return (r, g, b)
    return (255, 255, 255)

@dataclass
class RichChar:
    char: str
    color: Tuple[int, int, int] = (255, 255, 255)
    shake: bool = False
    wait_before: float = 0.0
    se_trigger: Optional[str] = None

class RichTextParser:
    TAG_REGEX = re.compile(
        r"\[(wait:\s*[\d\.]+|color:\s*[^\]]+|/color|shake|/shake|se:\s*[^\]]+)\]",
        re.IGNORECASE
    )

    @classmethod
    def strip_tags(cls, text: str) -> str:
        """Strip all inline tags, returning plain text."""
        return cls.TAG_REGEX.sub("", text)

    @classmethod
    def parse(cls, text: str) -> List[RichChar]:
        """Parse text with inline tags into a list of RichChar objects."""
        tokens = cls.TAG_REGEX.split(text)
        result: List[RichChar] = []

        current_color = (255, 255, 255)
        current_shake = False
        pending_wait = 0.0
        pending_se = None

        for token in tokens:
            if not token:
                continue

            lower_token = token.lower().strip()
            
            # Check tags
            if lower_token.startswith("wait:"):
                try:
                    val = float(lower_token.split(":", 1)[1].strip())
                    pending_wait += val
                except ValueError:
                    pass
            elif lower_token.startswith("color:"):
                c_val = token.split(":", 1)[1].strip()
                current_color = parse_color(c_val)
            elif lower_token == "/color":
                current_color = (255, 255, 255)
            elif lower_token == "shake":
                current_shake = True
            elif lower_token == "/shake":
                current_shake = False
            elif lower_token.startswith("se:"):
                pending_se = token.split(":", 1)[1].strip()
            else:
                # Normal text content
                for ch in token:
                    result.append(RichChar(
                        char=ch,
                        color=current_color,
                        shake=current_shake,
                        wait_before=pending_wait,
                        se_trigger=pending_se
                    ))
                    # Reset pending one-shot triggers after attaching to first char
                    pending_wait = 0.0
                    pending_se = None

        return result
