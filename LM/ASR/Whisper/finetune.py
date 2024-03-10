
from transformers import WhisperFeatureExtractor
feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-base")

from transformers import WhisperTokenizer
tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-base", language="chinese", task="transcribe")

from transformers import WhisperProcessor
processor = WhisperProcessor.from_pretrained("openai/whisper-base", language="chinese", task="transcribe")

from datasets import Audio

common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16000))

print(common_voice["train"][0])