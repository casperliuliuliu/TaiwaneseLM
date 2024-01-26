"""
Training Models with MFCCs vs. Raw WAV
Regarding training models, particularly in machine learning and deep learning:

Direct WAV Training: It's possible to train models directly on raw audio waveforms (WAV format). This approach has gained traction with the advent of deeper and more complex neural networks. Models like WaveNet and some variants of convolutional neural networks (CNNs) can handle raw audio data effectively.

MFCCs as Features: However, training on raw audio can be computationally expensive and might require more data to achieve the same performance as a feature-based approach. MFCCs, being a more compact representation, can capture essential characteristics of the audio signal and are computationally more efficient. They are especially useful when resources are limited or when using more traditional machine learning models.
"""

"""
Common Feature Extraction for Audio:

In the realm of audio signal processing and particularly in speech and music analysis, several feature extraction methods are used, each with its own characteristics and applications. Here's an introduction to some common audio feature extraction techniques, along with a comparison:

### 1. Mel-Frequency Cepstral Coefficients (MFCCs)
- **Description**: MFCCs are coefficients that collectively make up an MFC. They are derived from the Fourier transform of a log power spectrum on a nonlinear mel scale of frequency.
- **Use Cases**: Widely used in speech recognition, speaker identification, and other audio classification tasks.
- **Advantages**: Effective in capturing the timbral and spectral characteristics of audio.
- **Limitations**: May not capture temporal dynamics effectively.

### 2. Spectrogram
- **Description**: A spectrogram is a visual representation of the spectrum of frequencies in a sound or other signal as they vary with time. It's essentially a collection of FFTs over time.
- **Use Cases**: Used for analysis of frequencies over time, in speech analysis, music genre classification, etc.
- **Advantages**: Provides a 2D representation of audio, capturing both frequency and time information.
- **Limitations**: The resolution is limited by the window size of the FFT.

### 3. Zero Crossing Rate (ZCR)
- **Description**: The rate at which the signal changes its sign (from positive to negative and vice versa). It's a measure of the noisiness or the frequency of the signal.
- **Use Cases**: Useful in music genre classification, speech-music discrimination.
- **Advantages**: Simple to compute and can indicate the presence of high-frequency content.
- **Limitations**: Limited information about the actual frequency content.

### 4. Chroma Features
- **Description**: Chroma features are a powerful tool for analyzing music as they capture the harmonic and melodic characteristics of audio.
- **Use Cases**: Common in music information retrieval for tasks like chord detection and music similarity.
- **Advantages**: Good for analyzing tonal content.
- **Limitations**: Not very informative for non-musical content.

### 5. Short-Time Fourier Transform (STFT)
- **Description**: STFT is used to determine the sinusoidal frequency and phase content of local sections of a signal as it changes over time.
- **Use Cases**: Foundation for many other features; used in speech processing, music analysis.
- **Advantages**: Captures both frequency and time information.
- **Limitations**: The fixed size of the window can be a limitation for signals with changing frequency content.

### 6. Linear Predictive Coding (LPC)
- **Description**: LPC models the signal as a linear combination of its past values and a prediction error.
- **Use Cases**: Used in speech analysis and compression, voice-over-IP (VoIP).
- **Advantages**: Good at representing the spectral envelope of a sound.
- **Limitations**: Less effective for non-speech signals or music.

### 7. Temporal Features
- **Description**: These include features like energy, entropy of energy, and statistical measures extracted from the amplitude of the waveform.
- **Use Cases**: Used in emotion recognition, speech-music discrimination, sound classification.
- **Advantages**: Captures energy dynamics of the signal.
- **Limitations**: Might not be sufficient for detailed frequency analysis.

### Comparison
- **Complexity**: MFCCs and LPC are more complex to compute than basic features like ZCR and energy.
- **Information Captured**: Spectrogram, STFT, and Chroma features are more informative for frequency analysis over time, while MFCCs and LPC are better for spectral envelope representation.
- **Application Suitability**: MFCCs are more suited for speech-related tasks, Chroma for music tonality, ZCR for rhythmic content, and spectrogram for a detailed time-frequency analysis.
- **Computational Resources**: Extracting features like MFCCs and Chroma features requires more computational resources compared to simpler features like ZCR or temporal features.

Choosing the right feature depends on the specific requirements of the task at hand, the nature of the audio signal, and the computational resources available. For instance, speech recognition systems heavily rely on MFCCs, while music information retrieval might benefit more from Chroma features and spectrograms.

"""
import librosa
import matplotlib.pyplot as plt

def preprocess_audio(filename):
    audio, sample_rate = librosa.load(filename, sr=None)
    print(audio.mean())
    print(sample_rate)
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=128)
    return mfccs

if __name__ == "__main__":
    vocal_audio = "D:/Casper/Data/Taiwanese/wav/ZC04/train/ZC04-F01/ZC04-F01_01.wav"
    sound_audio = "D:/Casper/TaiwaneseLM/multimodal/ImageBind/.assets/dog_audio.wav"
    print(preprocess_audio(vocal_audio).shape)

