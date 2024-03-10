from ailabs_asr.streaming import StreamingClient
import sys
desired_path = "D:/Casper/Other"
sys.path.append(desired_path)

from my_config import get_config
config = get_config()
yating_key = config['yating_key']
# import pyaudio
def on_processing_sentence(message):
  print(f'hello: {message["asr_sentence"]}')

def on_final_sentence(message):
  print(f'world: {message["asr_sentence"]}')

# init the streaming client
asr_client = StreamingClient(yating_key)

# start streaming with wav file
asr_client.start_streaming_wav(
  pipeline='asr-zh-tw-std',
  file='D:\Casper\your-voice-file.wav',
  verbose=False, # enable verbose to show detailed recognition result
  on_processing_sentence=on_processing_sentence,
  on_final_sentence=on_final_sentence)
  

# import asyncio
# import ailabs_asr.transcriber as t
# from ailabs_asr.types import ModelConfig, TranscriptionConfig
# from concurrent.futures import as_completed
# audio='D:\Casper\example.mp3'

# async def main():
#   model = ModelConfig('asr-zh-en-std')
#   config = TranscriptionConfig(True, True)
#   c = t.Transcriber(yating_key, model, config)
#   multiple_tasks = []
#   for _ in range(2):
#     transcript = c.transcribe(audio)
#     task = transcript.wait_for_completion_async()
#     multiple_tasks.append(task)
    
#   for task in as_completed(multiple_tasks):    
#     print(task.result().transcript)

# asyncio.run(main())