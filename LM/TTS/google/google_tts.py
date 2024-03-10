from gtts import gTTS
from pydub import AudioSegment
import os
import tempfile

def speak_vocabulary(words):
    # Convert the list of words to a single string
    text_to_speak = ", ".join(words)

    # Create a gTTS object
    tts = gTTS(text=text_to_speak, lang='zh-TW', slow=False)

    # Save the speech to a temporary file and play it
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts.save(fp.name)
        os.system(f"afplay {fp.name}")


def speak_vocabulary_fast(words, speed=1.5):  # speed > 1.0 to speed up, < 1.0 to slow down
    # Convert the list of words to a single string
    text_to_speak = ", ".join(words)

    # Create a gTTS object
    tts = gTTS(text=text_to_speak, lang='en', slow=False)

    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts_fp = fp.name
        tts.save(tts_fp)

    # Load the saved mp3 file and alter the speed
    audio = AudioSegment.from_mp3(tts_fp)
    print(audio)
    fast_audio = audio.speedup(playback_speed=speed)

    # Save the altered audio to another temporary file and play it
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fast_fp:
        fast_audio.export(fast_fp.name, format="mp3")
        os.system(f"afplay {fast_fp.name}")

    # Clean up the initial tts file
    os.remove(tts_fp)

# Example usage
words = ["apple", "banana", "cherry"]
words = ["你好"]
speak_vocabulary_fast(words, speed=10)  # Increase the speed to 1.5 times the normal speed
# # Example usage
# words = ["測試", "casper", "nostalgia","卡布奇諾"]
# speak_vocabulary(words)
