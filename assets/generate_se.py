"""Generate default Undertale-like 8-bit voice blip sound effects."""
import numpy as np
import soundfile as sf
import os

def create_blip(filename: str, freq: float = 440.0, duration: float = 0.045, sample_rate: int = 44100, wave_type: str = "square"):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if wave_type == "square":
        # Square wave (classic 8-bit sound)
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "triangle":
        # Triangle wave (softer sound)
        wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    else:
        wave = np.sin(2 * np.pi * freq * t)
        
    # Apply exponential decay envelope for punchy click
    envelope = np.exp(-t * 50)
    audio = wave * envelope * 0.5
    
    sf.write(filename, audio.astype(np.float32), sample_rate)
    print(f"Generated {filename}")

if __name__ == "__main__":
    out_dir = "assets/se"
    os.makedirs(out_dir, exist_ok=True)
    
    # Default narrator blip (~440Hz square)
    create_blip(os.path.join(out_dir, "voice_default.wav"), freq=420.0, duration=0.04, wave_type="square")
    # Low blip (Sans-like ~150Hz)
    create_blip(os.path.join(out_dir, "voice_low.wav"), freq=160.0, duration=0.05, wave_type="square")
    # High blip (Papyrus/Toriel ~580Hz)
    create_blip(os.path.join(out_dir, "voice_high.wav"), freq=560.0, duration=0.035, wave_type="triangle")
