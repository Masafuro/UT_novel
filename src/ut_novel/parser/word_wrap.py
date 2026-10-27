"""Word wrapping utilities supporting inline rich text tags."""
from PIL import ImageFont, ImageDraw, Image
from typing import List, Union
from ut_novel.parser.rich_text import RichTextParser, RichChar

class WordWrapper:
    def __init__(self, font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont], max_width: int, asterisk_indent: int = 0):
        self.font = font
        self.max_width = max_width
        self.asterisk_indent = asterisk_indent
        self._dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    def wrap_rich_chars(self, rich_chars: List[RichChar], prefix_asterisk: bool = True) -> List[RichChar]:
        """
        Wrap a list of RichChar objects by words to fit within max_width pixels.
        Inserts RichChar('\n') at line wrap boundaries.
        """
        asterisk_prefix = "* " if prefix_asterisk else ""
        asterisk_w = int(self._dummy_draw.textlength(asterisk_prefix, font=self.font)) if prefix_asterisk else 0

        # Group rich_chars into words (split by space or explicit newline)
        words: List[List[RichChar]] = []
        current_word: List[RichChar] = []

        for rc in rich_chars:
            if rc.char == "\n":
                if current_word:
                    words.append(current_word)
                    current_word = []
                words.append([rc])  # Explicit newline token
            elif rc.char == " ":
                current_word.append(rc)
                words.append(current_word)
                current_word = []
            else:
                current_word.append(rc)

        if current_word:
            words.append(current_word)

        # Now lay out words onto lines
        result: List[RichChar] = []
        current_line_text = ""
        is_first_line = True

        for word_chars in words:
            # If explicit newline
            if len(word_chars) == 1 and word_chars[0].char == "\n":
                result.append(word_chars[0])
                current_line_text = ""
                is_first_line = False
                continue

            word_text = "".join(rc.char for rc in word_chars)
            test_line = current_line_text + word_text
            
            avail_w = self.max_width - (asterisk_w if is_first_line else self.asterisk_indent)
            test_w = self._dummy_draw.textlength(test_line, font=self.font)

            if test_w <= avail_w or not current_line_text:
                current_line_text += word_text
                result.extend(word_chars)
            else:
                # Wrap to next line
                # Inherit attributes of the first char in word for the newline
                sample_rc = word_chars[0]
                result.append(RichChar(char="\n", color=sample_rc.color, shake=sample_rc.shake))
                is_first_line = False
                current_line_text = word_text.lstrip()
                result.extend(word_chars)

        return result
