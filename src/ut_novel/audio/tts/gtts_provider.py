"""gTTS (Google Text-To-Speech) provider for English speech generation."""
import os
import hashlib
import io
from typing import Optional
from gtts import gTTS
from pydub import AudioSegment
from ut_novel.audio.tts.base import BaseTTSProvider

class GTTSProvider(BaseTTSProvider):
    def __init__(self, cache_dir: str = ".cache/tts"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def synthesize(self, text: str, voice_id: Optional[str] = None, speed: float = 1.0) -> AudioSegment:
        # Clean text from any markup tags if present (e.g. [shake], etc.)
        import re
        clean_text = re.sub(r"\[.*?\]", "", text).strip()
        if not clean_text:
            return AudioSegment.silent(duration=100)

        tld = "com"
        lang = "en"
        if voice_id:
            # support uk, us, ca, au, etc.
            if voice_id.lower() in ["uk", "co.uk", "british"]:
                tld = "co.uk"
            elif voice_id.lower() in ["au", "com.au", "australian"]:
                tld = "com.au"
            elif voice_id.lower() in ["ca", "ca", "canadian"]:
                tld = "ca"

        # Cache key based on text and voice
        cache_key = hashlib.md5(f"{clean_text}_{lang}_{tld}_{speed}".encode("utf-8")).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.mp3")

        if os.path.exists(cache_file):
            audio = AudioSegment.from_file(cache_file, format="mp3")
        else:
            tts = gTTS(text=clean_text, lang=lang, tld=tld, slow=(speed < 0.9))
            tts.save(cache_file)
            audio = AudioSegment.from_file(cache_file, format="mp3")

        # Convert to 44100Hz mono for consistent mixing
        return audio.set_frame_rate(44100).set_channels(1)
