"""FFmpeg video encoder via pipe for fast and memory-efficient MP4 creation."""
import subprocess
import os
from typing import Optional
from PIL import Image

class FFmpegPipeEncoder:
    def __init__(
        self,
        output_path: str,
        width: int = 1920,
        height: int = 1080,
        fps: int = 30,
        audio_path: Optional[str] = None
    ):
        self.output_path = output_path
        self.width = width
        self.height = height
        self.fps = fps
        self.audio_path = audio_path
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        """Start the FFmpeg subprocess with rawvideo input pipe."""
        os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
        
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.width}x{self.height}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",  # Read from stdin
        ]

        if self.audio_path and os.path.exists(self.audio_path):
            cmd.extend([
                "-i", self.audio_path,
                "-c:a", "aac",
                "-b:a", "192k",
            ])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "veryfast",
            "-crf", "18",
            self.output_path
        ])

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

    def write_frame(self, image: Image.Image):
        """Write a PIL Image (RGB) to FFmpeg stdin."""
        if self.process is None or self.process.stdin is None:
            raise RuntimeError("FFmpeg process is not started.")
        
        # Ensure RGB format
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        self.process.stdin.write(image.tobytes())

    def finish(self):
        """Close stdin and wait for FFmpeg to finish encoding."""
        if self.process is None:
            return

        if self.process.stdin:
            self.process.stdin.close()
            
        stderr = self.process.stderr.read() if self.process.stderr else b""
        retcode = self.process.wait()
        
        if retcode != 0:
            raise RuntimeError(f"FFmpeg failed with return code {retcode}: {stderr.decode('utf-8', errors='ignore')}")
