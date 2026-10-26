"""Audio mixer for combining dialogue speech, BGM looping/fadeout, and sound effects."""
import os
import math
from pydub import AudioSegment
from typing import Optional

class AudioMixer:
    @staticmethod
    def mix_bgm_and_voice(
        voice_track: AudioSegment,
        bgm_path: Optional[str] = None,
        bgm_volume: float = 0.5,
        fade_out_ms: int = 1500
    ) -> AudioSegment:
        """
        Overlay looped BGM with fade-out over the voice track.
        """
        if not bgm_path or not os.path.exists(bgm_path):
            return voice_track

        # Load BGM
        bgm = AudioSegment.from_file(bgm_path).set_frame_rate(44100).set_channels(1)
        
        # Calculate volume gain in dB (1.0 = 0dB, 0.5 = -6dB, 0.1 = -20dB)
        if bgm_volume <= 0.0:
            return voice_track
        gain_db = 20 * math.log10(min(1.0, max(0.01, bgm_volume)))
        bgm = bgm.apply_gain(gain_db)

        target_len_ms = len(voice_track)
        if len(bgm) == 0:
            return voice_track

        # Loop BGM until it covers the target length
        looped_bgm = bgm
        while len(looped_bgm) < target_len_ms:
            looped_bgm = looped_bgm + bgm

        # Trim to exact length
        looped_bgm = looped_bgm[:target_len_ms]

        # Apply smooth fade out at the end
        if target_len_ms > fade_out_ms:
            looped_bgm = looped_bgm.fade_out(fade_out_ms)

        # Mix voice over BGM (BGM is background, voice is overlay)
        mixed = looped_bgm.overlay(voice_track)
        return mixed
