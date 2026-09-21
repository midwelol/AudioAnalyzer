# Audio Analyzer

A python based audio analysis tool I created to explore digital signal processing concepts including amplitude, RMS, dBFS, FFT-based frequency analysis, and waveform generation.

## Overview

Audio Analyzer is a Python project that analyzes and generates digital audio signals. I built it as a hands on way to learn fundamental digital signal processing concepts alongside my reading of ThinkDSP. This project allowed me to blend what I learned with ThinkDSP with Pythons scientific computing ecosystems. 

This project can load WAV audio, inspect audio metadata, perform amplitude and frequency-domain analysis, generate test signals, and visualize results. It uses NumPy for numerical operations, SciPy for signal-processing utilities, Matplotlib for visualization, and pytest for automated testing.

## Features

- WAV file loading and metadata extraction
- Support for multiple audio sample widths
- Stereo-to-mono conversion
- Audio normalization
- Peak amplitude measurement
- RMS amplitude measurement
- dBFS conversion
- Time-axis generation
- FFT-based frequency analysis
- Dominant-frequency detection
- Windowed FFT analysis
- Sine-wave generation
- Audio waveform visualization
- Automated unit tests with pytest

## DSP Concepts

### Peak Amplitude

Peak amplitude measures the largest absolute sample value in an audio signal.

For a discrete signal the peak = max(|x[n]|)

The analyzer uses peak amplitude to determine the maximum instantaneous sample level of the signal.

### RMS Amplitude

RMS (Root Mean Square) returns a measure of the average magnitude of an audio signal.

For a discrete signal RMS = sqrt((1/N) * Σ x[n]^2)

Unlike the peak amplitude, RMS represents the overall energy level of the signal rather than only its largest samples.

### dBFS

The analyzer converts amplitude measurements to dBFS (decibels relative to full scale).

For a discrete signal dBFS = 20 log10(amplitude)

0 dBFS represents the maximum representable digital level, while negative values represent lower levels.

It's important to mention that dBFS isnt just "decibles" but rather a description of digital amplitude relative to the maximum digital level.

### FFT / Frequency Analysis

This project uses NumPy's real-valued FFT (rfft) to transform the audio signal from the time domain into the frequency domain. The resulting spectrum is used to identify the frequency components present in the signal and determine the dominant frequency.

The frequency bins are calculated from the sample rate and FFT size.

The basic relationship is frequency_bin = k * sample_rate / N. 
Where:
- k = FFT bin index
- sample_rate = samples per second
- N = FFT size

### Windowing

Before performing frequency analysis, the analyzer can apply a window function to the signal.

Windowing reduces some spectral leakage which is caused by analyzing a finite section of a continuous signal.

This project uses a Hann window before performing the FFT. The FFT amplitude is then corrected for the window's coherent gain so that the resulting spectral amplitudes remain meaningful relative to the input signal.

## Project Structure

```text
AudioAnalyzer/
├── code/
│   ├── tests/
│   │   └── test_audio.py
│   ├── audio.py
│   └── main.py
├── .gitignore
└── README.md
```

### audio.py

Contains the main audio representation and analysis functionality, including audio loading, amplitude analysis, FFT analysis, and waveform generation.

### main.py

Provides the entry point for running the analyzer and experimenting with its functionality.

### test_audio.py

Contains automated tests for the audio-processing functionality using pytest.

## Installation

### Requirements

- Python 3.13+
- NumPy
- SciPy
- Matplotlib
- pytest

### Setup

Clone the repository:

git clone https://github.com/midwelol/AudioAnalyzer.git
cd AudioAnalyzer

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install numpy scipy matplotlib pytest

## Usage

The analyzer can load a WAV file and perform several types of analysis.

When running main.py, the console will prompt you to enter the path of an audio file.

It will then return the data from the audio file, which is:
- Sample Rate
- Frames
- Duration
- Channels
- Peak Amplitude
- RMS
- Peak Amplitude (dBFS)
- RMS (dBFS)
- Dominant Frequency
- FFT Peak

Then you will be prompted with options for graphing

What would you like to see?
1. Waveform
2. Frequency Spectrum (dBFS)
3. Both.

## Example Analysis 

In this example, I will be analyzing an audio file called "test.wav" located in a folder called "test_data"

Enter the path to a WAV file: C:\Users\sande\PycharmProjects\AudioAnalyzer\code\test_data\test.wav

Sample Rate 44100
Frames 3136846
Duration 71.1302947845805
Channels 2
Peak amplitude 0.4999542236328125
RMS:  0.0798501335384859
Peak amp (dbfs):  -6.021395166630833
RMS (dbfs):  -21.954487064528987
Dominant Frequency:  198.1996565977418
FFT Peak:  -38.95883428889948 dBFS

What would you like to see?
1. Waveform
2. Frequency Spectrum (dBFS)
3. Both

Enter your choice: 3

Selecting option 3 displays both the time-domain waveform and frequency-domain spectrum.

<img width="640" height="480" alt="Figure_1" src="https://github.com/user-attachments/assets/d47cbd01-2a77-4fb2-a06a-49443d2d4909" />

## Technologies

- Python
- NumPy
- SciPy
- Matplotlib
- pytest
- Git/GitHub

## Limitations

- Currently supports WAV files rather than compressed audio formats.
- Sample-width support is currently limited to 8-, 16-, and 32-bit PCM.
- Frequency analysis currently operates on the entire loaded signal rather than selectable analysis windows.
- The command-line interface is intended primarily for experimentation and learning rather than production audio analysis.

## Testing

The project includes automated tests using pytest to verify the core audio-analysis functionality.

The test suite verifies:

- Peak amplitude measurement against a known sine-wave amplitude
- RMS measurement against the theoretical RMS value of a sine wave
- dBFS conversion
- Dominant-frequency detection using FFT analysis
- Frequency detection across multiple test frequencies (100 Hz, 440 Hz, 1 kHz, and 5 kHz)
- FFT amplitude accuracy after Hann-window correction
- Error handling for unsupported sample widths

Test signals are generated programmatically with known amplitudes and frequencies, allowing the analysis functions to be compared against expected results.

Run the test suite with pytest







