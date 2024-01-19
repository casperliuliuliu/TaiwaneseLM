from gtts import gTTS
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

# Example usage
words = ["測試", "casper", "nostalgia","卡布奇諾"]
speak_vocabulary(words)
