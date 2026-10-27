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
    
    # Default narrator blip (~420Hz square)
    create_blip(os.path.join(out_dir, "voice_default.wav"), freq=420.0, duration=0.04, wave_type="square")
    # Low pitch blip (Male / dev_boy_1 ~160Hz)
    create_blip(os.path.join(out_dir, "voice_low.wav"), freq=160.0, duration=0.05, wave_type="square")
    # High pitch blip (Female / dev_girl_1 ~560Hz)
    create_blip(os.path.join(out_dir, "voice_high.wav"), freq=560.0, duration=0.035, wave_type="triangle")

    # Retro sparkle / save chime
    def create_chime(filename: str, sample_rate: int = 44100):
        notes = [523.25, 659.25, 783.99, 1046.50]
        note_dur = 0.08
        audio_parts = []
        for freq in notes:
            t = np.linspace(0, note_dur, int(sample_rate * note_dur), endpoint=False)
            wave = np.sin(2 * np.pi * freq * t) + 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
            env = np.exp(-t * 20)
            audio_parts.append(wave * env * 0.35)
        audio = np.concatenate(audio_parts)
        sf.write(filename, audio.astype(np.float32), sample_rate)
        print(f"Generated {filename}")

    create_chime(os.path.join(out_dir, "save.wav"))
