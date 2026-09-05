from audio import load_audio, decode_samples, to_mono, make_time_axis, normalize, peak_amp, create_wave, make_wave


sr = 44100

created_wave = create_wave(1, 440, 2, sr)

make_wave("test_tone.wav", sr, created_wave)
audio = load_audio("test_tone.wav")
decoded_audio = decode_samples(audio)
mono = to_mono(decoded_audio, audio)
normalized = normalize(mono, audio)
peak = peak_amp(normalized)

print("Sample Rate", audio.sample_rate)
print("Frames", audio.num_frames)
print("Duration", audio.num_frames / audio.sample_rate)
print("Channels", audio.channels)
print("Peak amplitude", peak)
