"""Background video reader using FFmpeg subprocess with seamless looping."""
import subprocess
import os
from typing import Optional
from PIL import Image

class BackgroundVideoReader:
    def __init__(self, video_path: str, width: int = 1920, height: int = 1080, fps: int = 30):
        self.video_path = video_path
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_size = width * height * 3  # RGB24
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        """Start FFmpeg process reading looped video frames in RGB24 raw format."""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Background video not found: {self.video_path}")

        cmd = [
            "ffmpeg",
            "-stream_loop", "-1",  # Loop indefinitely
            "-i", self.video_path,
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),
            "-an",  # No audio
            "-"     # Pipe to stdout
        ]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=self.frame_size * 2
        )

    def read_frame(self) -> Optional[Image.Image]:
        """Read the next video frame as a PIL Image."""
        if self.process is None or self.process.stdout is None:
            return None

        raw_bytes = self.process.stdout.read(self.frame_size)
        if len(raw_bytes) < self.frame_size:
            return None

        return Image.frombytes("RGB", (self.width, self.height), raw_bytes)

    def close(self):
        """Terminate the FFmpeg background process."""
        if self.process:
            if self.process.stdout:
                self.process.stdout.close()
            self.process.terminate()
            self.process.wait()
            self.process = None
