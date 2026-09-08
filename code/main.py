from audio import *
import numpy as np

sr = 44100

created_wave = create_wave(0.25, 440, 0.1, sr)

make_wave("test_data/test_tone.wav", sr, created_wave)
filename = input("Audio file you want to test from the test_data folder (e.g. test.wav): ")
audio = load_audio("test_data/" + filename)
decoded_audio = decode_samples(audio)
mono = to_mono(decoded_audio, audio)
normalized = normalize(mono, audio)
peak = peak_amp(normalized)
root_mean_square = find_rms(normalized)
time_axis = make_time_axis(audio)
freq, mag = find_common_frequencies(normalized, audio)
dominant = find_dominant_frequency(freq, mag)
mag_to_amp = 2 * mag / normalized.size
mag_dbfs = to_dbfs(mag_to_amp)
fft_peak = np.max(mag_dbfs)

print("Sample Rate", audio.sample_rate)
print("Frames", audio.num_frames)
print("Duration", audio.num_frames / audio.sample_rate)
print("Channels", audio.channels)
print("Peak amplitude", peak)
print("Expected RMS: ", peak / np.sqrt(2))
print("RMS: ", root_mean_square)
print("Peak amp (dbfs): ", to_dbfs(peak))
print("RMS (dbfs): ", to_dbfs(root_mean_square))
print(np.max(mag))
print(peak * len(normalized) / 2)
print("Dominant Frequency: ", dominant)
print("FFT Peak: ", fft_peak, "dBFS")




plot_frequency_dbfs(freq, mag_dbfs)

