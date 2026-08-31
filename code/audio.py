import struct
import wave
import numpy as np
from dataclasses import dataclass


@dataclass
class Audio:
    sample_rate: int
    sample_width: int
    channels: int
    num_frames: int
    data: bytes



def load_audio(filename):
    w = wave.open(filename, "rb")
    sample_rate = w.getframerate()
    sample_width = w.getsampwidth()
    channels = w.getnchannels()
    num_frames = w.getnframes()
    data = w.readframes(num_frames)
    return Audio(sample_rate, sample_width, channels, num_frames, data)


def decode_samples():
    pass

def split_audio():
    pass

def make_mono():
    pass

def make_time_axis():
    pass