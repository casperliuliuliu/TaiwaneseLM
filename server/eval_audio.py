from ailabs_asr.streaming import StreamingClient
import sys
from openai import OpenAI
from pydub import AudioSegment
desired_path = "D:/Casper/Other"
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)
from get_server_config import get_config
config = get_config()
yating_key = config['yating_key']
my_api_key = config["OPENAI_API_KEY"]

yating_result = ''
client = OpenAI(api_key=my_api_key)

def mp32wav(mp3_path,wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def asr_from_whisper(audio_path):
    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language="zh"
    # options = whisper.DecodingOptions()
    )
    print(transcription.text)
    return transcription.text

def asr_from_yating(audio_path):
    global yating_result
    yating_result = ''
    # init the streaming client
    asr_client = StreamingClient(yating_key)

    # start streaming with wav file
    asr_client.start_streaming_wav(
    pipeline='asr-zh-tw-std',
    # verbose=True,
    file=audio_path,
    # verbose=False, # enable verbose to show detailed recognition result
    on_processing_sentence=on_processing_sentence,
    on_final_sentence=on_final_sentence)

    return yating_result

def on_processing_sentence(message):
    global yating_result
    yating_result += message["asr_sentence"]
    print(f'hello: {message["asr_sentence"]}')

def on_final_sentence(message):
    global yating_result
    yating_result = message["asr_sentence"]
    print(f'world: {message["asr_sentence"]}')


def eval_yating(audio_path, text):
    pass

def eval_whisper(audio_path):  
    pass

if __name__ == "__main__":
    wav_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/吃葡萄不吐葡萄皮，不吃葡萄，到吐葡萄皮。.wav"
    wav_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/yating/example.mp3"
    # print("real resul:", asr_from_yating(wav_path))
    print("real resul:", asr_from_whisper(wav_path))