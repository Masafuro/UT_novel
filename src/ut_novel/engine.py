"""Core NovelEngine supporting Aspect Ratio Presets (16:9 and 9:16 Shorts), BGM Looping/Fadeout, and Video Backgrounds."""
import os
from typing import Optional, Dict
from PIL import Image
from pydub import AudioSegment

from ut_novel.models import DialogBoxConfig, CharacterConfig
from ut_novel.parser.script_parser import ScriptParser, ParsedScript, DialogueLine
from ut_novel.parser.word_wrap import WordWrapper
from ut_novel.visual.textbox import DialogBoxRenderer
from ut_novel.visual.bg_video import BackgroundVideoReader
from ut_novel.audio.blip import BlipAudioGenerator
from ut_novel.audio.tts import GTTSProvider, CustomAudioProvider, BaseTTSProvider
from ut_novel.audio.mixer import AudioMixer
from ut_novel.timeline import AudioDrivenTimeline, SequenceFrameState
from ut_novel.encoder.ffmpeg_pipe import FFmpegPipeEncoder

class NovelEngine:
    def __init__(self, default_config: Optional[DialogBoxConfig] = None):
        self.default_config = default_config
        self.parser = ScriptParser()
        self.blip_generator = BlipAudioGenerator()
        
        self.tts_providers: Dict[str, BaseTTSProvider] = {
            "gtts": GTTSProvider(),
            "custom": CustomAudioProvider(),
        }

    def render_script_to_video(
        self,
        script_path: str,
        output_path: str,
        override_aspect_ratio: Optional[str] = None,
        override_fps: Optional[int] = None,
        preview_seconds: Optional[float] = None,
        temp_audio_path: Optional[str] = None
    ):
        print(f"=== Rendering Script: {script_path} ===")
        parsed = self.parser.parse_file(script_path)
        
        # Determine aspect ratio and layout configuration
        aspect_ratio = override_aspect_ratio or parsed.aspect_ratio or "16:9"
        cfg = DialogBoxConfig.get_preset(aspect_ratio)
        renderer = DialogBoxRenderer(cfg)
        fps = override_fps or parsed.fps or 30

        print(f"   Layout: {aspect_ratio} ({cfg.screen_width}x{cfg.screen_height}) @ {fps}fps")

        # 1. Preload character portrait images
        loaded_portraits: Dict[str, Image.Image] = {}
        for char_id, char_cfg in parsed.characters.items():
            for face_name, face_path in char_cfg.faces.items():
                key = f"{char_id}:{face_name}"
                if os.path.exists(face_path):
                    loaded_portraits[key] = Image.open(face_path).convert("RGBA")

        # 2. Word wrapping calculation with RichChar
        for line in parsed.lines:
            has_portrait = False
            if line.speaker and line.speaker in parsed.characters:
                char_cfg = parsed.characters[line.speaker]
                face = line.face or char_cfg.default_face
                if face and f"{line.speaker}:{face}" in loaded_portraits:
                    has_portrait = True

            max_w = cfg.box_width - cfg.text_margin_x * 2
            if has_portrait:
                max_w -= (cfg.portrait_size + 40)

            asterisk_w = int(renderer.font.getlength("* "))
            wrapper = WordWrapper(renderer.font, max_width=max_w, asterisk_indent=asterisk_w)
            line.wrapped_rich_chars = wrapper.wrap_rich_chars(line.rich_chars, prefix_asterisk=True)

        # 3. Audio Synthesis (TTS Pre-generation)
        print("1. Synthesizing speech and calculating durations...")
        line_audio_durations: Dict[int, float] = {}
        tts_audio_clips: Dict[int, AudioSegment] = {}

        for d_idx, line in enumerate(parsed.lines):
            if line.voice_mode == "tts":
                provider_key = line.tts_provider
                provider = self.tts_providers.get(provider_key, self.tts_providers["gtts"])
                
                voice_param = line.custom_audio_path if line.custom_audio_path else line.tts_voice_id
                speech_clip = provider.synthesize(text=line.plain_text, voice_id=voice_param, speed=line.tts_speed)
                duration_sec = len(speech_clip) / 1000.0
                line_audio_durations[d_idx] = duration_sec
                tts_audio_clips[d_idx] = speech_clip
                print(f"   [TTS] Line {d_idx} ({line.speaker}): {duration_sec:.2f}s")

        # 4. Build Synchronized Timeline
        print("2. Building synchronized timeline...")
        timeline = AudioDrivenTimeline(fps=fps, default_frames_per_char=2, clear_pause_sec=0.25)
        frames, audio_events, total_duration = timeline.build_timeline(parsed.lines, line_audio_durations)

        # Handle preview truncation if requested
        if preview_seconds and preview_seconds < total_duration:
            max_frames = int(preview_seconds * fps)
            frames = frames[:max_frames]
            total_duration = preview_seconds
            print(f"   Preview mode enabled: truncating to {preview_seconds:.1f}s")

        print(f"   Total frames: {len(frames)} ({total_duration:.2f}s)")

        # 5. Audio Mixing: Voice Tracks + BGM Loop + Fadeout
        print("3. Mixing voice tracks and background music (BGM)...")
        temp_audio = temp_audio_path or os.path.join(os.path.dirname(output_path), "temp_mixed_audio.wav")
        total_ms = int(total_duration * 1000)
        voice_track = AudioSegment.silent(duration=total_ms, frame_rate=44100)

        # Overlay voice blips
        blip_track = self.blip_generator.generate_track_from_events(audio_events, total_duration)
        voice_track = voice_track.overlay(blip_track)

        # Overlay TTS clips
        line_start_times: Dict[int, float] = {}
        for f in frames:
            if f.dialogue_index not in line_start_times and f.is_speaking:
                line_start_times[f.dialogue_index] = f.time_sec

        for d_idx, clip in tts_audio_clips.items():
            start_t = line_start_times.get(d_idx, 0.0)
            voice_track = voice_track.overlay(clip, position=int(start_t * 1000))

        # Mix with looped BGM
        final_audio = AudioMixer.mix_bgm_and_voice(
            voice_track=voice_track,
            bgm_path=parsed.bgm_path,
            bgm_volume=parsed.bgm_volume,
            fade_out_ms=1500
        )
        final_audio.export(temp_audio, format="wav")

        # 6. Initialize Background
        is_bg_video = False
        bg_video_reader: Optional[BackgroundVideoReader] = None
        static_bg_image: Optional[Image.Image] = None

        if parsed.bg_path and os.path.exists(parsed.bg_path):
            ext = os.path.splitext(parsed.bg_path)[1].lower()
            if ext in [".mp4", ".mov", ".webm", ".mkv"]:
                is_bg_video = True
                print(f"   Using background video: {parsed.bg_path}")
                bg_video_reader = BackgroundVideoReader(
                    video_path=parsed.bg_path,
                    width=cfg.screen_width,
                    height=cfg.screen_height,
                    fps=fps
                )
                bg_video_reader.start()
            else:
                # Cover scaling for static background
                raw_bg = Image.open(parsed.bg_path).convert("RGBA")
                # Scale to fill screen
                scale = max(cfg.screen_width / raw_bg.width, cfg.screen_height / raw_bg.height)
                scaled_w = int(raw_bg.width * scale)
                scaled_h = int(raw_bg.height * scale)
                scaled_bg = raw_bg.resize((scaled_w, scaled_h), Image.Resampling.BICUBIC)
                crop_x = (scaled_w - cfg.screen_width) // 2
                crop_y = (scaled_h - cfg.screen_height) // 2
                static_bg_image = scaled_bg.crop((crop_x, crop_y, crop_x + cfg.screen_width, crop_y + cfg.screen_height))
        else:
            static_bg_image = Image.new("RGBA", (cfg.screen_width, cfg.screen_height), (0, 0, 0, 255))

        # 7. Video Encoding
        print(f"4. Rendering frames & encoding to {output_path}...")
        encoder = FFmpegPipeEncoder(
            output_path=output_path,
            width=cfg.screen_width,
            height=cfg.screen_height,
            fps=fps,
            audio_path=temp_audio
        )
        encoder.start()

        try:
            for i, f_state in enumerate(frames):
                if is_bg_video and bg_video_reader is not None:
                    current_bg = bg_video_reader.read_frame()
                    if current_bg is None:
                        current_bg = static_bg_image
                else:
                    current_bg = static_bg_image

                portrait_img = None
                if f_state.speaker and f_state.face:
                    portrait_key = f"{f_state.speaker}:{f_state.face}"
                    portrait_img = loaded_portraits.get(portrait_key)

                frame_img = renderer.render_rich_frame(
                    base_image=current_bg,
                    visible_rich_chars=f_state.visible_rich_chars,
                    portrait_image=portrait_img,
                    is_speaking=f_state.is_speaking,
                    speaking_tick=f_state.speaking_tick,
                    frame_index=f_state.frame_index,
                    prefix_asterisk=bool(f_state.visible_rich_chars)
                )

                encoder.write_frame(frame_img)

                if i % 60 == 0:
                    print(f"   Progress: {i}/{len(frames)} frames", end="\r")

            print(f"\n   Progress: {len(frames)}/{len(frames)} frames done.")
        finally:
            if bg_video_reader is not None:
                bg_video_reader.close()

        print("5. Finalizing video...")
        encoder.finish()

        if os.path.exists(temp_audio):
            os.remove(temp_audio)

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Successfully generated {output_path} ({size_mb:.2f} MB)")
