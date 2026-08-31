from time import monotonic

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import sys
import os
import struct

#learning how to open and get wav file metadata
wv = wave.open("test.wav", "rb")
sr = wv.getframerate()
width = wv.getsampwidth()
channels = wv.getnchannels()
numframes = wv.getnframes()

data = wv.readframes(numframes)

numsamples = numframes * channels

bitdepth = width * 8 #1 byte = 8 bit
bitrate_bps = sr * bitdepth * channels

#print(type(data))
#print(len(data))
#print(data[:20])

#try to get the amplitude
fmt = f"{numsamples}h"
samples = struct.unpack(fmt, data)

print(type(samples))
print(len(samples))
print(samples[:20])

left = samples[::2]
right = samples[1::2]

mono = ((np.array(left) + np.array(right)) / 2 )

duration = numframes / sr
time = np.arange(numframes)

time_seconds = time / sr
print(time[:10])

plt.plot(time_seconds, mono)
plt.show()