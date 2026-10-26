"""Abstract base class for Text-To-Speech providers."""
from abc import ABC, abstractmethod
from typing import Optional
from pydub import AudioSegment

class BaseTTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, voice_id: Optional[str] = None, speed: float = 1.0) -> AudioSegment:
        """
        Synthesize speech from text and return as an AudioSegment.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier / accent (e.g., 'en-us', 'en-uk')
            speed: Playback speed multiplier
        """
        pass
