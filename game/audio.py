import os
import wave
import struct

ASSETS_AUDIO_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')


def ensure_sounds():
    os.makedirs(ASSETS_AUDIO_DIR, exist_ok=True)
    # create simple placeholder wav files if missing
    def write_simple_wav(path, freq=440, duration_ms=100):
        framerate = 44100
        amplitude = 8000
        n_samples = int(framerate * duration_ms / 1000.0)
        with wave.open(path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)
            for i in range(n_samples):
                t = float(i) / framerate
                val = int(amplitude * 0.5 * (1.0 + 0.5))
                data = struct.pack('<h', val)
                wf.writeframesraw(data)

    jump_path = os.path.join(ASSETS_AUDIO_DIR, 'jump.wav')
    coin_path = os.path.join(ASSETS_AUDIO_DIR, 'coin.wav')
    hit_path = os.path.join(ASSETS_AUDIO_DIR, 'hit.wav')

    for p in (jump_path, coin_path, hit_path):
        if not os.path.exists(p):
            # write a tiny silent-ish wav as placeholder
            write_simple_wav(p)
