from audio import (
    Audio,
    load_audio,
    decode_samples,
    to_mono,
    normalize,
    peak_amp,
    find_rms,
    to_dbfs,
    find_frequency_spectrum,
    find_dominant_frequency,
    make_wave,
    create_wave
)
import numpy as np
import pytest


def test_peak_amplitude(tmp_path):
    # Verify peak amplitude using a sine wave with a known amplitude.
    amp = 0.25
    test_freq = 440
    duration = 0.1
    sr_wave = 44100

    test_signal = create_wave(amp, test_freq, duration, sr_wave)
    test_file = tmp_path / "peak_amplitude_test.wav"
    make_wave(test_file, sr_wave, test_signal)
    audio = load_audio(test_file)
    decoded_audio = decode_samples(audio)
    mono = to_mono(decoded_audio, audio)
    normalized = normalize(mono, audio)
    test_peak = peak_amp(normalized)
    expected_peak = amp
    tolerance = 0.01
    assert abs(test_peak - expected_peak) <= tolerance, f"Expected Peak ~{expected_peak}, got {test_peak}"

def test_dominant_frequency(tmp_path):
    # Verify the FFT identifies the known dominant frequency.
    amp = 0.25
    test_freq = 440
    duration = 0.1
    sr_wave = 44100

    test_signal = create_wave(amp, test_freq, duration, sr_wave)
    test_file = tmp_path / "dominant_freq_test.wav"
    make_wave(test_file, sr_wave, test_signal)
    audio = load_audio(test_file)
    decoded_audio = decode_samples(audio)
    mono = to_mono(decoded_audio, audio)
    normalized = normalize(mono, audio)
    freq, amplitudes = find_frequency_spectrum(normalized, audio)
    dominant_frequency_test = find_dominant_frequency(freq, amplitudes)
    expected_dominant_frequency = 440
    tolerance = 10
    assert abs(dominant_frequency_test - expected_dominant_frequency) <= tolerance, f"Expected dominant frequency ~{expected_dominant_frequency}, got {dominant_frequency_test}"

def test_rms(tmp_path):
    # Verify RMS against the theoretical RMS value of a sine wave.
    amp = 0.25
    test_freq = 440
    duration = 0.1
    sr_wave = 44100

    test_signal = create_wave(amp, test_freq, duration, sr_wave)
    test_file = tmp_path / "rms_test.wav"
    make_wave(test_file, sr_wave, test_signal)
    audio = load_audio(test_file)
    decoded_audio = decode_samples(audio)
    mono = to_mono(decoded_audio, audio)
    normalized = normalize(mono, audio)
    rms_test = find_rms(normalized)
    expected_rms = 0.25 / np.sqrt(2)
    tolerance = 0.01
    assert abs(rms_test - expected_rms) <= tolerance, f"Expected RMS ~{expected_rms}, got {rms_test}"

def test_dbfs(tmp_path):
    # Verify peak amplitude is converted to the expected dBFS value.
    amp = 0.25
    test_freq = 440
    duration = 0.1
    sr_wave = 44100

    test_signal = create_wave(amp, test_freq, duration, sr_wave)
    test_file = tmp_path / "dbfs_test.wav"
    make_wave(test_file, sr_wave, test_signal)
    audio = load_audio(test_file)
    decoded_audio = decode_samples(audio)
    mono = to_mono(decoded_audio, audio)
    normalized = normalize(mono, audio)
    peak = peak_amp(normalized)
    dbfs_test = to_dbfs(peak)
    expected_dbfs = 20 * np.log10(amp)
    tolerance = 0.01
    assert abs(dbfs_test - expected_dbfs) <= tolerance, f"Expected DBFS ~{expected_dbfs}, got {dbfs_test}"

def test_unsupported_sample_width():
    # Verify unsupported sample widths raise a ValueError.
    audio = Audio(
        sample_rate=44100,
        sample_width=3,
        channels=1,
        num_frames=1,
        data=b"\x00\x00\x00"
    )
    with pytest.raises(ValueError):
        decode_samples(audio)