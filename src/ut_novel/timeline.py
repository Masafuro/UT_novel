"""Audio-driven timeline calculations supporting RichText tags, Voice Blips, and TTS."""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from ut_novel.models import SplashConfig
from ut_novel.parser.script_parser import DialogueLine
from ut_novel.parser.rich_text import RichChar, RichTextParser

@dataclass
class SequenceFrameState:
    frame_index: int
    time_sec: float
    dialogue_index: int
    speaker: Optional[str]
    face: Optional[str]
    visible_rich_chars: List[RichChar] = field(default_factory=list)
    is_typing: bool = False
    is_speaking: bool = False
    speaking_tick: int = 0
    show_textbox: bool = True
    fade_alpha: float = 1.0
    bg_override: Optional[str] = None

    @property
    def visible_text(self) -> str:
        return "".join(rc.char for rc in self.visible_rich_chars)

@dataclass
class AudioEvent:
    timestamp_sec: float
    character: str
    sound_path: str
    should_play: bool

class AudioDrivenTimeline:
    def __init__(self, fps: int = 30, default_frames_per_char: int = 2, clear_pause_sec: float = 0.25):
        self.fps = fps
        self.default_frames_per_char = default_frames_per_char
        self.clear_pause_sec = clear_pause_sec

    def build_timeline(
        self,
        dialogue_lines: List[DialogueLine],
        line_audio_durations: Dict[int, float],
        splash_start: Optional[SplashConfig] = None,
        splash_end: Optional[SplashConfig] = None
    ) -> Tuple[List[SequenceFrameState], List[AudioEvent], float]:
        frames: List[SequenceFrameState] = []
        audio_events: List[AudioEvent] = []
        
        current_frame = 0

        def add_frame(
            dialogue_idx: int = -1,
            speaker: Optional[str] = None,
            face: Optional[str] = None,
            visible_chars: Optional[List[RichChar]] = None,
            is_typing: bool = False,
            is_speaking: bool = False,
            speaking_tick: int = 0,
            show_textbox: bool = True,
            fade_alpha: float = 1.0,
            bg_override: Optional[str] = None
        ):
            nonlocal current_frame
            frames.append(SequenceFrameState(
                frame_index=current_frame,
                time_sec=current_frame / self.fps,
                dialogue_index=dialogue_idx,
                speaker=speaker,
                face=face,
                visible_rich_chars=list(visible_chars) if visible_chars else [],
                is_typing=is_typing,
                is_speaking=is_speaking,
                speaking_tick=speaking_tick,
                show_textbox=show_textbox,
                fade_alpha=fade_alpha,
                bg_override=bg_override
            ))
            current_frame += 1

        # 1. Opening Splash Screen (splash_start)
        if splash_start and splash_start.image:
            total_splash_frames = max(1, int(splash_start.duration * self.fps))
            if splash_start.transition == "fade_black":
                fade_in_frames = int(splash_start.fade_in * self.fps)
                fade_out_frames = int(splash_start.fade_out * self.fps)
                hold_frames = max(0, total_splash_frames - fade_in_frames - fade_out_frames)

                for i in range(fade_in_frames):
                    alpha = (i + 1) / fade_in_frames if fade_in_frames > 0 else 1.0
                    add_frame(show_textbox=False, fade_alpha=alpha, bg_override=splash_start.image)

                for _ in range(hold_frames):
                    add_frame(show_textbox=False, fade_alpha=1.0, bg_override=splash_start.image)

                for i in range(fade_out_frames):
                    alpha = max(0.0, 1.0 - (i + 1) / fade_out_frames) if fade_out_frames > 0 else 0.0
                    add_frame(show_textbox=False, fade_alpha=alpha, bg_override=splash_start.image)

                # Brief black pause before dialogue
                black_pause_frames = int(self.fps * 0.25)
                for _ in range(black_pause_frames):
                    add_frame(show_textbox=False, fade_alpha=0.0)

                # Dialogue scene fade-in (0.35s)
                scene_fade_in_frames = int(self.fps * 0.35)
                for i in range(scene_fade_in_frames):
                    alpha = (i + 1) / scene_fade_in_frames
                    add_frame(show_textbox=True, fade_alpha=alpha)
            else:
                for _ in range(total_splash_frames):
                    add_frame(show_textbox=False, fade_alpha=1.0, bg_override=splash_start.image)

        punctuation_pause = {
            ',': int(self.fps * 0.15),
            ':': int(self.fps * 0.15),
            ';': int(self.fps * 0.15),
            '.': int(self.fps * 0.35),
            '!': int(self.fps * 0.35),
            '?': int(self.fps * 0.35),
        }

        for d_idx, d_line in enumerate(dialogue_lines):
            rich_chars = d_line.wrapped_rich_chars
            voice_mode = d_line.voice_mode
            speaking_tick = 0

            if voice_mode == "tts" and d_idx in line_audio_durations:
                # --- TTS Audio-Driven Mode ---
                speech_duration = line_audio_durations[d_idx]
                total_speech_frames = max(1, int(speech_duration * self.fps))
                char_count = len(rich_chars)

                for frame_offset in range(total_speech_frames):
                    ratio = (frame_offset + 1) / total_speech_frames
                    revealed_count = min(char_count, int(ratio * char_count))
                    current_visible = rich_chars[:revealed_count]

                    frames.append(SequenceFrameState(
                        frame_index=current_frame,
                        time_sec=current_frame / self.fps,
                        dialogue_index=d_idx,
                        speaker=d_line.speaker,
                        face=d_line.face,
                        visible_rich_chars=current_visible,
                        is_typing=True,
                        is_speaking=True,
                        speaking_tick=speaking_tick
                    ))
                    current_frame += 1
                    speaking_tick += 1

                final_chars = rich_chars
            else:
                # --- Classic Voice Blip Mode with Rich Tags ---
                voice_path = d_line.voice_sound or "assets/se/voice_default.wav"
                visible_chars: List[RichChar] = []

                for rc in rich_chars:
                    # Inline tag: [wait: sec]
                    if rc.wait_before > 0:
                        wait_frames = int(rc.wait_before * self.fps)
                        for _ in range(wait_frames):
                            frames.append(SequenceFrameState(
                                frame_index=current_frame,
                                time_sec=current_frame / self.fps,
                                dialogue_index=d_idx,
                                speaker=d_line.speaker,
                                face=d_line.face,
                                visible_rich_chars=list(visible_chars),
                                is_typing=False,
                                is_speaking=False,
                                speaking_tick=0
                            ))
                            current_frame += 1

                    # Trigger SE (either custom se_trigger or voice blip)
                    time_sec = current_frame / self.fps
                    if rc.se_trigger:
                        se_file = f"assets/se/{rc.se_trigger}.wav" if not rc.se_trigger.endswith(".wav") else rc.se_trigger
                        audio_events.append(AudioEvent(
                            timestamp_sec=time_sec,
                            character=rc.char,
                            sound_path=se_file,
                            should_play=True
                        ))
                    else:
                        should_play_blip = rc.char.isalnum()
                        audio_events.append(AudioEvent(
                            timestamp_sec=time_sec,
                            character=rc.char,
                            sound_path=voice_path,
                            should_play=should_play_blip
                        ))

                    visible_chars.append(rc)

                    for _ in range(self.default_frames_per_char):
                        frames.append(SequenceFrameState(
                            frame_index=current_frame,
                            time_sec=current_frame / self.fps,
                            dialogue_index=d_idx,
                            speaker=d_line.speaker,
                            face=d_line.face,
                            visible_rich_chars=list(visible_chars),
                            is_typing=True,
                            is_speaking=True,
                            speaking_tick=speaking_tick
                        ))
                        current_frame += 1
                        speaking_tick += 1

                    # Punctuation pause
                    if rc.char in punctuation_pause:
                        for _ in range(punctuation_pause[rc.char]):
                            frames.append(SequenceFrameState(
                                frame_index=current_frame,
                                time_sec=current_frame / self.fps,
                                dialogue_index=d_idx,
                                speaker=d_line.speaker,
                                face=d_line.face,
                                visible_rich_chars=list(visible_chars),
                                is_typing=False,
                                is_speaking=False,
                                speaking_tick=0
                            ))
                            current_frame += 1

                final_chars = visible_chars

            # Post-speech pause
            pause_frames = int(self.fps * d_line.pause_after)
            for _ in range(pause_frames):
                frames.append(SequenceFrameState(
                    frame_index=current_frame,
                    time_sec=current_frame / self.fps,
                    dialogue_index=d_idx,
                    speaker=d_line.speaker,
                    face=d_line.face,
                    visible_rich_chars=final_chars,
                    is_typing=False,
                    is_speaking=False,
                    speaking_tick=0
                ))
                current_frame += 1

            # Transition clear pause
            if d_idx < len(dialogue_lines) - 1:
                clear_frames = int(self.fps * self.clear_pause_sec)
                for _ in range(clear_frames):
                    frames.append(SequenceFrameState(
                        frame_index=current_frame,
                        time_sec=current_frame / self.fps,
                        dialogue_index=d_idx,
                        speaker=None,
                        face=None,
                        visible_rich_chars=[],
                        is_typing=False,
                        is_speaking=False,
                        speaking_tick=0
                    ))
                    current_frame += 1
        # 3. Ending Splash Screen (splash_end)
        if splash_end and splash_end.image:
            total_splash_frames = max(1, int(splash_end.duration * self.fps))
            if splash_end.transition == "fade_black":
                # Dialogue scene fade-out (0.35s)
                scene_fade_out_frames = int(self.fps * 0.35)
                for i in range(scene_fade_out_frames):
                    alpha = max(0.0, 1.0 - (i + 1) / scene_fade_out_frames)
                    add_frame(show_textbox=True, fade_alpha=alpha)

                # Brief black pause
                black_pause_frames = int(self.fps * 0.25)
                for _ in range(black_pause_frames):
                    add_frame(show_textbox=False, fade_alpha=0.0)

                # Fade in splash end
                fade_in_frames = int(splash_end.fade_in * self.fps)
                fade_out_frames = int(splash_end.fade_out * self.fps)
                hold_frames = max(0, total_splash_frames - fade_in_frames - fade_out_frames)

                for i in range(fade_in_frames):
                    alpha = (i + 1) / fade_in_frames if fade_in_frames > 0 else 1.0
                    add_frame(show_textbox=False, fade_alpha=alpha, bg_override=splash_end.image)

                for _ in range(hold_frames):
                    add_frame(show_textbox=False, fade_alpha=1.0, bg_override=splash_end.image)

                for i in range(fade_out_frames):
                    alpha = max(0.0, 1.0 - (i + 1) / fade_out_frames) if fade_out_frames > 0 else 0.0
                    add_frame(show_textbox=False, fade_alpha=alpha, bg_override=splash_end.image)
            else:
                for _ in range(total_splash_frames):
                    add_frame(show_textbox=False, fade_alpha=1.0, bg_override=splash_end.image)

        total_duration = current_frame / self.fps
        return frames, audio_events, total_duration

class SimpleTimeline(AudioDrivenTimeline):
    """Backward compatibility wrapper for early milestone scripts."""
    def __init__(self, fps: int = 30, frames_per_char: int = 2, post_dialog_pause: float = 1.5):
        super().__init__(fps=fps, default_frames_per_char=frames_per_char)
        self.post_dialog_pause = post_dialog_pause

    def build_timeline_for_text(self, text: str):
        rich_chars = RichTextParser.parse(text)
        line = DialogueLine(
            raw_text=text,
            plain_text=text,
            rich_chars=rich_chars,
            wrapped_rich_chars=rich_chars,
            pause_after=self.post_dialog_pause
        )
        return self.build_timeline([line], {})
