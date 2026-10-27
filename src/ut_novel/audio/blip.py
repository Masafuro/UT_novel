"""Voice Blip Audio Generator supporting multiple character voice sound effects."""
import os
from pydub import AudioSegment
from typing import List, Dict, Optional
from ut_novel.timeline import AudioEvent

class BlipAudioGenerator:
    def __init__(self, default_blip_path: str = "assets/se/voice_default.wav"):
        self.default_blip_path = default_blip_path
        self._sound_cache: Dict[str, AudioSegment] = {}
        self._load_sound(default_blip_path)

    def _load_sound(self, sound_path: str) -> AudioSegment:
        if sound_path in self._sound_cache:
            return self._sound_cache[sound_path]

        if os.path.exists(sound_path):
            sample = AudioSegment.from_file(sound_path)
        elif os.path.exists(self.default_blip_path):
            sample = AudioSegment.from_file(self.default_blip_path)
        else:
            sample = AudioSegment.silent(duration=10)

        self._sound_cache[sound_path] = sample
        return sample

    def generate_track_from_events(
        self,
        audio_events: List[AudioEvent],
        total_duration_sec: float
    ) -> AudioSegment:
        """Create an AudioSegment where character blip SEs are overlaid at specified timestamps."""
        total_ms = int(total_duration_sec * 1000)
        track = AudioSegment.silent(duration=total_ms, frame_rate=44100)

        for event in audio_events:
            if event.should_play:
                pos_ms = int(event.timestamp_sec * 1000)
                if pos_ms < total_ms:
                    sample = self._load_sound(event.sound_path)
                    track = track.overlay(sample, position=pos_ms)

        return track

    # Backward compatibility alias
    generate_blip_track_for_events = generate_track_from_events
