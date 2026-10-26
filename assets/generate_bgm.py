"""Generate a charming Undertale-style 8-bit chiptune ambient loop music."""
import numpy as np
import soundfile as sf
import os

def generate_chiptune_loop(filename: str, sample_rate: int = 44100):
    # BPM = 96, 4 beats per measure
    bpm = 96
    beat_dur = 60.0 / bpm
    total_beats = 16  # 4 measures (10 seconds)
    total_duration = total_beats * beat_dur
    total_samples = int(sample_rate * total_duration)

    audio = np.zeros(total_samples, dtype=np.float32)

    # Chords (frequencies in Hz): Am, F, C, G
    # Melodic arpeggio notes
    chords = [
        [220.0, 261.63, 329.63, 440.0],  # Am (A, C, E, A)
        [174.61, 220.0, 261.63, 349.23],  # F (F, A, C, F)
        [261.63, 329.63, 392.00, 523.25],  # C (C, E, G, C)
        [196.00, 246.94, 293.66, 392.00],  # G (G, B, D, G)
    ]

    # Generate 16th-note arpeggiated pulse waves
    note_dur = beat_dur / 4.0
    note_samples = int(sample_rate * note_dur)

    pattern = [0, 1, 2, 3, 2, 1, 2, 3] * 2  # 16 notes per measure

    for m_idx, chord in enumerate(chords):
        m_start_beat = m_idx * 4
        for n_idx, p_val in enumerate(pattern):
            note_time = (m_start_beat * beat_dur) + (n_idx * note_dur)
            start_s = int(note_time * sample_rate)
            end_s = min(total_samples, start_s + note_samples)
            if start_s >= total_samples:
                break

            freq = chord[p_val % len(chord)]
            t = np.linspace(0, (end_s - start_s) / sample_rate, end_s - start_s, endpoint=False)
            
            # Pulse wave (duty cycle 25% like NES/GameBoy)
            phase = (t * freq) % 1.0
            pulse = np.where(phase < 0.25, 0.4, -0.4)
            # Soft decay
            envelope = np.exp(-t * 12.0)
            audio[start_s:end_s] += (pulse * envelope * 0.15).astype(np.float32)

    # Add gentle bass notes
    bass_notes = [110.0, 87.31, 130.81, 98.00]
    for m_idx, b_freq in enumerate(bass_notes):
        start_s = int(m_idx * 4 * beat_dur * sample_rate)
        end_s = int((m_idx + 1) * 4 * beat_dur * sample_rate)
        t = np.linspace(0, (end_s - start_s) / sample_rate, end_s - start_s, endpoint=False)
        # Triangle bass
        tri = 2 * np.abs(2 * (t * b_freq - np.floor(t * b_freq + 0.5))) - 1
        env = np.exp(-t * 1.5)
        audio[start_s:end_s] += (tri * env * 0.2).astype(np.float32)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sf.write(filename, audio, sample_rate)
    print(f"Generated BGM: {filename} ({total_duration:.2f}s)")

if __name__ == "__main__":
    generate_chiptune_loop("assets/bgm/ruins_theme.wav")
