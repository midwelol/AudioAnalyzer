import wave
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import scipy.io


@dataclass
class Audio:
    sample_rate: int
    sample_width: int
    channels: int
    num_frames: int
    data: bytes


# Generate a known sine wave for testing audio analysis functions.
def create_wave(amp, freq, duration, sr_wave):
    sample_count = int(duration * sr_wave)
    test_time = np.arange(sample_count)
    test_time_seconds = test_time / sr_wave

    gen_wave = amp * np.sin((2 * np.pi) * freq * test_time_seconds)

    # Convert the normalized signal to the int16 range used by the WAV file.
    gen_wave = gen_wave * 32767
    gen_wave = gen_wave.astype(np.int16)

    return gen_wave


# Write generated samples to a WAV file for testing.
def make_wave(filename, sr, gen_wave):
    scipy.io.wavfile.write(filename, sr, gen_wave)


# Read WAV metadata and raw audio data from a file.
def load_audio(filename):
    try:
        with wave.open(str(filename), "rb") as w:
            sample_rate = w.getframerate()
            sample_width = w.getsampwidth()
            channels = w.getnchannels()
            num_frames = w.getnframes()
            data = w.readframes(num_frames)
    except wave.Error:
        raise ValueError("Could not read WAV file")

    return Audio(sample_rate, sample_width, channels, num_frames, data)


# Convert raw WAV bytes into a NumPy array using the appropriate sample format.
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

    # Verify that the decoded sample count matches the WAV metadata.
    if audio.num_frames * audio.channels == len(decoded_array):
        return decoded_array
    else:
        raise ValueError(
            f'expected {audio.num_frames * audio.channels} samples, '
            f'got {len(decoded_array)}'
        )


# Convert stereo audio to mono by averaging the left and right channels.
def to_mono(samples, audio):
    if audio.channels == 1:
        return samples
    elif audio.channels == 2:
        left = samples[::2]
        right = samples[1::2]
        return ((np.array(left) + np.array(right)) / 2)
    else:
        raise ValueError("Unsupported channels")


# Create a time value for each audio frame.
def make_time_axis(audio):
    time = np.arange(audio.num_frames)
    time_axis = time / audio.sample_rate
    return time_axis


# Convert integer PCM samples to a normalized amplitude range.
def normalize(samples, audio):
    if audio.sample_width == 1:
        # 8-bit PCM is unsigned, so shift its midpoint to zero first.
        shift = samples - ((2**8) / 2)
        return shift / ((2**8) / 2)

    elif audio.sample_width == 2:
        # 16-bit PCM is signed, so divide by its full-scale amplitude.
        return samples / ((2**16) / 2)

    elif audio.sample_width == 4:
        # 32-bit PCM is signed, so divide by its full-scale amplitude.
        return samples / ((2**32) / 2)

    else:
        raise ValueError("NORMALIZE: Unsupported sample width")


# Find the largest absolute sample amplitude.
def peak_amp(samples):
    return np.max(np.abs(samples))


# Calculate the root mean square (RMS) amplitude of the signal.
def find_rms(samples):
    return np.sqrt(np.mean(samples**2))


# Convert amplitude values to decibels relative to full scale (dBFS).
def to_dbfs(value):
    if np.isscalar(value):
        if value <= 0:
            return -np.inf
        return 20 * np.log10(value)

    result = np.full_like(value, -np.inf, dtype=float)
    positive = value > 0
    result[positive] = 20 * np.log10(value[positive])

    return result


# Plot the audio signal's amplitude over time.
def plot_waveform(time_axis, samples):
    plt.plot(time_axis, samples)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Amplitude vs Time")
    plt.show()


# Calculate the frequency spectrum using a real-valued FFT.
def find_frequency_spectrum(samples, audio):
    n = samples.size
    window = np.hanning(n)
    windowed_samples = samples * window

    fft_result = np.fft.rfft(windowed_samples)
    magnitudes = np.abs(fft_result)
    frequencies = np.fft.rfftfreq(n, 1.0/audio.sample_rate)

    # Correct for the Hann window's coherent gain.
    amplitudes = magnitudes * (2.0 / np.sum(window))

    # DC should not be doubled.
    amplitudes[0] /= 2

    # Nyquist should not be doubled for an even-length signal.
    if n % 2 == 0:
        amplitudes[-1] /= 2

    return frequencies, amplitudes


# Plot the FFT magnitude spectrum.
def plot_common_frequencies(frequencies, magnitudes):
    plt.plot(frequencies, magnitudes)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Common Frequencies")
    plt.show()


# Find the frequency bin with the greatest FFT magnitude.
def find_dominant_frequency(frequencies, magnitudes):
    max_mag_index = np.argmax(magnitudes)

    return frequencies[max_mag_index]


# Plot the frequency spectrum using dBFS.
def plot_frequency_dbfs(frequencies, dbfs):
    plt.plot(frequencies, dbfs)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("dBFS")
    plt.title("Frequency Spectrum")
    plt.ylim(-120, 3)
    plt.show()


# Display the waveform and frequency spectrum together.
def plot_both(time_axis, samples, frequencies, dbfs):
    fig, (waveform, spectrum) = plt.subplots(2, 1)

    waveform.plot(time_axis, samples)
    waveform.set_xlabel("Time (seconds)")
    waveform.set_ylabel("Amplitude")
    waveform.set_title("Waveform")

    spectrum.plot(frequencies, dbfs)
    spectrum.set_xlabel("Frequency (Hz)")
    spectrum.set_ylabel("dBFS")
    spectrum.set_title("Frequency Spectrum")

    plt.tight_layout()
    plt.show()







