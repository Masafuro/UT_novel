"""Milestone 2 MVP Script: Render a typing animation video with voice blips."""
import os
import sys

# Ensure src is in sys.path
sys.path.insert(0, os.path.abspath("src"))

from ut_novel.models import DialogBoxConfig
from ut_novel.visual.textbox import DialogBoxRenderer
from ut_novel.audio.blip import BlipAudioGenerator
from ut_novel.timeline import SimpleTimeline
from ut_novel.encoder.ffmpeg_pipe import FFmpegPipeEncoder
from PIL import Image, ImageDraw

def create_dummy_portrait() -> Image.Image:
    p_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(p_img)
    # Simple retro white face
    p_draw.rectangle([10, 10, 90, 90], outline=(255, 255, 255), width=4)
    p_draw.rectangle([30, 30, 40, 40], fill=(255, 255, 255))
    p_draw.rectangle([60, 30, 70, 40], fill=(255, 255, 255))
    p_draw.line([(30, 70), (70, 70)], fill=(255, 255, 255), width=4)
    return p_img

def main():
    print("=== Milestone 2: Rendering MVP Typing Video with Voice Blips ===")
    
    dialog_text = "Hello, human.\nWelcome to the underground."
    fps = 30
    frames_per_char = 2
    output_mp4 = "output/m2_test.mp4"
    temp_audio_wav = "output/temp_m2_audio.wav"
    os.makedirs("output", exist_ok=True)

    # 1. Timeline generation
    print("1. Calculating timeline and events...")
    timeline = SimpleTimeline(fps=fps, frames_per_char=frames_per_char, post_dialog_pause=1.5)
    frames, audio_events, total_duration = timeline.build_timeline_for_text(dialog_text)
    print(f"   Total frames: {len(frames)} ({total_duration:.2f}s)")

    # 2. Audio track generation
    print("2. Generating voice blip audio track...")
    audio_gen = BlipAudioGenerator(default_blip_path="assets/se/voice_default.wav")
    audio_track = audio_gen.generate_blip_track_for_events(audio_events, total_duration)
    audio_track.export(temp_audio_wav, format="wav")
    print(f"   Saved audio to {temp_audio_wav}")

    # 3. Video rendering & encoding via FFmpeg pipe
    print("3. Rendering frames & encoding via FFmpeg pipe...")
    config = DialogBoxConfig(screen_width=1920, screen_height=1080)
    renderer = DialogBoxRenderer(config)
    portrait = create_dummy_portrait()

    encoder = FFmpegPipeEncoder(
        output_path=output_mp4,
        width=config.screen_width,
        height=config.screen_height,
        fps=fps,
        audio_path=temp_audio_wav
    )
    encoder.start()

    # Pre-render background image once for performance
    base_bg = Image.new("RGB", (config.screen_width, config.screen_height), (0, 0, 0))

    last_text = ""
    cached_frame = None

    for i, f_state in enumerate(frames):
        # Cache optimization: if visible text hasn't changed, reuse previous frame
        if f_state.visible_text == last_text and cached_frame is not None:
            encoder.write_frame(cached_frame)
        else:
            frame_img = renderer.render_frame(
                base_image=base_bg,
                text=f_state.visible_text,
                portrait_image=portrait
            )
            cached_frame = frame_img
            last_text = f_state.visible_text
            encoder.write_frame(frame_img)

        if i % 30 == 0:
            print(f"   Progress: {i}/{len(frames)} frames", end="\r")

    print(f"\n   Progress: {len(frames)}/{len(frames)} frames done.")
    print("4. Finishing FFmpeg encoding...")
    encoder.finish()

    # Clean up temp audio
    if os.path.exists(temp_audio_wav):
        os.remove(temp_audio_wav)

    file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"Successfully generated {output_mp4} ({file_size_mb:.2f} MB)")
    print("=== Milestone 2 verification successful! ===")

if __name__ == "__main__":
    main()
