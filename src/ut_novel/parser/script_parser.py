"""Markdown Script Parser with YAML frontmatter support and RichText metadata."""
import re
import os
import frontmatter
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ut_novel.models import CharacterConfig, DialogBoxConfig, SplashConfig
from ut_novel.parser.rich_text import RichTextParser, RichChar

@dataclass
class DialogueLine:
    speaker: Optional[str] = None
    face: Optional[str] = None
    raw_text: str = ""
    plain_text: str = ""
    rich_chars: List[RichChar] = field(default_factory=list)
    wrapped_rich_chars: List[RichChar] = field(default_factory=list)
    voice_mode: str = "blip"  # "blip" or "tts"
    voice_sound: Optional[str] = None
    tts_provider: str = "gtts"
    tts_voice_id: Optional[str] = None
    tts_speed: float = 1.0
    custom_audio_path: Optional[str] = None
    pause_after: float = 1.5

@dataclass
class ParsedScript:
    title: str = "Untitled"
    aspect_ratio: str = "16:9"
    fps: int = 30
    bg_path: Optional[str] = None
    bgm_path: Optional[str] = None
    bgm_volume: float = 0.7
    splash_start: Optional[SplashConfig] = None
    splash_end: Optional[SplashConfig] = None
    characters: Dict[str, CharacterConfig] = field(default_factory=dict)
    lines: List[DialogueLine] = field(default_factory=list)

class ScriptParser:
    DIALOGUE_REGEX = re.compile(
        r"^\*\s*(?:([a-zA-Z0-9_-]+)(?:\(([a-zA-Z0-9_-]+)\))?:\s*)?(.*)$"
    )
    VOICE_TAG_REGEX = re.compile(r'\[voice:\s*["\']?([^"\'\]]+)["\']?\]')

    def _parse_splash(self, data) -> Optional[SplashConfig]:
        if not data:
            return None
        if isinstance(data, str):
            return SplashConfig(image=data)
        elif isinstance(data, dict):
            return SplashConfig(
                image=data.get("image", ""),
                duration=float(data.get("duration", 3.0)),
                fade_in=float(data.get("fade_in", data.get("fade_sec", 0.5))),
                fade_out=float(data.get("fade_out", data.get("fade_sec", 0.5))),
                transition=data.get("transition", "fade_black")
            )
        return None

    def parse_file(self, filepath: str) -> ParsedScript:
        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        meta: Dict = post.metadata if isinstance(post.metadata, dict) else {}
        bg_val = meta.get("bg")
        bgm_val = meta.get("bgm")
        fps_val = meta.get("fps", 30)
        bgm_vol_val = meta.get("bgm_volume", 0.7)

        parsed = ParsedScript(
            title=str(meta.get("title", "Untitled")),
            aspect_ratio=str(meta.get("aspect_ratio", "16:9")),
            fps=int(fps_val) if isinstance(fps_val, (int, str, float)) else 30,
            bg_path=str(bg_val) if bg_val else None,
            bgm_path=str(bgm_val) if bgm_val else None,
            bgm_volume=float(bgm_vol_val) if isinstance(bgm_vol_val, (int, str, float)) else 0.7,
            splash_start=self._parse_splash(meta.get("splash_start", meta.get("splash_intro"))),
            splash_end=self._parse_splash(meta.get("splash_end", meta.get("splash_outro")))
        )

        # Parse characters
        raw_chars = meta.get("characters")
        if isinstance(raw_chars, dict):
            for char_id, c_data in raw_chars.items():
                if not isinstance(c_data, dict):
                    continue
                tts_info = c_data.get("tts")
                if not isinstance(tts_info, dict):
                    tts_info = {}
                tts_speed_val = tts_info.get("speed", 1.0)
                parsed.characters[str(char_id)] = CharacterConfig(
                    name=str(c_data.get("name", char_id)),
                    voice_mode=str(c_data.get("voice_mode", "blip")),
                    blip_sound=str(c_data.get("voice", c_data.get("blip_sound", "assets/se/voice_default.wav"))),
                    tts_provider=str(tts_info.get("provider", "gtts")),
                    tts_voice_id=str(tts_info.get("voice_id")) if tts_info.get("voice_id") else None,
                    tts_speed=float(tts_speed_val) if isinstance(tts_speed_val, (int, str, float)) else 1.0,
                    font_path=str(c_data.get("font")) if c_data.get("font") else None,
                    default_face=str(c_data.get("default_face")) if c_data.get("default_face") else None,
                    faces=dict(c_data.get("faces", {}))
                )

        # Parse body dialogue lines
        body_lines = post.content.splitlines()
        for line_str in body_lines:
            line_str = line_str.strip()
            if not line_str or line_str.startswith("#"):
                continue

            match = self.DIALOGUE_REGEX.match(line_str)
            if match:
                speaker_id = match.group(1)
                face = match.group(2)
                text = match.group(3)

                # Check for inline custom voice tag
                custom_audio = None
                voice_match = self.VOICE_TAG_REGEX.search(text)
                if voice_match:
                    custom_audio = voice_match.group(1).strip()
                    text = self.VOICE_TAG_REGEX.sub("", text).strip()

                # Default voice settings
                voice_mode = "blip"
                voice_sound = "assets/se/voice_default.wav"
                tts_provider = "gtts"
                tts_voice_id = None
                tts_speed = 1.0

                if speaker_id and speaker_id in parsed.characters:
                    c_cfg = parsed.characters[speaker_id]
                    voice_mode = c_cfg.voice_mode
                    voice_sound = c_cfg.blip_sound
                    tts_provider = c_cfg.tts_provider
                    tts_voice_id = c_cfg.tts_voice_id
                    tts_speed = c_cfg.tts_speed
                    if not face and c_cfg.default_face:
                        face = c_cfg.default_face

                if custom_audio:
                    voice_mode = "tts"
                    tts_provider = "custom"

                # Parse rich characters and clean plain text for TTS
                plain_text = RichTextParser.strip_tags(text)
                rich_chars = RichTextParser.parse(text)

                parsed.lines.append(DialogueLine(
                    speaker=speaker_id,
                    face=face,
                    raw_text=text,
                    plain_text=plain_text,
                    rich_chars=rich_chars,
                    wrapped_rich_chars=[],
                    voice_mode=voice_mode,
                    voice_sound=voice_sound,
                    tts_provider=tts_provider,
                    tts_voice_id=tts_voice_id,
                    tts_speed=tts_speed,
                    custom_audio_path=custom_audio
                ))

        return parsed
