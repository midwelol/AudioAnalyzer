from audio import (
    load_audio,
    decode_samples,
    to_mono,
    normalize,
    peak_amp,
    find_rms,
    to_dbfs,
    find_common_frequencies,
    find_dominant_frequency,
    plot_frequency_dbfs,
    make_time_axis,
    plot_waveform,
    plot_both
)
import numpy as np


# Load the WAV file and prepare the samples for analysis.
filename = input("Enter the path to a WAV file: ")
audio = load_audio(filename)
decoded_audio = decode_samples(audio)
mono = to_mono(decoded_audio, audio)
normalized = normalize(mono, audio)

# Calculate amplitude and RMS measurements.
peak = peak_amp(normalized)
root_mean_square = find_rms(normalized)

# Create the time axis and calculate the frequency spectrum using an FFT.
time_axis = make_time_axis(audio)
freq, mag = find_common_frequencies(normalized, audio)
dominant = find_dominant_frequency(freq, mag)

# Convert the FFT magnitude to amplitude and then to dBFS.
mag_to_amp = 2 * mag / normalized.size
mag_dbfs = to_dbfs(mag_to_amp)
fft_peak = np.max(mag_dbfs)

# Display audio properties and calculated measurements.
print("Sample Rate", audio.sample_rate)
print("Frames", audio.num_frames)
print("Duration", audio.num_frames / audio.sample_rate)
print("Channels", audio.channels)
print("Peak amplitude", peak)
print("RMS: ", root_mean_square)
print("Peak amp (dbfs): ", to_dbfs(peak))
print("RMS (dbfs): ", to_dbfs(root_mean_square))
print("Dominant Frequency: ", dominant)
print("FFT Peak: ", fft_peak, "dBFS")

# Let the user choose which visualization to display.
print("What would you like to see?")
print("1. Waveform")
print("2. Frequency Spectrum (dBFS)")
print("3. Both")

choice = int(input("Enter your choice: "))
if choice == 1:
    plot_waveform(time_axis, normalized)
elif choice == 2:
    plot_frequency_dbfs(freq, mag_dbfs)
elif choice == 3:
    plot_both(time_axis, normalized, freq, mag_dbfs)
else:
    print("Invalid choice")

