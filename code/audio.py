import wave
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class Audio:
    sample_rate: int
    sample_width: int
    channels: int
    num_frames: int
    data: bytes



def load_audio(filename):
    try:
        with wave.open(filename, "rb") as w:
            sample_rate = w.getframerate()
            sample_width = w.getsampwidth()
            channels = w.getnchannels()
            num_frames = w.getnframes()
            data = w.readframes(num_frames)
    except wave.Error:
        raise ValueError("Loader doesnt support float32 files")
    return Audio(sample_rate, sample_width, channels, num_frames, data)

def decode_samples(audio):
    if audio.sample_width == 1:
        fmt = np.uint8
    elif audio.sample_width == 2:
        fmt = np.int16
    elif audio.sample_width == 4:
        fmt = np.int32
    else:
        raise ValueError("Unsupported sample width")
    decoded_array = np.frombuffer(audio.data, dtype=fmt)
    if audio.num_frames * audio.channels == len(decoded_array):
        return decoded_array
    else:
        raise ValueError(f'expected {audio.num_frames * audio.channels} samples, got {len(decoded_array)}')

def to_mono(samples, audio):
    if audio.channels == 1:
        return samples
    elif audio.channels == 2:
        left = samples[::2]
        right = samples[1::2]
        return ((np.array(left) + np.array(right)) / 2)
    else:
        raise ValueError("Unsupported channels")

def make_time_axis(audio):
    time = np.arange(audio.num_frames)
    time_seconds = time / audio.sample_rate
    return time_seconds

